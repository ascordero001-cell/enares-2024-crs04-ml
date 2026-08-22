from pathlib import Path

import pytest

from enares.indicators.school import school_form, vp_escuela


ROOT = Path(__file__).resolve().parents[2]


def form(**overrides):
    values = {
        "item": 1,
        "gateway": 1,
        "confirmation_a": None,
        "confirmation_c": None,
        "confirmation_e": None,
    }
    values.update(overrides)
    return school_form(**values)


def test_any_confirmation_opens_the_form():
    assert form(confirmation_a=1) == 1
    assert form(confirmation_c=1) == 1
    assert form(confirmation_e=1) == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"item": None, "confirmation_a": 1},
        {"item": 2, "confirmation_a": 1},
        {"gateway": None, "confirmation_a": 1},
        {"gateway": 2, "confirmation_a": 1},
    ],
)
def test_item_and_gateway_must_both_be_open(overrides):
    assert form(**overrides) == 0


def test_missing_or_nonmatching_confirmations_become_zero():
    assert form() == 0
    assert form(
        confirmation_a=2,
        confirmation_c=2,
        confirmation_e=2,
    ) == 0


def test_vp_escuela_aggregates_any_positive_form():
    assert vp_escuela([0] * 14) == 0
    assert vp_escuela([0, 0, 1] + [0] * 11) == 1


def test_generated_dataform_model_contains_exactly_fourteen_forms():
    model = (
        ROOT
        / "dataform/definitions/analytical/"
        "pilot_33_school_v0_5.sqlx"
    ).read_text(encoding="utf-8")

    for index in range(1, 15):
        assert f"C3P223_{index}_1" in model

    assert "C3P223_15_1" not in model