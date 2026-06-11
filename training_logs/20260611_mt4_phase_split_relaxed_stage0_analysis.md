# 2026-06-11 MT4 Phase-Split Relaxed Stage 0 Analysis

## Goal

Previous Stage 0 phase-split training learned x/y alignment but failed the top-down z gate.
This run relaxes the top-down setup before attempting Stage 1:

1. Keep the top-down x/y target at `1 cm`.
2. Relax top-down z tolerance from `0.012 m` to `0.030 m`.
3. Move the top-down staging z from exact workspace max to `workspace_center.z + 0.015 m`.
4. Record training videos for visual inspection.

## Code Change

- Environment: `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py`
- `top_down_height_success_radius`: `0.012 -> 0.030`
- Added `top_down_staging_z_offset = 0.015`
- `top_down_target_z`: `workspace_max.z -> workspace_center.z + top_down_staging_z_offset`

For the current reach-limited MT4 workspace:

- workspace center z: `0.103 m`
- workspace max z: `0.1305 m`
- relaxed staging z: `0.118 m`

## Training Run

| item | value |
| --- | --- |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| run name | `mt4_phase_split_relaxed_stage0_128env_300iter_video` |
| envs | 128 |
| iterations | 300 |
| seed | 42 |
| training time | `286.25 s` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video` |
| final checkpoint | `model_299.pt` |

Videos:

- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/videos/train/rl-video-step-0.mp4`
- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/videos/train/rl-video-step-2400.mp4`
- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/videos/train/rl-video-step-4800.mp4`
- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/videos/train/rl-video-step-7200.mp4`

## Final Scalars

| metric | first | final | best |
| --- | ---: | ---: | ---: |
| `Train/mean_reward` | 70.1319 | 7085.7593 | 7085.7593 |
| `workspace_entry_success_rate` | 0.0000 | 0.0000 | 0.0000 |
| `workspace_entry_success_hold_rate` | 0.0000 | 0.0000 | 0.0000 |
| `mean_distance` | 0.1742 m | 0.0507 m | n/a |
| `mean_workspace_entry_error` | 0.1398 m | 0.0209 m | n/a |
| `workspace_entry_radius_rate` | 0.0000 | 0.8538 | 0.9128 |
| `inside_workspace_rate` | 0.0000 | 0.0000 | 0.0891 |
| `top_down_xy_1cm_rate` | 0.0000 | 0.5415 | 0.5415 |
| `mean_top_down_xy_error` | 0.1402 m | 0.0182 m | n/a |
| `top_down_height_ready_rate` | 0.0000 | 0.0000 | 0.0032 |
| `mean_top_down_height_error` | 0.1167 m | 0.0597 m | n/a |
| `top_down_phase_ready_rate` | 0.0000 | 0.0000 | 0.0000 |
| `top_down_phase_latched_rate` | 0.0000 | 0.0000 | 0.0000 |
| `descent_phase_success_rate` | 0.0000 | 0.0000 | 0.0000 |
| `target_three_camera_visible_rate` | 0.0000 | 0.9004 | 0.9241 |
| `gripper_stereo_visible_rate` | 1.0000 | 1.0000 | 1.0000 |
| `near_center_7cm_rate` | 0.0000 | 0.9226 | 0.9353 |
| `center_3cm_rate` | 0.0000 | 0.0000 | 0.0100 |
| `center_1cm_rate` | 0.0000 | 0.0000 | 0.0000 |

## Phase Result

| phase | success criterion | final rate | status |
| --- | --- | ---: | --- |
| Phase 0A / x-y setup | x/y error < 1 cm | 0.5415 | improved |
| Phase 0B / relaxed top height setup | z near staging height within 3 cm | 0.0000 final / 0.0032 best | still failed |
| Phase 0 latch | x/y and z ready at same time | 0.0000 | failed |
| Phase 1 / descent entry | inside workspace after Phase 0 latch | 0.0000 | blocked |
| Stage 1 / 3x3 plane | Stage 0 gate must pass first | not run | held |
| Stage 2 / 3x3x3 volume | Stage 1 must pass first | not run | held |

## Interpretation

The relaxed run improved the parts we wanted to preserve:

- x/y top-down alignment improved from 45.4% final in the previous run to 54.2% final.
- Three-camera target visibility stayed strong at 90.0% final.
- Workspace proximity remained high: `workspace_entry_radius_rate=0.8538`, best `0.9128`.
- There were transient actual workspace entries: best `inside_workspace_rate=0.0891`.

The blocker is still the z gate. Even after lowering the staging height and widening the tolerance to 3 cm, mean top-down z error settled around 6 cm and the final `top_down_height_ready_rate` stayed 0. Because the latch requires x/y and z to be ready at the same time, Phase 1 remained blocked.

## Next Adjustment

Do not start Stage 1 yet.

The next useful change is not only a larger numeric tolerance. Split the latch into sequential subphases:

1. Latch Phase 0A when x/y error is below 1 cm.
2. After Phase 0A is latched, enable z/descent shaping instead of requiring z readiness at the same instant.
3. Track separate metrics for `xy_latched_rate`, `z_descent_ready_rate`, and `inside_workspace_after_xy_latch_rate`.
4. Keep final Stage 0 success as `inside_workspace & required_camera_visibility & xy_latched`.

This matches the intended behavior more closely: first get above the target in x/y, then adjust z into the workspace.
