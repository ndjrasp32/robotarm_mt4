# 2026-05-17 23:22:21 Mirobot Joint Limit GUI Sweep

## Summary

- purpose: GUI에서 각 policy-controlled joint가 URDF/action clamp의 lower/upper까지 움직이는지 짧게 확인
- command:

```bash
./scripts/sweep_mirobot_joint_limits_gui.sh --move_time 0.8 --hold_time 0.25 --settle_time 1.0 --post_time 2.0
```

## Sweep Order

1. `joint_1`: home -> lower -> upper -> home
2. `joint_2_1`: home -> lower -> upper -> home
3. `joint_3`: home -> lower -> upper -> home
4. `joint_4`: home -> lower -> upper -> home
5. `joint_l4`: home -> lower -> upper -> home
6. `gripper_body_joint`: home -> lower -> upper -> home

## Notes

- `joint_2_2` is not swept directly as a policy action.
- During the sweep, `joint_2_2` follows `joint_2_1` through `MirobotReachPregraspEnv._action_to_sim_joint_pos`.
- The sweep ran in Isaac Sim GUI on `DISPLAY=:1` and exited normally.
- This is a visual check, not a learning run.

