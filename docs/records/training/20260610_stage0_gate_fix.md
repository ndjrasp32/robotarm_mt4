# 2026-06-10 MT4 Stage 0 gate fix 기록

## 내 제안

- student 쪽에서 정리한 camera-coordinate curriculum을 MT4 asset 기준으로 이어간다.
- 보정은 최소화하되, 학습을 한 번 진행할 때마다 날짜/시간 제목의 md 파일로 남긴다.
- 각 기록에는 내 제안, Codex 제안, 최종 결정, 학습 진행, 학습 결과와 그래프 표현을 포함한다.

## Codex 제안

- Stage 0 결과에서 `success_hold_rate`가 높아도 `inside_workspace_rate=0.0000`이면 Stage 1로 넘어가지 않는다.
- 우선순위 1, 2, 3을 순서대로 처리한다.
  1. `gripper_body` 기준 gripper center, forward axis, gripper camera offset 설정 확인
  2. `workspace_entry_success_radius=0.065`가 workspace 바깥 근접 성공을 latch하는지 점검
  3. Stage 0 성공 조건을 `inside_workspace`와 결합

## 최종 결정

- `gripper_center_offset_b=(0.055, 0.0, 0.0)`, `gripper_forward_axis_b=(1.0, 0.0, 0.0)`, `gripper_camera_offset_b=(-0.035, 0.0, 0.018)`는 이번 패치에서 유지한다.
- Stage 0 실패의 직접 원인은 axis 변경으로 확정하지 않고, 먼저 성공 gate가 너무 느슨한 문제를 고친다.
- `workspace_entry_success_radius`는 0.065 m에서 0.020 m로 낮춘다.
- Stage 0 성공 판정은 이제 `inside_workspace & gripper_stereo_visible`만 성공으로 인정한다.
- radius 조건은 성공 판정이 아니라 진단 지표 `workspace_entry_radius_rate`로 남긴다.

## 학습 진행

이번 항목은 학습 실행이 아니라 Stage 0 gate 수정이다. 실제 로봇 motion은 실행하지 않았다.

다음 시뮬레이션 재실행 명령:

```bash
./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh
```

## 학습 결과

아직 재학습 전이다. 기존 Stage 0 결과는 아래와 같이 해석한다.

| metric | previous value | interpretation |
| --- | ---: | --- |
| `workspace_entry_success_rate` | 0.0281 | 기존 기준의 근접 성공 |
| `workspace_entry_success_hold_rate` | 0.8650 | latch 영향으로 과대 표시 가능 |
| `inside_workspace_rate` | 0.0000 | 실제 작업공간 내부 진입 실패 |
| `mean_workspace_entry_error` | 0.1151 m | 보수 workspace까지 평균 11.5 cm 부족 |
| `target_three_camera_visible_rate` | 0.0056 | gripper camera 기준 target visibility 거의 없음 |

그래프 표현:

```text
inside_workspace_rate          0.0000 | 
target_three_camera_visible    0.0056 | #
workspace_entry_success_rate   0.0281 | ###
success_hold_rate              0.8650 | ###########################################
```

## 다음 판단

- 수정 후 Stage 0를 다시 돌려 `inside_workspace_rate`, `workspace_entry_radius_rate`, `mean_workspace_entry_error`를 본다.
- `inside_workspace_rate`가 계속 0이면 workspace center/size 또는 gripper offset audit으로 넘어간다.
- `target_three_camera_visible_rate`가 계속 낮으면 gripper camera forward axis/offset을 GUI로 직접 확인한다.
