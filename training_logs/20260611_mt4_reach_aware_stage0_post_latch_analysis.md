# MT4 reach-aware Stage 0 post-latch entry analysis

Date: 2026-06-11

All runs below are IsaacLab simulation only. No real MT4 robot motion was executed.

## Code change

The previous top-down Stage 0 assumed the gripper could first align above the target and then descend vertically. Manual hardware-range inspection suggested that pose sequence is not reliable for the MT4 linkage, so Stage 0 now uses a reach-aware pre-entry phase:

1. Approach axis: world `-X`.
2. Pre-entry staging point: `target - approach_axis * 0.035 m`, which places the gripper outside the workspace on the base-facing side.
3. Latch condition: lateral error to the approach line below `0.015 m` and standoff-axis error below `0.020 m`.
4. After latch, pre-entry position reward is disabled and reward shifts to workspace entry, target-center progress, visibility, and inside-workspace bonus.

Implementation files:

- `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py`
- `scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh`

## Runs

| run | purpose | training time | run dir |
| --- | --- | ---: | --- |
| `mt4_reach_aware_stage0_128env_300iter_video` | First reach-aware pre-entry reward | `289.62 s` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video` |
| `mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video` | Disable setup reward after latch and increase entry reward | `293.86 s` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video` |

## Metric comparison

| metric | first reach-aware final | first best | post-latch final | post-latch best |
| --- | ---: | ---: | ---: | ---: |
| `success_rate` | `0.000000` | `0.000977` | `0.099365` | `0.158447` |
| `success_hold_rate` | `0.000000` | `0.007812` | `0.650879` | `0.719727` |
| `approach_entry_success_rate` | `0.000000` | `0.000977` | `0.099365` | `0.158447` |
| `inside_workspace_rate` | `0.000000` | `0.228271` | `0.104004` | `0.228271` |
| `workspace_entry_radius_rate` | `0.721191` | `0.882324` | `0.856689` | `0.911133` |
| `mean_workspace_entry_error` | `0.025284 m` | `0.021476 m` | `0.016226 m` | `0.014910 m` |
| `approach_phase_latched_rate` | `0.832520` | `0.858398` | `0.801025` | `0.857666` |
| `mean_approach_lateral_error` | `0.039158 m` | `0.038415 m` | `0.037258 m` | `0.029300 m` |
| `approach_lateral_ready_rate` | `0.031494` | `0.036865` | `0.028076` | `0.054443` |
| `mean_approach_standoff_error` | `0.010700 m` | `0.009236 m` | `0.013154 m` | `0.008759 m` |
| `approach_standoff_ready_rate` | `0.917480` | `0.938721` | `0.877686` | `0.937988` |
| `target_three_camera_visible_rate` | `0.739502` | `0.906982` | `0.677490` | `0.879639` |
| `near_center_7cm_rate` | `0.822998` | `0.890381` | `0.916260` | `0.926514` |
| `fine_center_4cm_rate` | `0.000000` | `0.296631` | `0.142334` | `0.296631` |

## Videos copied into repo

First reach-aware run:

- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-7200.mp4`

Post-latch entry run:

- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-7200.mp4`

## Interpretation

The first reach-aware reward confirmed the new pre-entry idea: the policy learned the standoff axis and camera visibility, with `approach_phase_latched_rate` reaching `0.858398`. However, it learned to remain near the pre-entry staging pose instead of entering the workspace, so final `inside_workspace_rate` returned to `0.000000`.

The post-latch reward fix corrected that failure mode. Once the pre-entry phase latches, the setup-position reward is removed and the policy is paid for workspace entry and target-center progress. This produced a usable Stage 0 signal: final `success_rate=0.099365`, final `inside_workspace_rate=0.104004`, and max `success_rate=0.158447`.

The remaining bottleneck is lateral precision. The current pre-entry lateral latch threshold is `0.015 m`, while the learned mean lateral error settles around `0.037 m`. This suggests the strict 1.5 cm approach-line gate is still tighter than the practical reachable posture for this asset. Stage 1 should not start from this checkpoint yet; one more Stage 0 pass should either relax the lateral pre-entry gate to about `0.035-0.040 m` or make the latch use workspace-entry radius plus camera visibility instead of the staging-line lateral threshold.
