#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/env/.venv/bin/activate"
(cd "$ROOT/external/wmt26-model-compression" && python -m modelzip.setup --work "$ROOT/data/prepared/modelzip_work" --langs ces-deu eng-zho_Hans eng-ara_EG)
python "$ROOT/scripts/inventory_data.py"
