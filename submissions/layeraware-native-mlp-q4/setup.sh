#!/usr/bin/env bash
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
venv_dir="$root_dir/.venv"
project_root=$(cd "$root_dir/../.." && pwd)
if [[ -n "${MODELZIP_SOURCE:-}" ]]; then
  modelzip_source="$MODELZIP_SOURCE"
elif [[ -d "$project_root/modelzip" && -f "$project_root/pyproject.toml" ]]; then
  modelzip_source="$project_root"
elif [[ -d "$project_root/external/wmt26-model-compression/modelzip" ]]; then
  modelzip_source="$project_root/external/wmt26-model-compression"
else
  echo "Cannot locate modelzip; set MODELZIP_SOURCE to the organizer repository, wheel, or package spec." >&2
  exit 1
fi

if [[ ! -x "$venv_dir/bin/python" ]]; then uv venv --python 3.12 "$venv_dir"; fi
source "$venv_dir/bin/activate"
uv pip install -r "$root_dir/requirements.txt"
uv pip install --no-deps -e "$modelzip_source"
