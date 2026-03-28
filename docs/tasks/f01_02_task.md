# Lista de Tareas — Validación de Infraestructura Supabase (`f01_02`)

> Trazabilidad: Estas tareas implementan `docs/plans/f01_02_plan.md`.
> Actualiza marcando `[x]` al completar. **NUNCA borres tareas completadas.**
> Documento: `docs/tasks/f01_02_task.md`
> Versión: 1.0
> Fecha: 2026-03-28
> Elaborado por: Triple S (Sabbia Solutions & Services)

## Convenciones de Anotación

- **`(independiente)`** — Sin dependencias, puede iniciar de inmediato (tras obtener credenciales).
- **`(depends_on: TSK-2-XX)`** — Espera a que `TSK-2-XX` esté completa.
- **`(parallel_with: TSK-2-XX)`** — Puede ejecutarse simultáneamente con `TSK-2-XX`.

---

## Prerrequisito Desbloqueante

> `[RSK-01]` — Antes de iniciar cualquier tarea, las credenciales `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` deben estar disponibles. Si no están, documentar bloqueo en `PROJECT_handoff.md` y escalar al responsable. Ninguna tarea puede comenzar sin este prerequisito.

---

## Mapa de Dependencias

```
PREREQUISITO EXTERNO:
  Credenciales Supabase disponibles → desbloqueante para todo B1

BLOQUE 1 — Setup entorno (secuencial, tras prerequisito desbloqueado):
  TSK-2-01 → Crear .venv e instalar dependencias
  TSK-2-02 → Crear pipeline/.env y pipeline/.env.example  ← paralela con TSK-2-01
  TSK-2-03 → Implementar pipeline/config.py  ← depends_on: TSK-2-01 + TSK-2-02

BLOQUE 2 — Verificar usr_* (paralelo con B3, depends_on: TSK-2-03):
  TSK-2-04 → Verificar estructura usr_ventas y usr_inventario
  TSK-2-05 → Verificar estructura usr_productos y usr_sedes  ← paralela con TSK-2-04

BLOQUE 3 — Aprovisionar tss_* (paralelo con B2, depends_on: TSK-2-03):
  TSK-2-06 → Redactar DDL en schema.sql (tss_pipeline_log + cuarentena)  ← paralela con TSK-2-04
  TSK-2-07 → Redactar DDL en schema.sql (Bronze + Silver)  ← paralela con TSK-2-06
  TSK-2-08 → Redactar DDL (Gold) + ejecutar DDL completo en Supabase  ← depends_on: TSK-2-06 + TSK-2-07
  TSK-2-09 → Habilitar RLS y policies service_role en las 10 tablas tss_*  ← depends_on: TSK-2-08

BLOQUE 4 — Suite pytest (depends_on: TSK-2-05 + TSK-2-09):
  TSK-2-10 → Implementar TestEnvironmentConfig + TestSupabaseConnectivity
  TSK-2-11 → Implementar TestClientTableStructure  ← paralela con TSK-2-10
  TSK-2-12 → Implementar TestTripleSTableStructure + TestRLSPolicies  ← depends_on: TSK-2-10 + TSK-2-11
  TSK-2-13 → Implementar TestPerformanceIndexes + ejecutar suite completa  ← depends_on: TSK-2-12

BLOQUE 5 — Sincronizar schema.sql + configurar MCP (depends_on: TSK-2-13):
  TSK-2-14 → Finalizar y sincronizar docs/database/schema.sql
  TSK-2-15 → Configurar MCP de Supabase en .claude/settings.json  ← paralela con TSK-2-14

CIERRE (depends_on: TSK-2-14 + TSK-2-15):
  TSK-2-16 → Actualizar PROJECT_handoff.md
  TSK-2-17 → Crear commit atómico en feat/etapa-1-2  ← depends_on: TSK-2-16
```

---

## Bloque 1 — Setup de Entorno Local

- [ ] `[TSK-2-01]` Crear el ambiente virtual Python en `pipeline/.venv` e instalar las 4 dependencias desde `pipeline/requirements.txt` _(independiente — tras credenciales disponibles)_
  - **REQ que implementa**: `[DAT-05]`, `[REQ-12]` (infraestructura base)
  - **Componente [ARC]**: `[ARC-06]`
  - **Archivos**: `pipeline/requirements.txt`, `pipeline/.venv/`
  - **Pasos**:
    1. Crear `pipeline/requirements.txt` con: `supabase>=2.0.0`, `python-dotenv>=1.0.0`, `pytest>=7.4.0`, `pytest-cov>=4.1.0`
    2. `cd pipeline && python -m venv .venv`
    3. Activar: `source .venv/Scripts/activate` (Windows) o `.venv/bin/activate` (Linux/Mac)
    4. `pip install -r requirements.txt`
  - **DoD**: `pip list` dentro del `.venv` muestra `supabase`, `python-dotenv`, `pytest`, `pytest-cov` con versiones conformes. `.venv/` listado en `.gitignore`.

