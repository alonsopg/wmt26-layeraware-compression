#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/results/raw"
mkdir -p "$OUT"

{
  echo "timestamp_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname: $(hostname)"
  echo "os_release:"
  cat /etc/os-release 2>&1 || true
  echo "kernel: $(uname -a)"
  echo "disk_space:"
  df -h "$ROOT" 2>&1 || true
  echo "ram:"
  free -h 2>&1 || true
  echo "cpu_count: $(getconf _NPROCESSORS_ONLN 2>/dev/null || nproc 2>/dev/null || true)"
  echo "cuda_version:"
  nvcc --version 2>&1 || true
  echo "python_versions:"
  command -v python 2>&1 || true
  python --version 2>&1 || true
  command -v python3 2>&1 || true
  python3 --version 2>&1 || true
  echo "environment:"
  echo "CONDA_PREFIX=${CONDA_PREFIX:-<unset>}"
  echo "VIRTUAL_ENV=${VIRTUAL_ENV:-<unset>}"
  if [[ -n "${HF_TOKEN:-}" ]]; then echo "HF_TOKEN=present"; else echo "HF_TOKEN=absent"; fi
  echo "huggingface_login_status:"
  if command -v hf >/dev/null 2>&1; then hf auth whoami 2>&1 || true
  elif command -v huggingface-cli >/dev/null 2>&1; then huggingface-cli whoami 2>&1 || true
  else echo "Hugging Face CLI unavailable"; fi
  echo "gpu_inventory:"
  nvidia-smi --query-gpu=index,name,memory.total,driver_version --format=csv 2>&1 || true
  echo "prior_iwslt_locations:"
  find "$HOME" -maxdepth 5 -type d \( -iname '*iwslt*compression*' -o -iname 'iwslt-2026-model-compression' \) 2>/dev/null | head -50
} > "$OUT/machine_report.txt"

nvidia-smi > "$OUT/nvidia_smi_initial.txt" 2>&1 || true
cat "$OUT/machine_report.txt"
