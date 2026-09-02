from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from filingsgraph.schemas.financial_facts import FinancialFact
from filingsgraph.xbrl.concepts import normalize_concept
from filingsgraph.xbrl.periods import fiscal_year_from_frame, fiscal_period_from_frame
from filingsgraph.xbrl.units import normalize_unit, normalize_value

FLOW_METRICS = {"revenue", "net_income", "operating_income", "gross_profit", "capex"}


def parse_companyfacts(path: str | Path, ticker: str | None = None, forms: set[str] | None = None) -> list[FinancialFact]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    cik = str(data.get("cik", "")).zfill(10)
    forms = forms or {"10-K", "10-Q"}
    out: list[FinancialFact] = []
    for taxonomy, concepts in data.get("facts", {}).items():
        for concept, payload in concepts.items():
            metric, method, confidence = normalize_concept(concept)
            label = payload.get("label")
            for unit, facts in payload.get("units", {}).items():
                for f in facts:
                    if f.get("form") not in forms or "val" not in f:
                        continue
                    frame = f.get("frame")
                    end = f.get("end")
                    fy = fiscal_year_from_frame(frame, end, f.get("fy"))
                    fp = fiscal_period_from_frame(frame, f.get("fp"))
                    val = float(f["val"])
                    out.append(
                        FinancialFact(
                            cik=cik,
                            ticker=ticker,
                            concept=concept,
                            label=label,
                            taxonomy=taxonomy,
                            unit=normalize_unit(unit),
                            raw_value=val,
                            scale=1.0,
                            normalized_value=normalize_value(val),
                            start_date=f.get("start"),
                            end_date=end,
                            instant_date=None if f.get("start") else end,
                            fiscal_year=fy,
                            fiscal_period=fp,
                            form_type=f.get("form"),
                            accession_number=f.get("accn"),
                            filed_date=f.get("filed"),
                            frame=frame,
                            normalized_metric=metric,
                            mapping_method=method,
                            mapping_confidence=confidence,
                        )
                    )
    return out


def _duration_days(start: str | None, end: str | None) -> int | None:
    if not start or not end:
        return None
    try:
        return (date.fromisoformat(end) - date.fromisoformat(start)).days
    except ValueError:
        return None


def annual_fact_score(
    fact: FinancialFact,
    *,
    target_accession: str | None = None,
    target_report_date: str | None = None,
) -> tuple[float, ...]:
    """Deterministic preference score for one annual fact candidate.

    The strongest signal is provenance: a fact from the exact downloaded 10-K
    accession and report date. For flow metrics we additionally favor a roughly
    annual duration, preventing quarterly/comparative contexts from winning.
    """
    exact_accession = 1.0 if target_accession and fact.accession_number == target_accession else 0.0
    exact_end = 1.0 if target_report_date and fact.end_date == target_report_date else 0.0
    fy_period = 1.0 if fact.fiscal_period in {"FY", None} else 0.0
    duration = _duration_days(fact.start_date, fact.end_date)
    if fact.normalized_metric in FLOW_METRICS:
        annual_duration = 1.0 if duration is not None and 300 <= duration <= 400 else 0.0
    else:
        # Instant metrics such as assets/cash legitimately have no start date.
        annual_duration = 1.0 if fact.start_date is None else 0.0
    return (
        exact_accession,
        exact_end,
        annual_duration,
        fy_period,
        float(fact.mapping_confidence or 0.0),
        1.0 if fact.mapping_method == "deterministic_map" else 0.0,
    )


def choose_annual_fact(
    facts: list[FinancialFact],
    metric: str,
    fiscal_year: int,
    *,
    target_accession: str | None = None,
    target_report_date: str | None = None,
) -> FinancialFact | None:
    candidates = [
        f
        for f in facts
        if f.normalized_metric == metric
        and f.fiscal_year == fiscal_year
        and f.form_type == "10-K"
        and (target_report_date is None or f.end_date == target_report_date)
    ]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda f: annual_fact_score(
            f,
            target_accession=target_accession,
            target_report_date=target_report_date,
        ),
    )
