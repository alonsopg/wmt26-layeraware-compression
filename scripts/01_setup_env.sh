#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if command -v python3.12 >/dev/null 2>&1; then DEFAULT_PYTHON="$(command -v python3.12)";
elif command -v uv >/dev/null 2>&1; then DEFAULT_PYTHON="$(uv python find 3.12)";
else DEFAULT_PYTHON="$(command -v python3)"; fi
PYTHON_BIN="${PYTHON_BIN:-$DEFAULT_PYTHON}"
if [[ -d "$ROOT/env/.venv" ]] && ! "$ROOT/env/.venv/bin/python" -c 'import sys; assert sys.version_info[:2] == (3,12)' 2>/dev/null; then
  rm -rf "$ROOT/env/.venv"
fi
"$PYTHON_BIN" -m venv "$ROOT/env/.venv"
source "$ROOT/env/.venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install -e "$ROOT/external/wmt26-model-compression"
python -m pip install 'torch==2.7.0' 'transformers>=4.51.1,<5' 'accelerate==1.6.0' 'bitsandbytes==0.45.3' sentencepiece safetensors 'huggingface_hub>=0.34.0,<1.0' datasets pandas numpy tqdm sacrebleu psutil pyyaml packaging
python -m pip freeze > "$ROOT/results/raw/python_freeze.txt"
dpkg-query -W -f='${Package}\t${Version}\n' > "$ROOT/results/raw/system_packages.txt" 2>/dev/null || true
