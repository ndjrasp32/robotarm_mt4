# 2026-06-13 Stage 1 seq25 skip-stalled 전체 sweep 결과

## 요약

Stage 1 5x5 plane 순차 학습에 정체 영역 자동 skip을 추가하고, 영역 1-25 전체를 한 번 sweep했다. 실제 MT4 하드웨어 motion은 실행하지 않았고 IsaacLab simulation만 사용했다.

결과는 `14/25` 영역 mastered, `11/25` 영역 skipped다. 1-14번은 10회 이상 성공했고, 15-25번은 새 성공이 `3840` env steps 동안 나오지 않아 자동으로 skipped 처리됐다. 이 기록의 목적은 성공한 영역과 막힌 영역을 모두 남긴 뒤 다음 실험 대상을 좁히는 것이다.

## 변경

이번 실험을 위해 `Mirobot-Coordinate-Plane-Direct-v0` curriculum에 아래 기능을 추가했다.

| 항목 | 내용 |
| --- | --- |
| `MT4_REGION_STALL_STEPS` | 활성 영역에서 새 성공이 없는 기간이 이 값을 넘으면 영역을 skipped로 표시 |
| `region_skipped` | 영역별 skipped 상태를 TensorBoard와 CSV에 기록 |
| `skip_reason` | `region_mastery.csv`에 skip 이유 기록 |
| sweep script | `scripts/train_mirobot_coordinate_stage1_plane_sweep25_skip.sh` 추가 |

기본 실행 조건은 `MT4_MAX_ITERATIONS=3000`, `MT4_REGION_STALL_STEPS=3840`, `num_envs=128`이다.

## 실행 조건

| 항목 | 값 |
| --- | --- |
| task | `Mirobot-Coordinate-Plane-Direct-v0` |
| run name | `mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_15-19-11_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter` |
| num envs | `128` |
| max iterations | `3000` |
| 실제 진행 checkpoint | `model_2000.pt`까지 생성 |
| seed | `42` |
| plane shape | `5x5`, regions `1..25` |
| tool-tip down offset | `0.035 m` |
| center success radius | `0.012 m` |
| top-down XY success radius | `0.012 m` |
| mastery target | `10` successes per region |
| stall skip limit | `3840` env steps without new success |

Command:

```bash
./scripts/train_mirobot_coordinate_stage1_plane_sweep25_skip.sh
```

## 결과

| metric | final |
| --- | ---: |
| mastered regions | `14/25` |
| skipped regions | `11/25` |
| final active region number | `25` |
| final mean distance | `0.0334 m` |
| final success rate | `0.0000` |
| final top-down XY 12mm rate | `0.0000` |
| final center 3cm rate | `0.0000` |
| final gripper camera visible rate | `1.0000` |

Region mastery:

| region range | result |
| --- | --- |
| `1..14` | mastered |
| `15..25` | skipped: `no_new_success_for_3840_env_steps` |

영역별 성공 횟수:

| region | success_count | status |
| ---: | ---: | --- |
| 1 | 14 | mastered |
| 2 | 18 | mastered |
| 3 | 24 | mastered |
| 4 | 12 | mastered |
| 5 | 14 | mastered |
| 6 | 11 | mastered |
| 7 | 25 | mastered |
| 8 | 21 | mastered |
| 9 | 21 | mastered |
| 10 | 18 | mastered |
| 11 | 10 | mastered |
| 12 | 34 | mastered |
| 13 | 39 | mastered |
| 14 | 11 | mastered |
| 15-25 | 0 | skipped |

## 판단

이번 sweep는 "막히면 멈추지 않고 기록 후 다음 영역으로 넘긴다"는 목적은 달성했다. 1-14번은 자동으로 mastered 처리됐고, 15번부터는 모두 skip되어 전체 25개 영역의 상태가 `region_mastery.csv`에 남았다.

다만 이전 2026-06-12 run에서는 15번까지 mastered였는데 이번 run은 14번까지만 mastered다. 따라서 현재 조건에서 병목은 15번 전후로 보는 것이 맞다. 15-25는 단순 iteration 연장만으로는 바로 해결될 가능성이 낮고, 특히 높은 z row와 좌측 y 영역에서 center 12mm gate를 닫지 못하는 문제가 이어진다.

다음 실험은 전체 sweep을 더 길게 늘리기보다 `15`, `16`, `17`을 짧은 focus run으로 나눠서 비교해야 한다. 기록상 17번은 추가 학습 후에도 약 3cm 근처에서 12mm 중심 성공 반경을 못 닫았고, 18번 중앙은 성공 가능했다. 즉 영역 인식보다 마지막 중심 접근/하강 reward와 좌측 y 편향 보정이 핵심이다.

## 산출물

| 항목 | 경로 |
| --- | --- |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_15-19-11_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter` |
| latest checkpoint | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_15-19-11_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter/model_2000.pt` |
| region mastery | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_15-19-11_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter/region_mastery.csv` |
| workspace cells | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_15-19-11_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter/workspace_reach_limited_25_cells.md` |
