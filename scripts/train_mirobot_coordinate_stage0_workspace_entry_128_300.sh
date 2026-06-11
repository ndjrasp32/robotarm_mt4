#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
TASK_NAME="Mirobot-Coordinate-Workspace-Entry-Direct-v0"

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" || "${TERM}" == "unknown" ]]; then
  export TERM=xterm-256color
fi

MAX_ITERATIONS="${MT4_MAX_ITERATIONS:-600}"

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] Stage 0: MT4 URDF coordinate reach-aware workspace-entry curriculum"
echo "[INFO] action joints: joint_1, joint_2_1, joint_3, gripper_body_joint"
echo "[INFO] passive sim joints follow hardware-transfer mapping"
echo "[INFO] success requires gripper center inside the reach-limited workspace after a workspace-entry phase latch, body stereo visibility, and 45deg gripper-camera visibility"
echo "[INFO] num_envs=128 max_iterations=${MAX_ITERATIONS} headless=true"

"${ISAACLAB_DIR}/isaaclab.sh" -p "${PROJECT_DIR}/tools/rsl_rl/train_mirobot.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations "${MAX_ITERATIONS}" \
  --headless \
  --seed "${MT4_SEED:-42}" \
  --run_name mt4_reach_aware_stage0_entrygate_128env_600iter \
  "$@"