- [ ] `[TSK-2-02]` Crear `pipeline/.env` con credenciales reales y `pipeline/.env.example` con placeholders versionado en Git _(parallel_with: TSK-2-01)_
  - **REQ que implementa**: `[DAT-05]`
  - **Componente [ARC]**: `[ARC-06]`
  - **Archivos**: `pipeline/.env`, `pipeline/.env.example`, `.gitignore`
  - **Pasos**:
    1. Confirmar que `.gitignore` incluye la entrada `pipeline/.env`
    2. Crear `pipeline/.env` con `SUPABASE_URL=<url_real>` y `SUPABASE_SERVICE_KEY=<key_real>`
    3. Crear `pipeline/.env.example` con `SUPABASE_URL=https://XXXX.supabase.co` y `SUPABASE_SERVICE_KEY=your-service-role-key-here`
    4. Hacer commit únicamente de `.env.example`
  - **DoD**: `pipeline/.env` existe localmente y NO aparece en `git status`. `pipeline/.env.example` aparece versionado con placeholders.

- [ ] `[TSK-2-03]` Implementar `pipeline/config.py` con la función `get_supabase_client()` _(depends_on: TSK-2-01, TSK-2-02)_
  - **REQ que implementa**: `[REQ-12]`, `[DAT-05]`
  - **Componente [ARC]**: `[ARC-06]`
  - **Archivos**: `pipeline/config.py`
  - **Interfaz obligatoria**:
    ```python
    def get_supabase_client() -> supabase.Client:
        """Retorna cliente Supabase autenticado con service_role key.
        Carga SUPABASE_URL y SUPABASE_SERVICE_KEY desde .env con python-dotenv.
        Lanza EnvironmentError si alguna variable falta.
        NUNCA acepta valores hardcodeados.
        """
    ```
  - **DoD**: `python -c "from config import get_supabase_client; c = get_supabase_client(); print('OK')"` ejecutado desde `pipeline/` retorna `OK` sin errores.

---

## Bloque 2 — Verificar Tablas `usr_*` en Supabase

- [ ] `[TSK-2-04]` Verificar existencia y estructura de `usr_ventas` y `usr_inventario` mediante consultas a `information_schema` _(depends_on: TSK-2-03)_
  - **REQ que implementa**: `[REQ-01]`, `[REQ-02]`
  - **Componente [ARC]**: `[ARC-01]`
  - **Riesgo activo**: `[RSK-02]`, `[RSK-03]`
  - **Archivos**: notas en `docs/database/schema.sql` (comentarios `-- DISCREPANCIA:` si aplica)
  - **Pasos**:
    1. Ejecutar en Supabase SQL Editor: `SELECT column_name, data_type FROM information_schema.columns WHERE table_name IN ('usr_ventas', 'usr_inventario') AND table_schema = 'public' ORDER BY table_name, ordinal_position;`
    2. Confirmar columnas requeridas: `usr_ventas` → `id`, `fecha_hora`, `id_sede`, `sku`, `cantidad`, `precio`, `costo`; `usr_inventario` → `id`, `fecha_hora`, `id_sede`, `sku`, `stock_fisico`
    3. Si hay discrepancias: `-- DISCREPANCIA: usr_ventas.campo — tipo encontrado: X, tipo esperado: Y`
    4. Si tabla no existe: DETENER y aplicar protocolo `[RSK-02]` (abrir CC antes de continuar)
  - **DoD**: Confirmación documentada de ambas tablas con columnas requeridas. Discrepancias registradas en `schema.sql`. `[MET-01]` parcialmente verificada.

