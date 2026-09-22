"""Human-readable, presentation-only labels for the approved V0 catalog.

The release keeps its immutable ``indicator_id`` and ``indicator_name`` fields.
This module only translates those identifiers for the UI using the approved
questionnaire dictionaries and the semantics already versioned in Stage 03/04.
"""

from __future__ import annotations

import re

MODULE_LABELS = {
    "3.1": "Características y percepciones",
    "3.2": "Violencia en el hogar",
    "3.3": "Violencia en el entorno escolar",
    "3.4": "Violencia sexual",
    "3.5": "Acumulación de violencias",
    "3.6": "Búsqueda de ayuda",
}

PSYCHOLOGICAL_HOME_ITEMS = {
    1: "Insultos o lisuras que hacen sentir mal",
    2: "Apodos que hacen sentir mal",
    3: "Descalificación de lo que hace o dice",
    4: "Burlas",
    5: "Humillación o vergüenza",
    6: "Amenaza de golpe o abandono",
    7: "Amenaza de muerte",
    8: "Encierro",
    9: "Expulsión o amenaza de expulsión del hogar",
    10: "Prohibición de jugar con pares",
    11: "Otra situación de violencia psicológica",
}

PHYSICAL_HOME_ITEMS = {
    1: "Jalones de cabello u orejas",
    2: "Cachetadas o nalgadas",
    3: "Patadas, mordidas o puñetazos",
    4: "Golpes con objetos",
    5: "Quemaduras",
    6: "Ataque con cuchillo, arma u otro objeto",
    7: "Otra situación de violencia física",
}

PSYCHOLOGICAL_SCHOOL_ITEMS = {
    1: "Insultos, burlas o desprecio",
    2: "Apodos o chapas que hacen sentir mal",
    3: "Comparación desfavorable con otras personas",
    4: "Descalificación de lo que hace o dice",
    5: "Rechazo, aislamiento o exclusión del grupo",
    6: "Daño o intento de daño a sus pertenencias",
    7: "Ocultamiento de sus pertenencias",
    8: "Chismes que hacen sentir mal",
    9: "Difusión en internet de fotos o videos que avergüenzan",
    10: "Mensajes ofensivos virtuales o escritos",
    11: "Encierro en el colegio",
    12: "Amenaza de daño físico",
    13: "Amenaza de muerte",
    14: "Otra situación de violencia psicológica",
}

PHYSICAL_SCHOOL_ITEMS = {
    1: "Jalones de cabello u orejas",
    2: "Cachetadas, cocachos, pellizcos o nalgadas",
    3: "Patadas, puñetazos, codazos o rodillazos",
    4: "Golpes con objetos",
    5: "Ahorcamiento o intento de asfixia",
    6: "Daño con lápiz, lapicero o regla",
    7: "Quemaduras",
    8: "Ataque con objetos filudos",
    9: "Ataque con pistola",
    10: "Otra situación de violencia física",
}

SEXUAL_VIOLENCE_ITEMS = {
    1: "Miradas a partes íntimas que causan incomodidad",
    2: "Comentarios o bromas de tipo sexual",
    3: "Exposición forzada a desnudez o relaciones sexuales",
    4: "Intento de quitarle la ropa contra su voluntad",
    5: "Obligación de tocar el cuerpo de otra persona",
    6: "Tocamientos incómodos en el cuerpo",
    7: "Masturbación de otra persona delante de la o el adolescente",
    8: "Obligación de masturbarse",
    9: "Exhibición de genitales",
    10: "Amenaza para tener relaciones sexuales",
    11: "Relaciones sexuales forzadas",
    12: "Otra situación de violencia sexual",
    13: "Abuso de confianza con intención sexual",
    14: "Llamadas o mensajes privados de tipo sexual",
    15: "Amenaza de publicar contenido íntimo",
    16: "Difusión de contenido íntimo sin permiso",
}

INSTITUTIONS_HOME = {
    1: "Comisaría",
    2: "Juzgado o Juez de Paz",
    3: "Fiscalía o Ministerio Público",
    4: "DEMUNA",
    5: "Unidad de Protección Especial (UPE)",
    6: "Centro Emergencia Mujer (CEM)",
    7: "Sector educación (Minedu, DRE o UGEL)",
    8: "Establecimiento de salud",
    9: "Gobernación",
    10: "Otra institución",
    11: "No sabe a qué institución acudió",
}

