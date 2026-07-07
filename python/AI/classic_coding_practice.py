#! /usr/bin/python3

"""
NOTES
Search pattern: frontier holds states to explore,
    visited prevents repeats, parent reconstructs path.
"""

import numpy as np
from functools import cache


def get_neighbors(grid: list | np.ndarray, cell: tuple | list):
    if isinstance(grid, list):
        dim = len(grid)
    elif isinstance(grid, np.ndarray):
        dim = grid.shape[0]
    neighbors = []
    for deltas in ((1, 1), (1, -1), (-1, -1), (-1, -1)):
        if (
            cell[0] + deltas[0] >= 0
            and cell[1] + deltas[1] >= 0
            and cell[0] + deltas[0] < dim
            and cell[1] + deltas[1] < dim
        ):
            neighbors.append((cell[0] + deltas[0], cell[1] + deltas[1]))
    return neighbors


def two_sum_indices(nums, target):
    """
    Think of this problem as given a number, find the sum - number in rest of the list
    Heuristic:
    - potentially sort in ascending order. Then use two pointer approach
    say left pointer is X value and right is Y
    right pointer moves until X + Y < sum meaning X must increase to bring the sum back
    """

    sorted_list = sorted(nums)
    ptr_a = 0
    ptr_b = len(sorted_list) - 1
    combinations = []
    while ptr_b > ptr_a:
        if sorted_list[ptr_a] + sorted_list[ptr_b] == target:
            combinations.append((ptr_a, ptr_b))
        if sorted_list[ptr_a] + sorted_list[ptr_b] < target:
            ptr_a += 1
        ptr_b -= 1
    return combinations


def bfs_path(grid, start, goal):
    """
    FIFO
    """

    def get_children(curr):
        pass

    qu = list()
    is_visited = set()  # Make this Nd based on grid shape or a hash map
    qu.append((start))
    while len(qu) > 0:
        curr = qu.pop()
        is_visited.add(curr)
        for child in get_children(curr):
            if child not in is_visited:
                qu.append(child)


def fibonnacci_iterative(n):
    if n < 0:
        raise ValueError("Invalid n")
    if n <= 1:
        return n
    n_1 = 0
    n_2 = 1
    for _ in range(2, n + 1):
        new_sum = n_1 + n_2
        n_1 = n_2
        n_2 = new_sum
    return n_2


@cache
def fibonacci_recursive(n):
    if n < 0:
        raise ValueError("Invalid n")
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def transform_points(T, points):
    """
    T is homogeneous matrix [4,4]
    points: [N,3]
    """
    tf_points = T @ np.hstack((points, np.ones(shape=(points.shape[0], 1)))).T
    return tf_points[:3, :].T


if __name__ == "__main__":
    print(fibonnacci_iterative(20))
    print(fibonacci_recursive(20))
