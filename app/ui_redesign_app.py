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


def _default_index(options: tuple[str, ...], preferred: str) -> int:
    return options.index(preferred) if preferred in options else 0


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
    dimension_options = tuple(
        dict.fromkeys(result.row.disaggregation for result in module_rows)
    )
    dimension = st.sidebar.selectbox(
        "Dimensión",
        dimension_options,
        index=_default_index(dimension_options, "Nacional"),
    )
    dimension_rows = [
        result for result in module_rows if result.row.disaggregation == dimension
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
