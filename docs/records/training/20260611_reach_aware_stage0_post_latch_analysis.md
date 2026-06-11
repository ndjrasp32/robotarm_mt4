# 2026-06-11 MT4 Stage 0 reach-aware post-latch 분석

Date: 2026-06-11

아래 실행은 모두 IsaacLab simulation에서만 진행했다. 실제 MT4 로봇 motion은 실행하지 않았다.

## 코드 변경

기존 top-down Stage 0은 gripper가 먼저 target 위에서 정렬된 뒤 수직으로 내려올 수 있다고 가정했다. 실제 기기를 손으로 움직여 본 hardware-range 확인 결과, 이 pose sequence는 MT4 linkage에서 안정적이지 않을 가능성이 컸다. 그래서 Stage 0을 reach-aware pre-entry phase로 바꿨다.

1. Approach axis: world `-X`.
2. Pre-entry staging point: `target - approach_axis * 0.035 m`. gripper를 base-facing side의 workspace 바깥에 둔다.
3. Latch condition: approach line에 대한 lateral error `0.015 m` 이하, standoff-axis error `0.020 m` 이하.
4. Latch 이후 pre-entry position reward를 끄고 workspace entry, target-center progress, visibility, inside-workspace bonus로 reward를 옮긴다.

구현 파일:

- `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py`
- `scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh`

## 실행

| 실행 | 목적 | 학습 시간 | run dir |
| --- | --- | ---: | --- |
| `mt4_reach_aware_stage0_128env_300iter_video` | 첫 reach-aware pre-entry reward 확인 | `289.62 s` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video` |
| `mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video` | latch 이후 setup reward 제거 및 entry reward 강화 | `293.86 s` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video` |

## 지표 비교

| 지표 | first reach-aware final | first best | post-latch final | post-latch best |
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

## 저장된 영상

첫 reach-aware 실행:

- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_15-48-51_mt4_reach_aware_stage0_128env_300iter_video/rl-video-step-7200.mp4`

Post-latch entry 실행:

- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_15-55-46_mt4_reach_aware_stage0_post_latch_entry_128env_300iter_video/rl-video-step-7200.mp4`

## 해석

첫 reach-aware reward는 새 pre-entry 아이디어가 동작한다는 점을 확인했다. policy는 standoff axis와 camera visibility를 학습했고 `approach_phase_latched_rate`는 `0.858398`까지 올라갔다. 하지만 workspace에 들어가기보다 pre-entry staging pose 근처에 머무는 동작을 학습해서 최종 `inside_workspace_rate`는 다시 `0.000000`이 됐다.

post-latch reward 수정은 이 failure mode를 완화했다. pre-entry phase가 latch되면 setup-position reward를 제거하고 workspace entry와 target-center progress에 보상을 주도록 바꿨다. 그 결과 Stage 0 신호가 생겼고, 최종 `success_rate=0.099365`, 최종 `inside_workspace_rate=0.104004`, 최대 `success_rate=0.158447`을 얻었다.

남은 bottleneck은 lateral precision이다. 현재 pre-entry lateral latch threshold는 `0.015 m`인데, 학습된 mean lateral error는 약 `0.037 m` 부근에서 안정된다. 즉 strict 1.5cm approach-line gate는 이 asset에서 실제 도달 가능한 자세보다 빡빡하다. 이 checkpoint에서 바로 Stage 1을 시작하지 말고, 한 번 더 Stage 0을 돌리면서 lateral pre-entry gate를 `0.035-0.040 m` 정도로 완화하거나 staging-line lateral threshold 대신 workspace-entry radius와 camera visibility 기반 latch를 쓰는 것이 맞다.
