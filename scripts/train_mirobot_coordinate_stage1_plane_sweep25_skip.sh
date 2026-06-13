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

MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-3000}"
REGION_STALL_STEPS="${MT4_REGION_STALL_STEPS:-3840}"
TOOL_TIP_DOWN_OFFSET="${MT4_TOOL_TIP_DOWN_OFFSET:-0.035}"
TOOL_TIP_DOWN_MM="$(python3 -c 'import os; print(int(round(float(os.environ.get("MT4_TOOL_TIP_DOWN_OFFSET", "0.035")) * 1000)))')"

export MT4_REGION_STALL_STEPS="${REGION_STALL_STEPS}"

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 1 sweep: regions 1..25 with stall-skip enabled"
echo "[INFO] target cells advance sequentially; mastered after 10 successes"
echo "[INFO] stalled active region is marked skipped after ${REGION_STALL_STEPS} env steps without a new success"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/rsl_rl/train_mirobot.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  --run_name mt4_coordinate_plane_seq25_skipstalled${REGION_STALL_STEPS}_tipdown${TOOL_TIP_DOWN_MM}mm_128env_${MAX_ITERATIONS}iter \
  "$@"
