#!/usr/bin/env python3

"""
Challenge-2: Task Space Controller for 2DOF Planar Robot

References:
https://studywolf.wordpress.com/2013/09/02/robot-control-jacobians-velocity-and-force/
https://irislab.tech/course_robotics/lec22/osc.html

Objective:
- Maintain a constant velocity v* tangential to a surface.
- Maintain a constant force F* normal to the surface.

System Assumptions:
- A 2 DoF planar robot operating in 2D.
- Gravity is ignored.
- Joints are frictionless.
- Full feedback available: joint positions, velocities, and torques.

Choices:
- Operational Space Control (OSC) is a good choice for this application.
- Impendance controller
- Admittance controller

Intuitively: impedance controller acts like a spring (push me and i'll push back proportionally)
admittance controller is similar to a mass blob (push me and i'll move proportionally)
Both are good for compliance behavior. In our application with velocity and force control
for an application that too in cartesian space, we can use operational space control.

Control Approach: Operational Space Control (OSC)
- The velocity controller uses proportional control based on the difference between desired and actual end-effector velocity.
- The force controller applies derivative control on the desired vs. actual end-effector force.

Torque Feedback Role:
- Modeling inaccuracies
- Surface compliance
- External disturbances

By introducing torque feedback, we enable closed-loop force control:
- Estimate the actual end-effector force using the inverse of the Jacobian transpose applied to torque feedback.
- Compare it to the desired force.
- Update the torque command accordingly.
This makes the control loop more robust and responsive to environmental variations.


Can this work without torque feedback?
- Yes, for velocity-only tasks. The velocity control component does not require torque feedback.
- No, for accurate force regulation. Without torque or force sensing, you cannot close the loop on force, and the applied contact pressure may drift due to unmodeled dynamics or surface variation.

Design Principles:
1. Use of object-oriented design to encapsulate controller behavior.
2. Modular structure for maintainability and extensibility.
3. Easily extendable to robots with more degrees of freedom.
4. Numerical stability ensured using `numpy` safeguards and shape checks.
"""

# External

import numpy as np

# Internal

from chef_interview.utils import load_yaml


class TaskSpaceController2DOF:
    def __init__(self, controller_config: dict):
        """
        Initialize controller from config.

        Parameters:
        - controller_config: Dictionary containing controller parameters
            - link_lengths: List containing lengths of the 2 links
            - gains:
                - k_p: Gain for velocity control (tangential direction)
                - k_f: Gain for force control (normal direction)
        """

        assert (
            len(controller_config["link_lengths"]) == 2
        ), "Only 2 DOF planar robot supported."

        self._l1 = controller_config["link_lengths"][0]
        self._l2 = controller_config["link_lengths"][1]
        self._k_p = controller_config["gains"]["k_p"]
        self._k_f = controller_config["gains"]["k_f"]

    def forward_kinematics(self, q: np.ndarray) -> np.ndarray:
        """
        Compute end-effector position in 2D from joint angles.

        Returns:
        - end_effector_position: End-effector position (2x1)
        """

        theta1, theta2 = q
        x = self._l1 * np.cos(theta1) + self._l2 * np.cos(theta1 + theta2)
        y = self._l1 * np.sin(theta1) + self._l2 * np.sin(theta1 + theta2)
        return np.array([x, y])

    def jacobian(self, q: np.ndarray) -> np.ndarray:
        """
        Compute 2x2 Jacobian matrix of the end-effector.

        Returns:
        - J: Jacobian matrix (2x2)
        """

        theta1, theta2 = q
        J = np.zeros((2, 2), dtype=np.float64)
        J[0, 0] = -self._l1 * np.sin(theta1) - self._l2 * np.sin(theta1 + theta2)
        J[0, 1] = -self._l2 * np.sin(theta1 + theta2)
        J[1, 0] = self._l1 * np.cos(theta1) + self._l2 * np.cos(theta1 + theta2)
        J[1, 1] = self._l2 * np.cos(theta1 + theta2)
        return J

    def compute_control(
        self,
        q: np.ndarray,
        q_dot: np.ndarray,
        velocity_desired: np.ndarray,
        force_desired: np.ndarray,
        tau_measured: np.ndarray,
    ) -> np.ndarray:
        """
        Compute joint torques using hybrid velocity-force control in task space.

        Returns:
        - tau_command: Joint torque commands (2,)
        """

        J = self.jacobian(q)

        v_actual = np.matmul(J, q_dot)
        # Estimate actual end-effector force from joint torque feedback
        # Pinv to avoid division by zero for singular matrices (Not a big deal here)
        f_actual = np.matmul(np.linalg.pinv(J.T), tau_measured)
        # Task-space control law with feedback
        velocity_error = velocity_desired - v_actual  # Proportional control
        # Mass matrix is not considered here.
        force_error = force_desired - f_actual  # Derivative control
        u_task = self._k_p * velocity_error + self._k_f * force_error
        # Map to joint torques. Mass matrix is not considered here.
        tau_command = np.matmul(J.T, u_task)
        # Not a motion command that would have position, velocity, or acceleration.
        # It is a torque command that would be applied to the robot.
        return tau_command


def main():
    # Load controller config
    config = load_yaml()
    controller_config = config[config["controller_name"]]

    # Initialize controller
    controller = TaskSpaceController2DOF(controller_config)

    # Test the controller
    q = np.radians([30.0, 45.0])
    q_dot = np.array([0.0, 0.0])  # Assume stationary
    v_des = np.array([0.1, 0.0])  # Move along x-axis
    f_des = np.array([0.0, -5.0])  # Constant downward force

    tau = controller.compute_control(q, q_dot, v_des, f_des)
    print("Computed joint torques:", tau)


if __name__ == "__main__":
    main()
