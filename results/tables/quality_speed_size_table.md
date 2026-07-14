# Quality–speed–size results

| System | ΔchrF vs BF16 | Size reduction vs BF16 | VRAM reduction vs BF16 | Relative generation speed |
|---|---:|---:|---:|---:|
| Layer-aware native MLP-q4 | -0.15 | 51.7% | 44.7% | 0.62× |
| IWSLT selected-layer q3+Zstd | -0.19 | 36.4% | 0.1% | 1.00×* |
| Organizer BNB-q4 | -0.78 | 65.8% | 54.5% | 0.60× |

Relative generation speed is BF16 seconds/line divided by system seconds/line on the local A6000. Native selective q4 and the storage codec are statistically indistinguishable in quality (BLEU p=0.3576, chrF p=0.2561), but native q4 cuts post-decode VRAM by 44.6% and storage by 24.0% relative to the codec artifact.

\* Excludes Zstd decompression.
