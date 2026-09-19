"""Prepare safe evidence for one manually authorized Stage 04 shadow run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from enares.stage04.shadow_pipeline import (
    PipelineInputContract,
    prepare_authorized_aggregate,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--aggregate", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--approval-registry", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads(args.contract.read_text(encoding="utf-8"))
    contract = PipelineInputContract(**payload)
    evidence = prepare_authorized_aggregate(
        contract,
        aggregate_path=args.aggregate,
        manifest_path=args.manifest,
        approval_registry_path=args.approval_registry,
    )
    args.output_directory.mkdir(parents=True, exist_ok=True)
    (args.output_directory / "preparation-evidence.json").write_text(
        evidence.as_json(), encoding="utf-8", newline="\n"
    )
    (args.output_directory / "preparation-evidence.md").write_text(
        evidence.as_markdown(), encoding="utf-8", newline="\n"
    )
    print("PASS_PREPARED_NO_CLOUD_MUTATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
