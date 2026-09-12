# Sprint 04.2 — Corte 2 de cobertura funcional local

Estado: CORTE2_ENGINEERING_CHECKPOINT_APPROVED_MERGED; NUMERIC_DATA_GATE_OPEN.
El checkpoint de ingeniería fue aprobado y fusionado mediante PR #57; Sprint 04.2 no está cerrado.
Alcance: LOCAL_SHADOW_ONLY. Cloud NOT_AUTHORIZED. Presupuesto USD 0.
Exportación deshabilitada; publicación, cutover y sustitución de V0 no autorizados.

## Avance verificable

- Rama creada desde el merge del PR #56: 10692b160bcc8a0998c2b4ea622c74c066b5a952.
- Registro y navegación común 3.1–3.6; nueve dimensiones configuradas.
- 3.6 rotulado Búsqueda de ayuda.
- Golden 3.2 preservado, incluyendo el hash original del CSV:
  43f689ba9a54fb98eb3af821c76133a3ff5882abfced64dd87f0c922c3e4465e.
- Módulos sin contrato conciliado muestran sin datos; no reciben cifras por defecto.
- Pruebas negativas adicionales para identificadores de ejecución y mezcla de releases.
- Run técnico local identificado como sprint042-corte2-local-coverage-001; no modifica
  current_release ni crea una ejecución cloud.
- Matriz detallada módulo × indicador × nueve dimensiones creada con estado de datos y
  evidencia fail-closed por combinación.
- Barrera de autorización reforzada en dos capas: la validación central rechaza toda fila V0
  cuya dimensión no esté en `authorized_dimensions`, y la interfaz detiene el flujo antes de
  consultar el repositorio cuando la combinación no está autorizada.
- La disponibilidad observada en V0 no concede autorización. Solo 3.2 / `VF_HOGAR` /
  `Nacional` continúa autorizado; el fixture sintético conserva sus estados didácticos.

## Conciliación del catálogo y gate restante

En la lectura de Drive se verificaron los hashes del agregado y del diccionario:

- tabulados_crs04_long.csv:
  15B845DA4A886FDCF54A96D8B8471B6F6BE618AE18B43024488C6BD6B23D0BB4.
- diccionario_indicadores.csv:
  F5FD6979A19EBC9F510C307705B1E7DE12556A8F5A81DDBC566E97347337BD2C.

El borrador anterior derivó 74 filas y asignó flags de calidad falsos por defecto.
Esa ampliación fue retirada antes de publicar: la fuente no entregaba esos estados.
La aplicación vuelve a consumir exclusivamente el CSV y el manifiesto aprobados de 3.2.

Para ampliar cifras se necesita resolver:

1. Resuelto mediante diccionario y paquete rector de Drive: 3.1 selecciona
   justifica_castigo_parental/docente y 3.5 PV_hogar_escuela. Evidencia:
   indicator_reconciliation_corte2.md. Los centinelas previos no se usan para esas tarjetas.
2. Resuelto por aclaración de la usuaria: N del denominador usa exclusivamente base_unw.
   La función denominator_count rechaza valores ausentes o inválidos sin sustituirlos.
3. Resuelto documentalmente: los catálogos completos 3.1–3.6 fueron cruzados con
   diccionario y agregado. Resultado: 516 indicadores y 3014 filas, sin IDs sin salida.
   Evidencia: reconciliation_modules_31_36.md y los seis registros por módulo.
4. Pendiente: estados de calidad y supresión explícitamente autorizados para las filas nuevas.
5. Pendiente: adaptadores para salidas special/incomplete y decisiones sobre estadísticas
   vacías documentadas en 3.4–3.6; no se sustituyen valores ausentes.
6. Resuelto: run de evidencia técnica `sprint042-corte2-local-coverage-001`, preservando
   el manifiesto del golden anterior. No se
   atribuye retroactivamente al CSV legado ni al golden 3.2.

## Verificación y pendientes

La suite anterior obtuvo 213 passed, pero no comprobaba en todas las capas la autorización de
esos estados. Se añadieron pruebas negativas de validación y repositorio, prueba positiva del
golden y AppTest para asegurar que la UI se detiene antes de consultar filas no autorizadas.
Resultado local actual: 220 passed, 0 failed, incluidos los gates de autorización y diez
pruebas de la conversión de N.
Ejecutado con Python 3.12 y pytest, deshabilitando
la caché y usando una carpeta temporal nueva por permisos del entorno Windows.
Incluye AppTest de navegación y ausencia de cifras pendientes; no acredita su autorización.
git diff --check: sin errores de whitespace en los cambios de trabajo.

Se renovaron capturas de resumen, módulos 3.1–3.6, estados, selector cerrado/abierto y ancho
reducido. La revisión HCI local a 1280 × 900 y 390 × 844 confirmó navegación por teclado, foco
visible, etiquetas, selector legible, botón Exportar deshabilitado y ausencia de solapamiento.
El clon limpio reprodujo 220 passed y Dataform compiló 44 acciones. La CI del SHA revisado quedó
aprobada. La comprensión de etiquetas por una persona revisora y los gates
numéricos/metodológicos continúan pendientes antes de cerrar el sprint.

No se declara cerrado Sprint 04.2. La revisión del PR no autoriza cifras nuevas, cloud,
exportación, publicación ni cutover.
