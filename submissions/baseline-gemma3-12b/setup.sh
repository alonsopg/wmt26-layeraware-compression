#!/usr/bin/env bash
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
venv_dir="$root_dir/.venv"
project_root=$(cd "$root_dir/../.." && pwd)
modelzip_source="${MODELZIP_SOURCE:-$project_root/external/wmt26-model-compression}"

if [[ ! -x "$venv_dir/bin/python" ]]; then uv venv --python 3.12 "$venv_dir"; fi
source "$venv_dir/bin/activate"
uv pip install -r "$root_dir/requirements.txt"
uv pip install --no-deps -e "$modelzip_source"
