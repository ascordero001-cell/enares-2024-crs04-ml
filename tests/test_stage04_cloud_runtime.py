from __future__ import annotations

from pathlib import Path

from app.streamlit_app import configured_repositories
from enares.stage04.repository import BigQueryRepository

ROOT = Path(__file__).resolve().parents[1]


def test_authenticated_shadow_configuration_builds_bigquery_repository(
    monkeypatch,
) -> None:
    monkeypatch.setenv("STAGE04_DATA_MODE", "AUTHENTICATED_SHADOW")
    monkeypatch.setenv(
        "STAGE04_BQ_TABLE_FQN",
        "project-id.stage04_shadow_published.v_dashboard_current",
    )
    monkeypatch.setenv("STAGE04_RELEASE_ID", "approved-release")
    monkeypatch.setenv("STAGE04_RUN_ID", "approved-run")

    repository, demo = configured_repositories()

    assert isinstance(repository, BigQueryRepository)
    assert repository.table_fqn.endswith(".v_dashboard_current")
    assert repository.release_id == "approved-release"
    assert repository.run_id == "approved-run"
    assert demo is None


def test_cloud_image_contains_only_manifest_bound_aggregate_metadata() -> None:
    dockerfile = (ROOT / "Dockerfile.cloud").read_text(encoding="utf-8")
    requirements = (ROOT / "requirements-cloud-runtime.txt").read_text(
        encoding="utf-8"
    )

    assert "google-cloud-bigquery==3.45.0" in requirements
    assert "COPY --chown=app:app app ./app" not in dockerfile
    assert "v0_authorized_full_indicator_estimates.csv" not in dockerfile
    assert "demo_indicator_estimates.csv" not in dockerfile
    assert "v0_authorized_full_indicator_estimates.manifest.json" in dockerfile
    assert "v0_drive_hash_manifest.md" in dockerfile


def test_published_view_matches_bigquery_repository_projection() -> None:
    view = (
        ROOT / "dataform" / "definitions" / "published" / "v_dashboard_current.sqlx"
    ).read_text(encoding="utf-8")
    settings = (ROOT / "dataform" / "workflow_settings.yaml").read_text(
        encoding="utf-8"
    )

    assert "schema: dataform.projectConfig.vars.publishedDataset" in view
    assert "publishedDataset:" in settings
    for field in (
        "source_hash",
        "git_commit_sha",
        "container_image_digest",
        "dataform_release",
        "engine_version",
        "scale",
        "universe",
        "denominator",
        "quality_status",
    ):
        assert f"estimates.{field}" in view


def test_cloud_image_workflow_exports_only_after_main_merge() -> None:
    workflow = (ROOT / ".github" / "workflows" / "cloud-image.yml").read_text(
        encoding="utf-8"
    )

    assert "Dockerfile.cloud" in workflow
    assert 'github.event_name == \'push\'' in workflow
    assert "refs/heads/main" in workflow
    assert "retention-days: 1" in workflow
    assert "test ! -e /app/app/data/v0_authorized_full_indicator_estimates.csv" in workflow
