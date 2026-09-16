"""Synthetic Streamlit prototype for the Stage 04 C0 navigation gate."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enares.stage04.c0_fixture import CATALOG_SIZE, build_synthetic_catalog
from enares.stage04.catalog_navigation import CatalogLocator, filter_catalog


def _facet(
    label: str,
    values: tuple[str, ...],
    *,
    key: str,
) -> str | None:
    return st.selectbox(
        label,
        values,
        index=None,
        placeholder="Todos",
        key=key,
    )


def _result_label(locator: CatalogLocator) -> str:
    return (
        f"{locator.focus.capitalize()} — {locator.population} — "
        f"{locator.period} — {locator.context}"
    )


def render() -> None:
    catalog = build_synthetic_catalog()
    st.set_page_config(page_title="C0 sintético", layout="wide")
    st.title("C0 · Navegación sintética del catálogo")
    st.caption(f"{CATALOG_SIZE} indicadores sintéticos · sin cifras V0")

    modules = tuple(dict.fromkeys(row.module_id for row in catalog))
    module_id = st.selectbox("Módulo", modules, key="c0_module")
    dimensions = tuple(
        dict.fromkeys(row.dimension for row in catalog if row.module_id == module_id)
    )
    dimension = st.selectbox("Dimensión", dimensions, key="c0_dimension")
    query = st.text_input("Buscar indicador", key="c0_query")

    if not query.strip():
        st.info("Escriba los términos de la tarea congelada.")
        return

    initial_matches = filter_catalog(
        catalog,
        module_id=module_id,
        dimension=dimension,
        query=query,
    )
    if not initial_matches:
        st.warning("No se encontró un indicador sintético.")
        return

    st.subheader("Refinar resultados")
    st.caption(
        "Use los datos del enunciado para distinguir candidatos antes de confirmar."
    )
    columns = st.columns(4)
    with columns[0]:
        focus = _facet(
            "Tema",
            tuple(dict.fromkeys(row.focus for row in initial_matches)),
            key="c0_focus",
        )
    with columns[1]:
        population = _facet(
            "Población",
            tuple(dict.fromkeys(row.population for row in initial_matches)),
            key="c0_population",
        )
    with columns[2]:
        period = _facet(
            "Periodo",
            tuple(dict.fromkeys(row.period for row in initial_matches)),
            key="c0_period",
        )
    with columns[3]:
        context = _facet(
            "Ámbito",
            tuple(dict.fromkeys(row.context for row in initial_matches)),
            key="c0_context",
        )

    matches = filter_catalog(
        catalog,
        module_id=module_id,
        dimension=dimension,
        query=query,
        focus=focus,
        population=population,
        context=context,
        period=period,
    )
    st.caption(f"Resultados: {len(matches)} de {CATALOG_SIZE}")
    if not matches:
        st.warning("No se encontró un indicador sintético.")
        return

    selected = st.selectbox(
        "Resultado",
        matches,
        index=None,
        placeholder="Seleccione un indicador",
        format_func=_result_label,
        key="c0_result",
    )
    if selected is None:
        st.info("Revise los candidatos y seleccione uno para continuar.")
        return

    st.info(
        "Va a confirmar: "
        f"{selected.focus}; {selected.population}; {selected.period}; {selected.context}."
    )

    if st.button("Confirmar indicador", key="c0_confirm"):
        st.session_state["c0_confirmed_id"] = selected.indicator_id
        st.session_state["c0_confirmed_label"] = selected.label

    confirmed_id = st.session_state.get("c0_confirmed_id")
    if confirmed_id == selected.indicator_id:
        st.code(confirmed_id, language=None)
        st.write(st.session_state["c0_confirmed_label"])
        st.caption(f"{selected.dimension} · {selected.category}")


if __name__ == "__main__":
    render()
