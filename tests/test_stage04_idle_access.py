"""Inactivity checks for the private Stage 04 dashboard."""

from hashlib import pbkdf2_hmac
from pathlib import Path
from time import monotonic

from streamlit.testing.v1 import AppTest

from app.ui_redesign_app import IDLE_BLOCKED_KEY, IDLE_LAST_ACTIVITY_KEY, LOGIN_OK_KEY
from app.views.idle_access import IDLE_TIMEOUT_SECONDS, idle_expired
from app.views.login_access import MIN_PBKDF2_ITERATIONS, verify_credentials

ROOT = Path(__file__).resolve().parents[1]
TEST_USERNAME = "synthetic-reviewer"
TEST_PASSWORD = "synthetic-password-for-test-only"
TEST_SALT = b"synthetic-salt-16"
TEST_HASH = (
    f"pbkdf2_sha256${MIN_PBKDF2_ITERATIONS}${TEST_SALT.hex()}$"
    f"{pbkdf2_hmac('sha256', TEST_PASSWORD.encode(), TEST_SALT, MIN_PBKDF2_ITERATIONS).hex()}"
)


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


def test_private_credentials_are_checked_without_plaintext_configuration() -> None:
    assert verify_credentials(TEST_USERNAME, TEST_PASSWORD, TEST_USERNAME, TEST_HASH)
    assert not verify_credentials(TEST_USERNAME, "wrong", TEST_USERNAME, TEST_HASH)
    assert not verify_credentials("wrong", TEST_PASSWORD, TEST_USERNAME, TEST_HASH)
    assert not verify_credentials(TEST_USERNAME, TEST_PASSWORD, TEST_USERNAME, "bad")


def test_cloud_entry_shows_login_before_any_results(monkeypatch) -> None:
    monkeypatch.setenv("STAGE04_DATA_MODE", "AUTHENTICATED_SHADOW")
    monkeypatch.setenv("STAGE04_LOGIN_USERNAME", TEST_USERNAME)
    monkeypatch.setenv("STAGE04_LOGIN_PASSWORD_HASH", TEST_HASH)
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "Iniciar sesión"
    assert [field.label for field in app.text_input] == ["Usuario", "Contraseña"]
    assert LOGIN_OK_KEY not in app.session_state
    assert not app.dataframe

    app.text_input[0].set_value(TEST_USERNAME)
    app.text_input[1].set_value("wrong")
    app.button[0].click().run(timeout=30)
    assert not app.exception
    assert LOGIN_OK_KEY not in app.session_state
    assert app.title[0].value == "Iniciar sesión"


def test_cloud_entry_fails_closed_without_password_hash(monkeypatch) -> None:
    monkeypatch.setenv("STAGE04_DATA_MODE", "AUTHENTICATED_SHADOW")
    monkeypatch.setenv("STAGE04_LOGIN_USERNAME", TEST_USERNAME)
    monkeypatch.delenv("STAGE04_LOGIN_PASSWORD_HASH", raising=False)
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)

    assert not app.exception
    assert app.title[0].value == "Iniciar sesión"
    assert not app.text_input
    assert not app.dataframe


def test_cloud_login_expires_and_requires_password_again(monkeypatch) -> None:
    monkeypatch.setenv("STAGE04_DATA_MODE", "AUTHENTICATED_SHADOW")
    monkeypatch.setenv("STAGE04_LOGIN_USERNAME", TEST_USERNAME)
    monkeypatch.setenv("STAGE04_LOGIN_PASSWORD_HASH", TEST_HASH)
    app = AppTest.from_file(str(ROOT / "app" / "ui_redesign_app.py")).run(timeout=30)
    app.text_input[0].set_value(TEST_USERNAME)
    app.text_input[1].set_value(TEST_PASSWORD)
    app.button[0].click().run(timeout=30)

    assert app.session_state[LOGIN_OK_KEY] is True
    app.session_state[IDLE_LAST_ACTIVITY_KEY] = monotonic() - IDLE_TIMEOUT_SECONDS - 1
    app.run(timeout=30)

    assert not app.exception
    assert LOGIN_OK_KEY not in app.session_state
    assert app.title[0].value == "Iniciar sesión"
    assert not app.dataframe
