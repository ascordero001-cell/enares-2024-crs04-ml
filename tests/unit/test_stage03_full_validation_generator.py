from scripts.generate_stage03_full_validation_dataform import (
    EXPECTED_CLEANED_COLUMNS,
    EXPECTED_DERIVED_COLUMNS,
    EXPECTED_FULL_COLUMNS,
    cleaned_columns,
    derived_columns,
    full_columns,
    render_model,
    render_parity_assertion,
    render_quality_assertion,
    section_columns,
)


def test_full_contract_has_exact_authority_coverage_without_collisions():
    cleaned = cleaned_columns()
    derived = derived_columns()
    full = full_columns()

    assert len(cleaned) == EXPECTED_CLEANED_COLUMNS == 1206
    assert [len(columns) for _, columns in section_columns()] == [
        71,
        50,
        51,
        424,
        40,
        94,
    ]
    assert len(derived) == EXPECTED_DERIVED_COLUMNS == 730
    assert len(full) == EXPECTED_FULL_COLUMNS == 1937
    assert len(set(full)) == len(full)
    assert not set(cleaned) & set(derived)


def test_full_model_joins_every_shadow_section_and_rebuilds_id_aula():
    model = render_model()

    for section in range(31, 37):
        assert f'${{ref("analytical_crs04_stage{section}_v0_5")}}' in model
    assert '${ref("analytical_crs04_adolescents")}' not in model
    assert "CAST(cleaned.C3ANIO AS STRING)" in model
    assert "UPPER(TRIM(CAST(cleaned.C3SECC AS STRING)))" in model
    for column in derived_columns():
        assert f"AS `{column}`" in model


def test_full_quality_gate_checks_rows_keys_and_exact_schema_size():
    quality = render_quality_assertion()

    assert "row_count" in quality
    assert "duplicate_key_groups" in quality
    assert "null_id_aula" in quality
    assert "schema_column_count" in quality
    assert "column_count != 1937" in quality


def test_full_parity_normalizes_keys_and_projects_all_columns():
    parity = render_parity_assertion()

    assert '${ref("analytical_crs04_adolescents")}' in parity
    assert 'CAST(reference_source.`ID` AS INT64)' in parity
    assert 'CAST(reference_source.`COLEGIAL_ID` AS INT64)' in parity
    assert "TO_JSON_STRING(candidate) IS DISTINCT FROM TO_JSON_STRING(reference)" in parity
    for column in full_columns():
        assert f"AS `{column}`" in parity
