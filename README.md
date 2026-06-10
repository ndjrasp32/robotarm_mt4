# robotarm_mt4

## 한국어

`robotarm_mt4`는 WLKATA Mirobot/MT4 asset, hardware mapping, Mars twin 확인용 IsaacLab direct RL 저장소입니다.

학생용 staged curriculum과 긴 실험 archive는 `robotarm_student`에서 관리합니다. 이 저장소는 실제 MT4 이식에 가까운 asset/task 기준선, joint/action mapping, safety gate를 관리합니다.

### 오늘부터 보는 기준

매일 시작할 때는 이 순서만 봅니다.

1. `docs/CURRENT_BASELINE.md`
2. `README.md`
3. `notes/`는 기준 문서에 링크된 항목만 필요할 때 확인

새 노트는 asset, mapping, safety, task 기준이 실제로 바뀐 경우에만 하나 추가합니다. 단순 실행 로그, plot 결과, 임시 확인은 README 기준으로 승격하지 않습니다.

### 리셋 이유

2026-05-22 기준으로 작업 기준을 리셋했습니다. 이전 상태에서는 날짜별 노트가 늘어났고, 저장소 이름이 `robotarm_student`와 `robotarm_mt4`로 정리되었으며, 학생용 curriculum과 하드웨어 전이 책임이 섞여 있었습니다. 이제 이 저장소는 MT4 asset fidelity, hardware mapping, safe simulation 기준선으로만 봅니다. 오래된 `notes/`는 archive입니다.

### 현재 asset

- 원본 ROS2 xacro: `/home/spark-robotics/work/robotarm/mt4_ws/src/complex_mobile_robot_description/urdf/complex_mobile_robot_description.urdf.xacro`
- Isaac용 clean URDF 복사본: `assets/urdf/mirobot_wlkata_isaac_clean.urdf`
- Isaac용 USD 복사본: `assets/usd/mirobot_real/mt4_from_wlkata_isaac_clean.usd`
- 공식 WLKATA MT4 URDF 기록: `notes/20260518_133328_official_mt4_urdf_check.md`

### 첫 task

- Gym task: `Mirobot-Reach-Pregrasp-Direct-v0`
- Python package: `source/mirobot_reach_direct`
- 학습 로그: `~/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_reach_pregrasp_direct`
- plot/checkpoint 선택 결과: `logs/plots`

### 화성 로버 디지털 트윈 task

화성 중력 `-3.711 m/s^2`, 동적 큐브 충돌, 마찰, home pose reset을 적용한 확인용 direct RL 환경입니다.

- `Mirobot-Mars-Twin-Pick-Direct-v0`
- `Mirobot-Mars-Twin-Place-Direct-v0`
- `Mirobot-Mars-Twin-Stack-Direct-v0`
- `Mirobot-Mars-Twin-Push-Direct-v0`
- `Mirobot-Mars-Twin-Pull-Direct-v0`

바로 열어서 확인:

```bash
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/view_mirobot_mars_twin_gui.sh --mission pull
./scripts/view_mirobot_mars_twin_gui.sh --mission stack
```

학습 실행:

```bash
./scripts/train_mirobot_mars_twin.sh push
./scripts/train_mirobot_mars_twin.sh pull
./scripts/train_mirobot_mars_twin.sh pick
./scripts/train_mirobot_mars_twin.sh place
./scripts/train_mirobot_mars_twin.sh stack
```

현재 환경은 물리 기반 디지털 트윈의 첫 기준선입니다. `push/pull`은 동적 물체 접촉 검증에 바로 쓸 수 있고, `pick/place/stack`은 실제 MT4 gripper finger/파지 구조가 URDF에 충분히 표현되어 있는지 확인한 뒤 grasp attachment 또는 gripper collision 모델을 보강해야 합니다.

### 실제 MT4 perception 기준

실제 MT4 기기 학습과 hardware-transfer 판단은 이 저장소에서 관리합니다. 목표 지점 포착과 높이 추정은 Pi Camera 두 대 구성을 기준으로 진행합니다.

