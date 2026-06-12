#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"

cd "${PROJECT_DIR}"
python3 -m compileall -q source tools
./scripts/inspect_mirobot_asset.sh

cd "${ISAACLAB_DIR}"
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi
./isaaclab.sh -p - <<'PY'
from isaaclab.app import AppLauncher

app_launcher = AppLauncher(headless=True)
simulation_app = app_launcher.app

import gymnasium as gym
import mirobot_reach_direct

spec = gym.spec("Mirobot-Reach-Pregrasp-Direct-v0")
print("[OK] registered", spec.id)
print("[OK] env cfg", spec.kwargs["env_cfg_entry_point"])

simulation_app.close()
PY
