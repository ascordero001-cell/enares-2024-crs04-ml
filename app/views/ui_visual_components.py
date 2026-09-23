"""Reusable native Streamlit components for the Stage 04 visual contract."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

import streamlit as st

VISUAL_TOKENS = {
    "paper": "#F1F4F9",
    "surface": "#FFFFFF",
    "surface_secondary": "#EAEFF6",
    "border": "#DBE3EE",
    "ink": "#16202E",
    "ink_soft": "#4B5A72",
    "brand": "#22405F",
    "brand_strong": "#16293D",
    "accent": "#0E7C6B",
    "success": "#2F9E5C",
    "warning": "#9A6B08",
    "information": "#2E5EA8",
    "critical": "#B23A2E",
}

SCOPE_CONTAINER_KEY = "stage04_" + "scope_banner"

VISUAL_CSS = """
<style>
:root {
  --s04-paper: #F1F4F9;
  --s04-surface: #FFFFFF;
  --s04-surface-2: #EAEFF6;
  --s04-border: #DBE3EE;
  --s04-ink: #16202E;
  --s04-ink-soft: #4B5A72;
  --s04-brand: #22405F;
  --s04-brand-strong: #16293D;
  --s04-accent: #0E7C6B;
  --s04-success: #2F9E5C;
  --s04-warning: #9A6B08;
  --s04-information: #2E5EA8;
  --s04-critical: #B23A2E;
}
.stApp { background: var(--s04-paper); color: var(--s04-ink); }
.block-container { max-width: 1360px; padding-top: 1.15rem; padding-bottom: 2.5rem; }
h1, h2, h3 { color: var(--s04-brand-strong); font-family: Georgia, serif; }
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] * {
  color: var(--s04-ink-soft) !important;
  opacity: 1 !important;
}
[data-testid="stMetricValue"] { font-family: Consolas, monospace; color: var(--s04-brand-strong); }
.st-key-stage04_header,
.st-key-stage04_scope_banner,
.st-key-stage04_left_rail,
.st-key-stage04_center,
.st-key-stage04_right_rail,
.st-key-stage04_module_strip,
.st-key-stage04_quality_legend,
.st-key-stage04_indicator_sheet,
.st-key-stage04_release_history {
  background: var(--s04-surface);
  border: 1px solid var(--s04-border);
  border-radius: 12px;
  padding: 1rem;
}
.st-key-stage04_header { border-top: 4px solid var(--s04-brand); }
.st-key-stage04_scope_banner { border-left: 4px solid var(--s04-information); margin: .75rem 0 1rem; }
.st-key-stage04_left_rail, .st-key-stage04_right_rail { position: sticky; top: 1rem; }
.st-key-stage04_module_strip { margin-bottom: 1rem; }
.st-key-stage04_module_strip [data-testid="stVerticalBlockBorderWrapper"] {
  min-height: 150px;
  border-color: var(--s04-border);
}
.st-key-stage04_view { overflow-x: auto; }
.st-key-stage04_view button { white-space: nowrap; }
.st-key-stage04_left_rail label, .st-key-stage04_right_rail label { color: var(--s04-ink-soft); }
@media (max-width: 1080px) {
  .st-key-stage04_left_rail, .st-key-stage04_right_rail { position: static; }
  .st-key-stage04_layout [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
  .st-key-stage04_layout [data-testid="stColumn"] { min-width: min(100%, 320px); flex: 1 1 100%; }
  .st-key-stage04_module_strip [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
  .st-key-stage04_module_strip [data-testid="stColumn"] {
    min-width: calc(33.333% - .75rem);
    flex: 1 1 calc(33.333% - .75rem);
  }
}
@media (max-width: 780px) {
  .st-key-stage04_header [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
  .st-key-stage04_header [data-testid="stColumn"] { min-width: 100%; flex: 1 1 100%; }
  .st-key-stage04_header h1 { font-size: 2.15rem; overflow-wrap: normal; word-break: normal; }
}
@media (max-width: 560px) {
  .block-container { padding-left: .65rem; padding-right: .65rem; }
  .st-key-stage04_header h1 { font-size: 1.8rem; overflow-wrap: normal; word-break: normal; }
  .st-key-stage04_module_strip [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
  .st-key-stage04_module_strip [data-testid="stColumn"] { min-width: calc(50% - .5rem); flex: 1 1 calc(50% - .5rem); }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .001ms !important; transition-duration: .001ms !important; }
}
</style>
"""


def inject_visual_css() -> None:
    """Install static CSS without interpolating runtime values."""
    st.html(VISUAL_CSS)


def render_header(*, release_label: str, subtitle: str) -> None:
    """Render the institutional header with native text components."""
    with st.container(key="stage04_header"):
        glifo, title, release = st.columns((0.7, 5.0, 2.1), vertical_alignment="center")
        with glifo:
            st.markdown("## 04")
        with title:
            st.caption("ENARES 2024 · VIGILANCIA POBLACIONAL")
            st.title("Violencia contra niñas, niños y adolescentes")
            st.caption(subtitle)
        with release:
            st.caption("ESTADO DEL RELEASE")
            st.code(release_label, language=None)
            st.caption("Acceso autenticado · no publicación")


def render_scope_banner(message: str) -> None:
    """Render the current scope with native, escaped Streamlit output."""
    with st.container(key=SCOPE_CONTAINER_KEY):
        st.info(message)


def render_module_strip(
    modules: Iterable[Mapping[str, str]],
    *,
    caption: str = "INDICADORES CLAVE POR MÓDULO · FIXTURE SINTÉTICO",
    metric_label: str = "Valor sintético",
) -> None:
    """Render six summaries without dynamic HTML."""
    module_list = list(modules)
    with st.container(key="stage04_module_strip"):
        st.caption(caption)
        columns = st.columns(len(module_list))
        for column, module in zip(columns, module_list, strict=True):
            with column, st.container(border=True):
                st.caption(f"MÓDULO {module['code']}")
                st.markdown(f"**{module['label']}**")
                st.caption(module["indicator"])
                if module["value"].endswith("%"):
                    st.metric(
                        metric_label, module["value"], label_visibility="collapsed"
                    )
                else:
                    st.markdown(f"**{module['value']}**")
                st.caption(module["state"])


def render_quality_legend(*, synthetic: bool = True) -> None:
    """Render the approved meaning of independent quality states."""
    with st.container(key="stage04_quality_legend"):
        st.subheader("Cómo leer los estados")
        qualifier = "cifra sintética" if synthetic else "cifra V0"
        st.success(f"Sin alerta — {qualifier} visible.")
        st.warning("CV alto — cifra visible y referencial.")
        st.warning("N reducido — cifra visible con alerta; no se suprime.")
        st.error("Suprimido — ningún campo estadístico protegido llega a la vista.")


def render_release_history(
    *,
    message: str = "Sin release sintético publicado. Esta vista prueba composición, no promoción.",
) -> None:
    """Render the supplied release-history state."""
    with st.container(key="stage04_release_history"):
        st.subheader("Historial")
        st.info(message)
        st.caption("V0 continúa oficial · publicación y cutover: NOT_AUTHORIZED")


def render_indicator_sheet(fields: Mapping[str, str]) -> None:
    """Render one selected synthetic indicator using native values."""
    with st.container(key="stage04_indicator_sheet"):
        st.subheader("Ficha del indicador activo")
        for label, value in fields.items():
            st.caption(label.upper())
            st.write(value)
