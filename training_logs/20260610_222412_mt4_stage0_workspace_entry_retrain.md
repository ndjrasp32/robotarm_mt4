# 2026-06-10 22:24:12 MT4 Stage 0 Workspace-Entry Retrain

## 내 제안

- student 쪽에서 했던 흐름처럼, 먼저 가동 영역 판정부터 확인한다.
- 수정 제안사항을 기록으로 남기고, 한 번 학습을 진행하면서 수치를 분석한다.
- Stage 1 장기 학습으로 바로 넘어가지 않고 Stage 0 gate 수정 효과를 먼저 본다.

## Codex 제안

- 기존 `workspace_entry_success_radius=0.065` 기준은 workspace 바깥 근접 상태도 성공으로 latch할 수 있으므로, 성공 판정을 더 엄격하게 바꾼다.
- `workspace_entry_success_radius`는 0.020 m로 줄이고, 이 값은 성공 판정이 아니라 진단 지표로만 사용한다.
- Stage 0 성공은 `inside_workspace & gripper_stereo_visible`일 때만 인정한다.
- 이번 학습에서는 `success_rate`보다 `inside_workspace_rate`, `workspace_entry_radius_rate`, `mean_workspace_entry_error`, camera visibility를 우선 판단한다.

## 최종 결정

- 실제 로봇 motion은 실행하지 않았다.
- IsaacLab headless 시뮬레이션으로 Stage 0 workspace-entry 128 env, 300 iteration을 실행한 결과를 이번 판단 기준으로 삼는다.
- 이번 결과에서 `inside_workspace_rate`가 0이면 Stage 1 volume 학습은 보류한다.
- 다음 수정 후보는 workspace center/size audit 또는 gripper center/offset audit이다.

## 학습 진행

실행 명령:

```bash
./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh
```

실행 정보:

| item | value |
| --- | --- |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-10_22-24-12_mt4_coordinate_stage0_workspace_entry_128env_300iter` |
| envs | 128 |
| iterations | 300 |
| seed | 42 |
| checkpoint | `model_299.pt` |
| measured scalar wall time | 270.01 s |

이번 실행에 포함된 코드 변경:

```diff
- workspace_entry_success_radius = 0.065
+ workspace_entry_success_radius = 0.020

+ workspace_entry_radius_rate = workspace_entry_error < workspace_entry_success_radius

- success = workspace_entry_error < workspace_entry_success_radius
+ success = inside_workspace & gripper_stereo_visible
```

## 학습 결과

| metric | 0 | 50 | 100 | 150 | 200 | 250 | 299 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `mean_reward` | 39.3386 | 1538.8225 | 2095.6362 | 2230.6951 | 2272.5720 | 2285.7581 | 2286.7859 |
| `workspace_entry_success_rate` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `inside_workspace_rate` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `workspace_entry_radius_rate` | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| `mean_workspace_entry_error` | 0.1362 | 0.1029 | 0.0948 | 0.0883 | 0.0817 | 0.0833 | 0.0825 |
| `target_three_camera_visible_rate` | 0.0000 | 0.4260 | 0.8464 | 0.8340 | 0.8730 | 0.8503 | 0.8049 |
| `gripper_stereo_visible_rate` | 0.6970 | 0.8345 | 0.9683 | 0.9775 | 0.9846 | 0.9753 | 0.9741 |
| `mean_gripper_camera_direction_error` | 1.1368 | 0.6002 | 0.2307 | 0.2350 | 0.2472 | 0.2628 | 0.2889 |
| `mean_gripper_camera_target_depth` | -1.2608 | -0.5416 | -0.0130 | -0.0527 | -0.0985 | -0.1164 | -0.1631 |
| `mean_distance` | 0.2652 | 0.2354 | 0.2266 | 0.2183 | 0.2117 | 0.2141 | 0.2116 |

그래프:

- reward: `training_logs/figures/20260610_222412_stage0_reward.png`
- success/workspace: `training_logs/figures/20260610_222412_stage0_success_workspace.png`
- distance error: `training_logs/figures/20260610_222412_stage0_error.png`
- visibility: `training_logs/figures/20260610_222412_stage0_visibility.png`

텍스트 그래프, final iteration 기준:

```text
mean_reward                       2286.7859 | ################################################
target_three_camera_visible_rate     0.8049 | ########################################
gripper_stereo_visible_rate          0.9741 | #################################################
inside_workspace_rate                0.0000 |
workspace_entry_radius_rate          0.0000 |
workspace_entry_success_rate         0.0000 |
mean_workspace_entry_error_m         0.0825 | ########
```

## 분석

Reward는 39.34에서 2286.79까지 상승했고, target three-camera visibility도 0.0000에서 0.8049까지 올라갔다. 즉 정책은 target을 카메라에 넣는 방향과 gripper stereo visibility를 유지하는 방향은 학습했다.

하지만 엄격한 workspace-entry 기준은 전혀 통과하지 못했다. `inside_workspace_rate`, `workspace_entry_radius_rate`, `workspace_entry_success_rate`가 모두 0.0000으로 끝났고, 평균 workspace boundary error도 0.0825 m 남았다. 이전 run의 `mean_workspace_entry_error=0.1151 m`보다는 줄었지만, 2 cm radius나 실제 workspace 내부 진입에는 아직 멀다.

`mean_gripper_camera_target_depth`가 -0.1631 m로 끝난 점도 중요하다. target visibility는 좋아졌지만 gripper camera 기준 target이 여전히 forward depth 양수 방향에 안정적으로 들어온 상태가 아니다. camera projection reward가 workspace 내부 진입보다 쉬운 방향으로 최적화됐을 가능성이 있다.

## 다음 판단

- Stage 1 volume 학습은 아직 진행하지 않는다.
- 다음 1순위는 workspace center/size가 실제 MT4 reachable gripper center와 맞는지 audit하는 것이다.
- 동시에 `gripper_center_offset_b`와 `gripper_camera_offset_b`가 `gripper_body` frame에서 올바른 방향인지 GUI 또는 reach sampling으로 확인한다.
- 다음 학습 전에는 success reward와 workspace-entry reward가 camera visibility만으로 우회되지 않도록 reward weight를 분리해서 조정한다.
