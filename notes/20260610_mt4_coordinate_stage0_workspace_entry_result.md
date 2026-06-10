# 2026-06-10 MT4 Coordinate Stage 0 Workspace-Entry Result

## 실행

| item | value |
| --- | --- |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| command | `./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-10_18-43-56_mt4_coordinate_stage0_workspace_entry_128env_300iter` |
| final checkpoint | `model_299.pt` |
| training time | `250.41 s` |
| envs / iterations | `128 / 300` |

## 최종 batch 지표

| metric | value |
| --- | ---: |
| `workspace_entry_success_rate` | 0.0281 |
| `workspace_entry_new_success_rate` | 0.0042 |
| `workspace_entry_success_hold_rate` | 0.8650 |
| `mean_workspace_entry_error` | 0.1151 m |
| `inside_workspace_rate` | 0.0000 |
| `mean_distance` | 0.2452 m |
| `target_stereo_visible_rate` | 1.0000 |
| `gripper_stereo_visible_rate` | 0.8572 |
| `target_gripper_camera_visible_rate` | 0.0056 |
| `target_three_camera_visible_rate` | 0.0056 |
| `camera_region_match_rate` | 1.0000 |
| `mean_gripper_camera_direction_error` | 0.9570 |
| `mean_action_std` | 1.02 |

## 판단

런타임 포팅 자체는 성공했다. 새 task는 IsaacLab에서 등록되고, observation 51개와 action 4개로 정책/critic 네트워크가 정상 생성됐으며, 300 iteration 학습도 완료됐다.

하지만 Stage 1 volume curriculum으로 바로 넘어가기는 이르다. `success_hold_rate`가 높게 나온 이유는 workspace-entry 성공을 latch해서 episode 끝까지 유지하도록 만든 영향이다. 반면 최종 batch의 `inside_workspace_rate=0.0000`, `mean_workspace_entry_error=0.1151 m`, `target_three_camera_visible_rate=0.0056`이므로 실제 gripper 중심이 conservative workspace 안으로 안정적으로 들어왔다고 볼 수 없다.

## 다음 수정 우선순위

1. MT4 URDF에서 `gripper_body` 기준 forward axis와 gripper camera offset을 다시 확인한다.
2. `workspace_entry_success_radius=0.065`가 workspace 바깥 근접 성공을 너무 쉽게 latch하는지 점검한다.
3. Stage 0의 성공 조건을 `inside_workspace` 또는 더 작은 boundary error와 결합한다.
4. conservative workspace center/size를 실제 MT4 gripper reach sampling 기준으로 다시 audit한다.
5. 위 수정 전에는 `Mirobot-Coordinate-Volume-Direct-v0` 장기 학습을 실행하지 않는다.
