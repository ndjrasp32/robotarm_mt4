# 현재 기준 - robotarm_mt4

Date: 2026-06-11 KST

## 한국어

### 저장소 역할

`robotarm_mt4`는 Mirobot/MT4 asset과 hardware-transfer baseline 저장소입니다.

이 저장소에서 관리하는 범위:

- Mirobot/MT4 URDF/USD asset check
- joint/action mapping과 hardware-transfer notes
- 실제 asset에 가까운 Mars twin simulation check
- visual inspection, plotting, checkpoint utility scripts

넓은 학생용 curriculum archive와 staged classroom experiment는 `robotarm_student`에서 관리합니다.

### 현재 기준

Active task package:

- `source/mirobot_reach_direct`

Main task IDs:

- `Mirobot-Reach-Pregrasp-Direct-v0`
- `Mirobot-Mars-Twin-Pick-Direct-v0`
- `Mirobot-Mars-Twin-Place-Direct-v0`
- `Mirobot-Mars-Twin-Stack-Direct-v0`
- `Mirobot-Mars-Twin-Push-Direct-v0`
- `Mirobot-Mars-Twin-Pull-Direct-v0`

현재 hardware-transfer rule:

- policy action은 네 개의 MT4 command-facing joint로 제한합니다.
- mapping reference: `docs/records/design/20260518_mt4_hardware_transfer_mapping.md`
- dynamic object contact reference: `docs/records/design/20260518_dynamic_cube_target.md`
- official WLKATA MT4 URDF check reference: `docs/records/design/20260518_official_mt4_urdf_check.md`
- perception baseline reference: `docs/records/design/20260608_dual_pi_camera_perception_plan.md`
- student coordinate curriculum handoff: `docs/records/design/20260610_student_coordinate_handoff_and_training_plan.md`
- latest MT4 coordinate stage0 result: `docs/records/training/20260610_stage0_workspace_entry_result.md`
- MT4 reach-limited 27-cell workspace audit: `docs/records/design/20260611_mt4_reach_limited_workspace_audit.md`
- latest MT4 coordinate Stage 1 plane result: `docs/records/training/20260611_stage1_plane_xy035_center035_analysis.md`

### 실제 MT4 Perception Baseline

실제 MT4 기기 학습은 이 저장소에서만 관리합니다. 학생용 simulation curriculum은 `robotarm_student`에 고정하고, 이 저장소에서는 실제 asset, hardware mapping, safety gate와 연결되는 perception 기준만 관리합니다.

카메라 구성:

- body/front camera: 로봇팔 몸통 전면에 고정하고 작업 공간 전체와 목표 물체를 관찰한다.
- wrist/downward camera: 집게 끝 아래쪽을 향하게 고정해 grasp 직전의 상대 위치, 높이, 접촉 후보 영역을 관찰한다.

학습 전환 기준:

1. 내부 target 좌표를 쓰는 기존 Isaac baseline을 hardware-transfer 비교 기준으로 유지한다.
2. 두 카메라의 mount pose, field of view, occlusion을 simulation에서 먼저 확인한다.
3. 카메라에서 추정한 target position/height를 내부 좌표와 비교해 오차를 기록한다.
4. policy observation을 내부 좌표에서 카메라 추정 좌표로 바꾼다.
5. 좌표 추정이 안정화된 뒤에만 image feature 또는 end-to-end vision policy를 검토한다.
6. 실제 로봇 motion은 Safety Gate를 통과한 뒤에만 다룬다.

### 리셋 이유

2026-05-22 기준으로 baseline을 리셋했습니다. 이전 작업 상태는 날짜별 노트가 너무 많고, 저장소 이름이 바뀌었으며, 학생용 curriculum과 하드웨어 전이 책임이 섞여 있었습니다. 이제 이 저장소는 Mirobot/MT4 asset과 hardware-transfer baseline입니다. 이전 기록은 daily source of truth가 아니라 `docs/records/archive/` 보관 기록입니다.

### 실제 시작 순서

오늘은 여기서 시작합니다.

1. visual command로 scene 또는 task를 먼저 확인합니다.
2. scene이 맞아 보일 때만 training command를 하나 실행합니다.
3. checkpoint를 plot/select합니다.
4. 카메라 mount와 target position/height 추정은 내부 좌표 baseline과 비교해 기록합니다.
5. MT4 asset, mapping, perception, safety, task 기준이 바뀐 경우에만 이 파일을 갱신합니다.

