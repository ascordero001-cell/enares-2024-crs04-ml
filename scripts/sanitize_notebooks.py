"""Remove executed outputs and execution metadata from tracked notebooks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
EXECUTION_METADATA = {"execution", "executionInfo", "outputId"}


def sanitize(path: Path) -> bool:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            if cell.get("outputs"):
                cell["outputs"] = []
                changed = True
            if cell.get("execution_count") is not None:
                cell["execution_count"] = None
                changed = True

        metadata = cell.get("metadata", {})
        for key in EXECUTION_METADATA & metadata.keys():
            del metadata[key]
            changed = True

    if changed:
        serialized = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
        path.write_text(serialized, encoding="utf-8", newline="\n")
    return changed


def main() -> None:
    changed = [path for path in NOTEBOOKS.rglob("*.ipynb") if sanitize(path)]
    print(f"Sanitized {len(changed)} notebook(s)")


if __name__ == "__main__":
    main()
