from __future__ import annotations
import json
from pathlib import Path
from filingsgraph.schemas.financial_facts import FinancialFact
from filingsgraph.xbrl.concepts import normalize_concept
from filingsgraph.xbrl.periods import fiscal_year_from_frame, fiscal_period_from_frame
from filingsgraph.xbrl.units import normalize_unit, normalize_value

def parse_companyfacts(path: str | Path, ticker: str | None = None, forms: set[str] | None = None) -> list[FinancialFact]:
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    cik=str(data.get("cik", "")).zfill(10)
    forms=forms or {"10-K","10-Q"}
    out=[]
    for taxonomy, concepts in data.get("facts", {}).items():
        for concept, payload in concepts.items():
            metric, method, confidence=normalize_concept(concept)
            label=payload.get("label")
            for unit, facts in payload.get("units", {}).items():
                for f in facts:
                    if f.get("form") not in forms or "val" not in f: continue
                    frame=f.get("frame")
                    end=f.get("end")
                    fy=fiscal_year_from_frame(frame,end,f.get("fy"))
                    fp=fiscal_period_from_frame(frame,f.get("fp"))
                    val=float(f["val"])
                    out.append(FinancialFact(
                        cik=cik, ticker=ticker, concept=concept, label=label, taxonomy=taxonomy,
                        unit=normalize_unit(unit), raw_value=val, scale=1.0, normalized_value=normalize_value(val),
                        start_date=f.get("start"), end_date=end, instant_date=None if f.get("start") else end,
                        fiscal_year=fy, fiscal_period=fp, form_type=f.get("form"), accession_number=f.get("accn"),
                        filed_date=f.get("filed"), frame=frame, normalized_metric=metric,
                        mapping_method=method, mapping_confidence=confidence,
                    ))
    return out

def choose_annual_fact(facts: list[FinancialFact], metric: str, fiscal_year: int) -> FinancialFact | None:
    candidates=[f for f in facts if f.normalized_metric==metric and f.fiscal_year==fiscal_year and f.form_type=="10-K" and f.fiscal_period in {"FY", None}]
    if not candidates: return None
    candidates.sort(key=lambda x: (x.filed_date or "", x.mapping_confidence), reverse=True)
    return candidates[0]
