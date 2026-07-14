#!/usr/bin/env python
"""Quality-equivalent emulation of IWSLT selected-layer q3+Zstd decode.

The codec's decoded weights equal round(weight * 1024) / 1024 cast through FP16.
Zstd changes storage only, so it is not invoked in the forward path here. This keeps
the quality/VRAM comparison faithful but marks speed as emulated rather than exact.
"""
import logging as LOG
import time

from modelzip.submission import (
    DEF_MAX_NEW_TOKENS, DEF_MAX_NEW_TOKENS_OVER_INPUT, Gemma3LLMBase,
    TRANSLATE_PROMPT, default_model_path, parse_inference_args, run_inference,
)

LOG.basicConfig(level=LOG.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class StorageCodecQ3LLM(Gemma3LLMBase):
    @property
    def model(self):
        if self._model is None:
            import torch
            from transformers import Gemma3ForConditionalGeneration
            start = time.perf_counter()
            self._model = Gemma3ForConditionalGeneration.from_pretrained(
                self.model_dir, device_map={"": 0}, torch_dtype=torch.bfloat16, local_files_only=True
            )
            selected = 0
            with torch.no_grad():
                for name, module in self._model.named_modules():
                    if not name.startswith("model.language_model.layers."):
                        continue
                    if not name.endswith(("mlp.gate_proj", "mlp.up_proj", "mlp.down_proj")):
                        continue
                    # Exact Quantize(digits=3) grid; FP16 is the codec's encoded dtype.
                    decoded = (module.weight.float().mul_(1024).round_().div_(1024).half()).to(torch.bfloat16)
                    module.weight.copy_(decoded)
                    selected += 1
            if selected != 144:
                raise RuntimeError(f"expected 144 selected MLP projections, got {selected}")
            self._model.eval()
            LOG.info("Applied quality-equivalent selected-layer q3 codec decode to %d modules in %.3fs", selected, time.perf_counter()-start)
        return self._model

def parse_args():
    return parse_inference_args(
        default_model=default_model_path(__file__),
        description="IWSLT-style selected-layer q3+Zstd quality/VRAM ablation",
        default_prompt=TRANSLATE_PROMPT,
        default_max_new_tokens=DEF_MAX_NEW_TOKENS,
        default_max_new_tokens_over_input=DEF_MAX_NEW_TOKENS_OVER_INPUT,
    )

if __name__ == "__main__": run_inference(parse_args(), StorageCodecQ3LLM, use_chat_template=True)
