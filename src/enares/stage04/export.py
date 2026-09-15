"""Deterministic, aggregate-only CSV and XLSX exports for Stage 04."""

from __future__ import annotations

import csv
import io
import math
import re
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from xml.etree.ElementTree import Element, SubElement, tostring

from .authorized_scopes import D09_CATEGORY_LABELS
from .presentation import DIMENSION_PRESENTATIONS
from .repository import IndicatorEstimate, is_verified_authorized_estimate
from .validation import validate_estimates

EXPORT_COLUMNS = (
    "module_id",
    "indicator_id",
    "indicator_name",
    "dimension",
    "source_dimension",
    "category",
    "source_category",
    "estimate_percent",
    "standard_error",
    "ci95_lower",
    "ci95_upper",
    "cv",
    "base_unw",
    "cv_flag",
    "n_flag",
    "quality_status",
    "quality_note",
    "universe",
    "denominator",
    "release_id",
    "run_id",
    "source_version",
    "state",
)

_FORMULA_PREFIXES = ("=", "+", "-", "@")
_FORBIDDEN_TEXT_PATTERNS = ("c:\\users\\", "/users/", "/home/", "d:\\", "\\\\", "file:///", "drive.google.com", "docs.google.com")
_XML_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
_CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
_SAFE_SLUG = re.compile(r"[^a-z0-9._-]+")


@dataclass(frozen=True)
class ExportBundle:
    """Two equivalent download representations of one validated aggregate cut."""

    basename: str
    csv_bytes: bytes
    xlsx_bytes: bytes
    row_count: int


def _safe_text(value: object) -> str:
    text = "" if value is None else str(value)
    return f"'{text}" if text.startswith(_FORMULA_PREFIXES) else text


def _display_dimension(source: str) -> str:
    presentation = DIMENSION_PRESENTATIONS.get(source)
    return presentation.display_name if presentation else source


def _display_category(row: IndicatorEstimate) -> str:
    category = D09_CATEGORY_LABELS.get((row.disaggregation, row.category), row.category)
    clean = category.removesuffix(" [referencial]")
    return f"{clean} [referencial]" if row.cv_flag else clean


def _record(row: IndicatorEstimate) -> dict[str, object]:
    return {
        "module_id": row.module_id,
        "indicator_id": row.indicator_id,
        "indicator_name": row.indicator_name,
        "dimension": _display_dimension(row.disaggregation),
        "source_dimension": row.disaggregation,
        "category": _display_category(row),
        "source_category": row.category,
        "estimate_percent": row.estimate,
        "standard_error": row.standard_error,
        "ci95_lower": row.ci95_lower,
        "ci95_upper": row.ci95_upper,
        "cv": row.cv,
        "base_unw": row.n_unweighted,
        "cv_flag": row.cv_flag,
        "n_flag": row.n_flag,
        "quality_status": row.quality_status,
        "quality_note": row.quality_note,
        "universe": row.universe,
        "denominator": row.denominator,
        "release_id": row.release_id,
        "run_id": row.run_id,
        "source_version": row.source_version,
        "state": "SHADOW",
    }


def _assert_no_private_locator(record: dict[str, object]) -> None:
    for value in record.values():
        if isinstance(value, str) and any(
            pattern in value.lower() for pattern in _FORBIDDEN_TEXT_PATTERNS
        ):
            raise ValueError("Export text contains a forbidden private locator")


def build_export_records(rows: Iterable[IndicatorEstimate]) -> list[dict[str, object]]:
    """Validate and project one authorized V0 cut without recalculation or imputation."""
    materialized = list(rows)
    if not materialized:
        raise ValueError("An export requires at least one aggregate row")
    if not all(is_verified_authorized_estimate(row) for row in materialized):
        raise ValueError("Only provenance-verified V0 aggregates can be exported")
    validate_estimates(materialized)
    records = [_record(row) for row in materialized]
    for record in records:
        _assert_no_private_locator(record)
    return records


