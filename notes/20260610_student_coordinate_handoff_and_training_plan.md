# 2026-06-10 Student Coordinate Curriculum Handoff and MT4 Training Plan

## 목적

`robotarm_student`에서 검증한 three-camera coordinate curriculum을 실제 MT4 asset 저장소인 `robotarm_mt4`로 옮기기 위한 전달 기록이다. 이 문서는 실제 로봇 motion 지시가 아니라 IsaacLab simulation 학습 계획이다. 실제 기기 구동은 기존 Safety Gate 이후에만 다룬다.

## student 레포에서 넘어온 결론

검증된 흐름:

1. body left/right stereo camera projection으로 목표 영역을 추정한다.
2. gripper-mounted camera projection으로 마지막 상대 위치, depth, visible 여부를 추가한다.
3. 정책에는 내부 target 생성 좌표를 직접 주지 않고, 카메라에서 추정한 target-relative xyz, region feature, camera feature를 준다.
4. 성공 조건은 단순 batch success rate가 아니라 영역별 누적 success count와 `mastered_region_count`로 본다.
5. 성공한 env는 즉시 reset하지 않고, 해당 episode time limit까지 성공 자세를 유지한다.
6. 성공 marker를 보이게 띄워 학습/데모에서 성공 상태를 눈으로 확인한다.

최종 student 기준:

| item | value |
| --- | --- |
| conservative workspace center | `(0.305, 0.00, 0.205)` |
| conservative workspace size | `(0.09, 0.14, 0.09)` |
| 27-region task | `Isaac-MT4-Coordinate-Volume-Direct-v0` |
| 27-region result | 27/27 regions mastered at 1 cm |
| precision task | `Isaac-MT4-Coordinate-Volume-Precision-Direct-v0` |
| precision result | 26/27 regions mastered at 5 mm after 800 iterations |

해석:

- 실패 원인은 27영역 자체가 아니라, 처음 작업 박스가 안정 가동범위 밖이었다.
- 새 asset으로 옮길 때는 먼저 joint/action mapping과 gripper 중심 위치를 다시 맞춘 뒤, 보수 작업 박스에서 학습해야 한다.
- 5mm 정밀 제어는 가능성이 열렸지만, 실제 MT4 asset에서는 축, 링크, gripper offset이 다르므로 바로 5mm warm start를 적용하지 않는다.

## robotarm_mt4 적용 내용

새 후보 task를 추가했다.

| task | purpose |
| --- | --- |
| `Mirobot-Coordinate-Workspace-Entry-Direct-v0` | MT4 URDF 축으로 gripper가 카메라 가시 작업공간에 들어오는지 확인 |
| `Mirobot-Coordinate-Plane-Direct-v0` | front 3x3 plane region curriculum |
| `Mirobot-Coordinate-Volume-Direct-v0` | conservative 3x3x3 volume curriculum |
| `Mirobot-Coordinate-Volume-Precision-Direct-v0` | 5mm precision 후보, stage1 성공 이후 사용 |

축/조인트 차이 대응:

- student action은 simplified asset 5축이었다.
- MT4 action은 실제 command-facing 4축만 사용한다: `joint_1`, `joint_2_1`, `joint_3`, `gripper_body_joint`.
- sim 내부에서는 `joint_2_2`가 `joint_2_1`을 따라가고, `joint_4`, `joint_l4`는 passive home target을 유지한다.
- gripper center offset은 MT4 기존 baseline의 `gripper_center_offset_b=(0.055,0,0)`를 사용한다.
- observation은 5축 기준 54개에서 4축 기준 51개로 줄었다.

## 학습 계획

### Stage 0: workspace-entry smoke

명령:

```bash
./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh
```

목표:

- 새 URDF/USD에서 action mapping이 깨지지 않는지 확인한다.
- `inside_workspace_rate`, `gripper_stereo_visible_rate`, `mean_workspace_entry_error`를 본다.
- 학습 중 NaN, joint explosion, gripper 방향 반전이 있으면 stage1로 가지 않는다.

진행 기준:

- `inside_workspace_rate`가 의미 있게 상승한다.
- gripper가 보수 작업 박스 근처로 들어온다.
- passive linkage가 비정상적으로 꺾이지 않는다.

### Stage 1: conservative 3x3x3 volume

명령:

```bash
./scripts/train_mirobot_coordinate_stage1_volume_128_600.sh
```

목표:

- student에서 성공한 보수 작업 박스를 실제 MT4 asset 기준으로 재검증한다.
- `mastered_region_count`, `region_mastery.csv`, `target_three_camera_visible_rate`, `camera_region_match_rate`, `mean_distance`를 본다.
- 바로 27/27을 기대하지 않고, 어느 영역에서 막히는지 먼저 기록한다.

진행 기준:

- 첫 600 iteration에서 `mastered_region_count > 0`이면 stage1 연장 가치가 있다.
- `inside_workspace_rate=0`이면 작업 박스 또는 gripper offset부터 다시 audit한다.
- `camera_region_match_rate`가 낮으면 camera mount/FOV부터 수정한다.

### Stage 2: 5mm precision

조건:

- Stage 1에서 27/27 또는 명확한 plateau와 원인 분석이 끝난 뒤에만 실행한다.
- Stage 1 checkpoint를 warm start로 사용한다.

목표:

- `center_success_radius=0.005`
- 낮은 overshoot
- 낮은 action scale
- entropy/action std 완화 검토

## 보고 주기

학습이 실제로 들어가면 중간 분석은 약 5분에 한 번만 한다. 중간 보고는 다음만 포함한다.

- 현재 iteration 또는 elapsed time
- `mastered_region_count`
- `mean_distance`
- `inside_workspace_rate`
- `target_three_camera_visible_rate`
- 막힌 영역 또는 비정상 동작 여부

완료 후에는 최종 checkpoint, 핵심 지표, 다음 판단만 보고한다.

## 현재 판단

바로 실제 로봇 motion으로 가지 않는다. 오늘의 첫 실행은 Stage 0 workspace-entry smoke다. 이 단계가 통과해야 Stage 1 volume curriculum을 신뢰할 수 있다.
