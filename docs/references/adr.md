# Decisiones Arquitectónicas (ADR)

### ADR-001 — SQL-First para transformaciones pesadas
**Decisión**: Transformaciones implementadas en SQL (Supabase stored procedures), no en Python.
**Razón**: PostgreSQL es 10-100x más rápido que pandas para el mismo dataset. Reduce latencia y costo.
**Consecuencia**: Python orquesta y valida; SQL transforma y agrega.

### ADR-002 — Medallion Architecture (Bronze/Silver/Gold)
**Decisión**: Tres capas de datos con propósitos distintos.
**Razón**: Trazabilidad completa. Si Gold tiene error, se reprocesa desde Silver sin tocar datos crudos del cliente.
**Consecuencia**: Mayor uso de storage, pero auditoría perfecta de cada transformación.

### ADR-003 — Sin RBAC (todos los gerentes ven lo mismo)
**Decisión**: Dashboard sin restricciones de acceso por rol.
**Razón**: Decisión explícita del cliente (ver PROJECT_scope.md §5). Simplifica arquitectura.
**Consecuencia**: Si se requiere RBAC en el futuro, es un CC que afecta múltiples capas.

### ADR-004 — Alertas determinísticas (sin ML)
**Decisión**: 12 alertas basadas en umbrales fijos, no modelos predictivos.
**Razón**: Fuera de alcance (ver PROJECT_scope.md §7). Reduce complejidad y tiempo de go-live.
**Consecuencia**: Umbrales deben calibrarse manualmente en Fase 3.5 con datos reales.

### ADR-005 — T-1 obligatorio (sin datos del día en curso)
**Decisión**: Dashboard nunca muestra datos de la jornada en curso.
**Razón**: Jornada incompleta genera métricas engañosas.
**Consecuencia**: Gerentes siempre trabajan con información de ayer, no de hoy.
