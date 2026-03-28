# Plan de Implementación — Validación de Infraestructura Supabase (`f01_02`)

> Documento: `docs/plans/f01_02_plan.md`
> Versión: 1.0
> Fecha: 2026-03-28
> Estado: Activo
> Elaborado por: Triple S (Sabbia Solutions & Services)
> Trazabilidad: Este plan ejecuta `docs/reqs/f01_02_prd.md` según el diseño de `docs/specs/f01_02_spec.md`.

---

## 1. Resumen del Plan

La Etapa 1.2 no produce lógica de negocio: produce **certeza de infraestructura**. El objetivo es demostrar, con evidencia verificable, que Supabase está correctamente aprovisionado y que el toolchain Python puede operar contra él antes de que cualquier etapa de ingeniería de datos comience.

**Estrategia general:** Secuencia en tres fases con una dependencia crítica al inicio — las credenciales de Supabase (`[RSK-01]`). Una vez desbloqueada esa dependencia, el trabajo se estructura en: (1) preparar el entorno local, (2) aprovisionar y verificar el esquema en Supabase, (3) implementar y ejecutar la suite pytest, (4) sincronizar la documentación y configurar el MCP.

**Hitos clave:**
- Credenciales en `pipeline/.env` — prerequisito desbloqueante.
- 10 tablas `tss_*` creadas y verificadas en Supabase.
- `pytest pipeline/tests/test_infra_connectivity.py` pasa al 100% en < 30 segundos.
- `docs/database/schema.sql` sincronizado y reproducible.
- MCP de Supabase configurado en `settings.json`.

---

## 2. Ruta Crítica

### 2.1 Diagrama de Dependencias

```
INICIO
  ↓
[PREREQUISITO: Obtener credenciales Supabase — RSK-01]
  ↓
[B1: Setup de entorno local] (1 día) — Independiente tras prerequisito
  ↓
[B2: Verificar tablas usr_*] (1 día) ──────── paralelo ────── [B3: Aprovisionar tss_*] (2 días)
     Depende de B1                                                  Depende de B1
  ↓                                                                         ↓
  └──────────────────────── ambos deben completarse ───────────────────────┘
                                     ↓
              [B4: Suite pytest de conectividad] (2 días) — Depende de B2 + B3
                                     ↓
              [B5: Sincronizar schema.sql + configurar MCP] (1 día) — Depende de B4
                                     ↓
                              FIN — Infraestructura certificada
```

### 2.2 Análisis de Ruta Crítica

| Bloque | Duración Est. | Dependencias | En Ruta Crítica |
|---|---|---|---|
| Prerequisito: credenciales | Variable | Externa (usuario) | SI — desbloqueante |
| B1 — Setup entorno local | 1 día | Credenciales disponibles | SI |
| B2 — Verificar tablas `usr_*` | 1 día | B1 | NO (paralelo con B3) |
| B3 — Aprovisionar tablas `tss_*` | 2 días | B1 | SI |
| B4 — Suite pytest conectividad | 2 días | B2 + B3 | SI |
| B5 — schema.sql + MCP | 1 día | B4 | SI |

**Ruta crítica:** Prerequisito → B1 → B3 → B4 → B5 = **6 días mínimos**

---

## 3. Backlog de Trabajo (WBS)

### B1 — Setup de Entorno Local

