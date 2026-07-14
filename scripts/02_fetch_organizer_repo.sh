#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/external/wmt26-model-compression"
if [[ -d "$DEST/.git" ]]; then git -C "$DEST" pull --ff-only; else git clone https://github.com/thammegowda/wmt26-model-compression "$DEST"; fi
git -C "$DEST" rev-parse HEAD
