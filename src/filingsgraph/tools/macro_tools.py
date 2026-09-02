from __future__ import annotations
from pathlib import Path
import pandas as pd
from filingsgraph.core.config import ROOT, get_settings


def get_macro_series(series_name: str) -> pd.DataFrame:
    """Load an optional locally downloaded macro CSV. Core FilingsGraph does not require FRED."""
    path = ROOT / "data" / "macro" / f"{series_name}.csv"
    if not path.exists():
        raise FileNotFoundError(
            f"Optional macro series not found: {path}. Place a public CSV there or enable a future user-key FRED adapter."
        )
    return pd.read_csv(path)


def compare_macro_period(series_name: str, start: str, end: str) -> dict:
    df = get_macro_series(series_name)
    date_col = next((c for c in df.columns if c.lower() in {"date", "observation_date"}), None)
    if not date_col:
        raise ValueError("Macro CSV requires a date/observation_date column")
    df[date_col] = pd.to_datetime(df[date_col])
    value_cols = [c for c in df.columns if c != date_col]
    if not value_cols:
        raise ValueError("Macro CSV has no value column")
    sub = df[(df[date_col] >= pd.Timestamp(start)) & (df[date_col] <= pd.Timestamp(end))]
    return {"series": series_name, "start": start, "end": end, "rows": sub.to_dict(orient="records")}
