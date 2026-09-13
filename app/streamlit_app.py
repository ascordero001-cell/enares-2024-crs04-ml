"""Streamlit entry point for the local-only ENARES Stage 04 shell."""

from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from app.config import FUTURE_DIMENSIONS, MODULES, NAVIGATION, module_for_page
from app.views.stage04_dashboard import (
    EXPORT_ENABLED,
    build_numeric_card,
    build_state_cards,
    filter_estimates,
    load_validated_estimates,
)
from enares.stage04.repository import (
    AuthorizedAggregateRepository,
    DemoRepository,
    IndicatorRepository,
)

def local_repositories():
    """Create only repositories backed by checked-in aggregate or synthetic fixtures."""
    data = ROOT / "app" / "data"
    authorized = AuthorizedAggregateRepository(
        data / "v0_authorized_indicator_estimates.csv",
        data / "v0_authorized_indicator_estimates.manifest.json",
        ROOT / "docs" / "stage04" / "v0_drive_hash_manifest.md",
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
        "no habilita búsquedas individuales, exportación ni acceso cloud."
    )


def _numeric_summary(card: dict, heading: str | None = None) -> None:
    st.subheader(heading or "Resumen nacional · Módulo 3.2")
    st.caption(
        f"{card['indicator_id']} · {card['disaggregation']} / {card['category']}"
    )
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


def _state_gallery(cards: list[dict]) -> None:
    st.subheader("Estados visuales didácticos")
    columns = st.columns(3)
    for column, card in zip(columns, cards, strict=True):
        with column:
            with st.container(border=True):
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


def render() -> None:
    st.set_page_config(page_title="ENARES 2024 · Shadow", page_icon="◉", layout="wide")
    _styles()
    authorized, demo = local_repositories()
    try:
        authorized_rows = filter_estimates(authorized, "3.2", "Nacional", "Total")
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
    dimension = st.sidebar.selectbox("Dimensión", FUTURE_DIMENSIONS, index=dimension_index)
    st.sidebar.button("Exportar", disabled=not EXPORT_ENABLED, help="Exportación no autorizada")
    st.sidebar.caption("Cloud: NOT_AUTHORIZED · Tope autorizado: USD 20/mes total")

    if page == "Resumen":
        if dimension != "Nacional":
            st.info(
                f"{dimension}: sin datos en el resumen del corte local. "
                "No se fabrican resultados."
            )
            return
        _numeric_summary(summary)
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
            categories = tuple(row.category for row in dimension_rows)
            category = st.selectbox("Categoría", categories)
            matches = filter_estimates(
                authorized,
                module.module_id,
                dimension,
                category,
            )
            if len(matches) != 1:
                st.error("La combinación autorizada no está disponible de forma única.")
                return
            card = build_numeric_card(matches[0])
            _numeric_summary(card, f"Resultado agregado · {module.full_label}")
    elif page == "Metodología":
        st.subheader("Metodología y límites")
        st.write("Las cifras V0 se consumen como agregados aprobados; la aplicación no recalcula Stage 03.")
        st.warning(
            "En 3.1–3.6, CV > 15 % es visible y referencial; base_unw < 30 "
            "es visible con alerta. Ninguna regla activa supresión."
        )
        st.write("SHADOW permite evaluación local. APPROVED requiere revisión formal. PUBLISHED requiere un gate institucional separado.")
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
        f"{module.module_id}: {len(module.authorized_dimensions)}/9 dimensiones autorizadas"
        for module in MODULES
    )
    st.caption(f"Cobertura local: {coverage}")
    st.caption("Sin exportación · Sin búsqueda individual · Cloud bloqueado")


if __name__ == "__main__":
    render()
