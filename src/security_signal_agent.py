#!/usr/bin/env python3
"""Clean-room DataHub governance signal agent for the AgentHack spike.

The agent deliberately composes read-only DataHub Lite calls:
1. list dataset URNs
2. get dataset aspects
3. join schema tags, ownership, freshness, and upstream lineage

It produces one narrow security/governance signal rather than trying to wrap
the whole DataHub platform.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VENV_BIN = ROOT / ".venv" / "bin"
SPIKE_HOME = ROOT / "home"


@dataclass
class DatasetSignal:
    urn: str
    name: str
    owners: list[str]
    pii_fields: list[str]
    last_observed_hours_ago: int
    freshness_slo_hours: int
    upstreams: list[str]
    downstream_count: int

    @property
    def stale(self) -> bool:
        return self.last_observed_hours_ago > self.freshness_slo_hours

    @property
    def severity(self) -> str:
        if self.pii_fields and not self.owners and self.stale:
            return "HIGH"
        if self.pii_fields and (not self.owners or self.stale or self.downstream_count):
            return "MEDIUM"
        return "LOW"

    @property
    def reason(self) -> str:
        parts = []
        if self.pii_fields:
            parts.append(f"PII fields: {', '.join(self.pii_fields)}")
        if not self.owners:
            parts.append("no registered owner")
        if self.stale:
            parts.append(
                f"stale: {self.last_observed_hours_ago}h since observed vs {self.freshness_slo_hours}h SLO"
            )
        if self.downstream_count:
            parts.append(f"{self.downstream_count} downstream dataset(s)")
        return "; ".join(parts) or "no governance risk signal"


def run_datahub(*args: str) -> str:
    env = os.environ.copy()
    env["HOME"] = str(SPIKE_HOME)
    env["PATH"] = f"{VENV_BIN}:{env['PATH']}"
    result = subprocess.run(
        ["datahub", "lite", *args],
        cwd=ROOT,
        env=env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def list_urns() -> list[str]:
    return [line.strip() for line in run_datahub("list-urns").splitlines() if line.startswith("urn:")]


def get_dataset(urn: str) -> dict[str, Any]:
    return json.loads(run_datahub("get", urn, "--verbose"))


def pii_fields(dataset: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for field in dataset.get("schemaMetadata", {}).get("fields", []):
        tags = field.get("globalTags", {}).get("tags", [])
        if any(tag.get("tag") == "urn:li:tag:PII" for tag in tags):
            out.append(field["fieldPath"])
    return out


def owners(dataset: dict[str, Any]) -> list[str]:
    return [
        owner["owner"].split(":")[-1]
        for owner in dataset.get("ownership", {}).get("owners", [])
        if owner.get("owner")
    ]


def freshness(dataset: dict[str, Any]) -> tuple[int, int]:
    props = dataset.get("datasetProperties", {}).get("customProperties", {})
    return int(props.get("last_observed_hours_ago", "0")), int(
        props.get("freshness_slo_hours", "24")
    )


def upstreams(dataset: dict[str, Any]) -> list[str]:
    return [
        upstream["dataset"]
        for upstream in dataset.get("upstreamLineage", {}).get("upstreams", [])
        if upstream.get("dataset")
    ]


def dataset_name(dataset: dict[str, Any], urn: str) -> str:
    return dataset.get("datasetProperties", {}).get("name") or urn


def build_signals() -> list[DatasetSignal]:
    urns = list_urns()
    datasets = {urn: get_dataset(urn) for urn in urns}
    reverse_lineage: dict[str, int] = {urn: 0 for urn in urns}
    for dataset in datasets.values():
        for upstream in upstreams(dataset):
            reverse_lineage[upstream] = reverse_lineage.get(upstream, 0) + 1

    signals: list[DatasetSignal] = []
    for urn, dataset in datasets.items():
        last_seen, slo = freshness(dataset)
        signals.append(
            DatasetSignal(
                urn=urn,
                name=dataset_name(dataset, urn),
                owners=owners(dataset),
                pii_fields=pii_fields(dataset),
                last_observed_hours_ago=last_seen,
                freshness_slo_hours=slo,
                upstreams=upstreams(dataset),
                downstream_count=reverse_lineage.get(urn, 0),
            )
        )

    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    return sorted(signals, key=lambda item: (severity_rank[item.severity], item.name))


def main() -> int:
    signals = build_signals()
    print("# DataHub Security Governance Signal")
    print()
    print("| Severity | Dataset | Owners | Reason |")
    print("|---|---|---|---|")
    for signal in signals:
        owners_text = ", ".join(signal.owners) if signal.owners else "MISSING"
        print(f"| {signal.severity} | `{signal.name}` | {owners_text} | {signal.reason} |")

    high = [signal for signal in signals if signal.severity == "HIGH"]
    print()
    print(
        f"Summary: {len(high)} high-risk dataset(s) combine PII, missing ownership, and stale freshness."
    )
    return 0 if high else 2


if __name__ == "__main__":
    sys.exit(main())
