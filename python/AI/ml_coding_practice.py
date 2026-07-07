#! /usr/bin/python3

"""
NOTES:
For two 1D vectors @ will do a dot product and * is element wise multiplication

Need batched column vector?
(B, D) -> (B, D, 1)
Use x[..., None] or x.unsqueeze(-1)
Broadcasting aligns dims from right: (B, D) * (D,) -> (B, D).
expand makes broadcasting explicit: (1, D).expand(B, -1) -> (B, D).
Use -1 in expand to keep that dimension unchanged.

Planar FK:
Link i angle = theta[0] + ... + theta[i], not just theta[i].
Use torch ops for tensor math so code can batch, run on GPU, and keep gradients.

Attention:
Q @ K.T -> scores shaped (B, Tq, Tk): every query scores every key.
softmax over keys dim: each query chooses where to look.
Attention memory grows with B * heads * Tq * Tk, not just embedding dim.
fp32 uses 4 bytes/number, fp16/bfloat16 use 2 bytes/number.
Multi-head attention is parallel attention: (B, H, T, D) runs H heads at once.
Use transpose(-2, -1) for attention so it works for single or multi-head.
Attention compute: QK.T and weights@V dominate.

Causal Mask:
T = 4

causal_mask = torch.triu(
    torch.ones(T, T),
    diagonal=1
).bool()

print(causal_mask)

K-Means (NumPy / PyTorch):
Goal: partition N points with D features into k clusters.
Input points have shape (N, D); centroids have shape (k, D).

Interview thought process:
1. Initialize k centroids by sampling k different input points.
2. Assignment step: compute every point-to-centroid distance -> (N, k).
3. Choose the closest centroid for each point with argmin -> labels (N,).
4. Update step: sum points by label and divide by cluster counts.
5. If a cluster has zero points, reinitialize it instead of dividing by zero.
6. Stop when centroid movement is below tolerance or max_iter is reached.

Useful NumPy functions:
- np.random.choice(..., replace=False): sample initial centroid indices.
- points[:, np.newaxis] - centroids: broadcast to pairwise differences (N, k, D).
- np.linalg.norm(..., axis=2): reduce feature differences to distances (N, k).
- np.argmin(distances, axis=1): assign each point to a cluster.
- np.add.at(sums, labels, points): accumulate point sums by repeated labels.
- np.bincount(labels, minlength=k): count points in every cluster.
- counts[:, np.newaxis]: reshape counts from (k,) to (k, 1) for broadcasting.

Useful PyTorch functions:
- torch.randperm(N)[:k]: sample k distinct initial point indices.
- torch.cdist(points, centroids): pairwise distances with shape (N, k).
- torch.argmin(distances, dim=1): produce cluster labels with shape (N,).
- sums.index_add_(0, labels, points): accumulate point sums by cluster label.
- torch.bincount(labels, minlength=k): count points assigned to each cluster.
- counts.clamp_min(1): prevent division by zero before repairing empty clusters.
- counts.unsqueeze(1): reshape (k,) to (k, 1) for feature-wise broadcasting.
- torch.linalg.vector_norm(new - old): measure total centroid movement.
- torch.no_grad(): avoid building an autograd graph for this iterative algorithm.

Complexity per iteration: O(N * k * D) compute and O(N * k) distance memory.
K-means can converge to a local optimum, so initialization and multiple restarts matter.
"""

import math
import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

DEVICE = "cuda"
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#### Workspace Vel ####


def jacobian_velocity(J: torch.Tensor, qdot: torch.Tensor) -> torch.Tensor:
    """
    Each row of Jacobian gets multiplied by each column of qdot
    qdot had only one column so size of (N, )
    J has three rows and N columns
    Each row in J is workspace translation i.e. X, Y, Z
    Each column in J implies sensitivity of translation with each joint
    So each row of output is SUM( sensitivity * corresponding joint )
    """

    workspace_vel = torch.empty(size=(J.shape[0],), dtype=J.dtype, device=J.device)
    logger.info(f"Inputs: Jacobian: {J}, Qdot: {qdot}\n\n")
    logger.info(f"Workspace velc before: {workspace_vel}")
    for idx, grad_coord in enumerate(J):
        workspace_vel[idx] = grad_coord @ qdot
    logger.info(f"Workspace velc after: {workspace_vel}")
    return workspace_vel


def batched_jacobian_velocity(J: torch.Tensor, qdot: torch.Tensor) -> torch.Tensor:
    workspace_vel = torch.empty(
        size=(J.shape[0], J.shape[1]), dtype=J.dtype, device=J.device
    )
    for idx, (jac, qd) in enumerate(zip(J, qdot)):
        workspace_vel[idx] = jacobian_velocity(jac, qd)
    return workspace_vel


