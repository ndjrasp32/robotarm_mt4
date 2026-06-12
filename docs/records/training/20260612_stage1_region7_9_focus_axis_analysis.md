# 2026-06-12 Stage 1 region 7/9 focus 접근축 분석

## 요약

7번과 9번은 로봇 기준으로 같은 상단열 병목으로 보고, 단일 영역 focus 학습을 같은 조건으로 비교했다. 두 run 모두 IsaacLab simulation에서만 실행했고 실제 MT4 로봇 motion은 실행하지 않았다.

결론은 단순히 step 수를 늘리면 해결되는 문제가 아니다. 7번과 9번 모두 1600 iteration 동안 성공 0회였고, 카메라 영역 인식과 x축 standoff는 대부분 충족했지만 y/z lateral 정렬이 2cm gate 안으로 들어가지 못했다.

## 제안과 실행

제안:

1. 7번만 추가 학습하지 않고, 7번과 9번을 같은 조건으로 분리 학습한다.
2. success, center distance, top-down XY, standoff, gripper-camera visibility를 비교해 위치 문제와 접근축/reward 문제를 분리한다.
3. 두 위치가 같은 패턴으로 실패하면 다음 단계는 더 긴 학습이 아니라 lateral precision reward 또는 상단열 접근 target 표현을 수정한다.

실행 조건:

| 항목 | 값 |
| --- | --- |
| task | `Mirobot-Coordinate-Plane-Direct-v0` |
| num envs | `128` |
| max iterations | `1600` |
| seed | `42` |
| center success radius | `0.020 m` |
| top-down XY success radius | `0.020 m` |
| region mastery target | `10` new successes |
| video | enabled, length `200`, interval `4800` |

실행 명령:

```bash
MT4_FOCUS_REGION=9 MT4_MAX_ITERATIONS=1600 ./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh --video --video_length 200 --video_interval 4800
```

7번 run은 같은 조건의 기존 run을 분석했다.

## Run 경로

| region | run dir |
| ---: | --- |
| 7 | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_12-36-15_mt4_coordinate_plane_seq9_10success_020_region7_128env_1600iter` |
| 9 | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_13-17-50_mt4_coordinate_plane_seq9_10success_020_region9_128env_1600iter` |

## 핵심 지표

| 지표 | region 7 final | region 7 best | region 9 final | region 9 best |
| --- | ---: | ---: | ---: | ---: |
| success rate | `0.0000` | `0.0000` | `0.0000` | `0.0000` |
| success count | `0` | `0` | `0` | `0` |
| center 2cm rate | `0.0000` | `0.0000` | `0.0000` | `0.0000` |
| center 3cm rate | `0.0000` | `0.0054` | `0.0000` | `0.0010` |
| near center 7cm rate | `0.9421` | `0.9448` | `0.9390` | `0.9436` |
| top-down XY 2cm rate | `0.0000` | `0.0005` | `0.0000` | `0.0000` |
| top-down standoff ready | `0.9373` | `0.9407` | `0.9407` | `0.9526` |
| mean distance | `0.0501 m` | `0.0500 m` min | `0.0512 m` | `0.0507 m` min |
| mean top-down XY error | `0.0460 m` | `0.0447 m` min | `0.0478 m` | `0.0455 m` min |
| mean standoff error | `0.0126 m` | `0.0117 m` min | `0.0129 m` | `0.0126 m` min |
| camera region match | `1.0000` | `1.0000` | `1.0000` | `1.0000` |
| camera region entry | `0.9670` | `0.9675` | `0.9661` | `0.9675` |
| gripper-camera visible | `0.8447` | `0.8911` | `0.7983` | `0.8303` |
| mean reward | `9563.0` | `9596.7` | `8604.7` | `8646.6` |

## 판단

카메라 인식 병목은 아니다. 두 run 모두 target camera region match가 `1.0000`이고, camera region entry도 최종 `0.966` 이상이다.

x축 접근 standoff도 주 병목이 아니다. top-down height/standoff ready가 두 run 모두 최종 약 `94%`다.

실패 지점은 y/z lateral 정렬이다. top-down XY 2cm gate는 region 7에서 최고 `0.0005`, region 9에서 최고 `0.0000`이고, 평균 top-down XY error는 최종 `4.6-4.8cm`에 머물렀다. 이 값은 기존 3.5cm 기준도 안정적으로 넘지 못하고, 2.0cm 기준에는 훨씬 부족하다.

따라서 7번과 9번은 위치 자체가 서로 다른 문제가 아니라 상단열 공통 접근/정밀 reward 문제로 보는 것이 맞다. 현재 reward는 근처 7cm까지 끌어오는 힘은 충분하지만, 마지막 2cm로 lateral을 닫는 압력이 약하다.

## 다음 조치

다음 실험은 단순 iteration 증가가 아니라 reward 구조를 바꿔야 한다.

