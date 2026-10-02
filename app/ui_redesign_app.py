"""Private Stage 04 dashboard using the verified V0 topic map."""

from __future__ import annotations

import os
import sys
from dataclasses import replace
from functools import partial
from hashlib import sha256
from html import escape
from pathlib import Path
from textwrap import wrap

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, ROOT / "src"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from app.repositories import configured_repositories
from app.views.export_controls import render_safe_export
from app.views.ui_redesign_real import (
    MODULE_IDS,
    STATE_LABELS,
    AuthorizedRedesignResult,
    ModuleIsolationError,
    enforce_module_isolation,
    format_cv,
    format_n,
    load_authorized_results,
    numeric_values_are_visible,
    protected_export_row,
    protected_interval,
    protected_percentage,
    rows_for_topic,
    safe_metadata_text,
    visible_cut,
    visible_indicator_name,
    visible_table_record,
)
from app.views.ui_visual_components import (
    inject_mockup_css,
    render_exact_header,
    render_exact_scope_banner,
    render_exact_table,
    render_module_cards,
    render_quality_legend,
    render_release_history,
    render_topic_navigation,
)
from enares.stage04.display_taxonomy import (
    OTHER_CHARACTERISTICS,
    STANDARD_DIMENSIONS,
    assert_standard_category_coverage,
    category_sort_key,
    display_category,
    display_dimension,
)
from enares.stage04.report_topics import (
    HEADLINE_INDICATOR_BY_MODULE,
    STANDARD_DISAGGREGATIONS,
    AssignmentIndex,
    ReportTopic,
    TopicCatalogError,
    load_topic_mapping,
    resolve_assignment,
    topic_by_id,
    topics_for_module,
)
from enares.stage04.repository import IndicatorRepository, RepositoryError

PRESENTATION_MODULE_LABELS = {
    "3.1": "Percepciones",
    "3.2": "Violencia en el hogar",
    "3.3": "Violencia en el entorno escolar",
    "3.4": "Violencia sexual",
    "3.5": "Acumulación de violencias",
    "3.6": "Ayuda y respuesta",
}
STATE_CLASS = {
    "PUBLISHABLE_SHADOW": "ok",
    "REFERENCE_HIGH_CV": "warn",
    "SMALL_N": "info",
    "REFERENCE_HIGH_CV_AND_SMALL_N": "warn",
    "CONTEXT_ONLY": "muted",
    "SUPPRESSED": "crit",
}
SECONDARY_VIEWS = (
    "Resumen nacional",
    "Brechas",
    "Calidad y notas",
    "Estado del gate",
    "Historial",
)
VISIBLE_VIEWS = (SECONDARY_VIEWS[0], *MODULE_IDS, *SECONDARY_VIEWS[1:])
NAVIGATION_WIDGET_ID = "stage04_visible_tab"
STANDARD_FILTERS = STANDARD_DIMENSIONS
SPECIAL_FILTER_KEY = "real_special_dimension"
NO_SELECTION = "Todas"


def _source_identity() -> str:
    """Bind a process snapshot to the approved release, manifests and local fixture."""
    paths = (
        ROOT / "app/data/v0_authorized_full_indicator_estimates.manifest.json",
        ROOT / "docs/stage04/v0_drive_hash_manifest.md",
        ROOT / "src/enares/stage04/report_topic_map.csv",
    )
    identity = [os.getenv("STAGE04_DATA_MODE", "LOCAL_AUTHORIZED")]
    identity.extend(sha256(path.read_bytes()).hexdigest() for path in paths)
    if identity[0] == "LOCAL_AUTHORIZED":
        identity.append(
            sha256(
                (ROOT / "app/data/v0_authorized_full_indicator_estimates.csv").read_bytes()
            ).hexdigest()
        )
    else:
        identity.extend(
            os.getenv(name, "")
            for name in (
                "STAGE04_BQ_TABLE_FQN",
                "STAGE04_RELEASE_ID",
                "STAGE04_RUN_ID",
            )
        )
    return ":".join(identity)


