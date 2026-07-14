#!/usr/bin/env python
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ref=ROOT/'data/prepared/modelzip_work/tests/eng-zho_Hans/wmt25-ref.eng-zho_Hans.zho_Hans'
pred=ROOT/'results/predictions'
pairs=[
 ('global_q4_vs_native', pred/'organizer-bnb-q4.full331.txt', pred/'layeraware-native-mlp-q4.full331.txt'),
 ('codec_q3_vs_native', pred/'iwslt-storage-codec-q3.full331.txt', pred/'layeraware-native-mlp-q4.full331.txt'),
 ('bf16_vs_native', pred/'baseline-bf16.full331.txt', pred/'layeraware-native-mlp-q4.full331.txt'),
]
parts=[]
for label,base,system in pairs:
    cmd=['sacrebleu',str(ref),'-i',str(base),str(system),'--metrics','bleu','chrf','--tokenize','zh','--lowercase','--chrf-lowercase','--paired-bs','--paired-bs-n','10000','--paired-jobs','1','--format','text']
    done=subprocess.run(cmd,text=True,capture_output=True,check=True)
    parts += [f'## {label}','',done.stdout.strip(),'']
out=ROOT/'results/metrics/paired_significance.txt'; out.write_text('\n'.join(parts)+'\n'); print(out.read_text())
