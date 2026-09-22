"""Single repository factory shared by every Stage 04 UI entrypoint."""

from __future__ import annotations

import os
from pathlib import Path

from enares.stage04.repository import (
    AuthorizedAggregateRepository,
    BigQueryRepository,
    DemoRepository,
    IndicatorRepository,
)

ROOT = Path(__file__).resolve().parents[1]


def local_repositories() -> tuple[IndicatorRepository, DemoRepository]:
    """Create repositories backed only by checked-in aggregate/synthetic fixtures."""
    data = ROOT / "app" / "data"
    registry = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"
    authorized = AuthorizedAggregateRepository(
        data / "v0_authorized_full_indicator_estimates.csv",
        data / "v0_authorized_full_indicator_estimates.manifest.json",
        registry,
    )
    demo = DemoRepository(data / "demo_indicator_estimates.csv")
    return authorized, demo


def configured_repositories() -> tuple[IndicatorRepository, DemoRepository | None]:
    """Select local or authenticated-shadow data without mixing transports."""
    mode = os.environ.get("STAGE04_DATA_MODE", "LOCAL_AUTHORIZED")
    if mode == "LOCAL_AUTHORIZED":
        return local_repositories()
    if mode != "AUTHENTICATED_SHADOW":
        raise ValueError("Unsupported Stage 04 data mode")

    required = {
        name: os.environ.get(name)
        for name in (
            "STAGE04_BQ_TABLE_FQN",
            "STAGE04_RELEASE_ID",
            "STAGE04_RUN_ID",
        )
    }
    if not all(required.values()):
        raise ValueError("Authenticated shadow configuration is incomplete")
    manifest = (
        ROOT / "app" / "data" / "v0_authorized_full_indicator_estimates.manifest.json"
    )
    registry = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"
    return (
        BigQueryRepository(
            table_fqn=required["STAGE04_BQ_TABLE_FQN"],
            release_id=required["STAGE04_RELEASE_ID"],
            run_id=required["STAGE04_RUN_ID"],
            manifest_path=manifest,
            approval_registry_path=registry,
        ),
        None,
    )
