from pathlib import Path

import pytest

from enares.indicators.household import household_form, vp_hogar


ROOT = Path(__file__).resolve().parents[2]


def form(**overrides):
    values = {
        "sexo": 1,
        "item": 1,
        "gateway": 1,
        "perpetrator_a": None,
        "perpetrator_e": None,
        "confirm_c": None,
        "confirm_d": None,
        "confirm_f": None,
    }
    values.update(overrides)
    return household_form(**values)


def test_direct_perpetrator_codes_open_the_form():
    assert form(perpetrator_a=1) == 1
    assert form(perpetrator_e=19) == 1


def test_nonstandard_a_requires_both_confirmations():
    assert form(
        perpetrator_a=8,
        confirm_c=1,
        confirm_d=1,
    ) == 1

    assert form(
        perpetrator_a=8,
        confirm_c=1,
        confirm_d=0,
    ) == 0


def test_nonstandard_e_requires_confirmation_f():
    assert form(
        perpetrator_e=8,
        confirm_f=1,
    ) == 1

    assert form(
        perpetrator_e=8,
        confirm_f=0,
    ) == 0


@pytest.mark.parametrize(
    "overrides",
    [
        {"sexo": None},
        {"sexo": 3},
        {"item": None},
        {"item": 2},
        {"gateway": None},
        {"gateway": 2},
    ],
)
def test_closed_or_invalid_cases_become_zero(overrides):
    assert form(**overrides) == 0


def test_vp_hogar_aggregates_any_positive_form():
    assert vp_hogar([0] * 11) == 0
    assert vp_hogar([0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]) == 1


def test_generated_dataform_model_contains_exactly_eleven_forms():
    model = (
        ROOT
        / "dataform/definitions/analytical/"
        "pilot_32_household_v0_5.sqlx"
    ).read_text(encoding="utf-8")

    for index in range(1, 12):
        assert f"C3P201_{index}_1" in model

    assert "C3P201_12_1" not in model