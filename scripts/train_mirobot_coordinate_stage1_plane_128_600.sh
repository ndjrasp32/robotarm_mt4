#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
TASK_NAME="Mirobot-Coordinate-Plane-Direct-v0"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-600}"

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 1: MT4 URDF reach-limited 3x3 camera-coordinate plane curriculum"
echo "[INFO] MT4 top-down reach-limited workspace center=(-0.078,0.00,0.103), size=(0.045,0.095,0.055)"
echo "[INFO] target cells advance sequentially from region 1 to 9 at x=-0.078 before depth expansion"
echo "[INFO] each region is mastered after 5 new successes; mastered regions stop producing reward"
echo "[INFO] success requires same camera cell, body stereo visibility, 45deg gripper-camera visibility, 3.5cm top-down XY gate, and 3.5cm center distance"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/rsl_rl/train_mirobot.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  --run_name mt4_coordinate_plane_seq9_5success_035_128env_600iter \
  "$@"
