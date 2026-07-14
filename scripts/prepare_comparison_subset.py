#!/usr/bin/env python
"""Create a deterministic reference-backed comparison set inside modelzip work."""
import argparse
import json
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--lines", type=int, default=32)
    p.add_argument("--lang-pair", default="eng-zho_Hans")
    p.add_argument("--name", default="cmp32")
    a = p.parse_args()
    root = Path(__file__).resolve().parents[1]
    d = root / "data/prepared/modelzip_work/tests" / a.lang_pair
    src = d / f"wmt25-ref.{a.lang_pair}.eng"
    ref = d / f"wmt25-ref.{a.lang_pair}.zho_Hans"
    meta = d / f"wmt25-ref.{a.lang_pair}.meta"
    src_lines, ref_lines, meta_lines = src.read_text().splitlines(), ref.read_text().splitlines(), meta.read_text().splitlines()
    if not (len(src_lines) == len(ref_lines) == len(meta_lines)):
        raise ValueError("source/reference/meta line count mismatch")
    n = min(a.lines, len(src_lines))
    outputs = {
        d / f"{a.name}.{a.lang_pair}.eng": src_lines[:n],
        d / f"{a.name}.{a.lang_pair}.zho_Hans": ref_lines[:n],
        d / f"{a.name}.{a.lang_pair}.meta": meta_lines[:n],
    }
    for path, lines in outputs.items(): path.write_text("\n".join(lines) + "\n")
    manifest = {"name": a.name, "lang_pair": a.lang_pair, "lines": n, "source": str(src), "reference": str(ref), "selection": "first_n_in_official_order"}
    (root / "data/manifests/comparison_subset.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest))

if __name__ == "__main__": main()