@st.cache_resource(show_spinner=False)
def _verified_release_snapshot(
    identity: str, _repository: IndicatorRepository
) -> tuple[AuthorizedRedesignResult, ...]:
    """Validate once per immutable release identity; share only frozen rows."""
    del identity
    results = tuple(load_authorized_results(_repository))
    assert_standard_category_coverage(
        (result.row.disaggregation, result.row.category) for result in results
    )
    return results


def _query_state(
    topic_ids_by_module: dict[str, tuple[str, ...]],
) -> tuple[str, str, str]:
    raw_view = str(st.query_params.get("view", "Módulo 3.1"))
    raw_topic = str(st.query_params.get("topic", ""))
    candidate = raw_view.removeprefix("Módulo ")
    if candidate in MODULE_IDS:
        module_id = candidate
        visible_view = candidate
    elif raw_view in SECONDARY_VIEWS:
        module_id = str(st.session_state.get("active_module_id", "3.1"))
        if module_id not in MODULE_IDS:
            module_id = "3.1"
        visible_view = raw_view
    else:
        module_id, visible_view = "3.1", "3.1"
    topics = topic_ids_by_module[module_id]
    topic_id = raw_topic if raw_topic in topics else topics[0]
    return module_id, visible_view, topic_id


def _ensure_navigation_state(
    topic_ids_by_module: dict[str, tuple[str, ...]],
) -> tuple[str, str]:
    query_module, visible_view, query_topic = _query_state(topic_ids_by_module)
    marker = f"{st.query_params.get('view', '')}|{query_topic}"
    if st.session_state.get("last_view_query") != marker:
        st.session_state["active_module_id"] = query_module
        st.session_state["active_report_topic_id"] = query_topic
        st.session_state["stage04_visible_tab"] = visible_view
        st.session_state["last_view_query"] = marker
    module_id = str(st.session_state.get("active_module_id", query_module))
    if module_id not in MODULE_IDS:
        module_id = query_module
    topic_id = str(st.session_state.get("active_report_topic_id", query_topic))
    if topic_id not in topic_ids_by_module[module_id]:
        topic_id = topic_ids_by_module[module_id][0]
        st.session_state["active_report_topic_id"] = topic_id
    st.query_params["topic"] = topic_id
    return module_id, topic_id


def _activate_module(module_id: str) -> None:
    if module_id not in MODULE_IDS:
        raise ValueError(f"Unknown module: {module_id}")
    topic_id = f"{module_id}.01"
    st.session_state["active_module_id"] = module_id
    st.session_state["active_report_topic_id"] = topic_id
    st.session_state["stage04_visible_tab"] = module_id
    st.session_state["last_view_query"] = f"Módulo {module_id}|{topic_id}"
    for key in tuple(st.session_state):
        if str(key).startswith("real_filter_") or key == SPECIAL_FILTER_KEY:
            del st.session_state[key]
    st.query_params["view"] = f"Módulo {module_id}"
    st.query_params["topic"] = topic_id


def _sync_visible_view() -> None:
    selected = str(st.session_state["stage04_visible_tab"])
    if selected in MODULE_IDS:
        _activate_module(selected)
    elif selected in SECONDARY_VIEWS:
        st.query_params["view"] = selected
        st.session_state["last_view_query"] = (
            f"{selected}|{st.session_state.get('active_report_topic_id', '')}"
        )
    else:
        raise ValueError(f"Unknown visible view: {selected}")


def _sync_topic_nav(module_id: str, valid_ids: tuple[str, ...]) -> None:
    topic_id = str(st.session_state[f"stage04_topic_nav_{module_id.replace('.', '_')}"])
    if not _topic_selection_is_current(
        module_id, topic_id, st.session_state.get("active_module_id"), valid_ids
    ):
        return
    st.session_state["active_report_topic_id"] = topic_id
    st.session_state["last_view_query"] = f"Módulo {module_id}|{topic_id}"
    st.query_params["view"] = f"Módulo {module_id}"
    st.query_params["topic"] = topic_id


def _topic_selection_is_current(
    module_id: str, topic_id: str, active_module_id: object, valid_ids: tuple[str, ...]
) -> bool:
    # Streamlit can deliver a prior module's widget callback after the card
    # callback has already switched modules. That stale event is not a new
    # selection and must not interrupt the current render.
    if module_id != active_module_id:
        return False
    if topic_id not in valid_ids:
        raise ValueError("Invalid topic navigation")
    return True


