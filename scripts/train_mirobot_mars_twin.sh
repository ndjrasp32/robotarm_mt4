#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"
ISAACLAB_DIR="${HOME}/work/isaac/src/IsaacLab"
MISSION="${1:-push}"

case "${MISSION}" in
  pick) TASK_NAME="Mirobot-Mars-Twin-Pick-Direct-v0" ;;
  place) TASK_NAME="Mirobot-Mars-Twin-Place-Direct-v0" ;;
  stack) TASK_NAME="Mirobot-Mars-Twin-Stack-Direct-v0" ;;
  push) TASK_NAME="Mirobot-Mars-Twin-Push-Direct-v0" ;;
  pull) TASK_NAME="Mirobot-Mars-Twin-Pull-Direct-v0" ;;
  *)
    echo "[ERROR] Unknown mission: ${MISSION}"
    echo "        Use one of: pick place stack push pull"
    exit 1
    ;;
esac
shift || true

cd "${ISAACLAB_DIR}"
unset CMEEL_PREFIX
export PYTHONPATH="${PROJECT_DIR}/source:${PYTHONPATH:-}"
if [[ -z "${TERM:-}" || "${TERM}" == "dumb" ]]; then
  export TERM=xterm-256color
fi

echo "[INFO] Training ${TASK_NAME}"
echo "[INFO] num_envs=128 max_iterations=1200 headless=true"

./isaaclab.sh -p "${PROJECT_DIR}/tools/rsl_rl/train_mirobot.py" \
  --task "${TASK_NAME}" \
  --num_envs 128 \
  --max_iterations 1200 \
  --headless \
  "$@"
