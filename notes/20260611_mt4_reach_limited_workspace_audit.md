# 2026-06-11 MT4 Reach-Limited Workspace Audit

## Purpose

Define the first MT4 coordinate workspace from actual simulated gripper-center reach, not from the wider student asset workspace. This is still IsaacLab simulation only. No real robot motion was executed.

## Reach Sampling Result

Headless IsaacLab sampled 65,536 random poses inside the four hardware-facing action joint limits:

| item | value |
| --- | --- |
| action joints | `joint_1`, `joint_2_1`, `joint_3`, `gripper_body_joint` |
| joint lower | `(-1.57, -1.00, 0.00, -1.57)` |
| joint upper | `(1.57, 1.57, 1.57, 1.57)` |
| sampled gripper center min | `(-0.142064, -0.186312, -0.063900)` |
| sampled gripper center max | `(0.207345, 0.186865, 0.323081)` |
| sampled gripper center mean | `(0.016088, -0.001077, 0.073129)` |
| old Stage 0 workspace | `center=(0.270, 0.000, 0.140), size=(0.180, 0.220, 0.160)` |
| old workspace sample hit rate | `0.004639` |

The old Stage 1 student workspace `center=(0.305, 0.000, 0.205), size=(0.090, 0.140, 0.090)` is outside this MT4 asset's sampled front reach because sampled `x_max` was about `0.207 m`.

## MT4 Workspace Baseline

Use this top-down reach-limited workspace for Stage 0 workspace-entry, Stage 1 3x3 plane curriculum, and Stage 2 27-cell volume curriculum:

| item | value |
| --- | --- |
| center | `(-0.078000, 0.000000, 0.103000)` |
| size | `(0.045000, 0.095000, 0.055000)` |
| min | `(-0.100500, -0.047500, 0.075500)` |
| max | `(-0.055500, 0.047500, 0.130500)` |
| safety margin basis | `10 mm` from sampled robust envelope before final box selection |
| Stage 1 3x3 plane x | `-0.078000` |
| Stage 1 3x3 plane y/z cell size | `(0.031667, 0.018333)` |
| Stage 2 3x3x3 cell size | `(0.015000, 0.031667, 0.018333)` |

This is deliberately smaller than the student workspace. The x-axis is the limiting dimension for this MT4 USD/URDF mapping. A second top-down audit showed that the previous positive-x box was reachable only without the required downward approach; `inside_and_top_down_ready_rate` was `0.000000`.

## Stage 1 3x3 Plane Region Centers

Stage 1 fixes the entry x position at the workspace center and learns only the y/z camera-region match first.

| region | x | y | z |
| ---: | ---: | ---: | ---: |
| 1 | -0.078000 | -0.031667 | 0.084667 |
| 2 | -0.078000 | 0.000000 | 0.084667 |
| 3 | -0.078000 | 0.031667 | 0.084667 |
| 4 | -0.078000 | -0.031667 | 0.103000 |
| 5 | -0.078000 | 0.000000 | 0.103000 |
| 6 | -0.078000 | 0.031667 | 0.103000 |
| 7 | -0.078000 | -0.031667 | 0.121333 |
| 8 | -0.078000 | 0.000000 | 0.121333 |
| 9 | -0.078000 | 0.031667 | 0.121333 |

## Stage 2 27 Region Centers

Region indexing follows the environment code: x column changes first, then y row, then z depth.

| region | x | y | z |
| ---: | ---: | ---: | ---: |
| 1 | -0.093000 | -0.031667 | 0.084667 |
| 2 | -0.078000 | -0.031667 | 0.084667 |
| 3 | -0.063000 | -0.031667 | 0.084667 |
| 4 | -0.093000 | 0.000000 | 0.084667 |
| 5 | -0.078000 | 0.000000 | 0.084667 |
| 6 | -0.063000 | 0.000000 | 0.084667 |
| 7 | -0.093000 | 0.031667 | 0.084667 |
| 8 | -0.078000 | 0.031667 | 0.084667 |
| 9 | -0.063000 | 0.031667 | 0.084667 |
| 10 | -0.093000 | -0.031667 | 0.103000 |
| 11 | -0.078000 | -0.031667 | 0.103000 |
| 12 | -0.063000 | -0.031667 | 0.103000 |
| 13 | -0.093000 | 0.000000 | 0.103000 |
| 14 | -0.078000 | 0.000000 | 0.103000 |
| 15 | -0.063000 | 0.000000 | 0.103000 |
| 16 | -0.093000 | 0.031667 | 0.103000 |
| 17 | -0.078000 | 0.031667 | 0.103000 |
| 18 | -0.063000 | 0.031667 | 0.103000 |
| 19 | -0.093000 | -0.031667 | 0.121333 |
| 20 | -0.078000 | -0.031667 | 0.121333 |
| 21 | -0.063000 | -0.031667 | 0.121333 |
| 22 | -0.093000 | 0.000000 | 0.121333 |
| 23 | -0.078000 | 0.000000 | 0.121333 |
| 24 | -0.063000 | 0.000000 | 0.121333 |
| 25 | -0.093000 | 0.031667 | 0.121333 |
| 26 | -0.078000 | 0.031667 | 0.121333 |
| 27 | -0.063000 | 0.031667 | 0.121333 |

## Camera Calibration Flow

Initial simulation flow:

1. Treat the MT4 base frame as the workspace frame.
2. Define fixed body cameras at `left_camera_pos=(0.035, -0.255, 0.225)` and `right_camera_pos=(0.035, 0.255, 0.225)`.
3. Aim both body cameras at the workspace center `(-0.078, 0.000, 0.103)`.
4. Project target and gripper center into left/right normalized image coordinates.
5. Triangulate stereo rays back into the MT4 base frame.
6. Clamp the estimated target to the workspace min/max bounds.
7. Convert the clamped target to one of the 9 plane region IDs first, then one of the 27 volume region IDs after depth expansion.
8. Use the gripper camera projection only for close-range final relative pose, depth, and visibility.
9. Mount the gripper camera in simulation as a 45-degree inside-looking camera: body-frame forward axis `(0.70710678, 0.0, -0.70710678)`, i.e. `(+X, 0, -Z)` from outside toward the gripper/target side.
10. Include the dynamic gripper-camera forward vector in policy observations so arm rotation changes the learned camera-view state.

Real camera flow later:

1. Capture a checkerboard or AprilTag board at known points in the MT4 workspace.
2. Estimate each camera intrinsic matrix and distortion coefficients.
3. Estimate each camera-to-base extrinsic transform.
4. Convert detected target pixels to rays, triangulate body stereo rays, then transform to MT4 base coordinates.
5. Reject targets outside the workspace min/max bounds.
6. Map accepted targets to the 9 plane region IDs first, then the 27 volume region IDs after depth expansion.
7. Compare camera-estimated coordinates against simulation/internal coordinates before any real robot motion.

## Decision

Stage 1 should not jump directly to the old student 27-cell box. Re-run Stage 0 workspace-entry with this MT4 reach-limited box first, stabilize the 9-cell plane, and only then expand depth into the 27-cell volume.
