import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPPER_SNAKE_MD = re.compile(r"^[A-Z0-9]+(?:_[A-Z0-9]+)*\.md$")
LOWER_SNAKE_MD = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*\.md$")


def test_root_normative_documents_use_upper_snake_case():
    normative_files = (
        ROOT / "PRE_STAGE04.md",
        ROOT / "NAMING_CONVENTIONS.md",
        ROOT / "CRS04_STAGE04_CORREGIDO_VER6_NUEVA_METODOLOGIA.md",
        ROOT / "CRS04_STAGE04_HOJA_ARQUITECTONICA_APP_VIGILANCIA.md",
        ROOT / "CRS04_STAGE04_VERSION_0_REGISTRO.md",
    )

    for path in normative_files:
        assert path.is_file(), f"Falta el documento normativo: {path.name}"
        assert UPPER_SNAKE_MD.fullmatch(path.name), (
            f"El documento normativo no usa MAYUSCULAS_SNAKE.md: {path.name}"
        )


def test_stage04_markdown_uses_snake_case():
    stage04_dir = ROOT / "docs" / "stage04"
    assert stage04_dir.is_dir(), "Falta docs/stage04"

    markdown_files = list(stage04_dir.rglob("*.md"))
    assert markdown_files, "docs/stage04 debe contener al menos un documento Markdown"

    invalid = [
        str(path.relative_to(ROOT))
        for path in markdown_files
        if not LOWER_SNAKE_MD.fullmatch(path.name)
    ]
    assert not invalid, f"Archivos Stage 04 con nombres no canónicos: {invalid}"


def test_bootstrap_files_have_no_download_suffixes():
    checked_files = [
        ROOT / "PRE_STAGE04.md",
        ROOT / "NAMING_CONVENTIONS.md",
        ROOT / "CRS04_STAGE04_CORREGIDO_VER6_NUEVA_METODOLOGIA.md",
        ROOT / "CRS04_STAGE04_HOJA_ARQUITECTONICA_APP_VIGILANCIA.md",
        ROOT / "CRS04_STAGE04_VERSION_0_REGISTRO.md",
        *(ROOT / "docs" / "stage04").rglob("*"),
    ]
    invalid = [str(path.relative_to(ROOT)) for path in checked_files if "(1)" in path.name]
    assert not invalid, f"Se encontraron sufijos de descarga: {invalid}"
