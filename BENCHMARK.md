# Benchmark Policy

All headline metrics are **TBD until produced by local execution**.

FilingsGraph evaluates:

- retrieval: Recall@5/10, Precision@K, Hit Rate, MRR, nDCG@10;
- numeric: fact selection, exact calculation, unit, period, concept resolution;
- temporal: correct-period accuracy and risk-change classification;
- graph: entity resolution, edge/path accuracy, graph-added evidence recall, expansion rate;
- grounding: citation precision/completeness and unsupported-claim rate;
- routing: query classification and tool-selection accuracy;
- system: P50/P95 latency, component latency, memory/VRAM observations when available.

Ablations compare dense, BM25, hybrid, reranked hybrid, structured XBRL, temporal retrieval, graph retrieval,
and the full routed system. Generated results are written to `reports/`.
