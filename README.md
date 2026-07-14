# WMT26 Layer-Aware Compression

Reproducible code and evidence for team **alonso**'s WMT26 Model Compression submission, `layeraware-native-mlp-q4`. The system is a constrained-track English-to-Simplified-Chinese extension of `google/gemma-3-12b-it`. It applies native BitsAndBytes NF4 with double quantization to the 144 MLP gate/up/down projections in the 48 text-transformer blocks while preserving attention, embeddings, normalization, `lm_head`, and vision modules in BF16.

- Submitted model and runnable bundle: [alonsopg/wmt26-layeraware-native-mlp-q4](https://huggingface.co/alonsopg/wmt26-layeraware-native-mlp-q4)
- Organizer contract: [thammegowda/wmt26-model-compression](https://github.com/thammegowda/wmt26-model-compression#submission-contract)
- ACL-format system-paper draft: [`paper/main.pdf`](paper/main.pdf) ([LaTeX source](paper/main.tex))
- Submission status and exact revision: [`SUBMISSION_HANDOFF.md`](SUBMISSION_HANDOFF.md)
- Chronological experiment log: [`STATUS.md`](STATUS.md)

## Main result

The reference-backed local comparison used 332 WMT25 English–Chinese records, batch size 8, and one RTX A6000. BLEU is SacreBLEU with the Chinese tokenizer; timing excludes model load.

| System | chrF | BLEU | Generation s/line | Peak VRAM (GiB) | Artifact (GiB) |
|---|---:|---:|---:|---:|---:|
| BF16 base | 28.45 | 31.65 | 1.354 | 26.46 | 22.74 |
| Organizer global q4 | 27.67 | 30.80 | 2.271 | 12.04 | 7.78 |
| Prior q3 + Zstd | 28.26 | 31.39 | 1.358* | 26.43 | 14.46 |
| **Layer-aware native MLP q4** | **28.30** | **31.37** | **2.175** | **14.64** | **10.99** |

Relative to organizer global q4, the submitted extension gained +0.63 chrF and +0.56 BLEU. A 10,000-trial paired bootstrap gave `p=0.0003` for chrF and `p=0.0061` for BLEU. `*` The prior method's timing excludes Zstd decompression and is not directly comparable end-to-end. See [`results/tables/main_results.md`](results/tables/main_results.md) and [`results/metrics/paired_significance.txt`](results/metrics/paired_significance.txt).

## Repository contents

- `submissions/`: lightweight source and launch wrappers for all compared systems; generated model workdirs are intentionally excluded
- `scripts/`: environment, model preparation, evaluation, significance, packaging, and reporting commands
- `src/layeraware/`: experiment utilities
- `results/`: metrics, predictions, raw GPU traces, paper-ready prose/tables, and the submission receipt
- `experiments/`: experiment definitions
- `data/manifests/`: committed selection metadata; prepared organizer data is regenerated locally
- `artifacts/zips/*.sha256`: checksums for locally retained submission archives

Large model weights and ZIP archives are not stored in Git. The exact submitted weights and runnable source are hosted in the public Hugging Face repository above; the final local ZIP checksum is `f4ca6461b1faf5da6859d1d3d8972d575ef20b2e0d021bd03232a054aa578e65`.

## Quick start

```bash
bash scripts/00_check_machine.sh
bash scripts/01_setup_env.sh
bash scripts/02_fetch_organizer_repo.sh
bash scripts/03_prepare_data.sh
PYTHONPATH=src env/.venv/bin/python scripts/04_probe_model_layers.py
bash scripts/05_build_submissions.sh
bash scripts/06_run_sanitychecks.sh
bash scripts/09_package_submission.sh submissions/layeraware-native-mlp-q4
```

The official inference interface is:

```bash
bash submissions/layeraware-native-mlp-q4/run.sh --lang-pair eng-zho_Hans --batch-size 8 --input input.txt --output output.txt
```

Gemma 3 is gated. Accept its Hugging Face terms and authenticate before model preparation. Logs belong on stderr; output must contain exactly one translation per input line.

## Reproduce the comparison

After the quick-start preparation and builds, run:

```bash
bash scripts/run_full_core_comparison.sh
env/.venv/bin/python scripts/paired_significance.py
env/.venv/bin/python scripts/08_collect_results.py
```

Hardware-dependent speed and memory numbers will differ from the recorded RTX A6000 run. The official organizers evaluate submissions on their standardized environment.

## Submission record

The organizer form returned HTTP 200 and a Google Forms confirmation marker at `2026-07-14T14:09:21Z`. The client-side record is [`results/raw/wmt26_form_submission_receipt.json`](results/raw/wmt26_form_submission_receipt.json). Organizer-side acknowledgement must come from the task organizers; the receipt does not expose their private response sheet.

## Paper draft

Build the five-page non-anonymous WMT26 system-paper draft with:

```bash
git submodule update --init --recursive
make -C paper
```

The current draft uses the official ACL style, reports all local evidence, and leaves official WMT26 blind-test and organizer H100 results as explicit pre-submission follow-ups.
