# 2026-06-11 MT4 Stage 0 standoff 2cm 600iter 분석

## 범위

이 실행은 reach-aware pre-entry standoff를 `0.035 m`에서 `0.020 m`로 완화하고, Stage 0 학습 step을 늘린 뒤, random target 환경에서 60초 learned-policy demo를 기록한 결과다.

모든 실행은 IsaacLab simulation에서만 진행했다. 실제 MT4 로봇 motion은 실행하지 않았다.

## 코드/스크립트 변경

| 파일 | 변경 |
| --- | --- |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | reach-aware Stage 0 pre-entry target의 `approach_standoff_distance`를 `0.035 m`에서 `0.020 m`로 변경했다. |
| `scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh` | 기본 `MT4_MAX_ITERATIONS`를 `300`에서 `600`으로 늘리고 run name을 `600iter` 기준으로 갱신했다. |
| `scripts/play_mirobot_coordinate_stage0_demo_60s.sh` | 선택한 checkpoint와 random reset target을 사용해 60초 coordinate Stage 0 demo를 기록하는 스크립트를 추가했다. |

## 학습 실행

| 항목 | 값 |
| --- | --- |
| run name | `mt4_reach_aware_stage0_standoff2cm_128env_600iter_video` |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| num envs | `128` |
| max iterations | `600` |
| seed | `42` |
| training time | `590.19 s` |
| checkpoint used for demo | `model_599.pt` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video` |

학습 명령:

```bash
MT4_MAX_ITERATIONS=600 ./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh --video --video_length 240 --video_interval 2400 --run_name mt4_reach_aware_stage0_standoff2cm_128env_600iter_video
```

데모 명령:

```bash
MT4_CHECKPOINT=/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/model_599.pt ./scripts/play_mirobot_coordinate_stage0_demo_60s.sh
```

## 영상

저장소에 복사한 학습 영상:

- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-7200.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-9600.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-12000.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-14400.mp4`
- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/train/rl-video-step-16800.mp4`

학습된 policy 데모:

- `training_logs/videos/2026-06-11_16-51-01_mt4_reach_aware_stage0_standoff2cm_128env_600iter_video/play/rl-video-step-0.mp4`
  - duration: `59.983333 s`
  - size: `1,854,549 bytes`

## 최종 지표

| 지표 | 최종값 |
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

## 분석

pre-entry standoff를 `3.5 cm`에서 `2.0 cm`로 줄인 것은 standoff axis 조건에 도움이 됐다. 최종 `approach_standoff_ready_rate`는 `0.9270`까지 올라갔고 mean standoff error는 `1.07 cm`로 안정됐다.

하지만 Stage 0 entry 성공은 나오지 않았다. 이유는 lateral pre-entry gate가 학습된 자세에 비해 너무 빡빡했기 때문이다. 최종 mean lateral error는 `3.23 cm`였고 latch threshold는 `1.5 cm`로 남아 있었다. 그래서 `approach_lateral_ready_rate=0.0000`, `approach_phase_latched_rate=0.0000`이 유지됐고, success는 설계상 막혔다.

그래도 policy는 유용한 부분 동작을 학습했다. `workspace_entry_radius_rate=0.9177`, `mean_workspace_entry_error=1.00 cm`, `target_three_camera_visible_rate=0.8967`로 workspace 근접 능력은 크게 좋아졌다. 다만 strict lateral latch를 만족하지 못한 채 workspace 근처 pose로 접근하는 경향이 있으므로, 다음 생산적인 수정은 standoff를 더 줄이는 것이 아니라 gate를 완화하거나 재정의하는 것이다.

## 다음 판단

이 checkpoint에서는 아직 Stage 1로 넘어가지 않는다.

다음 Stage 0 pass는 `top_down_xy_success_radius`를 `0.015 m`에서 약 `0.035 m`로 완화하거나, lateral latch를 `workspace_entry_radius_rate`와 camera visibility 기반 gate로 바꾸는 쪽이 맞다. 이렇게 하면 관측된 learned lateral error와 맞으면서도 로봇이 의도한 reachable side에서 접근하도록 유지할 수 있다.