Visual inspection:

```bash
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/view_mirobot_mars_twin_gui.sh --mission pull
```

Repeatable training:

```bash
./scripts/train_mirobot_reach_128_1000.sh
./scripts/train_mirobot_mars_twin.sh push
./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh
./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh
./scripts/train_mirobot_coordinate_stage2_volume_128_600.sh
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

2026-06-10 Stage 0 coordinate workspace-entry 학습은 task/runtime 포팅 확인에는 성공했지만, `inside_workspace_rate=0.0000`으로 끝났습니다. 2026-06-11 top-down reach sampling 기준으로 MT4 작업 박스를 `center=(-0.078, 0.000, 0.103)`, `size=(0.045, 0.095, 0.055)`로 다시 잡았습니다. gripper camera는 집게 body 기준 `(+X, 0, -Z)` 45도 방향으로 밖에서 안쪽을 보게 두고, 관측에는 동적 gripper-camera forward 벡터를 포함합니다. 학습 순서는 Stage 0 workspace-entry, Stage 1 3x3 plane, Stage 2 27-cell volume입니다.

### Safety Gate

실제 로봇 motion은 아래 항목이 기록되기 전까지 실행 기준으로 올리지 않습니다.

- home pose joint table
- conservative joint limits
- Isaac joint/action to MT4 SDK command mapping
- no-motion connection check
- low-speed single-joint check
- emergency stop and recovery procedure

### 문서 운영 규칙

- 문서 인덱스와 기록 양식은 `docs/records/README.md`를 따른다.
- 기준 설계 기록은 `docs/records/design/`에 둔다.
- 학습 결과와 분석 기록은 `docs/records/training/`에 둔다.
- 현재 기준에 직접 쓰지 않는 과거 기록은 `docs/records/archive/`에 둔다.
- routine command output은 새 노트로 만들지 않습니다.
- 새 관찰은 dated record로 남기되, MT4 asset, mapping, safety, task baseline이 바뀔 때만 이 파일을 갱신합니다.
- 오늘 기준 판단은 `README.md`와 이 파일만으로 끝나야 합니다.

### 다음 작업

1. 이 저장소를 MT4 asset fidelity, mapping, safe simulation에 집중시킨다.
2. `pick/place/stack`을 stable로 보기 전에 `push/pull` contact behavior를 검증한다.
3. body/front camera와 wrist/downward camera의 mount pose와 관측 범위를 정의한다.
4. target position/height 추정값을 내부 좌표 baseline과 비교한다.
5. 실제 robot motion은 safety gate 뒤에 둔다.
6. 의미 있는 변경이나 실험마다 concise note 하나만 기록한다.
7. 이 파일이 링크하지 않는 dated note는 archive로 취급한다.

## English

### Repository Role

`robotarm_mt4` is the Mirobot/MT4 asset and hardware-transfer baseline repository.

Use this repository for:

- Mirobot/MT4 URDF/USD asset checks
- joint/action mapping and hardware-transfer notes
- Mars twin simulation checks close to the real asset
- visual inspection, plotting, and checkpoint utility scripts

Use `robotarm_student` for the broader student curriculum archive and staged classroom experiments.

### Current Baseline

Active task package:

- `source/mirobot_reach_direct`

Main task IDs:

- `Mirobot-Reach-Pregrasp-Direct-v0`
- `Mirobot-Mars-Twin-Pick-Direct-v0`
- `Mirobot-Mars-Twin-Place-Direct-v0`
- `Mirobot-Mars-Twin-Stack-Direct-v0`
- `Mirobot-Mars-Twin-Push-Direct-v0`
- `Mirobot-Mars-Twin-Pull-Direct-v0`

Current hardware-transfer rule:

- policy actions are limited to four MT4 command-facing joints
- mapping reference: `docs/records/design/20260518_mt4_hardware_transfer_mapping.md`
- dynamic object contact reference: `docs/records/design/20260518_dynamic_cube_target.md`
- official WLKATA MT4 URDF check reference: `docs/records/design/20260518_official_mt4_urdf_check.md`
- perception baseline reference: `docs/records/design/20260608_dual_pi_camera_perception_plan.md`
- student coordinate curriculum handoff: `docs/records/design/20260610_student_coordinate_handoff_and_training_plan.md`
- latest MT4 coordinate stage0 result: `docs/records/training/20260610_stage0_workspace_entry_result.md`
- MT4 reach-limited 27-cell workspace audit: `docs/records/design/20260611_mt4_reach_limited_workspace_audit.md`
- latest MT4 coordinate Stage 1 plane result: `docs/records/training/20260611_stage1_plane_xy035_center035_analysis.md`

### Real MT4 Perception Baseline

Real MT4 device learning belongs only in this repository. Keep the student simulation curriculum fixed in `robotarm_student`; this repository owns perception decisions that connect to the real asset, hardware mapping, and safety gate.

Camera setup:

- body/front camera: fixed on the front of the robot body to observe the workspace and target object.
- wrist/downward camera: fixed near the gripper tip and aimed downward to observe final relative pose, height, and contact/grasp candidates.

Learning transition:

1. Keep the existing Isaac internal-target-coordinate baseline as the hardware-transfer comparison baseline.
2. Verify both camera mount poses, fields of view, and occlusion in simulation first.
3. Compare camera-estimated target position/height against the internal coordinates and record the error.
4. Transition policy observations from internal coordinates to camera-estimated coordinates.
5. Consider image features or end-to-end vision policy only after coordinate estimation is stable.
6. Keep real robot motion behind the Safety Gate.

### Reset Rationale

The baseline was reset on 2026-05-22 because the previous working state had too many dated notes, the repositories had been renamed, and student curriculum responsibilities were mixed with hardware-transfer responsibilities. From now on, this repository is the Mirobot/MT4 asset and hardware-transfer baseline. Older records are preserved under `docs/records/archive/` rather than treated as the daily source of truth.

### Practical Starting Point

Start here today:

1. Confirm the scene or task with a visual command.
2. Run one training command only after the scene looks correct.
3. Plot/select the checkpoint.
4. Record camera mount and target position/height estimation against the internal-coordinate baseline.
5. Update this file only if the MT4 asset, mapping, perception, safety, or task baseline changes.

Visual inspection:

```bash
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/view_mirobot_mars_twin_gui.sh --mission pull
```

Repeatable training:

```bash
./scripts/train_mirobot_reach_128_1000.sh
./scripts/train_mirobot_mars_twin.sh push
./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh
./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh
./scripts/train_mirobot_coordinate_stage2_volume_128_600.sh
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

