# Data layout

Runtime-generated SEC data is intentionally excluded from Git.

- `raw/filings/`: cached SEC filing HTML
- `raw/xbrl/`: cached SEC Company Facts JSON
- `processed/`: normalized documents, facts, DuckDB
- `index/`: Qdrant-local and BM25 artifacts
- `graph/`: NetworkX graph artifacts
- `evaluation/`: generated DEV and frozen TEST benchmark JSONL

Every network download is cached. Re-running ingestion should reuse local files unless `--force` is supplied.
