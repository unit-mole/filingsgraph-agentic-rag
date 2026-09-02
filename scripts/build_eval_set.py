from __future__ import annotations

import argparse
import hashlib
import random
import re
from collections import defaultdict

from filingsgraph.core.config import ROOT, load_yaml
from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository
from scripts._common import load_jsonl, save_jsonl, save_json

STOPWORDS = {
    "the","and","for","that","with","from","this","have","has","were","was","are","our","their","its",
    "which","into","about","such","may","could","would","will","also","than","these","those","been","being",
    "company","companies","business","including","other","more","year","fiscal","results","operations","risk",
}


def _topic_terms(topic: str) -> list[str]:
    return [x for x in re.findall(r"[a-z]+", topic.lower()) if len(x) > 3]


def _contains_topic(text: str, topic: str) -> bool:
    t = text.lower()
    terms = _topic_terms(topic)
    return bool(terms) and any(term in t for term in terms)


def _salient_phrase(text: str, max_terms: int = 5) -> str:
    first = re.split(r"(?<=[.!?])\s+", text.strip())[0]
    toks = [x.lower() for x in re.findall(r"[A-Za-z][A-Za-z-]+", first)]
    picked: list[str] = []
    for tok in toks:
        if len(tok) < 4 or tok in STOPWORDS or tok in picked:
            continue
        picked.append(tok)
        if len(picked) >= max_terms:
            break
    return " ".join(picked) if picked else first[:100]


def _stable_key(q: dict) -> str:
    return hashlib.sha1(
        f"{q.get('category')}|{q.get('question')}|{q.get('expected_company')}|{q.get('expected_periods')}".encode()
    ).hexdigest()


