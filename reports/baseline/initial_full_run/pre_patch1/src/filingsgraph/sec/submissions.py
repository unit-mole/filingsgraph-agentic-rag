from filingsgraph.sec.client import SECClient

def submissions_url(cik: str) -> str:
    return f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json"

def get_submissions(cik: str, client: SECClient | None = None, force: bool = False) -> dict:
    client = client or SECClient()
    return client.get_json(submissions_url(cik), force=force)
