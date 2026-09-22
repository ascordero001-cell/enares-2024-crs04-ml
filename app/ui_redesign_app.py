"""Authorized-data implementation of the Stage 04 visual contract."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.streamlit_app import configured_repositories
from app.views.ui_redesign_real import (
    STATE_LABELS,
    AuthorizedRedesignResult,
    forest_record,
    load_authorized_results,
    numeric_card,
    table_record,
)
from app.views.ui_visual_components import (
    inject_visual_css,
    render_header,
    render_indicator_sheet,
    render_module_strip,
    render_quality_legend,
    render_release_history,
    render_scope_banner,
)
from enares.stage04.indicator_labels import MODULE_LABELS, indicator_option_label
from enares.stage04.repository import RepositoryError

DIMENSION_FILTERS = (
    ("Departamento", "Todos"),
    ("Área", "Todas"),
    ("Sexo", "Todos"),
    ("Área × sexo", "Todos"),
    ("Idioma del hogar", "Todos"),
    ("Etnicidad", "Todas"),
    ("Tipo de hogar", "Todos"),
    ("Discapacidad", "Todas"),
)

VIEW_LABELS = (
    "Resumen nacional",
    "Módulo 3.1",
    "Módulo 3.2",
    "Módulo 3.3",
    "Módulo 3.4",
    "Módulo 3.5",
    "Módulo 3.6",
    "Brechas",
    "Calidad y notas",
    "Estado del gate",
    "Historial",
)


def _initial_view() -> str:
    value = st.query_params.get("view", VIEW_LABELS[0])
    return value if value in VIEW_LABELS else VIEW_LABELS[0]


def _sync_view_query() -> None:
    selected = st.session_state.get("stage04_view")
    if selected in VIEW_LABELS:
        st.query_params["view"] = selected
        if selected.startswith("Módulo "):
            st.session_state["real_module_filter"] = selected.removeprefix("Módulo ")


def _sync_module_view() -> None:
    """Keep the active view, title and URL aligned with the module filter."""
    selected = st.session_state.get("real_module_filter")
    view = f"Módulo {selected}" if selected in MODULE_LABELS else "Resumen nacional"
    st.session_state["stage04_view"] = view
    st.query_params["view"] = view


def _valid_session_value(key: str, options: tuple[str, ...], fallback: str) -> None:
    if st.session_state.get(key) not in options:
        st.session_state[key] = fallback


def _dimension_filter_selection(
    rows: list[AuthorizedRedesignResult],
) -> tuple[str, str | None]:
    """Expose approved dimensions while allowing only one active cut."""
    options_by_dimension: dict[str, tuple[str, ...]] = {}
    for dimension, default in DIMENSION_FILTERS:
        categories = tuple(
            dict.fromkeys(
                result.row.category
                for result in rows
                if result.row.disaggregation == dimension
            )
        )
        options_by_dimension[dimension] = (default, *categories)
        _valid_session_value(
            f"real_filter_{dimension}", options_by_dimension[dimension], default
        )

    active_dimension = next(
        (
            dimension
            for dimension, default in DIMENSION_FILTERS
            if st.session_state.get(f"real_filter_{dimension}", default) != default
        ),
        None,
    )
    selected_values: dict[str, str] = {}
    for dimension, default in DIMENSION_FILTERS:
        selected_values[dimension] = st.selectbox(
            dimension,
            options_by_dimension[dimension],
            key=f"real_filter_{dimension}",
            disabled=active_dimension is not None and active_dimension != dimension,
        )

    active_dimension = next(
        (
            dimension
            for dimension, default in DIMENSION_FILTERS
            if selected_values[dimension] != default
        ),
        None,
    )
    if active_dimension is None:
        return "Nacional", None
    return active_dimension, selected_values[active_dimension]


def _filter_results(
    results: list[AuthorizedRedesignResult],
    *,
    module_id: str,
    dimension: str,
    category_filter: str | None,
    states: tuple[str, ...],
    indicator_id: str,
    category: str,
) -> list[AuthorizedRedesignResult]:
    """Apply one effective selection without constructing absent combinations."""
    return [
        result
        for result in results
        if (module_id == "Todos" or result.row.module_id == module_id)
        and result.row.disaggregation == dimension
        and (category_filter is None or result.row.category == category_filter)
        and result.state in states
        and (indicator_id == "Todos" or result.row.indicator_id == indicator_id)
        and (category == "Todas" or result.row.category == category)
    ]


def _module_summaries(
    results: list[AuthorizedRedesignResult],
) -> list[dict[str, str]]:
    summaries: list[dict[str, str]] = []
    for module_id in MODULE_LABELS:
        rows = [result for result in results if result.row.module_id == module_id]
        summaries.append(
            {
                "code": module_id,
                "label": MODULE_LABELS[module_id],
                "indicator": f"{len({result.row.indicator_id for result in rows})} indicadores aprobados",
                "value": f"{len(rows)} filas",
                "state": "Release V0 verificado",
            }
        )
    return summaries


def _render_state(result: AuthorizedRedesignResult) -> None:
    message = (
        f"{result.row.module_id} · {result.display_name} — {STATE_LABELS[result.state]}"
    )
    if result.state == "PUBLISHABLE_SHADOW":
        st.success(message)
    elif result.state in {
        "REFERENCE_HIGH_CV",
        "SMALL_N",
        "REFERENCE_HIGH_CV_AND_SMALL_N",
    }:
        st.warning(message)
    elif result.state == "SUPPRESSED":
        st.error(message)
    else:
        st.info(message)


def _render_overview(rows: list[AuthorizedRedesignResult]) -> None:
    a, b, c = st.columns(3)
    a.metric("Resultados visibles", len(rows))
    b.metric("Indicadores", len({result.row.indicator_id for result in rows}))
    c.metric(
        "Alertas de precisión",
        sum(bool(result.row.cv_flag or result.row.n_flag) for result in rows),
    )
    st.info("Los filtros presentan únicamente combinaciones existentes en V0.")


def _render_table(rows: list[AuthorizedRedesignResult]) -> None:
    if rows:
        st.dataframe(
            [table_record(result) for result in rows],
            hide_index=True,
            width="stretch",
        )
    else:
        st.info("No hay resultados autorizados para esta combinación de filtros.")


def _render_forest(rows: list[AuthorizedRedesignResult], *, indicator_id: str) -> None:
    if indicator_id == "Todos":
        st.info("Selecciona un indicador para mostrar el forest plot.")
        return
    forest_rows = [record for result in rows if (record := forest_record(result))]
    if not forest_rows:
        st.info("Esta selección no contiene estadísticas aptas para el forest plot.")
        return
    st.vega_lite_chart(
        forest_rows,
        {
            "layer": [
                {
                    "mark": {"type": "rule", "strokeWidth": 3},
                    "encoding": {
                        "y": {"field": "label", "type": "nominal", "title": None},
                        "x": {
                            "field": "lower",
                            "type": "quantitative",
                            "title": "Porcentaje",
                            "scale": {"domain": [0, 100]},
                        },
                        "x2": {"field": "upper"},
                        "tooltip": ["label", "estimate", "lower", "upper", "state"],
                    },
                },
                {
                    "mark": {"type": "point", "filled": True, "size": 90},
                    "encoding": {
                        "y": {"field": "label", "type": "nominal", "title": None},
                        "x": {
                            "field": "estimate",
                            "type": "quantitative",
                            "scale": {"domain": [0, 100]},
                        },
                        "color": {
                            "field": "state",
                            "type": "nominal",
                            "title": "Estado",
                        },
                        "tooltip": ["label", "estimate", "lower", "upper", "state"],
                    },
                },
            ]
        },
        width="stretch",
    )


def _render_detail(result: AuthorizedRedesignResult) -> None:
    card = numeric_card(result)
    if card is None:
        _render_state(result)
        st.caption(result.row.quality_note)
        return
    st.subheader(result.display_name)
    st.caption(f"Código: {result.row.indicator_id}")
    estimate, error, cv, sample = st.columns(4)
    estimate.metric("Estimación", str(card["estimate_text"]))
    error.metric("Error estándar", str(card["standard_error_text"]))
    cv.metric("CV", str(card["cv_text"]).replace("CV ", ""))
    sample.metric("N no ponderado", str(card["n_text"]).replace("N no ponderado: ", ""))
    st.write(card["interval_text"])
    _render_state(result)
    st.caption(card["quality_note"])
    st.text(card["universe_text"])
    st.caption(card["denominator_text"])


def render() -> None:
    st.set_page_config(
        page_title="ENARES · vigilancia poblacional",
        page_icon="◉",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_visual_css()

    try:
        repository, _ = configured_repositories()
        results = load_authorized_results(repository)
    except (RepositoryError, OSError, TypeError, ValueError):
        st.error("La fuente agregada autorizada no superó la validación.")
        return

    release_ids = {result.row.release_id for result in results}
    run_ids = {result.row.run_id for result in results}
    release_label = (
        next(iter(release_ids)) if len(release_ids) == 1 else "RELEASE NO ÚNICO"
    )
    render_header(
        release_label=release_label,
        subtitle="Catálogo V0 autorizado · acceso autenticado en shadow.",
    )
    render_scope_banner(
        "CONTROLLED_SHADOW: 516 indicadores y 3,014 filas agregadas verificadas. "
        "Sin microdatos, recálculo, cruces nuevos, publicación ni cutover."
    )
    render_module_strip(
        _module_summaries(results),
        caption="COBERTURA DEL CATÁLOGO V0 POR MÓDULO",
        metric_label="Cobertura",
    )

    module_options = ("Todos", *MODULE_LABELS)
    state_options = tuple(STATE_LABELS)
    initial_view = _initial_view()
    if "stage04_view" not in st.session_state:
        st.session_state["stage04_view"] = initial_view
    if "real_module_filter" not in st.session_state:
        st.session_state["real_module_filter"] = (
            initial_view.removeprefix("Módulo ")
            if initial_view.startswith("Módulo ")
            else "Todos"
        )
    _valid_session_value("real_module_filter", module_options, "Todos")

    with st.container(key="stage04_layout"):
        left, center, right = st.columns((270, 800, 272), gap="medium")
        with left, st.container(key="stage04_left_rail"):
            st.subheader("Filtros V0")
            module_id = st.selectbox(
                "Módulo",
                module_options,
                key="real_module_filter",
                on_change=_sync_module_view,
                format_func=lambda value: (
                    "Todos" if value == "Todos" else f"{value} · {MODULE_LABELS[value]}"
                ),
            )
            module_rows = [
                result
                for result in results
                if module_id == "Todos" or result.row.module_id == module_id
            ]
            dimension, category_filter = _dimension_filter_selection(module_rows)
            states = tuple(
                st.multiselect(
                    "Estados visibles",
                    state_options,
                    default=state_options,
                    format_func=lambda value: STATE_LABELS[value],
                    key="real_state_filter",
                )
            )
            dimension_rows = [
                result
                for result in module_rows
                if result.row.disaggregation == dimension
                and (category_filter is None or result.row.category == category_filter)
                and result.state in states
            ]
            indicator_options = (
                "Todos",
                *dict.fromkeys(result.row.indicator_id for result in dimension_rows),
            )
            _valid_session_value("real_indicator_filter", indicator_options, "Todos")
            option_by_id = {
                result.row.indicator_id: indicator_option_label(
                    result.row.indicator_id, result.row.module_id
                )
                for result in dimension_rows
            }
            indicator_id = st.selectbox(
                "Indicador",
                indicator_options,
                key="real_indicator_filter",
                format_func=lambda value: (
                    "Todos" if value == "Todos" else option_by_id[value]
                ),
            )
            indicator_rows = [
                result
                for result in dimension_rows
                if indicator_id == "Todos" or result.row.indicator_id == indicator_id
            ]
            category_options = (
                "Todas",
                *dict.fromkeys(result.row.category for result in indicator_rows),
            )
            _valid_session_value("real_category_filter", category_options, "Todas")
            category = st.selectbox(
                "Categoría", category_options, key="real_category_filter"
            )
            st.caption("Una sola desagregación activa; no se fabrican cruces.")
            with st.container(border=True):
                st.caption("COBERTURA DE LA SELECCIÓN")
                st.write(f"{len(indicator_rows)} fila(s) antes de categoría")
                st.write(
                    f"{len({row.row.indicator_id for row in indicator_rows})} indicador(es)"
                )

        rows = _filter_results(
            results,
            module_id=module_id,
            dimension=dimension,
            category_filter=category_filter,
            states=states,
            indicator_id=indicator_id,
            category=category,
        )

        with center, st.container(key="stage04_center"):
            selected_view = st.segmented_control(
                "Vista",
                VIEW_LABELS,
                selection_mode="single",
                required=True,
                key="stage04_view",
                on_change=_sync_view_query,
                label_visibility="collapsed",
                width="stretch",
            )
            active_view = selected_view or VIEW_LABELS[0]
            if active_view == "Resumen nacional":
                _render_overview(rows)
                _render_table(rows)
                _render_forest(rows, indicator_id=indicator_id)
            elif active_view.startswith("Módulo "):
                st.subheader(active_view)
                _render_table(rows)
                _render_forest(rows, indicator_id=indicator_id)
            elif active_view == "Brechas":
                st.subheader("Brechas")
                st.info(
                    "La vista presenta agregados V0 existentes; no calcula diferencias nuevas."
                )
                _render_table(rows)
            elif active_view == "Calidad y notas":
                render_quality_legend(synthetic=False)
                for result in rows:
                    _render_state(result)
            elif active_view == "Estado del gate":
                st.subheader("Estado del gate")
                st.warning(
                    "Integración autorizada en shadow · despliegue y cambio de tráfico "
                    "requieren aprobación separada."
                )
            else:
                run_label = (
                    next(iter(run_ids)) if len(run_ids) == 1 else "múltiples runs"
                )
                render_release_history(
                    message=(
                        f"Release vigente: {release_label} · run: {run_label}. "
                        "Sin publicación ni cutover."
                    )
                )

        with right, st.container(key="stage04_right_rail"):
            st.subheader("Alertas y hallazgos")
            flagged = [
                result
                for result in rows
                if result.row.cv_flag or result.row.n_flag or result.row.suppress_flag
            ]
            if rows and not flagged:
                st.success("Sin alertas en la selección.")
            elif not rows:
                st.info("No hay alertas ni indicador activo para esta selección.")
            for result in flagged:
                _render_state(result)
            if len(rows) == 1:
                active = rows[0]
                _render_detail(active)
                render_indicator_sheet(
                    {
                        "Módulo": (
                            f"{active.row.module_id} · "
                            f"{MODULE_LABELS[active.row.module_id]}"
                        ),
                        "Indicador": active.display_name,
                        "Código": active.row.indicator_id,
                        "Dimensión": active.row.disaggregation,
                        "Categoría": active.row.category,
                        "Estado": STATE_LABELS[active.state],
                    }
                )
            elif rows:
                st.info("Elige un indicador y una categoría para abrir su ficha.")
            st.subheader("Exportar")
            st.button("Descargar corte visible", disabled=True)
            st.caption("La exportación se habilitará solo con el flujo ya autorizado.")

    st.divider()
    st.caption(
        "V0 continúa oficial · acceso público, publicación y cutover: NOT_AUTHORIZED"
    )


if __name__ == "__main__":
    render()
