# DataHub AgentHack Spike

Bounded no-spend feasibility spike for Build with DataHub: The Agent Hackathon.

## Verdict

`HUNT_NOW_BOUNDED`, with one correction:

- The public demo UI is reachable, but anonymous/default DataHub API, GMS, and GraphQL access did not work.
- Full local DataHub quickstart is not feasible on this Mac without freeing substantially more disk. After removing the approved Splunk container/image/anonymous volumes and compacting Colima, the machine had about 12 GiB free, but the DataHub pull still drove host free space down to about 3.4 GiB before the full backend stack finished. The attempt was aborted and the partial Docker images were pruned.
- DataHub Lite does work locally and can support a narrow screen-recordable security-governance demo.

## Working Proof

This spike builds a clean-room DataHub Lite catalog with four synthetic datasets and runs a small agent that composes:

- dataset enumeration
- schema field PII tags
- ownership
- freshness metadata
- upstream/downstream lineage

The working signal is:

`warehouse.raw_customer_profiles` is HIGH risk because it has PII fields, no registered owner, stale freshness, and a downstream consumer.

## Included Assets

- [scripts/generate_cleanroom_metadata.py](scripts/generate_cleanroom_metadata.py) builds the synthetic DataHub metadata.
- [src/security_signal_agent.py](src/security_signal_agent.py) ranks governance/security findings.
- [demo.sh](demo.sh) runs the proof end-to-end.
- [docs/architecture_diagram.md](docs/architecture_diagram.md) explains the current architecture and production upgrade path.
- [docs/demo_video_script.md](docs/demo_video_script.md) gives a sub-3-minute demo script.
- [docs/devpost_copy.md](docs/devpost_copy.md) gives claim-safe Devpost copy.
- [SUBMISSION_NOTES.md](SUBMISSION_NOTES.md) captures safe Devpost wording and honest boundaries.

## Run

```bash
cd /Users/theodornengoy/work/datahub-agenthack-2026-07-07
PATH="$PWD/.venv/bin:$PATH" HOME="$PWD/home" python scripts/generate_cleanroom_metadata.py
PATH="$PWD/.venv/bin:$PATH" HOME="$PWD/home" datahub lite import metadata/cleanroom_security_catalog.json
PATH="$PWD/.venv/bin:$PATH" HOME="$PWD/home" python src/security_signal_agent.py
```

Expected summary:

```text
Summary: 1 high-risk dataset(s) combine PII, missing ownership, and stale freshness.
```

## Verify Before Publishing

```bash
PATH="$PWD/.venv/bin:$PATH" HOME="$PWD/home" python scripts/verify_submission_ready.py
```

This reruns the demo and checks that public-facing docs do not claim the official MCP server ran locally.

## Optional REST Demo

```bash
PATH="$PWD/.venv/bin:$PATH" HOME="$PWD/home" datahub lite serve --port 8979
curl http://127.0.0.1:8979/ping
curl http://127.0.0.1:8979/entities
curl 'http://127.0.0.1:8979/search?query=raw'
```

Stop the server with `Ctrl-C`.

## Next Decision

Proceed only if one of these is true:

- enough extra disk is freed for full DataHub quickstart and `mcp-server-datahub` can call real MCP tools, or
- the final submission is intentionally framed around DataHub Lite plus Agent Context/analytics-agent style composition, not the official MCP server.

Do not spend time guessing public-demo credentials.

## Installed Official Agent Packages

The local venv includes:

- `mcp-server-datahub==0.6.0`
- `datahub-agent-context==1.6.0.10`

The current runnable proof uses DataHub Lite CLI/REST because the official Agent Context Kit and MCP tools expect a full DataHub backend/GraphQL client. The installed MCP server bootstraps `DataHubClient.from_env(...)`; the Agent Context builders likewise require a `DataHubClient`. That is the next integration step, not a claim already made by this spike.
