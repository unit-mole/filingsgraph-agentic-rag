# FilingsGraph Correction Patch 1

Purpose: repair four issues exposed by the first full baseline run without redownloading SEC data.

## Fixes

1. Non-standard 10-K section extraction (including semantic headings used by recent Intel annual reports).
2. Filing-aligned annual XBRL fact selection using accession/report-date provenance and annual-duration checks.
3. Balanced, category-stratified evaluation benchmark with DEV-only tuning and an explicitly frozen TEST split.
4. Safer query routing plus DEV-tuned blended BGE reranking so a reranker cannot silently destroy a strong hybrid baseline.

## Apply

Extract this folder directly inside the `filingsgraph` project root so the layout is:

`filingsgraph\FilingsGraph_Correction_Patch_1\APPLY_PATCH_1.cmd`

With the existing `.venv` activated, run:

`call FilingsGraph_Correction_Patch_1\APPLY_PATCH_1.cmd`

The installer backs up current `src`, `scripts`, `configs`, `tests`, and the v1 evaluation benchmark under:

`reports\baseline\initial_full_run\pre_patch1\`

It then compiles the code and runs the focused patch tests.

## Rebuild after patch

Do not redownload SEC filings or Company Facts.

Run:

`python -m scripts.build_documents`

Inspect `reports\final\parsing_report.json`. The target is 20/20 filings with at least one target section. If any filing still has zero target sections, stop and review before rebuilding downstream artifacts.

Then:

`python -m scripts.build_database`

Create the new benchmark version (this intentionally replaces the old frozen test only because the old benchmark was already inspected and is archived as the baseline):

`python -m scripts.build_eval_set --force-test`

Rebuild the retrieval index and graph because chunk IDs/evidence may have changed:

`python -m scripts.build_index`

`python -m scripts.build_graph`

## Tune on DEV only

Run:

`python -m scripts.evaluate_retrieval --split dev --skip-reranker`

`python -m scripts.tune_reranker`

`python -m scripts.evaluate_retrieval --split dev`

`python -m scripts.evaluate_financial --split dev`

`python -m scripts.evaluate_agent --split dev`

Do not run the new TEST split until the DEV results are reviewed and the architecture is frozen.
