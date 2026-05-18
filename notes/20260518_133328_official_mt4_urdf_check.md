# Official WLKATA MT4 URDF Check

Date: 2026-05-18 13:33:28 KST

## Why this check exists

The local SolidWorks-derived Mirobot/MT4 asset was useful for early IsaacLab bring-up, but the joint-limit GUI sweep showed behavior that looked mechanically disconnected. Since the learning policy is intended to transfer to the physical MT4 arm, the simulation asset should match the vendor model as closely as possible instead of simplifying away the linkage.

## Official source used

- Repository: `https://github.com/wlkata/Wlkata_MT4_ROS2`
- Checked local clone commit: `aee2ad2b689dc04cef145f491e4cf257c7ee95bc`
- Source URDF: `wlkata_mt4_description/urdf/wlkata_mt4_description.urdf`
- Local pinned copy: `assets/urdf/wlkata_mt4_official/wlkata_mt4_official.urdf`
- Local mesh copy: `assets/urdf/wlkata_mt4_official/meshes/`
- Isaac-generated USD: `assets/usd/wlkata_mt4_official/wlkata_mt4_official.usd`

## Joint structure found in the official URDF

The official MT4 arm model exposes four active revolute joints:

| SDK field | Official URDF joint | Lower rad | Upper rad | Lower deg | Upper deg |
| --- | --- | ---: | ---: | ---: | ---: |
| X | `joint1` | -2.094 | 2.443 | -120.0 | 140.0 |
| Y | `joint2` | -0.575 | 0.994 | -32.9 | 56.9 |
| Z | `joint3` | -0.244 | 0.994 | -14.0 | 56.9 |
| A | `joint4` | -3.141 | 3.141 | -180.0 | 180.0 |

The remaining URDF joints model the MT4 parallel linkage:

- `joint5` mimics `joint2` with multiplier `1`.
- `joint6` mimics `joint3` with multiplier `-1`.
- `joint7` mimics `joint3` with multiplier `-1`.
- `joint8` mimics `joint2` with multiplier `1`.
- `joint9` mimics `joint3` with multiplier `-1`.
- `joint10` mimics `joint2` with multiplier `1`.
- `joint11` mimics `joint3` with multiplier `1`.

## Isaac import adjustment

Isaac/PhysX requires mimic revolute joints to have finite limits. The vendor URDF used `continuous` on the mimic linkage joints, so the local pinned copy was adjusted for Isaac import only:

- `joint5`, `joint6`, `joint7`, `joint8`, `joint9`, `joint10`, and `joint11` were changed from `continuous` to `revolute`.
- Finite limits `lower="-3.141"` and `upper="3.141"` were added to those mimic joints.
- The actual active joint limits from the vendor file were kept unchanged.

The importer is recorded in `tools/import_official_mt4_urdf.py`.

## Verification

The official URDF was imported with:

```bash
unset CMEEL_PREFIX
export TERM=xterm-256color
/home/spark-robotics/work/isaac/src/IsaacLab/isaaclab.sh -p tools/import_official_mt4_urdf.py
```

The import completed successfully and generated the USD asset under `assets/usd/wlkata_mt4_official/`. Isaac emitted only expected mimic velocity-limit warnings, because velocity limits on mimic joints are ignored after the mimic relationship is parsed.

Import summary:

- Parsed links: `12`
- Parsed joints: `11`
- USD prim count: `53`
- Joint-like USD prim count: `13`
- Articulation root count: `1`
- Rigid body count: `12`

## Gripper finding

This official MT4 URDF describes the arm body and linkage, but it does not include an actuated gripper finger model. That matches the hardware/software split seen in WLKATA materials: the arm trajectory uses `X/Y/Z/A`, while gripper or pump commands are separate tool/end-effector commands.

For transfer learning, the right split is therefore:

- Use the official MT4 URDF/USD for the arm body and kinematic linkage.
- Keep the policy arm action mapping aligned to physical `X/Y/Z/A`.
- Add the gripper/suction behavior as a separate end-effector tool action/model instead of pretending it is `joint4`.

## Next step

Create a second IsaacLab robot config/task variant that uses the official USD and active joints `joint1`, `joint2`, `joint3`, `joint4`. After that GUI sweep passes, migrate the training environment from the older local asset to the official MT4 asset.
