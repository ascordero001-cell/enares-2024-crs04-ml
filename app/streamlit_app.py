"""Streamlit entry point for the local-only ENARES Stage 04 shell."""

from __future__ import annotations

import sys
from collections.abc import Iterable
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from app.config import FUTURE_DIMENSIONS, MODULES, NAVIGATION, module_for_page
from app.views.stage04_dashboard import (
    EXPORT_ENABLED,
    build_d01_task_groups,
    build_numeric_card,
    build_state_cards,
    d09_category_label,
    filter_estimates,
    load_validated_estimates,
    precision_category_label,
)
from enares.stage04.export import build_export_bundle
from enares.stage04.repository import (
    AuthorizedAggregateRepository,
    DemoRepository,
    IndicatorEstimate,
    IndicatorRepository,
)


def local_repositories():
    """Create only repositories backed by checked-in aggregate or synthetic fixtures."""
    data = ROOT / "app" / "data"
    registry = ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md"
    authorized = AuthorizedAggregateRepository(
        data / "v0_authorized_full_indicator_estimates.csv",
        data / "v0_authorized_full_indicator_estimates.manifest.json",
        registry,
    )
    demo = DemoRepository(data / "demo_indicator_estimates.csv")
    return authorized, demo


def _styles() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] { background: #102d25; }
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #f6fbf8;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] > div {
            background: #ffffff;
            color: #17251f;
        }
        [data-testid="stSidebar"] [data-baseweb="select"] input,
        [data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"],
        [data-testid="stSidebar"] [data-baseweb="select"] svg,
        [data-baseweb="popover"] [role="option"] {
            color: #17251f !important;
            fill: #17251f;
        }
        [data-testid="stSidebar"] button:disabled {
            background: #d4d9d6;
            color: #46524d !important;
            border-color: #a7b0ac;
            opacity: 1;
        }
        [data-testid="stSidebar"] :focus-visible {
            outline: 3px solid #f3c44e !important;
            outline-offset: 2px;
        }
        [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {
            opacity: 1 !important;
        }
        [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] p,
        [data-testid="stAppViewContainer"] table thead
        [data-testid="stMarkdownContainer"] p {
            color: #565f5b !important;
        }
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
            color: #f6fbf8 !important;
        }
        [data-testid="stAppViewContainer"] [data-testid="stCode"] .number {
            color: #0b6f63;
        }
        [data-testid="stAppViewContainer"] [data-testid="stAlertContentSuccess"] p {
            color: #116c2e;
        }
        [data-testid="stAppViewContainer"] [data-testid="stAlertContentWarning"] p {
            color: #765500;
        }
        [data-testid="stAppViewContainer"] [data-testid="stAlertContentError"] p {
            color: #92272b;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _header(release_id: str, created_at: str) -> None:
    st.caption("ENARES 2024 · DEMO/SHADOW")
    st.title("Vigilancia de violencia contra adolescentes")
    st.text(
        "Corte local seguro para adolescentes de 12–17 años · "
        f"Release {release_id} · {created_at}"
    )
    st.warning(
        "No es una publicación institucional. V0 continúa oficial; este prototipo "
        "no habilita búsquedas individuales ni acceso cloud. Las descargas reproducen "
        "únicamente el corte agregado V0 visible."
    )


def _numeric_summary(card: dict, heading: str | None = None) -> None:
    st.subheader(heading or "Resumen nacional · Módulo 3.2")
    st.caption(
        f"{card['indicator_id']} · {card['disaggregation']} / {card['category_display']}"
    )
    st.write(card["indicator_name"])
    a, b, c, d = st.columns(4)
    a.metric("Estimación", card["estimate_text"])
    b.metric("Error estándar", card["standard_error_text"])
    c.metric("CV", card["cv_text"].replace("CV ", ""))
    d.metric("N no ponderado", card["n_text"].replace("N no ponderado: ", ""))
    st.write(card["interval_text"])
    st.info(card["quality_label"])
    st.caption(card["quality_note"])
    st.text(card["universe_text"])
    st.caption(card["denominator_text"])


def _download_cut(rows: Iterable[IndicatorEstimate], basename: str) -> None:
    """Offer two equivalent formats only after the institutional aggregate gate."""
    if not EXPORT_ENABLED:
        return
    try:
        bundle = build_export_bundle(rows, basename=basename)
    except (ValueError, OSError, KeyError, TypeError):
        st.error("El corte no superó la validación para exportación.")
        return
    csv_column, xlsx_column = st.columns(2)
    csv_column.download_button(
        "Descargar CSV",
        data=bundle.csv_bytes,
        file_name=f"{bundle.basename}.csv",
        mime="text/csv",
        on_click="ignore",
    )
    xlsx_column.download_button(
        "Descargar Excel",
        data=bundle.xlsx_bytes,
        file_name=f"{bundle.basename}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        on_click="ignore",
    )
    st.caption(
        f"Exportación agregada: {bundle.row_count} fila(s) · mismo corte en CSV y Excel"
    )


def _state_gallery(cards: list[dict]) -> None:
    st.subheader("Estados visuales didácticos")
    columns = st.columns(3)
    for column, card in zip(columns, cards, strict=True):
        with column, st.container(border=True):
            st.caption("DEMO SINTÉTICO")
            st.subheader(card["category"])
            st.text(card["quality_label"])
            st.caption(card["quality_note"])
            if card["quality_status"] == "SUPPRESSED_EXERCISE":
                st.text("Los campos protegidos no llegan a la interfaz.")
            else:
                st.text(f"{card['estimate_text']} · {card['interval_text']}")
            st.caption("Estado: SHADOW")


def _validated_state_gallery(
    repository: IndicatorRepository,
    module_id: str = "3.2",
) -> None:
    """Render demo states only after repository and row validation succeeds."""
    try:
        cards = build_state_cards(repository, module_id)
    except ValueError:
        st.error("Los resultados no superaron la validación estadística.")
        return
    _state_gallery(cards)


def _d01_table(cards: list[dict]) -> None:
    st.table(
        [
            {
                "Indicador": card["indicator_name"],
                "Estimación": card["estimate_text"],
                "N no ponderado": card["n_text"].replace("N no ponderado: ", ""),
                "Calidad": card["quality_label"],
            }
            for card in cards
        ]
    )


def _render_d01_groups(repository: IndicatorRepository) -> None:
    try:
        task_execution, relationship = build_d01_task_groups(repository)
    except (ValueError, OSError, KeyError, TypeError):
        st.error("Los resultados no superaron la validación estadística.")
        return
    st.subheader("Quién realiza tareas en el hogar · ítems 1–7")
    st.caption(
        "La medida identifica si la tarea la realiza principalmente una mujer del hogar."
    )
    _d01_table(task_execution)
    st.subheader("Quién acompaña a la adolescente · ítems 8–10")
    st.caption(
        "La medida identifica si quien acompaña es principalmente una mujer del hogar."
    )
    _d01_table(relationship)
    rows = [
        row
        for row in load_validated_estimates(repository, "3.1")
        if row.indicator_id == "Componentes"
        and row.disaggregation == "Tareas del hogar"
    ]
    _download_cut(rows, "enares-stage04-31-nacional")


def _render_vs_matrices(repository: IndicatorRepository) -> None:
    rows = [
        row
        for row in load_validated_estimates(repository, "3.5")
        if row.indicator_id in {"Solap_VS_12M", "Solap_VS_VIDA"}
    ]
    if len(rows) != 16:
        raise ValueError("D06/D07 authorized matrices must contain exactly 16 rows")
    st.subheader("Matrices de solapamiento de violencia sexual")
    indicator = st.selectbox("Indicador matricial", ("Solap_VS_12M", "Solap_VS_VIDA"))
    matrix = st.selectbox("Matriz", ("2×2", "3×3"))
    matrix_rows = [
        row
        for row in rows
        if row.indicator_id == indicator and row.disaggregation == matrix
    ]
    by_category = {row.category: row for row in matrix_rows}
    category_options: list[str] = list(by_category)
    category = st.selectbox(
        "Categoría matricial",
        category_options,
        format_func=lambda value: precision_category_label(
            value, by_category[value].cv_flag
        ),
    )
    selected = [row for row in matrix_rows if row.category == category]
    if len(selected) != 1:
        raise ValueError("The selected D06/D07 V0 matrix cell is not unique")
    _numeric_summary(build_numeric_card(selected[0]), f"{indicator} · matriz {matrix}")
    _download_cut(selected, f"enares-stage04-35-{indicator}-{matrix}")


def render() -> None:
    st.set_page_config(page_title="ENARES 2024 · Shadow", page_icon="◉", layout="wide")
    _styles()
    authorized, demo = local_repositories()
    try:
        authorized_rows = [
            row
            for row in filter_estimates(authorized, "3.2", "Nacional", "Total")
            if row.indicator_id == "VF_HOGAR"
        ]
    except ValueError:
        st.error("Los resultados no superaron la validación estadística.")
        return
    if len(authorized_rows) != 1:
        st.error("El agregado autorizado Nacional / Total no está disponible.")
        return
    summary = build_numeric_card(authorized_rows[0])
    _header(summary["release_id"], summary["created_at"])

    st.sidebar.markdown("## ENARES · Stage 04")
    requested_page = st.query_params.get("page", NAVIGATION[0])
    page_index = NAVIGATION.index(requested_page) if requested_page in NAVIGATION else 0
    page = st.sidebar.radio("Navegación", NAVIGATION, index=page_index)
    requested_dimension = st.query_params.get("dimension", FUTURE_DIMENSIONS[0])
    dimension_index = (
        FUTURE_DIMENSIONS.index(requested_dimension)
        if requested_dimension in FUTURE_DIMENSIONS
        else 0
    )
    dimension = st.sidebar.selectbox(
        "Dimensión", FUTURE_DIMENSIONS, index=dimension_index
    )
    st.sidebar.caption(
        "Exportación segura: disponible solo en cortes agregados V0 autorizados"
    )
    st.sidebar.caption(
        "Cloud: NOT_AUTHORIZED · Techo máximo: USD 20/mes · Objetivo: USD 0"
    )

    if page == "Resumen":
        if dimension != "Nacional":
            st.info(
                f"{dimension}: sin datos en el resumen del corte local. "
                "No se fabrican resultados."
            )
            return
        _numeric_summary(summary)
        _download_cut(authorized_rows, "enares-stage04-resumen-nacional")
        _validated_state_gallery(demo)
    elif module := module_for_page(page):
        st.subheader(module.full_label)
        st.caption(f"Estado de datos: {module.data_state}")
        if dimension not in module.available_dimensions:
            st.info(
                f"{dimension}: sin datos autorizados para {module.module_id}. "
                "No se fabrican resultados."
            )
            return

        source = "V0 autorizado"
        if module.module_id == "3.2":
            source_options = ("V0 autorizado", "Demo sintético")
            requested_source = st.query_params.get("source", source_options[0])
            source_index = (
                source_options.index(requested_source)
                if requested_source in source_options
                else 0
            )
            source = st.radio(
                "Fuente local",
                source_options,
                index=source_index,
                horizontal=True,
            )

        if source == "Demo sintético":
            _validated_state_gallery(demo)
        else:
            if module.module_id == "3.1" and dimension == "Nacional":
                _render_d01_groups(authorized)
            if dimension not in module.authorized_dimensions:
                st.info(
                    f"{dimension}: sin datos autorizados para {module.module_id}. "
                    "El gate de calidad y supresión está pendiente. "
                    "No se fabrican resultados."
                )
                return
            try:
                dimension_rows = [
                    row
                    for row in load_validated_estimates(authorized, module.module_id)
                    if row.disaggregation == dimension
                ]
            except (ValueError, OSError, KeyError, TypeError):
                st.error("Los resultados no superaron la validación estadística.")
                return
            if not dimension_rows:
                st.info(
                    f"{dimension}: sin datos autorizados para {module.module_id}. "
                    "Pendiente de conciliación del contrato y los estados de calidad. "
                    "No se fabrican resultados."
                )
                return
            query = st.text_input("Buscar indicador", key=f"real_query_{module.module_id}")
            if query.strip():
                terms = query.casefold().split()
                dimension_rows = [
                    row
                    for row in dimension_rows
                    if all(
                        term in f"{row.indicator_id} {row.indicator_name} {row.category}".casefold()
                        for term in terms
                    )
                ]
            if not dimension_rows:
                st.info("No hay coincidencias en este módulo y dimensión.")
                return
            indicator_ids = tuple(
                dict.fromkeys(row.indicator_id for row in dimension_rows)
            )
            if len(indicator_ids) > 1:
                selected_indicator = st.selectbox("Indicador", indicator_ids)
                dimension_rows = [
                    row
                    for row in dimension_rows
                    if row.indicator_id == selected_indicator
                ]
            categories = tuple(row.category for row in dimension_rows)
            category = st.selectbox(
                "Categoría",
                categories,
                format_func=(
                    lambda value: (
                        d09_category_label(dimension, value)
                        if module.module_id == "3.5"
                        else value
                    )
                ),
            )
            matches = [row for row in dimension_rows if row.category == category]
            if len(matches) != 1:
                st.error("La combinación autorizada no está disponible de forma única.")
                return
            if matches[0].quality_status == "CONTEXT_ONLY":
                st.info(matches[0].quality_note)
                st.caption(
                    f"{matches[0].indicator_id} · {matches[0].disaggregation} · "
                    f"{matches[0].category}"
                )
                st.caption("Sin tarjeta, tabla numérica ni exportación.")
                return
            card = build_numeric_card(matches[0])
            _numeric_summary(card, f"Resultado agregado · {module.full_label}")
            _download_cut(
                matches,
                f"enares-stage04-{module.module_id.replace('.', '')}-{matches[0].indicator_id}-{dimension}",
            )
            if module.module_id == "3.5" and dimension == "Nacional":
                try:
                    _render_vs_matrices(authorized)
                except (ValueError, OSError, KeyError, TypeError):
                    st.error("Las matrices D06/D07 no superaron la validación.")
    elif page == "Metodología":
        st.subheader("Metodología y límites")
        st.write(
            "Las cifras V0 se consumen como agregados aprobados; la aplicación no recalcula Stage 03."
        )
        st.warning(
            "En 3.1–3.6, CV > 15 % es visible y referencial; base_unw < 30 "
            "es visible con alerta. Ninguna regla activa supresión."
        )
        st.write(
            "SHADOW permite evaluación local. APPROVED requiere revisión formal. PUBLISHED requiere un gate institucional separado."
        )
    else:
        st.subheader("Estado del release")
        st.code(summary["release_id"])
        st.success("SHADOW · agregado V0 identificado por manifiesto")
        st.error("PUBLISHED: NOT_AUTHORIZED")
        st.caption(
            "BigQuery, DDL y Cloud Run: BLOCKED_BY_CLOUD_GATE; "
            "configuración y primer despliegue pendientes de verificación"
        )

    st.divider()
    coverage = " · ".join(
        f"{module.module_id}: {len(module.authorized_dimensions)} alcances autorizados"
        for module in MODULES
    )
    st.caption(f"Cobertura local: {coverage}")
    st.caption(
        "Exportación limitada al corte agregado V0 visible · "
        "Sin búsqueda individual · Cloud bloqueado"
    )


if __name__ == "__main__":
    render()
