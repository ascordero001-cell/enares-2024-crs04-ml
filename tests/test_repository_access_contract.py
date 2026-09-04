import hashlib
import json
from pathlib import Path

import pytest

from enares.stage04.repository import (
    AuthorizedAggregateRepository,
    BigQueryRepository,
    DemoRepository,
    IndicatorRepository,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "app" / "data" / "demo_indicator_estimates.csv"
V0_FIXTURE = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.csv"
V0_MANIFEST = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.manifest.json"
V0_REGISTRY = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"


def test_demo_repository_implements_expected_signature_and_preserves_quality():
    repository: IndicatorRepository = DemoRepository(FIXTURE)
    rows = repository.list_estimates("3.2")

    assert len(rows) == 3
    assert {row.quality_status for row in rows} == {
        "PUBLISHABLE_CANDIDATE",
        "REFERENCE_HIGH_CV",
        "SUPPRESSED_EXERCISE",
    }
    assert all(row.synthetic for row in rows)
    assert all(row.engine_version == "v0_csv" for row in rows)


def test_demo_repository_exposes_no_sensitive_attributes():
    row = DemoRepository(FIXTURE).list_estimates("3.2")[0]
    forbidden = {"respondent_id", "person_id", "nna_id", "name", "birth_date", "address"}
    assert forbidden.isdisjoint(vars(row))


def test_suppressed_demo_row_contains_no_protected_statistics():
    rows = DemoRepository(FIXTURE).list_estimates("3.2")
    suppressed = next(row for row in rows if row.quality_status == "SUPPRESSED_EXERCISE")
    assert suppressed.estimate is None
    assert suppressed.standard_error is None
    assert suppressed.ci95_lower is None
    assert suppressed.ci95_upper is None
    assert suppressed.cv is None
    assert suppressed.n_unweighted is None
    assert suppressed.weighted_population is None
    assert suppressed.suppress_flag is True


def test_bigquery_repository_is_explicitly_blocked():
    with pytest.raises(RuntimeError, match="BLOCKED_BY_CLOUD_GATE"):
        BigQueryRepository().list_estimates("3.2")


def test_authorized_aggregate_repository_reads_only_manifest_bound_v0():
    rows = AuthorizedAggregateRepository(V0_FIXTURE, V0_MANIFEST, V0_REGISTRY).list_estimates("3.2")
    assert len(rows) == 1
    assert rows[0].indicator_id == "VF_HOGAR"
    assert rows[0].synthetic is False
    assert rows[0].source_hash in V0_REGISTRY.read_text(encoding="utf-8")


def test_demo_repository_rejects_non_synthetic_row(tmp_path):
    content = FIXTURE.read_text(encoding="utf-8")
    modified = content.replace(",true\n", ",false\n", 1)
    fixture = tmp_path / "demo.csv"
    fixture.write_text(modified, encoding="utf-8", newline="\n")
    with pytest.raises(ValueError, match="only synthetic=true"):
        DemoRepository(fixture).list_estimates("3.2")


def test_authorized_repository_rejects_unapproved_source_hash(tmp_path):
    manifest = json.loads(V0_MANIFEST.read_text(encoding="utf-8"))
    manifest["source_hash"] = "b" * 64
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="approved V0 registry"):
        AuthorizedAggregateRepository(V0_FIXTURE, manifest_path, V0_REGISTRY).list_estimates("3.2")


def test_authorized_repository_rejects_sensitive_columns(tmp_path):
    lines = V0_FIXTURE.read_text(encoding="utf-8").splitlines()
    fixture = tmp_path / "v0.csv"
    fixture.write_text(
        f"{lines[0]},respondent_id\n{lines[1]},person-1\n",
        encoding="utf-8",
        newline="\n",
    )
    manifest = json.loads(V0_MANIFEST.read_text(encoding="utf-8"))
    manifest["file_name"] = fixture.name
    manifest["sha256"] = hashlib.sha256(fixture.read_bytes()).hexdigest()
    manifest_path = tmp_path / "v0.manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="Sensitive columns"):
        AuthorizedAggregateRepository(fixture, manifest_path, V0_REGISTRY).list_estimates("3.2")
