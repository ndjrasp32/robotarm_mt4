#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"

echo "[WARN] stage1_volume is deprecated. Run Stage 1 plane first:"
echo "[WARN]   ${PROJECT_DIR}/scripts/train_mirobot_coordinate_stage1_plane_128_600.sh"
echo "[WARN] Forwarding to Stage 2 volume for compatibility."

exec "${PROJECT_DIR}/scripts/train_mirobot_coordinate_stage2_volume_128_600.sh" "$@"
