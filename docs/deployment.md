# Deployment

FilingsGraph has two deployment modes by design.

## 1. Full local workstation mode (primary)

The complete V6 system is intended to run locally on the GPU workstation. This is the mode that includes SEC ingestion, BGE-M3 embeddings, BGE reranking, DuckDB/XBRL calculations, temporal NetworkX GraphRAG, Qwen3 synthesis, verification, FastAPI, Gradio and Phoenix tracing.

This mode does **not** require a paid LLM API.

## 2. Hugging Face Spaces portfolio demo

A public Space should remain small and honest about its compute. `scripts.prepare_hf_space` creates a curated public SEC evidence subset under `deploy/huggingface/demo_data/`. The included CPU application demonstrates evidence retrieval without pretending that free CPU hardware is running the full Qwen3-14B workstation stack.

After the local pipeline and final evaluation have completed:

```bat
python -m scripts.prepare_hf_space
python -m pip install -U huggingface_hub
hf auth login
hf repos create filingsgraph-demo --repo-type space --sdk gradio --public
hf upload <YOUR_HF_USERNAME>/filingsgraph-demo deploy\huggingface . --repo-type space
```

Replace `<YOUR_HF_USERNAME>` with the account shown by `hf auth whoami`.

The current Hugging Face CLI documents `hf repos create ... --repo-type space --sdk gradio` for Space creation and `hf upload ... --repo-type space` for folder uploads. If the CLI syntax changes later, run `hf repos create --help` and `hf upload --help` rather than installing system-level tools.

## Public deployment data rules

Do not upload:

- `.env` or tokens;
- local model weights;
- corporate/private documents;
- unrelated local caches;
- huge raw SEC caches that the demo does not need.

The deployment preparation script copies only the curated public demo artifacts required by the Space.

## Optional GPU/ZeroGPU path

If Hugging Face ZeroGPU or another suitable GPU Space is genuinely available to the account, a later deployment experiment can add a smaller local model such as Qwen3-8B. This is optional. The portfolio demo must remain functional without purchasing persistent GPU hardware.

## GitHub deployment workflow

The main GitHub repository should contain the complete engineering project. The Hugging Face Space should contain the curated `deploy/huggingface` application produced after local validation. This keeps the public demo lightweight while preserving the full V0→V6 implementation, evaluation artifacts and architecture in GitHub.
