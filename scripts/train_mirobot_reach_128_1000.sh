#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/mirobot_arm_test"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
TASK_NAME="Mirobot-Reach-Pregrasp-Direct-v0"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] num_envs=128 max_iterations=1000 headless=true"

./isaaclab.sh -p "${PROJECT_DIR}/tools/rsl_rl/train_mirobot.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations 1000 \
  --headless \
  "$@"

