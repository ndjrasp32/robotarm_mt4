# 2026-06-12 Stage 1 seq25 tipdown35 1차 결과

## 요약

3x3 plane에서 5x5 plane으로 영역을 세분화하고, 영역을 로봇팔 쪽으로 10mm 당긴 뒤 35mm 낮춘 target workspace 기준으로 Stage 1 순차 학습을 실행했다. 실제 MT4 하드웨어 motion은 실행하지 않았고 IsaacLab simulation만 사용했다.

결과는 `15/25` 영역 mastered다. 1-15번은 10회 이상 성공했고, 16번부터는 1200 iteration 안에 성공하지 못했다. 새 성공 판정은 기존 20mm보다 엄격한 12mm center/top-down XY 기준이다.

## 실행 조건

| 항목 | 값 |
| --- | --- |
| task | `Mirobot-Coordinate-Plane-Direct-v0` |
| run name | `mt4_coordinate_plane_seq25_10success_012_tipdown35mm_128env_1200iter` |
| num envs | `128` |
| max iterations | `1200` |
| seed | `42` |
| arm/end workspace center | `(-0.068, 0.000, 0.103)` |
| target workspace center | `(-0.068, 0.000, 0.068)` |
| workspace size | `(0.045, 0.095, 0.055)` |
| plane shape | `5x5`, regions `1..25` |
| tool-tip down offset | `0.035 m` |
| center success radius | `0.012 m` |
| top-down XY success radius | `0.012 m` |
| camera cell success margin | `0.08` cell |
| mastery target | `10` successes per region |
| video | enabled, length `200`, interval `4800` |

Command:

```bash
./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh --video --video_length 200 --video_interval 4800
```

## 결과

| metric | final |
| --- | ---: |
| mastered regions | `15/25` |
| active region at end | `16` |
| final mean distance | `0.0376 m` |
| final camera region entry rate | `0.9155` |
| final camera region match rate | `1.0000` |
| final top-down XY 12mm rate | `0.7148` |
| final top-down XY 1cm rate | `0.2627` |
| final gripper camera visible rate | `0.9321` |
| final center 3cm rate | `0.6206` |
| final fine center 4cm rate | `0.8960` |

Region mastery:

| region range | result |
| --- | --- |
| `1..15` | mastered |
| `16` | active, `0` successes |
| `17..25` | not reached |

## 판단

로봇팔 쪽으로 10mm 당긴 5x5 영역은 하단/중단 15개 영역에서 작동했다. 3x3에서 7/9가 막혔던 것과 달리, 이번에는 5x5 기준 상단 이전의 `16`번, 즉 네 번째 높이 줄의 좌측 영역에서 병목이 시작됐다.

최종 16번에서 top-down XY 12mm rate는 높지만 `center_success_radius_rate`가 0이라, 성공 조건을 만족하려면 center distance 12mm 쪽을 더 직접적으로 닫아야 한다. 다음 실험은 16번 focus로 짧게 돌려서 높이 줄 병목인지 좌측 y 병목인지 분리하는 것이 맞다.

## 후속 focus run 정리

순차 run 이후 16, 21, 17, 18번을 같은 5x5/tipdown35 조건으로 개별 focus 학습했다.

| region | target center `(x, y, z)` | run | 결과 |
| ---: | --- | --- | --- |
| 16 | `(-0.068, -0.038, 0.079)` | `2026-06-12_17-01-46_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region16_128env_1200iter` | `region_mastery.csv` 미생성, 10회 mastery 실패 |
| 21 | `(-0.068, -0.038, 0.090)` | `2026-06-12_17-21-02_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region21_128env_1200iter` | `region_mastery.csv` 미생성, 10회 mastery 실패 |
| 17 | `(-0.068, -0.019, 0.079)` | `2026-06-12_19-02-07_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_128env_1200iter` | 1차 focus 실패 |
| 18 | `(-0.068, 0.000, 0.079)` | `2026-06-12_19-20-23_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region18_128env_1200iter` | `success_count=35`, `mastered=1` |
| 17 추가 | `(-0.068, -0.019, 0.079)` | `2026-06-12_23-13-19_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_region17_continue_128env_800iter` | `success_count=0`, `mastered=0` |

16/21은 둘 다 로봇 기준 좌측 끝열(`y=-0.038`)이지만, 21번은 16번보다 한 층 더 높다(`z=0.090` vs `0.079`). 17/18은 같은 높이 줄(`z=0.079`)에 있고, 18번이 중앙(`y=0.000`)이다. 따라서 17과 18은 미러 관계가 아니라, 18을 중심으로 17과 19가 좌우 미러처럼 배치된다.

현재 해석은 `18` 중앙은 학습 가능하지만 `17` 좌측 중앙 근처는 추가 학습 후에도 12mm center gate를 못 닫는다는 것이다. 17번 추가 run의 최종 평균 distance는 `0.0316 m`, run 중 최저 평균 distance는 `0.0295 m`라서 영역/가시성보다 마지막 중심 접근 보상이 병목이다. 자세한 실패 위치와 영상 경로는 `20260612_stage1_region17_continue_failure_record.md`에 따로 기록했다.

## 산출물

| 항목 | 경로 |
| --- | --- |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_16-25-12_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_128env_1200iter` |
| final checkpoint | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_16-25-12_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_128env_1200iter/model_1199.pt` |
| region mastery | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_16-25-12_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_128env_1200iter/region_mastery.csv` |
| workspace cells | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_16-25-12_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_128env_1200iter/workspace_reach_limited_25_cells.md` |
| latest video | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_16-25-12_mt4_coordinate_plane_seq25_10success_012_tipdown35mm_128env_1200iter/videos/train/rl-video-step-33600.mp4` |
