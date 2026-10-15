# Acceso privado del piloto Stage 04

**Decisión supervisora:** issue #149, comentario del 2026-10-13. El acceso
autorizado usa Identity Platform (correo/contraseña), IAP con identidades
externas y un backend Cloud Run privado. El formulario público separado solo
sirve `Usuario`, `Contraseña` e `Ingresar`; traduce el alias visible
`vigilancia` a una identidad interna. No contiene V0 ni puede consultar el
repositorio. La credencial compartida no identifica individualmente a cada
persona usuaria.

El flujo anterior de hash PBKDF2 dentro de Streamlit se retiró. En modo
`AUTHENTICATED_SHADOW`, la aplicación **rechaza antes de abrir V0** una
petición sin JWT firmado por IAP, con audiencia exacta del servicio piloto,
emisor IAP, proveedor Identity Platform `password` y UID aprobado. Ninguna
cabecera de identidad sin firma ni variable de sesión sustituye esa prueba.
La ausencia de configuración falla cerrada.

## Configuración del piloto

- Servicio principal `enares-stage04-shadow`: sin cambios durante el piloto.
- Backend piloto `enares-stage04-iap-pilot`: IAP activo, `roles/run.invoker`
  solo para la cuenta técnica de IAP; nunca `allUsers` ni
  `allAuthenticatedUsers`.
- Servicio de autenticación: imagen aislada de `auth_ui/`, sin código de V0;
  `STAGE04_FIREBASE_API_KEY`, `STAGE04_FIREBASE_AUTH_DOMAIN` y
  `STAGE04_IDP_EMAIL` son configuración pública del cliente, no contraseñas.
  `STAGE04_PILOT_URL` apunta al origen privado al que se vuelve tras cerrar
  la cookie IAP para iniciar un flujo nuevo.
- Backend: `STAGE04_IAP_PROJECT_NUMBER`, `STAGE04_IAP_REGION`,
  `STAGE04_IAP_SERVICE`, `STAGE04_IAP_EXPECTED_UID` y
  `STAGE04_IAP_SERVICE_URL`. El UID debe proceder de la cuenta creada en
  Identity Platform, no de lo que envía el navegador.
- La contraseña debe ser **nueva y fuerte**, administrada en Identity
  Platform y rotada antes del piloto. Nunca se coloca en Git, imagen, logs,
  URLs, variables de entorno visibles ni comentarios. La recuperación se
  realiza mediante el correo interno de la identidad y el flujo de
  restablecimiento de Identity Platform; una rotación revoca la clave anterior.

## Inactividad y verificación

El cliente borra filtros, resultados y estado a los 300 s de inactividad.
El cierre debe terminar la cookie IAP mediante
`?gcp-iap-mode=GCIP_SIGNOUT` y volver al formulario. La política IAP `LOGIN`
con `maxAge=300s` **no cubre identidades externas**, según la documentación
de Google; no se la cuenta como control de este requisito. Hasta comprobar
en navegador el cierre y reingreso obligatorios, el piloto no se promueve.

El formulario utiliza persistencia de credenciales solo en memoria de la
página, no en almacenamiento de sesión ni local. Aplica espera creciente en
el cliente tras tres errores; Identity Platform también dispone de límites
de abuso propios. El servicio de formulario registra únicamente el evento
fijo `stage04_login_denied`, sin usuario, contraseña ni detalle del error.
Ese evento ayuda a investigar fallos del formulario, **pero no es un contador
autoritativo**: un cliente que llame directamente a la API puede omitirlo.
No se habilita reCAPTCHA ni registro de actividad de Identity Platform sin
evaluar antes el costo y la posible retención de datos.

## Estado del piloto al 2026-10-14

- IAP del servicio piloto usa Identity Platform externo; una solicitud
  anónima recibe 302 al formulario propio. El backend piloto tiene cero
  bindings públicos; el servicio principal no recibió cambios.
- El formulario separado responde `/`, `/config` y `/bundle.js`; no sirve
  rutas de V0. La primera compilación corrigió su política CSP para permitir
  la llamada de configuración de Identity Platform.