def _stratified_split(questions: list[dict], dev_fraction: float, seed: int) -> tuple[list[dict], list[dict]]:
    rng = random.Random(seed)
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for q in questions:
        by_cat[q["category"]].append(q)
    dev: list[dict] = []
    test: list[dict] = []
    for cat, rows in sorted(by_cat.items()):
        rows = sorted(rows, key=_stable_key)
        rng.shuffle(rows)
        if len(rows) <= 1:
            cut = len(rows)
        else:
            cut = max(1, min(len(rows) - 1, round(len(rows) * dev_fraction)))
        dev.extend(rows[:cut])
        test.extend(rows[cut:])
    rng.shuffle(dev)
    rng.shuffle(test)
    for q in dev:
        q["split"] = "dev"
    for q in test:
        q["split"] = "test"
    return dev, test


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force-test", action="store_true", help="Replace the frozen test split. Use only when creating a new benchmark version.")
    args = ap.parse_args()

    cfg = load_yaml("evaluation.yaml")
    targets = cfg.get("category_targets", {})
    seed = int(cfg.get("seed", 42))
    dev_fraction = float(cfg.get("dev_fraction", 0.70))
    rng = random.Random(seed)
    chunks = load_jsonl("data/processed/chunks.jsonl")
    topics = load_yaml("graph.yaml").get("risk_topics", [])
    questions: list[dict] = []

    # ---------- Text retrieval gold ----------
    # Stratify by ticker/section/year before sampling so one issuer/section does
    # not dominate. Questions are semantic topic prompts, not copied first
    # sentences, reducing BM25 leakage while preserving deterministic gold.
    text_candidates: list[dict] = []
    for c in chunks:
        text = c.get("text", "")
        if len(text) < 180:
            continue
        phrase = _salient_phrase(text)
        if not phrase:
            continue
        text_candidates.append(
            {
                "category": "textual_lookup",
                "question": f"What did {c['ticker']} disclose in FY{c.get('fiscal_year')} {c['section']} about {phrase}?",
                "expected_company": c["ticker"],
                "expected_filing": c["accession_number"],
                "expected_section": c["section"],
                "relevant_chunk_ids": [c["chunk_id"]],
                "expected_periods": [c["fiscal_year"]] if c.get("fiscal_year") else [],
            }
        )
    rng.shuffle(text_candidates)
    questions.extend(text_candidates[: int(targets.get("textual_lookup", 60))])

    # ---------- Filing-aligned XBRL fact gold ----------
    db = Database()
    repo = Repository(db)
    numeric_candidates: list[dict] = []
    for company in repo.companies():
        ticker = company["ticker"]
        for metric in ("revenue", "net_income", "operating_income", "capex", "assets", "cash"):
            for row in repo.metric_history(ticker, metric):
                numeric_candidates.append(
                    {
                        "category": "exact_financial_fact",
                        "question": f"What was {ticker} {metric.replace('_', ' ')} in FY{row['fiscal_year']}?",
                        "expected_company": ticker,
                        "expected_value": row["value"],
                        "expected_unit": row["unit"],
                        "expected_periods": [row["fiscal_year"]],
                        "metadata": {
                            "metric": metric,
                            "fact_id": row.get("fact_id"),
                            "expected_accession": row.get("target_accession") or row.get("accession_number"),
                            "concept": row.get("concept"),
                        },
                    }
                )
    db.close()
    rng.shuffle(numeric_candidates)
    questions.extend(numeric_candidates[: int(targets.get("exact_financial_fact", 40))])

    # Index Item 1A chunks by ticker/year and create topic evidence maps.
    risk_chunks: dict[str, dict[int, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for c in chunks:
        if c.get("section") == "Item 1A" and c.get("fiscal_year"):
            risk_chunks[c["ticker"]][int(c["fiscal_year"])].append(c)

    # ---------- Temporal gold ----------
    temporal_candidates: list[dict] = []
    mixed_candidates: list[dict] = []
    for ticker, years_map in risk_chunks.items():
        years = sorted(years_map)
        for old_y, new_y in zip(years, years[1:]):
            for topic in topics:
                old_hits = [c for c in years_map[old_y] if _contains_topic(c.get("text", ""), topic)]
                new_hits = [c for c in years_map[new_y] if _contains_topic(c.get("text", ""), topic)]
                if not old_hits and not new_hits:
                    continue
                rel = list(dict.fromkeys([c["chunk_id"] for c in (old_hits[:2] + new_hits[:2])]))
                temporal_candidates.append(
                    {
                        "category": "temporal",
                        "question": f"How did {ticker}'s {topic} risk disclosure change from FY{old_y} to FY{new_y}?",
                        "expected_company": ticker,
                        "expected_periods": [old_y, new_y],
                        "relevant_chunk_ids": rel,
                        "metadata": {"risk_topic": topic},
                    }
                )
                mixed_candidates.append(
                    {
                        "category": "mixed",
                        "question": f"How did {ticker} revenue change from FY{old_y} to FY{new_y}, and how did its {topic} risk disclosure change over the same period?",
                        "expected_company": ticker,
                        "expected_periods": [old_y, new_y],
                        "relevant_chunk_ids": rel,
                        "metadata": {"risk_topic": topic, "metric": "revenue"},
                    }
                )
    rng.shuffle(temporal_candidates)
    rng.shuffle(mixed_candidates)
    questions.extend(temporal_candidates[: int(targets.get("temporal", 30))])
    questions.extend(mixed_candidates[: int(targets.get("mixed", 20))])

    # ---------- Graph-relevant cross-company gold ----------
    graph_candidates: list[dict] = []
    years = sorted({int(c["fiscal_year"]) for c in chunks if c.get("fiscal_year")})
    for year in years:
        for topic in topics:
            hits = [
                c for c in chunks
                if c.get("section") == "Item 1A"
                and c.get("fiscal_year") == year
                and _contains_topic(c.get("text", ""), topic)
            ]
            companies = sorted({c["ticker"] for c in hits})
            if len(companies) < 2:
                continue
            graph_candidates.append(
                {
                    "category": "graph",
                    "question": f"Which selected companies share exposure to {topic} risk in FY{year}, and what filing evidence connects them?",
                    "expected_companies": companies,
                    "expected_periods": [year],
                    "relevant_chunk_ids": list(dict.fromkeys(c["chunk_id"] for c in hits[:10])),
                    "metadata": {"risk_topic": topic},
                }
            )
    rng.shuffle(graph_candidates)
    questions.extend(graph_candidates[: int(targets.get("graph", 30))])

    # ---------- No-answer controls ----------
    tickers = sorted({c["ticker"] for c in chunks})
    no_answer_candidates: list[dict] = []
    for i in range(max(1, int(targets.get("no_answer", 20)))):
        t = tickers[i % len(tickers)] if tickers else "NVDA"
        no_answer_candidates.append(
            {
                "category": "no_answer",
                "question": f"What acquisition price did {t} pay for fictional target FG-{1000+i}, which is not present in the selected filings?",
                "expected_company": t,
                "expected_answer": None,
                "relevant_chunk_ids": [],
                "metadata": {"should_abstain": True},
            }
        )
    questions.extend(no_answer_candidates[: int(targets.get("no_answer", 20))])

    # Assign stable IDs only after the candidate set is complete.
    dedup: dict[str, dict] = {}
    for q in questions:
        dedup[_stable_key(q)] = q
    questions = list(dedup.values())
    for i, q in enumerate(sorted(questions, key=_stable_key)):
        q["id"] = f"fg2-{q['category'][:4]}-{i:04d}"
        q.setdefault("split", "")

    dev, proposed_test = _stratified_split(questions, dev_fraction, seed)
    save_jsonl("data/evaluation/dev/questions.jsonl", dev)

    test_path = ROOT / "data/evaluation/test/questions.jsonl"
    if test_path.exists() and not args.force_test:
        existing = load_jsonl("data/evaluation/test/questions.jsonl")
        test = existing if existing else proposed_test
        if not existing:
            save_jsonl("data/evaluation/test/questions.jsonl", test)
    else:
        test = proposed_test
        save_jsonl("data/evaluation/test/questions.jsonl", test)

    combined = dev + test
    categories = {
        c: sum(q.get("category") == c for q in combined)
        for c in sorted({q.get("category") for q in combined})
    }
    report = {
        "benchmark_version": "v2_patch1",
        "total": len(combined),
        "dev": len(dev),
        "test": len(test),
        "categories": categories,
        "target_categories": targets,
        "note": "DEV may be used for tuning. TEST is frozen unless --force-test is explicitly supplied.",
    }
    save_json("reports/final/eval_dataset_report.json", report)
    print(report)


if __name__ == "__main__":
    main()
