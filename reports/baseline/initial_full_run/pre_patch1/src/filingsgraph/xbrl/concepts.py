CANONICAL_CONCEPTS = {
    "Revenues": "revenue",
    "RevenueFromContractWithCustomerExcludingAssessedTax": "revenue",
    "SalesRevenueNet": "revenue",
    "NetIncomeLoss": "net_income",
    "OperatingIncomeLoss": "operating_income",
    "GrossProfit": "gross_profit",
    "Assets": "assets",
    "Liabilities": "liabilities",
    "StockholdersEquity": "equity",
    "PaymentsToAcquirePropertyPlantAndEquipment": "capex",
    "CashAndCashEquivalentsAtCarryingValue": "cash",
}

def normalize_concept(raw: str) -> tuple[str, str, float]:
    if raw in CANONICAL_CONCEPTS:
        return CANONICAL_CONCEPTS[raw], "deterministic_map", 1.0
    return raw, "raw_concept", 0.5
