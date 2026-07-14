#!/usr/bin/env python
"""Time processor load, model load, and generation separately in a fresh process."""
import argparse
import json
import time
from pathlib import Path

from modelzip.submission import Gemma3LLMBase, write_output_lines

class CodecQ3LLM(Gemma3LLMBase):
    @property
    def model(self):
        if self._model is None:
            import torch
            from transformers import Gemma3ForConditionalGeneration
            self._model = Gemma3ForConditionalGeneration.from_pretrained(
                self.model_dir, device_map={"": 0}, torch_dtype=torch.bfloat16, local_files_only=True
            )
            selected = 0
            with torch.no_grad():
                for name, module in self._model.named_modules():
                    if name.startswith("model.language_model.layers.") and name.endswith(("mlp.gate_proj", "mlp.up_proj", "mlp.down_proj")):
                        decoded = (module.weight.float().mul_(1024).round_().div_(1024).half()).to(torch.bfloat16)
                        module.weight.copy_(decoded); selected += 1
            if selected != 144: raise RuntimeError(f"expected 144 codec targets, got {selected}")
            self._model.eval()
        return self._model

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--system-id", required=True); p.add_argument("--model", required=True, type=Path)
    p.add_argument("--input", required=True, type=Path); p.add_argument("--reference", required=True, type=Path)
    p.add_argument("--output", required=True, type=Path); p.add_argument("--result", required=True, type=Path)
    p.add_argument("--batch-size", type=int, default=8); p.add_argument("--codec-q3", action="store_true")
    a=p.parse_args(); cls=CodecQ3LLM if a.codec_q3 else Gemma3LLMBase
    import torch
    torch.manual_seed(0)
    wall0=time.perf_counter(); llm=cls(a.model, use_chat_template=True)
    t=time.perf_counter(); _=llm.processor; processor_s=time.perf_counter()-t
    t=time.perf_counter(); _=llm.model; model_s=time.perf_counter()-t
    lines=a.input.read_text().splitlines()
    torch.cuda.reset_peak_memory_stats()
    t=time.perf_counter(); outputs=llm.translate_lines("eng-zho_Hans", lines, batch_size=a.batch_size); generation_s=time.perf_counter()-t
    a.output.parent.mkdir(parents=True, exist_ok=True); a.output.write_text("\n".join(x.replace("\n"," ") for x in outputs)+"\n")
    from sacrebleu.metrics import BLEU, CHRF
    refs=a.reference.read_text().splitlines()
    result={"system_id":a.system_id,"batch_size":a.batch_size,"lines":len(lines),"processor_load_seconds":processor_s,"model_load_seconds":model_s,"generation_seconds":generation_s,"generation_seconds_per_line":generation_s/len(lines),"end_to_end_seconds":time.perf_counter()-wall0,"torch_peak_allocated_mib":torch.cuda.max_memory_allocated()/2**20,"chrf":CHRF(lowercase=True).corpus_score(outputs,[refs]).score,"bleu":BLEU(lowercase=True,tokenize="zh").corpus_score(outputs,[refs]).score,"valid_line_count":len(outputs)==len(lines),"output":str(a.output)}
    a.result.parent.mkdir(parents=True, exist_ok=True); a.result.write_text(json.dumps(result,indent=2)+"\n"); print(json.dumps(result))

if __name__ == "__main__": main()
