# 2026-06-11 MT4 Reach-Aware Stage 0 Entry-Gate / 600iter Analysis

## Scope

This run replaces the strict lateral pre-entry latch for Stage 0 with a workspace-entry gate. The lateral and standoff metrics are still logged, but the phase latch now opens when the gripper reaches the conservative workspace boundary within `0.020 m` while the target is visible from the body stereo cameras and the gripper camera.

All execution was IsaacLab simulation only. No real MT4 robot motion was executed.

## Code / Script Changes

| file | change |
| --- | --- |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | Added `workspace_entry_phase_latch_by_entry`; Stage 0 uses workspace-entry radius plus three-camera visibility for the phase latch instead of the strict lateral/standoff latch. |
| `scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh` | Updated the default run name to `mt4_reach_aware_stage0_entrygate_128env_600iter` and clarified the success description. |

## Training Run

| item | value |
| --- | --- |
| run name | `mt4_reach_aware_stage0_entrygate_128env_600iter` |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| num envs | `128` |
| max iterations | `600` |
| seed | `42` |
| training time | `590.84 s` |
| checkpoint used for demo | `model_599.pt` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter` |

Command:

```bash
MT4_MAX_ITERATIONS=600 ./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh --video --video_length 240 --video_interval 2400
```

Demo command:

```bash
MT4_CHECKPOINT=/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/model_599.pt ./scripts/play_mirobot_coordinate_stage0_demo_60s.sh
```

## Videos

Training videos copied into the repo:

- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-7200.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-9600.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-12000.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-14400.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-16800.mp4`

Learned-policy demo:

- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/play/rl-video-step-0.mp4`
  - duration: `59.983333 s`
  - size: `1,856,697 bytes`

## Final Metrics

| metric | final |
| --- | ---: |
| `Train/mean_reward` | `19147.40` |
| `workspace_entry_success_rate` | `0.4839` |
| `workspace_entry_new_success_rate` | `0.0029` |
| `workspace_entry_success_hold_rate` | `0.8513` |
| `mean_distance` | `0.0466 m` |
| `mean_workspace_entry_error` | `0.0089 m` |
| `workspace_entry_radius_rate` | `0.9216` |
| `mean_approach_lateral_error` | `0.0386 m` |
| `approach_lateral_ready_rate` | `0.0000` |
| `mean_approach_standoff_error` | `0.0125 m` |
| `approach_standoff_ready_rate` | `0.9070` |
| `top_down_phase_ready_rate` | `0.7761` |
| `top_down_phase_latched_rate` | `0.9250` |
| `inside_workspace_rate` | `0.4856` |
| `target_three_camera_visible_rate` | `0.7795` |
| `fine_center_4cm_rate` | `0.5120` |
| `near_center_7cm_rate` | `0.9282` |

## Analysis

The entry-gate change fixed the previous hard blocker. The prior 2cm standoff run reached `workspace_entry_radius_rate=0.9177` but kept `approach_phase_latched_rate=0.0000` because the learned lateral error stayed above the strict `0.015 m` latch threshold. In this run, lateral readiness still stayed at `0.0000`, but the new entry gate allowed the phase to latch at `0.9250`.

Stage 0 now produces real workspace-entry successes: final `workspace_entry_success_rate=0.4839`, `inside_workspace_rate=0.4856`, and `descent/approach_entry_success_rate=0.4839`. The policy is still not precise at the center target (`center_1cm_rate=0.0000`, `fine_center_4cm_rate=0.5120`), so this is a usable Stage 0 entry policy rather than a final targeting policy.

The main remaining weakness is gripper-camera target visibility. `target_three_camera_visible_rate=0.7795` is good enough to train Stage 0, but it is below the workspace-boundary rate of `0.9216`, so some near-entry poses are still lost because the gripper camera does not see the target.

## Recommendation

Stage 0 is now good enough to move to the next curriculum pass. Keep the entry-gate latch for Stage 0, and start the next Stage 1 plane-localization run from this policy only if the Stage 1 task can tolerate a roughly 50 percent initial workspace-entry success rate. If Stage 1 fails to bootstrap, the next Stage 0 improvement should increase gripper-camera visibility reward rather than tightening the lateral latch again.
