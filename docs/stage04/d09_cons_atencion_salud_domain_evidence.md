# Evidencia de dominio D09 — `CONS_ATENCION_SALUD`

**Estado:** `DOMAIN_APPROVED; R_V0_STRUCTURAL_EQUIVALENCE_VERIFIED; NUMERIC_SCOPE_PENDING`
**Decisión:** Rita, 2026-09-13, revisión del PR #60
**Alcance:** contraste de solo lectura; no conecta cifras a la aplicación ni modifica V0.

## Contrato aprobado

| Campo | Definición |
|---|---|
| Indicador | `CONS_ATENCION_SALUD` |
| Módulo | 3.5 Consecuencias |
| Dominio | `CONS_ALGUNA = 1` |
| Numerador | `CONS_ATENCION_SALUD = 1` dentro del dominio |
| Denominador | Respuestas válidas de `CONS_ATENCION_SALUD` dentro de `CONS_ALGUNA = 1` |
| N visible | `base_unw` del denominador condicionado |
| Fuera del dominio | `CONS_ATENCION_SALUD = NULL`; no integra el denominador |

## Trazabilidad R/V0

Se releyeron directamente en Drive privado los objetos de la baseline aprobada, identificados por
el manifiesto existente:

- productor R `tabulados.R`, SHA-256
  `A45A73F40D728713A52800653991EBDBFF4E80A0D9A6A8318E8D7BD266597C1D`;
- especificaciones R V0 `stage3_r_tabulation_specs.csv`;
- salida `tabulados_crs04_long.csv`, SHA-256
  `15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4`;
- diccionario V0 `diccionario_indicadores.csv`, SHA-256
  `F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C`.

El diccionario y las especificaciones no rellenan `domain_variable/domain_value` para D09, pero
declaran tratamiento literal de `SYSMIS/NULL` y `na.rm` en R. La salida V0 demuestra la restricción:
para los 22 pares exactos de D09, `base_unw(CONS_ATENCION_SALUD)` coincide 22/22 con
`target_unw(CONS_ALGUNA)` del mismo par. No se registran aquí los valores para evitar incorporar
nuevas cifras reales al PR.

La implementación Stage 03 conservada en
`scripts/generate_stage35_dataform.py` expresa la misma regla: produce `NULL` cuando
`CONS_ALGUNA != 1` o es `NULL`. La sintaxis SPSS 3.5 congelada la confirma en los bloques
L663–675 y L748–762. Por tanto, el productor R excluye fuera de dominio mediante missing y su
`base_unw` equivale al filtro explícito `CONS_ALGUNA = 1` con respuesta válida.

## Prueba sintética

`tests/test_stage04_candidate_adapter.py` prueba que:

- únicamente respuestas 0/1 válidas dentro de `CONS_ALGUNA = 1` integran `base_unw`;
- únicamente el valor 1 integra `target_unw`;
- ausencias dentro del dominio no se imputan;
- cualquier valor observado fuera del dominio se rechaza;
- el helper rechaza filas no marcadas explícitamente como sintéticas.

## Límite

La equivalencia del denominador está resuelta. La autorización de los 22 pares y de sus cifras
continúa pendiente. Stage 04 no recalcula D09 en la interfaz ni sobrescribe la baseline.
