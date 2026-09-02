from __future__ import annotations
import json
import re
import uuid
from pathlib import Path

from filingsgraph.agents.planner import plan
from filingsgraph.core.config import ROOT, load_yaml
from filingsgraph.retrieval.filters import infer_query_filters
from filingsgraph.llm.prompts import SYSTEM_PROMPT, SYNTHESIS_TEMPLATE
from filingsgraph.llm.grounding import enforce_grounding_contract, has_factual_claim, build_evidence_first_fallback
from filingsgraph.security.prompt_injection import wrap_untrusted_data
from filingsgraph.verification.citations import verify_citations
from filingsgraph.verification.numeric import verify_calculations
from filingsgraph.verification.temporal import verify_temporal
from filingsgraph.verification.claims import verify_entities, detect_contradictions

METRIC_TERMS = {
    "revenue": ["revenue", "sales"],
    "net_income": ["net income", "earnings"],
    "operating_income": ["operating income"],
    "gross_profit": ["gross profit"],
    "capex": ["capex", "capital expenditure", "capital spending"],
    "assets": ["assets"],
    "cash": ["cash", "cash equivalents"],
}


def infer_metric(question: str) -> str | None:
    q = question.lower()
    for metric, terms in METRIC_TERMS.items():
        if any(term in q for term in terms):
            return metric
    return None


def load_chunks() -> list[dict]:
    p = ROOT / "data" / "processed" / "chunks.jsonl"
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


