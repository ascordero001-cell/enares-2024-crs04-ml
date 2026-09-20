"""Authorized-data Streamlit entry point for Stage 04 UI redesign Etapa 3."""

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
    filter_authorized_results,
    forest_record,
    load_authorized_results,
    numeric_card,
    table_record,
)
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


def _default_index(options: tuple[str, ...], preferred: str) -> int:
    return options.index(preferred) if preferred in options else 0


def _dimension_filter_selection(
    module_rows: list[AuthorizedRedesignResult],
) -> tuple[str, str | None]:
    """Render one-control-per-dimension without enabling dynamic crosses."""
    options_by_dimension: dict[str, tuple[str, ...]] = {}
    for dimension, default in DIMENSION_FILTERS:
        categories = tuple(
            dict.fromkeys(
                result.row.category
                for result in module_rows
                if result.row.disaggregation == dimension
            )
        )
        options_by_dimension[dimension] = (default, *categories)
        key = f"redesign_filter_{dimension}"
        if st.session_state.get(key, default) not in options_by_dimension[dimension]:
            st.session_state[key] = default

    active_dimension = next(
        (
            dimension
            for dimension, default in DIMENSION_FILTERS
            if st.session_state.get(f"redesign_filter_{dimension}", default) != default
        ),
        None,
    )
    selected_values: dict[str, str] = {}
    for dimension, default in DIMENSION_FILTERS:
        selected_values[dimension] = st.sidebar.selectbox(
            dimension,
            options_by_dimension[dimension],
            key=f"redesign_filter_{dimension}",
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


def _render_detail(result: AuthorizedRedesignResult) -> None:
    card = numeric_card(result)
    if card is None:
        st.info(STATE_LABELS[result.state])
        st.caption(result.row.quality_note)
        return
    st.subheader("Detalle del agregado seleccionado")
    st.caption(
        f"{card['indicator_id']} · {card['disaggregation']} / {card['category_display']}"
    )
    estimate, error, cv, sample = st.columns(4)
    estimate.metric("Estimación", str(card["estimate_text"]))
    error.metric("Error estándar", str(card["standard_error_text"]))
    cv.metric("CV", str(card["cv_text"]).replace("CV ", ""))
    sample.metric("N no ponderado", str(card["n_text"]).replace("N no ponderado: ", ""))
    st.write(card["interval_text"])
    if result.row.cv_flag or result.row.n_flag:
        st.warning(STATE_LABELS[result.state])
    else:
        st.success(STATE_LABELS[result.state])
    st.caption(card["quality_note"])
    st.text(card["universe_text"])
    st.caption(card["denominator_text"])


def render() -> None:
    st.set_page_config(
        page_title="ENARES · rediseño conectado",
        page_icon="◉",
        layout="wide",
    )
    st.caption("ENARES 2024 · CONTROLLED_SHADOW · V0 AUTORIZADO")
    st.title("Vigilancia poblacional de violencia")
    st.warning(
        "No es una publicación institucional. La interfaz consume únicamente agregados "
        "verificados; no recalcula Stage 03 ni permite búsquedas individuales."
    )

    try:
        repository, _ = configured_repositories()
        results = load_authorized_results(repository)
    except (RepositoryError, OSError, TypeError, ValueError):
        st.error("La fuente agregada autorizada no superó la validación.")
        return

    module_options = tuple(dict.fromkeys(result.row.module_id for result in results))
    st.sidebar.header("Filtros autorizados")
    module_id = st.sidebar.selectbox(
        "Módulo",
        module_options,
        index=_default_index(module_options, "3.2"),
    )
    module_rows = [result for result in results if result.row.module_id == module_id]
    dimension, category_filter = _dimension_filter_selection(module_rows)
    dimension_rows = [
        result
        for result in module_rows
        if result.row.disaggregation == dimension
        and (category_filter is None or result.row.category == category_filter)
    ]
    indicator_options = tuple(
        dict.fromkeys(result.row.indicator_id for result in dimension_rows)
    )
    indicator_id = st.sidebar.selectbox(
        "Indicador",
        indicator_options,
        index=_default_index(indicator_options, "VF_HOGAR"),
    )
    state_options = tuple(STATE_LABELS)
    states = tuple(
        st.sidebar.multiselect(
            "Estados visibles",
            state_options,
            default=state_options,
            format_func=lambda value: STATE_LABELS[value],
        )
    )
    st.sidebar.caption("Opciones derivadas de filas verificadas del release actual.")
    st.sidebar.caption("Publicación y cutover: NOT_AUTHORIZED")

    selected = filter_authorized_results(
        results,
        module_id=module_id,
        dimension=dimension,
        indicator_id=indicator_id,
        states=states,
        category=category_filter,
    )
    overview, table, forest, states_tab = st.tabs(
        ("Panorama", "Tabla", "Forest plot", "Estados")
    )

    with overview:
        release_ids = {result.row.release_id for result in selected}
        a, b, c = st.columns(3)
        a.metric("Resultados visibles", len(selected))
        b.metric("Release", next(iter(release_ids)) if len(release_ids) == 1 else "—")
        c.metric(
            "Alertas de precisión",
            sum(bool(result.row.cv_flag or result.row.n_flag) for result in selected),
        )
        if not selected:
            st.info("No hay resultados autorizados para esta combinación de filtros.")
        elif len(selected) == 1:
            _render_detail(selected[0])
        else:
            categories = tuple(result.row.category for result in selected)
            category = st.selectbox("Categoría para detalle", categories)
            detail = [result for result in selected if result.row.category == category]
            if len(detail) != 1:
                st.error("La combinación autorizada no está disponible de forma única.")
            else:
                _render_detail(detail[0])

    with table:
        if selected:
            st.dataframe(
                [table_record(result) for result in selected],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No hay filas autorizadas para mostrar.")

    with forest:
        forest_rows = [
            record for result in selected if (record := forest_record(result))
        ]
        if forest_rows:
            st.vega_lite_chart(
                forest_rows,
                {
                    "layer": [
                        {
                            "mark": {"type": "rule", "strokeWidth": 3},
                            "encoding": {
                                "y": {"field": "label", "type": "nominal", "title": None},
                                "x": {"field": "lower", "type": "quantitative", "title": "Porcentaje", "scale": {"domain": [0, 100]}},
                                "x2": {"field": "upper"},
                                "tooltip": ["label", "estimate", "lower", "upper", "state"],
                            },
                        },
                        {
                            "mark": {"type": "point", "filled": True, "size": 90},
                            "encoding": {
                                "y": {"field": "label", "type": "nominal", "title": None},
                                "x": {"field": "estimate", "type": "quantitative", "scale": {"domain": [0, 100]}},
                                "color": {"field": "state", "type": "nominal", "title": "Estado"},
                                "tooltip": ["label", "estimate", "lower", "upper", "state"],
                            },
                        },
                    ]
                },
                use_container_width=True,
            )
        else:
            st.info("Esta selección no contiene estadísticas aptas para el forest plot.")

    with states_tab:
        if not selected:
            st.info("No hay estados autorizados para esta selección.")
        for result in selected:
            with st.container(border=True):
                st.write(f"{result.row.category} — {STATE_LABELS[result.state]}")
                st.caption(result.row.quality_note)

    st.divider()
    st.caption(
        "V0 continúa oficial · acceso público, publicación y cutover: NOT_AUTHORIZED"
    )


if __name__ == "__main__":
    render()
