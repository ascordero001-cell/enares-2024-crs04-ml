from __future__ import annotations

from enares.stage04.catalog_navigation import CatalogLocator, filter_catalog

FROZEN_LOCATORS = (
    CatalogLocator("3.1", "SYN_C0_31_001", "Normas repetidas sobre cuidado (hogar)", "Nacional", "Total"),
    CatalogLocator("3.2", "SYN_C0_32_001", "Violencia física en el hogar: episodio repetido (12 meses)", "Nacional", "Total"),
    CatalogLocator("3.3", "SYN_C0_33_001", "Violencia psicológica en la escuela: episodio repetido (12 meses)", "Nacional", "Total"),
    CatalogLocator("3.4", "SYN_C0_34_001", "Situación sintética de violencia sexual (alguna vez)", "Nacional", "Total"),
    CatalogLocator("3.5", "SYN_C0_35_001", "Consecuencias físicas acumuladas (tres o más)", "Nacional", "Total"),
    CatalogLocator("3.6", "SYN_C0_36_001", "Búsqueda de ayuda después de un episodio (persona adulta)", "Nacional", "Total"),
    CatalogLocator("3.2", "SYN_C0_DEP_001", "Violencia física en el hogar: episodio repetido (12 meses)", "Departamento", "Departamento sintético 07"),
    CatalogLocator("3.2", "SYN_C0_DISTRACTOR_01", "Violencia física en el hogar: episodio repetido (alguna vez)", "Nacional", "Total"),
    CatalogLocator("3.5", "SYN_C0_DISTRACTOR_02", "Consecuencias físicas acumuladas (una o más)", "Nacional", "Total"),
)

FROZEN_TASKS = (
    ("3.1", "Nacional", "cuidado hogar", "SYN_C0_31_001"),
    ("3.2", "Nacional", "fisica 12 meses", "SYN_C0_32_001"),
    ("3.3", "Nacional", "psicologica escuela 12 meses", "SYN_C0_33_001"),
    ("3.4", "Nacional", "sexual alguna vez", "SYN_C0_34_001"),
    ("3.5", "Nacional", "consecuencias tres", "SYN_C0_35_001"),
    ("3.6", "Nacional", "ayuda persona adulta", "SYN_C0_36_001"),
    ("3.2", "Departamento", "fisica sintetico 07", "SYN_C0_DEP_001"),
)


def test_c0_frozen_tasks_resolve_one_synthetic_locator_each():
    for module_id, dimension, query, expected in FROZEN_TASKS:
        matches = filter_catalog(
            FROZEN_LOCATORS,
            module_id=module_id,
            dimension=dimension,
            query=query,
        )
        assert [row.indicator_id for row in matches] == [expected]


def test_c0_covers_six_modules_and_one_departmental_task():
    assert {task[0] for task in FROZEN_TASKS} == {"3.1", "3.2", "3.3", "3.4", "3.5", "3.6"}
    assert sum(task[1] == "Departamento" for task in FROZEN_TASKS) == 1


def test_c0_rejects_any_non_synthetic_locator():
    real = CatalogLocator("3.1", "REAL", "No permitido", "Nacional", "Total", synthetic=False)
    try:
        filter_catalog([real], module_id="3.1", dimension="Nacional", query="permitido")
    except ValueError as error:
        assert "synthetic=true" in str(error)
    else:
        raise AssertionError("C0 must reject non-synthetic locators")


def test_c0_search_is_accent_and_case_insensitive():
    matches = filter_catalog(
        FROZEN_LOCATORS,
        module_id="3.3",
        dimension="Nacional",
        query="PSICOLOGICA ESCUELA",
    )
    assert [row.indicator_id for row in matches] == ["SYN_C0_33_001"]
