# 2026-05-18 13:13:25 MT4 Simulation Mapping GUI

## Purpose

Add a GUI check that matches the current training/deployment interface instead of moving raw URDF joints directly.

The viewer drives only the four hardware-facing MT4 command fields:

| MT4 SDK field | Isaac policy joint |
| --- | --- |
| `X` | `joint_1` |
| `Y` | `joint_2_1` |
| `Z` | `joint_3` |
| `A` | `gripper_body_joint` |

Internal simulation targets are still sent to the full MT4 asset:

- `joint_2_2 = joint_2_1`
- `joint_4 = 0.65`
- `joint_l4 = 0.35`

## Commands

```bash
./scripts/show_mt4_hardware_mapping_gui.sh
./scripts/show_mt4_hardware_mapping_gui.sh --profile workspace
```

Use `axis-sweep` to inspect one real command axis at a time. Use `workspace` to inspect combined poses that look closer to actual reach/pregrasp use.

## What To Check In GUI

- `X` should rotate the base/yaw behavior.
- `Y` should move the shoulder/linkage side and `joint_2_2` should follow it internally.
- `Z` should move the main lift/elbow behavior.
- `A` should rotate the gripper body.
- `joint_4` and `joint_l4` should not appear as independently policy-controlled axes. If the visual linkage looks wrong while the four command axes look correct, the next fix should be a calibrated passive-linkage relation inside `_action_to_sim_joint_pos()`, not adding those joints to the policy action.

## Verification

Both profiles were smoke-tested headless:

```bash
./scripts/show_mt4_hardware_mapping_gui.sh --headless --profile axis-sweep --move_time 0.02 --hold_time 0.01 --settle_time 0.01 --post_time 0.01
./scripts/show_mt4_hardware_mapping_gui.sh --headless --profile workspace --move_time 0.02 --hold_time 0.01 --settle_time 0.01 --post_time 0.01
```
