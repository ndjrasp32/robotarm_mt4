# 2026-05-17 Mirobot joint upper-limit GUI sweep 기록

## 요약

- purpose: GUI에서 각 policy-controlled joint를 상한 최대각까지 한 번씩 이동시켜 확인
- command:

```bash
./scripts/sweep_mirobot_joint_limits_gui.sh --mode upper --move_time 1.8 --hold_time 1.4 --settle_time 1.5 --post_time 4.0
```

## sweep 순서

1. `joint_1`: home -> upper(max) -> home, upper `1.57` rad
2. `joint_2_1`: home -> upper(max) -> home, upper `1.57` rad
3. `joint_3`: home -> upper(max) -> home, upper `1.57` rad
4. `joint_4`: home -> upper(max) -> home, upper `1.57` rad
5. `joint_l4`: home -> upper(max) -> home, upper `1.57` rad
6. `gripper_body_joint`: home -> upper(max) -> home, upper `1.57` rad

## 메모

- Isaac Sim GUI opened on `DISPLAY=:1`.
- The script completed with exit code `0`.
- `joint_2_2` is not a policy action; it follows `joint_2_1` through `MirobotReachPregraspEnv._action_to_sim_joint_pos`.
- This run is a visual joint-limit check, not a learning run.
