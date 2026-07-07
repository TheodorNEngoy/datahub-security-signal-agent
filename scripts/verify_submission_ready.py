#!/usr/bin/env python3
"""Submission guardrails for the DataHub AgentHack prototype."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_demo() -> str:
    result = subprocess.run(
        [str(ROOT / "demo.sh")],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=True,
    )
    return result.stdout


def check_demo_output(output: str) -> list[str]:
    failures: list[str] = []
    required_fragments = [
        "warehouse.raw_customer_profiles",
        "PII fields: email, ssn_last4",
        "no registered owner",
        "stale: 96h since observed vs 24h SLO",
        "1 downstream dataset(s)",
        "Summary: 1 high-risk dataset(s)",
    ]
    for fragment in required_fragments:
        if fragment not in output:
            failures.append(f"demo output missing: {fragment}")
    return failures


def check_claim_boundaries() -> list[str]:
    failures: list[str] = []
    docs = [
        ROOT / "README.md",
        ROOT / "SUBMISSION_NOTES.md",
        ROOT / "docs" / "demo_video_script.md",
        ROOT / "docs" / "architecture_diagram.md",
    ]
    forbidden_claims = [
        "official MCP tools ran",
        "official DataHub MCP tools ran",
        "full DataHub backend works locally",
        "public demo MCP access works",
    ]
    for path in docs:
        text = path.read_text()
        for claim in forbidden_claims:
            if claim.lower() in text.lower():
                failures.append(f"{path.relative_to(ROOT)} contains overclaim: {claim}")
    return failures


def main() -> int:
    print("[1/2] Running demo.sh")
    output = run_demo()
    print(output)

    print("[2/2] Checking submission guardrails")
    failures = check_demo_output(output) + check_claim_boundaries()
    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: demo output and claim boundaries are submission-ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
