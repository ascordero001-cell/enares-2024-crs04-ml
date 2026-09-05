"""Streamlit entry point for the local-only ENARES Stage 04 shell."""

from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from app.config import FUTURE_DIMENSIONS, NAVIGATION
from app.views.stage04_dashboard import (
    EXPORT_ENABLED,
    build_numeric_card,
    build_state_cards,
    filter_estimates,
)
from enares.stage04.repository import AuthorizedAggregateRepository, DemoRepository

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
        .stApp { background: #f5f7f4; color: #17251f; }
        [data-testid="stSidebar"] { background: #102d25; }
        [data-testid="stSidebar"] * { color: #f6fbf8 !important; }
        [data-testid="stSidebar"] [data-baseweb="select"] * { color: #17251f !important; }
        .hero { padding: 1.6rem 1.8rem; border-radius: 18px; color: white;
                background: linear-gradient(125deg,#0d4435,#1f745c 62%,#d59f45); }
        .eyebrow { letter-spacing: .12em; font-size: .75rem; font-weight: 700; opacity: .86; }
        .hero h1 { margin: .25rem 0; font-size: 2.15rem; }
        .hero p { margin: 0; opacity: .9; max-width: 54rem; }
        .notice { margin: 1rem 0; padding: .75rem 1rem; border-left: 4px solid #d59f45;
                  background: #fff8e9; border-radius: 8px; color: #4b3a18; }
        .status-card { padding: 1rem; border: 1px solid #dce6e1; border-radius: 14px;
                       background: white; min-height: 175px; }
        .status-card h4 { margin: 0 0 .5rem; color: #164c3c; }
        .pill { display:inline-block; padding:.25rem .55rem; border-radius:999px;
                background:#e2f2ea; color:#18533f; font-size:.78rem; font-weight:700; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _header(release_id: str, created_at: str) -> None:
    st.markdown(
        f"""
        <section class="hero">
          <div class="eyebrow">ENARES 2024 · DEMO/SHADOW</div>
          <h1>Vigilancia de violencia contra adolescentes</h1>
          <p>Corte local seguro para adolescentes de 12–17 años · Release {release_id} · {created_at}</p>
        </section>
        <div class="notice"><b>No es una publicación institucional.</b> V0 continúa oficial;
        este prototipo no habilita búsquedas individuales, exportación ni acceso cloud.</div>
        """,
        unsafe_allow_html=True,
    )


def _numeric_summary(card: dict) -> None:
    st.subheader("Resumen nacional · Módulo 3.2")
    st.caption("VF_HOGAR · Nacional / Total")
    a, b, c, d = st.columns(4)
    a.metric("Estimación", card["estimate_text"])
    b.metric("Error estándar", card["standard_error_text"])
    c.metric("CV", card["cv_text"].replace("CV ", ""))
    d.metric("N no ponderado", card["n_text"].replace("N no ponderado: ", ""))
    st.markdown(f"**{card['interval_text']}**")
    st.info(card["quality_label"])
    st.write(card["universe_text"])
    st.caption(card["denominator_text"])


def _state_gallery(cards: list[dict]) -> None:
    st.subheader("Estados visuales didácticos")
    columns = st.columns(3)
    for column, card in zip(columns, cards, strict=True):
        with column:
            if card["quality_status"] == "SUPPRESSED_EXERCISE":
                detail = "Los campos protegidos no llegan a la interfaz."
            else:
                detail = f"{card['estimate_text']} · {card['interval_text']}"
            st.markdown(
                f"""<div class="status-card"><span class="pill">DEMO SINTÉTICO</span>
                <h4>{card['category']}</h4><b>{card['quality_label']}</b>
                <p>{detail}</p><small>Estado: SHADOW</small></div>""",
                unsafe_allow_html=True,
            )


def render() -> None:
    st.set_page_config(page_title="ENARES 2024 · Shadow", page_icon="◉", layout="wide")
    _styles()
    authorized, demo = local_repositories()
    authorized_rows = filter_estimates(authorized, "3.2", "Nacional", "Total")
    if len(authorized_rows) != 1:
        st.error("El agregado autorizado Nacional / Total no está disponible.")
        return
    summary = build_numeric_card(authorized_rows[0])
    _header(summary["release_id"], summary["created_at"])

    st.sidebar.markdown("## ENARES · Stage 04")
    requested_page = st.query_params.get("page", NAVIGATION[0])
    page_index = NAVIGATION.index(requested_page) if requested_page in NAVIGATION else 0
    page = st.sidebar.radio("Navegación", NAVIGATION, index=page_index)
    dimension = st.sidebar.selectbox("Dimensión", FUTURE_DIMENSIONS)
    st.sidebar.button("Exportar", disabled=not EXPORT_ENABLED, help="Exportación no autorizada")
    st.sidebar.caption("Cloud: NOT_AUTHORIZED · Presupuesto: USD 0")

    if dimension != "Nacional":
        st.info(f"{dimension}: sin datos en este corte local. No se fabrican resultados.")
        return

    if page == "Resumen":
        _numeric_summary(summary)
        _state_gallery(build_state_cards(demo))
    elif page == "Módulo 3.2":
        st.subheader("Módulo 3.2 · Violencia en el hogar")
        source_options = ("V0 autorizado", "Demo sintético")
        requested_source = st.query_params.get("source", source_options[0])
        source_index = source_options.index(requested_source) if requested_source in source_options else 0
        source = st.radio("Fuente local", source_options, index=source_index, horizontal=True)
        if source == "V0 autorizado":
            _numeric_summary(summary)
        else:
            _state_gallery(build_state_cards(demo))
    elif page == "Metodología":
        st.subheader("Metodología y límites")
        st.write("Las cifras V0 se consumen como agregados aprobados; la aplicación no recalcula Stage 03.")
        st.warning("CV > 0.15, N < 30 y tolerancia 1e-9 continúan como propuestas pendientes.")
        st.write("SHADOW permite evaluación local. APPROVED requiere revisión formal. PUBLISHED requiere un gate institucional separado.")
    else:
        st.subheader("Estado del release")
        st.code(summary["release_id"])
        st.success("SHADOW · agregado V0 identificado por manifiesto")
        st.error("PUBLISHED: NOT_AUTHORIZED")
        st.caption("BigQuery, DDL, Cloud Run, IAM y facturación: BLOCKED_BY_CLOUD_GATE")

    st.divider()
    st.caption("Módulos pendientes: 3.1, 3.3, 3.4, 3.5 y 3.6 · Sin exportación · Sin búsqueda individual")


if __name__ == "__main__":
    render()