1. `top_down_xy_weight`를 Stage 1 plane에서도 명시적으로 켜고, 7cm 안에서는 lateral precision reward를 강하게 준다.
2. center distance reward와 top-down XY reward를 분리해서, x축 standoff를 맞춘 뒤 y/z lateral을 계속 줄이도록 만든다.
3. 성공 전 latch가 없어도 2cm 근처의 dense reward가 유지되도록 `fine_center_radius`와 `precision_center_weight`를 상단열 focus run에서 강화한다.
4. 수정 후 region 7/9를 다시 600-800 iteration 정도로 짧게 비교한다. 여기서 top-down XY 2cm rate가 0에서 벗어나면 전체 1..9 순차 학습으로 되돌린다.

## 산출물

| region | latest checkpoint | latest video |
| ---: | --- | --- |
| 7 | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_12-36-15_mt4_coordinate_plane_seq9_10success_020_region7_128env_1600iter/model_1599.pt` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_12-36-15_mt4_coordinate_plane_seq9_10success_020_region7_128env_1600iter/videos/train/rl-video-step-9600.mp4` |
| 9 | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_13-17-50_mt4_coordinate_plane_seq9_10success_020_region9_128env_1600iter/model_1599.pt` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_13-17-50_mt4_coordinate_plane_seq9_10success_020_region9_128env_1600iter/videos/train/rl-video-step-9600.mp4` |

## Reward 보강 후 재검증

상단열 병목이 lateral precision으로 확인되어 Stage 1 plane reward를 보강했다.

코드 변경:

| 파일 | 변경 |
| --- | --- |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | Stage 1 plane에서 `precision_center_weight=12`, `fine_center_weight=18`로 강화 |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | `top_down_xy_weight=24`, `top_down_height_weight=2` 추가 |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | front-face reward에 7cm에서 2cm까지 줄어드는 top-down XY dense reward 추가 |

검증:

```bash
python3 -m py_compile source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py
MT4_FOCUS_REGION=7 MT4_MAX_ITERATIONS=800 ./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh --video --video_length 200 --video_interval 4800
MT4_FOCUS_REGION=9 MT4_MAX_ITERATIONS=800 ./scripts/train_mirobot_coordinate_stage1_plane_128_600.sh --video --video_length 200 --video_interval 4800
```

재검증 결과:

| 지표 | old region 7 / 1600 | new region 7 / 800 | old region 9 / 1600 | new region 9 / 800 |
| --- | ---: | ---: | ---: | ---: |
| success rate final | `0.0000` | `0.0042` | `0.0000` | `0.0000` |
| success rate best | `0.0000` | `0.0095` | `0.0000` | `0.0000` |
| mastered count final | `0` | `1` | `0` | `0` |
| region success count final | `0` | `2890.9` | `0` | `0` |
| center 2cm rate final | `0.0000` | `0.0051` | `0.0000` | `0.0000` |
| center 3cm rate final | `0.0000` | `0.0586` | `0.0000` | `0.0789` |
| fine center 4cm rate final | `0.0378` | `0.1167` | `0.0146` | `0.3110` |
| top-down XY 2cm rate final | `0.0000` | `0.0217` | `0.0000` | `0.0000` |
| top-down XY 2cm rate best | `0.0005` | `0.0862` | `0.0000` | `0.0000` |
| mean top-down XY error min | `0.0447 m` | `0.0375 m` | `0.0455 m` | `0.0437 m` |
| gripper-camera visible final | `0.8447` | `0.1006` | `0.7983` | `0.3267` |

판단:

7번은 reward 보강으로 성공 가능성이 열렸다. 기존 1600iter에서는 성공 0회였지만, 보강 후 800iter에서 region 7이 mastered로 올라갔고 top-down XY 2cm rate 최고값도 `0.0005 -> 0.0862`로 개선됐다.

9번은 아직 실패다. center 3cm와 fine center 4cm는 개선됐지만 top-down XY 2cm gate가 끝까지 0이라 성공 조건을 만들지 못했다. 즉 7/9가 완전히 동일한 병목은 아니고, 9번에는 y/z lateral closure 또는 자세/가시성 tradeoff가 추가로 남아 있다.

다음 수정은 9번 전용으로 해야 한다. 후보는 9번 상단 우측에서 lateral 축을 더 강하게 직접 보상하거나, gripper-camera visibility와 lateral precision이 서로 충돌하지 않도록 gripper-camera direction/visibility 보상 가중치를 낮추는 실험이다.

보강 후 산출물:

| region | checkpoint | latest video |
| ---: | --- | --- |
| 7 | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_13-42-14_mt4_coordinate_plane_seq9_10success_020_region7_128env_800iter/model_799.pt` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_13-42-14_mt4_coordinate_plane_seq9_10success_020_region7_128env_800iter/videos/train/rl-video-step-9600.mp4` |
| 9 | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_13-53-47_mt4_coordinate_plane_seq9_10success_020_region9_128env_800iter/model_799.pt` | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-12_13-53-47_mt4_coordinate_plane_seq9_10success_020_region9_128env_800iter/videos/train/rl-video-step-9600.mp4` |
