# Controlled English–Chinese comparison

First 32 reference-backed WMT25 records; batch 8; deterministic greedy decoding on one RTX A6000. Generation time excludes processor/model loading. BLEU uses the SacreBLEU Chinese tokenizer.

| System | chrF | BLEU | ΔchrF vs BF16 | Gen s/line | Peak VRAM GiB | Artifact GiB |
|---|---:|---:|---:|---:|---:|---:|
| layeraware-native-mlp-q4 | 28.10 | 32.32 | +0.20 | 2.257 | 12.99 | 10.99 |
| baseline-bf16 | 27.90 | 32.10 | +0.00 | 1.434 | 24.77 | 22.74 |
| organizer-bnb-q8 | 27.70 | 31.83 | -0.20 | 3.928 | 15.71 | 12.34 |
| iwslt-storage-codec-q3 | 27.66 | 31.80 | -0.24 | 1.451 | 24.80 | 14.46 |
| organizer-bnb-q4 | 27.65 | 31.95 | -0.25 | 2.380 | 11.91 | 7.78 |

The storage-codec artifact size is an exact selected-weight q3+Zstd payload plus raw non-selected tensor bytes and auxiliary files. Its runtime uses quality-equivalent eager decoded weights, so generation/VRAM reflect the post-decode state; model-load time omits Zstd decode and is not directly comparable.

This 32-sentence sample is suitable for directional evidence, not a final significance claim.