INSTITUTIONS_SCHOOL_OR_VS = {
    1: "Comisaría",
    2: "Juzgado o Juez de Paz",
    3: "Fiscalía o Ministerio Público",
    4: "DEMUNA",
    5: "Unidad de Protección Especial (UPE)",
    6: "Centro Emergencia Mujer (CEM)",
    7: "Sector educación (Minedu, DRE o UGEL)",
    8: "Dirección de la institución educativa",
    9: "Establecimiento de salud",
    10: "Gobernación",
    11: "Otra institución",
    12: "No sabe a qué institución acudió",
}

CONSEQUENCE_ITEMS = {
    1: "Moretones o hinchazones",
    2: "Heridas o cicatrices",
    3: "Fracturas o dientes rotos",
    4: "Sangrado",
    5: "Quemaduras",
    6: "Otra consecuencia física",
}

AGGRESSOR_GROUPS = {
    1: "Familiares",
    2: "Familiares mujeres",
    3: "Familiares hombres",
    4: "Otros ascendientes",
    5: "Estudiantes del mismo u otro colegio",
    6: "Otra persona",
    7: "Pareja o expareja",
    8: "Personas adultas del colegio",
    9: "Personal de centro de acogida residencial",
}

HOUSEHOLD_AGGRESSOR_GROUPS = {
    1: "Madre",
    2: "Padre",
    3: "Madrastra",
    4: "Padrastro",
    5: "Hermana, hermano, hermanastra o hermanastro con rol parental",
    6: "Tía o tío con rol parental",
    7: "Personal adulto de centro de acogida residencial",
    8: "Otros familiares o ascendientes con rol parental",
}

SCHOOL_AGGRESSOR_GROUPS = {
    1: "Compañera o compañero del salón",
    2: "Compañera o compañero del salón de mayor edad",
    3: "Compañera o compañero del salón de la misma edad",
    4: "Compañera o compañero del salón de menor edad",
    5: "Estudiante de otra aula del mismo colegio",
    6: "Estudiante de otra aula del mismo colegio de mayor edad",
    7: "Estudiante de otra aula del mismo colegio de la misma edad",
    8: "Estudiante de otra aula del mismo colegio de menor edad",
    9: "Estudiante de otro colegio",
}

ICVAC_COMPONENTS = {
    "201": "Agresión física grave",
    "202": "Agresión física leve",
    "203": "Aislamiento",
    "209": "Otra forma de violencia física",
    "301": "Violación",
    "302": "Agresión sexual con contacto",
    "303": "Violencia sexual sin contacto",
    "309": "Otra situación de violencia sexual",
    "401": "Aterrorizar",
    "402": "Hostigar o humillar",
    "409": "Otra violencia psicológica",
}

CP_COMPONENTS = {
    1: "Acoso sexual verbal o visual",
    2: "Exposición sexual no consentida",
    3: "Tocamientos u otros actos con contacto",
    4: "Amenaza para tener relaciones sexuales",
    5: "Relaciones sexuales forzadas",
    6: "Abuso de confianza con intención sexual",
    7: "Mensajes privados de tipo sexual",
    8: "Amenaza o difusión de contenido íntimo",
    9: "Otra situación de violencia sexual",
}

