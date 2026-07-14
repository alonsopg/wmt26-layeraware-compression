#!/usr/bin/env bash
set -euo pipefail

# Reproducibility recipe for the mixed native layer-aware artifact.

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
project_root=$(cd "$root_dir/../.." && pwd)
base_model="${BASE_MODEL_DIR:-$project_root/artifacts/models/cache/google/gemma-3-12b-it}"

"$root_dir/.venv/bin/python" "$project_root/scripts/prepare_layeraware_native.py" \
    --model "$base_model" \
    --module-csv "$project_root/results/raw/gemma3_12b_linear_modules.csv" \
    --output "${MODEL_DIR:-$root_dir/workdir/model}"
