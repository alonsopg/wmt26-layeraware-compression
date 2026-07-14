---
base_model: google/gemma-3-12b-it
library_name: transformers
pipeline_tag: text-generation
license: gemma
language:
- en
- zh
- cs
- de
- ar
tags:
- wmt26
- machine-translation
- bitsandbytes
- quantization
---

# Native Layer-Aware MLP-q4 Extension

This constrained-track system applies native BitsAndBytes NF4 only to the 144 text-transformer MLP `gate_proj`, `up_proj`, and `down_proj` modules. Attention projections, embeddings, norms, the language-model head, and vision modules remain BF16. It uses no calibration or fine-tuning data.

- Base model: `google/gemma-3-12b-it`
- Runtime: PyTorch + Transformers + BitsAndBytes
- Model artifact: mixed MLP-q4/BF16 model at `workdir/model`, or set `MODEL_DIR` when running.

This is the deployment-relevant extension of the selected-layer codec hypothesis. Unlike the codec ablation, quantized weights remain native 4-bit tensors at inference.

## Setup

```bash
bash setup.sh
```

`setup.sh` installs this submission's runtime dependencies and the organizer `modelzip` helper package into `./.venv`. When running outside the organizer repository, set `MODELZIP_SOURCE`.

## Compress

```bash
bash compress.sh
```

`compress.sh` is optional documentation/reproducibility support. It applies NF4 with double quantization only to the 144 text-transformer MLP gate/up/down projections and serializes the mixed checkpoint under `workdir/model`.

## Run

```bash
bash run.sh --lang-pair eng-zho_Hans --batch-size 8 --input input.txt --output output.txt
```

## Local validation

On 332 reference-backed WMT25 English–Chinese records, this system obtained 28.30 chrF and 31.37 BLEU, compared with 27.67 chrF and 30.80 BLEU for the organizer global-q4 baseline. Peak local VRAM was 14.64 GiB on an RTX A6000. These development results are not official WMT26 scores.
