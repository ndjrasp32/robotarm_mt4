# Current Baseline - robotarm_mt4

Date: 2026-05-22 KST

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
- mapping reference: `notes/20260518_111647_mt4_hardware_transfer_mapping.md`
- dynamic object contact reference: `notes/20260518_134455_dynamic_cube_target.md`
- official WLKATA MT4 URDF check reference: `notes/20260518_133328_official_mt4_urdf_check.md`

### 리셋 이유

2026-05-22 기준으로 baseline을 리셋했습니다. 이전 작업 상태는 날짜별 노트가 너무 많고, 저장소 이름이 바뀌었으며, 학생용 curriculum과 하드웨어 전이 책임이 섞여 있었습니다. 이제 이 저장소는 Mirobot/MT4 asset과 hardware-transfer baseline입니다. 이전 `notes/` 항목은 daily source of truth가 아니라 archive입니다.

### 실제 시작 순서

오늘은 여기서 시작합니다.

1. visual command로 scene 또는 task를 먼저 확인합니다.
2. scene이 맞아 보일 때만 training command를 하나 실행합니다.
3. checkpoint를 plot/select합니다.
4. MT4 asset, mapping, safety, task 기준이 바뀐 경우에만 이 파일을 갱신합니다.

Visual inspection:

```bash
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/view_mirobot_mars_twin_gui.sh --mission pull
```

Repeatable training:

```bash
./scripts/train_mirobot_reach_128_1000.sh
./scripts/train_mirobot_mars_twin.sh push
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

### Safety Gate

실제 로봇 motion은 아래 항목이 기록되기 전까지 실행 기준으로 올리지 않습니다.

- home pose joint table
- conservative joint limits
- Isaac joint/action to MT4 SDK command mapping
- no-motion connection check
- low-speed single-joint check
- emergency stop and recovery procedure

### 문서 운영 규칙

- 기존 `notes/`는 historical archive입니다.
- routine command output은 새 노트로 만들지 않습니다.
- 새 관찰은 dated note로 남기되, MT4 asset, mapping, safety, task baseline이 바뀔 때만 이 파일을 갱신합니다.
- 오늘 기준 판단은 `README.md`와 이 파일만으로 끝나야 합니다.

### 다음 작업

1. 이 저장소를 MT4 asset fidelity, mapping, safe simulation에 집중시킨다.
2. `pick/place/stack`을 stable로 보기 전에 `push/pull` contact behavior를 검증한다.
3. 실제 robot motion은 safety gate 뒤에 둔다.
4. 의미 있는 변경이나 실험마다 concise note 하나만 기록한다.
5. 이 파일이 링크하지 않는 dated note는 archive로 취급한다.

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
- mapping reference: `notes/20260518_111647_mt4_hardware_transfer_mapping.md`
- dynamic object contact reference: `notes/20260518_134455_dynamic_cube_target.md`
- official WLKATA MT4 URDF check reference: `notes/20260518_133328_official_mt4_urdf_check.md`

### Reset Rationale

The baseline was reset on 2026-05-22 because the previous working state had too many dated notes, the repositories had been renamed, and student curriculum responsibilities were mixed with hardware-transfer responsibilities. From now on, this repository is the Mirobot/MT4 asset and hardware-transfer baseline. Older `notes/` entries remain archive rather than the daily source of truth.

### Practical Starting Point

Start here today:

1. Confirm the scene or task with a visual command.
2. Run one training command only after the scene looks correct.
3. Plot/select the checkpoint.
4. Update this file only if the MT4 asset, mapping, safety, or task baseline changes.

Visual inspection:

```bash
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/view_mirobot_mars_twin_gui.sh --mission pull
```

Repeatable training:

```bash
./scripts/train_mirobot_reach_128_1000.sh
./scripts/train_mirobot_mars_twin.sh push
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

### Safety Gate

Do not promote real robot motion into the working baseline until these items are recorded:

- home pose joint table
- conservative joint limits
- Isaac joint/action to MT4 SDK command mapping
- no-motion connection check
- low-speed single-joint check
- emergency stop and recovery procedure

### Documentation Policy

- Existing `notes/` are historical archive.
- Do not create a new note for routine command output.
- Record new observations as dated notes, then update this file only when the MT4 asset, mapping, safety, or task baseline changes.
- Daily baseline decisions should be possible from `README.md` and this file alone.

### Next Work

1. Keep this repository focused on MT4 asset fidelity, mapping, and safe simulation.
2. Verify `push/pull` contact behavior before treating `pick/place/stack` as stable.
3. Keep real robot motion behind the safety gate.
4. Record only one concise note per meaningful change or experiment.
5. Treat dated notes as archive unless this file links to them.