The 2026-06-10 Stage 0 coordinate workspace-entry run validated task/runtime porting, but ended with `inside_workspace_rate=0.0000`. The 2026-06-11 top-down reach sampling audit moved the MT4 workspace to `center=(-0.078, 0.000, 0.103)`, `size=(0.045, 0.095, 0.055)`. The gripper camera points along the gripper-body `(+X, 0, -Z)` 45-degree axis from outside toward the gripper/target side, and the observation includes the dynamic gripper-camera forward vector. The order is now Stage 0 workspace-entry, Stage 1 3x3 plane, then Stage 2 27-cell volume.

### Safety Gate

Do not promote real robot motion into the working baseline until these items are recorded:

- home pose joint table
- conservative joint limits
- Isaac joint/action to MT4 SDK command mapping
- no-motion connection check
- low-speed single-joint check
- emergency stop and recovery procedure

### Documentation Policy

- Follow the record index and format in `docs/records/README.md`.
- Put baseline design records under `docs/records/design/`.
- Put training results and analysis under `docs/records/training/`.
- Put historical records that are not directly used by the current baseline under `docs/records/archive/`.
- Do not create a new note for routine command output.
- Record new observations as dated records, then update this file only when the MT4 asset, mapping, safety, or task baseline changes.
- Daily baseline decisions should be possible from `README.md` and this file alone.

### Next Work

1. Keep this repository focused on MT4 asset fidelity, mapping, and safe simulation.
2. Verify `push/pull` contact behavior before treating `pick/place/stack` as stable.
3. Define mount poses and fields of view for the body/front camera and wrist/downward camera.
4. Compare target position/height estimates against the internal-coordinate baseline.
5. Keep real robot motion behind the safety gate.
6. Record only one concise note per meaningful change or experiment.
7. Treat dated notes as archive unless this file links to them.
