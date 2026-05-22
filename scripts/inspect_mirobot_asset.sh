#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${HOME}/work/robotarm/robotarm_mt4"

cd "${PROJECT_DIR}"
python3 tools/inspect_mirobot_asset.py "$@"

