# YouTube/Vimeo Upload Packet

This records the public demo video upload used for the Devpost submission.

## File

`dist/datahub-security-signal-agent-demo.mp4` in this local working tree.

## Title

DataHub Security Signal Agent - AgentHack Demo

## Description

Demo for Build with DataHub: The Agent Hackathon.

DataHub Security Signal Agent is a read-only prototype that turns DataHub metadata into a prioritized security-governance review queue.

GitHub: https://github.com/TheodorNEngoy/datahub-security-signal-agent

The demo uses DataHub Lite for a reproducible no-cloud-account metadata round trip: SDK-generated Metadata Change Proposal records, local ingestion, and a read-only agent that ranks datasets by PII tags, ownership, freshness metadata, and lineage.

Current boundary: the official `mcp-server-datahub` and `datahub-agent-context` packages are documented as the next full-backend integration path; their tools were not run end-to-end in this local proof.

## Settings

- Visibility: Public
- Audience: Not made for kids
- Paid promotion: No
- Tags: DataHub, AgentHack, data governance, metadata, security, AI agents

## Published URL

https://www.youtube.com/watch?v=KY4GNaZrHz0

## Verification

```bash
PATH="$PWD/.venv/bin:$PATH" HOME="$PWD/home" python scripts/verify_submission_ready.py
```
