"""GPU tracing entry point; the shell wrapper is scripts/run_with_gpu_trace.sh."""
from pathlib import Path

GPU_TRACE_FIELDS = ["timestamp", "gpu_id", "memory_used_mib", "utilization_gpu_pct", "utilization_memory_pct", "run_id"]

def peak_mib(csv_path: str | Path) -> int | None:
    import csv
    with Path(csv_path).open() as f:
        values = [int(r["memory_used_mib"]) for r in csv.DictReader(f)]
    return max(values, default=None)
