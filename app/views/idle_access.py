"""Pure inactivity boundary for the private Stage 04 browser session."""

from json import dumps
from pathlib import Path

IDLE_TIMEOUT_SECONDS = 300
AUTH_CLOCK_SKEW_SECONDS = 60


def idle_expired(last_activity: float | None, now: float) -> bool:
    """Require an explicit continuation at or after five minutes idle."""
    return last_activity is not None and now - last_activity >= IDLE_TIMEOUT_SECONDS


def fresh_password_authentication(auth_time: int | None, now: float) -> bool:
    """Admit a new browser session only after a recent password sign-in."""
    if auth_time is None or auth_time <= 0:
        return False
    age = now - auth_time
    return -AUTH_CLOCK_SKEW_SECONDS <= age < IDLE_TIMEOUT_SECONDS


def browser_session_allowed(
    auth_time: int | None, bound_auth_time: object, now: float
) -> bool:
    """Keep active sessions, but reject a stale IAP cookie on new sessions."""
    if auth_time is None:
        return False
    return bound_auth_time == auth_time or fresh_password_authentication(auth_time, now)


def iap_signout_url(service_url: str) -> str | None:
    """Build the IAP cookie-ending URL from trusted service configuration."""
    if not service_url.startswith("https://") or any(
        character in service_url for character in ('"', "'", "<", ">", "?", "#")
    ):
        return None
    return f"{service_url.rstrip('/')}?gcp-iap-mode=GCIP_SIGNOUT"


def client_idle_guard_html(service_url: str) -> str | None:
    """Return fixed browser-side protection for a trusted IAP service URL."""
    signout_url = iap_signout_url(service_url)
    if signout_url is None:
        return None
    template = Path(__file__).with_name("idle_guard.js").read_text(encoding="utf-8")
    return template.replace("__STAGE04_SIGNOUT_URL__", dumps(signout_url))
