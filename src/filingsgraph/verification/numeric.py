import math,re

def verify_calculations(calculations:list[dict],tolerance:float=1e-8)->dict:
    failures=[]
    for c in calculations:
        if c.get('expected') is not None and not math.isclose(float(c['output']),float(c['expected']),rel_tol=tolerance,abs_tol=tolerance): failures.append(c.get('calculation_id'))
    return {"ok":not failures,"failures":failures,"count":len(calculations)}

def numeric_statements(text:str)->list[str]: return re.findall(r'(?<!\w)[+-]?\d[\d,.]*(?:\.\d+)?%?',text)
