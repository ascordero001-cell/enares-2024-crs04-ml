"""Inactivity checks for the private Stage 04 dashboard."""

from pathlib import Path
from time import monotonic

from streamlit.testing.v1 import AppTest

from app.ui_redesign_app import IDLE_BLOCKED_KEY, IDLE_LAST_ACTIVITY_KEY
from app.views.idle_access import IDLE_TIMEOUT_SECONDS, idle_expired

ROOT = Path(__file__).resolve().parents[1]


def test_idle_boundary_is_exactly_300_seconds() -> None:
    assert IDLE_TIMEOUT_SECONDS == 300
    assert not idle_expired(None, 300.0)
    assert not idle_expired(1.0, 300.999)
    assert idle_expired(1.0, 301.0)


def test_expired_session_clears_state_and_requires_continuation() -> None:
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)
    assert not app.exception
    app.session_state["real_filter_Sexo"] = "1"
    app.session_state[IDLE_LAST_ACTIVITY_KEY] = monotonic() - IDLE_TIMEOUT_SECONDS - 1
    app.run(timeout=30)

    assert not app.exception
    assert app.session_state[IDLE_BLOCKED_KEY] is True
    assert "real_filter_Sexo" not in app.session_state
    assert app.title[0].value == "Sesión bloqueada por inactividad"
    assert any(button.label == "Continuar con Google" for button in app.button)

    next(button for button in app.button if button.label == "Continuar con Google").click().run(timeout=30)
    assert not app.exception
    assert IDLE_BLOCKED_KEY not in app.session_state
    assert app.session_state[IDLE_LAST_ACTIVITY_KEY] > 0
