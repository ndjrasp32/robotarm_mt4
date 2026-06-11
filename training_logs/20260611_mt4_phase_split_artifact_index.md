# 2026-06-11 MT4 Phase-Split Training Artifact Index

## Scope

This commit records the MT4 coordinate curriculum work after switching to a top-down, phase-split Stage 0 gate. All runs are IsaacLab simulation only. No real MT4 robot motion was executed.

## Main Records

| file | purpose |
| --- | --- |
| `notes/20260611_mt4_reach_limited_workspace_audit.md` | Reach sampling audit and final MT4 workspace definition |
| `training_logs/20260611_mt4_phase_split_stage0_analysis.md` | First phase-split Stage 0 run analysis |
| `training_logs/20260611_mt4_phase_split_relaxed_stage0_analysis.md` | Relaxed z-gate Stage 0 run analysis |
| `training_logs/20260611_mt4_reach_aware_stage0_post_latch_analysis.md` | Reach-aware non-vertical Stage 0 runs and post-latch entry analysis |
| `training_logs/20260611_mt4_reach_aware_stage0_standoff2cm_600iter_analysis.md` | 2cm standoff, 600 iteration Stage 0 run with 60s learned-policy demo |
| `training_logs/20260611_mt4_reach_aware_stage0_entrygate_600iter_analysis.md` | Workspace-entry phase gate Stage 0 run with 60s learned-policy demo |
| `training_logs/20260610_222412_mt4_stage0_workspace_entry_retrain.md` | Previous strict workspace-entry baseline |

## Committed Videos

| run | videos |
| --- | --- |
| `2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video/rl-video-step-2400.mp4` |
| `2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video` | `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video` | train: `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-0.mp4` ... `rl-video-step-16800.mp4`; demo: `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/play/rl-video-step-0.mp4` |
| `2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter` | train: `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-0.mp4` ... `rl-video-step-16800.mp4`; demo: `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/play/rl-video-step-0.mp4` |

## Figures

| file | purpose |
| --- | --- |
| `training_logs/figures/20260610_222412_stage0_reward.png` | Stage 0 reward trend |
| `training_logs/figures/20260610_222412_stage0_success_workspace.png` | Stage 0 success and workspace-entry trend |
| `training_logs/figures/20260610_222412_stage0_error.png` | Stage 0 distance and workspace error trend |
| `training_logs/figures/20260610_222412_stage0_visibility.png` | Stage 0 camera visibility trend |

## Latest Result Summary

The latest Stage 0 run replaced the strict lateral latch with a workspace-entry phase gate. This fixed the previous latch blocker while preserving the lateral metrics as diagnostics.

| metric | final |
| --- | ---: |
| `workspace_entry_success_rate` | 0.4839 |
| `workspace_entry_radius_rate` | 0.9216 |
| `mean_workspace_entry_error` | 0.0089 m |
| `mean_approach_lateral_error` | 0.0386 m |
| `approach_lateral_ready_rate` | 0.0000 |
| `approach_standoff_ready_rate` | 0.9070 |
| `approach_phase_latched_rate` | 0.9250 |
| `inside_workspace_rate` | 0.4856 |
| `target_three_camera_visible_rate` | 0.7795 |

Stage 1 3x3 plane can now be attempted from this entry-gated Stage 0 policy. If Stage 1 fails to bootstrap, improve gripper-camera visibility before tightening lateral constraints again.
