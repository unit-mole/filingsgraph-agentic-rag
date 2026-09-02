from __future__ import annotations

import argparse,csv,random
from pathlib import Path
from scripts._common import load_json

ALLOWED="NEW|REMOVED|UNCHANGED|EXPANDED|REDUCED"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--sample-size",type=int,default=30); args=ap.parse_args()
    data=load_json("reports/temporal/temporal_evaluation.json",{}) or {}
    rows=[]
    for block in data.get("rows",[]):
        for c in block.get("changes",[]):
            rows.append({
                "ticker":block.get("ticker"),"from_year":block.get("from"),"to_year":block.get("to"),
                "topic":c.get("topic"),"predicted_change_type":c.get("change_type"),
                "similarity":c.get("similarity"),"old_excerpt":(c.get("old_excerpt") or "")[:800],
                "new_excerpt":(c.get("new_excerpt") or "")[:800],"gold_change_type":"","review_note":"",
            })
    rng=random.Random(42); rng.shuffle(rows)
    # Ensure broad issuer coverage before filling the rest deterministically.
    chosen=[]; seen=set()
    for r in rows:
        if r["ticker"] not in seen:
            chosen.append(r); seen.add(r["ticker"])
    for r in rows:
        if len(chosen)>=args.sample_size: break
        if r not in chosen: chosen.append(r)
    p=Path("reports/gold/temporal_review.csv"); p.parent.mkdir(parents=True,exist_ok=True)
    fields=list(chosen[0]) if chosen else ["ticker","from_year","to_year","topic","predicted_change_type","similarity","old_excerpt","new_excerpt","gold_change_type","review_note"]
    with p.open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(chosen)
    print({"rows":len(chosen),"path":str(p),"instruction":f"Fill gold_change_type with one of {ALLOWED}, save CSV, then run scripts.score_temporal_gold."})

if __name__=="__main__": main()
