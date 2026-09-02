from __future__ import annotations

import csv,json
from pathlib import Path
from sklearn.metrics import accuracy_score,f1_score
from scripts._common import save_json

ALLOWED={"NEW","REMOVED","UNCHANGED","EXPANDED","REDUCED"}

def main():
    p=Path("reports/gold/temporal_review.csv")
    if not p.exists(): raise FileNotFoundError("Run python -m scripts.export_temporal_gold first.")
    with p.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
    reviewed=[r for r in rows if (r.get("gold_change_type") or "").strip().upper() in ALLOWED]
    if not reviewed: raise ValueError("No reviewed temporal rows. Fill gold_change_type in reports/gold/temporal_review.csv first.")
    y_true=[r["gold_change_type"].strip().upper() for r in reviewed]; y_pred=[r["predicted_change_type"].strip().upper() for r in reviewed]
    report={"reviewed_rows":len(reviewed),"total_review_rows":len(rows),"risk_change_f1":f1_score(y_true,y_pred,average="macro",zero_division=0),"risk_change_accuracy":accuracy_score(y_true,y_pred),"labels":sorted(ALLOWED),"gold_source":"human-reviewed reports/gold/temporal_review.csv"}
    save_json("reports/temporal/temporal_gold_metrics.json",report); print(json.dumps(report,indent=2))

if __name__=="__main__": main()
