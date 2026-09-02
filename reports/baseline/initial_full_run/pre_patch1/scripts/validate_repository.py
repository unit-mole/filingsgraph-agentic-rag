from __future__ import annotations
import json
from pathlib import Path

REQUIRED = [
    "README.md", "LICENSE", "SECURITY.md", "DATA_SOURCES.md", "BENCHMARK.md", "CONTRIBUTING.md",
    "pyproject.toml", ".env.example", "docker-compose.yml", "Makefile", "docs/WINDOWS_RUNBOOK.md",
    "configs/companies.yaml", "configs/models.yaml", "configs/retrieval.yaml", "configs/graph.yaml",
    "src/filingsgraph/sec/client.py", "src/filingsgraph/parsing/chunking.py", "src/filingsgraph/xbrl/facts.py",
    "src/filingsgraph/retrieval/hybrid.py", "src/filingsgraph/reranking/reranker.py",
    "src/filingsgraph/finance/calculations.py", "src/filingsgraph/temporal/risk_diff.py",
    "src/filingsgraph/graph/builder.py", "src/filingsgraph/agents/nodes.py",
    "src/filingsgraph/verification/citations.py", "src/filingsgraph/security/prompt_injection.py",
    "src/filingsgraph/api/main.py", "app/gradio_app.py", "deploy/huggingface/app.py",
    "scripts/run_pipeline.py", "scripts/build_index.py", "scripts/build_graph.py", "scripts/evaluate_all.py",
]

def main():
    root = Path(__file__).resolve().parents[1]
    missing = [p for p in REQUIRED if not (root / p).exists()]
    empty_core = []
    for p in (root / "src" / "filingsgraph").rglob("*.py"):
        if p.name == "__init__.py":
            continue
        if p.stat().st_size < 20:
            empty_core.append(str(p.relative_to(root)))
    result = {"required_files": len(REQUIRED), "missing": missing, "empty_core_modules": empty_core, "ok": not missing and not empty_core}
    print(json.dumps(result, indent=2))
    if not result["ok"]:
        raise SystemExit(2)

if __name__ == "__main__":
    main()
