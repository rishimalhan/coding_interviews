#!/usr/bin/env python3

"""
Discussions / Notes

Reference: https://towardsdatascience.com/what-are-intrinsic-and-extrinsic-camera-parameters-in-computer-vision-7071b72fb8ec/

1) Simulated Perception
# Extrinsics:
-> world_frame: A reference frame used for defining the geometric transformations/relationships with each other. Also known as global cartesian coordinate system in this code base.
-> base_frame: depth optical frame or camera frame about which RGB and depth data recorded by the camera sensor is defined.
    - X1, Y1, Z1 -> translation components for the base_frame
    - R1 -> rotation matrix 3X3 of the base_frame
    - X1, Y1, Z1, and R1 combined are also called the camera extinsics or the external parameters. They define the localization of the camera in real world.

# Intrinsics:
-> (x0, y0) is the point where optical line hits the image plane (ideally same as optical center in 3D, however, manufacturing defects exist)
    - Above is representative of a simple pinhole camera model where external light passes through a pinhole and makes an inverted image on the image plane. This point through which light passes is optical point and line from this point along camera length to image plane is what is discussed.
-> fx and fy are the pixel per normalized unit in X and Y axes of image
    - e.g. 1300 pixels per meter
    - However, total image width could be > fx e.g. 2100 pixels
    - Image width and height represent sensor resolution VS fx and fy focal lengths define how 3D gets mapped to 2D
    - In other words, it defines how much zoom/magnification the camera has
    - Farther away a point in camera view, smaller the image or closer the pixel to x0,y0 center and vice versa
    - fx or fy < Width: Possible. Just means zoomed in

# Pixelated coordinates:
-> Extrinsics and intrinsics combined transform the world coordinates that camera sees to the pixelated coordinates relative to x0 and y0.
    - x = f(P, X), where x is 2D pixel coordinates and X is 3D point
    - P = K [R | t]
    - P is 11 DOF combined Extrinsics (6DOF) and Intrinsics (5DOF) matrix
-> Let's not forget skew. For analog cameras skew is important as
-> u and v represent coordinates in image. Corner = <0,0>
    - For RGB- u and v are color values
    - For depth- u and v are depth value
    - For RGBD- u and v are both
-> FOV or field of view is the angle at which camera can see
    - FOV = 2 * arctangent( (W / 2) / f )
-> Most modern cameras skew is well aligned. so s -> 0

K = | fx   s   x0 |
    |  0  fy   y0 |
    |  0   0    1 |


# Challenge-1

1. Camera pixel coordinates into homogenous coordinates

Cannot recover Z from this data. RGB does not give any 3D position. We cannot recover point in 3D without depth data. Hence we use a concept of normalized camera coordinates where pixels are normalized to the focal length.

Ask here:
Given a pixel location (u, v), convert it to a homogeneous 3D ray direction in the camera frame, under the assumption that the point lies along that ray starting at the optical center

point_normalized or direction = K_inv @ <u, v, 1>

# Then if Z is known:
P_camera  or [X, Y, Z] = direction[:2] * Z, Z
P_world = T_wc @ P_camera

2. With Depth:
Z=Z from depth map

# Assumptions:
- Intel realsense is a stereo vision camera
- Skew for digital camera is usually close to 0


# Implementation:

1. Use concepts from OOP and design patterns.
2. Modularity and multiprocessing helps with load balancing and parallelization.
3. Make this functional and robust then focus on performance.
4. Have the ability to add new cameras and sensors using abstraction.
5. Check behavior of the code with different inputs.
6. Use strategy from experience and design from first principles.
7. Use AI (chatgpt) for debugging, numpy optimizations instead of for loops and docstrings.
8. Add logging.
9. Add try-except blocks for error handling.
"""

# External

import os
import numpy as np

# Internal

from chef_interview.utils import ROOT, load_yaml


