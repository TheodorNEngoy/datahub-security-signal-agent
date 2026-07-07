#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export HOME="$ROOT/home"
export PATH="$ROOT/.venv/bin:$PATH"

mkdir -p "$HOME/.datahub/lite"
cat >"$HOME/.datahubenv" <<EOF
gms:
  server: http://localhost:8080
lite:
  type: duckdb
  config:
    file: $HOME/.datahub/lite/datahub.duckdb
EOF

python "$ROOT/scripts/generate_cleanroom_metadata.py"
datahub lite import "$ROOT/metadata/cleanroom_security_catalog.json" >/tmp/datahub-agenthack-lite-import.log 2>&1 || {
  cat /tmp/datahub-agenthack-lite-import.log
  exit 1
}
python "$ROOT/src/security_signal_agent.py"
