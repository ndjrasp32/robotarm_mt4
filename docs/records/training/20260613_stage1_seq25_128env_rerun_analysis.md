# 2026-06-13 Stage 1 seq25 128env rerun 결과

## 요약

`Mirobot-Coordinate-Plane-Direct-v0`를 CUDA `cuda:0`, `num_envs=128`로 다시 실행했다. 목적은 5x5 plane 영역 `1..25`를 순차로 돌면서 영역별 10회 성공 시 mastered로 넘기고, 새 성공이 없는 영역은 `3840 env steps` 정체 기준으로 skipped 처리해 끝까지 기록하는 것이다.

실제 MT4 하드웨어 motion은 실행하지 않았고 IsaacLab simulation 학습만 수행했다.

최종 결과는 `14/25` mastered, `11/25` skipped다. `1..14` 영역은 10회 이상 성공했고, `15..25` 영역은 새 성공 없이 정체되어 모두 skipped로 기록됐다.

2026-06-13 17:38 KST 재실행에서는 전체 영역 기록 완료 시 trainer가 정상 종료되도록 코드가 보강됐다. 마지막 영역이 `active`로 남지 않고, runner가 `iteration 1880`에서 checkpoint를 저장한 뒤 종료했다.

2026-06-13 20:12 KST에 같은 조건을 Boss Bot `/chat`에서 다시 실행했고, 결과는 동일하게 `14/25` mastered, `11/25` skipped였다. 이번 실행도 `cuda:0`, `num_envs=128`로 돌았고, 전체 영역 기록 완료 후 `iteration 1880`에서 정상 종료했다.

## 실행 조건

| 항목 | 값 |
| --- | --- |
| task | `Mirobot-Coordinate-Plane-Direct-v0` |
| command | `MT4_MAX_ITERATIONS=3000 MT4_REGION_STALL_STEPS=3840 MT4_TOOL_TIP_DOWN_OFFSET=0.035 ./scripts/train_mirobot_coordinate_stage1_plane_sweep25_skip.sh --device cuda:0` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_17-38-14_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter` |
| stdout log | `training_logs/run_stdout/20260613_173809_seq25_128env_stall3840_after_stopfix.log` |
| num envs | `128` |
| device | `cuda:0` |
| seed | `42` |
| max iterations | `3000`, but stopped after all 25 regions were recorded |
| stopped iteration | `1880/3000` |
| training time | `1542.8s` |
| mastery target | `10` successes per region |
| stall skip limit | `3840 env steps without new success` |
| tool-tip down offset | `0.035 m` |

### 2026-06-13 20:12 KST rerun

| 항목 | 값 |
| --- | --- |
| command | `MT4_MAX_ITERATIONS=3000 MT4_REGION_STALL_STEPS=3840 MT4_SEED=42 ./scripts/train_mirobot_coordinate_stage1_plane_sweep25_skip.sh --device cuda:0` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_20-12-45_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter` |
| session log | `training_logs/session_logs/stage1_sweep25_128env_cuda_tmux_20260613_201240.log` |
| num envs | `128` |
| device | `cuda:0` |
| seed | `42` |
| stopped iteration | `1880/3000` |
| training time | `1594.5s` |
| final checkpoint | `model_1880.pt` |

## 결과

| metric | final |
| --- | ---: |
| mastered regions | `14/25` |
| skipped regions | `11/25` |
| final active region number | none; curriculum complete |
| final success rate | `0.0000` |
| final stop reason | all 25 regions recorded |

## Region mastery

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
| 15-25 | 0 | skipped: `no_new_success_for_3840_env_steps` |

## 대표 checkpoint

이번 coordinate run 전용 checkpoint 선택기는 별도로 없어서, 기존 `plot_and_select_mirobot_best.sh` 결과는 사용하지 않았다. 해당 스크립트는 예전 `mirobot_reach_pregrasp_direct` 실험을 선택하므로 이번 결과와 맞지 않는다.

이번 stop-fix run의 stdout 기준 최고 `Mean reward`는 iteration `1032`의 `24603.21`이다. 저장된 checkpoint 중 mean reward가 가장 높은 저장 지점은 iteration `1000`이고, 해당 checkpoint는 아래 파일이다.

`/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_17-38-14_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter/model_1000.pt`

최종 정상 종료 checkpoint는 `model_1880.pt`다. 다만 이번 선택은 stdout의 mean reward 기준이며, 별도 play/evaluation으로 검증한 best policy는 아니다.

20:12 KST rerun의 최종 정상 종료 checkpoint도 `model_1880.pt`다.

`/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-13_20-12-45_mt4_coordinate_plane_seq25_skipstalled3840_tipdown35mm_128env_3000iter/model_1880.pt`

## 코드 확인

- `region_mastery.csv`에서 curriculum complete 이후 active region이 남지 않도록 수정했다.
- `coordinate_curriculum/plane_localization_region_curriculum_complete` 로그를 추가했다.
- 모든 영역이 mastered/skipped로 기록되면 trainer가 checkpoint를 저장하고 정상 종료하도록 `train_mirobot.py`에 optional stop hook을 추가했다.
- 원시 stdout/session 로그는 크기가 커서 `training_logs/run_stdout/`, `training_logs/session_logs/`를 git ignore 처리하고, 요약 분석만 문서로 남긴다.

## 판단

이번 재실행도 이전 sweep와 같은 병목을 재현했다. 카메라 가시성은 유지되지만, 15번 이후 영역에서 중심 12mm/3cm gate를 닫지 못해 새 성공이 나오지 않는다. 단순히 max iteration을 늘리는 것보다 15번 이후, 특히 좌측/상단 계열 영역의 마지막 중심 접근과 하강 보상을 따로 손보는 편이 낫다.

다음 실험은 전체 25영역 반복보다 `MT4_FOCUS_REGION=15`, `16`, `17` 단기 focus run으로 나누고, `top_down_xy_weight`, `target_overshoot_penalty_weight`, `preferred_approach_weight`를 조정해 12mm 중심 접근 성공을 먼저 회복하는 방향이 맞다.
