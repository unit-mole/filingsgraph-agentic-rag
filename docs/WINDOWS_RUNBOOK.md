# FilingsGraph — Windows 11 / Office-System Runbook

This runbook assumes Docker Desktop and WSL2 are already installed. **No administrator command is required by the default Windows path.** Do not use `winget`, `choco`, system-wide CUDA/driver changes, `sudo apt`, or IT policy changes on the office machine.

## 1. Extract and enter the project — CMD

```bat
cd /d D:\Projects\filingsgraph
```

Use any writable user folder; the path above is only an example.

## 2. Create local Python environment — CMD

```bat
py -3.11 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
```

If `py -3.11` is unavailable but `python --version` is Python 3.11, use `python -m venv .venv`.

## 3. Verify GPU/environment — CMD

```bat
python -m scripts.check_environment
nvidia-smi
```

Expected: `reports\final\environment.json`. For the full local model path, PyTorch should report CUDA available, the RTX 5090 and BF16 support. If it does not, **do not modify office-system drivers/admin settings**; return the report and `nvidia-smi` output for debugging.

## 4. Configure SEC identity — CMD

```bat
copy .env.example .env
notepad .env
```

Replace the examples with your real contact information:

```text
SEC_USER_AGENT=FilingsGraph research-project Your Name your.real.email@company.com
SEC_CONTACT_EMAIL=your.real.email@company.com
SEC_REQUESTS_PER_SECOND=5
```

The project refuses SEC downloads while the example identity is still present.

## 5. Optional Docker infrastructure — CMD

The core project works with DuckDB + embedded Qdrant + NetworkX, so Docker databases are not mandatory. To mirror the production infrastructure and enable Phoenix:

```bat
docker compose up -d postgres qdrant phoenix
docker compose ps
```

Neo4j Community is optional only:

```bat
docker compose --profile neo4j up -d neo4j
```

## 6. Validate SEC connectivity/Fair Access — CMD

```bat
python -m scripts.validate_sec_access
```

Expected: `ok=True`. If SEC returns 403/429, stop and return the output rather than repeatedly retrying.

## 7. Resolve companies + download bounded corpus — CMD

```bat
python -m scripts.resolve_companies
python -m scripts.download_filings
python -m scripts.download_companyfacts
python -m scripts.validate_data
```

Expected outputs:

- `data\processed\companies.json`
- `data\processed\filings_metadata.json`
- `data\raw\filings\...`
- `data\raw\xbrl\...`
- `reports\final\data_quality.json`

## 8. Parse filings + build financial database — CMD

```bat
python -m scripts.build_documents
python -m scripts.build_database
```

Expected outputs:

- `data\processed\sections.jsonl`
- `data\processed\chunks.jsonl`
- `data\processed\table_manifest.json`
- `data\processed\filingsgraph.duckdb`
- `reports\final\parsing_report.json`
- `reports\final\xbrl_normalization_report.json`

## 9. Build dense + sparse retrieval — CMD

```bat
python -m scripts.build_index
```

The first run downloads `BAAI/bge-m3`. Default Qdrant is embedded/local; no Qdrant Docker server is required. BM25 is persisted as `data\index\bm25.pkl`.

For a lightweight plumbing-only check that must **not** be used as portfolio retrieval metrics:

```bat
python -m scripts.build_index --smoke --dense-backend numpy
```

## 10. Build temporal knowledge graph — CMD

```bat
python -m scripts.build_graph
```

Expected:

- `data\graph\filingsgraph.json`
- `reports\final\graph_build_report.json`

## 11. Build DEV + frozen TEST benchmark — CMD

```bat
python -m scripts.build_eval_set
```

Expected:

- `data\evaluation\dev\questions.jsonl`
- `data\evaluation\test\questions.jsonl`
- `reports\final\eval_dataset_report.json`

After freezing the TEST set, do not tune against it.

## 12. Run V0 → V6 gates — CMD

```bat
python -m scripts.run_v0
python -m scripts.run_v1
python -m scripts.run_v2
python -m scripts.run_v3
python -m scripts.run_v4
python -m scripts.run_v5
python -m scripts.run_v6
```