- [ ] `[TSK-2-05]` Verificar existencia y estructura de `usr_productos` y `usr_sedes`, incluyendo conteos y estado RLS _(parallel_with: TSK-2-04)_
  - **REQ que implementa**: `[REQ-03]`, `[REQ-04]`
  - **Componente [ARC]**: `[ARC-01]`
  - **Riesgo activo**: `[RSK-02]`, `[RSK-03]`, `[RSK-04]`
  - **Archivos**: notas en `docs/database/schema.sql`
  - **Pasos**:
    1. Columnas: `SELECT column_name, data_type FROM information_schema.columns WHERE table_name IN ('usr_productos', 'usr_sedes') AND table_schema = 'public';`
    2. Conteos: `SELECT COUNT(*) FROM usr_sedes;` (debe = 7) y `SELECT COUNT(*) FROM usr_productos;` (debe >= 1)
    3. RLS: `SELECT tablename, rowsecurity FROM pg_tables WHERE tablename IN ('usr_ventas','usr_inventario','usr_productos','usr_sedes');`
    4. Si RLS deshabilitado: documentar como BLOQUEANTE (`[RSK-04]`), reportar al cliente, NO modificar tablas
  - **DoD**: `usr_sedes` = 7 registros (`[MET-06]`). `usr_productos` >= 1 registro (`[MET-07]`). Estado RLS documentado. `[MET-01]` completamente verificada.

---

## Bloque 3 — Aprovisionar Tablas `tss_*` en Supabase

- [ ] `[TSK-2-06]` Redactar DDL en `docs/database/schema.sql` para `tss_pipeline_log`, `tss_cuarentena_ventas` y `tss_cuarentena_inventario` _(parallel_with: TSK-2-04)_
  - **REQ que implementa**: `[REQ-08]`
  - **Componente [ARC]**: `[ARC-02]`, `[ARC-04]`
  - **Archivos**: `docs/database/schema.sql`
  - **Pasos**:
    1. Redactar `tss_pipeline_log` con: `run_id UUID PK DEFAULT gen_random_uuid()`, `run_at TIMESTAMPTZ DEFAULT now()`, `mode TEXT CHECK (mode IN ('validate','etl','alerts','full'))`, `status TEXT CHECK (status IN ('running','success','failed','partial'))`, `records_processed INTEGER DEFAULT 0`, `records_quarantined INTEGER DEFAULT 0`, `errors INTEGER DEFAULT 0`, `duration_s NUMERIC`, `error_detail TEXT`
    2. Redactar `tss_cuarentena_ventas` con campos nullable + `_error_code TEXT NOT NULL`, `_error_detail TEXT NOT NULL`, `_quarantined_at TIMESTAMPTZ DEFAULT now()`, `_pipeline_run_id UUID NOT NULL`
    3. Redactar `tss_cuarentena_inventario` análogo
    4. Añadir cabecera: `-- Última sincronización: 2026-03-28`
  - **DoD**: 3 bloques DDL en `schema.sql` con sintaxis SQL válida.

- [ ] `[TSK-2-07]` Redactar DDL en `docs/database/schema.sql` para las tablas Bronze y Silver _(parallel_with: TSK-2-06)_
  - **REQ que implementa**: `[REQ-05]`, `[REQ-06]`
  - **Componente [ARC]**: `[ARC-02]`, `[ARC-04]`
  - **Archivos**: `docs/database/schema.sql`
  - **Pasos**:
    1. `tss_bronze_ventas`: `id UUID PK`, `src_id TEXT NOT NULL`, `fecha_hora TIMESTAMPTZ NOT NULL`, `id_sede TEXT NOT NULL`, `sku TEXT NOT NULL`, `cantidad NUMERIC NOT NULL`, `precio NUMERIC NOT NULL`, `costo NUMERIC`, `_ingested_at TIMESTAMPTZ DEFAULT now()`, `_pipeline_run_id UUID NOT NULL`
    2. `tss_bronze_inventario` análogo (sin `precio`/`costo`, con `stock_fisico NUMERIC NOT NULL`)
    3. `tss_silver_ventas` igual que Bronze + `fecha_hora_cot TIMESTAMPTZ NOT NULL`, `fecha_cot DATE NOT NULL`, `CHECK (cantidad > 0)`, `CHECK (precio > 0)`, `_validated_at TIMESTAMPTZ DEFAULT now()`
    4. `tss_silver_inventario` con `CHECK (stock_fisico >= 0)`
  - **DoD**: 4 bloques DDL (2 Bronze + 2 Silver) con CHECKs conformes a la SPEC sección 2.1.

