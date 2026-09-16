# Paso 48 — seis sesiones Playwright concurrentes

**Estado:** `LOCAL_SCRIPT_READY; CLOUD_MEASUREMENT_BLOCKED`

## Mitad local adelantada

`scripts/check_six_sessions.mjs` abre exactamente seis contextos de navegador independientes y los
ejecuta de forma concurrente contra la aplicación. Cada sesión aplica una ruta y un filtro distinto:

| Sesión | Página | Dimensión / acción | Evidencia esperada |
|---|---|---|---|
| S01 | Resumen | Nacional | resumen nacional visible |
| S02 | Módulo 3.1 | Nacional | tabla de tareas del hogar visible |
| S03 | Módulo 3.2 | Nacional; cambia a Demo sintético | estados didácticos visibles |
| S04 | Módulo 3.5 | Nacional | matrices de solapamiento visibles |
| S05 | Módulo 3.2 | Departamento | respuesta fail-closed `sin datos autorizados` |
| S06 | Metodología | Nacional | límites metodológicos visibles |

El script falla ante HTTP no exitoso, excepción de página, falta de la evidencia esperada o una
latencia superior a 30 segundos. Registra latencia por sesión, p95, duración de pared y variación
de memoria RSS del proceso conductor. La CI inicia la aplicación local y ejecuta el mismo guion.

## Ejecución local

Con la aplicación disponible en `http://127.0.0.1:8501`:

```powershell
npm ci
npx playwright install chromium
npm run test:six-sessions
```

Se puede definir otra URL local con `APP_URL`. No se usan credenciales, identidades reales,
microdatos ni recursos cloud.

## Resultado local reproducido

Ejecución del 2026-09-15 sobre seis contextos concurrentes:

- resultado: `PASS`;
- respuestas: 6/6 con HTTP 200 y evidencia visible esperada;
- duración de pared: 3.410 ms;
- latencia p95 de ruta: 3.326 ms;
- latencias individuales: S01 3.242 ms; S02 2.521 ms; S03 3.326 ms; S04 3.212 ms;
  S05 3.087 ms; S06 3.071 ms;
- variación RSS del conductor Node: 33.443.840 bytes;
- errores de página: 0.

Estos valores son diagnósticos de la máquina local y no constituyen un objetivo de rendimiento
institucional. La CI vuelve a ejecutar el guion y decide por integridad funcional y por el límite
explícito de 30 segundos por sesión.

## Mitad bloqueada

La variación RSS del conductor no sustituye métricas de Cloud Run. Consumo del servicio, número de
instancias y concurrencia efectiva del despliegue quedan expresamente como `PENDING_CLOUD_RUN` y
solo se medirán después de completar la secuencia de desbloqueo cloud y desplegar el fixture
sintético. Este control no autoriza facturación, IAM, despliegue ni conexión de cifras reales.
