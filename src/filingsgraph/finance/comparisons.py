from filingsgraph.finance.calculations import growth_rate

def compare_period_values(old:dict,new:dict)->dict:
    if old.get('unit')!=new.get('unit'): raise ValueError('Cannot compare different units')
    change=float(new['value'])-float(old['value'])
    pct=growth_rate(float(old['value']),float(new['value'])) if float(old['value'])!=0 else None
    return {"from_year":old.get('fiscal_year'),"to_year":new.get('fiscal_year'),"old_value":old['value'],"new_value":new['value'],"absolute_change":change,"percent_change":pct,"unit":old.get('unit')}
