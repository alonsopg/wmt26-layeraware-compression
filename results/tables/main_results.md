# Main results

Full local reference-backed comparison on 332 WMT25 English–Chinese records, batch size 8, deterministic greedy decoding, one RTX A6000. Generation speed excludes processor/model loading. BLEU uses SacreBLEU's Chinese tokenizer.

| System | chrF | BLEU-zh | Generation s/line | Peak VRAM GiB | Artifact GiB |
|---|---:|---:|---:|---:|---:|
| Organizer BF16 baseline | **28.45** | **31.65** | **1.354** | 26.46 | 22.74 |
| Layer-aware native MLP-q4 | 28.30 | 31.37 | 2.175 | 14.64 | 10.99 |
| IWSLT selected-layer q3+Zstd | 28.26 | 31.39 | 1.358* | 26.43 | 14.46 |
| Organizer BNB-q4 | 27.67 | 30.80 | 2.271 | **12.04** | **7.78** |

Native layer-aware q4 improves over global q4 by **+0.63 chrF** and **+0.56 BLEU**, with paired-bootstrap p-values 0.0003 and 0.0061 respectively. It also generates 4.2% faster locally, at the cost of 2.60 GiB more peak VRAM and a 3.21 GiB larger artifact.

\* Storage-codec generation reflects eagerly decoded weights and omits Zstd decompression.
