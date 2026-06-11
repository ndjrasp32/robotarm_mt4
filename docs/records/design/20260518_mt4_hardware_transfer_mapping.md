# 2026-05-18 MT4 hardware transfer mapping 기록

## 결정

The IsaacLab task keeps the real MT4 URDF/USD asset, but the policy action space is now limited to the four arm-angle commands that can be sent to the real MT4 controller.

This avoids training a policy that controls simulation-only linkage joints that have no direct hardware command.

## 하드웨어 명령 action 벡터

| policy index | Isaac action joint | MT4 SDK angle field | deployment unit |
| --- | --- | --- | --- |
| 0 | `joint_1` | `X` | degrees |
| 1 | `joint_2_1` | `Y` | degrees |
| 2 | `joint_3` | `Z` | degrees |
| 3 | `gripper_body_joint` | `A` | degrees |

The action clamp still uses the URDF lower/upper limits in radians inside IsaacLab. Before sending to hardware, convert the four policy joint positions from radians to degrees.

Helper code for that conversion is in `source/mirobot_reach_direct/mt4_hardware_mapping.py`.

## 내부 simulation joint

| sim joint | current rule | why it is not a policy action |
| --- | --- | --- |
| `joint_2_2` | follows `joint_2_1` | parallel/support branch in the URDF tree |
| `joint_4` | held at `0.65` rad | passive/internal linkage pose pending calibration |
| `joint_l4` | held at `0.35` rad | passive/internal linkage pose pending calibration |

## 이식 주의점

The local MT4 CAD/URDF has extra revolute joints for the linkage. URDF represents a tree, so a closed/parallel linkage must be approximated as branches or internal joints. The current mapping is intentionally conservative: train only commands that the real arm can receive, while keeping the full MT4 asset for geometry and collision behavior.

Before deploying a trained policy to the real arm, calibrate or derive the exact passive-linkage relation for `joint_4` and `joint_l4`. If those joints are not constant on the physical mechanism, replace `MirobotReachPregraspEnv._action_to_sim_joint_pos()` with the measured relation instead of adding those joints back to the policy action vector.

## 확인한 참고자료

- 과거 로컬 MT4 SDK 참고 경로: `vendor/WLKATA-Python-SDK-wlkatapython/MT4_robot/MT4_UART.py`. 이 경로의 `writeangle(position, x, y, z, a)` 형태를 기준으로 mapping을 잡았다.
- 과거 로컬 MT4 CAD 참고 경로: `vendor/MT4-STL/` 아래 README. Omniverse/Isaac Sim용 MT4 CAD/STL/STEP asset 설명으로 사용했다.
- WLKATA MT4 public product material describes MT4 as a 4+1 DoF / 4-axis robotic arm: https://www.wlkata.com/pages/mt4-robotic-arm
- WLKATA `RosForMirobot-master` is a separate Mirobot ROS package and uses `mirobot_urdf_2`; it is useful as a comparison, but it is not the MT4 CAD asset currently in this repo: https://github.com/wlkata/RosForMirobot-master
