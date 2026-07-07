# Demo Video Script

Target length: 2 minutes.

## 0:00-0:15 Problem

"Data teams already have ownership, schema tags, freshness, and lineage in DataHub, but security review often still happens as a manual checklist. This prototype turns that metadata into a prioritized security-governance signal."

## 0:15-0:35 Setup

Show the repository files:

- `scripts/generate_cleanroom_metadata.py`
- `src/security_signal_agent.py`
- `metadata/cleanroom_security_catalog.json`

Say:

"This is a clean-room sample catalog. No proprietary data is used."

## 0:35-1:20 Run

Run:

```bash
./demo.sh
```

Point to the high-risk finding:

"The agent ranks `warehouse.raw_customer_profiles` as high risk because several independent DataHub signals combine: PII fields, no owner, stale freshness, and downstream consumers."

Then run one live DataHub Lite query:

```bash
HOME="$PWD/home" datahub lite get "urn:li:dataset:(urn:li:dataPlatform:postgres,warehouse.raw_customer_profiles,PROD)" --verbose
```

Say:

"This shows the finding is coming from DataHub Lite metadata, including schema tags, ownership state, freshness properties, and lineage."

## 1:20-1:45 Why DataHub Matters

"The key is not guessing from table names. The agent composes DataHub context: schema tags, ownership, custom freshness metadata, and lineage. That makes the finding explainable and reviewable."

## 1:45-2:00 Honest Boundary And Next Step

"This prototype runs on DataHub Lite for a no-spend local demo. The next upgrade is swapping the reads to the official DataHub MCP Server or Agent Context Kit tools against a full DataHub backend, then optionally writing accepted findings back into DataHub."
