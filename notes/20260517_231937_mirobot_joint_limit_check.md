# 2026-05-17 23:19:43 Mirobot Joint Limit Check

## Summary

- generated_at: 2026-05-17 23:19:43 KST
- task: `Mirobot-Reach-Pregrasp-Direct-v0`
- urdf: `/home/spark-robotics/work/robotarm/robotarm_mt4/assets/urdf/mirobot_wlkata_isaac_clean.urdf`
- all_urdf_position_limits_match_isaac_runtime: `True`
- all_urdf_velocity_limits_match_isaac_runtime: `True`
- all_urdf_effort_limits_match_isaac_runtime: `False`
- action_env_clamps_match_urdf_for_policy_joints: `True`
- oversized_positive_action_clamped_by_env: `True`
- oversized_negative_action_clamped_by_env: `True`

## Important Finding

URDF position lower/upper limits are present and are reflected in IsaacLab `default_joint_pos_limits` and runtime `joint_pos_limits`.
The current task also has matching action clamp limits for the six policy-controlled joints. `joint_2_2` is loaded in simulation and follows `joint_2_1` internally, but is not exposed as a policy action.
Velocity limits are also preserved from the URDF in this run. Effort limits are not preserved: the URDF says effort=10, while the current task actuator configuration writes effort=800.

## Joint Table

| joint | urdf_rad | urdf_deg | isaac_default_rad | isaac_runtime_rad | soft_rad | env_clamp_rad | home_rad | velocity | urdf_velocity | effort | urdf_effort | pos_match | velocity_match | effort_match | env_match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| joint_1 | [-1.570000, 1.570000] | [-89.95, 89.95] | [-1.570000, 1.570000] | [-1.570000, 1.570000] | [-1.570000, 1.570000] | [-1.570000, 1.570000] | 0.000000 | 9.999999 | 10.000000 | 800.000000 | 10.000000 | OK | OK | CHECK | OK |
| joint_2_1 | [-1.000000, 1.570000] | [-57.30, 89.95] | [-1.000000, 1.570000] | [-1.000000, 1.570000] | [-1.000000, 1.570000] | [-1.000000, 1.570000] | 0.350000 | 9.999999 | 10.000000 | 800.000000 | 10.000000 | OK | OK | CHECK | OK |
| joint_2_2 | [-1.000000, 1.570000] | [-57.30, 89.95] | [-1.000000, 1.570000] | [-1.000000, 1.570000] | [-1.000000, 1.570000] | - | 0.350000 | 9.999999 | 10.000000 | 800.000000 | 10.000000 | OK | OK | CHECK | OK |
| joint_3 | [0.000000, 1.570000] | [0.00, 89.95] | [0.000000, 1.570000] | [0.000000, 1.570000] | [0.000000, 1.570000] | [0.000000, 1.570000] | 0.750000 | 9.999999 | 10.000000 | 800.000000 | 10.000000 | OK | OK | CHECK | OK |
| joint_4 | [0.000000, 1.570000] | [0.00, 89.95] | [0.000000, 1.570000] | [0.000000, 1.570000] | [0.000000, 1.570000] | [0.000000, 1.570000] | 0.650000 | 9.999999 | 10.000000 | 800.000000 | 10.000000 | OK | OK | CHECK | OK |
| joint_l4 | [0.000000, 1.570000] | [0.00, 89.95] | [0.000000, 1.570000] | [0.000000, 1.570000] | [0.000000, 1.570000] | [0.000000, 1.570000] | 0.350000 | 9.999999 | 10.000000 | 800.000000 | 10.000000 | OK | OK | CHECK | OK |
| gripper_body_joint | [-1.570000, 1.570000] | [-89.95, 89.95] | [-1.570000, 1.570000] | [-1.570000, 1.570000] | [-1.570000, 1.570000] | [-1.570000, 1.570000] | 0.000000 | 9.999999 | 10.000000 | 800.000000 | 10.000000 | OK | OK | CHECK | OK |

## Notes

- `pos_match=OK` means URDF lower/upper equals both Isaac default and runtime position limits.
- `velocity_match=OK` means Isaac runtime velocity limit equals the URDF velocity value.
- `effort_match=CHECK` is expected right now because `ImplicitActuatorCfg.effort_limit=800.0` overrides the URDF effort=10.
- `env_match=OK` means policy action clamp matches URDF for policy-controlled joints, or the joint is an internal sim joint.
- `soft_rad` currently equals runtime limits because `soft_joint_pos_limit_factor` is 1.0.
- `joint_2_2` is not a policy action. In `MirobotReachPregraspEnv`, its command target is copied from `joint_2_1`.
