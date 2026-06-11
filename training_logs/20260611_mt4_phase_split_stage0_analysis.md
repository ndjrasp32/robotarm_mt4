# 2026-06-11 MT4 Phase-Split Stage 0 Analysis

## Goal

탑다운 방식으로 curriculum을 phase 분리한다.

1. Phase 0 / top-down setup: gripper center를 workspace 상단 기준 높이로 올리고, target x/y와 gripper center x/y 오차를 1 cm 미만으로 맞춘다.
2. Phase 1 / descent workspace-entry: Phase 0가 latch된 뒤에만 z 방향 descent 및 workspace 내부 진입 보상과 성공 판정을 인정한다.
3. Stage 1 / 3x3 plane, Stage 2 / 3x3x3 volume은 Stage 0 gate가 통과된 뒤 실행한다.

## Code Change

- Environment: `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py`
- Observation size: `57 -> 60`
- Added observation fields:
  - `top_down_phase_latched`
  - normalized `top_down_xy_error`
  - normalized `top_down_height_error`
- Added Stage 0 phase metrics:
  - `top_down_xy_1cm_rate`
  - `top_down_height_ready_rate`
  - `top_down_phase_ready_rate`
  - `top_down_phase_latched_rate`
  - `descent_phase_success_rate`
- Stage 0 success now requires:
  - `inside_workspace`
  - required camera visibility
  - `top_down_phase_latched`

## Training Run

| item | value |
| --- | --- |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| run name | `mt4_phase_split_progress_stage0_128env_300iter_video` |
| envs | 128 |
| iterations | 300 |
| seed | 42 |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video` |
| final checkpoint | `model_299.pt` |

Videos:

- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/videos/train/rl-video-step-0.mp4`
- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/videos/train/rl-video-step-2400.mp4`
- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/videos/train/rl-video-step-4800.mp4`
- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/videos/train/rl-video-step-7200.mp4`

## Final Scalars

| metric | first | final | best |
| --- | ---: | ---: | ---: |
| `Train/mean_reward` | 64.6595 | 6847.1260 | 6851.0815 |
| `workspace_entry_success_rate` | 0.0000 | 0.0000 | 0.0000 |
| `workspace_entry_success_hold_rate` | 0.0000 | 0.0000 | 0.0000 |
| `mean_distance` | 0.1742 m | 0.0515 m | n/a |
| `mean_workspace_entry_error` | 0.1398 m | 0.0214 m | n/a |
| `workspace_entry_radius_rate` | 0.0000 | 0.7939 | 0.8669 |
| `inside_workspace_rate` | 0.0000 | 0.0000 | 0.0444 |
| `top_down_xy_1cm_rate` | 0.0000 | 0.4543 | 0.5586 |
| `mean_top_down_xy_error` | 0.1402 m | 0.0190 m | n/a |
| `top_down_height_ready_rate` | 0.0000 | 0.0000 | 0.0000 |
| `mean_top_down_height_error` | 0.1292 m | 0.0728 m | n/a |
| `top_down_phase_ready_rate` | 0.0000 | 0.0000 | 0.0000 |
| `top_down_phase_latched_rate` | 0.0000 | 0.0000 | 0.0000 |
| `descent_phase_success_rate` | 0.0000 | 0.0000 | 0.0000 |
| `target_three_camera_visible_rate` | 0.0000 | 0.8989 | 0.9221 |
| `gripper_stereo_visible_rate` | 1.0000 | 1.0000 | 1.0000 |
| `near_center_7cm_rate` | 0.0000 | 0.9207 | 0.9343 |
| `center_3cm_rate` | 0.0000 | 0.0000 | 0.0061 |
| `center_1cm_rate` | 0.0000 | 0.0000 | 0.0000 |

## Phase Result

| phase | success criterion | final rate | status |
| --- | --- | ---: | --- |
| Phase 0A / x-y setup | x/y error < 1 cm | 0.4543 | partially learned |
| Phase 0B / top height setup | z near workspace top within 1.2 cm | 0.0000 | failed |
| Phase 0 latch | Phase 0A and 0B at same time | 0.0000 | failed |
| Phase 1 / descent entry | inside workspace after Phase 0 latch | 0.0000 | blocked |
| Stage 1 / 3x3 plane | Stage 0 gate must pass first | not run | held |
| Stage 2 / 3x3x3 volume | Stage 1 must pass first | not run | held |

## Interpretation

The phase split is now observable and measurable, but the current Stage 0 policy still does not satisfy the top-down gate.

The useful part is that x/y alignment started to learn: mean x/y error moved from 14.0 cm to 1.9 cm, and the 1 cm x/y rate reached 45.4% final / 55.9% best. Camera visibility also recovered to about 89.9% final.

The blocker is z. Mean top-down height error only improved from 12.9 cm to 7.3 cm, and `top_down_height_ready_rate` stayed at 0. This means Phase 0B never completed, so the latch never activated and Phase 1 workspace-entry reward/success stayed blocked by design.

## Next Adjustment

Do not start Stage 1 yet. The next Stage 0 run should make the top-down height setup easier before requiring descent:

1. Increase the top-height tolerance temporarily from `0.012 m` to about `0.030 m`.
2. Reduce the target top z from exact workspace max to a reachable staging band, e.g. `workspace_center.z + 0.010 to 0.020 m`.
3. Once `top_down_phase_latched_rate` is consistently above 0.5, tighten the z tolerance back toward 1.2 cm and then enable Stage 1.
