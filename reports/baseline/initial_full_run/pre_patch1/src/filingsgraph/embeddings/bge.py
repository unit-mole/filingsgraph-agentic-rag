from __future__ import annotations
import numpy as np
from filingsgraph.embeddings.base import EmbeddingProvider
from filingsgraph.core.config import get_settings

class BGEEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str | None = None, device: str | None = None, batch_size: int = 16):
        from sentence_transformers import SentenceTransformer
        s=get_settings(); self.model_name=model_name or s.embedding_model
        self.model=SentenceTransformer(self.model_name, device=device or s.device)
        self.batch_size=batch_size
    def encode(self,texts:list[str])->np.ndarray:
        return np.asarray(self.model.encode(texts,batch_size=self.batch_size,normalize_embeddings=True,show_progress_bar=len(texts)>100))

class HashEmbeddingProvider(EmbeddingProvider):
    """Deterministic lightweight fallback used only for tests/smoke fixtures, not portfolio metrics."""
    def __init__(self, dim:int=256): self.dim=dim
    def encode(self,texts:list[str])->np.ndarray:
        import hashlib, re
        out=np.zeros((len(texts),self.dim),dtype=np.float32)
        for i,text in enumerate(texts):
            for token in re.findall(r"[a-z0-9]+",text.lower()):
                h=int(hashlib.md5(token.encode()).hexdigest(),16)
                out[i,h%self.dim]+=1.0
            norm=np.linalg.norm(out[i])
            if norm: out[i]/=norm
        return out