EXACT_LABELS = {
    "AG_VF_09": "Violencia física escolar: otra persona agresora",
    "AG_VP_09": "Violencia psicológica escolar: otra persona agresora",
    "CONS_ALGUNA": "Alguna consecuencia de la violencia",
    "CONS_ATENCION_SALUD": "Atención de salud por consecuencias de la violencia",
    "Componentes": "Corresponsabilidad cotidiana en el hogar",
    "Hogar__VP_o_VF_HOGAR": (
        "Composición entre casos con violencia psicológica o física en el hogar"
    ),
    "HoraClase_ViolEsc": "Violencia escolar durante la clase",
    "HoraEntrada_ViolEsc": "Violencia escolar a la entrada",
    "HoraRecreo_ViolEsc": "Violencia escolar durante el recreo",
    "HoraSalida_ViolEsc": "Violencia escolar a la salida",
    "INDICADOR_8_2_7": "Violencia sexual reciente por persona distinta de la pareja",
    "INDICADOR_8_2_13": "Acoso sexual reciente por persona distinta de la pareja",
    "INDICADOR_8_2_8": "Primera situación de violencia sexual antes de los 12 años",
    "INDICADOR_8_3_6": "Violencia sexual ejercida por pareja o expareja",
    "INDICADOR_8_3_9": "Violencia sexual ejercida por una persona conocida",
    "LugarBano_ViolEsc": "Violencia escolar en el baño",
    "LugarFueraColegio_ViolEsc": "Violencia escolar fuera del colegio",
    "LugarOtro_ViolEsc": "Violencia escolar en otro lugar",
    "LugarPasilloEscalera_ViolEsc": "Violencia escolar en pasillos o escaleras",
    "LugarPatio_ViolEsc": "Violencia escolar en el patio",
    "LugarSalon_ViolEsc": "Violencia escolar en el salón",
    "PV_VF_hogar_VP_escuela": "Violencia física en el hogar y psicológica en la escuela",
    "PV_VF_hogar_escuela": "Violencia física en el hogar o la escuela",
    "PV_VP_VF_hogar_escuela": "Violencia psicológica o física en el hogar y la escuela",
    "PV_VP_VF_hogar_escuela_VS": "Violencias psicológica, física y sexual acumuladas",
    "PV_VP_hogar_VF_escuela": "Violencia psicológica en el hogar y física en la escuela",
    "PV_VP_hogar_escuela": "Violencia psicológica en el hogar o la escuela",
    "PV_condicional_con_VS": "Acumulación de violencia condicionada a violencia sexual",
    "PV_condicional_escuela_dado_hogar": "Violencia escolar entre quienes reportaron violencia en el hogar",
    "PV_condicional_escuela_sin_hogar": "Violencia escolar sin violencia en el hogar",
    "PV_condicional_hogar_dado_escuela": "Violencia en el hogar entre quienes reportaron violencia escolar",
    "PV_condicional_hogar_sin_escuela": "Violencia en el hogar sin violencia escolar",
    "PV_hogar_escuela": "Violencia acumulada en hogar y escuela",
    "PV_hogar_escuela1": "Violencia acumulada en hogar y escuela (clasificación complementaria)",
    "Solap_VP_VF_E": "Solapamiento de violencia psicológica y física en la escuela",
    "Solap_VP_VF_E__Coexistencia": "Coexistencia de violencia psicológica y física en la escuela",
    "Solap_VP_VF_H": "Solapamiento de violencia psicológica y física en el hogar",
    "Solap_VP_VF_H__Coexistencia": "Coexistencia de violencia psicológica y física en el hogar",
    "Solap_VS_12M": "Solapamiento de formas de violencia sexual en los últimos 12 meses",
    "Solap_VS_VIDA": "Solapamiento de formas de violencia sexual alguna vez",
    "VF_EJERCIDA": "Violencia física ejercida por la o el adolescente",
    "VF_ESCUELA": "Violencia física en la escuela",
    "VF_HOGAR": "Violencia física en el hogar",
    "VF_HOGAR_01": "Violencia física leve en el hogar",
    "VF_HOGAR_03": "Violencia física grave en el hogar",
    "VN_HOGAR1": "Negligencia en el hogar",
    "VP_EJERCIDA": "Violencia psicológica ejercida por la o el adolescente",
    "VP_ESCUELA": "Violencia psicológica en la escuela",
    "VP_HOGAR": "Violencia psicológica en el hogar",
    "VP_VF_E": "Violencia psicológica y física en la escuela",
    "VP_VF_HOGAR": "Violencia psicológica y física en el hogar",
    "VP_VF_VS_E": "Violencia psicológica, física o sexual en la escuela",
    "VP_VF_VS_HOGAR": (
        "Concurrencia de violencia psicológica, física y sexual en el hogar"
    ),
    "VP_o_VF_E": "Violencia psicológica o física en la escuela",
    "VP_o_VF_EJERCIDA": "Violencia psicológica o física ejercida",
    "VP_o_VF_ESCUELA": "Violencia psicológica o física en la escuela",
    "VP_o_VF_HOGAR": "Violencia psicológica o física en el hogar",
    "VP_o_VF_HOGAR__VP_o_VF_HOGAR": (
        "Prevalencia de violencia psicológica o física en el hogar"
    ),
    "VP_o_VF_o_VS_HOGAR": ("Alguna violencia psicológica, física o sexual en el hogar"),
    "VS": "Alguna situación de violencia sexual",
    "VS_12M": "Violencia sexual en los últimos 12 meses",
    "VS_E": "Violencia sexual en la escuela en los últimos 12 meses",
    "VS_E_1": "Violencia sexual en la escuela alguna vez",
    "VS_H": "Violencia sexual en el hogar en los últimos 12 meses",
    "VS_H_1": "Violencia sexual en el hogar alguna vez",
    "VS_OtraPersona_12M": "Violencia sexual reciente por otra persona",
    "VS_OtraPersona_VIDA": "Violencia sexual alguna vez por otra persona",
    "VS_VIDA": "Violencia sexual alguna vez",
    "apoyo_institucional_escuela": "Apoyo institucional ante violencia escolar",
    "apoyo_institucional_hogar": "Apoyo institucional ante violencia en el hogar",
    "apoyo_institucional_vs": "Apoyo institucional ante violencia sexual",
    "brecha_institucional_escuela": "Brecha de apoyo institucional ante violencia escolar",
    "brecha_institucional_hogar": "Brecha de apoyo institucional ante violencia en el hogar",
    "brecha_institucional_vs": "Brecha de apoyo institucional ante violencia sexual",
    "justifica_castigo_docente": "Justificación del castigo por docentes",
    "justifica_castigo_parental": "Justificación del castigo parental",
    "mito_fuera_casa": "Mito: la violencia sexual ocurre mayormente fuera de casa",
    "mito_locas": "Mito: la violencia sexual solo la cometen personas con trastornos",
    "mito_pobreza": "Mito: la violencia sexual solo afecta a personas pobres",
    "mito_sitios_oscuros": "Mito: la violencia sexual ocurre más en lugares oscuros",
    "num_consecuencias_fisicas": "Número de consecuencias físicas reportadas",
    "predominio_femenino_tareas": "Predominio femenino en tareas y cuidados del hogar",
    "rechaza_dejar_estudiar": "Rechazo a impedir que niñas y adolescentes estudien",
    "rechaza_trabajo_infantil_necesidad": "Rechazo al trabajo infantil por necesidad económica",
    "reconoce_derecho_denunciar": "Reconocimiento del derecho a denunciar violencia",
    "reconoce_derecho_opinar": "Reconocimiento del derecho a opinar",
    "conoce_demuna": "Conocimiento de la DEMUNA",
    "uso_demuna": "Uso de la DEMUNA",
    "C3P213": "No recibió ayuda porque no supieron cómo ayudarle",
    "C3P240": "No recibió ayuda ante violencia escolar: motivo reportado",
    "C4P256": "No recibió ayuda ante violencia sexual: motivo reportado",
    "recibio_ayuda_institucional_vs": (
        "Recibió ayuda institucional ante violencia sexual"
    ),
}

