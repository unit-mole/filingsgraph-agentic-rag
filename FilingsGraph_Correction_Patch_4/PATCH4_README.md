# FilingsGraph Correction Patch 4 — Specialized Quality Stabilization

Patch 4 is intentionally narrow. It does **not** modify the 17-file frozen core containing BGE-M3 retrieval, BM25, RRF fusion, reranker/filtering, XBRL selection, router/planner, chunking, or frozen retrieval/evaluation configuration.

## What it changes

1. **Grounded answer generation**
   - strict per-claim citation contract;
   - deterministic post-generation guard removes uncited factual lines instead of inventing citations;
   - invalid citation IDs are removed;
   - Qwen3-8B generation is made more concise/deterministic (`temperature=0`, `max_new_tokens=900`);
   - grounding evaluation adds non-empty-answer rate and mean supported claims per answer.

2. **Temporal risk-change classification**
   - replaces broad single-keyword topic matching with high-precision topic-specific rules;
   - distinguishes NEW/REMOVED from actual topic presence;
   - uses combined lexical similarity + information gain/loss for UNCHANGED/EXPANDED/REDUCED;
   - creates a **fresh blind review file** excluding the previously reviewed 30 temporal rows.

3. **Graph risk-edge extraction**
   - uses the same high-precision topic rules;
   - removes generic false positives such as bare `regulation`, `security`, or `manufacturing` matches;
   - raises rule-assisted edge confidence only when topic-specific evidence is present;
   - creates a **fresh blind edge review file** excluding the previously reviewed 30 edges.

4. **Evaluation hygiene**
   - `evaluate_patch4_diagnostic` scores Patch 4 against the already-reviewed diagnostic labels, clearly marked development-only;
   - final Temporal and Graph metrics are populated only after new blind review sheets are completed.

## Validated in the packaged source tree

- Python compilation: PASS
- Complete available test suite: **72 passed**
- Frozen-file comparison against the Patch-3 working tree: **0 frozen files changed**

## Required post-install sequence

From project root with `.venv` active:

```bat
call FilingsGraph_Correction_Patch_4\APPLY_PATCH_4.cmd
python -m scripts.build_graph
python -m scripts.evaluate_temporal
python -m scripts.evaluate_patch4_diagnostic
python -m scripts.evaluate_grounding --live
python -m scripts.check_v6_freeze
```

Do **not** rebuild SEC data, documents, DuckDB, Qdrant index, benchmark, or reranker.

If the development diagnostic and live grounding are acceptable, create fresh blind review sheets:

```bat
python -m scripts.export_temporal_gold_final --sample-size 30
python -m scripts.export_graph_gold_final --edge-sample-size 30
```

Then human-review those two CSVs before running:

```bat
python -m scripts.score_temporal_gold_final
python -m scripts.score_graph_gold_final
python -m scripts.evaluate_temporal
python -m scripts.evaluate_graph
```

The targets (for example >=90% claim support) are goals, **not guaranteed outputs**. Final claims must use the actual locally measured results.
