# Stage 04 — trazabilidad del rediseño frente a la maqueta

La referencia de diseño es `MAQUETA_APP_VIGILANCIA_CRS04.html` de la carpeta
privada `01_DOCUMENTOS_RECTORES` en Mi unidad. Su SHA-256 verificado es
`AE6D141A40497D8FB55E4FCF924726BBD1E65CF6321B4B341747725C0FA304CB`.
El CSS versionado en `app/assets/stage04_mockup.css` se generó a partir de
ese archivo y del adaptador Streamlit versionado. La aplicación no necesita
acceso a Drive al ejecutarse.

El agregado V0 permanece intacto en
`app/data/v0_authorized_full_indicator_estimates.csv` (SHA-256
`9160C6B4C44DC3CE4D3FD7F94FF0DF26FAFE1ACAD99A2B0DAEE833A046778C35`):
3 014 filas, 516 claves, un release y un run. La capa editorial contiene
80 temas, con 11/18/20/9/12/10 por módulo. El CSV versionado
`src/enares/stage04/report_topic_map.csv` asigna cada par de clave técnica y
alcance de desagregación a exactamente un tema. La carga falla si aparece
una fila V0 sin asignación, una asignación sin fila o un tema inesperadamente
vacío. El módulo mostrado se deriva de esta asignación, no del módulo
técnico del archivo fuente.

Las caracterizaciones usan pares de clave y desagregación distintos de
sus prevalencias estándar; por eso `VP_HOGAR`, `VF_HOGAR`, `VP_EJERCIDA`,
`VF_EJERCIDA` y `VS_12M` tienen rutas especiales para los temas de
caracterización. Los períodos vida/12 meses/antes de los 12 años se
mantienen separados, y las categorías y magnitudes del V0 no se recalculan.
Los tres temas sin fila V0 propia son:

- `3.2.09`: no hay un agregado distinto de supervisión/abandono en el
  release; `VF_HOGAR_03` corresponde al riesgo personal o inducido por
  cuidadores y se conserva en `3.2.10`.
- `3.3.17` y `3.3.18`: no hay caracterización `VP_ESCUELA` ni
  `VF_ESCUELA` en el release vigente.

En estos temas la interfaz muestra «Sin datos en el release V0 vigente»;
no sustituye una cifra de otro tema ni fabrica cruces. Las variables
internas del universo/denominador se traducen solo en la presentación; el
texto original y los hashes del V0 se conservan. Los estados de CV alto y N
reducido se muestran con alerta, sin supresión por recuento. Una fila
efectivamente suprimida no expone su valor en tabla, gráfico, ficha ni
exportación.

Comprobaciones: `tests/test_stage04_report_topics.py`,
`tests/test_stage04_module_isolation.py`, `tests/test_stage04_exact_mockup.py`,
la suite Python y `scripts/check_mockup_parity.mjs` en navegador real. Las
capturas de navegador se generan localmente en `artifacts/ui-parity/` y no
se incorporan al contenedor privado ni al repositorio.