HELP_CONTEXTS = {
    "hogar": "violencia en el hogar",
    "escuela": "violencia escolar",
    "vs": "violencia sexual",
}
HELP_PEOPLE = {
    "madre": "madre",
    "padre": "padre",
    "madrastra": "madrastra",
    "padrastro": "padrastro",
    "hermana": "hermana",
    "hermano": "hermano",
    "abuela": "abuela",
    "abuelo": "abuelo",
    "tia": "tía",
    "tio": "tío",
    "otro_pariente": "otro pariente",
    "familiar": "familiar",
    "pares_amigos": "pares o amistades",
    "escolar_adulto": "persona adulta del colegio",
    "car": "persona del centro de acogida residencial",
    "otro": "otra persona",
}


def _item_label(indicator_id: str) -> str | None:
    patterns = (
        (
            r"C3P201_(\d+)_1$",
            PSYCHOLOGICAL_HOME_ITEMS,
            "Violencia psicológica en el hogar",
        ),
        (r"C3P205_(\d+)_1,?$", PHYSICAL_HOME_ITEMS, "Violencia física en el hogar"),
        (
            r"C3P223_(\d+)_1$",
            PSYCHOLOGICAL_SCHOOL_ITEMS,
            "Violencia psicológica escolar",
        ),
        (r"C3P227_(\d+)_1$", PHYSICAL_SCHOOL_ITEMS, "Violencia física escolar"),
    )
    for pattern, labels, context in patterns:
        match = re.fullmatch(pattern, indicator_id)
        if match:
            return f"{context}: {labels[int(match.group(1))]}"
    return None


def _institution_label(indicator_id: str) -> str | None:
    match = re.fullmatch(r"(C3P215|C3P242|C4P258)_(\d+)", indicator_id)
    if not match:
        return None
    series, number = match.group(1), int(match.group(2))
    context = {
        "C3P215": "violencia en el hogar",
        "C3P242": "violencia escolar",
        "C4P258": "violencia sexual",
    }[series]
    labels = INSTITUTIONS_HOME if series == "C3P215" else INSTITUTIONS_SCHOOL_OR_VS
    return f"Institución buscada por {context}: {labels[number]}"


