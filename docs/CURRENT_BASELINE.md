# Current Baseline - robotarm_mt4

Date: 2026-05-22 KST

## Repository Role

`robotarm_mt4` is the Mirobot/MT4 asset and hardware-transfer baseline repository.

Use this repo for:

- Mirobot/MT4 URDF/USD asset checks
- joint/action mapping and hardware-transfer notes
- Mars twin simulation checks close to the real asset
- visual inspection, plotting, and checkpoint utility scripts

Use `robotarm_student` for the broader student curriculum archive and staged classroom experiments.

## Current Baseline

Active task package:

- `source/mirobot_reach_direct`

Main task IDs:

- `Mirobot-Reach-Pregrasp-Direct-v0`
- `Mirobot-Mars-Twin-Pick-Direct-v0`
- `Mirobot-Mars-Twin-Place-Direct-v0`
- `Mirobot-Mars-Twin-Stack-Direct-v0`
- `Mirobot-Mars-Twin-Push-Direct-v0`
- `Mirobot-Mars-Twin-Pull-Direct-v0`

Current hardware-transfer rule:

- policy actions are limited to four MT4 command-facing joints
- mapping reference: `notes/20260518_111647_mt4_hardware_transfer_mapping.md`
- dynamic object contact reference: `notes/20260518_134455_dynamic_cube_target.md`

## Reset Rationale

The project was reset to this baseline because the previous working state had too many daily notes, renamed repositories, and mixed student/hardware responsibilities. From 2026-05-22, this repo is treated as the Mirobot/MT4 asset and hardware-transfer baseline, and older `notes/` entries remain archive instead of the daily source of truth.

## Practical Starting Point

Start here today:

1. Confirm the scene or task with the visual command.
2. Run one training command only after the scene looks correct.
3. Plot/select the checkpoint.
4. Update this file only if the baseline changes.

For visual inspection:

```bash
./scripts/view_mirobot_mars_twin_gui.sh --mission push
./scripts/view_mirobot_mars_twin_gui.sh --mission pull
```

For repeatable training:

```bash
./scripts/train_mirobot_reach_128_1000.sh
./scripts/train_mirobot_mars_twin.sh push
./scripts/plot_and_select_mirobot_best.sh
./scripts/play_mirobot_best.sh
```

## Documentation Policy

The existing `notes/` folder is historical archive. Keep it, but do not make it the daily entry point.

Daily starting order:

1. Read this file.
2. Check `README.md`.
3. Use linked notes only when you need the original decision detail.
4. Add new dated notes for new observations.
5. Update this file only when the MT4 asset, mapping, or task baseline changes.

Do not create a new note for routine command output. Keep routine output in terminal/log files and promote only decisions, changed assumptions, or stable results back into this baseline.

## Next Work

1. Keep this repo focused on MT4 asset fidelity, mapping, and safe simulation.
2. Verify push/pull contact behavior before treating pick/place/stack as stable.
3. Keep real robot motion behind the safety gate.
4. Record only one concise note per meaningful change or experiment.
5. Treat the current dated notes as archive unless this file links to them.
