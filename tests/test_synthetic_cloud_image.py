from pathlib import Path

from enares.stage04.c0_fixture import CATALOG_SIZE, build_synthetic_catalog

ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_dockerfile_excludes_institutional_payloads() -> None:
    dockerfile = (ROOT / "Dockerfile.synthetic").read_text(encoding="utf-8")

    assert "COPY --chown=app:app app/__init__.py app/c0_navigation_app.py" in dockerfile
    assert "app/data" not in dockerfile
    assert "authorized_extract" not in dockerfile
    assert "repository.py" not in dockerfile
    assert "c0_navigation_app.py" in dockerfile


def test_synthetic_catalog_is_explicit_and_complete() -> None:
    catalog = build_synthetic_catalog()

    assert len(catalog) == CATALOG_SIZE == 516
    assert {row.module_id for row in catalog} == {
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
        "3.6",
    }
    assert all(row.synthetic is True for row in catalog)
