# Glosario de Términos

| Término | Definición |
|---|---|
| **T-1** | Día anterior completo y cerrado. El dashboard solo muestra datos de T-1 hacia atrás, nunca del día en curso (T+0). |
| **T+0** | Día en curso. Prohibido en el sistema. Datos parciales no representativos. |
| **COT** | Colombia Time (UTC-5). Toda lógica temporal usa `America/Bogota` vía `pytz`. |
| **Data Contract** | Acuerdo formal entre cliente y Triple S sobre formato, campos y frecuencia de datos. Definido en `docs/specs/f01_03_spec.md`. |
| **Bronze** | Capa raw del Medallion. Copia exacta de `usr_*` sin modificar. Tablas `tss_bronze_*`. |
| **Silver** | Capa limpia. Datos deduplicados, normalizados, con timezone COT. Tablas `tss_silver_*`. |
| **Gold** | Capa analítica. Métricas derivadas, clasificación ABC, alertas. Tablas `tss_gold_*`. |
| **ABC/Pareto** | Clasificación de productos por contribución al ingreso. A=top 80%, B=siguiente 15%, C=último 5%. Recalculada cada lunes sobre 90 días. |
| **Cuarentena** | Registro de datos rechazados por violar el Data Contract. Tablas `tss_cuarentena_*`. |
| **ERR_MTD_XXX** | Códigos de error del pipeline. Ver sección "Validación y Errores" en CLAUDE.md. |
| **SDD** | Software Design Document. Jerarquía: PRD → SPEC → Plan → Tasks. |
| **CC** | Control de Cambios (`CC_XXXXX.md`). Requerido antes de modificar cualquier etapa activa o cerrada. |
| **Triple S** | Sabbia Solutions & Services. Proveedor del proyecto. Propietario de tablas `tss_*`. |
| **Triple Persistencia** | Patrón obligatorio: registrar éxito/fallo en (1) archivo local `latest`, (2) log con timestamp, (3) `tss_pipeline_log`. |