- La verificación del flujo real detectó dos destinos que faltaban en la
  autorización del navegador: `iap.googleapis.com` como retorno de IAP en
  Identity Platform y el origen exacto del backend piloto en `connect-src`
  para que `gcip-iap` coloque su cookie. Se agregaron sin retirar los dominios
  existentes ni ampliar la política a otros destinos.
- La prueba de navegador integrada en Codex no llega a
  `www.googleapis.com` (`ERR_BLOCKED_BY_CLIENT`). Esto **no acredita ni
  descarta** el funcionamiento en Chrome normal. La persona titular completó
  fuera de esta conversación la rotación de contraseña y confirmó que el
  acceso válido en Chrome llega a «Resumen nacional»; la contraseña no se
  copia ni comunica aquí. La primera prueba manual de inactividad **falló**:
  después de más de 300 s seguían visibles los resultados. El fragmento
  periódico de Streamlit no se considera suficiente como control de cierre.
  La revisión piloto `enares-stage04-iap-pilot-00009-qur` añade un temporizador
  en el documento que oculta los resultados antes de navegar al cierre de IAP
  y comprueba también el retorno desde una pestaña en segundo plano. Tras
  pasar la CI del head `58e4f44dbc173cb351474ff2ed6ace244eaa5772`, se
  dirigió el 100 % del tráfico **solo del piloto** a esa revisión. Ana repitió
  en Chrome la prueba de más de 300 s sin actividad y confirmó que los
  resultados se ocultaron y apareció el login. La prueba anterior fallida se
  hizo cuando el enlace normal aún servía la revisión previa `00007-fat`.
  La prueba siguiente **falló**: al abrir de nuevo el enlace después de ver
  el login, el navegador entró directamente a los resultados sin pedir clave.
  Identity Platform e IAP pueden conservar su sesión durante hasta una hora
  después de un logout; el cierre visual no basta para reautenticar. Una nueva
  candidata bloquea en el backend las sesiones de navegador nuevas cuyo
  `gcip.auth_time` firmado por IAP tiene 300 s o más, aunque la cookie IAP
  todavía sea válida. La revisión `enares-stage04-iap-pilot-00011-vez` se
  compiló desde el commit exacto `238c1f63a17b01f80bd8278ffe3d938faf8c9ada`,
  pasó CI y se llevó al 100 % **solo del piloto**. Ana confirmó que al abrir
  de nuevo el enlace sin clave vio el formulario y no los resultados; tras
  introducir credenciales válidas volvió a «Resumen nacional». En una
  ventana de incógnito, una contraseña incorrecta y un usuario distinto
  permanecieron fuera de los resultados. Estas pruebas son observaciones
  manuales de Ana, no una auditoría independiente de Rita.
  Como restricción deliberada, una conexión nueva tras 300 s desde el último
  ingreso con contraseña pide reautenticación incluso si la sesión anterior
  tuvo actividad; una sesión que continúa abierta conserva el criterio de
  300 s **de inactividad**. Esto evita que una cookie IAP retenida durante
  hasta una hora abra una conexión nueva sin contraseña.
- Tras el ingreso, Ana recorrió los seis módulos 3.1–3.6 y confirmó que el
  selector de temas responde en cada uno. El catálogo de 80 temas (11, 18,
  20, 9, 12 y 10 por módulo) se fija en `report_topics.py` y sus pruebas de
  cobertura/aislamiento pasaron 41/41. No se presenta la prueba manual como
  una revisión visual individual de los 80 temas.
- El flujo ejecutable de `render()` retorna inmediatamente si `_idle_gate()`
  falla; solo después se llama a `_verified_release_snapshot()` y se accede
  al repositorio de agregados. Las pruebas de falta de JWT y falta de
  configuración IAP verifican que no se renderizan tablas. Esto respalda el
  gate de «V0 no se consulta antes de autenticar»; no se infiere solo de una
  etiqueta en la interfaz.
- El formulario piloto usa la revisión `enares-stage04-auth-pilot-00008-fes`
  (digest `sha256:b6af37ddc276c55510b00b545955fe8097b4ac4eb4eed283344e6fa4e490d38e`).
  Pasó por candidata al 0 %, pruebas locales de la política CSP y CI verde
  del commit `253484704270a0cd24cbebadf819c356b6bc0053` antes de recibir
  el 100 % del tráfico **solo del servicio de acceso piloto**. La revisión
  anterior `00006-niq` conserva una URL etiquetada para rollback. El servicio
  principal `enares-stage04-shadow` no cambió.
