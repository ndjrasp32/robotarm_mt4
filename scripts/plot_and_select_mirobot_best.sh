#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/mirobot_arm_test"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
PLOTS_DIR="${PROJECT_DIR}/logs/plots"
BEST_FILE="${PLOTS_DIR}/best_checkpoint.txt"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

echo "[INFO] Plotting Mirobot training curves and checkpoint summaries..."
./isaaclab.sh -p "${PROJECT_DIR}/tools/plot_mirobot_training_and_checkpoints.py"

echo "[INFO] Selecting best Mirobot checkpoint..."
./isaaclab.sh -p "${PROJECT_DIR}/tools/select_best_mirobot_checkpoint.py"

if [[ ! -s "${BEST_FILE}" ]]; then
  echo "[ERROR] best_checkpoint.txt was not created or is empty."
  echo "        Expected path: ${BEST_FILE}"
  exit 1
fi

echo "[OK] Best checkpoint:"
cat "${BEST_FILE}"

