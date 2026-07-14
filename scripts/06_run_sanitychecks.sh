#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}" bash "$ROOT/external/wmt26-model-compression/evals/sanitycheck.sh" "$ROOT/submissions/layeraware-primary"
