"""Fail-closed IAP identity verification, independent of Streamlit state."""

import json

from app.views.iap_identity import (
    IAP_CERTS_URL,
    IAP_ISSUER,
    cloud_run_iap_audience,
    verified_external_iap_auth_time,
    verify_external_iap_identity,
)

AUDIENCE = cloud_run_iap_audience(
    "901917389711", "us-central1", "enares-stage04-iap-pilot"
)
UID = "synthetic-authorized-uid"


def _claims(**overrides):
    claims = {
        "iss": IAP_ISSUER,
        "aud": AUDIENCE,
        "sub": "securetoken.google.com/example:synthetic-authorized-uid",
        "gcip": json.dumps(
            {
                "sub": UID,
                "auth_time": 1_800_000_000,
                "firebase": {"sign_in_provider": "password"},
            }
        ),
    }
    claims.update(overrides)
    return claims


def test_valid_external_password_identity_uses_signed_iap_verifier():
    observed: dict[str, str] = {}

    def verifier(token, _request, *, audience, certs_url):
        observed.update(token=token, audience=audience, certs_url=certs_url)
        return _claims()

    assert verify_external_iap_identity("signed-token", AUDIENCE, UID, verifier=verifier)
    assert observed == {
        "token": "signed-token",
        "audience": AUDIENCE,
        "certs_url": IAP_CERTS_URL,
    }


def test_missing_or_malformed_identity_never_opens_v0():
    good = lambda *_args, **_kwargs: _claims()
    assert not verify_external_iap_identity(None, AUDIENCE, UID, verifier=good)
    assert not verify_external_iap_identity("token", "", UID, verifier=good)
    assert not verify_external_iap_identity("token", AUDIENCE, "", verifier=good)
    for invalid in (
        _claims(iss="https://attacker.invalid"),
        _claims(aud="/projects/other/locations/us-central1/services/other"),
        _claims(gcip="not-json"),
        _claims(gcip=json.dumps({"sub": "other", "firebase": {"sign_in_provider": "password"}})),
        _claims(gcip=json.dumps({"sub": UID, "firebase": {"sign_in_provider": "google.com"}})),
        _claims(gcip=None),
    ):
        assert not verify_external_iap_identity(
            "token", AUDIENCE, UID, verifier=lambda *_args, item=invalid, **_kwargs: item
        )


def test_invalid_signature_fails_closed():
    def verifier(*_args, **_kwargs):
        raise ValueError("bad signature")

    assert not verify_external_iap_identity(
        "forged-token", AUDIENCE, UID, verifier=verifier
    )


def test_password_time_must_come_from_signed_iap_gcip_claims():
    good = lambda *_args, **_kwargs: _claims()
    assert verified_external_iap_auth_time(
        "signed-token", AUDIENCE, UID, verifier=good
    ) == 1_800_000_000
    for invalid_time in (None, False, "1800000000", 0, -1):
        claims = _claims(
            gcip=json.dumps(
                {
                    "sub": UID,
                    "auth_time": invalid_time,
                    "firebase": {"sign_in_provider": "password"},
                }
            )
        )
        assert verified_external_iap_auth_time(
            "signed-token",
            AUDIENCE,
            UID,
            verifier=lambda *_args, item=claims, **_kwargs: item,
        ) is None
    assert verified_external_iap_auth_time(
        "forged-token",
        AUDIENCE,
        UID,
        verifier=lambda *_args, **_kwargs: (_ for _ in ()).throw(ValueError("bad sig")),
    ) is None