- [ ] `[TSK-2-08]` Redactar DDL para tablas Gold y ejecutar el DDL completo de `schema.sql` en Supabase SQL Editor _(depends_on: TSK-2-06, TSK-2-07)_
  - **REQ que implementa**: `[REQ-05]`–`[REQ-08]`
  - **Componente [ARC]**: `[ARC-02]`, `[ARC-04]`
  - **Archivos**: `docs/database/schema.sql`
  - **Pasos**:
    1. `tss_gold_daily_sales`: `fecha_cot DATE NOT NULL`, `id_sede TEXT NOT NULL`, `sku TEXT NOT NULL`, `total_cantidad NUMERIC NOT NULL`, `total_venta NUMERIC NOT NULL`, `total_costo NUMERIC`, `margen_bruto NUMERIC`, `_computed_at TIMESTAMPTZ DEFAULT now()`, `_pipeline_run_id UUID NOT NULL`
    2. `tss_gold_abc_ranking` con `CHECK (categoria_abc IN ('A','B','C'))`
    3. `tss_gold_alerts` con `CHECK (alert_polarity IN ('NEGATIVA','POSITIVA'))`
    4. Ejecutar DDL completo en Supabase SQL Editor en orden: `tss_pipeline_log` → Bronze → Silver → Gold → cuarentena
    5. Verificar: `SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name LIKE 'tss_%';` → debe retornar 10
  - **DoD**: Consulta de verificación retorna exactamente 10. `[MET-02]` verificada.

- [ ] `[TSK-2-09]` Habilitar RLS y crear policies `service_role` en las 10 tablas `tss_*`, verificar índices de performance _(depends_on: TSK-2-08)_
  - **REQ que implementa**: `[REQ-09]`, `[REQ-10]`, `[REQ-11]`
  - **Componente [ARC]**: `[ARC-05]`
  - **Riesgo activo**: `[RSK-05]`
  - **Archivos**: `docs/database/schema.sql` (sección RLS e índices)
  - **Pasos**:
    1. Para cada tabla `tss_*`: `ALTER TABLE tss_[nombre] ENABLE ROW LEVEL SECURITY;`
    2. Para cada tabla `tss_*`: `CREATE POLICY "service_role_full_access" ON tss_[nombre] FOR ALL TO service_role USING (true) WITH CHECK (true);`
    3. Verificar: `SELECT tablename, rowsecurity FROM pg_tables WHERE tablename LIKE 'tss_%';` → todas `rowsecurity = true`
    4. Verificar índices en `pg_indexes` para: `usr_ventas(fecha_hora)`, `usr_ventas(sku)`, `usr_ventas(id_sede)`, `usr_inventario(sku)`, `usr_inventario(id_sede)`
    5. Documentar faltantes con `-- INDEX PENDIENTE: [tabla(columna)]`
  - **DoD**: `pg_policies` retorna >= 10 policies para tablas `tss_*`. `pg_tables` muestra `rowsecurity = true` en las 10 tablas. Índices faltantes documentados. `[MET-04]` verificada.

---

## Bloque 4 — Suite pytest de Conectividad

- [ ] `[TSK-2-10]` Implementar (TDD) `TestEnvironmentConfig` y `TestSupabaseConnectivity` _(depends_on: TSK-2-03, TSK-2-05, TSK-2-09)_
  - **REQ que implementa**: `[REQ-12]`
  - **Componente [ARC]**: `[ARC-03]`, `[ARC-06]`
  - **Archivos**: `pipeline/tests/__init__.py`, `pipeline/tests/test_infra_connectivity.py`
  - **Tests (5 en total)**:
    - `TestEnvironmentConfig`: variables de entorno cargadas, cliente instancia sin error, `EnvironmentError` si falta variable
    - `TestSupabaseConnectivity`: `SELECT 1` retorna resultado, round-trip < 3000 ms
  - **Orden TDD**: escribir test → ejecutar (FALLA) → implementar mínimo → ejecutar (PASA)
  - **DoD**: `pytest tests/test_infra_connectivity.py::TestEnvironmentConfig tests/test_infra_connectivity.py::TestSupabaseConnectivity -v` → 5/5 pasan, exit code 0.