def _module_summaries(
    results: list[AuthorizedRedesignResult],
    topics: tuple[ReportTopic, ...],
    assignment: AssignmentIndex,
) -> list[dict[str, str]]:
    index = topic_by_id(topics)
    summaries: list[dict[str, str]] = []
    for module_id in MODULE_IDS:
        headline = HEADLINE_INDICATOR_BY_MODULE[module_id]
        candidates = [
            result
            for result in results
            if result.row.indicator_id == headline
            and result.row.disaggregation == "Nacional"
            and result.row.category.casefold() in {"total", "nacional (total)"}
        ]
        if (
            len(candidates) != 1
            or headline not in index[f"{module_id}.01"].technical_indicator_ids
        ):
            raise ModuleIsolationError(f"Missing or ambiguous headline for {module_id}")
        result = candidates[0]
        period_suffix = _period_suffix(resolve_assignment(assignment, result.row).period_label)
        summaries.append(
            {
                "code": module_id,
                "label": PRESENTATION_MODULE_LABELS[module_id],
                "indicator": index[f"{module_id}.01"].title,
                "period_suffix": period_suffix,
                "value": protected_percentage(result, result.row.estimate),
                "state": STATE_LABELS[result.state],
                "state_class": STATE_CLASS[result.state],
            }
        )
    return summaries


def _period_suffix(period: str) -> str:
    if period == "No aplica":
        return ""
    return f" ({period.casefold()})"


def _inject_suppressed_ui_test_result(
    results: list[AuthorizedRedesignResult],
) -> list[AuthorizedRedesignResult]:
    """Local-only sentinel for browser verification of protected presentation."""
    if os.getenv("STAGE04_UI_TEST_INJECT_SUPPRESSED") != "1":
        return results
    if os.getenv("STAGE04_DATA_MODE") != "LOCAL_AUTHORIZED":
        raise RuntimeError(
            "Suppression UI fixture is permitted only in LOCAL_AUTHORIZED"
        )
    target = next(
        index
        for index, result in enumerate(results)
        if result.row.indicator_id == HEADLINE_INDICATOR_BY_MODULE["3.1"]
        and result.row.disaggregation == "Nacional"
        and result.row.category.casefold() in {"total", "nacional (total)"}
    )
    original = results[target]
    suppressed = replace(
        original.row,
        estimate=99.9,
        standard_error=99.9,
        ci95_lower=99.9,
        ci95_upper=99.9,
        cv=0.999,
        n_unweighted=1,
        suppress_flag=True,
        quality_note="Fila sintética suprimida para prueba de interfaz",
    )
    injected = list(results)
    injected[target] = replace(original, row=suppressed, state="SUPPRESSED")
    return injected


def _reset_invalid(key: str, options: tuple[str, ...]) -> None:
    if st.session_state.get(key, NO_SELECTION) not in options:
        st.session_state[key] = NO_SELECTION


def _clear_disaggregation() -> None:
    for dimension in STANDARD_FILTERS:
        st.session_state[f"real_filter_{dimension}"] = NO_SELECTION
    st.session_state[SPECIAL_FILTER_KEY] = NO_SELECTION


def _format_filter_value(value: str, *, source: str, has_national: bool) -> str:
    if source == "Departamento" and value == NO_SELECTION and has_national:
        return "Nacional (total)"
    return display_category(source, value) if value != NO_SELECTION else NO_SELECTION


