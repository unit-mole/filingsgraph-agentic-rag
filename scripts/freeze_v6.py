from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from filingsgraph.core.config import ROOT, get_settings
from scripts._common import load_json, save_json

FROZEN_FILES = [
    "src/filingsgraph/embeddings/bge.py",
    "src/filingsgraph/retrieval/dense.py",
    "src/filingsgraph/retrieval/sparse.py",
    "src/filingsgraph/retrieval/fusion.py",
    "src/filingsgraph/retrieval/hybrid.py",
    "src/filingsgraph/retrieval/filters.py",
    "src/filingsgraph/reranking/reranker.py",
    "src/filingsgraph/xbrl/facts.py",
    "src/filingsgraph/xbrl/concepts.py",
    "src/filingsgraph/xbrl/periods.py",
    "src/filingsgraph/xbrl/units.py",
    "src/filingsgraph/database/repositories.py",
    "src/filingsgraph/agents/router.py",
    "src/filingsgraph/agents/planner.py",
    "src/filingsgraph/parsing/chunking.py",
    "configs/retrieval.yaml",
    "configs/evaluation.yaml",
]


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()


def main():
    missing=[p for p in FROZEN_FILES if not (ROOT/p).exists()]
    if missing:
        raise FileNotFoundError(f"Cannot freeze; missing files: {missing}")
    s=get_settings()
    tuning=load_json("reports/experiments/reranker_tuning.json",{}) or {}
    manifest={
        "freeze_version":"v6_final_after_patch3",
        "created_utc":datetime.now(timezone.utc).isoformat(),
        "test_status":"OBSERVED: do not tune frozen retrieval/reranker/router/XBRL/chunking components against this TEST split.",
        "production_model":s.local_llm_model,
        "device":s.device,
        "embedding_model":s.embedding_model,
        "reranker_model":s.reranker_model,
        "reranker_weight":tuning.get("best_weight"),
        "frozen_components":[
            "BGE-M3 dense retrieval","BM25","RRF hybrid fusion","BGE reranker and DEV-tuned weight",
            "metadata filtering","XBRL fact-selection data layer","router/planner rules","hierarchical chunking"
        ],
        "files":{p:sha256(ROOT/p) for p in FROZEN_FILES},
    }
    path=save_json("reports/baseline/v6_final_frozen/FROZEN_COMPONENTS.json",manifest)
    print(json.dumps({"ok":True,"manifest":str(path),"production_model":s.local_llm_model,"files_hashed":len(FROZEN_FILES)},indent=2))

if __name__=="__main__": main()
