# Security

SEC filing content is treated as **untrusted data**, never as system instructions.

Controls implemented in the core path:

- source-domain allowlist (`sec.gov`, `www.sec.gov`, `data.sec.gov`);
- prompt-injection pattern detection and data/instruction separation;
- read-only research tools;
- typed Pydantic request/response models;
- query/tool/context limits;
- no agent-generated arbitrary URLs;
- optional external/commercial model providers disabled by default;
- secrets loaded from environment variables and `.env` ignored by Git;
- citation, entity, period, unit, and numeric verification before final reports.

Use the security test suite before deployment: `pytest tests/security -q`.
