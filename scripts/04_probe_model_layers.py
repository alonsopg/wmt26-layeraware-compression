#!/usr/bin/env python
import argparse, csv
from pathlib import Path
from transformers import AutoConfig, AutoModelForCausalLM
from layeraware.layer_policy import classify

def main():
    p = argparse.ArgumentParser(); p.add_argument("--model", default="google/gemma-3-12b-it"); p.add_argument("--out", default="results/raw")
    a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    config = AutoConfig.from_pretrained(a.model)
    with (out / "gemma3_12b_config.json").open("w") as f: f.write(config.to_json_string())
    # Meta-device construction inspects names without allocating weights.
    with __import__('accelerate').init_empty_weights(): model = AutoModelForCausalLM.from_config(config)
    rows=[]
    for name, mod in model.named_modules():
        weight=getattr(mod,"weight",None)
        rows.append({"name":name,"class":type(mod).__name__,"shape":"x".join(map(str,weight.shape)) if weight is not None else "","policy":classify(name)})
    for filename, selected in (("gemma3_12b_modules.csv",rows),("gemma3_12b_linear_modules.csv",[r for r in rows if "Linear" in r["class"]]),("gemma3_12b_mlp_policy_candidates.csv",[r for r in rows if r["policy"]=="mlp_q4_candidate"])):
        with (out/filename).open("w",newline="") as f: w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(selected)
if __name__ == "__main__": main()
