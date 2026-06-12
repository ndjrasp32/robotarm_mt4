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

MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-1200}"
FOCUS_REGION="${MT4_FOCUS_REGION:-}"
TOOL_TIP_DOWN_OFFSET="${MT4_TOOL_TIP_DOWN_OFFSET:-0.035}"
TOOL_TIP_DOWN_MM="$(python3 -c 'import os; print(int(round(float(os.environ.get("MT4_TOOL_TIP_DOWN_OFFSET", "0.035")) * 1000)))')"
RUN_FOCUS_SUFFIX=""
if [[ -n "${FOCUS_REGION}" ]]; then
  RUN_FOCUS_SUFFIX="_region${FOCUS_REGION}"
fi

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 1: MT4 URDF reach-limited 5x5 camera-coordinate plane curriculum"
echo "[INFO] MT4 arm/end workspace center=(-0.068,0.00,0.103), size=(0.045,0.095,0.055)"
echo "[INFO] virtual tool-tip is shifted ${TOOL_TIP_DOWN_OFFSET}m along body -Z and target workspace is shifted downward for the future down-mounted gripper"
echo "[INFO] target cells advance sequentially from region 1 to 25 at x=-0.068 before depth expansion"
if [[ -n "${FOCUS_REGION}" ]]; then
  echo "[INFO] focus region override: region ${FOCUS_REGION} only"
fi
echo "[INFO] each region is mastered after 10 new successes; mastered regions stop producing reward"
echo "[INFO] success requires same camera cell, body stereo visibility, 45deg gripper-camera visibility, 1.2cm top-down XY gate, and 1.2cm center distance"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/rsl_rl/train_mirobot.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  --run_name mt4_coordinate_plane_seq25_10success_012_tipdown${TOOL_TIP_DOWN_MM}mm${RUN_FOCUS_SUFFIX}_128env_${MAX_ITERATIONS}iter \
  "$@"