- [ ] `[TSK-2-11]` Implementar (TDD) `TestClientTableStructure` con 10 tests para las 4 tablas `usr_*` _(parallel_with: TSK-2-10)_
  - **REQ que implementa**: `[REQ-01]`–`[REQ-04]`
  - **Componente [ARC]**: `[ARC-01]`, `[ARC-03]`
  - **Archivos**: `pipeline/tests/test_infra_connectivity.py`
  - **Helper obligatorio**: `get_table_columns(client, table_name) -> list[str]` usando `information_schema.columns`
  - **Tests (10)**:
    - Existencia + columnas requeridas para las 4 tablas `usr_*`
    - `fecha_hora` es TIMESTAMPTZ en `usr_ventas` y `usr_inventario`
    - `usr_productos` COUNT >= 1, `usr_sedes` COUNT = 7
    - SELECT retorna resultado en `usr_ventas` y `usr_inventario`
  - **DoD**: `pytest tests/test_infra_connectivity.py::TestClientTableStructure -v` → 10/10 pasan, exit code 0.

- [ ] `[TSK-2-12]` Implementar (TDD) `TestTripleSTableStructure` (4 tests) y `TestRLSPolicies` (4 tests) _(depends_on: TSK-2-10, TSK-2-11)_
  - **REQ que implementa**: `[REQ-09]`, `[REQ-10]`, `[REQ-12]`
  - **Componente [ARC]**: `[ARC-03]`, `[ARC-05]`
  - **Archivos**: `pipeline/tests/test_infra_connectivity.py`
  - **Tests `TestTripleSTableStructure`** (4): existencia de Bronze, Silver, Gold y tablas de soporte
  - **Tests `TestRLSPolicies`** (4): RLS en `tss_*`, policy `service_role` en `tss_*`, INSERT real en `tss_pipeline_log` con teardown, RLS en `usr_*`
  - **DoD**: `pytest ::TestTripleSTableStructure ::TestRLSPolicies -v` → 8/8 pasan. No quedan registros de prueba en `tss_pipeline_log`.

- [ ] `[TSK-2-13]` Implementar `TestPerformanceIndexes` y ejecutar la suite completa con cobertura _(depends_on: TSK-2-12)_
  - **REQ que implementa**: `[REQ-11]`, `[REQ-12]`
  - **Componente [ARC]**: `[ARC-03]`, `[ARC-05]`
  - **Archivos**: `pipeline/tests/test_infra_connectivity.py`
  - **Test (1)**: verificar 5 índices en `pg_indexes`; emitir `logging.warning` si falta alguno — NUNCA `pytest.fail`
  - **Comando de cierre**:
    ```bash
    cd pipeline && source .venv/Scripts/activate
    pytest tests/test_infra_connectivity.py -v --cov=. --cov-report=term-missing
    ```
  - **DoD**: exit code 0, 0 FAILs, tiempo < 30 s, cobertura >= 90%. `[MET-03]` verificada.

---

## Bloque 5 — Sincronizar `schema.sql` y Configurar MCP

- [ ] `[TSK-2-14]` Finalizar y sincronizar `docs/database/schema.sql` con el estado real confirmado de Supabase _(depends_on: TSK-2-13)_
  - **REQ que implementa**: `[REQ-13]`
  - **Componente [ARC]**: `[ARC-04]`
  - **Archivos**: `docs/database/schema.sql`
  - **Pasos**:
    1. Sección 1: comentarios `-- usr_* (solo lectura)` con columnas y tipos reales confirmados en TSK-2-04 y TSK-2-05
    2. Secciones 2–5: DDL `CREATE TABLE IF NOT EXISTS` para las 10 tablas (ya redactado en TSK-2-06/07/08)
    3. Incorporar `-- DISCREPANCIA: [detalle]` donde aplique
    4. Incorporar `-- INDEX PENDIENTE: [tabla(columna)]` donde aplique
    5. Actualizar fecha: `-- Última sincronización: 2026-03-28`
  - **DoD**: DDL reproducible sin errores de sintaxis. Sección 1 refleja estructura real. `[MET-05]` verificada.

- [ ] `[TSK-2-15]` Configurar el MCP de Supabase en `.claude/settings.local.json` con el Personal Access Token _(parallel_with: TSK-2-14)_
  - **REQ que implementa**: extensión de `[REQ-12]` para agentes
  - **Componente [ARC]**: `[ARC-04]`
  - **Archivos**: `.claude/settings.local.json`
  - **Pasos**:
    1. Obtener Personal Access Token de Supabase (distinto al `SUPABASE_SERVICE_KEY`)
    2. Agregar configuración MCP de Supabase en `.claude/settings.local.json` con token y Project ID
    3. Verificar que `.claude/settings.local.json` está en `.gitignore`
    4. Reiniciar Claude Code y confirmar servidor MCP activo
    5. Verificar: introspección via MCP devuelve las 14 tablas esperadas (`usr_*` + `tss_*`)
  - **DoD**: Servidor MCP de Supabase aparece activo en Claude Code. Personal Access Token NO está en ningún archivo versionado.

