from __future__ import annotations
from functools import lru_cache
from pathlib import Path
from filingsgraph.core.config import ROOT
from filingsgraph.database.session import Database
from filingsgraph.database.repositories import Repository

@lru_cache(maxsize=1)
def get_repo():
    db=Database(); db.initialize(); return Repository(db)
