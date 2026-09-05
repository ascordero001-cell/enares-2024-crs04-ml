import inspect
import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from app.config import QUALITY_LABELS
from app.streamlit_app import local_repositories
from app.views.stage04_dashboard import (
    EXPORT_ENABLED,
    build_numeric_card,
    build_state_cards,
    filter_estimates,
)
from enares.stage04.privacy import PROTECTED_FIELDS
from enares.stage04.repository import BigQueryRepository, IndicatorRepository


ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "tests" / "golden" / "stage04_32_national"


def repositories() -> tuple[IndicatorRepository, IndicatorRepository]:
    return local_repositories()


def test_application_entrypoint_imports_and_builds_local_repositories():
    authorized, demo = repositories()
    assert isinstance(authorized, IndicatorRepository)
    assert isinstance(demo, IndicatorRepository)


def test_streamlit_application_starts_without_error():
    app = AppTest.from_file(str(ROOT / "app" / "streamlit_app.py"))
    app.run(timeout=15)
    assert not app.exception


def test_authorized_32_card_matches_approved_golden():
    authorized, _ = repositories()
    row = filter_estimates(authorized, "3.2", "Nacional", "Total")[0]
    card = build_numeric_card(row)
    expected = json.loads((GOLDEN / "expected_card_view_model.json").read_text(encoding="utf-8"))
    for key, value in expected.items():
        assert card[key] == value


def test_authorized_card_displays_required_statistics():
    authorized, _ = repositories()
    card = build_numeric_card(authorized.list_estimates("3.2")[0])
    for field in ("estimate_text", "standard_error_text", "interval_text", "cv_text", "n_text"):
        assert card[field]
    assert card["state"] == "SHADOW"
    assert card["release_id"]


def test_suppressed_demo_card_exposes_no_protected_value():
    _, demo = repositories()
    suppressed = next(card for card in build_state_cards(demo) if card["quality_status"] == "SUPPRESSED_EXERCISE")
    assert suppressed["protected_values_visible"] is False
    assert all(suppressed[field] is None for field in PROTECTED_FIELDS)


def test_demo_states_have_distinct_labels():
    _, demo = repositories()
    cards = build_state_cards(demo)
    assert {card["quality_status"] for card in cards} == set(QUALITY_LABELS)
    assert len({card["quality_label"] for card in cards}) == 3


def test_unsupported_filter_returns_no_rows_instead_of_fabricating_results():
    authorized, _ = repositories()
    assert filter_estimates(authorized, "3.2", "Sexo", "Mujer") == []


def test_application_does_not_open_private_or_individual_sources():
    import app.streamlit_app as entrypoint

    source = inspect.getsource(entrypoint).lower()
    assert ".sav" not in source
    assert "survey_input" not in source
    assert "google drive" not in source
    assert "respondent_id" not in source


def test_export_is_disabled_and_stage03_is_not_recalculated():
    import app.views.stage04_dashboard as dashboard

    assert EXPORT_ENABLED is False
    assert "stage03" not in inspect.getsource(dashboard).lower()


def test_bigquery_access_remains_blocked():
    with pytest.raises(RuntimeError, match="BLOCKED_BY_CLOUD_GATE"):
        BigQueryRepository().list_estimates("3.2")
