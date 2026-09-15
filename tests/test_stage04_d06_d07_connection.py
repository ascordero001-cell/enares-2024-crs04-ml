import csv
import hashlib
import json
import os
from dataclasses import replace
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from app.streamlit_app import local_repositories
from app.views.stage04_dashboard import precision_category_label
from enares.stage04.authorized_extract import build_d06_d07_authorized_extract
from enares.stage04.authorized_scopes import VS_MATRIX_PAIRS, VS_MATRIX_V0_CROSSES
from enares.stage04.repository import is_verified_authorized_estimate
from enares.stage04.validation import validate_estimates

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "app" / "data" / "v0_authorized_d06_d07_indicator_estimates.csv"
MANIFEST = (
    ROOT / "app" / "data" / "v0_authorized_d06_d07_indicator_estimates.manifest.json"
)
PARENT_SHA256 = "15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4"


def _rows():
    with EXTRACT.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_d06_d07_manifest_binds_exact_approved_extract():
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["row_count"] == 16
    assert manifest["scope"] == {"D06": 8, "D07": 8}
    assert manifest["synthetic"] is False
    assert manifest["source_hash"] == PARENT_SHA256
    assert manifest["sha256"] == hashlib.sha256(EXTRACT.read_bytes()).hexdigest()


def test_d06_d07_contain_two_complete_independent_v0_matrices():
    rows = _rows()
    assert {row["indicator_id"] for row in rows} == {"Solap_VS_12M", "Solap_VS_VIDA"}
    for indicator in ("Solap_VS_12M", "Solap_VS_VIDA"):
        selected = [row for row in rows if row["indicator_id"] == indicator]
        assert len(selected) == 8
        assert {
            (row["disaggregation"], row["category"]) for row in selected
        } == VS_MATRIX_PAIRS
    assert all(row["synthetic"] == "false" for row in rows)
    assert all(row["suppress_flag"] == "false" for row in rows)
    assert sum(row["cv_flag"] == "true" for row in rows) == 4
    assert all("[referencial]" not in row["category"] for row in rows)


def test_reference_marker_is_derived_exclusively_from_cv_flag():
    authorized, _ = local_repositories()
    rows = [
        row
        for row in authorized.list_estimates("3.5")
        if row.indicator_id in {"Solap_VS_12M", "Solap_VS_VIDA"}
    ]
    for row in rows:
        label = precision_category_label(row.category, row.cv_flag)
        assert ("[referencial]" in label) is row.cv_flag

    d07_rows = [row for row in rows if row.indicator_id == "Solap_VS_VIDA"]
    assert all(
        "[referencial]" not in precision_category_label(row.category, row.cv_flag)
        for row in d07_rows
    )


def test_d06_d07_repositories_derive_real_provenance_and_validate_crosses():
    authorized, _ = local_repositories()
    rows = [
        row
        for row in authorized.list_estimates("3.5")
        if row.indicator_id in {"Solap_VS_12M", "Solap_VS_VIDA"}
    ]
    assert len(rows) == 16
    assert all(is_verified_authorized_estimate(row) for row in rows)
    assert all(row.synthetic is False for row in rows)
    validate_estimates(rows)


def test_validation_passes_real_d06_d07_crosses_to_runtime_boundary(monkeypatch):
    calls = []

    def record_boundary(**kwargs):
        calls.append(kwargs)

    monkeypatch.setattr(
        "enares.stage04.validation.assert_v0_granularity_boundary", record_boundary
    )
    authorized, _ = local_repositories()
    rows = [
        row
        for row in authorized.list_estimates("3.5")
        if row.indicator_id in {"Solap_VS_12M", "Solap_VS_VIDA"}
    ]
    validate_estimates(rows)
    assert {next(iter(call["requested_crosses"])) for call in calls} == set(
        VS_MATRIX_V0_CROSSES
    )
    assert all(call["v0_crosses"] == set(VS_MATRIX_V0_CROSSES) for call in calls)
    assert all(call["synthetic"] is False for call in calls)


def test_validation_rejects_real_matrix_pair_not_present_in_v0():
    authorized, _ = local_repositories()
    row = next(
        row
        for row in authorized.list_estimates("3.5")
        if row.indicator_id == "Solap_VS_12M"
    )
    with pytest.raises(ValueError, match="outside the approved V0 matrix"):
        validate_estimates([replace(row, category="Cruce fabricado")])


def test_d06_d07_extract_rebuilds_byte_for_byte_from_private_parent(tmp_path):
    parent_value = os.environ.get("ENARES_V0_PARENT_AGGREGATE")
    if not parent_value:
        pytest.skip("Private V0 parent path is not available in CI")
    assert parent_value is not None
    output = tmp_path / EXTRACT.name
    manifest = tmp_path / MANIFEST.name
    build_d06_d07_authorized_extract(
        Path(parent_value),
        output,
        manifest,
        expected_parent_sha256=PARENT_SHA256,
        git_commit_sha="d3c2687bd738be879c65615e3572ff8a20628ff5",
        generated_at_utc="2026-09-14T21:45:00Z",
    )
    assert output.read_bytes() == EXTRACT.read_bytes()


def test_apptest_renders_both_v0_matrix_indicators_without_fabricated_crosses():
    app = AppTest.from_file(str(ROOT / "app" / "streamlit_app.py")).run(timeout=15)
    app.sidebar.radio[0].set_value("Módulo 3.5").run(timeout=15)
    assert not app.exception
    indicator = next(
        select for select in app.selectbox if select.label == "Indicador matricial"
    )
    assert set(indicator.options) == {"Solap_VS_12M", "Solap_VS_VIDA"}
    indicator.set_value("Solap_VS_VIDA").run(timeout=15)
    assert not app.exception
    matrix = next(select for select in app.selectbox if select.label == "Matriz")
    assert set(matrix.options) == {"2×2", "3×3"}
    assert len(app.metric) == 8