---

## Cierre de Etapa

- [ ] `[TSK-2-16]` Actualizar `PROJECT_handoff.md` con el estado final de la Etapa 1.2 _(depends_on: TSK-2-14, TSK-2-15)_
  - **Archivos**: `PROJECT_handoff.md`
  - **Contenido mínimo**:
    - Archivos creados/modificados en la etapa
    - Estado real medido de cada métrica `[MET-01]` a `[MET-07]`
    - Discrepancias encontradas y su resolución o CC abierto
    - Próxima acción: inicio de Etapa 1.3 — Data Contract
    - Bloqueos pendientes (índices, RLS de `usr_*`, etc.)
  - **DoD**: Un agente que lea `PROJECT_handoff.md` puede iniciar Etapa 1.3 sin contexto adicional.

- [ ] `[TSK-2-17]` Crear commit atómico en rama `feat/etapa-1-2` con todos los archivos de la etapa _(depends_on: TSK-2-16)_
  - **Archivos**: todos los creados/modificados en la etapa
  - **Pasos**:
    1. Verificar rama activa: `feat/etapa-1-2` (crear si no existe)
    2. Stagear: `git add pipeline/config.py pipeline/requirements.txt pipeline/.env.example pipeline/tests/ docs/database/schema.sql PROJECT_handoff.md`
    3. Verificar que `pipeline/.env` y `.claude/settings.local.json` NO están en el staging area
    4. `git commit -m "feat: etapa 1.2 completada — infraestructura Supabase certificada"`
  - **DoD**: Commit creado. `pipeline/.env` y `.claude/settings.local.json` ausentes del commit.

---

## Matriz de Trazabilidad: Tareas vs PRD vs SPEC vs Plan

| Tarea | Bloque Plan | `[ARC]` | `[REQ]` | `[MET]` |
|---|---|---|---|---|
| `[TSK-2-01]` | B1 | `[ARC-06]` | `[DAT-05]`, `[REQ-12]` parcial | — |
| `[TSK-2-02]` | B1 | `[ARC-06]` | `[DAT-05]` | — |
| `[TSK-2-03]` | B1 | `[ARC-06]` | `[REQ-12]` parcial | — |
| `[TSK-2-04]` | B2 | `[ARC-01]` | `[REQ-01]`, `[REQ-02]` | `[MET-01]` parcial |
| `[TSK-2-05]` | B2 | `[ARC-01]` | `[REQ-03]`, `[REQ-04]` | `[MET-01]`, `[MET-06]`, `[MET-07]` |
| `[TSK-2-06]` | B3 | `[ARC-02]`, `[ARC-04]` | `[REQ-08]` | — |
| `[TSK-2-07]` | B3 | `[ARC-02]`, `[ARC-04]` | `[REQ-05]`, `[REQ-06]` | — |
| `[TSK-2-08]` | B3 | `[ARC-02]`, `[ARC-04]` | `[REQ-05]`–`[REQ-08]` | `[MET-02]` |
| `[TSK-2-09]` | B3 | `[ARC-05]` | `[REQ-09]`, `[REQ-10]`, `[REQ-11]` | `[MET-04]` |
| `[TSK-2-10]` | B4 | `[ARC-03]`, `[ARC-06]` | `[REQ-12]` | — |
| `[TSK-2-11]` | B4 | `[ARC-01]`, `[ARC-03]` | `[REQ-01]`–`[REQ-04]` | `[MET-01]`, `[MET-06]`, `[MET-07]` |
| `[TSK-2-12]` | B4 | `[ARC-03]`, `[ARC-05]` | `[REQ-09]`, `[REQ-10]`, `[REQ-12]` | `[MET-04]` |
| `[TSK-2-13]` | B4 | `[ARC-03]`, `[ARC-05]` | `[REQ-11]`, `[REQ-12]` | `[MET-03]` |
| `[TSK-2-14]` | B5 | `[ARC-04]` | `[REQ-13]` | `[MET-05]` |
| `[TSK-2-15]` | B5 | `[ARC-04]` | `[REQ-12]` extensión | — |
| `[TSK-2-16]` | Cierre | — | Protocolo `CLAUDE.md` | `[MET-01]`–`[MET-07]` (reporte) |
| `[TSK-2-17]` | Cierre | — | Git Flow `CLAUDE.md` | — |