def records_to_csv(records: list[dict[str, object]]) -> bytes:
    """Serialize records as UTF-8 CSV, neutralizing spreadsheet formulas in text."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=EXPORT_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for record in records:
        writer.writerow(
            {
                column: (
                    _safe_text(value)
                    if isinstance(value, str) or value is None
                    else value
                )
                for column, value in record.items()
            }
        )
    return buffer.getvalue().encode("utf-8")


def _column_name(index: int) -> str:
    name = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(65 + remainder) + name
    return name


def _worksheet(records: list[dict[str, object]]) -> bytes:
    worksheet = Element(f"{{{_XML_NS}}}worksheet")
    sheet_data = SubElement(worksheet, f"{{{_XML_NS}}}sheetData")
    matrix: list[list[object]] = [list(EXPORT_COLUMNS)]
    matrix.extend([[record[column] for column in EXPORT_COLUMNS] for record in records])
    for row_number, values in enumerate(matrix, start=1):
        row_element = SubElement(
            sheet_data, f"{{{_XML_NS}}}row", {"r": str(row_number)}
        )
        for column_number, value in enumerate(values, start=1):
            reference = f"{_column_name(column_number)}{row_number}"
            if isinstance(value, bool):
                cell = SubElement(
                    row_element,
                    f"{{{_XML_NS}}}c",
                    {"r": reference, "t": "inlineStr"},
                )
                inline = SubElement(cell, f"{{{_XML_NS}}}is")
                SubElement(inline, f"{{{_XML_NS}}}t").text = str(value)
            elif isinstance(value, (int, float)) and not isinstance(value, bool):
                if isinstance(value, float) and not math.isfinite(value):
                    raise ValueError("Non-finite values cannot be exported")
                cell = SubElement(row_element, f"{{{_XML_NS}}}c", {"r": reference})
                SubElement(cell, f"{{{_XML_NS}}}v").text = str(value)
            else:
                cell = SubElement(
                    row_element,
                    f"{{{_XML_NS}}}c",
                    {"r": reference, "t": "inlineStr"},
                )
                inline = SubElement(cell, f"{{{_XML_NS}}}is")
                SubElement(inline, f"{{{_XML_NS}}}t").text = _safe_text(value)
    return tostring(worksheet, encoding="utf-8", xml_declaration=True)


def _xlsx_parts(records: list[dict[str, object]]) -> dict[str, bytes]:
    content_types = Element(f"{{{_CONTENT_TYPES_NS}}}Types")
    SubElement(
        content_types,
        f"{{{_CONTENT_TYPES_NS}}}Default",
        {
            "Extension": "rels",
            "ContentType": "application/vnd.openxmlformats-package.relationships+xml",
        },
    )
    SubElement(
        content_types,
        f"{{{_CONTENT_TYPES_NS}}}Default",
        {"Extension": "xml", "ContentType": "application/xml"},
    )
    SubElement(
        content_types,
        f"{{{_CONTENT_TYPES_NS}}}Override",
        {
            "PartName": "/xl/workbook.xml",
            "ContentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml",
        },
    )
    SubElement(
        content_types,
        f"{{{_CONTENT_TYPES_NS}}}Override",
        {
            "PartName": "/xl/worksheets/sheet1.xml",
            "ContentType": "application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml",
        },
    )

    package_rels = Element(f"{{{_PACKAGE_REL_NS}}}Relationships")
    SubElement(
        package_rels,
        f"{{{_PACKAGE_REL_NS}}}Relationship",
        {
            "Id": "rId1",
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument",
            "Target": "xl/workbook.xml",
        },
    )

    workbook = Element(f"{{{_XML_NS}}}workbook")
    sheets = SubElement(workbook, f"{{{_XML_NS}}}sheets")
    SubElement(
        sheets,
        f"{{{_XML_NS}}}sheet",
        {"name": "estimaciones", "sheetId": "1", f"{{{_REL_NS}}}id": "rId1"},
    )

    workbook_rels = Element(f"{{{_PACKAGE_REL_NS}}}Relationships")
    SubElement(
        workbook_rels,
        f"{{{_PACKAGE_REL_NS}}}Relationship",
        {
            "Id": "rId1",
            "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet",
            "Target": "worksheets/sheet1.xml",
        },
    )

    return {
        "[Content_Types].xml": tostring(
            content_types, encoding="utf-8", xml_declaration=True
        ),
        "_rels/.rels": tostring(package_rels, encoding="utf-8", xml_declaration=True),
        "xl/workbook.xml": tostring(workbook, encoding="utf-8", xml_declaration=True),
        "xl/_rels/workbook.xml.rels": tostring(
            workbook_rels, encoding="utf-8", xml_declaration=True
        ),
        "xl/worksheets/sheet1.xml": _worksheet(records),
    }


def records_to_xlsx(records: list[dict[str, object]]) -> bytes:
    """Build a minimal deterministic OOXML workbook with no metadata or external links."""
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, content in sorted(_xlsx_parts(records).items()):
            info = zipfile.ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o600 << 16
            archive.writestr(info, content)
    return output.getvalue()


def build_export_bundle(
    rows: Iterable[IndicatorEstimate], *, basename: str
) -> ExportBundle:
    """Create equivalent CSV/XLSX bytes from one validated record projection."""
    safe_basename = _SAFE_SLUG.sub("-", basename.lower()).strip("-._")
    if not safe_basename:
        raise ValueError("Export basename must contain a safe character")
    records = build_export_records(rows)
    return ExportBundle(
        basename=safe_basename,
        csv_bytes=records_to_csv(records),
        xlsx_bytes=records_to_xlsx(records),
        row_count=len(records),
    )
