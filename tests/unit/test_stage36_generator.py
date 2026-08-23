from scripts.generate_stage36_dataform import (
    PEOPLE,
    build_stage36_contract,
    output_columns,
    render_model,
    render_parity_assertion,
    render_quality_assertion,
)


def expressions() -> dict[str, str]:
    _, blocks = build_stage36_contract()
    return {name: sql for _, block in blocks for name, sql in block.items()}


def test_stage36_contract_matches_authority_counts():
    raw_inputs, blocks = build_stage36_contract()
    assert len(blocks) == 4
    assert [len(block) for _, block in blocks] == [52, 6, 33, 3]
    assert len(output_columns(blocks)) == 94
    assert len(set(output_columns(blocks))) == 94
    assert {"C3P209", "C3P237_21", "C4P253_21", "C4P260_4"}.issubset(raw_inputs)
    assert len(PEOPLE) == 16


def test_stage36_contract_preserves_domain_and_missing_rules():
    sql = expressions()
    assert sql["busco_ayuda_hogar"] == (
        "CASE WHEN C3P209 = 1 THEN 1 WHEN C3P209 = 2 THEN 0 END"
    )
    assert "C3P211 = 3 THEN NULL" in sql["recibio_ayuda_hogar_victimas"]
    assert "C4P254 = 3 THEN NULL" in sql["recibio_ayuda_vs_victimas"]
    assert "C4P252 IN (1,2)" in sql["ayuda_vs_familiar"]


def test_stage36_model_uses_only_prior_shadow_dependencies():
    model = render_model()
    for section in ["32", "33", "34"]:
        assert f'${{ref("analytical_crs04_stage{section}_v0_5")}}' in model
    assert '${ref("analytical_crs04_adolescents")}' not in model
    assert "block_04_36_ayuda_vs_derivados" in model


def test_stage36_quality_allows_nulls_but_rejects_nonbinary_values():
    _, blocks = build_stage36_contract()
    quality = render_quality_assertion()
    assert "binary_domains" in quality
    for column in output_columns(blocks):
        assert f"`{column}` NOT IN (0, 1)" in quality
        assert f"`{column}` IS NULL" not in quality


def test_stage36_parity_assertion_covers_every_output():
    _, blocks = build_stage36_contract()
    parity = render_parity_assertion()
    assert '${ref("analytical_crs04_adolescents")}' in parity
    for column in output_columns(blocks):
        assert f"candidate.`{column}` IS DISTINCT FROM reference.`{column}`" in parity