def _sexual_form_label(indicator_id: str) -> str | None:
    match = re.fullmatch(r"(Formas_[A-Za-z0-9_]+)__C4P248_(\d+)", indicator_id)
    if not match:
        return None
    scope, number = match.group(1), int(match.group(2))
    scope_label = {
        "Formas_VS_12M": "Violencia sexual en los últimos 12 meses",
        "Formas_VS_VIDA": "Violencia sexual alguna vez",
        "Formas_VS_E": "Violencia sexual en la escuela en los últimos 12 meses",
        "Formas_VS_E_1": "Violencia sexual en la escuela alguna vez",
        "Formas_Agresor_VS_H": "Violencia sexual en el hogar en los últimos 12 meses",
        "Formas_Agresor_VS_H_1": "Violencia sexual en el hogar alguna vez",
    }[scope]
    return f"{scope_label}: {SEXUAL_VIOLENCE_ITEMS[number]}"


def _grouped_sexual_label(indicator_id: str) -> str | None:
    match = re.fullmatch(
        r"(Formas_[A-Za-z0-9_]+)__(?:VS|VSE|VSH)_(CP\d+)", indicator_id
    )
    if match:
        scope, code = match.groups()
        timing = (
            "alguna vez"
            if scope.endswith("_1") or "VIDA" in scope
            else "últimos 12 meses"
        )
        place = (
            "en la escuela"
            if "VS_E" in scope
            else "en el hogar"
            if "VS_H" in scope
            else ""
        )
        return (
            f"Violencia sexual {place} ({timing}), componente CP: "
            f"{CP_COMPONENTS[int(code[-2:])]}"
        ).replace("  ", " ")
    match = re.fullmatch(r"(Formas_[A-Za-z0-9_]+)__ICVAC_(\d+)", indicator_id)
    if match:
        scope, code = match.groups()
        timing = (
            "alguna vez"
            if scope.endswith("_1") or "VIDA" in scope
            else "últimos 12 meses"
        )
        place = (
            "en la escuela"
            if "VS_E" in scope
            else "en el hogar"
            if "VS_H" in scope
            else ""
        )
        return (
            f"Violencia sexual {place} ({timing}), clasificación ICVAC: "
            f"{ICVAC_COMPONENTS[code]}"
        ).replace("  ", " ")
    return None


def _aggressor_label(indicator_id: str) -> str | None:
    match = re.fullmatch(
        r"(Agresor|Prev_Agresor)_VS_(12M|VIDA)?_?_*AG_(\d+)", indicator_id
    )
    if match:
        family, period, number_text = match.groups()
        number = int(number_text)
        timing = "últimos 12 meses" if period == "12M" else "alguna vez"
        if family == "Prev_Agresor":
            return (
                f"Prevalencia de violencia sexual según persona agresora "
                f"({timing}): {AGGRESSOR_GROUPS[number]}"
            )
        return (
            f"Distribución de personas agresoras entre víctimas de violencia "
            f"sexual ({timing}): {AGGRESSOR_GROUPS[number]}"
        )
    match = re.fullmatch(r"Agresor_(V[PF])_([EH])__AG_V[PF]_(\d+)", indicator_id)
    if match:
        violence, place, group_number = match.groups()
        kind = "física" if violence == "VF" else "psicológica"
        setting = "escuela" if place == "E" else "hogar"
        groups = SCHOOL_AGGRESSOR_GROUPS if place == "E" else HOUSEHOLD_AGGRESSOR_GROUPS
        return f"Violencia {kind} en {setting}: persona agresora: {groups[int(group_number)]}"
    return None


