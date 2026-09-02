# FilingsGraph Correction Patch 3 — V6 Stabilization

Patch 3 intentionally **does not modify the frozen retrieval/reranker/router/XBRL/chunking components**. It stabilizes presentation, grounding verification, gold-review evaluation, and runtime shutdown.

## What it changes

1. Removes Qwen `<think>...</think>` content from all provider-returned user-visible answers.
2. Corrects SEC trust semantics: filing text is authoritative evidence of what the filer reported, but untrusted as executable instructions.
3. Replaces the old "cite retrieved evidence" verifier with claim-level citation attachment metrics:
   - citation precision
   - claim support rate
   - unsupported claim rate
   - citation completeness
   Unused retrieved evidence is diagnostic only and no longer makes a valid answer fail.
4. Adds a real four-query V6 grounding run: `python -m scripts.evaluate_grounding --live`.
5. Adds human-review Temporal gold export/scoring.
6. Adds human-review Graph QA and edge precision export/scoring.
7. Adds V6 freeze manifest + integrity checker.
8. Closes local Qdrant before Python teardown to suppress the harmless shutdown warning.

## Apply

From the FilingsGraph root with `.venv` active:

```bat
call FilingsGraph_Correction_Patch_3\APPLY_PATCH_3.cmd
```

## After apply

```bat
python -m scripts.freeze_v6
python -m scripts.check_v6_freeze
python -m scripts.evaluate_grounding --live
python -m scripts.evaluate_temporal
python -m scripts.export_temporal_gold --sample-size 30
python -m scripts.export_graph_gold --edge-sample-size 30
```

Review:
- `reports\gold\temporal_review.csv`
- `reports\gold\graph_qa_review.csv`
- `reports\gold\graph_edge_review.csv`

Then score and regenerate:

```bat
python -m scripts.score_temporal_gold
python -m scripts.score_graph_gold
python -m scripts.evaluate_temporal
python -m scripts.evaluate_graph
python -m scripts.build_ablation_table
python -m scripts.evaluate_system
python -m scripts.export_failure_analysis
python -m scripts.export_final_results
python -m scripts.check_v6_freeze
pytest -q
pytest tests\security -q
```

Do not retune retrieval/reranker/router/XBRL/chunking against the already-observed TEST split.
