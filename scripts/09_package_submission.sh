#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUB="${1:?usage: $0 submissions/SUBMISSION_ID}"
SUB="$(realpath "$SUB")"; ID="$(basename "$SUB")"
for f in setup.sh run.sh requirements.txt README.md inference.py config.json; do [[ -f "$SUB/$f" ]] || { echo "missing $f" >&2; exit 1; }; done
mkdir -p "$ROOT/artifacts/zips"
(cd "$(dirname "$SUB")" && zip -qr "$ROOT/artifacts/zips/$ID.zip" "$ID" -x "$ID/.venv/*" "$ID/**/__pycache__/*")
sha256sum "$ROOT/artifacts/zips/$ID.zip" > "$ROOT/artifacts/zips/$ID.sha256"
echo "$ROOT/artifacts/zips/$ID.zip"
