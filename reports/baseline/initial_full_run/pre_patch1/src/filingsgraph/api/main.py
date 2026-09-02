from __future__ import annotations
from pathlib import Path
import json
from fastapi import FastAPI, HTTPException
from filingsgraph.schemas.queries import ResearchRequest
from filingsgraph.api.dependencies import get_repo
from filingsgraph.agents.planner import plan
from filingsgraph.api.routes.research import compare_companies, risk_evolution, company_graph

app = FastAPI(
    title="FilingsGraph API",
    version="0.1.0",
    description="Temporal financial due-diligence and risk intelligence. Research tool; not investment advice.",
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "filingsgraph", "paid_llm_required": False}

@app.get("/companies")
def companies():
    try:
        return get_repo().companies()
    except Exception:
        return []

@app.get("/filings")
def filings(ticker: str | None = None):
    repo = get_repo()
    q = "SELECT accession_number,ticker,form_type,filing_date,report_date,fiscal_year,source_url FROM filings"
    args = []
    if ticker:
        q += " WHERE upper(ticker)=upper(?)"
        args = [ticker]
    rows = repo.db.conn.execute(q, args).fetchall()
    cols = ["accession_number", "ticker", "form_type", "filing_date", "report_date", "fiscal_year", "source_url"]
    return [dict(zip(cols, r)) for r in rows]

@app.post("/research")
def research(req: ResearchRequest):
    # Lightweight API startup intentionally avoids loading multi-GB models at import time.
    p = plan(req.question, req.tickers, req.fiscal_years)
    return {
        "query_id": "planning-only",
        "question": req.question,
        "query_type": p.query_type,
        "plan": p.model_dump(),
        "answer": "Planning endpoint is healthy. Use the Gradio Full local model/index mode or initialize ResearchOrchestrator for live evidence synthesis.",
        "evidence": [],
        "calculations": [],
        "verification": {},
        "limitations": ["Heavy local models/indexes are lazy-loaded, not imported at API startup."],
    }

@app.get("/research/{query_id}")
def research_status(query_id: str):
    return {"query_id": query_id, "status": "stateless-local-demo", "note": "Persist research runs in a production extension if required."}

@app.post("/compare/companies")
def compare_companies_endpoint(payload: dict):
    try:
        return compare_companies(payload["tickers"], payload.get("metric", "revenue"))
    except Exception as e:
        raise HTTPException(400, str(e)) from e

@app.post("/compare/periods")
def compare_periods_endpoint(payload: dict):
    from filingsgraph.tools.xbrl_tools import compare_periods
    try:
        return compare_periods(
            get_repo(), payload["ticker"], payload["metric"], int(payload["old_year"]), int(payload["new_year"])
        )
    except Exception as e:
        raise HTTPException(400, str(e)) from e

@app.post("/risks/evolution")
def risks_evolution_endpoint(payload: dict):
    try:
        return risk_evolution(payload["ticker"])
    except Exception as e:
        raise HTTPException(400, str(e)) from e

@app.get("/graph/company/{ticker}")
def graph_company_endpoint(ticker: str):
    return company_graph(ticker)

@app.get("/graph/risk/{risk_id}")
def graph_risk_endpoint(risk_id: str):
    from filingsgraph.core.config import ROOT
    from filingsgraph.graph.builder import TemporalKnowledgeGraph
    p = ROOT / "data" / "graph" / "filingsgraph.json"
    if not p.exists():
        return {"risk_id": risk_id, "nodes": [], "edges": []}
    kg = TemporalKnowledgeGraph.load(p)
    matches = [n for n, a in kg.graph.nodes(data=True) if n == risk_id or risk_id.lower() in str(a.get("label", "")).lower()]
    from filingsgraph.graph.traversal import traverse
    return traverse(kg.graph, matches[:3], max_hops=2, max_nodes=30)

@app.post("/retrieval/debug")
def retrieval_debug(payload: dict):
    # Debug route is intentionally lightweight and does not silently download models.
    return {
        "question": payload.get("question"),
        "filters": payload.get("filters", {}),
        "instructions": "Use scripts.evaluate_retrieval or the full Gradio runtime after building the local index.",
    }

@app.get("/metrics/summary")
def metrics_summary():
    p = Path("reports/final/summary.json")
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"status": "TBD until evaluation is run"}
