"""Run the authorized metadata-only Stage 04 BigQuery preflight."""

from __future__ import annotations

import argparse
from pathlib import Path

from google.cloud import bigquery

from enares.stage04.cloud_metadata_preflight import preflight_bigquery_metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--dataset-id", required=True)
    parser.add_argument("--table-id", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    evidence = preflight_bigquery_metadata(
        client=bigquery.Client(project=args.project_id),
        project_id=args.project_id,
        dataset_id=args.dataset_id,
        table_id=args.table_id,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(evidence.as_json(), encoding="utf-8")
    return 0 if evidence.status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
