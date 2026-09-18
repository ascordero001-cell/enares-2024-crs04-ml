"""Fail-closed diagnostic for the synthetic-only Stage 04 cloud image."""

from __future__ import annotations

from enares.stage04.c0_fixture import CATALOG_SIZE, build_synthetic_catalog


def main() -> int:
    catalog = build_synthetic_catalog()
    modules = {row.module_id for row in catalog}
    if len(catalog) != CATALOG_SIZE or CATALOG_SIZE != 516:
        raise RuntimeError("synthetic catalog size mismatch")
    if modules != {"3.1", "3.2", "3.3", "3.4", "3.5", "3.6"}:
        raise RuntimeError("synthetic module coverage mismatch")
    if any(row.synthetic is not True for row in catalog):
        raise RuntimeError("non-synthetic locator detected")
    print("synthetic_release=PASS catalog=516 modules=6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