- **Objetivo:** Preparar el ambiente Python con dependencias correctas y credenciales accesibles.
- **Componentes `[ARC]`:** `[ARC-06]`
- **Requerimientos:** `[DAT-05]`, `[REQ-12]` (infraestructura previa al test)
- **Entregables:**
  - `pipeline/.venv/` creado y activo (nunca en Python global)
  - `pipeline/requirements.txt` con 4 dependencias: `supabase>=2.0.0`, `python-dotenv>=1.0.0`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`
  - `pipeline/.env` con `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` reales (en `.gitignore`)
  - `pipeline/.env.example` con placeholders (versionado en Git)
  - `pipeline/config.py` con `get_supabase_client()` implementado
- **Duración estimada:** 1 día
- **Dependencias:** Credenciales de Supabase disponibles (`[RSK-01]`)
- **Orden de ejecución:** Crear `.venv` → instalar desde `requirements.txt` → escribir `.env` → implementar `config.py` → verificar conexión.
- **Hito de aceptación:**
  - [ ] `python -c "from config import get_supabase_client; c = get_supabase_client(); print('OK')"` retorna `OK` sin errores
  - [ ] `pip list` muestra `supabase`, `python-dotenv`, `pytest`, `pytest-cov`
  - [ ] `.env` en `.gitignore`; `.env.example` versionado con placeholders

---

### B2 — Verificar Tablas `usr_*` en Supabase

- **Objetivo:** Confirmar que las 4 tablas del cliente existen con la estructura mínima esperada.
- **Componentes `[ARC]`:** `[ARC-01]`
- **Requerimientos:** `[REQ-01]`, `[REQ-02]`, `[REQ-03]`, `[REQ-04]`
- **Entregables:**
  - Confirmación de existencia y estructura de `usr_ventas`, `usr_inventario`, `usr_productos`, `usr_sedes`
  - Verificación de conteos: exactamente 7 en `usr_sedes`, al menos 1 en `usr_productos`
  - Notas de discrepancias (si las hay) para incorporar en `schema.sql`
- **Duración estimada:** 1 día
- **Dependencias:** B1 completado
- **Puede ejecutarse en paralelo con:** B3
- **Orden de ejecución:** Verificar existencia → columnas → conteos. NUNCA modificar `usr_*`. Si tabla falta, DETENER y aplicar `[RSK-02]`.
- **Riesgos activos:** `[RSK-02]`, `[RSK-03]`, `[RSK-04]`
- **Hito de aceptación:**
  - [ ] `information_schema.columns` confirma columnas requeridas en las 4 tablas `usr_*` (`[MET-01]`)
  - [ ] `SELECT COUNT(*) FROM usr_sedes` = 7 (`[MET-06]`)
  - [ ] `SELECT COUNT(*) FROM usr_productos` >= 1 (`[MET-07]`)
  - [ ] Discrepancias documentadas con formato `-- DISCREPANCIA: [tabla] [detalle]`

---

### B3 — Aprovisionar Tablas `tss_*` en Supabase

- **Objetivo:** Crear las 10 tablas de infraestructura de Triple S mediante DDL documentado.
- **Componentes `[ARC]`:** `[ARC-02]`
- **Requerimientos:** `[REQ-05]`, `[REQ-06]`, `[REQ-07]`, `[REQ-08]`, `[REQ-09]`, `[REQ-11]`
- **Entregables:**
  - 10 tablas `tss_*` en Supabase ejecutando el DDL de `docs/database/schema.sql` en Supabase SQL Editor:
    - Bronze: `tss_bronze_ventas`, `tss_bronze_inventario`
    - Silver: `tss_silver_ventas`, `tss_silver_inventario`
    - Gold: `tss_gold_daily_sales`, `tss_gold_abc_ranking`, `tss_gold_alerts`
    - Soporte: `tss_pipeline_log`, `tss_cuarentena_ventas`, `tss_cuarentena_inventario`
  - RLS habilitado con policy `service_role` (SELECT/INSERT/UPDATE/DELETE) en las 10 tablas
  - Índices verificados; faltantes documentados como `-- INDEX PENDIENTE`
- **Duración estimada:** 2 días
- **Dependencias:** B1 completado
- **Puede ejecutarse en paralelo con:** B2
- **Orden de ejecución:** DDL soporte primero (`tss_pipeline_log`) → Bronze → Silver → Gold. Aplicar RLS inmediatamente después de crear cada grupo.
- **Riesgo activo:** `[RSK-05]`
- **Hito de aceptación:**
  - [ ] `SELECT COUNT(*) FROM information_schema.tables WHERE table_name LIKE 'tss_%'` = 10 (`[MET-02]`)
  - [ ] `pg_tables` muestra `rowsecurity = true` en las 10 tablas `tss_*` (`[MET-04]`)
  - [ ] Al menos una policy `service_role` por tabla en `pg_policies`
  - [ ] Índices faltantes documentados con `-- INDEX PENDIENTE`

---

### B4 — Implementar Suite pytest de Conectividad

- **Objetivo:** Certificar con evidencia automatizable que la infraestructura es accesible desde Python.
- **Componentes `[ARC]`:** `[ARC-03]`, `[ARC-05]`
- **Requerimientos:** `[REQ-10]`, `[REQ-12]`
- **Entregables:**
  - `pipeline/tests/__init__.py` (si no existe)
  - `pipeline/tests/test_infra_connectivity.py` con 6 clases y ~24 tests:
    - `TestEnvironmentConfig` (3 tests): variables de entorno y cliente
    - `TestSupabaseConnectivity` (2 tests): conexión real y latencia
    - `TestClientTableStructure` (10 tests): existencia, columnas, conteos `usr_*`
    - `TestTripleSTableStructure` (4 tests): existencia y columnas `tss_*`
    - `TestRLSPolicies` (4 tests): RLS y permisos `service_role`
    - `TestPerformanceIndexes` (1 test, warning): índices de performance
  - Fixture `client` con scope `session`
  - Helper `get_table_columns()` implementado
- **Duración estimada:** 2 días
- **Dependencias:** B2 completado + B3 completado
- **Orden de implementación (TDD):** Test falla → implementación mínima → refactor. Secuencia: `TestEnvironmentConfig` → `TestSupabaseConnectivity` → `TestClientTableStructure` → `TestTripleSTableStructure` → `TestRLSPolicies` → `TestPerformanceIndexes`.
- **Hito de aceptación:**
  - [ ] `pytest pipeline/tests/test_infra_connectivity.py -v` → exit code 0, 0 FAILs (`[MET-03]`)
  - [ ] Tiempo total < 30 segundos
  - [ ] Cobertura >= 90% (`pytest --cov`)
  - [ ] `TestPerformanceIndexes` emite `logging.warning`, nunca `pytest.fail`

---

### B5 — Sincronizar `schema.sql` y Configurar MCP

- **Objetivo:** Cerrar la etapa con el DDL reproducible como fuente de verdad y el MCP operativo.
- **Componentes `[ARC]`:** `[ARC-04]`
- **Requerimientos:** `[REQ-13]`
- **Entregables:**
  - `docs/database/schema.sql` completo con:
    - Sección 1: comentarios `usr_*` con columnas y tipos reales confirmados en B2
    - Secciones 2–5: DDL `CREATE TABLE IF NOT EXISTS` para las 10 tablas `tss_*`
    - Comentarios `-- DISCREPANCIA: [detalle]` donde aplique
    - Comentarios `-- INDEX PENDIENTE: [tabla(columna)]` donde aplique
    - Fecha actualizada: `-- Última sincronización: 2026-03-28`
  - MCP de Supabase configurado en `.claude/settings.json` con Personal Access Token
- **Duración estimada:** 1 día
- **Dependencias:** B4 completado
- **Orden de ejecución:** Sincronizar `schema.sql` primero → luego configurar MCP con el Personal Access Token.
- **Hito de aceptación:**
  - [ ] `docs/database/schema.sql` existe con DDL reproducible para las 10 tablas `tss_*` (`[MET-05]`)
  - [ ] DDL sin errores de sintaxis SQL
  - [ ] Sección 1 refleja la estructura real confirmada de `usr_*`
  - [ ] MCP de Supabase aparece en lista de servidores activos en Claude Code y puede listar tablas
  - [ ] Commit atómico: `feat: etapa 1.2 completada — infraestructura Supabase certificada`

---

## 4. Estrategia de Pruebas

| Tipo | Clase pytest | Criterio de Éxito | Bloque |
|---|---|---|---|
| Unitaria — config | `TestEnvironmentConfig` | 3/3 pasan; `EnvironmentError` si falta variable | B1, B4 |
| Integración — conectividad | `TestSupabaseConnectivity` | Round-trip < 3000 ms; exit 0 | B4 |
| Integración — estructura cliente | `TestClientTableStructure` | 10/10 pasan; 7 sedes, ≥1 producto | B2, B4 |
| Integración — estructura Triple S | `TestTripleSTableStructure` | 4/4 pasan; lista faltantes si hay | B3, B4 |
| Integración — seguridad | `TestRLSPolicies` | 4/4 pasan; INSERT de prueba limpiado | B3, B4 |
| Warning — performance | `TestPerformanceIndexes` | `logging.warning` (no fallo) si índice falta | B3, B4 |

**Comando completo:**
```bash
cd pipeline && source .venv/Scripts/activate
pytest tests/test_infra_connectivity.py -v --cov=. --cov-report=term-missing
```

---

## 5. Consideraciones de Riesgo y Orden Seguro

| Riesgo | Protocolo de respuesta |
|---|---|
| `[RSK-01]` Credenciales no disponibles | No iniciar ningún bloque. Documentar bloqueo en `PROJECT_handoff.md`. Escalar al responsable. |
| `[RSK-02]` Nombres de tablas `usr_*` diferentes | DETENER B2. Documentar nombres reales. Abrir CC antes de continuar. |
| `[RSK-03]` Columnas faltantes o tipos incompatibles | Documentar discrepancias. Incorporar en `schema.sql`. Abrir CC con el cliente. |
| `[RSK-04]` RLS deshabilitado en `usr_*` | No modificar `usr_*`. Reportar al cliente como riesgo de seguridad. Documentar como BLOQUEANTE. |
| `[RSK-05]` Permisos insuficientes en `service_role` | Verificar con SELECT simple al inicio de B3. Coordinar con admin de Supabase si hay restricciones. |

---

## 6. Matriz de Trazabilidad: Plan vs SPEC vs PRD

| Bloque | `[ARC]` | `[REQ]` | `[OBJ]` | `[MET]` |
|---|---|---|---|---|
| B1 — Setup entorno | `[ARC-06]` | `[DAT-05]`, `[REQ-12]` parcial | `[OBJ-03]` | — |
| B2 — Verificar `usr_*` | `[ARC-01]` | `[REQ-01]`–`[REQ-04]` | `[OBJ-01]` | `[MET-01]`, `[MET-06]`, `[MET-07]` |
| B3 — Aprovisionar `tss_*` | `[ARC-02]` | `[REQ-05]`–`[REQ-09]`, `[REQ-11]` | `[OBJ-02]`, `[OBJ-05]` | `[MET-02]`, `[MET-04]` |
| B4 — Suite pytest | `[ARC-03]`, `[ARC-05]` | `[REQ-10]`, `[REQ-12]` | `[OBJ-03]`, `[OBJ-05]` | `[MET-03]`, `[MET-04]` |
| B5 — schema.sql + MCP | `[ARC-04]` | `[REQ-13]` | `[OBJ-04]` | `[MET-05]` |

---

## 7. Definition of Done (DoD)

La Etapa 1.2 se considera completada cuando **todos** los siguientes ítems están verificados:

**Entorno y configuración:**
- [ ] `pipeline/config.py` implementado con `get_supabase_client()` — sin valores hardcodeados
- [ ] `pipeline/requirements.txt` incluye las 4 dependencias con versiones mínimas
- [ ] `pipeline/.env` existe localmente en `.gitignore`
- [ ] `pipeline/.env.example` versionado con placeholders

**Verificación de infraestructura:**
- [ ] 4 tablas `usr_*` verificadas con estructura conforme (`[MET-01]`)
- [ ] `usr_sedes` = 7 registros (`[MET-06]`)
- [ ] `usr_productos` >= 1 registro (`[MET-07]`)
- [ ] 10 tablas `tss_*` existen en Supabase (`[MET-02]`)
- [ ] RLS habilitado con policies correctas en todas las tablas (`[MET-04]`)

**Tests y calidad:**
- [ ] `pytest pipeline/tests/test_infra_connectivity.py -v` → exit 0, 0 FAILs (`[MET-03]`)
- [ ] Tiempo total de suite < 30 segundos
- [ ] Cobertura >= 90%

**Documentación:**
- [ ] `docs/database/schema.sql` con DDL reproducible para las 10 tablas `tss_*` (`[MET-05]`)
- [ ] MCP de Supabase configurado y operativo en Claude Code

**Cierre:**
- [ ] Commit atómico en `feat/etapa-1-2`: `feat: etapa 1.2 completada — infraestructura Supabase certificada`
- [ ] `PROJECT_handoff.md` actualizado con estado final de la etapa
