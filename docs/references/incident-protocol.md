# Protocolo de Fallo en Producción

## Niveles de Severidad

| Nivel | Descripción | Tiempo de respuesta |
|---|---|---|
| **P1 — Crítico** | Pipeline falló, dashboard sin datos frescos antes de 8 AM | Inmediato |
| **P2 — Alto** | Pipeline corrió pero datos en cuarentena > 5% del volumen | < 2 horas |
| **P3 — Medio** | Pipeline corrió, alertas no se calcularon | < 4 horas |
| **P4 — Bajo** | Anomalía en logs, sin impacto visible | Próximo día hábil |

## Pasos ante Fallo P1

1. **Detectar** — Revisar `tss_pipeline_log` (`status = 'ERROR'`) y archivo local `latest`.
2. **Diagnosticar** — Leer log con timestamp para identificar módulo y error exacto.
3. **Notificar** — Informar al cliente: dashboard mostrará datos de T-2 hasta resolución.
4. **Corregir** — Si es dato del cliente: notificar con código `ERR_MTD_XXX`. Si es bug interno: hotfix en rama `fix/*`.
5. **Reejecutar** — `python pipeline/main.py --mode etl` manualmente una vez corregido.
6. **Cerrar** — Actualizar `tss_pipeline_log` y registrar en `docs/lessons/lessons-learned.md`.

**Regla**: Nunca silenciar errores con `pass`. Nunca reejecutar sin diagnóstico previo.
