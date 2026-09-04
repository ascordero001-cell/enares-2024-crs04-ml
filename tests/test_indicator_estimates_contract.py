from dataclasses import replace
from pathlib import Path

import pytest

from enares.stage04.repository import DemoRepository
from enares.stage04.validation import validate_estimates


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "app" / "data" / "demo_indicator_estimates.csv"


def demo_rows():
    return DemoRepository(FIXTURE).list_estimates("3.2")


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
    rows = demo_rows()
    pilot = next(row for row in rows if row.indicator_id == "VF_HOGAR")
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
