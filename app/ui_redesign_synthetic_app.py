"""Synthetic-only Streamlit structure for the Stage 04 UI redesign."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.views.ui_redesign_synthetic import (
    STATE_LABELS,
    SYNTHETIC_RESULTS,
    filter_synthetic_results,
    forest_record,
    state_code,
    table_record,
)


def _render_state(row) -> None:
    state = state_code(row)
    label = STATE_LABELS[state]
    message = f"{row.module_id} · {row.category} — {label}"
    if state == "PUBLISHABLE_SHADOW":
        st.success(message)
    elif state in {"REFERENCE_HIGH_CV", "SMALL_N", "REFERENCE_HIGH_CV_AND_SMALL_N"}:
        st.warning(message)
    elif state == "SUPPRESSED":
        st.error(message)
        st.caption("Los campos estadísticos protegidos no llegan a esta vista.")
    else:
        st.info(message)


def render() -> None:
    st.set_page_config(
        page_title="ENARES · rediseño sintético",
        page_icon="◉",
        layout="wide",
    )
    st.caption("ENARES 2024 · CONTROLLED_SHADOW")
    st.title("Rediseño de la vigilancia poblacional")
    st.warning(
        "Estructura 100 % sintética: no contiene cifras V0, no consulta BigQuery y no es una "
        "publicación institucional."
    )

    module_options = ("Todos", *dict.fromkeys(row.module_id for row in SYNTHETIC_RESULTS))
    dimension_options = (
        "Todas",
        *dict.fromkeys(row.dimension for row in SYNTHETIC_RESULTS),
    )
    state_options = tuple(STATE_LABELS)

    st.sidebar.header("Filtros sintéticos")
    module_id = st.sidebar.selectbox("Módulo", module_options)
    dimension = st.sidebar.selectbox("Dimensión", dimension_options)
    states = tuple(
        st.sidebar.multiselect(
            "Estados visibles",
            state_options,
            default=state_options,
            format_func=lambda value: STATE_LABELS[value],
        )
    )
    st.sidebar.caption("Opciones limitadas al fixture sintético versionado.")
    st.sidebar.caption("Exportación agregada real: sin cambios; no se ejecuta desde esta maqueta.")

    rows = filter_synthetic_results(
        module_id=module_id,
        dimension=dimension,
        states=states,
    )
    overview, table, forest, states_tab = st.tabs(
        ("Panorama", "Tabla", "Forest plot", "Estados")
    )

    with overview:
        a, b, c = st.columns(3)
        a.metric("Resultados visibles", len(rows))
        b.metric("Módulos", len({row.module_id for row in rows}))
        c.metric(
            "Alertas de precisión",
            sum(row.cv_flag or row.n_flag for row in rows),
        )
        st.info(
            "Los filtros solo cambian la presentación del fixture; no crean cruces ni "
            "recalculan indicadores."
        )

    with table:
        if rows:
            st.dataframe(
                [table_record(row) for row in rows],
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.info("No hay resultados sintéticos para esta combinación de filtros.")

    with forest:
        forest_rows = [record for row in rows if (record := forest_record(row))]
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
            st.caption("Puntos e intervalos completamente sintéticos.")
        else:
            st.info("Esta selección no contiene estadísticas aptas para el forest plot.")

    with states_tab:
        if not rows:
            st.info("No hay estados sintéticos para esta combinación de filtros.")
        for row in rows:
            with st.container(border=True):
                _render_state(row)

    st.divider()
    st.caption(
        "V0 continúa oficial · acceso público, publicación y cutover: NOT_AUTHORIZED"
    )


if __name__ == "__main__":
    render()
