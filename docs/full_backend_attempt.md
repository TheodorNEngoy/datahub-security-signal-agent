# Full Backend Attempt

Date: 2026-07-07

## Goal

Verify whether the prototype can be upgraded from DataHub Lite CLI/REST reads to the official DataHub backend plus `mcp-server-datahub` / `datahub-agent-context` tools on the local Mac.

## What Was Tried

1. Removed unused local Docker artifacts from a previous project to free disk.
2. Trimmed the Colima disk, recovering host free space to about 12 GiB.
3. Installed workspace-local Docker Compose v2.39.4 and verified its SHA256.
4. Increased Colima from 2 GiB to 6 GiB memory after DataHub quickstart rejected the lower Docker memory allocation.
5. Started:

```bash
DOCKER_HOST="unix://$HOME/.colima/default/docker.sock" \
PATH="$PWD/bin:$PWD/.venv/bin:$PATH" \
HOME="$PWD/home" \
datahub docker quickstart --version stable --pull-images --accept-version-default --arch arm64 --dump-logs-on-failure
```

## Result

The quickstart began pulling the v1.6.0 stack (`mysql`, `datahub-actions`, `opensearch`, `kafka-broker`, `datahub-gms-quickstart`, `frontend-quickstart`, and `system-update-quickstart`). Host free space fell from about 12 GiB to about 3.4 GiB before the full backend stack completed.

The run was aborted at the disk-risk stop line. Partial DataHub Docker images were removed and Docker was pruned back to an empty state.

## Source Evidence

- `mcp-server-datahub==0.6.0` installed successfully.
- `datahub-agent-context==1.6.0.10` installed successfully.
- The `mcp-server-datahub` entrypoint source shows it creates `DataHubClient.from_env(...)`.
- Agent Context builders require a `DataHubClient`.
- Therefore the official tools need a real DataHub backend URL/token or a completed local quickstart stack.

## Decision

Do not retry full quickstart on this disk state. Continue with the working DataHub Lite proof unless a no-cost backend/token appears or substantially more local disk is freed.
