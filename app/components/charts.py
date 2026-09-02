from __future__ import annotations
import pandas as pd
import plotly.express as px

def financial_history_figure(rows: list[dict]):
    if not rows:
        return None
    df = pd.DataFrame(rows)
    return px.line(df, x="fiscal_year", y="value", markers=True, title=f"{rows[0].get('ticker')} — {rows[0].get('metric')}")
