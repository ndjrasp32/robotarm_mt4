# 2026-06-11 MT4 Stage 1 plane XY 3.5cm 완화 분석

## 한국어

### 범위

이 실행은 Stage 1 3x3 plane localization에서 lateral/top-down XY gate와 center success radius를 모두 `0.035 m`로 완화한 결과다. 모든 실행은 IsaacLab simulation에서만 진행했고, 실제 MT4 로봇 motion은 실행하지 않았다.

이전 이어달리기 run은 이름에는 `035`가 있었지만 `env.yaml`에는 `center_success_radius=0.030`으로 남아 있었다. 이번 변경은 코드 기본값과 스크립트 설명을 함께 고쳐 같은 혼선을 막는다.

### 코드/스크립트 변경

| 파일 | 변경 |
| --- | --- |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | `MT4CoordinatePlaneEnvCfg`의 `center_success_radius`와 `top_down_xy_success_radius`를 `0.035 m`로 설정했다. |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | `top_down_xy_success_radius_rate` 로그를 추가하고, `top_down_xy_1cm_rate`는 이름 그대로 1cm 고정 지표로 정리했다. |
| `scripts/train_mirobot_coordinate_stage1_plane_128_600.sh` | Stage 1 성공 조건 설명과 기본 run name을 `035` 기준으로 갱신했다. |
| `scripts/play_mirobot_coordinate_stage1_plane_demo_60s.sh` | Stage 1 plane checkpoint 60초 demo 기록 스크립트를 추가했다. |

### 학습 실행

| 항목 | 값 |
| --- | --- |
| run name | `mt4_coordinate_plane_9cell_xy035_center035_128env_600iter` |
| task | `Mirobot-Coordinate-Plane-Direct-v0` |
| num envs | `128` |
| max iterations | `600` |
| seed | `42` |
| resume checkpoint | `2026-06-11_19-56-55_mt4_coordinate_plane_9cell_035_continue_128env_600iter/model_2396.pt` |
| training time | `521.99 s` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter` |

학습 명령:

```bash
MT4_MAX_ITERATIONS=600 ./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh --video --video_length 240 --video_interval 2400 --resume --load_run 2026-06-11_19-56-55_mt4_coordinate_plane_9cell_035_continue_128env_600iter --checkpoint model_2396.pt --run_name mt4_coordinate_plane_9cell_xy035_center035_128env_600iter
```

데모 명령:

```bash
MT4_CHECKPOINT=/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/model_2400.pt ./scripts/play_mirobot_coordinate_stage1_plane_demo_60s.sh
```

### 영상

저장소에 복사한 학습 영상:

- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-7200.mp4`
- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-9600.mp4`
- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-12000.mp4`
- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-14400.mp4`
- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/train/rl-video-step-16800.mp4`

학습된 policy 데모:

- `training_logs/videos/2026-06-11_20-14-22_mt4_coordinate_plane_9cell_xy035_center035_128env_600iter/play/rl-video-step-0.mp4`
  - checkpoint: `model_2400.pt`
  - duration: `59.983333 s`
  - resolution: `1280x720`
  - size: `1.7M`

### 최종 지표와 최고 지표

| 지표 | 최종값 | 최고값 |
| --- | ---: | ---: |
| `Train/mean_reward` | `11134.65` | `20596.38` at step `2414` |
| `plane_localization_success_rate` | `0.0000` | `0.1116` at step `2397` |
| `plane_localization_new_success_rate` | `0.0000` | `0.0293` at step `2397` |
| `plane_localization_success_hold_rate` | `0.0000` | `0.9241` at step `2399` |
| `mastered_region_count` | `4` | `4` from step `2404` |
| `mean_distance` | `0.0532 m` | - |
| `mean_plane_error` | `0.0177 m` | - |
| `camera_region_entry_rate` | `0.9363` | `0.9675` |
| `camera_region_match_rate` | `1.0000` | `1.0000` |
| `top_down_xy_success_radius_rate` | `0.0000` | `0.2852` at step `2397` |
| `top_down_phase_latched_rate` | `0.0000` | `0.9297` at step `2399` |
| `target_three_camera_visible_rate` | `0.7991` | `0.8921` |
| `center_success_radius_rate` | `0.0000` | `0.2153` at step `2398` |
| `near_center_7cm_rate` | `0.9019` | `0.9456` |

### 분석

`0.035 m` 완화는 실제로 blocker를 열었다. 이전 `0.010 m` XY gate에서는 `approach_lateral_ready_rate=0`으로 막혔지만, 이번 run 초반에는 `top_down_phase_latched_rate=0.9297`, `success_hold_rate=0.9241`, `mastered_region_count=4`까지 올라갔다.

하지만 학습 후반에는 active region 8에서 policy가 안정화되지 못하고 lateral error가 다시 커졌다. 최종 `mean_top_down_xy_error=0.0481 m`가 완화 threshold `0.035 m`를 넘어서면서 최종 batch success는 다시 0이 됐다. 즉 이번 수정은 gate 설계 문제는 풀었지만, sequential region progression이 다음 region에서 policy를 무너뜨리는 문제가 남았다.

### 다음 판단

Stage 1은 아직 Stage 2로 승격하지 않는다. 다만 `mastered_region_count=4`가 나왔기 때문에 Stage 1 접근 자체는 유효하다. 다음 시도는 `top_down_xy_success_radius`를 더 키우기보다, mastered region을 유지하면서 다음 region으로 넘어갈 때 policy가 붕괴하지 않도록 `region_mastery_successes`를 늘리거나 active-region sampling을 섞는 쪽이 맞다.

## English

This run relaxed Stage 1 plane localization to `center_success_radius=0.035 m` and `top_down_xy_success_radius=0.035 m`. It opened the previous XY-gate blocker: peak `top_down_phase_latched_rate` reached `0.9297`, peak `success_hold_rate` reached `0.9241`, and `mastered_region_count` reached `4`.

The final policy regressed on the active region, ending with final batch success at `0.0000` and final `mean_top_down_xy_error=0.0481 m`. Stage 1 should not advance to Stage 2 yet; the next useful change is stabilizing sequential region progression rather than widening the gate further.
