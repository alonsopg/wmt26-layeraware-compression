#!/usr/bin/env python
import csv, json
from pathlib import Path
from sacrebleu.metrics import BLEU, CHRF

ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'data/prepared/modelzip_work/tests/eng-zho_Hans/cmp32.eng-zho_Hans.zho_Hans'
SIZES={
 'baseline-bf16':24414181813,
 'organizer-bnb-q8':13250249250,
 'organizer-bnb-q4':8353809477,
 'layeraware-native-mlp-q4':11804446040,
}
METHODS={
 'baseline-bf16':('none','all BF16'),
 'organizer-bnb-q8':('BitsAndBytes int8','global q8'),
 'organizer-bnb-q4':('BitsAndBytes NF4','global q4'),
 'layeraware-native-mlp-q4':('BitsAndBytes NF4/BF16','144 text MLP projections q4; rest BF16'),
 'iwslt-storage-codec-q3':('Quantize q3 + Zstd','144 text MLP projections storage-coded; decoded BF16'),
}

def nvidia_peak(system):
    p=ROOT/f'results/raw/gpu_traces/direct_{system}.csv'
    with p.open() as f: return max((int(r['memory_used_mib']) for r in csv.DictReader(f)),default=0)

def main():
    codec=json.loads((ROOT/'results/metrics/storage_codec_size.json').read_text())
    SIZES['iwslt-storage-codec-q3']=codec['estimated_codec_artifact_bytes']
    refs=REF.read_text().splitlines(); rows=[]
    for p in sorted((ROOT/'results/metrics').glob('direct_*.json')):
        r=json.loads(p.read_text()); sid=r['system_id']; hyps=Path(r['output']).read_text().splitlines()
        r['chrf']=CHRF(lowercase=True).corpus_score(hyps,[refs]).score
        r['bleu']=BLEU(lowercase=True,tokenize='zh').corpus_score(hyps,[refs]).score
        r['nvidia_peak_vram_mib']=nvidia_peak(sid); r['artifact_bytes']=SIZES[sid]; r['artifact_gib']=SIZES[sid]/2**30
        r['compression_method'],r['layer_policy']=METHODS[sid]; rows.append(r)
        p.write_text(json.dumps(r,indent=2)+'\n')
    fields=['system_id','compression_method','layer_policy','batch_size','lines','chrf','bleu','processor_load_seconds','model_load_seconds','generation_seconds','generation_seconds_per_line','end_to_end_seconds','nvidia_peak_vram_mib','torch_peak_allocated_mib','artifact_bytes','artifact_gib','valid_line_count','output']
    out=ROOT/'results/metrics/comparison_eng_zho_cmp32.csv'
    with out.open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows([{k:r.get(k) for k in fields} for r in rows])
    base=next(r for r in rows if r['system_id']=='baseline-bf16')
    md=['# Controlled English–Chinese comparison','',f'First 32 reference-backed WMT25 records; batch 8; deterministic greedy decoding on one RTX A6000. Generation time excludes processor/model loading. BLEU uses the SacreBLEU Chinese tokenizer.','', '| System | chrF | BLEU | ΔchrF vs BF16 | Gen s/line | Peak VRAM GiB | Artifact GiB |', '|---|---:|---:|---:|---:|---:|---:|']
    for r in sorted(rows,key=lambda x:x['chrf'],reverse=True): md.append(f"| {r['system_id']} | {r['chrf']:.2f} | {r['bleu']:.2f} | {r['chrf']-base['chrf']:+.2f} | {r['generation_seconds_per_line']:.3f} | {r['nvidia_peak_vram_mib']/1024:.2f} | {r['artifact_gib']:.2f} |")
    md += ['', 'The storage-codec artifact size is an exact selected-weight q3+Zstd payload plus raw non-selected tensor bytes and auxiliary files. Its runtime uses quality-equivalent eager decoded weights, so generation/VRAM reflect the post-decode state; model-load time omits Zstd decode and is not directly comparable.', '', 'This 32-sentence sample is suitable for directional evidence, not a final significance claim.']
    (ROOT/'results/tables/comparison_eng_zho_cmp32.md').write_text('\n'.join(md)+'\n')
    print(out); print('\n'.join(md))
if __name__=='__main__': main()
