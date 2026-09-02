from __future__ import annotations
import time,psutil
from contextlib import contextmanager

@contextmanager
def measure(name:str,store:list[dict]):
    proc=psutil.Process(); start=time.perf_counter(); rss0=proc.memory_info().rss
    try: yield
    finally:
        item={"component":name,"latency_ms":(time.perf_counter()-start)*1000,"rss_delta_mb":(proc.memory_info().rss-rss0)/1e6}
        try:
            import torch
            item['cuda_allocated_mb']=torch.cuda.memory_allocated()/1e6 if torch.cuda.is_available() else 0.0
        except Exception: item['cuda_allocated_mb']=0.0
        store.append(item)
