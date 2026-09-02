from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np

class EmbeddingProvider(ABC):
    @abstractmethod
    def encode(self, texts: list[str]) -> np.ndarray: ...
