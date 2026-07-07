# Devpost Copy Draft

Use this only after replacing placeholders with the final public GitHub and video URLs.

## Project Name

DataHub Security Signal Agent

## Tagline

Turns DataHub metadata into a prioritized security-governance finding.

## Inspiration

Security review often happens outside the metadata catalog, even though DataHub already knows the signals reviewers need: schema tags, ownership, freshness, and lineage. This prototype shows how an agent can compose those signals into a focused review queue.

## What It Does

The prototype builds a clean-room DataHub Lite catalog with four synthetic warehouse datasets, then runs a read-only agent that ranks datasets by governance/security risk.

The demo finding is deterministic: `warehouse.raw_customer_profiles` is ranked HIGH because it combines PII-tagged fields, no registered owner, stale freshness metadata, and downstream lineage.

## How We Built It

- DataHub SDK classes generate Metadata Change Proposal records for synthetic datasets.
- DataHub Lite imports the metadata locally with no cloud account, credentials, or spend.
- A Python agent reads DataHub Lite metadata and composes schema tags, ownership, freshness custom properties, and lineage into ranked findings.
- The project is clean-room Apache-2.0 code.

## Use Of DataHub

DataHub is the source of truth for the agent's context: dataset entities, schema field tags, ownership, dataset properties, and lineage. The current runnable demo uses DataHub Lite because anonymous public-demo GMS/GraphQL access was not available and the local machine could not complete full Docker quickstart within its disk budget.

The official `mcp-server-datahub` and `datahub-agent-context` packages are installed in the project environment and documented as the next integration path once a full DataHub backend or valid token is available.

## Challenges

The main challenge was keeping the submission honest and no-spend. Public demo UI access worked, but API/GMS access required authentication. Full local DataHub quickstart was attempted after Docker cleanup, but image pulls drove the Mac near full disk before the stack completed. The project therefore ships a reliable DataHub Lite demo and documents the full-backend upgrade path instead of claiming an unverified MCP integration.

## Accomplishments

- Built a runnable DataHub metadata proof from a clean-room synthetic catalog.
- Produced one explainable high-risk finding from multiple independent DataHub signals.
- Added a submission guardrail script so demo output and claim boundaries stay consistent.
- Kept the project Apache-2.0 and reproducible with a single `./demo.sh`.

## What Is Next

Use a valid no-cost DataHub backend or free enough local disk for full quickstart, then replace Lite reads with official `mcp-server-datahub` / Agent Context Kit calls such as `search`, `get_entities`, and `get_lineage`. After that, add an opt-in write-back path that creates a DataHub document, tag, or ownership task for accepted findings.

## Links

- GitHub: TODO
- Demo video: TODO
