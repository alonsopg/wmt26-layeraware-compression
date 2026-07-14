# WMT26 Layer-Aware Compression Status

This log is append-only and uses UTC timestamps.

## 2026-07-14T11:28:51Z — Machine audit

- Command: `./scripts/00_check_machine.sh`
- Source version: new workspace; no git commit yet
- Created: `results/raw/machine_report.txt`, `results/raw/nvidia_smi_initial.txt`
- Result: 1× NVIDIA RTX A6000 (49,140 MiB), 44 GiB RAM, 119 GiB disk free, 8 CPUs; Hugging Face CLI authenticated as `alonsopg`; `HF_TOKEN` environment variable absent.
- Errors/blockers: CUDA compiler (`nvcc`) is not installed; this is not yet a runtime blocker. Host differs from organizer H100/Ubuntu 24.04 environment.
- Next: verify current WMT26 sources and test gated Gemma model API access before environment setup.

## 2026-07-14T11:30:00Z — Source and access verification

- Commands: opened official WMT26 task page and organizer README; cloned organizer repo; queried Hugging Face model metadata.
- Source versions: organizer `a4707272bf8605a75faa9968af8951dc85bd174c`; IWSLT local repo `a017da671872aa86fa7495688844f4e961c4d512`; Gemma `96b6f1eccf38110c56df3a15bffe176da04bfd80`.
- Created: `external/wmt26-model-compression/`.
- Result: Hugging Face user `alonsopg` can access gated `google/gemma-3-12b-it`.
- Error: first environment attempt used Python 3.11, but current `modelzip` requires Python >=3.12.
- Next: recreate the fresh environment with available Python 3.13 and install dependencies.

## 2026-07-14T11:34:51Z — Environment and first data setup attempt

- Command: `./scripts/01_setup_env.sh`; `./scripts/03_prepare_data.sh`
- Created: Python 3.12 environment at `env/.venv`, dependency freeze; initial warmup Czech–German files.
- Result: organizer dependencies installed successfully with pinned inference versions.
- Error: organizer data paths are repository-relative; invoking setup from project root could not find `data/wmt25/wmt25.cs-de_DE.paragraphs.jsonl`.
- Next: rerun data setup with the organizer repository as working directory.

## 2026-07-14T11:35:05Z — Data preparation and module probe

- Commands: `./scripts/03_prepare_data.sh`; `PYTHONPATH=src env/.venv/bin/python scripts/04_probe_model_layers.py`
- Source versions: organizer `a4707272bf8605a75faa9968af8951dc85bd174c`; Gemma config revision `96b6f1eccf38110c56df3a15bffe176da04bfd80`.
- Created: prepared warmup/WMT25/WMT25-reference data for all three task pairs, `results/raw/data_inventory.json`, module/config CSV/JSON files.
- Result: 499 linear modules and 348 MLP policy candidates (excluding CSV headers).
- Errors/blockers: none.
- Next: build q4 deadline-safe primary artifact under GPU tracing.

## 2026-07-14T11:38:41Z — Primary artifact and organizer sanity check

- Commands: `scripts/run_with_gpu_trace.sh build_layeraware_primary scripts/05_build_submissions.sh`; official `evals/sanitycheck.sh` via `scripts/06_run_sanitychecks.sh`.
- Created: q4 artifact in `submissions/layeraware-primary/workdir/model` (8,353,809,477 bytes); GPU traces for build and sanity runs.
- Result: organizer sanity check passed; output line-count contract passed.
- Error resolved: copied organizer `setup.sh` was not idempotent when `.venv` existed; guarded environment creation.
- Next: run primary English–Chinese warmup evaluation and package submission.

## 2026-07-14T11:38:54Z — Primary warmup evaluation

- Command: `python -m modelzip.evaluate ... --langs eng-zho_Hans --test-names warmup --metrics chrf --batch 1` under GPU tracing.
- Created: translation, stats, chrF score, `results/metrics/all_runs.csv`, result tables, artifact inventory.
- Result: valid 1/1 output lines; chrF 100.0 on organizer warmup; wall 11.414 s including load; peak VRAM 12,204 MiB; artifact 7.780 GiB.
- Error/blocker: scoring completed, then organizer evaluator failed only while backing up to its host-specific default `/mnt/tg/...`; local result files are intact. Future calls must set `--backup results/raw/eval_backup`.
- Next: create archive and checksum; broader batch/dev comparisons remain outstanding.

