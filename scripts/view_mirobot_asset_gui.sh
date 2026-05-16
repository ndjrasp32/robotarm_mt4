#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/mirobot_arm_test"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
export DISPLAY="${DISPLAY:-:1}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

if command -v xdpyinfo >/dev/null 2>&1 && ! xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then
  echo "[ERROR] DISPLAY=${DISPLAY} is not accessible from this shell."
  echo "        If you are using VNC, run this in the VNC terminal first:"
  echo "        xhost +SI:localuser:${USER}"
  exit 1
fi

echo "[INFO] Opening Mirobot asset viewer on DISPLAY=${DISPLAY}"
./isaaclab.sh -p "${PROJECT_DIR}/tools/view_mirobot_asset.py" "$@"

