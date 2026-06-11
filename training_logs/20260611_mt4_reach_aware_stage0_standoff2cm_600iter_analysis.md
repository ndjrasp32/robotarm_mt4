# 2026-06-11 MT4 Reach-Aware Stage 0 Standoff 2cm / 600iter Analysis

## Scope

This run responds to the 2026-06-11 request to relax the reach-aware pre-entry standoff from `0.035 m` to `0.020 m`, increase Stage 0 learning steps, and record a 60-second learned-policy demo with random environment targets.

All execution was IsaacLab simulation only. No real MT4 robot motion was executed.

## Code / Script Changes

| file | change |
| --- | --- |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | `approach_standoff_distance` changed from `0.035 m` to `0.020 m` for the reach-aware Stage 0 pre-entry target. |
| `scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh` | default `MT4_MAX_ITERATIONS` changed from `300` to `600`; run name updated to `600iter`. |
| `scripts/play_mirobot_coordinate_stage0_demo_60s.sh` | added 60-second coordinate Stage 0 demo recorder using the selected checkpoint and random reset targets. |

## Training Run

| item | value |
| --- | --- |
| run name | `mt4_reach_aware_stage0_standoff2cm_128env_600iter_video` |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| num envs | `128` |
| max iterations | `600` |
| seed | `42` |
| training time | `590.19 s` |
| checkpoint used for demo | `model_599.pt` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video` |

Command:

```bash
MT4_MAX_ITERATIONS=600 ./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh --video --video_length 240 --video_interval 2400 --run_name mt4_reach_aware_stage0_standoff2cm_128env_600iter_video
```

Demo command:

```bash
MT4_CHECKPOINT=/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/model_599.pt ./scripts/play_mirobot_coordinate_stage0_demo_60s.sh
```

## Videos

Training videos copied into the repo:

- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-7200.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-9600.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-12000.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-14400.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-16800.mp4`

Learned-policy demo:

- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/play/rl-video-step-0.mp4`
  - duration: `59.983333 s`
  - size: `1,854,549 bytes`

## Final Metrics

| metric | final |
| --- | ---: |
| `Train/mean_reward` | `7256.13` |
| `workspace_entry_success_rate` | `0.0000` |
| `workspace_entry_new_success_rate` | `0.0000` |
| `mean_distance` | `0.0449 m` |
| `mean_workspace_entry_error` | `0.0100 m` |
| `workspace_entry_radius_rate` | `0.9177` |
| `mean_approach_lateral_error` | `0.0323 m` |
| `approach_lateral_ready_rate` | `0.0000` |
| `mean_approach_standoff_error` | `0.0107 m` |
| `approach_standoff_ready_rate` | `0.9270` |
| `approach_phase_latched_rate` | `0.0000` |
| `inside_workspace_rate` | `0.0349` |
| `target_three_camera_visible_rate` | `0.8967` |
| `fine_center_4cm_rate` | `0.8708` |
| `near_center_7cm_rate` | `0.9299` |

## Analysis

Reducing the pre-entry standoff from `3.5 cm` to `2.0 cm` helped the standoff axis condition. The final `approach_standoff_ready_rate` reached `0.9270`, and the mean standoff error settled at `1.07 cm`.

The run still did not produce successful Stage 0 entries because the lateral pre-entry gate is too tight for the learned posture. The final mean lateral error was `3.23 cm`, while the latch threshold remains `1.5 cm`. Because `approach_lateral_ready_rate` stayed at `0.0000`, `approach_phase_latched_rate` also stayed at `0.0000`, and success remained blocked by design.

The policy did learn useful partial behavior: workspace proximity improved substantially, with `workspace_entry_radius_rate=0.9177`, `mean_workspace_entry_error=1.00 cm`, and `target_three_camera_visible_rate=0.8967`. However, it tends to approach a near-workspace pose without satisfying the strict lateral latch, so the next productive change is to relax or redefine that gate rather than further reducing standoff.

## Recommendation

Do not move to Stage 1 yet.

The next Stage 0 pass should relax `top_down_xy_success_radius` from `0.015 m` to about `0.035 m`, or replace the lateral latch with a gate based on `workspace_entry_radius_rate` plus camera visibility. This matches the observed learned lateral error while still requiring the robot to approach from the intended reachable side.
