"""Build the editorial V0 row-to-topic map; never transform V0 statistics.

Every rule below routes an existing technical key to an approved report topic.
Unknown keys fail closed. The generated CSV is committed and checked against
all 3,014 immutable V0 rows at runtime; this script is not a runtime dependency.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from enares.stage04.report_topics import (
    STANDARD_DISAGGREGATIONS,
    STANDARD_SCOPE,
    load_topic_mapping,
)

SOURCE = ROOT / "app/data/v0_authorized_full_indicator_estimates.csv"
DESTINATION = ROOT / "src/enares/stage04/report_topic_map.csv"

PERCEPTION_TOPICS = {
    "justifica_castigo_parental": "3.1.01",
    "justifica_castigo_docente": "3.1.02",
    "rechaza_trabajo_infantil_necesidad": "3.1.03",
    "reconoce_derecho_opinar": "3.1.04",
    "rechaza_dejar_estudiar": "3.1.05",
    "reconoce_derecho_denunciar": "3.1.06",
    "predominio_femenino_tareas": "3.1.07",
    "Componentes": "3.1.07",
    "mito_locas": "3.1.08",
    "mito_pobreza": "3.1.09",
    "mito_fuera_casa": "3.1.10",
    "mito_sitios_oscuros": "3.1.11",
}

EXACT_TOPICS = {
    "VP_HOGAR": "3.2.01",
    "VF_HOGAR": "3.2.03",
    "VS_H": "3.2.05",
    "VS_H_1": "3.2.05",
    "VF_HOGAR_01": "3.2.08",
    "VF_HOGAR_03": "3.2.10",  # C3P216A/C: personal and caregiver-induced risk.
    "VN_HOGAR1": "3.2.07",
    "INDICADOR_8_3_6": "3.2.11",  # Source formula: VP/VF/negligence in household.
    "VP_o_VF_HOGAR": "3.2.12",
    "VP_o_VF_HOGAR__VP_o_VF_HOGAR": "3.2.12",
    "Hogar__VP_o_VF_HOGAR": "3.2.12",
    "VP_VF_HOGAR": "3.2.13",
    "Solap_VP_VF_H": "3.2.14",
    "Solap_VP_VF_H__Coexistencia": "3.2.14",
    "VP_VF_VS_HOGAR": "3.2.15",
    "VP_o_VF_o_VS_HOGAR": "3.2.16",
    "VP_ESCUELA": "3.3.01",
    "VF_ESCUELA": "3.3.03",
    "VS_E": "3.3.05",
    "VS_E_1": "3.3.05",
    "VP_VF_E": "3.3.07",
    "VP_o_VF_E": "3.3.08",
    "VP_o_VF_ESCUELA": "3.3.08",
    "INDICADOR_8_3_9": "3.3.09",  # Source formula: VP or VF or VS at school.
    "VP_VF_VS_E": "3.3.10",
    "Solap_VP_VF_E": "3.3.11",
    "Solap_VP_VF_E__Coexistencia": "3.3.11",
    "VP_EJERCIDA": "3.3.13",
    "VF_EJERCIDA": "3.3.14",
    "VP_o_VF_EJERCIDA": "3.3.15",
    "VS_12M": "3.4.01",
    "VS_VIDA": "3.4.01",
    "Solap_VS_12M": "3.4.04",
    "Solap_VS_VIDA": "3.4.04",
    "VS_OtraPersona_12M": "3.4.05",
    "VS_OtraPersona_VIDA": "3.4.05",
    "INDICADOR_8_2_7": "3.4.06",
    "INDICADOR_8_2_8": "3.4.07",
    "INDICADOR_8_2_13": "3.4.08",
    "PV_hogar_escuela": "3.5.01",
    "PV_VP_hogar_escuela": "3.5.02",
    "PV_VF_hogar_escuela": "3.5.03",
    "PV_VP_hogar_VF_escuela": "3.5.04",
    "PV_VF_hogar_VP_escuela": "3.5.05",
    "PV_VP_VF_hogar_escuela": "3.5.06",
    "PV_hogar_escuela1": "3.5.07",
    "PV_VP_VF_hogar_escuela_VS": "3.5.08",
    "PV_condicional_con_VS": "3.5.09",
    "CONS_ALGUNA": "3.5.10",
    "CONS_ATENCION_SALUD": "3.5.11",
    "num_consecuencias_fisicas": "3.5.12",
    "busco_ayuda_hogar": "3.6.01",
    "recibio_ayuda_hogar": "3.6.01",
    "recibio_ayuda_hogar_victimas": "3.6.01",
    "brecha_ayuda_hogar": "3.6.01",
    "busco_ayuda_escuela": "3.6.02",
    "recibio_ayuda_escuela": "3.6.02",
    "recibio_ayuda_escuela_victimas": "3.6.02",
    "brecha_ayuda_escuela": "3.6.02",
    "busco_ayuda_vs": "3.6.03",
    "recibio_ayuda_vs": "3.6.03",
    "recibio_ayuda_vs_victimas": "3.6.03",
    "brecha_ayuda_vs": "3.6.03",
}

CHARACTERISATION_TOPICS = {
    "VP_HOGAR": "3.2.17",
    "VF_HOGAR": "3.2.18",
    "VP_EJERCIDA": "3.3.19",
    "VF_EJERCIDA": "3.3.20",
    "VS_12M": "3.4.09",
}


def topic_for(indicator_id: str, disaggregation: str) -> str:
    if (
        disaggregation not in STANDARD_DISAGGREGATIONS
        and indicator_id in CHARACTERISATION_TOPICS
    ):
        return CHARACTERISATION_TOPICS[indicator_id]
    if indicator_id in PERCEPTION_TOPICS:
        return PERCEPTION_TOPICS[indicator_id]
    if indicator_id in EXACT_TOPICS:
        return EXACT_TOPICS[indicator_id]
    if indicator_id.startswith(("Agresor_VP_H__", "C3P201_", "VP_ICVAC_")):
        return "3.2.02"
    if indicator_id.startswith(("Agresor_VF_H__", "C3P205_", "VF_ICVAC_")):
        return "3.2.04"
    if indicator_id.startswith("Formas_Agresor_VS_H"):
        return "3.2.06"
    if (
        indicator_id.startswith(("Agresor_VP_E__", "VPE_ICVAC_", "C3P223_"))
        or indicator_id == "AG_VP_09"
    ):
        return "3.3.02"
    if (
        indicator_id.startswith(("Agresor_VF_E__", "VFE_ICVAC_", "C3P227_"))
        or indicator_id == "AG_VF_09"
    ):
        return "3.3.04"
    if indicator_id.startswith("Formas_VS_E"):
        return "3.3.06"
    if indicator_id.startswith(("Lugar", "Hora")) and indicator_id.endswith("_ViolEsc"):
        return "3.3.12"
    if indicator_id.startswith("C3P233_"):
        return "3.3.16"
    if indicator_id.startswith(("Formas_VS_12M", "Formas_VS_VIDA")):
        return "3.4.02"
    if indicator_id.startswith(("Agresor_VS_", "Prev_Agresor_VS__")):
        return "3.4.03"
    if indicator_id.startswith("PV_condicional_"):
        return "3.5.09"
    if indicator_id.startswith("C3P243_"):
        return "3.5.12"
    if indicator_id.startswith("ayuda_hogar_"):
        return (
            "3.6.04"
            if not indicator_id.startswith(
                (
                    "ayuda_hogar_consejo",
                    "ayuda_hogar_consuelo",
                    "ayuda_hogar_hablo_",
                    "ayuda_hogar_llamo_",
                    "ayuda_hogar_respuesta_",
                    "ayuda_hogar_otro_tipo",
                )
            )
            else "3.6.07"
        )
    if indicator_id.startswith("ayuda_escuela_"):
        return (
            "3.6.05"
            if not indicator_id.startswith(
                (
                    "ayuda_escuela_consejo",
                    "ayuda_escuela_consuelo",
                    "ayuda_escuela_hablo_",
                    "ayuda_escuela_llamo_",
                    "ayuda_escuela_aviso_",
                    "ayuda_escuela_otro_tipo",
                )
            )
            else "3.6.07"
        )
    if indicator_id.startswith("ayuda_vs_"):
        return (
            "3.6.06"
            if not indicator_id.startswith(
                (
                    "ayuda_vs_consejo",
                    "ayuda_vs_hablo_",
                    "ayuda_vs_aviso_",
                    "ayuda_vs_reclamo_",
                    "ayuda_vs_refugio",
                    "ayuda_vs_otro_tipo",
                )
            )
            else "3.6.07"
        )
    if indicator_id.startswith(("apoyo_institucional_", "brecha_institucional_")):
        return "3.6.10" if indicator_id.endswith("_vs") else "3.6.09"
    if indicator_id.startswith("ayuda_inst_vs_"):
        return "3.6.07"
    if indicator_id in {"C3P213", "C3P240", "C4P256"}:
        return "3.6.08"
    if re.fullmatch(r"C3P215_\d+|C3P242_\d+", indicator_id):
        return "3.6.09"
    if re.fullmatch(r"C4P258_\d+", indicator_id) or indicator_id in {
        "conoce_demuna",
        "uso_demuna",
        "recibio_ayuda_institucional_vs",
    }:
        return "3.6.10"
    raise ValueError(
        f"No approved editorial topic for {indicator_id!r} / {disaggregation!r}"
    )


def period_for(indicator_id: str, topic_id: str) -> str:
    if topic_id == "3.4.07":
        return "Antes de los 12 años"
    if (
        "VIDA" in indicator_id
        or indicator_id in {"VS_H_1", "VS_E_1"}
        or indicator_id.startswith(
            ("Formas_VS_E_1__", "Formas_Agresor_VS_H_1__", "Prev_Agresor_VS__")
        )
    ):
        return "Alguna vez en la vida"
    if topic_id.startswith("3.4") or topic_id in {
        "3.2.05",
        "3.2.06",
        "3.3.05",
        "3.3.06",
    }:
        return "Últimos 12 meses"
    return "No aplica"


def series_for(indicator_id: str, topic_id: str) -> str:
    if topic_id == "3.4.03":
        return (
            "Total de adolescentes"
            if indicator_id.startswith("Prev_Agresor_")
            else "Entre víctimas"
        )
    if topic_id in {
        "3.2.02",
        "3.2.04",
        "3.3.02",
        "3.3.04",
        "3.2.06",
        "3.3.06",
        "3.4.02",
    }:
        if "Agresor" in indicator_id or indicator_id.startswith("Agresor_"):
            return "Persona agresora"
        if "ICVAC" in indicator_id:
            return "Forma ICVAC"
        return "Forma reportada"
    if topic_id in {"3.6.01", "3.6.02", "3.6.03"}:
        if indicator_id.startswith("busco_"):
            return "Buscó ayuda"
        if indicator_id.startswith("recibio_"):
            return "Recibió ayuda"
        return "Brecha de ayuda"
    if topic_id == "3.1.07":
        return "Predominio" if indicator_id.startswith("predominio_") else "Componente"
    return ""


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 3014 or len({row["indicator_id"] for row in rows}) != 516:
        raise ValueError("The V0 source is not the approved 3,014-row, 516-key release")
    pairs = sorted({(row["indicator_id"], row["disaggregation"]) for row in rows})
    records: list[tuple[str, ...]] = []
    for indicator_id, disaggregation in pairs:
        topic_id = topic_for(indicator_id, disaggregation)
        scope = (
            STANDARD_SCOPE
            if disaggregation in STANDARD_DISAGGREGATIONS
            else disaggregation
        )
        records.append(
            (
                topic_id[:3],
                topic_id,
                indicator_id,
                scope,
                period_for(indicator_id, topic_id),
                series_for(indicator_id, topic_id),
                "",
            )
        )
    deduplicated = sorted(set(records))
    if len(deduplicated) != len({(row[2], row[3]) for row in deduplicated}):
        raise ValueError("An indicator/scope has conflicting assignments")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    with DESTINATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            (
                "module_id",
                "report_topic_id",
                "indicator_id",
                "disaggregation_scope",
                "period_label",
                "series_label",
                "display_label_override",
            )
        )
        writer.writerows(deduplicated)
    from types import SimpleNamespace

    loaded = load_topic_mapping(
        DESTINATION,
        catalog_rows=[
            SimpleNamespace(
                indicator_id=row["indicator_id"], disaggregation=row["disaggregation"]
            )
            for row in rows
        ],
    )
    print(
        f"{len(loaded.topics)} topics, {len(loaded.assignments)} assignments, {len(rows)} V0 rows"
    )


if __name__ == "__main__":
    main()