def effective_cut(
    topic: ReportTopic, rows: list[AuthorizedRedesignResult]
) -> tuple[str | None, str | None]:
    if topic.national_only:
        st.info("Solo disponible a nivel nacional.")
    has_national = any(result.row.disaggregation == "Nacional" for result in rows)
    special_options = (
        NO_SELECTION,
        *sorted(
            {
                result.row.disaggregation
                for result in rows
                if result.row.disaggregation not in STANDARD_DISAGGREGATIONS
            }
        ),
    )
    options_by_dimension: dict[str, tuple[str, ...]] = {}
    for dimension in STANDARD_FILTERS:
        categories = {
            result.row.category
            for result in rows
            if result.row.disaggregation == dimension
        }
        ordered = sorted(
            categories, key=lambda value: category_sort_key(dimension, value)
        )
        options_by_dimension[dimension] = (NO_SELECTION, *ordered)
    for dimension, options in options_by_dimension.items():
        _reset_invalid(f"real_filter_{dimension}", options)
    _reset_invalid(SPECIAL_FILTER_KEY, special_options)
    active = next(
        (
            dimension
            for dimension in STANDARD_FILTERS
            if st.session_state.get(f"real_filter_{dimension}", NO_SELECTION)
            != NO_SELECTION
        ),
        None,
    )
    if (
        active is None
        and st.session_state.get(SPECIAL_FILTER_KEY, NO_SELECTION) != NO_SELECTION
    ):
        active = OTHER_CHARACTERISTICS
    st.button(
        "Volver a Nacional",
        on_click=_clear_disaggregation,
        disabled=not has_national or active is None or topic.national_only,
        width="stretch",
    )
    for dimension, options in options_by_dimension.items():
        st.selectbox(
            display_dimension(dimension),
            options,
            key=f"real_filter_{dimension}",
            format_func=partial(
                _format_filter_value, source=dimension, has_national=has_national
            ),
            disabled=topic.national_only
            or len(options) == 1
            or active not in (None, dimension),
        )
    st.selectbox(
        OTHER_CHARACTERISTICS,
        special_options,
        key=SPECIAL_FILTER_KEY,
        disabled=(
            topic.national_only
            or len(special_options) == 1
            or active not in (None, OTHER_CHARACTERISTICS)
        ),
        help="Solo cortes presentes en V0 para este tema; no construye cruces nuevos.",
    )
    if topic.national_only:
        return "Nacional", None
    if active == OTHER_CHARACTERISTICS:
        return str(st.session_state[SPECIAL_FILTER_KEY]), None
    if active is not None:
        return active, str(st.session_state[f"real_filter_{active}"])
    return (
        ("Nacional", None)
        if has_national
        else (None, None)
    )


