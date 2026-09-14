"""Deep local diagnostic for manifest-bound Stage 04 releases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.streamlit_app import local_repositories
from app.views.stage04_dashboard import filter_estimates, load_validated_estimates

MODULE_IDS = ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6")


def diagnose_release(expected_release: str | None = None) -> dict[str, object]:
    """Validate every visible module and report only non-sensitive release metadata."""
    authorized, _ = local_repositories()
    module_counts: dict[str, int] = {}
    for module_id in MODULE_IDS:
        rows = load_validated_estimates(authorized, module_id)
        if not rows:
            raise RuntimeError(f"Authorized module {module_id} has no visible rows")
        module_counts[module_id] = len(rows)

    summary_rows = filter_estimates(authorized, "3.2", "Nacional", "Total")
    if len(summary_rows) != 1:
        raise RuntimeError("The authorized 3.2 release diagnostic row is not unique")
    summary = summary_rows[0]
    if expected_release is not None and summary.release_id != expected_release:
        raise RuntimeError(
            "The active local release does not match the expected release"
        )

    return {
        "status": "ok",
        "release_id": summary.release_id,
        "source_version": summary.source_version,
        "modules": module_counts,
        "cloud": "NOT_AUTHORIZED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-release")
    args = parser.parse_args()
    try:
        result = diagnose_release(args.expected_release)
    except (OSError, KeyError, TypeError, ValueError, RuntimeError) as exc:
        print(json.dumps({"status": "error", "message": str(exc)}))
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
