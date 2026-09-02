from __future__ import annotations
import logging
from pathlib import Path
import time
import requests
from filingsgraph.core.config import get_settings, ROOT
from filingsgraph.sec.fair_access import RateLimiter
from filingsgraph.sec.cache import FileCache
from filingsgraph.security.source_validation import validate_source_url

log = logging.getLogger(__name__)

class SECClient:
    def __init__(self, cache_dir: str | Path = ROOT / "data" / "raw" / "http_cache", validate_identity: bool = True):
        self.settings = get_settings()
        if validate_identity:
            self.settings.validate_sec_identity()
        self.cache = FileCache(cache_dir)
        self.rate = RateLimiter(self.settings.sec_requests_per_second)
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": self.settings.sec_user_agent or "FilingsGraph local-test",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "application/json,text/html,application/xhtml+xml,*/*",
            }
        )

    def _fetch(self, url: str) -> bytes:
        validate_source_url(url)
        last_error: Exception | None = None
        for attempt in range(self.settings.sec_max_retries):
            try:
                self.rate.wait()
                r = self.session.get(url, timeout=self.settings.sec_timeout_seconds)
                if r.status_code in {429, 500, 502, 503, 504}:
                    raise requests.HTTPError(f"retryable SEC status={r.status_code}", response=r)
                r.raise_for_status()
                return r.content
            except requests.RequestException as exc:
                last_error = exc
                if attempt + 1 >= self.settings.sec_max_retries:
                    break
                time.sleep(min(16.0, 2.0**attempt))
        assert last_error is not None
        raise last_error

    def get_bytes(self, url: str, force: bool = False) -> bytes:
        validate_source_url(url)
        if not force:
            cached = self.cache.get(url)
            if cached is not None:
                return cached
        content = self._fetch(url)
        self.cache.put(url, content)
        return content

    def get_json(self, url: str, force: bool = False) -> dict:
        import json
        return json.loads(self.get_bytes(url, force=force).decode("utf-8"))

    def get_text(self, url: str, force: bool = False) -> str:
        return self.get_bytes(url, force=force).decode("utf-8", errors="replace")
