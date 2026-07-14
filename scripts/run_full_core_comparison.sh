#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/env/.venv/bin/python"; SCRIPT="$ROOT/scripts/benchmark_direct.py"
SRC="$ROOT/data/prepared/modelzip_work/tests/eng-zho_Hans/wmt25-ref.eng-zho_Hans.eng"
REF="$ROOT/data/prepared/modelzip_work/tests/eng-zho_Hans/wmt25-ref.eng-zho_Hans.zho_Hans"
run_one() {
  local id="$1" model="$2" codec="${3:-}"
  "$ROOT/scripts/run_with_gpu_trace.sh" "full_$id" "$PY" "$SCRIPT" --system-id "$id" --model "$model" --input "$SRC" --reference "$REF" --output "$ROOT/results/predictions/${id}.full331.txt" --result "$ROOT/results/metrics/full_${id}.json" --batch-size 8 $codec
}
run_one baseline-bf16 "$ROOT/artifacts/models/cache/google/gemma-3-12b-it"
run_one organizer-bnb-q4 "$ROOT/submissions/layeraware-primary/workdir/model"
run_one layeraware-native-mlp-q4 "$ROOT/submissions/layeraware-native-mlp-q4/workdir/model"
run_one iwslt-storage-codec-q3 "$ROOT/artifacts/models/cache/google/gemma-3-12b-it" --codec-q3
