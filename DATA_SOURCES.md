# Data Sources

FilingsGraph uses authoritative public SEC EDGAR resources as its mandatory data source.

## SEC resources

- `https://www.sec.gov/files/company_tickers.json` for runtime ticker/CIK resolution.
- `https://data.sec.gov/submissions/CIK##########.json` for filing metadata.
- `https://www.sec.gov/Archives/edgar/data/...` for primary filing documents.
- `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json` for structured XBRL facts.

The client requires a descriptive User-Agent/contact setting, applies local caching, exponential backoff,
and a configurable throttle whose default is 5 requests/second.

Optional FRED integration is disabled by default and is not required for any core capability.
