from urllib.parse import urlparse
from filingsgraph.core.constants import SEC_ALLOWED_HOSTS

def validate_source_url(url: str, allow_fred: bool = False) -> str:
    parsed = urlparse(url)
    allowed = set(SEC_ALLOWED_HOSTS)
    if allow_fred:
        allowed.add("fred.stlouisfed.org")
    if parsed.scheme != "https" or (parsed.hostname or "").lower() not in allowed:
        raise ValueError(f"Source URL is not allowlisted: {url}")
    return url
