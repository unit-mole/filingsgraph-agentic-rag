def validate_fact_period(fact:dict,year:int)->bool: return fact.get('fiscal_year')==year
def validate_units(facts:list[dict])->bool: return len({f.get('unit') for f in facts})<=1
