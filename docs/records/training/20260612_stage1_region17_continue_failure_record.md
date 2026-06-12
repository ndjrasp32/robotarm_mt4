# 2026-06-12 Stage 1 region 17 추가 학습 실패 기록

## 요약

17번 영역만 focus해서 기존 17번 run의 마지막 체크포인트에서 800 iteration을 추가 학습했다. 실제 MT4 하드웨어 motion은 실행하지 않았고 IsaacLab simulation만 사용했다.

결과는 실패다. 17번은 추가 학습 후에도 `success_count=0`, `mastered=0`으로 남았다. 카메라 region 판정과 접근 XY는 대부분 맞지만, 최종 tool-tip 중심 거리가 12mm 성공 반경 안으로 들어가지 못한다.

## 실행

| 항목 | 값 |
| --- | --- |
| task | `Mirobot-Coordinate-Plane-Direct-v0` |
| base checkpoint | `2026-06-12_19-02-07_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_128env_1200iter/model_1199.pt` |
| run name | `mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_continue_128env_800iter` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_23-13-19_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_continue_128env_800iter` |
| num envs | `128` |
| 추가 학습 | `800` iterations, resumed from `model_1199.pt` |
| final checkpoint | `model_1998.pt` |
| video | train video enabled, play video recorded with `num_envs=1` |

Command:

```bash
MT4_FOCUS_REGION=17 MT4_MAX_ITERATIONS=800 ./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh --video --video_length 300 --video_interval 2400 --resume --load_run 2026-06-12_19-02-07_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_128env_1200iter --checkpoint model_1199.pt --run_name mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_continue_128env_800iter
```

## 실패 위치

17번 target center:

| region | x | y | z |
| ---: | ---: | ---: | ---: |
| 17 | `-0.068000` | `-0.019000` | `0.079000` |

실패는 이 좌표 주변에서 반복됐다. 최종 평균 distance는 `0.0316 m`, run 중 최저 평균 distance는 step `1822`의 `0.0295 m`였다. 즉 정책은 17번 중심에서 약 `3 cm` 근처까지 접근하지만, 현재 성공 조건인 `center_success_radius=0.012 m`를 한 번도 만족하지 못했다.

## 지표

| metric | final | best |
| --- | ---: | ---: |
| success rate | `0.0000` | `0.0000` |
| region 17 success count | `0` | `0` |
| region 17 mastered | `0` | `0` |
| mean distance | `0.0316 m` | `0.0295 m` |
| center 12mm rate | `0.0000` | `0.0000` |
| center 3cm rate | `0.9021` | `0.9246` |
| fine center 4cm rate | `0.9197` | `0.9377` |
| mean top-down XY error | `0.0119 m` | `0.0097 m` |
| top-down XY 12mm rate | `0.8484` | `0.8916` |
| top-down height ready rate | `0.9290` | `0.9465` |
| gripper-camera target visible rate | `0.9287` | `0.9458` |
| inside workspace rate | `0.6204` | `0.6584` |

## 영상

학습 영상:

- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_23-13-19_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_continue_128env_800iter/videos/train/rl-video-step-24000.mp4`

보기 쉬운 1환경 play 영상:

- `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_23-13-19_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_continue_128env_800iter/videos/play/rl-video-step-0.mp4`

## 판단

17번은 단순 추가 학습으로 뚫리지 않았다. `top_down_xy_success_radius_rate`와 camera visibility는 충분히 높지만 `center_success_radius_rate`가 끝까지 0이라, 병목은 영역 인식보다 마지막 2 cm 정도의 중심 접근/하강 조건이다. 다음 실험은 성공 반경을 넓히는 것보다 17번 근처에서 center-distance reward를 더 직접적으로 주거나, 17번/18번을 비교해서 `y=-0.019` 방향 편향을 보정하는 쪽이 맞다.
