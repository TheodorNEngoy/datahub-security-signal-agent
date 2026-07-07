# Devpost Copy Draft

Use this only after replacing placeholders with the final public GitHub and video URLs.

## Project Name

DataHub Security Signal Agent

## Tagline

An agent that reads DataHub metadata - PII tags, ownership, freshness, lineage - and ranks datasets into a prioritized, explainable security review queue.

## Inspiration

Security review often happens outside the metadata catalog, even though DataHub already knows the signals reviewers need: schema tags, ownership, freshness, and lineage. This prototype shows how an agent can compose those signals into a focused review queue.

## What It Does

A read-only agent ranks every dataset in a DataHub catalog by security-governance risk and explains each ranking from the exact metadata signals that triggered it. The demo runs against a clean-room DataHub Lite catalog of four synthetic warehouse datasets - one command, no cloud account.

The demo finding is deterministic: `warehouse.raw_customer_profiles` is ranked HIGH because it combines PII-tagged fields, no registered owner, stale freshness metadata, and downstream lineage.

## How We Built It

- DataHub SDK classes generate Metadata Change Proposal records for synthetic datasets.
- DataHub Lite imports the metadata locally with no cloud account, credentials, or spend.
- A Python agent reads DataHub Lite metadata and composes schema tags, ownership, freshness custom properties, and lineage into ranked findings.
- The project is clean-room Apache-2.0 code.

## Use Of DataHub

DataHub is the source of truth for the agent's context: dataset entities, schema field tags, ownership, dataset properties, and lineage. The runnable demo uses DataHub Lite so the full metadata round trip - SDK-generated metadata, ingestion, then agent reads - is reproducible in one command with no cloud account, credentials, or Docker stack.

The official `mcp-server-datahub` and `datahub-agent-context` packages are installed in the project environment and documented as the next integration path once a full DataHub backend or valid token is available.

## Built With

python, datahub, datahub-lite, acryl-datahub-sdk

## Challenges

The main challenge was keeping the submission honest and no-spend. Within a strict no-spend, no-credentials constraint, we could not verify the official MCP server end-to-end: the hosted demo requires authenticated API access, and a full local quickstart was not feasible in the build environment. The project therefore ships a reliable DataHub Lite demo and documents the full-backend upgrade path instead of claiming an unverified MCP integration.

## Accomplishments

- Built a runnable DataHub metadata proof from a clean-room synthetic catalog.
- Produced one explainable high-risk finding from multiple independent DataHub signals.
- Added a submission guardrail script so demo output and claim boundaries stay consistent.
- Kept the project Apache-2.0 and reproducible with a single `./demo.sh`.

## What Is Next

Point the agent at a full DataHub backend and replace the Lite reads with official `mcp-server-datahub` / Agent Context Kit calls such as `search`, `get_entities`, and `get_lineage`. After that, add an opt-in write-back path that creates a DataHub document, tag, or ownership task for accepted findings.

## Links

- GitHub: https://github.com/TheodorNEngoy/datahub-security-signal-agent
- Demo video: TODO
