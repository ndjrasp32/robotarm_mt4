# 2026-06-11 MT4 Phase-Split Training Artifact Index

## Scope

This commit records the MT4 coordinate curriculum work after switching to a top-down, phase-split Stage 0 gate. All runs are IsaacLab simulation only. No real MT4 robot motion was executed.

## Main Records

| file | purpose |
| --- | --- |
| `notes/20260611_mt4_reach_limited_workspace_audit.md` | Reach sampling audit and final MT4 workspace definition |
| `training_logs/20260611_mt4_phase_split_stage0_analysis.md` | First phase-split Stage 0 run analysis |
| `training_logs/20260611_mt4_phase_split_relaxed_stage0_analysis.md` | Relaxed z-gate Stage 0 run analysis |
| `training_logs/20260610_222412_mt4_stage0_workspace_entry_retrain.md` | Previous strict workspace-entry baseline |

## Committed Videos

| run | videos |
| --- | --- |
| `2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video/rl-video-step-2400.mp4` |
| `2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-7200.mp4` |

## Figures

| file | purpose |
| --- | --- |
| `training_logs/figures/20260610_222412_stage0_reward.png` | Stage 0 reward trend |
| `training_logs/figures/20260610_222412_stage0_success_workspace.png` | Stage 0 success and workspace-entry trend |
| `training_logs/figures/20260610_222412_stage0_error.png` | Stage 0 distance and workspace error trend |
| `training_logs/figures/20260610_222412_stage0_visibility.png` | Stage 0 camera visibility trend |

## Latest Result Summary

The relaxed phase-split Stage 0 run improved x/y top-down alignment and camera visibility, but did not pass the z/descent gate.

| metric | final |
| --- | ---: |
| `top_down_xy_1cm_rate` | 0.5415 |
| `top_down_height_ready_rate` | 0.0000 |
| `top_down_phase_latched_rate` | 0.0000 |
| `descent_phase_success_rate` | 0.0000 |
| `inside_workspace_rate` | 0.0000 |
| `target_three_camera_visible_rate` | 0.9004 |
| `workspace_entry_radius_rate` | 0.8538 |

Stage 1 3x3 plane and Stage 2 27-cell volume remain held until Stage 0 can latch the top-down setup and enter the workspace.
