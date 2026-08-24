from scripts.generate_stage03_closure_dataform import (
    ANALYTICAL_RELEASE_GIT_COMMIT_SHA,
    RELEASE_ID,
    render_parity_assertion,
    render_pipeline_runs,
    render_quality_assertion,
    render_reporting_model,
    render_validation_results,
    survey_columns,
)


def test_full_survey_contract_has_explicit_approved_projection():
    columns = survey_columns()
    model = render_reporting_model()

    assert len(columns) == 737
    assert len(set(columns)) == 737
    assert columns[:7] == [
        "ID",
        "COLEGIAL_ID",
        "CCDD",
        "ID_AULA",
        "FACTOR_ALUMNOS",
        "SEXO",
        "AREA",
    ]
    assert "SELECT *" not in model
    assert '${ref("analytical_crs04_full_v0_5")}' in model
    for column in columns:
        assert f"analytical.`{column}`" in model


def test_full_survey_quality_gates_keys_design_and_schema():
    quality = render_quality_assertion()
    assert "duplicate_keys" in quality
    assert "FACTOR_ALUMNOS <= 0" in quality
    assert "column_count != 737" in quality
    assert "COUNT(*) != 18807" in quality


def test_full_survey_parity_covers_complete_projection():
    parity = render_parity_assertion()
    assert "EXCEPT DISTINCT" in parity
    assert parity.count("EXCEPT DISTINCT") == 2
    for column in survey_columns():
        assert f"reference_source.`{column}`" in parity


def test_pipeline_run_has_required_traceability_fields():
    pipeline_runs = render_pipeline_runs()
    for field in [
        "run_id",
        "release_id",
        "source_hash",
        "git_commit_sha",
        "dataform_release",
        "execution_started_at",
        "execution_finished_at",
        "validation_status",
    ]:
        assert field in pipeline_runs
    assert RELEASE_ID in pipeline_runs
    assert "dataform.projectConfig.vars.runId" in pipeline_runs
    assert "dataform.projectConfig.vars.gitCommitSha" in pipeline_runs
    assert ANALYTICAL_RELEASE_GIT_COMMIT_SHA in pipeline_runs
    assert "analytical_release_git_commit_sha" in pipeline_runs
    assert "promotion_status" in pipeline_runs
    assert '"shadow" AS promotion_status' in pipeline_runs


def test_validation_registry_is_aggregate_and_evidence_linked():
    registry = render_validation_results()
    assert registry.count(" AS validation_name") == 5
    assert "3014 validated; 3013 strict; 1 documented VS_12M exception" in registry
    assert "COLEGIAL_ID" not in registry
    assert "evidence_path" in registry
    assert "dataform.projectConfig.vars.runId" in registry