class ResearchOrchestrator:
    """Single routed research orchestrator with deterministic tools and independent verification."""

    def __init__(self, retriever=None, reranker=None, repo=None, graph=None, llm=None):
        self.retriever = retriever
        self.reranker = reranker
        self.repo = repo
        self.graph = graph
        self.llm = llm

    def _text_branch(self, question: str, p) -> list[dict]:
        if not (p.use_text and self.retriever):
            return []
        known = [str(x["ticker"]).upper() for x in load_yaml("companies.yaml").get("companies", []) if x.get("ticker")]
        filters = infer_query_filters(question, known)
        if len(p.entities) == 1:
            filters["ticker"] = p.entities[0].upper()
        if len(p.periods) == 1:
            filters["fiscal_year"] = p.periods[0]
        elif len(p.periods) > 1 and len(p.entities) == 1:
            filters["fiscal_year"] = sorted(set(p.periods))
        results = self.retriever.search(question, filters=filters or None, fusion_top_k=20)
        if self.reranker:
            results = self.reranker.rerank(question, results, top_k=8)
        evidence = []
        for i, r in enumerate(results[:8], 1):
            payload = r.get("payload", {})
            cid = (
                f"SEC-{payload.get('ticker','UNK')}-{payload.get('fiscal_year','NA')}-"
                f"{payload.get('section','UNK').replace(' ','')}-{i:03d}"
            )
            evidence.append(
                {
                    "citation_id": cid,
                    "evidence_type": "filing_chunk",
                    "company": payload.get("company_name"),
                    "ticker": payload.get("ticker"),
                    "fiscal_year": payload.get("fiscal_year"),
                    "filing": payload.get("accession_number"),
                    "section": payload.get("section"),
                    "source_url": payload.get("source_url"),
                    "source_excerpt": payload.get("text", "")[:1400],
                    "retrieval_method": r.get("method"),
                    "score": r.get("rerank_score", r.get("score")),
                    "payload": payload,
                }
            )
        return evidence

    def _xbrl_branch(self, question: str, p) -> tuple[list[dict], list[dict]]:
        if not (p.use_xbrl and self.repo and p.entities):
            return [], []
        metric = infer_metric(question)
        if not metric:
            return [], []
        evidence = []
        calculations = []
        from filingsgraph.finance.calculations import growth_rate

        for ticker in p.entities:
            history = self.repo.metric_history(ticker, metric)
            if p.periods:
                history = [h for h in history if h.get("fiscal_year") in set(p.periods)]
            for row in history:
                cid = f"XBRL-{ticker.upper()}-{metric.upper()}-{row.get('fiscal_year','NA')}"
                evidence.append(
                    {
                        "citation_id": cid,
                        "evidence_type": "xbrl_fact",
                        "company": ticker.upper(),
                        "ticker": ticker.upper(),
                        "fiscal_year": row.get("fiscal_year"),
                        "filing": row.get("accession_number"),
                        "section": "SEC XBRL Company Facts",
                        "source_url": None,
                        "source_excerpt": f"{metric} = {row.get('value')} {row.get('unit')}",
                        "retrieval_method": "deterministic_xbrl",
                        "score": 1.0,
                        "payload": row,
                    }
                )
            if len(history) >= 2:
                ordered = sorted(history, key=lambda x: x.get("fiscal_year") or 0)
                old, new = ordered[-2], ordered[-1]
                if old.get("unit") == new.get("unit") and float(old.get("value", 0)) != 0:
                    output = growth_rate(float(old["value"]), float(new["value"]))
                    calculations.append(
                        {
                            "calculation_id": f"CALC-{ticker.upper()}-{metric.upper()}-{old['fiscal_year']}-{new['fiscal_year']}",
                            "function": "growth_rate",
                            "inputs": {"previous": old["value"], "current": new["value"]},
                            "output": output,
                            "unit": "percent",
                            "source_fact_ids": [old.get("fact_id"), new.get("fact_id")],
                        }
                    )
        return evidence, calculations

    def _temporal_branch(self, p) -> tuple[list[dict], list[dict]]:
        if not (p.use_temporal and p.entities):
            return [], []
        chunks = load_chunks()
        topics = load_yaml("graph.yaml").get("risk_topics", [])
        from filingsgraph.temporal.risk_diff import compare_risk_disclosures

        evidence = []
        findings = []
        for ticker in p.entities:
            by_year: dict[int, list[str]] = {}
            source_by_year: dict[int, list[dict]] = {}
            for c in chunks:
                if c.get("ticker") == ticker.upper() and c.get("section") == "Item 1A" and c.get("fiscal_year"):
                    y = int(c["fiscal_year"])
                    if p.periods and y not in set(p.periods):
                        continue
                    by_year.setdefault(y, []).append(c.get("text", ""))
                    source_by_year.setdefault(y, []).append(c)
            years = sorted(by_year)
            for old_y, new_y in zip(years, years[1:]):
                changes = compare_risk_disclosures(
                    " ".join(by_year[old_y]), " ".join(by_year[new_y]), topics
                )
                for change in changes:
                    if change["change_type"] == "UNCHANGED" and not change.get("new_excerpt"):
                        continue
                    finding = {"ticker": ticker.upper(), "from_year": old_y, "to_year": new_y, **change}
                    findings.append(finding)
                    src = (source_by_year.get(new_y) or source_by_year.get(old_y) or [{}])[0]
                    cid = f"TEMP-{ticker.upper()}-{change['risk_id']}-{old_y}-{new_y}"
                    evidence.append(
                        {
                            "citation_id": cid,
                            "evidence_type": "temporal_risk_change",
                            "company": ticker.upper(),
                            "ticker": ticker.upper(),
                            "fiscal_year": new_y,
                            "filing": src.get("accession_number"),
                            "section": "Item 1A",
                            "source_url": src.get("source_url"),
                            "source_excerpt": change.get("new_excerpt") or change.get("old_excerpt") or "",
                            "retrieval_method": "temporal_alignment",
                            "score": change.get("similarity"),
                            "payload": finding,
                        }
                    )
        return evidence[:12], findings

    def _graph_branch(self, p, question: str = "") -> tuple[list[dict], list[dict]]:
        if not (p.use_graph and self.graph is not None and p.entities):
            return [], []
        from filingsgraph.graph.traversal import traverse

        evidence = []
        paths = []
        for ticker in p.entities:
            seeds = [
                n
                for n, a in self.graph.nodes(data=True)
                if a.get("node_type") == "Company" and str(a.get("ticker", "")).upper() == ticker.upper()
            ]
            if not seeds:
                continue
            result = traverse(
                self.graph,
                seeds,
                max_hops=2,
                max_nodes=30,
                period=max(p.periods) if p.periods else None,
            )
            paths.append({"ticker": ticker.upper(), **result})
            # Prioritize graph evidence that actually matches the risk topic named
            # in the question, then fall back to confidence. This keeps relevant
            # provenance inside the limited evidence bundle.
            from filingsgraph.risk_topics import infer_risk_topics_from_question, topic_match_score, temporal_topic_match_score
            requested = infer_risk_topics_from_question(question)
            topic = requested[0] if requested else None
            candidate_edges = [e for e in result.get("edges", []) if e.get("source_text_span")]
            def edge_rank(edge):
                span = edge.get("source_text_span", "")
                match = 0
                if topic:
                    match = max(topic_match_score(topic, span), temporal_topic_match_score(topic, span))
                return (1 if match else 0, match, float(edge.get("confidence") or 0.0))
            candidate_edges.sort(key=edge_rank, reverse=True)
            for i, edge in enumerate(candidate_edges[:10], 1):
                cid = f"GRAPH-{ticker.upper()}-{i:03d}"
                evidence.append(
                    {
                        "citation_id": cid,
                        "evidence_type": "graph_edge",
                        "company": ticker.upper(),
                        "ticker": ticker.upper(),
                        "fiscal_year": int(edge["valid_from"])
                        if str(edge.get("valid_from", "")).isdigit()
                        else None,
                        "filing": edge.get("filing_id"),
                        "section": "Graph relationship",
                        "source_url": None,
                        "source_excerpt": edge.get("source_text_span", "")[:1200],
                        "retrieval_method": "graph_traversal",
                        "score": edge.get("confidence"),
                        "payload": edge,
                    }
                )
        return evidence, paths

    def research(
        self, question: str, tickers: list[str] | None = None, years: list[int] | None = None
    ) -> dict:
        query_id = str(uuid.uuid4())
        p = plan(question, tickers, years)
        text_evidence = self._text_branch(question, p)
        xbrl_evidence, calculations = self._xbrl_branch(question, p)
        temporal_evidence, temporal_findings = self._temporal_branch(p)
        graph_evidence, graph_paths = self._graph_branch(p, question)

        # Put the routed specialized evidence first so it cannot be crowded out by
        # the 20-item synthesis/verification evidence budget. Core retrieval itself
        # is unchanged.
        qtype = str(p.query_type).upper()
        if qtype == "GRAPH":
            evidence = graph_evidence + text_evidence + xbrl_evidence + temporal_evidence
        elif qtype == "TEMPORAL":
            evidence = temporal_evidence + text_evidence + xbrl_evidence + graph_evidence
        elif qtype == "NUMERIC":
            evidence = xbrl_evidence + text_evidence + temporal_evidence + graph_evidence
        elif qtype == "MIXED":
            evidence = xbrl_evidence + temporal_evidence + graph_evidence + text_evidence
        else:
            evidence = text_evidence + xbrl_evidence + temporal_evidence + graph_evidence

        contradictions = detect_contradictions(evidence)
        limitations: list[str] = []
        if p.use_text and not any(e["evidence_type"] == "filing_chunk" for e in evidence):
            limitations.append("No textual filing evidence was retrieved from the local index.")
        if p.use_xbrl and not xbrl_evidence:
            limitations.append("The requested structured metric could not be resolved from the local XBRL database.")
        if p.use_graph and not graph_evidence:
            limitations.append("No provenance-bearing graph evidence matched the routed graph question.")

        bundle = "\n\n".join(
            f"[{e['citation_id']}] {wrap_untrusted_data(e.get('source_excerpt') or '')}"
            for e in evidence[:20]
        )
        prompt = SYNTHESIS_TEMPLATE.format(
            question=question,
            plan=p.model_dump_json(indent=2),
            evidence=bundle or "No evidence available.",
            calculations=json.dumps(calculations, indent=2),
            contradictions="\n".join(contradictions) or "None detected.",
        )
        prompt += "\n\nTemporal findings:\n" + json.dumps(temporal_findings[:20], indent=2)
        prompt += "\n\nGraph paths:\n" + json.dumps(graph_paths[:5], indent=2)

        if self.llm:
            answer = self.llm.generate(
                [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                max_new_tokens=900,
                temperature=0.0,
            )
            answer = enforce_grounding_contract(answer, evidence[:20])
            if not has_factual_claim(answer):
                answer = build_evidence_first_fallback(
                    qtype, question, evidence[:20], calculations, temporal_findings
                )
                answer = enforce_grounding_contract(answer, evidence[:20])
        else:
            snippets = "\n".join(
                f"[{e['citation_id']}] {e.get('source_excerpt','')[:300]}" for e in evidence[:6]
            )
            answer = (
                "Evidence bundle produced. Configure/load the local Qwen model for full analyst synthesis.\n\n"
                + (snippets or "No evidence available.")
            )

        verification = {
            "citations": verify_citations(answer, evidence[:20]),
            "numeric": verify_calculations(calculations),
            "temporal": verify_temporal(evidence, p.periods),
            "entity": verify_entities(evidence, p.entities),
        }
        return {
            "query_id": query_id,
            "question": question,
            "query_type": p.query_type,
            "plan": p.model_dump(),
            "answer": answer,
            "evidence": evidence,
            "calculations": calculations,
            "temporal_findings": temporal_findings,
            "graph_paths": graph_paths,
            "contradictions": contradictions,
            "verification": verification,
            "limitations": limitations,
        }
