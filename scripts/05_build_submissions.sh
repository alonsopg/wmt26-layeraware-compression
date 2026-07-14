#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export MODELZIP_SOURCE="$ROOT/external/wmt26-model-compression"
export MODEL_CACHE="${MODEL_CACHE:-$ROOT/artifacts/models/cache}"
bash "$ROOT/submissions/layeraware-primary/setup.sh"
bash "$ROOT/submissions/layeraware-primary/compress.sh"
