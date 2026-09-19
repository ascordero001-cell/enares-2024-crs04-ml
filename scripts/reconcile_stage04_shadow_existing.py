"""Reconcile an existing Stage 04 cloud snapshot and emit redacted evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from enares.stage04.cloud_reconciliation import reconcile_existing_snapshot
from enares.stage04.shadow_pipeline import PipelineInputContract


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--aggregate", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--approval-registry", required=True, type=Path)
    parser.add_argument("--table-fqn", required=True)
    parser.add_argument("--expected-total-bytes", required=True, type=int)
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()

    contract = PipelineInputContract(**json.loads(args.contract.read_text(encoding="utf-8")))
    from google.cloud import bigquery

    evidence = reconcile_existing_snapshot(
        contract,
        aggregate_path=args.aggregate,
        manifest_path=args.manifest,
        approval_registry_path=args.approval_registry,
        table_fqn=args.table_fqn,
        expected_total_bytes_processed=args.expected_total_bytes,
        client=bigquery.Client(),
    )
    args.output_directory.mkdir(parents=True, exist_ok=True)
    (args.output_directory / "reconciliation.json").write_text(
        evidence.as_json(), encoding="utf-8"
    )
    (args.output_directory / "reconciliation.md").write_text(
        evidence.as_markdown(), encoding="utf-8"
    )
    return 0 if evidence.status == "PASS_RECONCILE_EXISTING" else 2


if __name__ == "__main__":
    raise SystemExit(main())
