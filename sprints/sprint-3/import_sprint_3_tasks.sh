#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=================================================================="
echo "    CONECTA NEXUS - SPRINT 3 TASK IMPORT WRAPPER                 "
echo "=================================================================="

python3 "${SCRIPT_DIR}/import_sprint_3_tasks.py"
