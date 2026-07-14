#!/usr/bin/env bash
set -euo pipefail
root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
project_root=$(cd "$root_dir/../.." && pwd)
export MODEL_DIR="${MODEL_DIR:-$project_root/artifacts/models/cache/google/gemma-3-12b-it}"
source "$project_root/env/.venv/bin/activate"
python "$root_dir/inference.py" --model "$MODEL_DIR" "$@"