def batched_jacobian_velocity_vectorized(
    J: torch.Tensor, qdot: torch.Tensor
) -> torch.Tensor:
    """
    J is tensor of Bx3x6 and qdot is tensor of Bx6
    Goal is matrix math where each batch element goes through SUM( sensitivity * corresponding joint )
    Pytorch treats matrix multiplication between tensors from last dimensions
    i.e. Bx3x6 and Bx6x1 will be multiplied as for each b in B, 3x6 @ 6x1 which gives Bx3
    Math is:
    for b in B:
        SUM( sensitivity * corresponding joint )
    J @ qdot[..., None] returns a Bx3x1. Squeeze removes particular dim
    """
    logger.info(f"Inputs: Jacobian: {J}, Qdot: {qdot}\n\n")
    workspace_vel = (J @ qdot.unsqueeze(-1)).squeeze(-1)
    logger.info(f"Workspace velc: {workspace_vel}")
    return workspace_vel


#### FK 6DOF Planar ####


def fk_planar_6dof(thetas: torch.Tensor, link_lengths: torch.Tensor) -> torch.Tensor:
    transforms = torch.empty(
        size=(thetas.size(0), 2), dtype=thetas.dtype, device=thetas.device
    )
    running_angle = 0.0
    for idx, (theta, link_length) in enumerate(zip(thetas, link_lengths)):
        running_angle += theta
        transforms[idx] = torch.tensor(
            [
                link_length * torch.cos(running_angle),
                link_length * torch.sin(running_angle),
            ]
        )
    return torch.sum(transforms, dim=0)


def batched_fk_planar_6dof_vectorized(
    thetas: torch.Tensor, link_lengths: torch.Tensor
) -> torch.Tensor:
    """
    thetas is BxDOF and link_lengths is DOFx
    """
    cumsum = torch.cumsum(thetas, dim=1)  # B x DOF
    local_transforms = torch.stack(
        (link_lengths * cumsum.cos(), link_lengths * cumsum.sin()),
        dim=2,
    )  # Bx6x2 i.e. X, Y coordinates
    return local_transforms.sum(dim=1)  # Bx2


#### Scaled Dot Product Attention ####


def scaled_dot_product_attention(
    Q: torch.Tensor, K: torch.Tensor, V: torch.Tensor, mask: torch.Tensor = None
):
    """
    Q.shape == (B, Tq, Dh)
    K.shape == (B, Tk, Dh)
    V.shape == (B, Tk, Dv)
    out.shape == (B, Tq, Dv)

    Idea of attention is that every query token attens to key token
    and we compute a score. Naturally this score will be TxT square matrix
    Q: BxTxdh @ BxdhxT So each ij element SUM( dh_q * dh_k ) over all row/col
    """

    scores = Q @ K.transpose(1, 2)  # BTT
    scores /= math.sqrt(K.shape[-1])
    if mask is not None:
        scores = scores.masked_fill(mask, value=float("-inf"))
    weights = torch.softmax(scores, dim=-1)
    return weights @ V  # BTdv


#### Multi head attention ####


class MultiHeadSelfAttention(nn.Module):
    def __init__(
        self,
        d_model: int,
        num_heads: int,
        dropout: float = 0.8,
    ):
        super().__init__()

        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        self._d_model = d_model
        self._num_heads = num_heads
        self._d_head = int(self._d_model / self._num_heads)

        self._q_projection = nn.Linear(in_features=d_model, out_features=d_model).to(
            DEVICE
        )
        self._k_projection = nn.Linear(in_features=d_model, out_features=d_model).to(
            DEVICE
        )
        self._v_projection = nn.Linear(in_features=d_model, out_features=d_model).to(
            DEVICE
        )

        self._out_projection = nn.Linear(d_model, d_model).to(DEVICE)

        self._dropout = nn.Dropout(p=dropout).to(DEVICE)

    def forward(self, x: torch.Tensor, mask: torch.Tensor = None):
        batch_size, seq_length, _ = x.shape

        Q = self._q_projection(x)  # B, T, d_model
        K = self._k_projection(x)  # B, T, d_model
        V = self._v_projection(x)  # B, T, d_model

        # B x H x T x d_head
        Q = Q.view(batch_size, seq_length, self._num_heads, self._d_head).transpose(
            -3, -2
        )
        K = K.view(batch_size, seq_length, self._num_heads, self._d_head).transpose(
            -3, -2
        )
        V = V.view(batch_size, seq_length, self._num_heads, self._d_head).transpose(
            -3, -2
        )

        # B x H x T x T
        scaled_dot = Q @ K.transpose(-2, -1)
        scaled_dot /= math.sqrt(self._d_head)

        # Mask
        if mask is not None:
            scaled_dot = torch.masked_fill(
                input=scaled_dot, mask=mask == 0, value=float("-inf")
            )

        # Weights B x H x T x T
        weights = scaled_dot.softmax(dim=-1)
        weights = self._dropout(weights)

        # Concatenate B x H x T x d_head
        context = torch.matmul(weights, V)
        context = context.transpose(-3, -2).contiguous()
        context = context.view(batch_size, seq_length, self._d_model)

        # Output
        return self._out_projection(context)


