import json
from copy import deepcopy
from pathlib import Path

import pytest

from enares.stage04.repository import DemoRepository
from enares.stage04.view_model import to_card_view_model, to_indicator_contract


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden" / "stage04_32_national"
DEMO_FIXTURE = ROOT / "app" / "data" / "demo_indicator_estimates.csv"
NUMERIC_FIELDS = (
    "estimate",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
)
EXACT_FIELDS = (
    "indicator_id",
    "indicator_name",
    "module_id",
    "disaggregation",
    "category",
    "n_unweighted",
    "scale",
    "universe",
    "denominator",
    "state",
    "quality_status",
    "validation_status",
    "engine_version",
    "release_id",
    "source_hash",
)


def load_json(name: str) -> dict:
    return json.loads((GOLDEN / name).read_text(encoding="utf-8"))


def actual_pilot_row():
    selector = load_json("expected_indicator.json")
    rows = DemoRepository(DEMO_FIXTURE).list_estimates(selector["module_id"])
    matches = [
        row
        for row in rows
        if row.indicator_id == selector["indicator_id"]
        and row.disaggregation == selector["disaggregation"]
        and row.category == selector["category"]
    ]
    assert len(matches) == 1
    return matches[0]


def assert_matches_golden(actual: dict) -> None:
    expected = load_json("expected_indicator.json")
    tolerance = load_json("manifest.json")["numeric_tolerance"]["absolute"]
    for field in EXACT_FIELDS:
        assert field in actual, f"Missing exact golden field: {field}"
        assert actual[field] == expected[field]
    for field in NUMERIC_FIELDS:
        assert actual[field] == pytest.approx(expected[field], abs=tolerance, rel=0)


def test_approved_aggregate_matches_national_32_golden():
    actual = to_indicator_contract(actual_pilot_row())
    assert_matches_golden(actual)


def test_synthetic_change_to_estimate_fails():
    changed = deepcopy(to_indicator_contract(actual_pilot_row()))
    changed["estimate"] += 0.01
    with pytest.raises(AssertionError):
        assert_matches_golden(changed)


@pytest.mark.parametrize("field", ["release_id", "source_hash"])
def test_change_to_lineage_fails(field):
    changed = deepcopy(to_indicator_contract(actual_pilot_row()))
    changed[field] = "changed"
    with pytest.raises(AssertionError):
        assert_matches_golden(changed)


def test_missing_quality_status_fails():
    changed = deepcopy(to_indicator_contract(actual_pilot_row()))
    del changed["quality_status"]
    with pytest.raises(AssertionError, match="Missing exact golden field"):
        assert_matches_golden(changed)


def test_card_labels_and_states_are_exact():
    actual = to_card_view_model(actual_pilot_row())
    assert actual == load_json("expected_card_view_model.json")


@pytest.mark.parametrize(("field", "value"), [("module_label", "changed"), ("state", "APPROVED")])
def test_card_label_or_state_change_fails(field, value):
    actual = to_card_view_model(actual_pilot_row())
    actual[field] = value
    assert actual != load_json("expected_card_view_model.json")
