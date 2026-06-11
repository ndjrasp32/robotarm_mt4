#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
TASK_NAME="Mirobot-Coordinate-Plane-Direct-v0"
EXPERIMENT_DIR="${ISAACLAB_DIR}/logs/rsl_rl/mirobot_coordinate_curriculum_direct"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

CHECKPOINT="${MT4_CHECKPOINT:-}"
if [[ -z "${CHECKPOINT}" ]]; then
  CHECKPOINT="$(find "${EXPERIMENT_DIR}" -path "*/model_*.pt" -type f | sort -V | tail -n 1)"
fi

if [[ -z "${CHECKPOINT}" || ! -f "${CHECKPOINT}" ]]; then
  echo "[ERROR] No valid checkpoint found."
  echo "        Set MT4_CHECKPOINT=/path/to/model.pt or run Stage 1 training first."
  exit 1
fi

echo "[INFO] Recording 60s coordinate Stage 1 plane demo"
echo "[INFO] task=${TASK_NAME}"
echo "[INFO] checkpoint=${CHECKPOINT}"
echo "[INFO] random targets come from the 3x3 plane reset sampler"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/rsl_rl/play_mirobot.py" \
  --task "${TASK_NAME}" \
  --checkpoint "${CHECKPOINT}" \
  --num_envs "${MT4_DEMO_NUM_ENVS:-1}" \
  --video \
  --video_length "${MT4_DEMO_VIDEO_LENGTH:-3600}" \
  --headless \
  --seed "${MT4_DEMO_SEED:-123}" \
  "$@"