## 2026-07-14T11:47:00Z — Submission packaging

- Command: `bash scripts/09_package_submission.sh submissions/layeraware-primary`; `sha256sum -c`; `unzip -tq`.
- Created: `artifacts/zips/layeraware-primary.zip` (6.6 GiB) and `.sha256`.
- Result: SHA-256 `83a7c9bbb179348546f2a418862da62cb5db459582a7b1d6f8e90c831e62f8d3`; checksum verified; ZIP integrity verified; `.venv` excluded.
- Errors/blockers: the valid primary is the scientifically honest global q4 fallback, not a demonstrated mixed layer-aware native quantizer. Broader dev/batch sweeps and q8 comparisons were not completed.
- Next: fill team/contact fields, upload the artifact/model, submit the WMT form before July 15 AoE; then run reference-backed WMT25 comparisons for the paper.

## 2026-07-14T12:00:00Z — Native layer-aware extension

- Commands: `scripts/prepare_layeraware_native.py`; official organizer `evals/sanitycheck.sh`.
- Source versions: Transformers 4.57.6; BitsAndBytes 0.45.3; Gemma revision `96b6f1eccf38110c56df3a15bffe176da04bfd80`.
- Created: `submissions/layeraware-native-mlp-q4/workdir/model`, `layer_policy.json`, build/sanity GPU traces.
- Result: exactly 144 text-transformer MLP gate/up/down projections serialized as native NF4; all other linear modules preserved. Artifact 11,804,446,040 bytes. Organizer sanity check passed.
- Errors/blockers: none locally; H100 behavior not yet measured.
- Next: compare against BF16, organizer q8/q4, and prior IWSLT q3+Zstd method.

## 2026-07-14T12:18:00Z — Controlled five-system comparison

- Commands: organizer `modelzip.evaluate` and `scripts/run_direct_comparison.sh` on `cmp32`, batch 8; `scripts/measure_codec_storage.py`; `scripts/08_collect_results.py`.
- Created: predictions for five systems, per-system timing JSON, GPU traces, exact codec-size measurement, `results/metrics/comparison_eng_zho_cmp32.csv`, and paper-ready comparison tables.
- Result: native MLP-q4 28.10 chrF/32.32 BLEU, 2.257 generation s/line, 12.99 GiB peak VRAM, 10.99 GiB artifact. Global q4: 27.65/31.95, 2.380 s/line, 11.91 GiB VRAM, 7.78 GiB artifact. Prior q3+Zstd: 27.66/31.80, 1.451 s/line, 24.80 GiB post-decode VRAM, 14.46 GiB measured codec artifact.
- Errors/blockers: organizer `--metrics bleu` maps to unavailable `pymarian-eval`; BLEU was therefore computed with SacreBLEU's Chinese tokenizer. The 32-record subset is not sufficient for significance claims. Storage-codec speed excludes Zstd decompression.
- Next: finish and verify the native-extension archive; run the full reference set and H100 evaluation if available.

## 2026-07-14T12:42:00Z — Native-extension packaging

- Command: `scripts/09_package_submission.sh submissions/layeraware-native-mlp-q4`; `sha256sum -c`; `unzip -tq`.
- Created: `artifacts/zips/layeraware-native-mlp-q4.zip` (9.4 GiB) and checksum file.
- Result: ZIP integrity verified; `.venv` excluded; SHA-256 `81945162b8b72d7d6937040a4d7055928ebafc11fe34fac4cdcf1f98904232e7` verified.
- Errors/blockers: none.
- Next: run the full reference-backed core comparison.

## 2026-07-14T13:28:00Z — Full 332-record comparison and significance

- Commands: `scripts/run_full_core_comparison.sh`; `scripts/paired_significance.py` with 10,000 paired-bootstrap trials.
- Created: four full prediction files, full timing JSON, GPU traces, `results/metrics/comparison_eng_zho_full332.csv`, `results/metrics/paired_significance.txt`, updated main/paper tables.
- Result: native MLP-q4 28.30 chrF/31.37 BLEU versus global q4 27.67/30.80; deltas +0.63/+0.56 with p=0.0003/0.0061. Native peak VRAM 14.64 GiB versus q4 12.04 GiB and BF16 26.46 GiB. Native generation 2.175 s/line versus q4 2.271 s/line. Codec quality was statistically tied with native but required 26.43 GiB post-decode VRAM and a 14.46 GiB artifact.
- Errors/blockers: local hardware is RTX A6000 rather than organizer H100; no COMET/MetricX; storage-codec speed omits Zstd decompression.
- Next: upload native archive/model, fill team/contact fields, and validate on H100 or organizer infrastructure before official submission.

