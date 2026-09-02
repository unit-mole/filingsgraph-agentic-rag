# FilingsGraph Correction Patch 2

Patch 2 responds to the measured Patch-1 DEV results. It does **not** touch the frozen TEST split.

## What it fixes

1. **Graph routing:** the benchmark phrasing `Which selected companies share exposure ... and what filing evidence connects them?` is now recognized as GRAPH rather than TEXTUAL.
2. **Textual routing:** questions such as `What did NVDA disclose ... about revenue ...?` stay TEXTUAL instead of being misrouted merely because a financial word is present.
3. **Cohort entity resolution:** graph questions about the `selected companies` / cohort resolve to the configured NVDA, AMD, INTC, AVGO and QCOM cohort when no explicit ticker is supplied.
4. **Production metadata filtering:** explicit ticker, fiscal year(s), and SEC Item references are inferred from the question itself and passed to retrieval. This does not use benchmark gold metadata.
5. **Qdrant multi-period filtering:** list-valued fiscal-year filters are supported with MatchAny.
6. **Retrieval diagnostics:** evaluation now reports metrics by question category and adds `hybrid_filtered` as a measured architecture.
7. **Reranker tuning:** tuning uses DEV-only textual/temporal/mixed filing questions with query-derived metadata filters; graph QA is evaluated separately through GraphRAG.

## Apply

From the FilingsGraph root with `.venv` active:

```bat
call APPLY_PATCH_2.cmd
```

The script also works if these patch files are inside a `FilingsGraph_Correction_Patch_2` subfolder.

## Run after patch

No SEC download, document rebuild, database rebuild, index rebuild, graph rebuild, or benchmark rebuild is required.

```bat
python -m scripts.evaluate_agent --split dev
python -m scripts.evaluate_retrieval --split dev --skip-reranker
python -m scripts.tune_reranker
python -m scripts.evaluate_retrieval --split dev
python -m scripts.evaluate_financial --split dev
```

Do **not** run the frozen TEST split yet.
