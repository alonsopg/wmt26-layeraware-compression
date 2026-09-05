# Camera-ready response to WMT26 reviews

The camera-ready paper makes the following minimal changes in response to the reviews:

- It adds the released 945-segment blind-test CometKiwi-XXL and MetricX-24-XXL results for the submission, organizer global-q4 baseline, and BF16 baseline.
- It states explicitly that the submission is 60.6% slower than BF16 in the local RTX A6000 latency comparison. It also reports the organizer H100 throughput, where the submission is 0.1% below global q4 and 1.6% below BF16. The released organizer memory field is identified as host RSS, so the paper does not claim that local VRAM savings transfer to H100.
- It retains the FP4-versus-NF4 confound as a limitation and makes clear that no matched global-versus-selective NF4 ablation was run.
- It adds a serialized-size breakdown, including 1.88 GiB for the tied token embedding/output head and 0.78 GiB for the retained vision tower and multimodal projector.
- It reports the complete SacreBLEU paired-test signatures and clarifies that “layer-aware” means module-class-selective, with a uniform policy across all 48 text blocks.

Official scores were copied from organizer repository revision `652d2bf`; the exact rows used in the paper are saved in `results/metrics/official_wmt26_eng_zho.tsv`.

## Validation

- `make -C paper`: passed.
- `aclpubcheck -p other paper/main.pdf`: `All Clear!`
- Output: six A4 pages, no overfull boxes or unresolved citations/references, with all fonts embedded.
