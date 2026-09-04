import json
from copy import deepcopy
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden" / "stage04_32_national"
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


def assert_matches_golden(actual: dict) -> None:
    expected = load_json("expected_indicator.json")
    tolerance = load_json("manifest.json")["numeric_tolerance"]["absolute"]
    for field in EXACT_FIELDS:
        assert field in actual, f"Missing exact golden field: {field}"
        assert actual[field] == expected[field]
    for field in NUMERIC_FIELDS:
        assert actual[field] == pytest.approx(expected[field], abs=tolerance, rel=0)


def test_approved_aggregate_matches_national_32_golden():
    assert_matches_golden(load_json("expected_indicator.json"))


def test_synthetic_change_to_estimate_fails():
    changed = deepcopy(load_json("expected_indicator.json"))
    changed["estimate"] += 0.01
    with pytest.raises(AssertionError):
        assert_matches_golden(changed)


@pytest.mark.parametrize("field", ["release_id", "source_hash"])
def test_change_to_lineage_fails(field):
    changed = deepcopy(load_json("expected_indicator.json"))
    changed[field] = "changed"
    with pytest.raises(AssertionError):
        assert_matches_golden(changed)


def test_missing_quality_status_fails():
    changed = deepcopy(load_json("expected_indicator.json"))
    del changed["quality_status"]
    with pytest.raises(AssertionError, match="Missing exact golden field"):
        assert_matches_golden(changed)


def test_card_labels_and_states_are_exact():
    card = load_json("expected_card_view_model.json")
    assert card["module_label"] == "3.2 Violencia en el hogar"
    assert card["estimate_text"] == "16.74 %"
    assert card["state"] == "SHADOW"
    assert card["quality_status"] == "PUBLISHABLE_CANDIDATE"
    assert card["release_id"] == "enares2024-crs04-v0-shadow-001"
