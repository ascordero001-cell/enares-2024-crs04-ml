"""Inactivity and signed-identity checks for the private dashboard."""

from pathlib import Path
from time import monotonic

from streamlit.testing.v1 import AppTest

from app.ui_redesign_app import IDLE_BLOCKED_KEY, IDLE_LAST_ACTIVITY_KEY
from app.views.idle_access import (
    IDLE_TIMEOUT_SECONDS,
    browser_session_allowed,
    client_idle_guard_html,
    fresh_password_authentication,
    iap_signout_url,
    idle_expired,
)

ROOT = Path(__file__).resolve().parents[1]


def test_idle_boundary_is_exactly_300_seconds() -> None:
    assert IDLE_TIMEOUT_SECONDS == 300
    assert not idle_expired(None, 300.0)
    assert not idle_expired(1.0, 300.999)
    assert idle_expired(1.0, 301.0)


def test_new_browser_session_rejects_stale_password_even_with_valid_iap_cookie() -> None:
    assert fresh_password_authentication(1000, 1299.999)
    assert not fresh_password_authentication(1000, 1300)
    assert not fresh_password_authentication(None, 1300)
    assert not fresh_password_authentication(0, 1300)
    assert not fresh_password_authentication(2000, 1900)
    assert not browser_session_allowed(1000, None, 1300)
    assert browser_session_allowed(1000, None, 1299)
    assert browser_session_allowed(1000, 1000, 1600)
    assert not browser_session_allowed(1000, 999, 1600)


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


def test_cloud_entry_rejects_missing_iap_assertion_before_results(monkeypatch) -> None:
    monkeypatch.setenv("STAGE04_DATA_MODE", "AUTHENTICATED_SHADOW")
    monkeypatch.setenv("STAGE04_IAP_PROJECT_NUMBER", "901917389711")
    monkeypatch.setenv("STAGE04_IAP_REGION", "us-central1")
    monkeypatch.setenv("STAGE04_IAP_SERVICE", "enares-stage04-iap-pilot")
    monkeypatch.setenv("STAGE04_IAP_EXPECTED_UID", "synthetic-uid")
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "Acceso privado"
    assert not app.dataframe


def test_cloud_entry_fails_closed_without_iap_configuration(monkeypatch) -> None:
    monkeypatch.setenv("STAGE04_DATA_MODE", "AUTHENTICATED_SHADOW")
    monkeypatch.delenv("STAGE04_IAP_EXPECTED_UID", raising=False)
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "Acceso privado"
    assert not app.dataframe


def test_cloud_idle_ends_iap_cookie_before_a_new_password() -> None:
    assert iap_signout_url("https://pilot.example.test/") == (
        "https://pilot.example.test?gcp-iap-mode=GCIP_SIGNOUT"
    )
    assert iap_signout_url("http://pilot.example.test") is None
    assert iap_signout_url('https://pilot.example.test/"bad') is None


def test_browser_guard_hides_results_and_signs_out_after_300_seconds() -> None:
    html = client_idle_guard_html("https://pilot.example.test/")
    assert html is not None
    assert 'const timeoutMs = 300_000;' in html
    assert 'document.documentElement.style.visibility = "hidden";' in html
    assert 'window.location.replace(signoutUrl);' in html
    assert '"https://pilot.example.test?gcp-iap-mode=GCIP_SIGNOUT"' in html
    assert 'document.addEventListener("visibilitychange"' in html
    assert client_idle_guard_html("http://pilot.example.test") is None
