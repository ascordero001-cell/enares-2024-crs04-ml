import csv
import io
import zipfile
from dataclasses import replace
from xml.etree import ElementTree

import pytest

from app.streamlit_app import local_repositories
from enares.stage04.export import (
    EXPORT_COLUMNS,
    build_export_bundle,
    build_export_records,
)

XML_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def _xlsx_rows(payload: bytes) -> list[list[str]]:
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        root = ElementTree.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    rows = []
    for row in root.findall(f".//{{{XML_NS}}}row"):
        values = []
        for cell in row.findall(f"{{{XML_NS}}}c"):
            inline = cell.find(f"{{{XML_NS}}}is/{{{XML_NS}}}t")
            numeric = cell.find(f"{{{XML_NS}}}v")
            if inline is not None:
                values.append(inline.text or "")
            elif numeric is not None:
                values.append(numeric.text or "")
            else:
                values.append("")
        rows.append(values)
    return rows


def _authorized_row():
    authorized, _ = local_repositories()
    return authorized.list_estimates("3.2")[0]


def test_csv_and_excel_reproduce_the_same_authorized_cut():
    bundle = build_export_bundle([_authorized_row()], basename="3.2 Nacional")
    csv_rows = list(csv.reader(io.StringIO(bundle.csv_bytes.decode("utf-8"))))

    assert csv_rows == _xlsx_rows(bundle.xlsx_bytes)
    assert csv_rows[0] == list(EXPORT_COLUMNS)
    assert csv_rows[1][EXPORT_COLUMNS.index("estimate_percent")] == "16.743298178932108"
    assert csv_rows[1][EXPORT_COLUMNS.index("base_unw")] == "18807"
    assert bundle.basename == "3.2-nacional"
    assert bundle.row_count == 1


@pytest.mark.parametrize("prefix", ["=", "+", "-", "@"])
def test_text_formula_prefixes_are_literal_in_both_formats(prefix):
    row = replace(_authorized_row(), indicator_name=f"{prefix}unsafe")
    bundle = build_export_bundle([row], basename="safe")
    csv_rows = list(csv.reader(io.StringIO(bundle.csv_bytes.decode("utf-8"))))
    xlsx_rows = _xlsx_rows(bundle.xlsx_bytes)
    column = EXPORT_COLUMNS.index("indicator_name")

    assert csv_rows[1][column] == f"'{prefix}unsafe"
    assert xlsx_rows[1][column] == f"'{prefix}unsafe"
    assert b"<f" not in bundle.xlsx_bytes


def test_negative_numeric_values_are_not_rewritten_as_text():
    records = build_export_records([_authorized_row()])
    records[0]["standard_error"] = -0.5
    from enares.stage04.export import records_to_csv, records_to_xlsx

    csv_rows = list(csv.reader(io.StringIO(records_to_csv(records).decode("utf-8"))))
    xlsx_rows = _xlsx_rows(records_to_xlsx(records))
    column = EXPORT_COLUMNS.index("standard_error")
    assert csv_rows[1][column] == "-0.5"
    assert xlsx_rows[1][column] == "-0.5"


def test_synthetic_or_empty_cuts_cannot_be_exported():
    _, demo = local_repositories()
    with pytest.raises(ValueError, match="provenance-verified"):
        build_export_bundle(demo.list_estimates("3.2"), basename="demo")
    with pytest.raises(ValueError, match="at least one"):
        build_export_bundle([], basename="empty")
