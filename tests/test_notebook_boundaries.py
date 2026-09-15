import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
EXECUTION_METADATA = {"execution", "executionInfo", "outputId"}


def test_tracked_notebooks_do_not_store_execution_artifacts() -> None:
    paths = sorted(NOTEBOOKS.rglob("*.ipynb"))
    assert paths

    for path in paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "code":
                assert cell.get("outputs", []) == [], path
                assert cell.get("execution_count") is None, path
            assert EXECUTION_METADATA.isdisjoint(cell.get("metadata", {})), path


def test_stage04_runtime_does_not_import_notebooks_or_survey_input() -> None:
    runtime_files = [
        *sorted((ROOT / "src" / "enares" / "stage04").rglob("*.py")),
        *sorted((ROOT / "app").rglob("*.py")),
    ]
    source = "\n".join(path.read_text(encoding="utf-8") for path in runtime_files)

    assert "notebooks" not in source
    assert "survey_input" not in source
