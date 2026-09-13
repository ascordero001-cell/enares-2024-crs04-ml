# Decisiones supervisoras de Stage 04 — 2026-09-13

**Autoridad:** Rita Ricaldi (`ritaricaldi-cpu`)
**Evidencia:** [revisión del PR #60](https://github.com/ascordero001-cell/enares-2024-crs04-ml/pull/60#pullrequestreview-5191297314)
**Alcance:** implementación local y pruebas sintéticas; no autoriza cifras nuevas ni publicación.

## Resuelto

1. En 3.1–3.6, CV > 15 % conserva la prevalencia visible, la clasifica como referencial y añade:
   “Estimación referencial por precisión reducida: CV superior al 15 %. Interpretar con cautela.”
2. En 3.1–3.6, N no ponderado < 30 conserva la prevalencia visible y añade:
   “Estimación basada en menos de 30 observaciones no ponderadas. Interpretar con cautela.”
   N procede exclusivamente de `base_unw`.
3. En 3.5, `CONS_ATENCION_SALUD` se estima dentro de `CONS_ALGUNA = 1`, usando respuestas
   válidas como denominador condicionado.
4. El presupuesto máximo total de Stage 04 es USD 20 mensuales. Ana y Rita son las
   administradoras designadas.

CV/N son señales de calidad, no reglas de confidencialidad. No activan automáticamente
`suppress_flag`. La igualdad CV=15 % o N=30 no activa la alerta; ausencias no se imputan.

## Pendiente

- autorización exacta de nuevas cifras por indicador, dimensión y categoría;
- tratamiento final de familias incompletas/especiales y tolerancia de paridad;
- política independiente de confidencialidad y riesgo de reconstrucción;
- identidades privadas, roles, billing, alertas, límites y pruebas efectivas de acceso;
- GO/NO-GO técnico del primer despliegue y cualquier publicación o cutover.

Este registro no cambia V0, sus hashes, los scripts R, las sintaxis SPSS ni los golden históricos.
