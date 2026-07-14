#!/usr/bin/env bash
set -uo pipefail
if [[ $# -lt 2 ]]; then echo "usage: $0 RUN_ID COMMAND [ARG ...]" >&2; exit 2; fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
run_id="$1"; shift
out="$ROOT/results/raw/gpu_traces/${run_id}.csv"
mkdir -p "$(dirname "$out")"
echo 'timestamp,gpu_id,memory_used_mib,utilization_gpu_pct,utilization_memory_pct,run_id' > "$out"
"$@" & cmd_pid=$!
while kill -0 "$cmd_pid" 2>/dev/null; do
  nvidia-smi --query-gpu=index,memory.used,utilization.gpu,utilization.memory --format=csv,noheader,nounits 2>/dev/null |
    while IFS=, read -r gpu mem ug um; do
      printf '%s,%s,%s,%s,%s,%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "${gpu// /}" "${mem// /}" "${ug// /}" "${um// /}" "$run_id" >> "$out"
    done
  sleep 1
done
wait "$cmd_pid"
