# Method description

We evaluate whether the selected-layer compression hypothesis transfers from speech translation to text-only MT. Our native layer-aware policy quantizes the 144 `gate_proj`, `up_proj`, and `down_proj` modules in Gemma 3's 48 text-transformer blocks using BitsAndBytes NF4 with double quantization and BF16 compute. Attention projections, embeddings, normalization layers, the language-model head, and vision modules remain BF16. The resulting mixed checkpoint is directly serializable and retains its quantized representation in GPU memory.

As a bridge to the prior IWSLT work, we also apply `numcodecs.Quantize(digits=3, dtype="f4", astype="f2")` followed by Zstd level 3 to the same text-MLP projections. Since Zstd is lossless after quantization, quality is evaluated using the exact decoded q3 weights. Storage is measured by actually encoding all 144 selected tensors, while inference VRAM is measured after decoded weights are materialized.
