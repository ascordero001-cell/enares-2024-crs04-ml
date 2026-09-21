"""Synthetic-only Streamlit implementation of the Stage 04 visual contract."""

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
from app.views.ui_visual_components import (
    inject_visual_css,
    render_header,
    render_indicator_sheet,
    render_module_strip,
    render_quality_legend,
    render_release_history,
    render_scope_banner,
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


def _render_state(row) -> None:
    state = state_code(row)
    message = f"{row.module_id} · {row.category} — {STATE_LABELS[state]}"
    if state == "PUBLISHABLE_SHADOW":
        st.success(message)
    elif state in {"REFERENCE_HIGH_CV", "SMALL_N", "REFERENCE_HIGH_CV_AND_SMALL_N"}:
        st.warning(message)
    elif state == "SUPPRESSED":
        st.error(message)
        st.caption("Los campos estadísticos protegidos no llegan a esta vista.")
    else:
        st.info(message)


def _module_summaries() -> list[dict[str, str]]:
    summaries: list[dict[str, str]] = []
    for module_id in ("3.1", "3.2", "3.3", "3.4", "3.5", "3.6"):
        candidates = [row for row in SYNTHETIC_RESULTS if row.module_id == module_id]
        numeric = next((row for row in candidates if row.estimate is not None), None)
        exemplar = numeric or candidates[0]
        summaries.append(
            {
                "code": module_id,
                "label": exemplar.module_label,
                "indicator": exemplar.indicator,
                "value": f"{numeric.estimate:.1f} %" if numeric else "Contexto",
                "state": STATE_LABELS[state_code(exemplar)],
            }
        )
    return summaries


def _render_overview(rows) -> None:
    a, b, c = st.columns(3)
    a.metric("Resultados visibles", len(rows))
    b.metric("Módulos", len({row.module_id for row in rows}))
    c.metric("Alertas de precisión", sum(row.cv_flag or row.n_flag for row in rows))
    st.info(
        "Los filtros solo presentan el fixture; no crean cruces ni recalculan indicadores."
    )


def _render_table(rows) -> None:
    if rows:
        st.dataframe(
            [table_record(row) for row in rows], hide_index=True, width="stretch"
        )
    else:
        st.info("No hay resultados sintéticos para esta combinación de filtros.")


def _render_forest(rows) -> None:
    forest_rows = [record for row in rows if (record := forest_record(row))]
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
                        "tooltip": [
                            "label",
                            "estimate",
                            "lower",
                            "upper",
                            "state",
                        ],
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
                        "tooltip": [
                            "label",
                            "estimate",
                            "lower",
                            "upper",
                            "state",
                        ],
                    },
                },
            ]
        },
        width="stretch",
    )
    st.caption("Puntos e intervalos completamente sintéticos.")


def _render_states(rows) -> None:
    if not rows:
        st.info("No hay estados sintéticos para esta combinación de filtros.")
    for row in rows:
        with st.container(border=True):
            _render_state(row)


def render() -> None:
    st.set_page_config(
        page_title="ENARES · rediseño sintético",
        page_icon="◉",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_visual_css()
    render_header(
        release_label="CONTROLLED_SHADOW · FIXTURE",
        subtitle="Composición sintética para validar la paridad visual antes de conectar V0.",
    )
    render_scope_banner(
        "Estructura 100 % sintética: no contiene cifras V0, no consulta BigQuery y no es una publicación institucional."
    )
    render_module_strip(_module_summaries())

    module_options = (
        "Todos",
        *dict.fromkeys(row.module_id for row in SYNTHETIC_RESULTS),
    )
    state_options = tuple(STATE_LABELS)

    with st.container(key="stage04_layout"):
        left, center, right = st.columns((270, 800, 272), gap="medium")
        with left, st.container(key="stage04_left_rail"):
            st.subheader("Filtros sintéticos")
            module_id = st.selectbox("Módulo", module_options)
            module_rows = [
                row
                for row in SYNTHETIC_RESULTS
                if module_id == "Todos" or row.module_id == module_id
            ]
            dimension_options = (
                "Todas",
                *dict.fromkeys(row.dimension for row in module_rows),
            )
            dimension = st.selectbox("Dimensión", dimension_options)
            states = tuple(
                st.multiselect(
                    "Estados visibles",
                    state_options,
                    default=state_options,
                    format_func=lambda value: STATE_LABELS[value],
                )
            )
            candidate_rows = filter_synthetic_results(
                module_id=module_id, dimension=dimension, states=states
            )
            indicator_options = (
                "Todos",
                *dict.fromkeys(row.indicator for row in candidate_rows),
            )
            indicator = st.selectbox("Indicador", indicator_options)
            indicator_rows = [
                row
                for row in candidate_rows
                if indicator == "Todos" or row.indicator == indicator
            ]
            category_options = (
                "Todas",
                *dict.fromkeys(row.category for row in indicator_rows),
            )
            category = st.selectbox("Categoría", category_options)
            st.caption("Opciones limitadas al fixture sintético versionado.")
            st.caption("No se fabrican combinaciones ausentes.")
            with st.container(border=True):
                st.caption("COBERTURA DEL FIXTURE")
                st.write(f"{len(indicator_rows)} fila(s) antes de categoría")
                st.write(f"{len({row.module_id for row in indicator_rows})} módulo(s)")

        rows = [
            row
            for row in indicator_rows
            if category == "Todas" or row.category == category
        ]

        with center, st.container(key="stage04_center"):
            active_view = st.segmented_control(
                "Vista",
                VIEW_LABELS,
                selection_mode="single",
                default=_initial_view(),
                required=True,
                key="stage04_view",
                on_change=_sync_view_query,
                label_visibility="collapsed",
                width="stretch",
            )
            if active_view == "Resumen nacional":
                _render_overview(rows)
                _render_table(rows)
                _render_forest(rows)
            elif active_view.startswith("Módulo "):
                module_id_view = active_view.removeprefix("Módulo ")
                selected_module_rows = [
                    row for row in SYNTHETIC_RESULTS if row.module_id == module_id_view
                ]
                st.subheader(active_view)
                _render_table(selected_module_rows)
                _render_forest(selected_module_rows)
            elif active_view == "Brechas":
                st.subheader("Brechas")
                st.info(
                    "Vista estructural sintética. No calcula diferencias entre cifras V0."
                )
            elif active_view == "Calidad y notas":
                render_quality_legend()
                _render_states(rows)
            elif active_view == "Estado del gate":
                st.subheader("Estado del gate")
                st.warning(
                    "Gate 2 en preparación · datos reales y cloud permanecen bloqueados."
                )
            else:
                render_release_history()

        active = rows[0] if rows else SYNTHETIC_RESULTS[0]
        with right, st.container(key="stage04_right_rail"):
            st.subheader("Alertas y hallazgos")
            flagged = [
                row for row in rows if row.cv_flag or row.n_flag or row.suppress_flag
            ]
            if not flagged:
                st.success("Sin alertas en la selección sintética.")
            for row in flagged:
                _render_state(row)
            render_indicator_sheet(
                {
                    "Módulo": active.module_id,
                    "Indicador": active.indicator,
                    "Dimensión": active.dimension,
                    "Categoría": active.category,
                    "Estado": STATE_LABELS[state_code(active)],
                }
            )
            st.subheader("Exportar")
            st.button("Descargar corte visible", disabled=True)
            st.caption("Deshabilitado en el fixture sintético de composición.")

    st.divider()
    st.caption(
        "V0 continúa oficial · acceso público, publicación y cutover: NOT_AUTHORIZED"
    )


if __name__ == "__main__":
    render()
