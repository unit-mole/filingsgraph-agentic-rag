import numpy as np
def summarize_latency(values:list[float])->dict:
    if not values:return {"p50_ms":None,"p95_ms":None,"mean_ms":None}
    return {"p50_ms":float(np.percentile(values,50)),"p95_ms":float(np.percentile(values,95)),"mean_ms":float(np.mean(values))}
