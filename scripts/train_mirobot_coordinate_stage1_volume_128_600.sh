#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
TASK_NAME="Mirobot-Coordinate-Volume-Direct-v0"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-600}"

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 1: MT4 URDF 3x3x3 camera-coordinate curriculum"
echo "[INFO] conservative workspace center=(0.305,0.00,0.205), size=(0.09,0.14,0.09)"
echo "[INFO] success requires same 3D cell, body stereo visibility, gripper camera visibility, and 1cm center distance"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/rsl_rl/train_mirobot.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  --run_name mt4_coordinate_volume_128env_600iter \
  "$@"