def _render_topic_chart(
    topic: ReportTopic,
    results: list[AuthorizedRedesignResult],
    assignment: AssignmentIndex,
    *,
    active_dimension: str | None,
    active_category: str | None,
) -> None:
    periods = sorted(
        {resolve_assignment(assignment, result.row).period_label for result in results}
    )
    for period in periods:
        period_rows = [
            result
            for result in results
            if resolve_assignment(assignment, result.row).period_label == period
            and numeric_values_are_visible(result)
            and result.row.estimate is not None
        ]
        national = [
            result
            for result in period_rows
            if result.row.disaggregation == "Nacional"
            and result.row.category.casefold() in {"total", "nacional (total)"}
        ]
        national_value = national[0].row.estimate if len(national) == 1 else None
        use_bars = topic.national_only or not any(
            result.row.disaggregation != "Nacional" for result in period_rows
        )
        dimensions = (
            ("Nacional",)
            if use_bars
            else tuple(
                dimension
                for dimension in (
                    *STANDARD_FILTERS,
                    *sorted(
                        {
                            row.row.disaggregation
                            for row in period_rows
                            if row.row.disaggregation
                            not in STANDARD_DISAGGREGATIONS
                        }
                    ),
                )
                if dimension != "Nacional"
                and any(row.row.disaggregation == dimension for row in period_rows)
                and active_dimension in (None, "Nacional", dimension)
            )
        )
        if not dimensions:
            st.info("Esta selección no contiene valores visibles para el gráfico.")
            continue
        for dimension in dimensions:
            chart_rows = [
                row for row in period_rows if row.row.disaggregation == dimension
            ]
            category_counts: dict[str, int] = {}
            for row in chart_rows:
                category_counts[row.row.category] = category_counts.get(row.row.category, 0) + 1
            records = []
            for result in chart_rows:
                item = resolve_assignment(assignment, result.row)
                category = display_category(dimension, result.row.category)
                if use_bars or category_counts[result.row.category] > 1:
                    indicator = visible_indicator_name(
                        result, topic=topic, topic_assignment=item
                    )
                    label = f"{indicator} · {category}"
                else:
                    label = category
                wrapped_label = "\n".join(
                    wrap(label, width=52, break_long_words=False, break_on_hyphens=False)
                )
                records.append(
                    {
                        "label": wrapped_label,
                        "full_label": label,
                        "estimate": result.row.estimate,
                        "lower": result.row.ci95_lower,
                        "upper": result.row.ci95_upper,
                        "cv": None if result.row.cv is None else result.row.cv * 100,
                        "n": result.row.n_unweighted,
                        "referential": bool(result.row.cv_flag),
                        "selected": result.row.category == active_category,
                    }
                )
            records.sort(key=lambda row: float(row["estimate"] or 0), reverse=True)
            st.html(
                '<div class="chart-group-head">'
                f"{escape(display_dimension(dimension) + _period_suffix(period))}</div>"
            )
            tooltip = [
                {"field": "full_label", "title": "Categoría"},
                {"field": "estimate", "title": "Estimación", "format": ".1f"},
                {"field": "cv", "title": "CV (%)", "format": ".1f"},
                {"field": "n", "title": "N"},
            ]
            y = {
                "field": "label",
                "type": "nominal",
                "title": None,
                "sort": [str(row["label"]) for row in records],
                "axis": {
                    "labelLimit": 420,
                    "labelLineHeight": 13,
                    "labelExpr": "split(datum.label, '\\n')",
                },
            }
            x = {
                "field": "estimate",
                "type": "quantitative",
                "title": "Porcentaje",
                "scale": {"domain": [0, 100]},
            }
            if use_bars:
                spec: dict[str, object] = {
                    "mark": {"type": "bar", "cornerRadiusEnd": 4, "color": "#0E7C6B"},
                    "encoding": {"y": y, "x": x, "tooltip": tooltip},
                }
            else:
                layers = []
                if national_value is not None:
                    layers.append(
                        {
                            "mark": {
                                "type": "rule",
                                "color": "#0E7C6B",
                                "strokeDash": [6, 4],
                            },
                            "data": {"values": [{"national_value": national_value}]},
                            "encoding": {
                                "x": {
                                    "field": "national_value",
                                    "type": "quantitative",
                                    "scale": {"domain": [0, 100]},
                                }
                            },
                        }
                    )
                layers.extend(
                    [
                        {
                            "mark": {"type": "rule", "color": "#0E7C6B", "strokeWidth": 2},
                            "encoding": {
                                "y": y,
                                "x": {
                                    "field": "lower",
                                    "type": "quantitative",
                                    "scale": {"domain": [0, 100]},
                                },
                                "x2": {"field": "upper"},
                            },
                        },
                        {
                            "mark": {
                                "type": "point",
                                "size": 105,
                                "stroke": "#0E7C6B",
                                "strokeWidth": 2,
                            },
                            "encoding": {
                                "y": y,
                                "x": x,
                                "fill": {
                                    "condition": [
                                        {"test": "datum.selected", "value": "#B23A2E"},
                                        {"test": "datum.referential", "value": "white"},
                                    ],
                                    "value": "#0E7C6B",
                                },
                                "tooltip": tooltip,
                            },
                        },
                    ]
                )
                spec = {"layer": layers}
            max_lines = max(
                (str(row["label"]).count("\n") + 1 for row in records), default=1
            )
            spec["height"] = {"step": max(28, max_lines * 15 + 6)}
            spec["padding"] = {"left": 12, "right": 12}
            spec["config"] = {
                "background": "#FFFFFF",
                "axis": {"gridColor": "#DBE3EE", "labelColor": "#4B5A72"},
                "view": {"stroke": None},
            }
            # Inline the already aggregate-only values in Vega-Lite. Passing
            # them as a separate dataframe makes Streamlit rebuild Arrow data
            # for every chart on every navigation, despite the tiny row count.
            spec["data"] = {"values": records}
            st.vega_lite_chart(spec, width="stretch")


