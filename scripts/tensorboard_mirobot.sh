#!/usr/bin/env bash
set -euo pipefail

cd "${HOME}/work/isaac/src/IsaacLab"
./isaaclab.sh -p -m tensorboard.main --logdir logs/rsl_rl/mirobot_reach_pregrasp_direct "$@"

