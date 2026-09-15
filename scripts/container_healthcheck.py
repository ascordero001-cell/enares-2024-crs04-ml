"""Shallow liveness check for the pinned Streamlit server."""

from __future__ import annotations

import os
import sys
from urllib.request import urlopen


def health_url(port: str | None = None) -> str:
    """Build the local Streamlit health URL without accepting a remote host."""
    selected = port or os.environ.get("PORT", "8080")
    if not selected.isascii() or not selected.isdecimal():
        raise ValueError("PORT must be a decimal integer")
    numeric_port = int(selected)
    if not 1 <= numeric_port <= 65535:
        raise ValueError("PORT is outside the valid range")
    return f"http://127.0.0.1:{numeric_port}/_stcore/health"


def check_health(*, opener=urlopen, port: str | None = None) -> None:
    """Require Streamlit's tested health route to answer 200/ok."""
    with opener(health_url(port), timeout=2) as response:
        body = response.read().decode("utf-8").strip().lower()
        if response.status != 200 or body != "ok":
            raise RuntimeError("Streamlit health check did not return 200/ok")


def main() -> int:
    try:
        check_health()
    except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
        print(f"unhealthy: {exc}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