def _context_name(universe: str) -> str:
    lower = universe.casefold()
    if "escuela" in lower or "_e_" in lower:
        return "Escuela"
    if "hogar" in lower or "_h_" in lower:
        return "Hogar"
    if "_vs" in lower or lower.startswith("vs_"):
        return "Violencia sexual"
    return "Población del indicador"


def _render_context_universes(rows: list[AuthorizedRedesignResult]) -> None:
    national = [row for row in rows if row.row.disaggregation == "Nacional"]
    candidates = national or rows
    contexts: dict[tuple[str, str, str], None] = {}
    for result in candidates:
        row = result.row
        contexts[(_context_name(row.universe), row.universe, row.denominator)] = None
    cards = []
    for context, universe, denominator in contexts:
        cards.append(
            "<div>"
            f"<span>{escape(context)} · UNIVERSO</span>{escape(safe_metadata_text(universe))}"
            f"<span>DENOMINADOR</span>{escape(safe_metadata_text(denominator))}"
            "</div>"
        )
    st.html('<section class="ficha" data-testid="stage04-context-universes">' + "".join(cards) + "</section>")


def _render_detail_ficha(
    detail: AuthorizedRedesignResult | None,
    *,
    module_id: str,
    topic: ReportTopic,
    assignment: AssignmentIndex,
) -> None:
    items = [
        ("Módulo", f"{module_id} · {PRESENTATION_MODULE_LABELS[module_id]}"),
        ("Tema", topic.title),
    ]
    if detail is None:
        items.append(("Estado", "Sin datos en el release V0 vigente"))
    else:
        item = resolve_assignment(assignment, detail.row)
        items.extend(
            [
                ("Indicador", visible_indicator_name(detail, topic=topic, topic_assignment=item)),
                ("Período", item.period_label),
                ("Universo", safe_metadata_text(detail.row.universe)),
                ("Denominador", safe_metadata_text(detail.row.denominator)),
                ("Corte", visible_cut(detail)),
                ("Estado", STATE_LABELS[detail.state]),
                ("Estimación", protected_percentage(detail, detail.row.estimate)),
                ("IC95%", protected_interval(detail)),
                ("CV", format_cv(detail.row.cv if numeric_values_are_visible(detail) else None)),
                ("N no ponderado", format_n(detail.row.n_unweighted if numeric_values_are_visible(detail) else None)),
            ]
        )
        if item.period_label == "Período no precisado":
            items.insert(4, ("Nota sobre período", "La fuente no precisa un plazo único para esta serie."))
    html = "".join(
        f"<div><span>{escape(label)}</span>{escape(value)}</div>" for label, value in items
    )
    st.html('<section class="ficha" data-testid="stage04-detail-sheet">' + html + "</section>")


def _render_secondary(
    view: str,
    *,
    results: list[AuthorizedRedesignResult],
    summaries: list[dict[str, str]],
    assignment: AssignmentIndex,
    topics: dict[str, ReportTopic],
    release_label: str,
    run_label: str,
) -> None:
    if view == "Resumen nacional":
        st.html('<div class="section-head"><h2>Resumen nacional</h2></div>')
        render_exact_table(
            ("Módulo", "Tema principal", "Estimación", "Estado"),
            tuple(
                (
                    f"{row['code']} · {row['label']}",
                    row["indicator"] + row["period_suffix"],
                    row["value"],
                    row["state"],
                )
                for row in summaries
            ),
        )
    elif view == "Brechas":
        st.markdown("### Brechas")
        st.info("Solo cifras V0 existentes; no se calculan contrastes nuevos.")
        rows = []
        for result in results:
            item = resolve_assignment(assignment, result.row)
            if "diferencia" in topics[item.topic_id].title.casefold():
                rows.append(
                    (
                        item.module_id,
                        topics[item.topic_id].title,
                        item.period_label,
                        protected_percentage(result, result.row.estimate),
                        STATE_LABELS[result.state],
                    )
                )
        render_exact_table(("Módulo", "Tema", "Período", "Estimación", "Estado"), rows)
    elif view == "Calidad y notas":
        render_quality_legend(synthetic=False)
        for state, label in STATE_LABELS.items():
            count = sum(result.state == state for result in results)
            if count:
                st.write(f"{label}: {count} fila(s)")
    elif view == "Estado del gate":
        st.success(
            f"Release agregado en shadow privado: {release_label} · run: {run_label}."
        )
        st.caption("Sin acceso público, microdatos, recálculo ni cruces nuevos.")
    elif view == "Historial":
        render_release_history(
            message=f"Release vigente: {release_label} · run: {run_label}."
        )
    else:
        raise ValueError(f"Unknown secondary view: {view}")


