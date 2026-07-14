#!/usr/bin/env python
import json, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; work=ROOT/'data/prepared/modelzip_work'
inventory={"work":str(work),"files":[]}
for p in sorted(work.rglob('*')):
    if not p.is_file(): continue
    lines=p.read_text(errors='replace').splitlines() if p.stat().st_size < 200_000_000 else []
    inventory['files'].append({"path":str(p.relative_to(ROOT)),"bytes":p.stat().st_size,"lines":len(lines)})
for lang in ('ces-deu','eng-zho_Hans','eng-ara_EG'):
    candidates=[p for p in work.rglob('*') if p.is_file() and lang in str(p) and ('src' in p.name or 'input' in p.name)]
    if candidates:
        src=candidates[0]; dst=ROOT/'data/prepared'/lang/'dev.input.txt'; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        content=dst.read_text().splitlines(); (dst.parent/'smoke.32.input.txt').write_text('\n'.join(content[:32])+('\n' if content else ''))
(ROOT/'results/raw/data_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
samples=['# Data samples','']
for row in inventory['files'][:10]: samples.append(f"- `{row['path']}`: {row['lines']} lines, {row['bytes']} bytes")
(ROOT/'results/raw/data_samples.md').write_text('\n'.join(samples)+'\n')
