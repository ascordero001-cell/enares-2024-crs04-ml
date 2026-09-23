from pathlib import Path

from streamlit.testing.v1 import AppTest

from app.streamlit_app import local_repositories
from app.views.stage04_dashboard import (
    build_d01_task_groups,
    d09_category_label,
    filter_estimates,
)
from enares.stage04.indicator_semantics import (
    D01_RELATIONSHIP_GROUP,
    D01_TASK_EXECUTION_GROUP,
)
from enares.stage04.validation import validate_estimates

ROOT = Path(__file__).resolve().parents[1]


def _run_application() -> AppTest:
    return AppTest.from_file(str(ROOT / "app" / "streamlit_app.py")).run(timeout=15)


def _visible_text(app: AppTest) -> str:
    groups = (
        app.caption,
        app.code,
        app.error,
        app.info,
        app.markdown,
        app.metric,
        app.subheader,
        app.text,
        app.warning,
    )
    return "\n".join(
        str(getattr(element, attribute, ""))
        for group in groups
        for element in group
        for attribute in ("value", "label")
    )


def test_local_repository_connects_the_complete_authorized_v0_counts():
    authorized, _ = local_repositories()
    expected = {"3.1": 1170, "3.2": 389, "3.3": 123, "3.4": 749, "3.5": 457, "3.6": 126}
    for module_id, count in expected.items():
        rows = authorized.list_estimates(module_id)
        validate_estimates(rows)
        assert len(rows) == count


def test_connected_module_labels_describe_the_authorized_content():
    from enares.stage04.modules import get_module

    assert get_module("3.1").label == "Roles y tareas en el hogar"
    assert get_module("3.5").label == "Acumulación y consecuencias de violencia"


def test_d01_builds_two_semantically_distinct_groups_in_approved_order():
    authorized, _ = local_repositories()
    task_execution, relationship = build_d01_task_groups(authorized)
    assert [card["category"] for card in task_execution] == [
        item.task for item in D01_TASK_EXECUTION_GROUP
    ]
    assert [card["category"] for card in relationship] == [
        item.task for item in D01_RELATIONSHIP_GROUP
    ]
    assert len(task_execution) == 7
    assert len(relationship) == 3
    assert all(
        card["quality_label"] == "Aprobado para shadow — sin alerta"
        for card in (*task_execution, *relationship)
        if card["quality_status"] == "PUBLISHABLE_CANDIDATE"
    )
    assert all("nadie" not in card["indicator_id"].lower() for card in relationship)


def test_d09_connects_domain_aliases_labels_and_visible_reference_cells():
    authorized, _ = local_repositories()
    rows = [
        row
        for row in authorized.list_estimates("3.5")
        if row.indicator_id == "CONS_ATENCION_SALUD"
    ]
    assert len(rows) == 22
    assert sum(row.cv_flag for row in rows) == 13
    assert all(not row.suppress_flag for row in rows)
    assert all("CONS_ALGUNA = 1" in row.universe for row in rows)
    assert d09_category_label("Idioma del hogar", "3") == "Quechua/Aymara"
    assert d09_category_label("Etnicidad", "6") == "No indígena ni afrodescendiente"
    assert filter_estimates(authorized, "3.5", "Departamento", "Amazonas")


def test_apptest_renders_d01_as_two_groups_and_d11_one_by_one():
    app = _run_application()
    next(select for select in app.selectbox if select.label == "Módulo").set_value(
        "3.1"
    ).run(timeout=15)
    next(
        select
        for select in app.selectbox
        if select.label == "Otra desagregación V0"
    ).set_value("Tareas del hogar").run(timeout=15)
    next(select for select in app.selectbox if select.label == "Indicador").set_value(
        "Componentes"
    ).run(timeout=15)
    visible = _visible_text(app)
    assert not app.exception
    assert "Quién realiza tareas en el hogar · ítems 1–7" in visible
    assert "Quién acompaña a la adolescente · ítems 8–10" in visible
    assert len(app.dataframe) == 2
    assert len(app.download_button) == 2

    for module_id, indicator in (
        ("3.3", "C3P223_10_1"),
        ("3.4", "Agresor_VS_12M__AG_01"),
        ("3.6", "C3P213"),
    ):
        app = _run_application()
        next(select for select in app.selectbox if select.label == "Módulo").set_value(
            module_id
        ).run(timeout=15)
        next(
            select for select in app.selectbox if select.label == "Indicador"
        ).set_value(indicator).run(timeout=15)
        assert not app.exception
        assert indicator in _visible_text(app)
        assert len(app.metric) == 4

    assert "No recibió ayuda porque no supieron cómo ayudarle" in _visible_text(app)


def test_apptest_d09_shows_approved_domain_and_no_suppression():
    app = _run_application()
    next(select for select in app.selectbox if select.label == "Módulo").set_value(
        "3.5"
    ).run(timeout=15)
    next(select for select in app.selectbox if select.label == "Indicador").set_value(
        "CONS_ATENCION_SALUD"
    ).run(timeout=15)
    visible = _visible_text(app)
    assert not app.exception
    assert "CONS_ALGUNA = 1" in visible
    assert "Los campos protegidos no llegan a la interfaz" not in visible
    assert len(app.metric) == 4
