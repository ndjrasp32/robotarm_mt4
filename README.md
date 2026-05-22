# robotarm_mt4

WLKATA Mirobot/MT4 asset, hardware mapping, Mars twin 확인용 IsaacLab direct RL repo입니다.
학생용 staged curriculum과 긴 실험 archive는 `robotarm_student`에서 관리하고, 이 저장소는 실제 MT4 이식에 가까운 asset/task 기준선을 관리합니다.

## 오늘부터 보는 기준

- 시작 문서: `docs/CURRENT_BASELINE.md`
- 현재 목표: Mirobot/MT4 reach, pregrasp, Mars twin asset/task 기준선 유지
- 실제 기기 제어, 캘리브레이션, 하드웨어 안전 검증은 이 저장소의 safety gate 뒤에서만 관리합니다.
- 과거 `notes/`는 참고 archive입니다. 새 기준 판단은 README와 `docs/CURRENT_BASELINE.md`를 우선합니다.

매일 시작할 때는 이 순서만 봅니다.

1. `docs/CURRENT_BASELINE.md`
2. `README.md`
3. `notes/`는 기준 문서에 링크된 항목만 필요할 때 확인

새 노트는 asset, mapping, safety, task 기준이 실제로 바뀐 경우에만 하나 추가합니다. 단순 실행 로그, plot 결과, 임시 확인은 README 기준으로 승격하지 않습니다.

## 현재 asset

- 원본 ROS2 xacro: `/home/spark-robotics/work/robotarm/mt4_ws/src/complex_mobile_robot_description/urdf/complex_mobile_robot_description.urdf.xacro`
- Isaac용 clean URDF 복사본: `assets/urdf/mirobot_wlkata_isaac_clean.urdf`
- Isaac용 USD 복사본: `assets/usd/mirobot_real/mt4_from_wlkata_isaac_clean.usd`

## 첫 task

- Gym task: `Mirobot-Reach-Pregrasp-Direct-v0`
- Python package: `source/mirobot_reach_direct`
- 학습 로그: `~/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_reach_pregrasp_direct`
- plot/checkpoint 선택 결과: `logs/plots`

## 화성 로버 디지털 트윈 task

공식 MT4 URDF에서 변환한 USD asset을 그대로 사용하고, Isaac Lab/PhysX에서 화성 중력 `-3.711 m/s^2`, 동적 큐브 충돌, 마찰, home pose reset을 적용한 확인용 direct RL 환경입니다.

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

## 실제 MT4 이식 기준

- 정책 action은 실제 MT4 arm-angle 명령으로 보낼 수 있는 4축만 사용합니다: `joint_1`, `joint_2_1`, `joint_3`, `gripper_body_joint`.
- 배포 시 매핑은 `X -> joint_1`, `Y -> joint_2_1`, `Z -> joint_3`, `A -> gripper_body_joint`입니다.
- `joint_2_2`, `joint_4`, `joint_l4`는 URDF/USD에는 남겨두되 정책 action으로 학습하지 않습니다. 현재는 `joint_2_2 = joint_2_1`, `joint_4 = 0.65`, `joint_l4 = 0.35`로 내부 target을 만듭니다.
- 매핑/주의사항 기록: `notes/20260518_111647_mt4_hardware_transfer_mapping.md`

## 실행

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
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

첫 버전은 reach/pregrasp 안정화용입니다. 실제 집기 정책으로 확장하기 전에 joint 대응, end-effector 축, gripper center offset을 GUI에서 반드시 확인해야 합니다.

## 문서 운영 규칙

- 새로 시작할 때는 먼저 `docs/CURRENT_BASELINE.md`를 본다.
- 수업/실습 중 발견한 내용은 `notes/YYYYMMDD_*.md`로 남긴다.
- 오래된 노트는 삭제하지 않고 archive로 유지한다.
- README에는 현재 기준과 실행 진입점만 둔다.
- 오늘의 작업 기준은 README와 `docs/CURRENT_BASELINE.md` 두 파일만으로 판단한다.
