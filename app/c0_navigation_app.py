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
from enares.stage04.catalog_navigation import filter_catalog


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

    matches = filter_catalog(
        catalog,
        module_id=module_id,
        dimension=dimension,
        query=query,
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
        format_func=lambda row: f"{row.label} · {row.category}",
        key="c0_result",
    )
    if selected is None:
        st.info("Revise los candidatos y seleccione uno para continuar.")
        return

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
