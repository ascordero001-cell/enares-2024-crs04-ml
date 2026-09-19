"""Execute the protected Stage 04 promotion after an immutable decision gate."""

from __future__ import annotations

import argparse
from pathlib import Path

from google.cloud import bigquery

from enares.stage04.cloud_promotion import (
    PromotionResources,
    load_promotion_decision,
    promote_reconciled_release,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision", required=True, type=Path)
    parser.add_argument("--decision-reference", required=True)
    parser.add_argument("--release-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--source-hash", required=True)
    parser.add_argument("--reconciliation-run-url", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    decision = load_promotion_decision(
        args.decision,
        release_id=args.release_id,
        run_id=args.run_id,
        source_hash=args.source_hash,
        reconciliation_run_url=args.reconciliation_run_url,
    )
    project = "enares-2024-crs04"
    resources = PromotionResources(
        outputs_table=f"{project}.enares2024_crs04_stage04_shadow_outputs.indicator_estimates",
        release_registry=f"{project}.enares2024_crs04_stage04_shadow_ops.release_registry",
        validation_results=f"{project}.enares2024_crs04_stage04_shadow_ops.validation_results",
        current_release=f"{project}.enares2024_crs04_stage04_shadow_ops.current_release",
        promotion_events=f"{project}.enares2024_crs04_stage04_shadow_ops.promotion_events",
        published_view=f"{project}.enares2024_crs04_stage04_shadow_published.v_dashboard_current",
    )
    evidence = promote_reconciled_release(
        client=bigquery.Client(project=project),
        decision=decision,
        resources=resources,
        decision_reference=args.decision_reference,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(evidence.as_json(), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
