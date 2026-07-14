#!/usr/bin/env python
"""Measure exact q3+Zstd selected-weight payload and total tensor payload estimate."""
import argparse, gc, json, time
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument("--model",required=True,type=Path); p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    import torch
    from numcodecs import Quantize, Zstd
    from safetensors import safe_open
    q=Quantize(digits=3,dtype="f4",astype="f2"); z=Zstd(level=3)
    total_raw=selected_raw=selected_encoded=0; selected_count=0; started=time.perf_counter()
    for shard in sorted(a.model.glob("*.safetensors")):
        with safe_open(shard,framework="pt",device="cpu") as f:
            for key in f.keys():
                tensor=f.get_tensor(key); raw=tensor.numel()*tensor.element_size(); total_raw+=raw
                selected=(key.startswith("language_model.model.layers.") and key.endswith(("mlp.gate_proj.weight","mlp.up_proj.weight","mlp.down_proj.weight")))
                if selected:
                    array=tensor.float().numpy(); quantized=q.encode(array); encoded=z.encode(quantized)
                    selected_raw+=raw; selected_encoded+=len(encoded); selected_count+=1
                    del array,quantized,encoded
                    if selected_count%12==0: print(f"selected={selected_count}/144 encoded_gib={selected_encoded/2**30:.3f}",flush=True)
                del tensor; gc.collect()
    if selected_count!=144: raise RuntimeError(f"expected 144 selected tensors, got {selected_count}")
    auxiliary=sum(x.stat().st_size for x in a.model.iterdir() if x.is_file() and x.suffix!=".safetensors")
    result={"method":"Quantize(digits=3,dtype=f4,astype=f2)+Zstd(level=3)","selected_tensors":selected_count,"all_tensor_raw_bytes":total_raw,"selected_raw_bytes":selected_raw,"selected_encoded_bytes":selected_encoded,"nonselected_raw_bytes":total_raw-selected_raw,"auxiliary_files_bytes":auxiliary,"estimated_codec_artifact_bytes":total_raw-selected_raw+selected_encoded+auxiliary,"elapsed_seconds":time.perf_counter()-started}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result))
if __name__=="__main__": main()
