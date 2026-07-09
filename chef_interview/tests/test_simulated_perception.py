#!/usr/bin/env python3

"""
Unit tests for simulated perception.

What are we checking for?
1. Image sizes, data type, shape, values, etc.
2. NaN, None, Inf, etc.
3. Multi-processing and asyncio deadlocks or race conditions.
4. Trigger time synchronization.
5. Input and output are consistent.
6. Transformations are correct. i.e. image to cloud, cloud to world, etc.
7. Check for camera intrinsics and extrinsics- If they are correct,
        inverse should be correct.
8. Check if x0,y0 = 0,0 gives a ray direction of 0,0,1.
9. Check handling of invalid data types and depth values.


Implementation:
1. Basic unit tests. Should be expanded and made more comprehensive. Wrote few for example.
2. Use AI (chatgpt) for numpy optimizations instead of for loops and docstrings.
3. Add logging.
4. Use strategy from experience and design from first principles.
5. Have the ability to add new cameras and sensors using abstraction.
6. Check behavior of the code with different inputs.
7. Use concepts from OOP and design patterns.
"""

# External

import pytest
import numpy as np

# Internal

from chef_interview.utils import load_yaml
from chef_interview.simulated_perception import SimulatedPerception


@pytest.fixture
def perception():
    """Create SimulatedPerception instance."""
    config = load_yaml()
    camera_config = config[config["camera_name"]]
    return SimulatedPerception(camera_config)


def test_principal_point_ray(perception):
    """Test if principal point (x0,y0) gives (0,0,1) ray."""
    # Shape is (Y, X, channels) = (height, width, 3)
    rgb = np.zeros((480, 640, 3), dtype=np.float64)  # Simple RGB image
    x0 = perception._camera_config["intrinsics"]["x0"]
    y0 = perception._camera_config["intrinsics"]["y0"]

    rays = perception.image_to_ray(rgb)
    principal_point_idx = int(y0) * 640 + int(x0)

    np.testing.assert_array_almost_equal(
        rays[principal_point_idx], np.array([0, 0, 1]), decimal=3
    )


def test_cloud_transformations(perception):
    """Test point cloud generation and transformations."""
    perception._world_T_camera = np.eye(4)

    # Create test RGBD with known depth
    test_rgbd = np.zeros((10, 10, 4))
    test_rgbd[:, :, 3] = 2.0  # 2 meter depth

    # Test camera frame cloud
    cloud_camera = perception.image_to_cloud(test_rgbd)
    assert cloud_camera.shape == (100, 3)

    # Test world frame transformation
    cloud_world = perception.image_to_cloud_world(test_rgbd)
    assert cloud_world.shape == (100, 3)
    assert np.allclose(cloud_world[:, 2], 2.0)


def test_trigger_camera_output(perception):
    """Test camera trigger output format and synchronization."""
    rgbd = perception.trigger_camera()

    # Check basic properties
    assert len(rgbd.shape) == 3
    assert rgbd.shape[2] == 4

    # Check RGB values
    assert rgbd.dtype == np.float64
    assert np.all(rgbd[..., :3] >= 0)  # RGB values non-negative
    assert np.all(rgbd[..., :3] <= 255)  # RGB values <= 255

    # Check depth values
    assert np.all(rgbd[..., 3] >= 0)  # Depth values non-negative
    assert np.all(rgbd[..., 3] <= 10.0)  # Reasonable depth range

    # Check for invalid values
    assert not np.any(np.isnan(rgbd))
    assert not np.any(np.isinf(rgbd))
