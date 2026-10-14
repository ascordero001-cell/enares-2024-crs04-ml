"""Pure inactivity boundary for the private Stage 04 browser session."""

from json import dumps
from pathlib import Path

IDLE_TIMEOUT_SECONDS = 300


def idle_expired(last_activity: float | None, now: float) -> bool:
    """Require an explicit continuation at or after five minutes idle."""
    return last_activity is not None and now - last_activity >= IDLE_TIMEOUT_SECONDS


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
