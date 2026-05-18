# mirobot_arm_test

실제 WLKATA Mirobot/MT4 URDF에서 변환한 Isaac Sim USD asset을 기준으로 IsaacLab direct RL task를 시작하는 repo입니다.

## 현재 asset

- 원본 ROS2 xacro: `/home/spark-robotics/work/robotarm/mt4_ws/src/complex_mobile_robot_description/urdf/complex_mobile_robot_description.urdf.xacro`
- Isaac용 clean URDF 복사본: `assets/urdf/mirobot_wlkata_isaac_clean.urdf`
- Isaac용 USD 복사본: `assets/usd/mirobot_real/mt4_from_wlkata_isaac_clean.usd`

## 첫 task

- Gym task: `Mirobot-Reach-Pregrasp-Direct-v0`
- Python package: `source/mirobot_reach_direct`
- 학습 로그: `~/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_reach_pregrasp_direct`
- plot/checkpoint 선택 결과: `logs/plots`

## 실제 MT4 이식 기준

- 정책 action은 실제 MT4 arm-angle 명령으로 보낼 수 있는 4축만 사용합니다: `joint_1`, `joint_2_1`, `joint_3`, `gripper_body_joint`.
- 배포 시 매핑은 `X -> joint_1`, `Y -> joint_2_1`, `Z -> joint_3`, `A -> gripper_body_joint`입니다.
- `joint_2_2`, `joint_4`, `joint_l4`는 URDF/USD에는 남겨두되 정책 action으로 학습하지 않습니다. 현재는 `joint_2_2 = joint_2_1`, `joint_4 = 0.65`, `joint_l4 = 0.35`로 내부 target을 만듭니다.
- 매핑/주의사항 기록: `notes/20260518_111647_mt4_hardware_transfer_mapping.md`

## 실행

```bash
./scripts/inspect_mirobot_asset.sh
./scripts/check_mirobot_joint_limits.sh
./scripts/sweep_mirobot_joint_limits_gui.sh
./scripts/sweep_mirobot_joint_limits_gui.sh --mode upper
./scripts/train_mirobot_visual_16_300.sh
./scripts/train_mirobot_reach_128_1000.sh
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

첫 버전은 reach/pregrasp 안정화용입니다. 실제 집기 정책으로 확장하기 전에 joint 대응, end-effector 축, gripper center offset을 GUI에서 반드시 확인해야 합니다.
