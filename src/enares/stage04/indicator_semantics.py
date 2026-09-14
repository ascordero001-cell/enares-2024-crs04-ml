"""Source-verified semantics required before Stage 04 adapter integration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HouseholdTaskFemaleSemantic:
    variable: str
    task: str


D01_UNIVERSE = (
    "Adolescentes de 12 a 17 años de CRS04 incluidos en la base analítica, "
    "con respuesta válida al ítem C3P302 correspondiente"
)
D01_REPORTING_SUBJECT = "La/el adolescente entrevistada/o informa quién realiza la tarea"
D01_FEMALE_REFERENCE = ("Madre", "Hermana", "Otra mujer")
D01_TASKS = (
    HouseholdTaskFemaleSemantic("tarea1_fem", "Cocinar"),
    HouseholdTaskFemaleSemantic("tarea2_fem", "Lavar/planchar ropa"),
    HouseholdTaskFemaleSemantic("tarea3_fem", "Compras mercado"),
    HouseholdTaskFemaleSemantic("tarea4_fem", "Dar dinero/gastos"),
    HouseholdTaskFemaleSemantic("tarea5_fem", "Limpieza"),
    HouseholdTaskFemaleSemantic("tarea6_fem", "Lavar platos/utensilios"),
    HouseholdTaskFemaleSemantic("tarea7_fem", "Cuidar hermanas/os"),
    HouseholdTaskFemaleSemantic("tarea8_fem", "Ayudar con tareas escolares"),
    HouseholdTaskFemaleSemantic("tarea9_fem", "Aconsejar y escuchar"),
    HouseholdTaskFemaleSemantic("tarea10_fem", "Jugar contigo"),
)

C3P213_TARGET_VALUE = 5
C3P213_TARGET_VALUE_LABEL = "No supieron cómo ayudarme"
C3P213_DISPLAY_LABEL = "No recibió ayuda porque no supieron cómo ayudarle"
C3P213_DOMAIN = "dom_no_recibio_hogar == 1"
