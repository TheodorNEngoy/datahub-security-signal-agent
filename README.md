# DataHub Security Signal Agent

DataHub Security Signal Agent is a read-only prototype that turns DataHub metadata into a prioritized, explainable security-governance review queue.

The demo builds a clean-room DataHub Lite catalog with four synthetic warehouse datasets, then ranks each dataset by combining DataHub context:

- schema field tags
- ownership
- freshness metadata
- upstream and downstream lineage

The deterministic demo finding is `warehouse.raw_customer_profiles`: it is ranked HIGH because it combines PII-tagged fields, no registered owner, stale freshness metadata, and downstream lineage.

## Built With

- Python
- DataHub SDK / `acryl-datahub`
- DataHub Lite
- `mcp-server-datahub` and `datahub-agent-context` as the documented full-backend upgrade path

## Quickstart

From a fresh clone:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./demo.sh
```

Expected summary:

```text
Summary: 1 high-risk dataset(s) combine PII, missing ownership, and stale freshness.
```

## Verify Before Publishing

```bash
. .venv/bin/activate
python scripts/verify_submission_ready.py
```

The verifier reruns the demo and checks public-facing docs for claim-boundary mistakes.

## Optional REST Demo

In one terminal:

```bash
. .venv/bin/activate
HOME="$PWD/home" datahub lite serve --port 8979
```

In another terminal:

```bash
curl http://127.0.0.1:8979/ping
curl http://127.0.0.1:8979/entities
curl 'http://127.0.0.1:8979/search?query=raw'
```

Stop the server with `Ctrl-C`.

## Repository Map

- [scripts/generate_cleanroom_metadata.py](scripts/generate_cleanroom_metadata.py) builds the synthetic DataHub Metadata Change Proposal records.
- [src/security_signal_agent.py](src/security_signal_agent.py) ranks governance/security findings from DataHub Lite.
- [demo.sh](demo.sh) runs the proof end-to-end.
- [scripts/verify_submission_ready.py](scripts/verify_submission_ready.py) checks demo output and public claim boundaries.
- [docs/architecture_diagram.md](docs/architecture_diagram.md) explains the architecture and production upgrade path.
- [docs/demo_video_script.md](docs/demo_video_script.md) gives a sub-3-minute demo script.
- [docs/devpost_copy.md](docs/devpost_copy.md) gives claim-safe Devpost copy.
- [docs/full_backend_attempt.md](docs/full_backend_attempt.md) records the full-backend attempt and why the local Docker path was stopped.

## Scope And Honest Boundary

The current runnable demo uses DataHub Lite so the full metadata round trip - SDK-generated metadata, ingestion, then agent reads - is reproducible in one command with no cloud account, credentials, or Docker stack.

The official `mcp-server-datahub` and `datahub-agent-context` packages are installed as project dependencies and documented as the next integration path. Their tools require a full DataHub backend or valid token and were not run end-to-end in this local proof.

## Next Step

Point the agent at a full DataHub backend and replace the Lite reads with official `mcp-server-datahub` or Agent Context Kit calls such as `search`, `get_entities`, and `get_lineage`. After that, add an opt-in write-back path that creates a DataHub document, tag, or ownership task for accepted findings.
