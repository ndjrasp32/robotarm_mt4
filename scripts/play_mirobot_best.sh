#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/mirobot_arm_test"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
TASK_NAME="Mirobot-Reach-Pregrasp-Direct-v0"
BEST_FILE="${PROJECT_DIR}/logs/plots/best_checkpoint.txt"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
export DISPLAY="${DISPLAY:-:1}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

if [[ ! -f "${BEST_FILE}" ]]; then
  echo "[ERROR] best_checkpoint.txt was not found."
  echo "        Expected path: ${BEST_FILE}"
  echo "        Run scripts/plot_and_select_mirobot_best.sh first."
  exit 1
fi

CHECKPOINT="$(tr -d '\r\n' < "${BEST_FILE}")"
if [[ -z "${CHECKPOINT}" || ! -f "${CHECKPOINT}" ]]; then
  echo "[ERROR] Invalid checkpoint recorded in ${BEST_FILE}:"
  echo "        ${CHECKPOINT}"
  exit 1
fi

if command -v xdpyinfo >/dev/null 2>&1 && ! xdpyinfo -display "${DISPLAY}" >/dev/null 2>&1; then
  echo "[WARN] DISPLAY=${DISPLAY} is not accessible from this shell."
  echo "       If you are using VNC, run this in the VNC terminal first:"
  echo "       xhost +SI:localuser:${USER}"
fi

echo "[INFO] Playing ${TASK_NAME}"
echo "[INFO] checkpoint=${CHECKPOINT}"

./isaaclab.sh -p "${PROJECT_DIR}/tools/rsl_rl/play_mirobot.py" \
  --task "${TASK_NAME}" \
  --checkpoint "${CHECKPOINT}" \
  "$@"

