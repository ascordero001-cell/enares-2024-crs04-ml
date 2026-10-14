"""Verify the signed IAP identity before opening the V0 repository."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any

from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests
from google.oauth2 import id_token

IAP_CERTS_URL = "https://www.gstatic.com/iap/verify/public_key"
IAP_ISSUER = "https://cloud.google.com/iap"


def cloud_run_iap_audience(project_number: str, region: str, service: str) -> str:
    """Build the exact signed-header audience of one Cloud Run service."""
    if not all((project_number.isdecimal(), region, service)):
        raise ValueError("IAP audience configuration is incomplete")
    return f"/projects/{project_number}/locations/{region}/services/{service}"


def verify_external_iap_identity(
    assertion: str | None,
    expected_audience: str,
    expected_uid: str,
    *,
    verifier: Callable[..., Mapping[str, Any]] | None = None,
) -> bool:
    """Accept only a signed IAP token for the configured Identity Platform user.

    Unsigned identity headers, a Streamlit session flag, and caller-provided
    usernames are never sufficient. A missing configuration fails closed.
    """
    if not assertion or not expected_audience or not expected_uid:
        return False
    if verifier is None:
        verifier = id_token.verify_token
    try:
        claims = verifier(
            assertion,
            requests.Request(),
            audience=expected_audience,
            certs_url=IAP_CERTS_URL,
        )
        if claims.get("iss") != IAP_ISSUER:
            return False
        if claims.get("aud") != expected_audience:
            return False
        gcip_raw = claims.get("gcip")
        gcip = json.loads(gcip_raw) if isinstance(gcip_raw, str) else gcip_raw
        if not isinstance(gcip, dict):
            return False
        firebase = gcip.get("firebase")
        if not isinstance(firebase, dict):
            return False
        if firebase.get("sign_in_provider") != "password":
            return False
        return gcip.get("sub") == expected_uid
    except (ValueError, TypeError, KeyError, OSError, GoogleAuthError):
        return False
