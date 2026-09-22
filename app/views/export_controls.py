"""Reusable safe export controls for authorized aggregate cuts."""

from __future__ import annotations

from collections.abc import Iterable

import streamlit as st

from app.views.stage04_dashboard import EXPORT_ENABLED
from enares.stage04.export import build_export_bundle
from enares.stage04.repository import IndicatorEstimate, RepositoryError


def render_safe_export(rows: Iterable[IndicatorEstimate], *, basename: str) -> None:
    """Render equivalent CSV/XLSX downloads after the existing export gate."""
    if not EXPORT_ENABLED:
        return
    try:
        bundle = build_export_bundle(rows, basename=basename)
    except (RepositoryError, ValueError, OSError, KeyError, TypeError):
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
