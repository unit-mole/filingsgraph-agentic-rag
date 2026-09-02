UNIT_ALIASES = {"USD": "USD", "shares": "shares", "USD/shares": "USD/share", "pure": "ratio"}

def normalize_unit(unit: str) -> str:
    return UNIT_ALIASES.get(unit, unit)

def normalize_value(value: float, scale: float = 1.0) -> float:
    return float(value) * float(scale)
