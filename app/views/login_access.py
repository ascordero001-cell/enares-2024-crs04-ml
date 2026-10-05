"""Server-side verification for the IAP-protected dashboard's second login gate."""

from __future__ import annotations

from hashlib import pbkdf2_hmac
from hmac import compare_digest

MIN_PBKDF2_ITERATIONS = 600_000


def verify_credentials(
    username: str,
    password: str,
    expected_username: str,
    encoded_hash: str,
) -> bool:
    """Check a salted PBKDF2 hash without keeping the raw password in code."""
    try:
        scheme, rounds_text, salt_hex, digest_hex = encoded_hash.split("$")
        rounds = int(rounds_text)
        salt = bytes.fromhex(salt_hex)
        expected_digest = bytes.fromhex(digest_hex)
    except (ValueError, TypeError):
        return False
    if (
        scheme != "pbkdf2_sha256"
        or rounds < MIN_PBKDF2_ITERATIONS
        or len(salt) < 16
        or len(expected_digest) != 32
        or not expected_username
    ):
        return False
    actual_digest = pbkdf2_hmac("sha256", password.encode(), salt, rounds)
    return compare_digest(actual_digest, expected_digest) and compare_digest(
        username, expected_username
    )