- body/front camera: 로봇팔 몸통 전면에 고정하고 작업 공간 전체와 목표 물체를 관찰합니다.
- wrist/downward camera: 집게 끝 아래쪽을 향하게 고정해 grasp 직전의 상대 위치, 높이, 접촉 후보 영역을 관찰합니다.
- 초기 전환은 raw image end-to-end 정책이 아니라, 카메라 extrinsic 보정과 target position/height 추정값을 내부 좌표 baseline과 비교하는 방식으로 시작합니다.
- 정책 observation은 단계적으로 전환합니다: 내부 target 좌표 baseline -> 카메라 추정 좌표 -> 필요 시 image feature 포함.
- 실제 로봇 motion은 아래 safety gate를 통과하기 전까지 실행 기준으로 올리지 않습니다.

참고 설계 기록: `notes/20260608_dual_pi_camera_perception_plan.md`
student coordinate curriculum handoff: `notes/20260610_student_coordinate_handoff_and_training_plan.md`

### 실제 MT4 이식 기준

- 정책 action은 실제 MT4 arm-angle 명령으로 보낼 수 있는 4축만 사용합니다: `joint_1`, `joint_2_1`, `joint_3`, `gripper_body_joint`.
- 배포 시 매핑은 `X -> joint_1`, `Y -> joint_2_1`, `Z -> joint_3`, `A -> gripper_body_joint`입니다.
- `joint_2_2`, `joint_4`, `joint_l4`는 URDF/USD에는 남겨두되 정책 action으로 학습하지 않습니다.
- 현재 내부 target은 `joint_2_2 = joint_2_1`, `joint_4 = 0.65`, `joint_l4 = 0.35`입니다.
- 매핑/주의사항 기록: `notes/20260518_111647_mt4_hardware_transfer_mapping.md`

### 실행

