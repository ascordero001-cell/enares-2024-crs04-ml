"""Pure inactivity boundary for the private Stage 04 browser session."""

IDLE_TIMEOUT_SECONDS = 300


def idle_expired(last_activity: float | None, now: float) -> bool:
    """Require an explicit continuation at or after five minutes idle."""
    return last_activity is not None and now - last_activity >= IDLE_TIMEOUT_SECONDS
