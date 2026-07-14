#!/usr/bin/env bash
set -euo pipefail
root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
project_root=$(cd "$root_dir/../.." && pwd)
source "$project_root/env/.venv/bin/activate"
python -c 'import torch, transformers, numcodecs, modelzip'