def k_means(
    points: np.array,
    max_iter: int = 1000,
    k: int = 3,
    seed: int = 42,
    tol: float = 1e-3,
):
    np.random.seed(seed)
    prev_centroids = np.empty(shape=(k, points.shape[1]))
    for iter in range(max_iter):
        if iter == 0:
            # random sample k centroids
            centroids = points[np.random.choice(points.shape[0], k, replace=False)]
        else:
            distances = np.linalg.norm(points[:, np.newaxis] - centroids, axis=2)
            labels = np.argmin(distances, axis=1)  # N
            centroids = np.zeros(shape=(k, points.shape[1]))
            np.add.at(centroids, labels, points)
            counts = np.bincount(labels, minlength=k)  # k,
            centroids /= counts[:, np.newaxis]
        if iter > 0 and np.linalg.norm(prev_centroids - centroids) < tol:
            break
        prev_centroids = centroids
    return centroids


@torch.no_grad()
def k_means_torch(
    points: torch.Tensor,
    max_iter: int = 1000,
    k: int = 3,
    seed: int = 42,
    tol: float = 1e-3,
) -> torch.Tensor:
    if points.ndim != 2:
        raise ValueError("points must have shape (num_points, num_features)")
    if not points.is_floating_point():
        raise TypeError("points must be a floating-point tensor")
    if not 1 <= k <= points.shape[0]:
        raise ValueError("k must be between 1 and the number of points")

    generator = torch.Generator(device=points.device).manual_seed(seed)
    initial_indices = torch.randperm(
        points.shape[0], generator=generator, device=points.device
    )[:k]
    centroids = points[initial_indices].clone()

    for _ in range(max_iter):
        distances = torch.cdist(points, centroids)  # (N, k)
        labels = torch.argmin(distances, dim=1)  # (N,)

        centroid_sums = torch.zeros_like(centroids)
        centroid_sums.index_add_(0, labels, points)
        counts = torch.bincount(labels, minlength=k)

        new_centroids = centroid_sums / counts.clamp_min(1).unsqueeze(1)

        empty_clusters = counts == 0
        num_empty = int(empty_clusters.sum().item())
        if num_empty:
            replacement_indices = torch.randperm(
                points.shape[0], generator=generator, device=points.device
            )[:num_empty]
            new_centroids[empty_clusters] = points[replacement_indices]

        shift = torch.linalg.vector_norm(new_centroids - centroids)
        centroids = new_centroids
        if shift < tol:
            logger.info("Converged...")
            break
    return centroids


if __name__ == "__main__":

    #### Workspace Vel ####
    batch_J = torch.rand(size=(100, 3, 6))
    batch_qdot = torch.rand(size=(100, 6))
    # batched_jacobian_velocity_vectorized(batch_J, batch_qdot)

    #### FK 6DOF Planar ####
    theta = torch.zeros(size=(6,))
    links = torch.ones(size=(6,))
    # expect [6, 0]
    # fk = fk_planar_6dof(theta, links)
    # logger.info(f"FK: {fk}")

    theta = torch.tensor([torch.pi / 2, 0, 0, 0, 0, 0])
    # expect [0, 6]
    # fk = fk_planar_6dof(theta, links)
    # logger.info(f"FK: {fk}")

    thetas = torch.zeros(size=(100, 6))
    # fks = batched_fk_planar_6dof_vectorized(thetas, links)
    # logger.info(f"FK: {fks}")

    #### Scaled Dot Product Attention ####

    # B, Tq, Tk, Dh, Dv = 100, 30, 30, 256, 256
    # Q = torch.rand(B, Tq, Dh).to(device="cuda")
    # K = torch.rand(B, Tk, Dh).to(device="cuda")
    # V = torch.rand(B, Tk, Dv).to(device="cuda")
    # mask = torch.triu(
    #     input=torch.ones(Tq, Tk, dtype=torch.bool, device=Q.device), diagonal=1
    # )
    # out = scaled_dot_product_attention(Q, K, V, mask=mask)
    # logger.info(out.shape)

    #### Multi head attention ####

    # B = 2
    # T = 5
    # D = 32
    # H = 4

    # x = torch.randn(B, T, D).to(DEVICE)
    # mha = MultiHeadSelfAttention(d_model=D, num_heads=4)
    # out = mha(x)

    # logger.info(f"Output shape: {out.shape}")

    #### K- Means ####

    points = np.random.normal(loc=0, scale=1.0, size=(1000, 10))
    centroids = k_means(points=points, k=3)
    logger.info(f"Centroids: {centroids}")
    centroids = k_means_torch(
        points=torch.randn(size=(10000000, 100), device="cuda"), k=20, max_iter=10000
    )
    logger.info(f"Centroids: {centroids}")
