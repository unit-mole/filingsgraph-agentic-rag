# FilingsGraph Package Validation

Validation performed before creating the downloadable Project 3 archive.

## Completed offline checks

- Full Python syntax compilation: `src`, `scripts`, `app`, `tests`, and `deploy/huggingface` — **PASS**.
- Repository completeness validator — **PASS** (`33` required paths checked, `0` missing, `0` empty core modules).
- Pytest suite — **PASS: 45/45 tests**.
- Original Project 3 specification is retained at `docs/PROJECT_REQUIREMENTS.md`.
- Windows no-admin runbook is retained at `docs/WINDOWS_RUNBOOK.md`.
- Hugging Face Space package is retained under `deploy/huggingface/`.

## What the 45 tests cover

The suite includes configuration/schemas, SEC entity-resolution and Fair Access guards, filing parsing/section extraction/table context, hierarchical chunking, XBRL normalization, deterministic financial calculations, dense/RRF retrieval fixtures, temporal risk changes, graph provenance/temporal validity, query routing/planning, verification, security controls, evaluation metrics, orchestrator integration and an API smoke path.

## Deliberately not fabricated

No retrieval, temporal, graph, grounding or local-Qwen performance score is pre-filled as a portfolio result. Those values must be produced from the locally downloaded SEC corpus and frozen evaluation data. Human-judgment metrics remain `TBD` until reviewed gold labels exist.

## Runtime validation that must occur on the target workstation

The packaging sandbox could not install missing third-party packages from PyPI because its container network could not resolve PyPI. Consequently, the following are intentionally validated by the Windows runbook on the user's workstation rather than falsely marked as completed here:

- fresh virtual-environment dependency installation;
- live SEC EDGAR downloads;
- BGE-M3 and reranker model downloads/inference;
- Qdrant/DuckDB full corpus construction;
- Qwen3-8B / Qwen3-14B GPU inference on the RTX workstation;
- Docker Desktop services and Phoenix export;
- real V0→V6 benchmark results;
- Hugging Face Space upload.

The default project path does not require administrator commands or mandatory paid model APIs.
