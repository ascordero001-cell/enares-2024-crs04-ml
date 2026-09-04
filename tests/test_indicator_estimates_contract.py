from dataclasses import replace
from pathlib import Path

import pytest

from enares.stage04.repository import AuthorizedAggregateRepository, DemoRepository
from enares.stage04.validation import validate_estimates


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "app" / "data" / "demo_indicator_estimates.csv"
V0_FIXTURE = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.csv"
V0_MANIFEST = ROOT / "app" / "data" / "v0_authorized_indicator_estimates.manifest.json"
V0_REGISTRY = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"


def demo_rows():
    return DemoRepository(FIXTURE).list_estimates("3.2")


def v0_rows():
    return AuthorizedAggregateRepository(V0_FIXTURE, V0_MANIFEST, V0_REGISTRY).list_estimates("3.2")


def test_demo_catalog_satisfies_aggregate_contract():
    validate_estimates(demo_rows())


def test_duplicate_key_fails():
    rows = demo_rows()
    with pytest.raises(ValueError, match="Duplicate"):
        validate_estimates([*rows, rows[0]])


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("estimate", 101.0, "outside"),
        ("standard_error", -1.0, "non-negative"),
        ("cv", -0.1, "non-negative"),
        ("n_unweighted", -1, "non-negative"),
        ("ci95_lower", 21.0, "contain"),
    ],
)
def test_invalid_numeric_contract_fails(field, value, message):
    rows = demo_rows()
    rows[0] = replace(rows[0], **{field: value})
    with pytest.raises(ValueError, match=message):
        validate_estimates(rows)


def test_failed_validation_state_is_blocking():
    rows = demo_rows()
    rows[0] = replace(rows[0], validation_status="FAILED")
    with pytest.raises(ValueError, match="FAILED"):
        validate_estimates(rows)


def test_legacy_v0_row_allows_missing_weighted_population():
    rows = v0_rows()
    pilot = rows[0]
    assert pilot.weighted_population is None
    validate_estimates(rows)


def test_positive_weighted_population_is_valid():
    rows = demo_rows()
    assert any((row.weighted_population or 0) > 0 for row in rows)
    validate_estimates(rows)


def test_negative_weighted_population_fails():
    rows = demo_rows()
    rows[0] = replace(rows[0], weighted_population=-1.0)
    with pytest.raises(ValueError, match="weighted_population"):
        validate_estimates(rows)


def test_suppressed_row_cannot_retain_weighted_population():
    rows = demo_rows()
    suppressed_index = next(i for i, row in enumerate(rows) if row.suppress_flag)
    rows[suppressed_index] = replace(rows[suppressed_index], weighted_population=1.0)
    with pytest.raises(ValueError, match="protected"):
        validate_estimates(rows)


def test_publishable_only_catalog_is_valid():
    publishable = next(row for row in demo_rows() if row.quality_status == "PUBLISHABLE_CANDIDATE")
    validate_estimates([publishable])


def test_catalog_without_suppressed_rows_is_valid():
    rows = [row for row in demo_rows() if not row.suppress_flag]
    validate_estimates(rows)


def test_suppressed_quality_status_without_flag_fails():
    suppressed = next(row for row in demo_rows() if row.quality_status == "SUPPRESSED_EXERCISE")
    exposed = next(row for row in demo_rows() if row.quality_status == "PUBLISHABLE_CANDIDATE")
    inconsistent = replace(exposed, quality_status="SUPPRESSED_EXERCISE", suppress_flag=False)
    assert suppressed.suppress_flag is True
    with pytest.raises(ValueError, match="requires suppress_flag"):
        validate_estimates([inconsistent])


def test_suppress_flag_with_publishable_status_and_visible_statistics_fails():
    publishable = next(row for row in demo_rows() if row.quality_status == "PUBLISHABLE_CANDIDATE")
    inconsistent = replace(publishable, suppress_flag=True)
    with pytest.raises(ValueError, match="protected"):
        validate_estimates([inconsistent])


def test_correctly_nullified_suppressed_row_is_valid():
    suppressed = next(row for row in demo_rows() if row.quality_status == "SUPPRESSED_EXERCISE")
    validate_estimates([suppressed])
