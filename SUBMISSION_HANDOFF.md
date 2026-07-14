# WMT26 Submission Handoff

## Submit this system

- System ID: `layeraware-native-mlp-q4`
- Designation: **PRIMARY**
- Track: **constrained**
- Language pair: `eng-zho_Hans`
- Archive: `artifacts/zips/layeraware-native-mlp-q4.zip`
- Archive size: approximately 9.4 GiB
- SHA-256: `f4ca6461b1faf5da6859d1d3d8972d575ef20b2e0d021bd03232a054aa578e65`
- Base model: `google/gemma-3-12b-it` revision `96b6f1eccf38110c56df3a15bffe176da04bfd80`
- Data used for calibration/fine-tuning: none

Method summary: native BitsAndBytes NF4 with double quantization is applied to the 144 `gate_proj`, `up_proj`, and `down_proj` modules in the 48 text-transformer blocks. Attention, embeddings, normalization, `lm_head`, and vision modules remain BF16.

Official run interface:

```bash
bash run.sh --lang-pair eng-zho_Hans --batch-size 8 --input input.txt --output output.txt
```

Verify after transfer:

```bash
cd artifacts/zips
sha256sum -c layeraware-native-mlp-q4.sha256
```

## Administrative submission completed

- Submitted: `2026-07-14T14:09:21Z`
- Institution: Independent researcher
- Team: `alonso`
- Contact: `mail@alonsopg.com`
- Public repository: <https://huggingface.co/alonsopg/wmt26-layeraware-native-mlp-q4>
- Experiment and reproducibility repository: <https://github.com/alonsopg/wmt26-layeraware-compression>
- Submitted repository revision: `609c25680eb89286a04cd70747da42c7f3c98412`
- Maximum batch size: `8`
- Consent to release system outputs for research: yes
- Organizer form response: HTTP 200 with confirmation detected
- Receipt: `results/raw/wmt26_form_submission_receipt.json`

No administrative submission work remains. Monitor the contact email for any organizer follow-up.

## Evidence

- Organizer sanity check: passed
- Full local evaluation: 332/332 valid output lines
- Native result: 28.30 chrF, 31.37 BLEU, 14.64 GiB peak VRAM, 10.99 GiB model artifact
- Global q4 comparison: 27.67 chrF, 30.80 BLEU, 12.04 GiB peak VRAM, 7.78 GiB model artifact
- Paired native-vs-global-q4 significance: chrF `p=0.0003`, BLEU `p=0.0061`

## Do not submit as the primary

`artifacts/zips/layeraware-primary.zip` is the earlier global-q4 fallback. It predates the validated native layer-aware extension and is retained only for reproducibility. If a contrastive system is desired, rebuild/relabel it explicitly as `organizer-bnb-q4-contrastive` before submitting it.