def _help_label(indicator_id: str) -> str | None:
    match = re.fullmatch(r"ayuda_(hogar|escuela|vs)_(.+)", indicator_id)
    if match:
        context, detail = match.groups()
        if detail in HELP_PEOPLE:
            return f"Persona a quien pidió ayuda por {HELP_CONTEXTS[context]}: {HELP_PEOPLE[detail]}"
        action = (
            detail.replace("_", " ").replace("hablo", "habló").replace("llamo", "llamó")
        )
        return f"Ayuda recibida por {HELP_CONTEXTS[context]}: {action}"
    match = re.fullmatch(r"ayuda_inst_vs_(.+)", indicator_id)
    if match:
        return "Respuesta institucional ante violencia sexual: " + match.group(
            1
        ).replace("_", " ")
    match = re.fullmatch(
        r"(busco|recibio)_ayuda_(hogar|escuela|vs)(?:_victimas)?", indicator_id
    )
    if match:
        action, context = match.groups()
        verb = "Buscó ayuda" if action == "busco" else "Recibió ayuda"
        denominator = (
            " entre víctimas"
            if indicator_id.endswith("_victimas")
            else " entre quienes buscaron ayuda"
            if action == "recibio"
            else ""
        )
        return f"{verb} por {HELP_CONTEXTS[context]}{denominator}"
    match = re.fullmatch(r"brecha_ayuda_(hogar|escuela|vs)", indicator_id)
    if match:
        return f"Brecha entre búsqueda y recepción de ayuda por {HELP_CONTEXTS[match.group(1)]}"
    return None


def _remaining_structured_label(indicator_id: str) -> str | None:
    match = re.fullmatch(r"C3P233_(1A|1|2A|2|3)_1", indicator_id)
    if match:
        descriptions = {
            "1": "Golpeó a estudiante del mismo colegio",
            "1A": "Golpeó a estudiante de otro colegio",
            "2": "Insultó o amenazó a estudiante del mismo colegio",
            "2A": "Insultó o amenazó a estudiante de otro colegio",
            "3": "Excluyó o ignoró a estudiante del mismo colegio",
        }
        return "Violencia ejercida: " + descriptions[match.group(1)]
    match = re.fullmatch(r"C3P243_(T)?(\d+)", indicator_id)
    if match:
        attended, number = match.groups()
        label = CONSEQUENCE_ITEMS[int(number)]
        return (
            f"Atención de salud por {label.lower()}"
            if attended
            else f"Consecuencia física: {label}"
        )
    match = re.fullmatch(r"(VFE|VF|VPE|VP)_ICVAC_(\d+)_.+", indicator_id)
    if match:
        prefix, code = match.groups()
        setting = "escuela" if prefix.endswith("E") else "hogar"
        return f"{ICVAC_COMPONENTS[code]} en {setting}"
    match = re.fullmatch(
        r"Formas_(VS_12M|VS_VIDA|VS_E(?:_1)?|Agresor_VS_H(?:_1)?)__"
        r"(?:VS|VSE|VSH)_AG(\d+)",
        indicator_id,
    )
    if match:
        scope, group_number = match.groups()
        timing = (
            "alguna vez"
            if scope.endswith("_1") or scope == "VS_VIDA"
            else "últimos 12 meses"
        )
        place = (
            " en el hogar"
            if "VS_H" in scope
            else " en la escuela"
            if "VS_E" in scope
            else ""
        )
        return (
            f"Persona agresora de violencia sexual{place} ({timing}): "
            f"{AGGRESSOR_GROUPS[int(group_number)]}"
        )
    return None


def indicator_option_label(indicator_id: str, module_id: str) -> str:
    """Return the accessible selector text with the immutable code second."""
    return f"{indicator_display_name(indicator_id, module_id)} — {indicator_id}"


def _fallback_label(indicator_id: str, module_id: str) -> str:
    words = indicator_id.replace("__", ": ").replace("_", " ").replace(",", "")
    words = re.sub(r"\bVP\b", "violencia psicológica", words)
    words = re.sub(r"\bVF\b", "violencia física", words)
    words = re.sub(r"\bVS\b", "violencia sexual", words)
    words = re.sub(r"\b12M\b", "últimos 12 meses", words)
    words = re.sub(r"\bVIDA\b", "alguna vez", words)
    words = re.sub(r"\s+", " ", words).strip()
    if words.casefold() == indicator_id.casefold():
        return f"Indicador de {MODULE_LABELS[module_id]}"
    return words[0].upper() + words[1:]


def indicator_display_name(indicator_id: str, module_id: str) -> str:
    """Return a stable human label while preserving the code outside this function."""
    if indicator_id in EXACT_LABELS:
        return EXACT_LABELS[indicator_id]
    for resolver in (
        _item_label,
        _institution_label,
        _sexual_form_label,
        _grouped_sexual_label,
        _aggressor_label,
        _help_label,
        _remaining_structured_label,
    ):
        label = resolver(indicator_id)
        if label:
            return label
    return _fallback_label(indicator_id, module_id)