- La candidata backend `enares-stage04-iap-pilot-00009-qur` usa la imagen
  `sha256:118a466e77f4b6a16c44800417d9019ab933622258855919cde2f3c3a29b7488`.
  La revisión anterior `00007-fat` conserva la etiqueta `idle-b` para rollback;
  el backend no tiene bindings públicos de invocación. La CI del nuevo head
  terminó en verde, incluida la auditoría WCAG 2.2 AA.
- La revisión actual del backend piloto `00011-vez` usa la imagen
  `sha256:180bce1f6a0df897797a9c477409192171d1d1218abf5d4b5946793f2c731b1d`.
  Su prueba anónima recibió 302, IAM sigue sin miembros públicos de
  invocación y la revisión anterior `00009-qur` conserva la etiqueta
  `idle-v2` como destino de rollback. El servicio principal continúa en
  `enares-stage04-shadow-sex182-ff47d4a` al 100 %.
- Ensayo de rollback **solo del piloto**: se creó el checkpoint `00013-vig`
  con el mismo digest corregido, sin tráfico inicial. Se dirigió el 100 % a
  `00013-vig`, se verificó el estado de tráfico y luego se revirtió el 100 % a
  `00011-vez`. Ambas revisiones quedaron `Ready` y las solicitudes anónimas
  a sus URLs reciben 302; el servicio principal permaneció intacto. Las
  revisiones `00007-fat` y `00009-qur` se conservan como evidencia histórica,
  **no** como destinos recomendados de rollback: preceden al gate de
  reautenticación firmado.
- Capacidad observada: backend piloto 2 CPU, 1 GiB, concurrencia 20,
  `maxScale=2`; servicio de acceso 1 CPU, 256 MiB, concurrencia 20,
  `maxScale=1`. Ambos tienen `minScale` sin fijar (escala a cero por defecto).
  La alerta presupuestaria existente sigue vigente; el objetivo operativo es
  gasto cero y el techo autorizado sigue siendo USD 20/mes total. Estos
  límites **no garantizan costo cero**; el gasto facturado todavía debe
  contrastarse en Billing antes de una promoción.
- Se verificó por lectura de Cloud Billing que el proyecto tiene facturación
  vinculada y existe un presupuesto mensual de PEN 67 (aproximación del techo
  USD 20) con avisos de gasto actual al 5 %, 25 %, 50 % y 100 %, además de
  un canal de notificación configurado. El presupuesto se aplica a la cuenta
  de facturación, sin filtro de proyecto; es una **alerta**, no un límite
  estricto de gasto. Esta comprobación no proporciona el costo real acumulado.
  Ana informó que el informe de Billing filtrado al proyecto muestra `0`
  durante esta verificación; no comunicó una moneda. Es una lectura manual
  puntual y puede tener retraso de contabilización, no una garantía de gasto
  futuro cero.
- **Estado de publicación: NO PROMOVER.** Este PR continúa en borrador hasta
  comprobar todos los criterios siguientes y recibir la revisión de Rita.

El paquete de aceptación exige: acceso correcto e incorrecto, usuario
incorrecto, anónimo sin cifras, backend directo rechazado, IAM privado,
ausencia de lectura V0 preautenticación, bloqueo y nueva contraseña tras
300 s, controles antiabuso, secretos ausentes de artefactos, navegación de
seis módulos/80 temas, CI verde, digest/revisión de la candidata, rollback y
capacidad/costo registrados. El PR permanece en borrador hasta completar el
piloto y enviar **una sola** solicitud de revisión a Rita.

Referencias oficiales: [identidades externas de IAP](https://docs.cloud.google.com/iap/docs/enable-external-identities),
[cabeceras firmadas](https://docs.cloud.google.com/iap/docs/signed-headers-howto),
[sesiones externas](https://docs.cloud.google.com/iap/docs/external-identity-sessions),
[vigencia de sesión IAP](https://docs.cloud.google.com/iap/docs/sessions-howto) y
[`auth_time` de Identity Platform](https://firebase.google.com/docs/reference/admin/node/firebase-admin.auth.decodedidtoken).
