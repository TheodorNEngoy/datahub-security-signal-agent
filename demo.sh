#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HOME="$ROOT/home"
export PATH="$ROOT/.venv/bin:$PATH"

python "$ROOT/scripts/generate_cleanroom_metadata.py"
datahub lite import "$ROOT/metadata/cleanroom_security_catalog.json" >/tmp/datahub-agenthack-lite-import.log 2>&1 || {
  cat /tmp/datahub-agenthack-lite-import.log
  exit 1
}
python "$ROOT/src/security_signal_agent.py"