## 2026-07-14T13:31:00Z — Final portability audit

- Commands: reran native `setup.sh`; refreshed `setup.sh` and `config.json` in the ZIP; recomputed SHA-256; reproduced all full-set scores from saved predictions.
- Result: setup discovers `modelzip` both in this nested workspace and when extracted directly under the organizer repository; designation is PRIMARY; all four systems have 332/332 lines; all scores reproduce exactly; native policy contains 144 targets.
- Final ZIP SHA-256: `f4ca6461b1faf5da6859d1d3d8972d575ef20b2e0d021bd03232a054aa578e65`.
- Next: fill team/contact placeholders and upload/submit.

## 2026-07-14T13:57:20Z — Technical handoff complete

- Commands: final official organizer sanity check; portable checksum verification; archive content listing.
- Created: `SUBMISSION_HANDOFF.md`; portable basename checksum file; final GPU sanity trace.
- Result: exact PRIMARY source passed organizer sanity again; portable checksum returned OK; archive contains all required scripts and three model shards, with no `.venv`.
- Errors/blockers: none technical. Only team/contact/upload/form administration remains.
- Next: administrator uploads `layeraware-native-mlp-q4.zip`, completes the prepared form fields, and submits.

## 2026-07-14T14:09:21Z — Administrative submission complete

- Commands: published the complete source/model bundle as a public Hugging Face repository; submitted the official organizer Google Form once; saved and checked the response receipt.
- Submitted identity: Independent researcher; team `alonso`; contact `mail@alonsopg.com`.
- Public repository: `https://huggingface.co/alonsopg/wmt26-layeraware-native-mlp-q4`, revision `609c25680eb89286a04cd70747da42c7f3c98412`.
- Submitted configuration: PRIMARY constrained `eng-zho_Hans`; maximum batch size 8; consent to release system outputs for research.
- Result: repository is public; form returned HTTP 200 and its confirmation marker was detected. Receipt saved at `results/raw/wmt26_form_submission_receipt.json`.
- Errors/blockers: none.
- Next: monitor `mail@alonsopg.com` for organizer follow-up.

## 2026-07-14T14:25:12Z — Reproducibility repository prepared

- Commands: initialized a `main` Git repository; added a repository-level ignore policy; expanded the README with the method, exact comparisons, significance, artifact links, and reproduction commands; staged and audited the complete lightweight workspace.
- Included: source, launch wrappers, experiment scripts, metrics, predictions, raw GPU traces, paper material, submission handoff, form receipt, and archive checksums.
- Excluded: local environments/caches, the organizer checkout, regenerated data copies, gated Gemma caches, generated model workdirs, and 16+ GiB ZIP archives. The submitted model remains public at `https://huggingface.co/alonsopg/wmt26-layeraware-native-mlp-q4`.
- Validation: 27 tracked JSON documents parsed; README local links resolved; tracked Python compiled; tracked shell scripts passed `bash -n`; no credential patterns or unignored files over 20 MiB were found.
- Result: 193 tracked files totaling approximately 3.02 MiB, ready for the initial commit and GitHub publication.
- External blocker: this machine has no account-wide GitHub credential; its available GitHub SSH key is scoped to another repository and cannot create a new repository.
- Next: authenticate GitHub account `alonsopg`, create `wmt26-layeraware-compression`, and push `main`.

## 2026-07-14T14:31:39Z — GitHub publication complete

- Commands: installed the GitHub CLI; completed GitHub device authorization as `alonsopg`; created the public repository; configured Git's authenticated HTTPS helper; pushed `main`.
- Repository: `https://github.com/alonsopg/wmt26-layeraware-compression`.
- Initial publication commit: `6095698` (`Publish WMT26 layer-aware compression experiment`).
- Result: the complete 193-file lightweight reproducibility snapshot is published, with heavyweight submitted weights linked to the public Hugging Face repository.
- Errors resolved: the first push lacked an HTTPS credential helper; `gh auth setup-git` connected Git to the approved account and the retry succeeded.
- Next: verify anonymous access and tag the finalized repository snapshot.