def render() -> None:
    st.set_page_config(
        page_title="ENARES · vigilancia poblacional",
        page_icon="◉",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_mockup_css()
    try:
        repository, _ = configured_repositories()
        if os.getenv("STAGE04_DATA_MODE") == "AUTHENTICATED_SHADOW":
            results = list(_verified_release_snapshot(_source_identity(), repository))
        else:
            results = load_authorized_results(repository)
            assert_standard_category_coverage(
                (result.row.disaggregation, result.row.category) for result in results
            )
        results = _inject_suppressed_ui_test_result(results)
        for result in results:
            safe_metadata_text(result.row.universe)
            safe_metadata_text(result.row.denominator)
        catalog = load_topic_mapping(
            ROOT / "src" / "enares" / "stage04" / "report_topic_map.csv",
            catalog_rows=[result.row for result in results],
        )
        assignments = catalog.assignments
        topics = catalog.topics
        topics_by_id = topic_by_id(topics)
        topic_ids_by_module = {
            module_id: tuple(
                topic.topic_id for topic in topics_for_module(topics, module_id)
            )
            for module_id in MODULE_IDS
        }
        module_id, topic_id = _ensure_navigation_state(topic_ids_by_module)
        module_rows = enforce_module_isolation(
            (
                result
                for result in results
                if resolve_assignment(assignments, result.row).module_id == module_id
            ),
            active_module_id=module_id,
            assignment=assignments,
        )
        topic = topics_by_id[topic_id]
        topic_rows = rows_for_topic(
            module_rows, active_module_id=module_id, topic=topic, assignment=assignments
        )
        release_ids = {result.row.release_id for result in results}
        run_ids = {result.row.run_id for result in results}
        if len(release_ids) != 1 or len(run_ids) != 1:
            raise ModuleIsolationError("Expected exactly one V0 release and run")
        release_label, run_label = next(iter(release_ids)), next(iter(run_ids))
        summaries = _module_summaries(results, topics, assignments)
    except (
        RepositoryError,
        OSError,
        TypeError,
        ValueError,
        TopicCatalogError,
        ModuleIsolationError,
    ):
        st.error(
            "La fuente agregada autorizada o su catálogo de temas no superó la validación."
        )
        return

    render_exact_header(
        release_label=release_label,
        release_state="RELEASE V0",
        cloud_state="SHADOW PRIVADO",
    )
    render_exact_scope_banner(
        "Sin microdatos, identificadores, recálculo ni cruces nuevos."
    )
    st.html(ROOT / "app/assets/stage04_history_sync.htm", unsafe_allow_javascript=True)
    with st.container(key="stage04_grid"):
        left, center, right = st.columns((210, 1000, 220), gap="medium")
        with left, st.container(key="stage04_left_rail"):
            with st.container(key="stage04_filters_panel"):
                st.html('<div class="panel-title">DESAGREGACIONES AUTORIZADAS</div>')
                dimension, category = effective_cut(topic, topic_rows)
                filtered = enforce_module_isolation(
                    (
                        result
                        for result in topic_rows
                        if (dimension is None or result.row.disaggregation == dimension)
                        and (category is None or result.row.category == category)
                    ),
                    active_module_id=module_id,
                    assignment=assignments,
                )
            with st.container(key="stage04_base_panel"):
                st.caption("BASE V0 VERIFICADA")
                st.write("516 claves técnicas · 3\u00a0014 filas agregadas")
        with center, st.container(key="stage04_center"):
            render_module_cards(
                summaries, active_module_id=module_id, on_select=_activate_module
            )
            selected = st.segmented_control(
                "Vista",
                VISIBLE_VIEWS,
                key=NAVIGATION_WIDGET_ID,
                on_change=_sync_visible_view,
                label_visibility="collapsed",
                width="stretch",
            )
            if selected in MODULE_IDS and selected != module_id:
                _activate_module(selected)
                st.rerun()
            if selected in MODULE_IDS:
                st.html(
                    '<div class="section-head"><h2>'
                    f"{escape(module_id)} · {escape(PRESENTATION_MODULE_LABELS[module_id])}"
                    "</h2></div>"
                )
                module_topics = topics_for_module(topics, module_id)
                render_topic_navigation(
                    module_topics,
                    active_module_id=module_id,
                    active_topic_id=topic_id,
                    on_select=partial(
                        _sync_topic_nav, module_id, topic_ids_by_module[module_id]
                    ),
                )
                st.html(
                    '<div class="section-head topic"><h2>'
                    f"{escape(topic.title)}</h2></div>"
                )
                if not topic_rows:
                    st.info("Sin datos en el release V0 vigente.")
                else:
                    _render_context_universes(topic_rows)
                    headers = (
                        "Indicador",
                        "Corte",
                        "Estimación",
                        "IC95%",
                        "CV",
                        "N",
                        "Estado y notas",
                    )
                    visible_rows = []
                    for result in filtered:
                        item = resolve_assignment(assignments, result.row)
                        row = visible_table_record(
                            result, topic=topic, topic_assignment=item
                        )
                        row["Indicador"] += _period_suffix(item.period_label)
                        visible_rows.append((item.period_label, row))
                    visible_rows.sort(key=lambda entry: (entry[0], entry[1]["Indicador"]))
                    render_exact_table(
                        headers,
                        tuple(
                            tuple(row[header] for header in headers)
                            for _, row in visible_rows
                        ),
                    )
                    _render_topic_chart(
                        topic,
                        topic_rows,
                        assignments,
                        active_dimension=dimension,
                        active_category=category,
                    )
            else:
                _render_secondary(
                    str(selected),
                    results=results,
                    summaries=summaries,
                    assignment=assignments,
                    topics=topics_by_id,
                    release_label=release_label,
                    run_label=run_label,
                )
        with right, st.container(key="stage04_right_rail"):
            with st.container(key="stage04_alerts_panel"):
                st.html('<div class="panel-title">ALERTAS Y HALLAZGOS</div>')
                flagged = [
                    row
                    for row in filtered
                    if row.row.cv_flag
                    or row.row.n_flag
                    or row.state in {"CONTEXT_ONLY", "SUPPRESSED"}
                ]
                if not flagged:
                    st.html('<div class="alert-item info"><div class="ai-title">Sin alertas en la selección.</div></div>')
                for result in flagged:
                    item = resolve_assignment(assignments, result.row)
                    label = visible_indicator_name(
                        result, topic=topic, topic_assignment=item
                    )
                    st.html(
                        '<div class="alert-item warn"><div>'
                        f'<div class="ai-title">{escape(label)}</div>'
                        f'<div class="ai-desc">{escape(visible_cut(result))} · '
                        f'{escape(STATE_LABELS[result.state])}</div>'
                        "</div></div>"
                    )
            with st.container(key="stage04_sheet_panel"):
                st.html('<div class="panel-title">FICHA DEL INDICADOR ACTIVO</div>')
                detail = next(
                    (
                        row
                        for row in filtered
                        if row.row.disaggregation == "Nacional"
                        and row.row.category.casefold() in {"total", "nacional (total)"}
                    ),
                    filtered[0] if filtered else None,
                )
                _render_detail_ficha(
                    detail, module_id=module_id, topic=topic, assignment=assignments
                )
            with st.container(key="stage04_export_panel"):
                st.html('<div class="panel-title">EXPORTAR</div>')
                if filtered:
                    render_safe_export(
                        [protected_export_row(result) for result in filtered],
                        basename=f"enares-stage04-{topic_id.replace('.', '-')}",
                    )
                else:
                    st.info("No hay un corte visible para exportar.")
    st.caption(
        "V0 continúa oficial · publicación institucional y cutover: NOT_AUTHORIZED"
    )


if __name__ == "__main__":
    render()
