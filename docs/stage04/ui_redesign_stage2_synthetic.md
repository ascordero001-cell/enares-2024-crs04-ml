# Rediseño UI — Etapa 2 sintética

- Issue: #144
- Alcance: estructura funcional, sin conexión real
- Datos: fixture en memoria `100 % sintético`
- Estado: `APPROVED_AND_MERGED`
- PR: #146
- Head aprobado: `ec42155cf38aafb6a10d0d1b33571c26366585fe`
- Merge SHA: `9eab462ae71699b196f89beb0e950d2c008daef1`

## Implementación

La maqueta funcional vive en `app/ui_redesign_synthetic_app.py` y utiliza únicamente componentes
nativos de Streamlit:

- filtros laterales de módulo, dimensión y estados;
- pestañas Panorama, Tabla, Forest plot y Estados;
- tabla con `st.dataframe`;
- forest plot con `st.vega_lite_chart`;
- mensajes semánticos de estado mediante `st.success`, `st.warning`, `st.info` y `st.error`.

No usa CSS nuevo, HTML dinámico ni `unsafe_allow_html`. Tampoco importa repositorios, abre archivos
o consulta BigQuery. El fixture se define en `app/views/ui_redesign_synthetic.py` y cada indicador
está marcado con el prefijo `SYN_`.

## Estados y protección

`cv_flag`, `n_flag` y `suppress_flag` se derivan y muestran por separado. Los estados suprimido,
contexto y pendiente no entregan estimación ni límites a la tabla o al forest plot. CV alto y N
reducido conservan el valor sintético visible con sus alertas correspondientes.

La supresión mostrada es exclusivamente un ejercicio sintético; no declara una regla activa para
V0. La combinación pendiente muestra ausencia de autorización y nunca fabrica una cifra.

## Exportación

La decisión vigente `EXPORT_ENABLED = True` de la app real no cambia. Esta maqueta sintética no
ejecuta exportación porque no es la ruta real y no debe crear un segundo contrato de descarga.

## Gate

La Etapa 3 permanece bloqueada. Rita debe revisar la estructura sintética, las pruebas AppTest y la
accesibilidad básica antes de conectar el layout al adaptador existente.
