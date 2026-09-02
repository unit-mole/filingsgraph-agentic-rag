import math
def exact_numeric_match(pred:float|None,gold:float|None,tol:float=1e-8)->float:
    if pred is None or gold is None:return 0.0
    return float(math.isclose(float(pred),float(gold),rel_tol=tol,abs_tol=tol))
