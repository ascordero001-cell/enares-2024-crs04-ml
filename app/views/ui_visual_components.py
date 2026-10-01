"""Reusable native Streamlit components for the Stage 04 visual contract."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from html import escape
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st

from enares.stage04.report_topics import ReportTopic

ASSET_ROOT = Path(__file__).resolve().parents[1] / "assets"


def inject_mockup_css() -> None:
    css = (ASSET_ROOT / "stage04_mockup.css").read_text(encoding="utf-8")
    st.html(f"<style>{css}</style>")


def render_exact_header(
    *, release_label: str, release_state: str, cloud_state: str
) -> None:
    st.html(
        '<header class="topbar" data-testid="stage04-exact-header">'
        '<div class="brandmark"><div class="glyph" aria-hidden="true">04</div>'
        '<div><div class="eyebrow">ENARES 2024 · CRS04 · STAGE 04</div>'
        "<h1>Vigilancia poblacional de violencia contra adolescentes</h1>"
        '<div class="sub">Perú · Adolescentes de 12 a 17 años · '
        "Resultados agregados, no expedientes individuales</div></div></div>"
        '<div class="release-chip"><div><div class="rc-label">Alcance vigente</div>'
        f'<div class="rc-id">{escape(release_label)}</div></div><div class="pills">'
        f'<span class="pill accent"><span class="dot"></span>{escape(release_state)}</span>'
        f'<span class="pill info"><span class="dot"></span>{escape(cloud_state)}</span>'
        "</div></div></header>"
    )


def render_exact_scope_banner(message: str) -> None:
    st.html(
        '<section class="banner" data-testid="stage04-exact-banner">'
        '<span class="tag">ACCESO CONTROLADO</span><div>'
        "<strong>Aplicación privada con resultados agregados.</strong> "
        f"{escape(message)}</div></section>"
    )


def render_module_cards(
    modules: Iterable[Mapping[str, str]], *, active_module_id: str
) -> None:
    cards: list[str] = []
    for module in modules:
        module_id = module["code"]
        active = " active" if module_id == active_module_id else ""
        current = ' aria-current="page"' if active else ""
        href = "?" + urlencode({"view": f"Módulo {module_id}"})
        cards.append(
            f'<a class="stripcard{active}" href="{escape(href)}"{current} '
            f'aria-label="Abrir módulo {escape(module_id)}: {escape(module["label"])}">'
            '<div class="sc-top">'
            f'<span class="sc-code">{escape(module_id)}</span>'
            f'<span class="pill {escape(module["state_class"])}" '
            f'aria-label="{escape(module["state"])}" title="{escape(module["state"])}">'
            f'<span class="dot" aria-hidden="true"></span>'
            f'<span class="state-text" aria-hidden="true">{escape(module["state"])}</span></span></div>'
            f"<h3>{escape(module['label'])}</h3>"
            f'<div class="sc-label" title="{escape(module["indicator"])}">{escape(module["indicator"])}</div>'
            f'<div class="sc-value">{escape(module["value"])}</div></a>'
        )
    st.html(
        '<nav class="strip" data-testid="stage04-module-cards" '
        'aria-label="Módulos 3.1 a 3.6">' + "".join(cards) + "</nav>"
    )


def render_topic_navigation(
    topics: Sequence[ReportTopic], *, active_module_id: str, active_topic_id: str
) -> None:
    links: list[str] = []
    for topic in topics:
        active = " active" if topic.topic_id == active_topic_id else ""
        current = ' aria-current="page"' if active else ""
        href = "?" + urlencode(
            {"view": f"Módulo {active_module_id}", "topic": topic.topic_id}
        )
        links.append(
            f'<a class="topic-link{active}" href="{escape(href)}"{current} '
            f'aria-label="Abrir {escape(topic.title)}">{escape(topic.title)}</a>'
        )
    st.html(
        '<section class="topic-catalog" data-testid="stage04-topic-catalog">'
        '<div class="topic-catalog-title">INDICADORES DEL MÓDULO '
        f'{escape(active_module_id)}</div><nav aria-label="Indicadores del módulo">'
        + "".join(links)
        + "</nav></section>"
    )


def render_exact_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    head = "".join(f"<th>{escape(value)}</th>" for value in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(value)}</td>" for value in row) + "</tr>"
        for row in rows
    )
    st.html(
        f'<div class="table-wrap"><table class="data"><thead><tr>{head}</tr>'
        f"</thead><tbody>{body}</tbody></table></div>"
    )


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