Outputs: `reports\baseline\v0_status.json` through `v6_status.json`. These gates verify architecture/artifacts; they do not invent performance numbers.

## 13. Formal evaluation — CMD

```bat
python -m scripts.evaluate_retrieval --split dev
python -m scripts.evaluate_retrieval --split test
python -m scripts.evaluate_financial
python -m scripts.evaluate_temporal
python -m scripts.evaluate_graph
python -m scripts.evaluate_agent
python -m scripts.evaluate_grounding
python -m scripts.ablate_graph
python -m scripts.ablate_structured
python -m scripts.export_failure_analysis
```

Outputs are written under `reports\experiments`, `reports\temporal`, `reports\graph`, `reports\ablations` and `reports\failure_analysis`.

Temporal/graph/grounding metrics that require human-reviewed gold intentionally remain `TBD` until that gold exists. The code does not manufacture them.

## 14. Optional Qwen3 8B vs 14B comparison — CMD

Only after the core pipeline works:

```bat
python -m scripts.model_comparison --models Qwen/Qwen3-8B Qwen/Qwen3-14B
```

This downloads large model weights and measures real local latency/output. It is not required to validate ingestion/retrieval/XBRL/graph plumbing.

## 15. Tests + security — CMD

```bat
pytest -q
pytest tests\security -q
```

## 16. FastAPI — separate CMD window

```bat
cd /d D:\Projects\filingsgraph
call .venv\Scripts\activate.bat
uvicorn filingsgraph.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Open `http://127.0.0.1:8000/docs`.

## 17. Gradio — separate CMD window

```bat
cd /d D:\Projects\filingsgraph
call .venv\Scripts\activate.bat
python app\gradio_app.py
```

Open `http://127.0.0.1:7860`.

Keep **Full local model/index** off for instant planning/database views. Enable it after BGE, reranker, Qdrant index and Qwen are ready.

## 18. Phoenix observability

If `docker compose up -d phoenix` is running, open `http://127.0.0.1:6006`. `PHOENIX_ENDPOINT` in `.env` controls OTLP export.

## 19. Export final result bundle — CMD

```bat
python -m scripts.export_final_results
```

Expected: `reports\final\summary.json`.

## 20. Automated end-to-end path — CMD

After `.venv`, dependencies and `.env` have been prepared:

```bat
RUN_ALL_WINDOWS.cmd
```

Use the individual commands above when debugging.

## 21. Prepare Hugging Face demo after local validation — CMD

First prepare the curated public demo only after the real local results have been reviewed:

```bat
python -m scripts.prepare_hf_space
python -m pip install -U huggingface_hub
hf auth login
hf auth whoami
hf repos create filingsgraph-demo --repo-type space --sdk gradio --public
hf upload <YOUR_HF_USERNAME>/filingsgraph-demo deploy\huggingface . --repo-type space
```

Replace `<YOUR_HF_USERNAME>` with the username returned by `hf auth whoami`. The Space package intentionally uses a CPU-friendly curated SEC evidence demo; it does not misrepresent free CPU hosting as full Qwen3-14B inference. Full deployment details are in `docs\deployment.md`.

## 22. What to send back after the first run

Return these files/outputs so tuning is results-based rather than speculative:

```text
reports/final/environment.json
reports/final/data_quality.json
reports/final/parsing_report.json
reports/final/xbrl_normalization_report.json
reports/final/index_report.json
reports/final/graph_build_report.json
reports/final/eval_dataset_report.json
reports/experiments/test_dense_retrieval.json
reports/experiments/test_bm25_retrieval.json
reports/experiments/test_hybrid_retrieval.json
reports/experiments/test_financial.json
reports/temporal/temporal_evaluation.json
reports/graph/graph_evaluation.json
reports/experiments/test_agent_routing.json
reports/experiments/grounding_evaluation.json
reports/ablations/graph_ablation.json
reports/ablations/structured_data_ablation.json
reports/failure_analysis/failure_analysis.json
reports/final/summary.json
pytest terminal output
any error traceback
```
