from pathlib import Path

from scripts.build_stage03_full_survey_notebook import SOURCE_NOTEBOOK, build_notebook


def _all_source(notebook: dict) -> str:
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def test_full_notebook_uses_cloud_candidate_and_official_reference() -> None:
    source_path = Path(SOURCE_NOTEBOOK)
    notebook = build_notebook(source_path)
    text = _all_source(notebook)

    assert "analytical_crs04_full_v0_5" in text
    assert "REFERENCE_OUTPUT_DIR/'spss_reference_results.csv'" in text
    assert "analytical_crs04_adolescents_for_r.csv" not in text


def test_full_notebook_isolates_every_generated_artifact() -> None:
    notebook = build_notebook()
    text = _all_source(notebook)

    assert "SHADOW_NAME = 'shadow_full_v0_5'" in text
    assert "OUTPUT_DIR = REFERENCE_OUTPUT_DIR / SHADOW_NAME" in text
    assert "LOG_DIR = ROOT_DRIVE / '05Resultados' / 'logs' / 'stage03' / SHADOW_NAME" in text
    assert "R_DIR = ROOT_DRIVE / '03Scripts_R' / SHADOW_NAME" in text
    assert "ROOT_DRIVE/'stage3_pass.md'" not in text


def test_full_notebook_has_strict_expected_gate() -> None:
    notebook = build_notebook()
    text = _all_source(notebook)

    assert "EXPECTED_INDICATORS=516" in text
    assert "EXPECTED_COMPARISON_ROWS=3014" in text
    assert "EXPECTED_STRICT_ROWS=3013" in text
    assert "EXPECTED_DOCUMENTED_EXCEPTIONS=1" in text
    assert "validated_rows==EXPECTED_COMPARISON_ROWS" in text
    assert "['indicator_id','dimension','categoria_spss']" in text
    assert "FULL SURVEY GATE: PASS" in text


def test_full_notebook_is_sanitized_and_noninteractive() -> None:
    notebook = build_notebook()
    text = _all_source(notebook)

    code_cells = [cell for cell in notebook["cells"] if cell.get("cell_type") == "code"]
    assert all(cell.get("execution_count") is None for cell in code_cells)
    assert all(cell.get("outputs") == [] for cell in code_cells)
    assert "files.download" not in text
    assert "artifacts_complete=all(" in text


def test_appended_evidence_cells_are_valid_python() -> None:
    notebook = build_notebook()

    for cell in notebook["cells"][-3:]:
        compile("".join(cell["source"]), "<generated-notebook-cell>", "exec")
