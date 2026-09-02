from __future__ import annotations

import hashlib
import json
from pathlib import Path
from filingsgraph.core.config import ROOT


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()


def main():
    p=ROOT/"reports/baseline/v6_final_frozen/FROZEN_COMPONENTS.json"
    if not p.exists():
        raise FileNotFoundError("Run python -m scripts.freeze_v6 first.")
    m=json.loads(p.read_text(encoding="utf-8")); changed=[]; missing=[]
    for rel,expected in m.get("files",{}).items():
        f=ROOT/rel
        if not f.exists(): missing.append(rel)
        elif sha256(f)!=expected: changed.append(rel)
    report={"ok":not changed and not missing,"changed":changed,"missing":missing,"files_checked":len(m.get("files",{}))}
    print(json.dumps(report,indent=2))
    if not report["ok"]: raise SystemExit(2)

if __name__=="__main__": main()