class SimulatedPerception:

    def __init__(self, camera_config: dict):
        self._camera_config = camera_config
        self._world_T_camera = np.eye(4, dtype=np.float64)
        self._world_T_camera[:3, :3] = np.array(
            self._camera_config["extrinsics"]["rotation"], dtype=np.float64
        )
        self._world_T_camera[:3, 3] = np.array(
            self._camera_config["extrinsics"]["translation"], dtype=np.float64
        )
        self._local_path_to_image = self._camera_config["local_path_to_image"]

    def image_to_ray(self, image_rgb: np.ndarray) -> np.ndarray:
        """
        Given an MxNx3 RGB image and intrinsics, return (M*N)x3 array

        Steps:
        1. Convert pixel coordinates (u,v) to normalized image coordinates (x',y'):
           x' = (u - cx) / fx
           y' = (v - cy) / fy
        2. Form homogeneous coordinates (x', y', 1)

        Returns:
        - rays: np.ndarray of shape (M*N, 3), each row is a vector [X,Y,1] in camera frame with Z = 1
        """
        H, W, _ = image_rgb.shape

        # Get camera parameters
        fx = self._camera_config["intrinsics"]["fx"]
        fy = self._camera_config["intrinsics"]["fy"]
        cx = self._camera_config["intrinsics"]["x0"]
        cy = self._camera_config["intrinsics"]["y0"]

        # Create pixel coordinate grid
        u_coords = np.arange(W, dtype=np.float64)
        v_coords = np.arange(H, dtype=np.float64)
        u_coords, v_coords = np.meshgrid(u_coords, v_coords)

        # Convert to normalized image coordinates with Z = 1
        x_prime = (u_coords - cx) / fx
        y_prime = (v_coords - cy) / fy

        # Stack into homogeneous coordinates
        return np.stack(
            [x_prime.ravel(), y_prime.ravel(), np.ones_like(x_prime.ravel())], axis=1
        )

    def image_to_cloud(self, image_rgbd: np.ndarray) -> np.ndarray:
        """
        Given an MxNx4 RGBD image and intrinsics, return (M*N)x3 array of 3D points.
        Point cloud is in the camera frame.

        Returns:
        - cloud: np.ndarray of shape (M*N, 3)
        """

        depths = image_rgbd[:, :, 3].reshape(-1)
        # Mask out invalid depths (e.g., 0, NaN, or inf)
        valid = (depths > 0) & np.isfinite(depths)
        # Get corresponding rays and valid depths only
        rays = self.image_to_ray(image_rgbd[:, :, :3])
        cloud = np.zeros_like(rays)
        cloud[valid] = rays[valid] * depths[valid][:, np.newaxis]
        return cloud

    def image_to_cloud_world(self, image_rgbd: np.ndarray) -> np.ndarray:
        # ToDo: This function still returning division by zero errors. Need to fix.

        """
        Given an MxNx4 RGBD image and intrinsics, return (M*N)x3 array of 3D points.
        Point cloud is in the world frame.

        Returns:
        - cloud_world: np.ndarray of shape (M*N, 3)
        """

        cloud_camera = self.image_to_cloud(image_rgbd)
        # Add homogeneous coordinate
        cloud_camera_h = np.hstack(
            [cloud_camera, np.ones((cloud_camera.shape[0], 1), dtype=np.float64)]
        )
        cloud_world = np.matmul(self._world_T_camera, cloud_camera_h.T).T
        return cloud_world[:, :3]

    def trigger_camera(self) -> np.ndarray:
        #  ToDo: Synchronize with actual camera trigger. Use Asyncio and multiprocessing.

        """
        Generate a sample RGBD image from file.
        Replace this with actual camera trigger.

        Returns:
        - rgbd_image: np.ndarray of shape (height, width, 4) where:
            - channels 0-2 are RGB (0-255)
            - channel 3 is depth in meters (0.5m to 3m)
        """

        # Read an image from file
        return np.load(os.path.join(ROOT, self._local_path_to_image)).astype(np.float64)


def main():
    # Load camera config
    config = load_yaml()
    camera_config = config[config["camera_name"]]

    # Initialize perception
    perception = SimulatedPerception(camera_config)

    # Trigger camera and get RGBD image
    rgbd = perception.trigger_camera()
    print(f"RGBD image shape: {rgbd.shape}")

    # Convert to world point cloud
    cloud_world = perception.image_to_cloud_world(rgbd)
    print(f"World point cloud shape: {cloud_world.shape}")
    print(f"Sample points (first 3):\n{cloud_world[:3]}")


if __name__ == "__main__":
    main()
