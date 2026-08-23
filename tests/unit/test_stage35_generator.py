from scripts.generate_stage35_dataform import (
    DEPENDENCIES,
    binary_non_null_columns,
    build_stage35_contract,
    output_columns,
    render_model,
    render_parity_assertion,
    render_quality_assertion,
)


def expressions() -> dict[str, str]:
    _, blocks = build_stage35_contract()
    return {name: sql for _, block in blocks for name, sql in block.items()}


def test_stage35_contract_matches_authority_counts():
    raw_inputs, blocks = build_stage35_contract()
    assert len(blocks) == 8
    assert [len(block) for _, block in blocks] == [15, 2, 5, 2, 3, 10, 2, 1]
    assert len(output_columns(blocks)) == 40
    assert len(set(output_columns(blocks))) == 40
    assert {"C3P233A", "C3P231_5E4", "C3P243_6", "C3P243_T6"}.issubset(raw_inputs)


def test_stage35_contract_preserves_key_formulas_and_nullable_domains():
    sql = expressions()
    assert sql["VS_HOGAR"] == "VS_H"
    assert "VP_o_VF_o_VS_HOGAR = 1" in sql["PV_hogar_escuela1"]
    assert "COALESCE(VS_12M, 0)" in sql["PV_indice_acum_VS"]
    assert "THEN NULL" in sql["CONS_ALGUNA"]
    assert "CONS_ALGUNA IS NULL THEN NULL" in sql["CONS_ATENCION_SALUD"]


def test_stage35_model_uses_only_prior_shadow_dependencies():
    model = render_model()
    for section in ["32", "33", "34"]:
        assert f'${{ref("analytical_crs04_stage{section}_v0_5")}}' in model
    assert '${ref("analytical_crs04_adolescents")}' not in model
    assert DEPENDENCIES["household"] == ["VP_HOGAR", "VF_HOGAR", "VP_o_VF_HOGAR"]


def test_stage35_quality_has_distinct_binary_count_and_nullable_checks():
    _, blocks = build_stage35_contract()
    quality = render_quality_assertion()
    binary = binary_non_null_columns(blocks)
    assert len(binary) == 35
    assert "accumulation_ranges" in quality
    assert "consequence_ranges" in quality
    assert "PV_indice_acum NOT BETWEEN 0 AND 4" in quality
    assert "CONS_NUM_CONSECUENCIAS NOT BETWEEN 0 AND 6" in quality
    assert "`CONS_ALGUNA` IS NULL" not in quality


def test_stage35_parity_assertion_covers_every_output():
    _, blocks = build_stage35_contract()
    parity = render_parity_assertion()
    assert '${ref("analytical_crs04_adolescents")}' in parity
    for column in output_columns(blocks):
        assert f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`" in parity
