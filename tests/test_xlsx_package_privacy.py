import io
import zipfile
from dataclasses import replace

import pytest

from app.streamlit_app import local_repositories
from enares.stage04.export import build_export_bundle


def _bundle(row=None):
    authorized, _ = local_repositories()
    selected = row or authorized.list_estimates("3.2")[0]
    return build_export_bundle([selected], basename="privacy-check")


def test_xlsx_contains_only_the_minimal_internal_package():
    with zipfile.ZipFile(io.BytesIO(_bundle().xlsx_bytes)) as archive:
        names = set(archive.namelist())

    assert names == {
        "[Content_Types].xml",
        "_rels/.rels",
        "xl/_rels/workbook.xml.rels",
        "xl/workbook.xml",
        "xl/worksheets/sheet1.xml",
    }
    assert not any(
        marker in name.lower()
        for name in names
        for marker in ("comment", "external", "custom", "drawing", "vba", "embedding")
    )


def test_xlsx_has_no_external_relationships_formulas_or_metadata():
    bundle = _bundle()
    with zipfile.ZipFile(io.BytesIO(bundle.xlsx_bytes)) as archive:
        package = b"\n".join(archive.read(name) for name in archive.namelist())

    assert b'TargetMode="External"' not in package
    assert b"<f" not in package
    assert b"docProps" not in package


@pytest.mark.parametrize(
    "private_locator",
    [
        r"C:\Users\private",
        "/Users/private",
        "/home/private",
        r"D:\private",
        r"\\server\share",
        "file:///private",
        "https://drive.google.com/private",
        "https://docs.google.com/private",
    ],
)
def test_export_rejects_personal_or_drive_locators(private_locator):
    authorized, _ = local_repositories()
    row = replace(
        authorized.list_estimates("3.2")[0],
        quality_note=f"internal {private_locator}",
    )
    with pytest.raises(ValueError, match="private locator"):
        _bundle(row)


def test_xlsx_archive_is_byte_deterministic():
    first = _bundle().xlsx_bytes
    second = _bundle().xlsx_bytes
    assert first == second
