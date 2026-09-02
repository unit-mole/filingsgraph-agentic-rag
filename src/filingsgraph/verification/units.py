def verify_units(calculations:list[dict])->dict:
    bad=[c.get('calculation_id') for c in calculations if c.get('unit_mismatch')]
    return {"ok":not bad,"bad":bad}
