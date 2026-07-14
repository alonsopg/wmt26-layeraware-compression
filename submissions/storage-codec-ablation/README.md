# IWSLT-Style Storage-Codec Ablation

This experiment transfers the previous paper's selected-layer `Quantize(digits=3, dtype=f4, astype=f2) + Zstd(level=3)` rule to Gemma's 144 text-transformer MLP gate/up/down projections. The run path materializes the exact decoded q3 values eagerly; therefore quality and post-decode VRAM are comparable, while runtime omits Zstd decompression and is labeled emulated. It is not the deployment-primary system because decoded weights occupy BF16 VRAM.

```bash
bash run.sh --lang-pair eng-zho_Hans --batch-size 8 --input input.txt --output output.txt
```
