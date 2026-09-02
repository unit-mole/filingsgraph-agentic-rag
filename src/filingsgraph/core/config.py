from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
import os
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[3]
load_dotenv(ROOT / ".env", override=False)

class Settings(BaseModel):
    model_provider: str = Field(default_factory=lambda: os.getenv("MODEL_PROVIDER", "local"))
    local_llm_backend: str = Field(default_factory=lambda: os.getenv("LOCAL_LLM_BACKEND", "transformers"))
    local_llm_model: str = Field(default_factory=lambda: os.getenv("LOCAL_LLM_MODEL", "Qwen/Qwen3-14B"))
    local_llm_base_url: str = Field(default_factory=lambda: os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:8000/v1"))
    fast_llm_model: str = Field(default_factory=lambda: os.getenv("FAST_LLM_MODEL", "Qwen/Qwen3-8B"))
    embedding_model: str = Field(default_factory=lambda: os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3"))
    reranker_model: str = Field(default_factory=lambda: os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3"))
    device: str = Field(default_factory=lambda: os.getenv("DEVICE", "cuda"))
    sec_user_agent: str = Field(default_factory=lambda: os.getenv("SEC_USER_AGENT", ""))
    sec_contact_email: str = Field(default_factory=lambda: os.getenv("SEC_CONTACT_EMAIL", ""))
    sec_requests_per_second: float = Field(default_factory=lambda: float(os.getenv("SEC_REQUESTS_PER_SECOND", "5")))
    sec_timeout_seconds: float = Field(default_factory=lambda: float(os.getenv("SEC_TIMEOUT_SECONDS", "45")))
    sec_max_retries: int = Field(default_factory=lambda: int(os.getenv("SEC_MAX_RETRIES", "5")))
    qdrant_mode: str = Field(default_factory=lambda: os.getenv("QDRANT_MODE", "local"))
    qdrant_url: str = Field(default_factory=lambda: os.getenv("QDRANT_URL", ""))
    qdrant_path: str = Field(default_factory=lambda: os.getenv("QDRANT_PATH", "data/index/qdrant"))
    database_mode: str = Field(default_factory=lambda: os.getenv("DATABASE_MODE", "duckdb"))
    database_url: str = Field(default_factory=lambda: os.getenv("DATABASE_URL", "data/processed/filingsgraph.duckdb"))
    graph_mode: str = Field(default_factory=lambda: os.getenv("GRAPH_MODE", "networkx"))
    graph_path: str = Field(default_factory=lambda: os.getenv("GRAPH_PATH", "data/graph/filingsgraph.json"))
    phoenix_endpoint: str = Field(default_factory=lambda: os.getenv("PHOENIX_ENDPOINT", ""))
    enable_fred: bool = Field(default_factory=lambda: os.getenv("ENABLE_FRED", "false").lower() == "true")
    enable_commercial_models: bool = Field(default_factory=lambda: os.getenv("ENABLE_COMMERCIAL_MODELS", "false").lower() == "true")

    def validate_sec_identity(self) -> None:
        ua = self.sec_user_agent.strip()
        email = self.sec_contact_email.strip()
        if not ua or "example.com" in ua.lower() or not email or "example.com" in email.lower():
            raise ValueError("Configure SEC_USER_AGENT and SEC_CONTACT_EMAIL in .env before SEC downloads.")
        if self.sec_requests_per_second <= 0 or self.sec_requests_per_second > 10:
            raise ValueError("SEC_REQUESTS_PER_SECOND must be >0 and <=10; project default is 5.")


def load_yaml(name: str) -> dict[str, Any]:
    path = ROOT / "configs" / name
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
