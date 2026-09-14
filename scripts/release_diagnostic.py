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
from app.views.stage04_dashboard import load_validated_estimates

MODULE_IDS = ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6")


def require_single_release(
    release_ids: set[str], expected_release: str | None = None
) -> str:
    """Fail closed unless every visible authorized row belongs to one release."""
    if len(release_ids) != 1:
        raise RuntimeError(
            "Authorized rows must contain exactly one release_id; "
            f"found {len(release_ids)}"
        )
    release_id = next(iter(release_ids))
    if expected_release is not None and release_id != expected_release:
        raise RuntimeError("The active local release does not match the expected release")
    return release_id


def diagnose_release(expected_release: str | None = None) -> dict[str, object]:
    """Validate every visible module and report only non-sensitive release metadata."""
    authorized, _ = local_repositories()
    module_counts: dict[str, int] = {}
    release_ids: set[str] = set()
    source_versions: set[str] = set()
    for module_id in MODULE_IDS:
        rows = load_validated_estimates(authorized, module_id)
        if not rows:
            raise RuntimeError(f"Authorized module {module_id} has no visible rows")
        module_counts[module_id] = len(rows)
        release_ids.update(row.release_id for row in rows)
        source_versions.update(row.source_version for row in rows)

    release_id = require_single_release(release_ids, expected_release)
    if len(source_versions) != 1:
        raise RuntimeError("Authorized rows do not share one source_version")

    return {
        "status": "ok",
        "release_id": release_id,
        "source_version": next(iter(source_versions)),
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
