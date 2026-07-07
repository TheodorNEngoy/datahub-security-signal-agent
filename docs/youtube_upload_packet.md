# YouTube/Vimeo Upload Packet

Use this for the required public demo video upload before pasting the final URL into Devpost.

## File

`/Users/theodornengoy/work/datahub-agenthack-2026-07-07/dist/datahub-security-signal-agent-demo.mp4`

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

## After Upload

Replace the `Demo video: TODO` line in `docs/devpost_copy.md` with the final public YouTube or Vimeo URL, then rerun:

```bash
PATH="$PWD/.venv/bin:$PATH" HOME="$PWD/home" python scripts/verify_submission_ready.py
```
