# 2026-06-11 MT4 학습 산출물 인덱스

## 한국어

이 문서는 2026-06-11 MT4 coordinate curriculum의 Stage 0과 Stage 1 변경, 학습 결과, 영상 산출물을 묶어 보는 인덱스다. 모든 실행은 IsaacLab simulation이며 실제 MT4 로봇 motion은 실행하지 않았다.

### 범위

top-down 수직 진입 가정이 실제 MT4 가동 범위에 맞지 않을 수 있어서 Stage 0을 reach-aware pre-entry 방식으로 바꿨다. 이후 lateral latch가 너무 빡빡한 문제가 보여서 최종적으로 workspace-entry gate를 사용했다.

### 주요 기록

| 문서 | 용도 |
| --- | --- |
| `docs/records/design/20260611_mt4_reach_limited_workspace_audit.md` | reach sampling과 최종 MT4 workspace 정의 |
| `docs/records/training/20260611_phase_split_stage0_analysis.md` | 첫 phase-split Stage 0 학습 분석 |
| `docs/records/training/20260611_phase_split_relaxed_stage0_analysis.md` | z-gate 완화 Stage 0 학습 분석 |
| `docs/records/training/20260611_reach_aware_stage0_post_latch_analysis.md` | reach-aware 비수직 접근과 post-latch 보상 분석 |
| `docs/records/training/20260611_reach_aware_stage0_standoff2cm_600iter_analysis.md` | standoff 2cm, 600iter, 60초 데모 분석 |
| `docs/records/training/20260611_reach_aware_stage0_entrygate_600iter_analysis.md` | workspace-entry gate, 600iter, 60초 데모 분석 |
| `docs/records/training/20260611_stage1_plane_xy035_center035_analysis.md` | Stage 1 plane XY/center 3.5cm 완화 분석 |
| `docs/records/training/20260612_stage1_seq9_5success_analysis.md` | Stage 1 순차 9영역, 5회 성공 mastery 분석 |
| `docs/records/training/20260610_stage0_workspace_entry_retrain.md` | 이전 strict workspace-entry 기준 |

### 영상

| 실행 | 영상 |
| --- | --- |
| `2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-34-18_mt4_phase_split_stage0_128env_300iter_video/rl-video-step-2400.mp4` |
| `2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_14-37-09_mt4_phase_split_progress_stage0_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_14-45-39_mt4_phase_split_relaxed_stage0_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video` | `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video` | `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-0.mp4`, `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-2400.mp4`, `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-4800.mp4`, `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-7200.mp4` |
| `2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video` | train: `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-0.mp4` ... `rl-video-step-16800.mp4`; demo: `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/play/rl-video-step-0.mp4` |
| `2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter` | train: `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-0.mp4` ... `rl-video-step-16800.mp4`; demo: `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/play/rl-video-step-0.mp4` |
| `2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter` | train: `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-0.mp4` ... `rl-video-step-16800.mp4`; demo: `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/play/rl-video-step-0.mp4` |

### 그래프

| 파일 | 용도 |
| --- | --- |
| `training_logs/figures/20260610_222412_stage0_reward.png` | Stage 0 reward trend |
| `training_logs/figures/20260610_222412_stage0_success_workspace.png` | Stage 0 success and workspace-entry trend |
| `training_logs/figures/20260610_222412_stage0_error.png` | Stage 0 distance and workspace error trend |
| `training_logs/figures/20260610_222412_stage0_visibility.png` | Stage 0 camera visibility trend |
| `logs/plots/20260612_seq9_5success/success_mastery_curve.png` | Stage 1 seq9 success and mastery trend |
| `logs/plots/20260612_seq9_5success/region_progress_curve.png` | Stage 1 seq9 active region and success counts |
| `logs/plots/20260612_seq9_5success/gate_error_curve.png` | Stage 1 seq9 gate rates and distance errors |

### 최신 결과 요약

최신 Stage 0 실행은 strict lateral latch 대신 workspace-entry phase gate를 사용했다. 이 변경으로 이전 latch blocker는 해소했고, lateral 지표는 성공 조건이 아니라 진단 지표로 남겼다.

| 지표 | 최종값 |
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

Stage 1 3x3 plane은 이 entry-gated Stage 0 policy에서 시도할 수 있다. 만약 Stage 1이 bootstrap에 실패하면 lateral constraint를 다시 조이기 전에 gripper-camera visibility를 먼저 개선한다.

최신 Stage 1 실행은 1번부터 9번까지 순차 영역 학습으로 바꾸고, 각 영역을 새 성공 5회에 mastered 처리했다. `mastered_region_count=9`를 step `428`에서 달성했고 최종 `region_mastery.csv`도 9개 영역 모두 mastered로 기록했다. 다만 모든 영역 mastered 뒤 reward가 마스킹되어 최종 `Train/mean_reward=0.00`이 됐고, final batch `success_rate=0.0073`이라 Stage 2로 넘기기 전 별도 eval이 필요하다.

## English

This record indexes the 2026-06-11 MT4 coordinate curriculum Stage 0 and Stage 1 artifacts after switching away from a top-down vertical-entry assumption. All runs were IsaacLab simulation only; no real MT4 robot motion was executed.

The latest Stage 0 run replaced the strict lateral latch with a workspace-entry phase gate. The latest Stage 1 run changed plane localization to sequential regions 1 through 9 with a 5-new-success mastery threshold. It reached `mastered_region_count=9`, but the final checkpoint still needs a separate eval before Stage 2 because final batch `success_rate=0.0073`.
