"""Build the isolated Stage 03 V0.5 full complex-survey validation notebook."""

from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_NOTEBOOK = (
    REPO_ROOT / "notebooks" / "03_limpieza" / "03_ENARES_2024_validacion_SPSS_R.ipynb"
)
TARGET_NOTEBOOK = (
    REPO_ROOT
    / "notebooks"
    / "03_limpieza"
    / "03B_ENARES_2024_cloud_full_survey_validation_v0_5.ipynb"
)


def _source(cell: dict) -> str:
    return "".join(cell.get("source", []))


def _set_source(cell: dict, source: str) -> None:
    cell["source"] = source.splitlines(keepends=True)


def _code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def _markdown_cell(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source.splitlines(keepends=True),
    }


def build_notebook(source_path: Path = SOURCE_NOTEBOOK) -> dict:
    notebook = json.loads(source_path.read_text(encoding="utf-8"))

    setup = _source(notebook["cells"][2])
    setup = setup.replace(
        "LOG_DIR = ROOT_DRIVE / '05Resultados' / 'logs' / 'stage03'\n"
        "OUTPUT_DIR = ROOT_DRIVE / '04Outputs'\n"
        "DOCS_DIR = ROOT_DRIVE / 'docs'\n"
        "R_DIR = ROOT_DRIVE / '03Scripts_R'",
        "REFERENCE_OUTPUT_DIR = ROOT_DRIVE / '04Outputs'\n"
        "SHADOW_NAME = 'shadow_full_v0_5'\n"
        "LOG_DIR = ROOT_DRIVE / '05Resultados' / 'logs' / 'stage03' / SHADOW_NAME\n"
        "OUTPUT_DIR = REFERENCE_OUTPUT_DIR / SHADOW_NAME\n"
        "DOCS_DIR = ROOT_DRIVE / 'docs' / SHADOW_NAME\n"
        "R_DIR = ROOT_DRIVE / '03Scripts_R' / SHADOW_NAME",
    )
    if "REFERENCE_OUTPUT_DIR" not in setup:
        raise RuntimeError("Could not isolate the notebook output directories")
    _set_source(notebook["cells"][2], setup)

    export = _source(notebook["cells"][4])
    export = export.replace(
        "analytical_crs04_adolescents'",
        "analytical_crs04_full_v0_5'",
    ).replace(
        "analytical_crs04_adolescents_for_r.csv",
        "analytical_crs04_full_v0_5_for_r.csv",
    )
    if "analytical_crs04_full_v0_5" not in export:
        raise RuntimeError("Could not select the full V0.5 BigQuery table")
    _set_source(notebook["cells"][4], export)

    contract = _source(notebook["cells"][6])
    contract = contract.replace(
        "[OUTPUT_DIR/'spss_reference_results.csv',\n"
        "                            OUTPUT_DIR/'spss_reference_results (1).csv']",
        "[REFERENCE_OUTPUT_DIR/'spss_reference_results.csv',\n"
        "                            REFERENCE_OUTPUT_DIR/'spss_reference_results (1).csv']",
    ).replace(
        "Falta spss_reference_results.csv en {OUTPUT_DIR}",
        "Falta spss_reference_results.csv en {REFERENCE_OUTPUT_DIR}",
    )
    if "REFERENCE_OUTPUT_DIR/'spss_reference_results.csv'" not in contract:
        raise RuntimeError("Could not route the official SPSS reference as read-only input")
    _set_source(notebook["cells"][6], contract)

    closure = _source(notebook["cells"][27])
    old_complete = "artifacts_complete=bool(artifact_manifest.exists.all())"
    new_complete = """required_shadow_artifacts=[
    export_path,specs_path,R_DIR/'survey_design.R',R_DIR/'tabulados.R',R_FILE,
    LOG_DIR/'stage3_csplan_validation.csv',
    LOG_DIR/'stage3_spss_vs_r_comparison.csv',
    LOG_DIR/'stage3_spss_vs_r_differences.csv',
    LOG_DIR/'stage3_spss_vs_r_coverage.csv',
    LOG_DIR/'stage3_spss_vs_r_strict_differences.csv']
artifacts_complete=all(path.exists() and path.stat().st_size>0
                       for path in required_shadow_artifacts)"""
    closure = closure.replace(old_complete, new_complete).replace(
        "(ROOT_DRIVE/'stage3_pass.md')",
        "(OUTPUT_DIR/'stage3_cloud_full_survey_pass.md')",
    )
    if new_complete not in closure or "ROOT_DRIVE/'stage3_pass.md'" in closure:
        raise RuntimeError("Could not patch the isolated closure gate")
    _set_source(notebook["cells"][27], closure)

    notebook["cells"][0]["source"] = [
        "# ENARES 2024 — Validación cloud completa V0.5 (SPSS vs. R)\n",
        "\n",
        "Valida la tabla cloud consolidada sin modificar los artefactos V0 oficiales. ",
        "El cierre exige 516 indicadores y las 3,014 filas del contrato estadístico.\n",
    ]

    notebook["cells"].extend(
        [
            _markdown_cell("## 12. Gate cloud completo y evidencia versionable\n"),
            _code_cell(
                """EXPECTED_INDICATORS=516
EXPECTED_COMPARISON_ROWS=3014
EXPECTED_STRICT_ROWS=3013
EXPECTED_DOCUMENTED_EXCEPTIONS=1

plan_audit=pd.read_csv(LOG_DIR/'stage3_csplan_validation.csv').iloc[0]
full_gate_checks={
    'indicator_specs': len(specs)==EXPECTED_INDICATORS,
    'spss_indicators': s.indicator_id.nunique()==EXPECTED_INDICATORS,
    'comparison_rows': len(comparison)==EXPECTED_COMPARISON_ROWS,
    'strict_rows': strict_equal_rows==EXPECTED_STRICT_ROWS,
    'documented_exceptions': documented_exception_rows==EXPECTED_DOCUMENTED_EXCEPTIONS,
    'validated_rows': validated_rows==EXPECTED_COMPARISON_ROWS,
    'only_spss_rows': only_spss==0,
    'only_r_rows': only_r==0,
    'analytical_rows': int(plan_audit['filas'])==18807,
    'strata': int(plan_audit['estratos'])==25,
    'psus': int(plan_audit['conglomerados'])==1115,
    'design_df': int(plan_audit['grados_libertad'])==1090,
    'closure_passed': bool(passed),
}
failed_checks=[name for name,ok in full_gate_checks.items() if not ok]
if failed_checks:
    raise RuntimeError(f'FULL SURVEY GATE failed: {failed_checks}')

print('Indicators:',len(specs))
print('Comparison rows:',len(comparison))
print('Strict matches:',strict_equal_rows)
print('Documented exceptions:',documented_exception_rows)
print('Validated rows:',validated_rows)
print('Survey design: 18807 rows, 25 strata, 1115 PSUs, 1090 df')
print('FULL SURVEY GATE: PASS')
"""
            ),
            _code_cell(
                """evidence_path=OUTPUT_DIR/'stage3_cloud_full_survey_pass.md'
comparison_evidence_path=LOG_DIR/'stage3_cloud_full_survey_comparison_20260823.csv'
comparison.to_csv(comparison_evidence_path,index=False)

exception_rows=comparison.loc[comparison.EXCEPCION_DOCUMENTADA.fillna(False),
                              ['indicator_id','dimension','categoria_spss']]
exception_text='; '.join(' — '.join(map(str,row)) for row in exception_rows.to_numpy())
evidence_text=(
    '# Stage 03 cloud full survey validation — CRS04\\n\\n'
    'Resultado: PASS_CON_EXCEPCION_DOCUMENTADA\\n\\n'
    f'- Fecha UTC: {RUN_UTC}\\n'
    f'- Tabla candidata: `{A}`\\n'
    f'- Export SHA-256: `{sha256(export_path)}`\\n'
    f'- Filas analíticas: {len(df)}\\n'
    f'- Indicadores: {len(specs)}\\n'
    f'- Filas comparadas: {len(comparison)}\\n'
    f'- Coincidencias estrictas SPSS–R: {strict_equal_rows}\\n'
    f'- Excepciones documentadas: {documented_exception_rows}\\n'
    f'- Filas validadas: {validated_rows}\\n'
    f'- Solo SPSS: {only_spss}\\n'
    f'- Solo R: {only_r}\\n'
    '- Diseño: 18,807 filas; 25 estratos; 1,115 UPM; 1,090 gl\\n'
    f'- Excepción histórica: {exception_text}\\n\\n'
    'La referencia SPSS V0 se leyó desde `04Outputs` y no fue modificada. '
    'Todos los productos de esta ejecución se escribieron bajo `shadow_full_v0_5`.\\n')
evidence_path.write_text(evidence_text,encoding='utf-8')

evidence_manifest=pd.DataFrame([
    {'file':str(evidence_path),'sha256':sha256(evidence_path)},
    {'file':str(comparison_evidence_path),'sha256':sha256(comparison_evidence_path)},
])
display(evidence_manifest)
print('Evidence:',evidence_path)
print('Comparison:',comparison_evidence_path)
print('FULL SURVEY EVIDENCE: PASS')
"""
            ),
            _code_cell(
                """import zipfile
bundle_path=OUTPUT_DIR/'stage3_cloud_full_survey_evidence_20260823.zip'
bundle_files=[
    evidence_path,
    comparison_evidence_path,
    LOG_DIR/'stage3_nb09_closure.csv',
    LOG_DIR/'stage3_spss_vs_r_coverage.csv',
]
with zipfile.ZipFile(bundle_path,'w',compression=zipfile.ZIP_DEFLATED) as bundle:
    for path in bundle_files:
        bundle.write(path,arcname=path.name)
print('Evidence bundle:',bundle_path)
"""
            ),
        ]
    )

    for cell in notebook["cells"]:
        if cell.get("cell_type") == "code":
            cell["execution_count"] = None
            cell["outputs"] = []

    return notebook


def main() -> None:
    notebook = build_notebook()
    TARGET_NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
    TARGET_NOTEBOOK.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    print(f"Created: {TARGET_NOTEBOOK}")
    print(f"Cells: {len(notebook['cells'])}")
    print("Outputs remaining: 0")
    print("FULL NOTEBOOK BUILD: PASS")


if __name__ == "__main__":
    main()
