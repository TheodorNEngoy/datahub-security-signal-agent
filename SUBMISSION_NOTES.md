# Submission Notes

## One-sentence pitch

Security Signal Agent turns DataHub metadata into a prioritized governance finding: sensitive datasets that combine PII, missing ownership, stale freshness, and downstream lineage.

## What works now

- Clean-room metadata generation for four synthetic production datasets.
- DataHub Lite ingestion.
- Agent-style read-only composition over DataHub metadata.
- A deterministic high-risk finding:
  `warehouse.raw_customer_profiles` has PII fields, no registered owner, stale freshness, and downstream consumers.
- Optional DataHub Lite REST API demo via `/entities` and `/search`.

## Honest boundary

This prototype currently uses DataHub Lite because the public DataHub demo does not expose anonymous GMS/GraphQL API access. A full local DataHub Docker quickstart was attempted after freeing the approved Docker artifacts and compacting Colima, but the pull still exhausted the practical disk budget before the backend stack finished. The official `mcp-server-datahub` and `datahub-agent-context` packages are installed as dependencies, but their full tool path needs a full DataHub backend or valid token and was not run end-to-end in this local proof.

## Why it fits the hackathon

- Uses DataHub metadata as the source of truth for ownership, schema tags, freshness, and lineage.
- Demonstrates an agentic workflow: gather context, join risk signals, rank findings, and return a concise action list.
- Clean-room Apache-2.0 code path; no proprietary code or data included.

## Best next upgrade

Use a valid no-cost DataHub backend or free substantially more disk, then swap the Lite calls for official `mcp-server-datahub` or Agent Context Kit tool calls: `search`, `get_entities`, and `get_lineage`.
