# 2026-06-11 MT4 Stage 0 엔트리 게이트 600iter 분석

## 범위

이 실행은 Stage 0의 strict lateral pre-entry latch를 workspace-entry gate로 바꾼 결과다. lateral과 standoff 지표는 계속 기록하지만, phase latch는 gripper가 보수적인 workspace boundary의 `0.020 m` 안에 들어오고 body stereo camera와 gripper camera에서 target이 보일 때 열린다.

모든 실행은 IsaacLab simulation에서만 진행했다. 실제 MT4 로봇 motion은 실행하지 않았다.

## 코드/스크립트 변경

| 파일 | 변경 |
| --- | --- |
| `source/mirobot_reach_direct/mirobot_coordinate_curriculum_env.py` | `workspace_entry_phase_latch_by_entry` 추가. Stage 0 phase latch를 strict lateral/standoff latch 대신 workspace-entry radius와 three-camera visibility 기준으로 변경했다. |
| `scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh` | 기본 run name을 `mt4_reach_aware_stage0_entrygate_128env_600iter`로 바꾸고 success 설명을 정리했다. |

## 학습 실행

| 항목 | 값 |
| --- | --- |
| run name | `mt4_reach_aware_stage0_entrygate_128env_600iter` |
| task | `Mirobot-Coordinate-Workspace-Entry-Direct-v0` |
| num envs | `128` |
| max iterations | `600` |
| seed | `42` |
| training time | `590.84 s` |
| checkpoint used for demo | `model_599.pt` |
| run dir | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter` |

학습 명령:

```bash
MT4_MAX_ITERATIONS=600 ./scripts/train_mirobot_coordinate_stage0_workspace_entry_128_300.sh --video --video_length 240 --video_interval 2400
```

데모 명령:

```bash
MT4_CHECKPOINT=/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_coordinate_curriculum_direct/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/model_599.pt ./scripts/play_mirobot_coordinate_stage0_demo_60s.sh
```

## 영상

저장소에 복사한 학습 영상:

- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-0.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-2400.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-4800.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-7200.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-9600.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-12000.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-14400.mp4`
- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/train/rl-video-step-16800.mp4`

학습된 policy 데모:

- `training_logs/videos/2026-06-11_17-14-59_mt4_reach_aware_stage0_entrygate_128env_600iter/play/rl-video-step-0.mp4`
  - duration: `59.983333 s`
  - size: `1,856,697 bytes`

## 최종 지표

| 지표 | 최종값 |
| --- | ---: |
| `Train/mean_reward` | `19147.40` |
| `workspace_entry_success_rate` | `0.4839` |
| `workspace_entry_new_success_rate` | `0.0029` |
| `workspace_entry_success_hold_rate` | `0.8513` |
| `mean_distance` | `0.0466 m` |
| `mean_workspace_entry_error` | `0.0089 m` |
| `workspace_entry_radius_rate` | `0.9216` |
| `mean_approach_lateral_error` | `0.0386 m` |
| `approach_lateral_ready_rate` | `0.0000` |
| `mean_approach_standoff_error` | `0.0125 m` |
| `approach_standoff_ready_rate` | `0.9070` |
| `top_down_phase_ready_rate` | `0.7761` |
| `top_down_phase_latched_rate` | `0.9250` |
| `inside_workspace_rate` | `0.4856` |
| `target_three_camera_visible_rate` | `0.7795` |
| `fine_center_4cm_rate` | `0.5120` |
| `near_center_7cm_rate` | `0.9282` |

## 분석

entry-gate 변경으로 이전 hard blocker가 풀렸다. 직전 2cm standoff 실행은 `workspace_entry_radius_rate=0.9177`까지 갔지만, 학습된 lateral error가 strict `0.015 m` latch threshold보다 커서 `approach_phase_latched_rate=0.0000`에 머물렀다. 이번 실행에서도 lateral readiness는 `0.0000`이었지만, 새 entry gate 덕분에 phase latch가 `0.9250`까지 열렸다.

Stage 0은 이제 실제 workspace-entry 성공을 만든다. 최종 `workspace_entry_success_rate=0.4839`, `inside_workspace_rate=0.4856`, `descent/approach_entry_success_rate=0.4839`다. 다만 center target 정밀도는 아직 부족하다. `center_1cm_rate=0.0000`, `fine_center_4cm_rate=0.5120`이므로 최종 targeting policy가 아니라 Stage 0 entry policy로 보는 게 맞다.

남은 약점은 gripper-camera target visibility다. `target_three_camera_visible_rate=0.7795`는 Stage 0 학습에는 충분하지만 workspace-boundary rate `0.9216`보다 낮다. 즉 workspace 근처까지 간 일부 pose가 gripper camera에서 target을 못 봐서 손실된다.

## 다음 판단

Stage 0은 다음 curriculum pass를 시도할 만큼 좋아졌다. Stage 0에는 entry-gate latch를 유지한다. Stage 1 plane-localization은 약 50% 초기 workspace-entry success rate를 감수할 수 있을 때 이 policy에서 시작한다. Stage 1 bootstrap이 실패하면 lateral latch를 다시 조이기보다 gripper-camera visibility reward를 먼저 강화한다.
