# FilingsGraph Correction Patch 5 — Final Specialized Quality Gate

Patch 5 is narrow and does **not** modify the frozen 17-file core (BGE-M3, BM25, RRF, reranker/filtering, XBRL selection, router/planner, chunking, retrieval/evaluation configuration).

## Why Patch 5 exists

Patch 4 fixed citation attachment but the four-case live grounding check showed:
- NUMERIC: useful and fully cited;
- MIXED: useful and fully cited;
- TEMPORAL: strict guard returned only the insufficiency fallback;
- GRAPH: strict guard returned only the insufficiency fallback.

Patch 4's graph development diagnostic also compared edge IDs, but an edge ID is shared by all candidate chunks for the same company/risk/filing/year. A better provenance span can replace an old false-positive span while keeping the same ID. Patch 5 therefore evaluates graph *evidence spans/rules*, not only edge-ID persistence.

## Changes

1. **Evidence-first fallback for TEMPORAL/GRAPH**
   - specialized evidence is placed first in the 20-item synthesis budget;
   - graph evidence matching the risk named in the question is prioritized;
   - if Qwen's strictly filtered answer has no factual claims, a deterministic evidence-first answer is built from existing TEMP/GRAPH/XBRL evidence and valid citation IDs;
   - no citation is invented and uncited model claims remain removed;
   - misleading "untrusted SEC data" presentation is stripped while security wrapping remains intact.

2. **Temporal change classifier v3**
   - broader temporal-only synonym/context detection without weakening graph extraction;
   - topic-local passages are kept isolated from neighboring unrelated risk text;
   - NEW/REMOVED are based on topic presence;
   - EXPANDED/REDUCED use containment + information gain/loss + topic-local evidence count;
   - prior reviewed rows remain development-only; fresh blind gold is still required for final reporting.

3. **Graph edge quality v3**
   - strong topic-specific evidence rules plus exposure/consequence cues;
   - explicit rejection of generic legal/manufacturing and regulatory-laundry-list false positives;
   - `build_graph` now selects the best provenance span deterministically for each company/risk/filing/year relation instead of allowing the last processed chunk to overwrite earlier evidence;
   - graph report's `risk_edges` now means unique stored risk edges, not raw candidate matches.

4. **Patch-5 diagnostic**
   - temporal diagnostic still compares current corpus predictions against the already-reviewed development labels;
   - graph diagnostic scores the already-reviewed evidence spans through the current edge-quality rule, avoiding edge-ID collision artifacts;
   - diagnostic is explicitly development-only.

## Validated in packaged source

- Python compilation: PASS
- Complete available suite: 79 tests passed
- Frozen-file comparison vs Patch 4 source: 0 frozen files changed

## Post-install commands

```bat
call FilingsGraph_Correction_Patch_5\APPLY_PATCH_5.cmd
python -m scripts.build_graph
python -m scripts.evaluate_temporal
python -m scripts.evaluate_patch5_diagnostic
python -m scripts.evaluate_grounding --live
python -m scripts.check_v6_freeze
```

Do not export/review the fresh blind Temporal/Graph files until this development gate has been inspected.
