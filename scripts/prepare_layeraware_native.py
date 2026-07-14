#!/usr/bin/env python
"""Serialize a mixed model: text MLP projections in NF4, all other modules BF16."""
import argparse
import csv
import json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--module-csv", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path)
    a = p.parse_args()
    if (a.output / "._OK").exists():
        print(f"Already prepared: {a.output}")
        return

    import torch
    from transformers import AutoProcessor, BitsAndBytesConfig, Gemma3ForConditionalGeneration

    rows = list(csv.DictReader(a.module_csv.open()))
    targets = {
        r["name"] for r in rows
        if r["name"].startswith("model.language_model.layers.")
        and r["policy"] == "mlp_q4_candidate"
        and r["name"].endswith(("gate_proj", "up_proj", "down_proj"))
    }
    all_linear = {r["name"] for r in rows}
    skip = sorted(all_linear - targets)
    if len(targets) != 144:
        raise ValueError(f"expected 144 text MLP projections, got {len(targets)}")
    qconfig = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        llm_int8_skip_modules=skip,
    )
    processor = AutoProcessor.from_pretrained(a.model, local_files_only=True)
    model = Gemma3ForConditionalGeneration.from_pretrained(
        a.model,
        local_files_only=True,
        device_map={"": 0},
        torch_dtype=torch.bfloat16,
        quantization_config=qconfig,
    )
    actual_targets = sorted(name for name, mod in model.named_modules() if mod.__class__.__name__ == "Linear4bit")
    if set(actual_targets) != targets:
        missing, extra = sorted(targets-set(actual_targets)), sorted(set(actual_targets)-targets)
        raise RuntimeError(f"mixed quantization mismatch: missing={missing[:5]} extra={extra[:5]}")
    a.output.mkdir(parents=True, exist_ok=True)
    processor.save_pretrained(a.output)
    model.save_pretrained(a.output, safe_serialization=True)
    policy = {"targets": actual_targets, "preserved_linear_modules": skip, "target_count": len(actual_targets), "base_model": str(a.model), "quantization": "NF4 double-quant; BF16 compute", "policy": "text MLP gate/up/down q4; non-MLP BF16"}
    (a.output / "layer_policy.json").write_text(json.dumps(policy, indent=2) + "\n")
    (a.output / "._OK").touch()
    print(f"Prepared {len(actual_targets)} selectively quantized modules at {a.output}")

if __name__ == "__main__": main()