```bash
./scripts/inspect_mirobot_asset.sh
./scripts/check_mirobot_joint_limits.sh
./scripts/show_mt4_hardware_mapping_gui.sh
./scripts/show_mt4_hardware_mapping_gui.sh --profile workspace
./scripts/sweep_mirobot_joint_limits_gui.sh
./scripts/sweep_mirobot_joint_limits_gui.sh --mode upper
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/train_mirobot_visual_16_300.sh
./scripts/train_mirobot_reach_128_1000.sh
./scripts/train_mirobot_mars_twin.sh push
./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh
./scripts/train_mirobot_coordinate_stage1_volume_128_600.sh
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

실제 집기 정책으로 확장하기 전에 joint 대응, end-effector 축, gripper center offset을 GUI에서 반드시 확인해야 합니다.

## English

`robotarm_mt4` is the IsaacLab direct-RL repository for WLKATA Mirobot/MT4 assets, hardware mapping, and Mars twin checks.

Student staged curriculum work and long experiment archives belong in `robotarm_student`. This repository owns the asset/task baseline closest to real MT4 transfer, joint/action mapping, and safety gates.

### Daily Starting Point

Start each day in this order:

1. `docs/CURRENT_BASELINE.md`
2. `README.md`
3. Open `notes/` only when the baseline links to a specific entry

Add a new note only when the asset, mapping, safety, or task baseline actually changes. Do not promote routine command output, plot results, or temporary checks into the README baseline.

### Reset Rationale

The working baseline was reset on 2026-05-22. The previous state had too many dated notes, the repositories had been renamed into `robotarm_student` and `robotarm_mt4`, and student curriculum work was mixed with hardware-transfer responsibilities. From now on, this repository is the baseline for MT4 asset fidelity, hardware mapping, and safe simulation. Older `notes/` remain archive.

### Current Asset

- source ROS2 xacro: `/home/spark-robotics/work/robotarm/mt4_ws/src/complex_mobile_robot_description/urdf/complex_mobile_robot_description.urdf.xacro`
- Isaac clean URDF copy: `assets/urdf/mirobot_wlkata_isaac_clean.urdf`
- Isaac USD copy: `assets/usd/mirobot_real/mt4_from_wlkata_isaac_clean.usd`
- official WLKATA MT4 URDF record: `notes/20260518_133328_official_mt4_urdf_check.md`

### First Task

- Gym task: `Mirobot-Reach-Pregrasp-Direct-v0`
- Python package: `source/mirobot_reach_direct`
- training logs: `~/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_reach_pregrasp_direct`
- plot/checkpoint selection output: `logs/plots`

### Mars Rover Digital Twin Tasks

These direct-RL environments apply Mars gravity `-3.711 m/s^2`, dynamic cube collision, friction, and home-pose reset.

- `Mirobot-Mars-Twin-Pick-Direct-v0`
- `Mirobot-Mars-Twin-Place-Direct-v0`
- `Mirobot-Mars-Twin-Stack-Direct-v0`
- `Mirobot-Mars-Twin-Push-Direct-v0`
- `Mirobot-Mars-Twin-Pull-Direct-v0`

Open visual checks:

```bash
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/view_mirobot_mars_twin_gui.sh --mission pull
./scripts/view_mirobot_mars_twin_gui.sh --mission stack
```

Run training:

```bash
./scripts/train_mirobot_mars_twin.sh push
./scripts/train_mirobot_mars_twin.sh pull
./scripts/train_mirobot_mars_twin.sh pick
./scripts/train_mirobot_mars_twin.sh place
./scripts/train_mirobot_mars_twin.sh stack
```

The current environment is the first physics-based digital-twin baseline. `push/pull` can immediately validate dynamic-object contact. `pick/place/stack` need gripper-finger or grasp-attachment modeling after confirming whether the real MT4 gripper structure is represented well enough in the URDF.

### Real MT4 Perception Baseline

Real MT4 device learning and hardware-transfer decisions belong in this repository. Target detection and height estimation should use a two Pi Camera setup as the current baseline.

- body/front camera: fixed on the front of the robot body to observe the workspace and target object.
- wrist/downward camera: fixed near the gripper tip and aimed downward to observe final relative pose, height, and contact/grasp candidates.
- Start the transition with camera extrinsic calibration and target position/height estimates compared against the internal-coordinate baseline, not raw-image end-to-end policy learning.
- Transition policy observations in stages: internal target-coordinate baseline -> camera-estimated target coordinates -> image features if needed.
- Do not promote real robot motion into the working baseline until the safety gate below is satisfied.

Reference design note: `notes/20260608_dual_pi_camera_perception_plan.md`
Student coordinate curriculum handoff: `notes/20260610_student_coordinate_handoff_and_training_plan.md`

### Real MT4 Transfer Rule

- Policy actions use only the four joints that can be sent as real MT4 arm-angle commands: `joint_1`, `joint_2_1`, `joint_3`, `gripper_body_joint`.
- Deployment mapping is `X -> joint_1`, `Y -> joint_2_1`, `Z -> joint_3`, `A -> gripper_body_joint`.
- `joint_2_2`, `joint_4`, and `joint_l4` remain in URDF/USD but are not policy actions.
- Current internal targets are `joint_2_2 = joint_2_1`, `joint_4 = 0.65`, and `joint_l4 = 0.35`.
- Mapping and caveat record: `notes/20260518_111647_mt4_hardware_transfer_mapping.md`

### Commands

```bash
./scripts/inspect_mirobot_asset.sh
./scripts/check_mirobot_joint_limits.sh
./scripts/show_mt4_hardware_mapping_gui.sh
./scripts/show_mt4_hardware_mapping_gui.sh --profile workspace
./scripts/sweep_mirobot_joint_limits_gui.sh
./scripts/sweep_mirobot_joint_limits_gui.sh --mode upper
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/train_mirobot_visual_16_300.sh
./scripts/train_mirobot_reach_128_1000.sh
./scripts/train_mirobot_mars_twin.sh push
./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh
./scripts/train_mirobot_coordinate_stage1_volume_128_600.sh
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

Before extending into real grasping policies, confirm joint correspondence, end-effector axis, and gripper-center offset in the GUI.
