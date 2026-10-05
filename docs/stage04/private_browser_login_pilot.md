# Acceso privado del piloto Stage 04

El servicio Cloud Run permanece protegido por IAP y limitado a las identidades
autorizadas. En `STAGE04_DATA_MODE=AUTHENTICATED_SHADOW`, la aplicación exige
además un formulario de usuario y contraseña **antes** de abrir el repositorio
de agregados V0. Esta segunda barrera no sustituye IAP ni autoriza acceso
público. El modo local de desarrollo conserva el flujo anterior.

El despliegue configura `STAGE04_LOGIN_USERNAME` y
`STAGE04_LOGIN_PASSWORD_HASH` fuera del repositorio. El hash tiene formato
`pbkdf2_sha256$600000$<sal hexadecimal de al menos 16 bytes>$<digest hexadecimal
de 32 bytes>`. La contraseña en claro nunca se incluye en Git, Docker, logs,
URLs ni comentarios de GitHub. Para generar un hash nuevo, usar un entorno
privado y una lectura interactiva sin eco; no pasar la contraseña como argumento
de línea de comandos. Si falta la configuración o el hash es inválido, el
servicio no muestra cifras.

Cada nueva sesión de Streamlit presenta el formulario aun cuando Google
recuerde la sesión IAP. Tras 300 segundos sin interacción con la aplicación,
se borran el estado local, los filtros y los resultados; para continuar se
vuelve a introducir el usuario y la contraseña. IAP también tiene una política
independiente de reautenticación `LOGIN` con `maxAge=300s` en el piloto. Esa
política es de duración máxima, no un contador de inactividad.

Antes de promover al servicio principal: revisión independiente del PR y su
CI, prueba manual del formulario con credenciales válidas e inválidas, prueba
de expiración a 300 segundos, acceso denegado para una cuenta Google no
autorizada, verificación de que el anónimo no ve cifras, comprobación de la
revisión candidata y rollback disponible. No reutilizar una contraseña
compartida débil como único control de acceso.
