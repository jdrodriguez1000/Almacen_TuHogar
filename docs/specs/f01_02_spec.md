# SPEC — Validación de Infraestructura Supabase (`f01_02`)

> Documento: `docs/specs/f01_02_spec.md`
> Versión: 1.0
> Fecha: 2026-03-28
> Estado: Activo
> Elaborado por: Triple S (Sabbia Solutions & Services)
> Trazabilidad: Este documento implementa los requerimientos de `docs/reqs/f01_02_prd.md`.

---

## 1. Visión de Arquitectura

Esta etapa es de tipo **INFRAESTRUCTURA Y VERIFICACIÓN**. No se implementa lógica de negocio ni pipeline ETL. El objetivo es confirmar que el substrato de base de datos en Supabase está correctamente aprovisionado y que el toolchain Python puede operar contra él.

La arquitectura consta de tres capas de actividad:
1. **Verificación** — scripts que leen `information_schema`, `pg_policies` y `pg_indexes` para confirmar el estado real de Supabase.
2. **Aprovisionamiento** — DDL `CREATE TABLE IF NOT EXISTS` ejecutado en Supabase console para crear las tablas `tss_*` faltantes.
3. **Certificación** — suite pytest que prueba la conectividad real extremo a extremo desde Python.

El MCP de Supabase es una herramienta de introspección futura. En esta etapa, **la configuración del MCP es una tarea a ejecutar** — no un prerrequisito. Toda verificación se realiza mediante `supabase-py` y consultas SQL directas.

### 1.1 Diagrama de Flujo

```
INICIO
  ↓
[ARC-06] Cargar config (.env) — SUPABASE_URL + SUPABASE_SERVICE_KEY
  ↓
[ARC-01] Verificar tablas usr_* (information_schema) ──────────────────┐
  ↓                                                                      │
[ARC-02] Crear/verificar tablas tss_* (DDL en Supabase console)         │
  ↓                                                                      │
[ARC-05] Verificar RLS (pg_policies) + índices (pg_indexes)             │
  ↓                                                                      │
[ARC-04] Sincronizar docs/database/schema.sql                           │
  ↓                                                                      │
[ARC-03] Ejecutar pytest test_infra_connectivity.py ←───────────────────┘
  ↓
FIN — Infraestructura certificada
```

### 1.2 Componentes de Arquitectura

| ID | Componente | Responsabilidad | Archivo |
|---|---|---|---|
| `[ARC-01]` | Verificador de tablas cliente | Consulta `information_schema.columns` para validar existencia y estructura de las 4 tablas `usr_*` | `pipeline/tests/test_infra_connectivity.py` |
| `[ARC-02]` | DDL de tablas Triple S | Define y ejecuta `CREATE TABLE IF NOT EXISTS` para las 10 tablas `tss_*`; fuente de verdad estructural | `docs/database/schema.sql` |
| `[ARC-03]` | Suite de conectividad pytest | Verifica conexión real a Supabase y ejecuta SELECT contra cada tabla desde Python usando `supabase-py` | `pipeline/tests/test_infra_connectivity.py` |
| `[ARC-04]` | schema.sql — fuente de verdad DDL | Documento DDL reproducible que sincroniza el estado real de Supabase; leído por todos los agentes | `docs/database/schema.sql` |
| `[ARC-05]` | Verificador RLS e índices | Consulta `pg_policies` y `pg_indexes` para confirmar que permisos y performance están configurados | `pipeline/tests/test_infra_connectivity.py` |
| `[ARC-06]` | Módulo de configuración | Carga variables de entorno desde `pipeline/.env` usando `python-dotenv`; único punto de acceso a credenciales | `pipeline/config.py` |

---

## 2. Especificaciones de Ingeniería de Datos

### 2.1 Esquemas de Tablas

#### Tablas `usr_*` — Solo lectura (propiedad del cliente)

Estas tablas no son creadas por Triple S. Se documentan como referencia para verificación.

**`usr_ventas`** — Transacciones de venta
| Columna | Tipo PostgreSQL | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID o BIGSERIAL | PRIMARY KEY | Identificador de transacción |
| `fecha_hora` | TIMESTAMPTZ | NOT NULL | Timestamp de la venta en UTC |
| `id_sede` | TEXT o INTEGER | NOT NULL, FK → `usr_sedes.id_sede` | Sede donde ocurrió la venta |
| `sku` | TEXT | NOT NULL, FK → `usr_productos.sku` | SKU del producto vendido |
| `cantidad` | INTEGER o NUMERIC | NOT NULL, > 0 | Unidades vendidas |
| `precio` | NUMERIC | NOT NULL, > 0 | Precio unitario de venta |
| `costo` | NUMERIC | NULLABLE | Costo unitario (puede ser null) |

**`usr_inventario`** — Registros de inventario físico
| Columna | Tipo PostgreSQL | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID o BIGSERIAL | PRIMARY KEY | Identificador de registro |
| `fecha_hora` | TIMESTAMPTZ | NOT NULL | Timestamp del registro en UTC |
| `id_sede` | TEXT o INTEGER | NOT NULL, FK → `usr_sedes.id_sede` | Sede del inventario |
| `sku` | TEXT | NOT NULL, FK → `usr_productos.sku` | SKU del producto |
| `stock_fisico` | INTEGER o NUMERIC | NOT NULL, >= 0 | Unidades en inventario físico |

**`usr_productos`** — Catálogo de SKUs
| Columna | Tipo PostgreSQL | Constraints | Descripción |
|---|---|---|---|
| `sku` | TEXT | PRIMARY KEY | Identificador único del producto |
| `nombre` | TEXT | NOT NULL | Nombre del producto |
| `familia` | TEXT | NOT NULL | Agrupación de nivel 1 |
| `categoria` | TEXT | NOT NULL | Agrupación de nivel 2 |
| `subcategoria` | TEXT | NULLABLE | Agrupación de nivel 3 |

**`usr_sedes`** — Catálogo de sedes
| Columna | Tipo PostgreSQL | Constraints | Descripción |
|---|---|---|---|
| `id_sede` | TEXT o INTEGER | PRIMARY KEY | Identificador único de sede |
| `nombre` | TEXT | NOT NULL | Nombre de la sede |
| `ciudad` | TEXT | NOT NULL | Ciudad donde opera la sede |

---

#### Tabla: `tss_bronze_ventas`
Espejo raw de `usr_ventas` con metadatos de ingesta. Sin transformaciones.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador interno Bronze |
| `src_id` | TEXT | NOT NULL | ID original de `usr_ventas.id` |
| `fecha_hora` | TIMESTAMPTZ | NOT NULL | Timestamp original (UTC) sin modificar |
| `id_sede` | TEXT | NOT NULL | Sede original |
| `sku` | TEXT | NOT NULL | SKU original |
| `cantidad` | NUMERIC | NOT NULL | Cantidad original |
| `precio` | NUMERIC | NOT NULL | Precio original |
| `costo` | NUMERIC | NULLABLE | Costo original |
| `_ingested_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de ingesta por el pipeline |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_bronze_inventario`
Espejo raw de `usr_inventario` con metadatos de ingesta.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador interno Bronze |
| `src_id` | TEXT | NOT NULL | ID original de `usr_inventario.id` |
| `fecha_hora` | TIMESTAMPTZ | NOT NULL | Timestamp original (UTC) |
| `id_sede` | TEXT | NOT NULL | Sede original |
| `sku` | TEXT | NOT NULL | SKU original |
| `stock_fisico` | NUMERIC | NOT NULL | Stock original |
| `_ingested_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de ingesta |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_silver_ventas`
Datos limpios y validados. Timezone convertido a COT. Columnas de calidad añadidas.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador Silver |
| `src_id` | TEXT | NOT NULL | ID original de `usr_ventas.id` |
| `fecha_hora` | TIMESTAMPTZ | NOT NULL | Timestamp original (UTC) |
| `fecha_hora_cot` | TIMESTAMPTZ | NOT NULL | Timestamp convertido a `America/Bogota` |
| `fecha_cot` | DATE | NOT NULL | Fecha en COT (para partición y filtros) |
| `id_sede` | TEXT | NOT NULL | Sede validada (existe en `usr_sedes`) |
| `sku` | TEXT | NOT NULL | SKU validado (existe en `usr_productos`) |
| `cantidad` | NUMERIC | NOT NULL CHECK (cantidad > 0) | Cantidad validada |
| `precio` | NUMERIC | NOT NULL CHECK (precio > 0) | Precio validado |
| `costo` | NUMERIC | NULLABLE | Costo (null permitido) |
| `_validated_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de validación Silver |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_silver_inventario`
Datos de inventario limpios con timezone COT.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador Silver |
| `src_id` | TEXT | NOT NULL | ID original de `usr_inventario.id` |
| `fecha_hora` | TIMESTAMPTZ | NOT NULL | Timestamp original (UTC) |
| `fecha_hora_cot` | TIMESTAMPTZ | NOT NULL | Timestamp convertido a COT |
| `fecha_cot` | DATE | NOT NULL | Fecha en COT |
| `id_sede` | TEXT | NOT NULL | Sede validada |
| `sku` | TEXT | NOT NULL | SKU validado |
| `stock_fisico` | NUMERIC | NOT NULL CHECK (stock_fisico >= 0) | Stock validado |
| `_validated_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de validación |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_gold_daily_sales`
Métricas agregadas de ventas diarias por sede y SKU.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador |
| `fecha_cot` | DATE | NOT NULL | Fecha de las métricas (COT) |
| `id_sede` | TEXT | NOT NULL | Sede |
| `sku` | TEXT | NOT NULL | SKU |
| `total_cantidad` | NUMERIC | NOT NULL | Suma de cantidad vendida en el día |
| `total_venta` | NUMERIC | NOT NULL | Suma de precio * cantidad |
| `total_costo` | NUMERIC | NULLABLE | Suma de costo * cantidad |
| `margen_bruto` | NUMERIC | NULLABLE | total_venta - total_costo |
| `_computed_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de cómputo |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_gold_abc_ranking`
Clasificación ABC/Pareto semanal por SKU y sede.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador |
| `semana_inicio` | DATE | NOT NULL | Primer día (lunes) de la semana analizada |
| `id_sede` | TEXT | NOT NULL | Sede (o 'GLOBAL' para ranking consolidado) |
| `sku` | TEXT | NOT NULL | SKU clasificado |
| `categoria_abc` | TEXT | NOT NULL CHECK (categoria_abc IN ('A','B','C')) | Clasificación |
| `porcentaje_venta_acum` | NUMERIC | NOT NULL | % acumulado de ventas que representa este SKU |
| `rank_venta` | INTEGER | NOT NULL | Posición en ranking de ventas |
| `_computed_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de cómputo |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_gold_alerts`
Alertas determinísticas generadas por el motor de reglas (Etapa 3.5).

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador |
| `alert_date` | DATE | NOT NULL | Fecha de la alerta (COT) |
| `alert_type` | TEXT | NOT NULL | Código de regla (ej. `STOCK_CRITICO`) |
| `alert_polarity` | TEXT | NOT NULL CHECK (alert_polarity IN ('NEGATIVA','POSITIVA')) | Tipo de alerta |
| `id_sede` | TEXT | NULLABLE | Sede afectada (null = global) |
| `sku` | TEXT | NULLABLE | SKU afectado (null = sede/global) |
| `alert_value` | NUMERIC | NULLABLE | Valor numérico que disparó la alerta |
| `threshold_value` | NUMERIC | NULLABLE | Umbral configurado |
| `alert_detail` | TEXT | NULLABLE | Descripción textual |
| `_generated_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de generación |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_pipeline_log`
Registro de ejecuciones del pipeline con estado y métricas.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `run_id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador único de ejecución |
| `run_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de inicio de ejecución |
| `mode` | TEXT | NOT NULL CHECK (mode IN ('validate','etl','alerts','full')) | Modo de ejecución |
| `status` | TEXT | NOT NULL CHECK (status IN ('running','success','failed','partial')) | Estado final |
| `records_processed` | INTEGER | NOT NULL DEFAULT 0 | Registros procesados exitosamente |
| `records_quarantined` | INTEGER | NOT NULL DEFAULT 0 | Registros enviados a cuarentena |
| `errors` | INTEGER | NOT NULL DEFAULT 0 | Errores no recuperables |
| `duration_s` | NUMERIC | NULLABLE | Duración en segundos |
| `error_detail` | TEXT | NULLABLE | Detalle del error si status = 'failed' |

---

#### Tabla: `tss_cuarentena_ventas`
Registros de `usr_ventas` rechazados por violación del Data Contract.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador de cuarentena |
| `src_id` | TEXT | NULLABLE | ID original (puede ser null si el registro es malformado) |
| `fecha_hora` | TIMESTAMPTZ | NULLABLE | Timestamp original |
| `id_sede` | TEXT | NULLABLE | Sede original |
| `sku` | TEXT | NULLABLE | SKU original |
| `cantidad` | NUMERIC | NULLABLE | Cantidad original |
| `precio` | NUMERIC | NULLABLE | Precio original |
| `costo` | NUMERIC | NULLABLE | Costo original |
| `_error_code` | TEXT | NOT NULL | Código de error (`ERR_MTD_XXX`) |
| `_error_detail` | TEXT | NOT NULL | Descripción del rechazo |
| `_quarantined_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de cuarentena |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

#### Tabla: `tss_cuarentena_inventario`
Registros de `usr_inventario` rechazados por violación del Data Contract.

| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY DEFAULT gen_random_uuid() | Identificador de cuarentena |
| `src_id` | TEXT | NULLABLE | ID original |
| `fecha_hora` | TIMESTAMPTZ | NULLABLE | Timestamp original |
| `id_sede` | TEXT | NULLABLE | Sede original |
| `sku` | TEXT | NULLABLE | SKU original |
| `stock_fisico` | NUMERIC | NULLABLE | Stock original |
| `_error_code` | TEXT | NOT NULL | Código de error (`ERR_MTD_XXX`) |
| `_error_detail` | TEXT | NOT NULL | Descripción del rechazo |
| `_quarantined_at` | TIMESTAMPTZ | NOT NULL DEFAULT now() | Timestamp de cuarentena |
| `_pipeline_run_id` | UUID | NOT NULL | FK lógica → `tss_pipeline_log.run_id` |

---

### 2.2 Esquemas de Validación

En esta etapa no se implementan esquemas Pandera (eso corresponde a Etapa 3.1). Lo que se verifica es la conformidad estructural mediante consultas a `information_schema`. La "validación" aquí es confirmar que el esquema real de Supabase coincide con el DDL documentado.

**Método de verificación estructural para `usr_*`:**
```python
# Pseudo-código de verificación (implementado en ARC-03)
EXPECTED_COLUMNS = {
    "usr_ventas": ["id", "fecha_hora", "id_sede", "sku", "cantidad", "precio", "costo"],
    "usr_inventario": ["id", "fecha_hora", "id_sede", "sku", "stock_fisico"],
    "usr_productos": ["sku", "nombre", "familia", "categoria", "subcategoria"],
    "usr_sedes": ["id_sede", "nombre", "ciudad"],
}

# Para cada tabla: SELECT column_name FROM information_schema.columns
# WHERE table_name = '{tabla}' AND table_schema = 'public'
# Comparar con EXPECTED_COLUMNS[tabla] — todos deben estar presentes
```

---

### 2.3 Contratos de Datos entre Capas

| Capa Origen | Capa Destino | Formato | Validación en esta etapa | SLA |
|---|---|---|---|---|
| `usr_ventas` | `tss_bronze_ventas` | Tabla PostgreSQL → DataFrame → INSERT | Solo verificación de existencia y estructura. ETL real en Etapa 3.2. | T+1 COT |
| `usr_inventario` | `tss_bronze_inventario` | Tabla PostgreSQL → DataFrame → INSERT | Solo verificación de existencia y estructura. ETL real en Etapa 3.2. | T+1 COT |
| `tss_bronze_*` | `tss_silver_*` | Tabla → DataFrame → Pandera → INSERT | Solo verificación DDL. Validación Pandera en Etapa 3.1. | T+1 COT |
| `tss_silver_*` | `tss_gold_*` | Tabla → DataFrame → agregaciones → INSERT | Solo verificación DDL. Métricas Gold en Etapa 3.3. | T+1 antes de 8 AM COT |

---

## 3. Diseño de Módulos y Funciones

### 3.1 `pipeline/config.py` — `[ARC-06]`

Módulo de configuración. Carga `.env` y expone un objeto de configuración inmutable.

```python
# Interfaz pública:
def get_supabase_client() -> supabase.Client:
    """Retorna cliente Supabase autenticado con service_role key."""
    # Carga SUPABASE_URL y SUPABASE_SERVICE_KEY desde .env
    # Usa python-dotenv. Lanza EnvironmentError si alguna variable falta.
    # NUNCA acepta valores hardcodeados.
```

**Inputs:** Variables de entorno `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` en `pipeline/.env`
**Output:** `supabase.Client` listo para operar
**Error:** `EnvironmentError` con mensaje descriptivo si falta alguna variable

---

### 3.2 `pipeline/tests/test_infra_connectivity.py` — `[ARC-01]`, `[ARC-03]`, `[ARC-05]`

Suite pytest completa. Estructura de clases y tests:

```python
class TestEnvironmentConfig:
    """Verifica que las variables de entorno necesarias están configuradas."""

    def test_supabase_url_present(self):
        """SUPABASE_URL existe en .env y no está vacía."""

    def test_supabase_service_key_present(self):
        """SUPABASE_SERVICE_KEY existe en .env y no está vacía."""

    def test_supabase_client_instantiates(self):
        """get_supabase_client() retorna cliente sin excepciones."""


class TestSupabaseConnectivity:
    """Verifica que el cliente Python puede conectarse a Supabase."""

    def test_connection_select_one(self):
        """Ejecuta SELECT 1 contra Supabase. Retorna en < 3 segundos."""

    def test_connection_latency(self):
        """Tiempo de round-trip al servidor < 3000ms."""


class TestClientTableStructure:
    """Verifica existencia y estructura de las 4 tablas usr_*."""

    def test_usr_ventas_exists(self):
        """usr_ventas existe en information_schema."""

    def test_usr_ventas_required_columns(self):
        """usr_ventas tiene: id, fecha_hora, id_sede, sku, cantidad, precio, costo."""

    def test_usr_inventario_exists(self):
        """usr_inventario existe en information_schema."""

    def test_usr_inventario_required_columns(self):
        """usr_inventario tiene: id, fecha_hora, id_sede, sku, stock_fisico."""

    def test_usr_productos_exists(self):
        """usr_productos existe en information_schema."""

    def test_usr_productos_required_columns(self):
        """usr_productos tiene: sku, nombre, familia, categoria, subcategoria."""

    def test_usr_productos_has_records(self):
        """usr_productos tiene al menos 1 registro activo (catálogo cargado)."""

    def test_usr_sedes_exists(self):
        """usr_sedes existe en information_schema."""

    def test_usr_sedes_required_columns(self):
        """usr_sedes tiene: id_sede, nombre, ciudad."""

    def test_usr_sedes_has_exactly_seven_records(self):
        """usr_sedes tiene exactamente 7 registros."""


class TestTripleSTableStructure:
    """Verifica existencia de las 10 tablas tss_* en Supabase."""

    TSS_TABLES = [
        "tss_bronze_ventas",
        "tss_bronze_inventario",
        "tss_silver_ventas",
        "tss_silver_inventario",
        "tss_gold_daily_sales",
        "tss_gold_abc_ranking",
        "tss_gold_alerts",
        "tss_pipeline_log",
        "tss_cuarentena_ventas",
        "tss_cuarentena_inventario",
    ]

    def test_all_tss_tables_exist(self):
        """Las 10 tablas tss_* existen en information_schema. Falla con lista de faltantes."""

    def test_tss_pipeline_log_columns(self):
        """tss_pipeline_log tiene: run_id, run_at, mode, status, records_processed,
           records_quarantined, errors, duration_s, error_detail."""

    def test_tss_bronze_ventas_columns(self):
        """tss_bronze_ventas tiene: id, src_id, fecha_hora, id_sede, sku, cantidad,
           precio, costo, _ingested_at, _pipeline_run_id."""

    def test_tss_cuarentena_ventas_columns(self):
        """tss_cuarentena_ventas tiene: id, src_id, _error_code, _error_detail,
           _quarantined_at, _pipeline_run_id."""


class TestRLSPolicies:
    """Verifica que RLS está habilitado en todas las tablas críticas."""

    def test_usr_tables_rls_enabled(self):
        """RLS habilitado en las 4 tablas usr_*. Consulta pg_tables.rowsecurity."""

    def test_tss_tables_rls_enabled(self):
        """RLS habilitado en las 10 tablas tss_*. Consulta pg_tables.rowsecurity."""

    def test_service_role_can_read_usr_ventas(self):
        """service_role puede ejecutar SELECT en usr_ventas sin error."""

    def test_service_role_can_write_tss_pipeline_log(self):
        """service_role puede ejecutar INSERT en tss_pipeline_log sin error.
           Limpia el registro de prueba al finalizar."""


class TestPerformanceIndexes:
    """Verifica existencia de índices de performance."""

    REQUIRED_INDEXES = [
        ("usr_ventas", "fecha_hora"),
        ("usr_ventas", "sku"),
        ("usr_ventas", "id_sede"),
        ("usr_inventario", "sku"),
        ("usr_inventario", "id_sede"),
    ]

    def test_required_indexes_exist(self):
        """Verifica cada índice en pg_indexes. Reporta faltantes como warning,
           no como fallo de test (índices son Media prioridad per PRD REQ-11)."""
```

**Convenciones de implementación:**
- Cada clase usa un fixture `client` con scope `session` — una sola conexión por ejecución.
- Los tests de estructura usan queries a `information_schema` via `supabase-py`.
- Tests de RLS usan queries a `pg_tables` via SQL directo.
- `TestPerformanceIndexes` usa `logging.warning` — no `pytest.fail` — si faltan índices.
- Tiempo máximo de suite completa: 30 segundos ([MET-03]).

---

### 3.3 Función helper de verificación de columnas

```python
# En test_infra_connectivity.py — función helper compartida

def get_table_columns(client: supabase.Client, table_name: str) -> list[str]:
    """
    Retorna lista de nombres de columnas de una tabla via information_schema.

    Input:  client (supabase.Client), table_name (str)
    Output: list[str] — nombres de columnas en minúsculas
    Error:  AssertionError si la tabla no existe
    """
```

---

## 4. Configuración Requerida

### 4.1 Variables de entorno — `pipeline/.env`

```dotenv
# Supabase — credenciales de acceso
SUPABASE_URL=https://<project-id>.supabase.co
SUPABASE_SERVICE_KEY=<service_role_key>

# Ambiente de ejecución
ENVIRONMENT=development   # development | production
```

**Notas:**
- `SUPABASE_SERVICE_KEY` es la `service_role` key de Supabase — tiene acceso completo bypassando RLS. Nunca exponer en código fuente, logs, ni commits.
- `.env` está en `.gitignore`. El archivo `.env.example` (sin valores reales) sí se versiona.

### 4.2 Dependencias Python — `pipeline/requirements.txt`

Las siguientes dependencias deben estar declaradas antes de implementar:

```
supabase>=2.0.0
python-dotenv>=1.0.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

### 4.3 MCP Supabase — pendiente de configurar

La integración del MCP de Supabase con Claude Code es una **tarea de esta etapa**. No es prerrequisito para los scripts Python — es una mejora de toolchain para que los agentes puedan introspeccionar la base de datos directamente. Se configura mediante `settings.json` del workspace de Claude Code una vez que se obtengan las credenciales (Personal Access Token de Supabase).

---

## 5. Estructura de `docs/database/schema.sql`

El archivo DDL tiene la siguiente estructura:

```sql
-- =============================================================================
-- docs/database/schema.sql
-- Fuente de verdad del esquema de Supabase para el proyecto Almacén TuHogar.
-- Mantenido por: Triple S (Sabbia Solutions & Services)
-- Última sincronización: YYYY-MM-DD
--
-- REGLAS:
-- 1. Este archivo siempre refleja el estado ACTUAL de Supabase.
-- 2. Toda modificación requiere CC aprobado antes de ejecutar.
-- 3. Tablas usr_* son de solo lectura para Triple S — no se modifican.
-- 4. Para aplicar: ejecutar en Supabase SQL Editor. Sin migraciones automáticas.
-- =============================================================================

-- ============================================================
-- SECCIÓN 1: TABLAS DEL CLIENTE (usr_*) — SOLO REFERENCIA
-- Triple S no crea ni altera estas tablas.
-- ============================================================

-- usr_ventas (solo lectura, propiedad del cliente)
-- Columnas observadas: id, fecha_hora, id_sede, sku, cantidad, precio, costo
-- Tipos confirmados: [completar tras verificación]

-- usr_inventario (solo lectura, propiedad del cliente)
-- Columnas observadas: id, fecha_hora, id_sede, sku, stock_fisico

-- usr_productos (solo lectura, propiedad del cliente)
-- Columnas observadas: sku, nombre, familia, categoria, subcategoria

-- usr_sedes (solo lectura, propiedad del cliente)
-- Columnas observadas: id_sede, nombre, ciudad

-- ============================================================
-- SECCIÓN 2: TABLAS TRIPLE S — BRONZE
-- ============================================================

CREATE TABLE IF NOT EXISTS tss_bronze_ventas (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    src_id           TEXT        NOT NULL,
    fecha_hora       TIMESTAMPTZ NOT NULL,
    id_sede          TEXT        NOT NULL,
    sku              TEXT        NOT NULL,
    cantidad         NUMERIC     NOT NULL,
    precio           NUMERIC     NOT NULL,
    costo            NUMERIC,
    _ingested_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

CREATE TABLE IF NOT EXISTS tss_bronze_inventario (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    src_id           TEXT        NOT NULL,
    fecha_hora       TIMESTAMPTZ NOT NULL,
    id_sede          TEXT        NOT NULL,
    sku              TEXT        NOT NULL,
    stock_fisico     NUMERIC     NOT NULL,
    _ingested_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

-- ============================================================
-- SECCIÓN 3: TABLAS TRIPLE S — SILVER
-- ============================================================

CREATE TABLE IF NOT EXISTS tss_silver_ventas (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    src_id           TEXT        NOT NULL,
    fecha_hora       TIMESTAMPTZ NOT NULL,
    fecha_hora_cot   TIMESTAMPTZ NOT NULL,
    fecha_cot        DATE        NOT NULL,
    id_sede          TEXT        NOT NULL,
    sku              TEXT        NOT NULL,
    cantidad         NUMERIC     NOT NULL CHECK (cantidad > 0),
    precio           NUMERIC     NOT NULL CHECK (precio > 0),
    costo            NUMERIC,
    _validated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

CREATE TABLE IF NOT EXISTS tss_silver_inventario (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    src_id           TEXT        NOT NULL,
    fecha_hora       TIMESTAMPTZ NOT NULL,
    fecha_hora_cot   TIMESTAMPTZ NOT NULL,
    fecha_cot        DATE        NOT NULL,
    id_sede          TEXT        NOT NULL,
    sku              TEXT        NOT NULL,
    stock_fisico     NUMERIC     NOT NULL CHECK (stock_fisico >= 0),
    _validated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

-- ============================================================
-- SECCIÓN 4: TABLAS TRIPLE S — GOLD
-- ============================================================

CREATE TABLE IF NOT EXISTS tss_gold_daily_sales (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha_cot        DATE        NOT NULL,
    id_sede          TEXT        NOT NULL,
    sku              TEXT        NOT NULL,
    total_cantidad   NUMERIC     NOT NULL,
    total_venta      NUMERIC     NOT NULL,
    total_costo      NUMERIC,
    margen_bruto     NUMERIC,
    _computed_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

CREATE TABLE IF NOT EXISTS tss_gold_abc_ranking (
    id                     UUID    PRIMARY KEY DEFAULT gen_random_uuid(),
    semana_inicio          DATE    NOT NULL,
    id_sede                TEXT    NOT NULL,
    sku                    TEXT    NOT NULL,
    categoria_abc          TEXT    NOT NULL CHECK (categoria_abc IN ('A','B','C')),
    porcentaje_venta_acum  NUMERIC NOT NULL,
    rank_venta             INTEGER NOT NULL,
    _computed_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id       UUID    NOT NULL
);

CREATE TABLE IF NOT EXISTS tss_gold_alerts (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    alert_date       DATE        NOT NULL,
    alert_type       TEXT        NOT NULL,
    alert_polarity   TEXT        NOT NULL CHECK (alert_polarity IN ('NEGATIVA','POSITIVA')),
    id_sede          TEXT,
    sku              TEXT,
    alert_value      NUMERIC,
    threshold_value  NUMERIC,
    alert_detail     TEXT,
    _generated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

-- ============================================================
-- SECCIÓN 5: TABLAS TRIPLE S — SOPORTE (LOG + CUARENTENA)
-- ============================================================

CREATE TABLE IF NOT EXISTS tss_pipeline_log (
    run_id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    run_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    mode                 TEXT        NOT NULL CHECK (mode IN ('validate','etl','alerts','full')),
    status               TEXT        NOT NULL CHECK (status IN ('running','success','failed','partial')),
    records_processed    INTEGER     NOT NULL DEFAULT 0,
    records_quarantined  INTEGER     NOT NULL DEFAULT 0,
    errors               INTEGER     NOT NULL DEFAULT 0,
    duration_s           NUMERIC,
    error_detail         TEXT
);

CREATE TABLE IF NOT EXISTS tss_cuarentena_ventas (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    src_id           TEXT,
    fecha_hora       TIMESTAMPTZ,
    id_sede          TEXT,
    sku              TEXT,
    cantidad         NUMERIC,
    precio           NUMERIC,
    costo            NUMERIC,
    _error_code      TEXT        NOT NULL,
    _error_detail    TEXT        NOT NULL,
    _quarantined_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

CREATE TABLE IF NOT EXISTS tss_cuarentena_inventario (
    id               UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    src_id           TEXT,
    fecha_hora       TIMESTAMPTZ,
    id_sede          TEXT,
    sku              TEXT,
    stock_fisico     NUMERIC,
    _error_code      TEXT        NOT NULL,
    _error_detail    TEXT        NOT NULL,
    _quarantined_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id UUID        NOT NULL
);

-- ============================================================
-- SECCIÓN 6: ÍNDICES DE PERFORMANCE
-- Verificar si existen antes de ejecutar. Coordinar con cliente para usr_*.
-- ============================================================

-- INDEX PENDIENTE: verificar existencia en Supabase antes de crear
-- CREATE INDEX IF NOT EXISTS idx_usr_ventas_fecha_hora ON usr_ventas (fecha_hora);
-- CREATE INDEX IF NOT EXISTS idx_usr_ventas_sku ON usr_ventas (sku);
-- CREATE INDEX IF NOT EXISTS idx_usr_ventas_id_sede ON usr_ventas (id_sede);
-- CREATE INDEX IF NOT EXISTS idx_usr_inventario_sku ON usr_inventario (sku);
-- CREATE INDEX IF NOT EXISTS idx_usr_inventario_id_sede ON usr_inventario (id_sede);

-- ============================================================
-- SECCIÓN 7: RLS — POLÍTICAS
-- Ejecutar en Supabase console. Ajustar según roles existentes.
-- ============================================================

-- Habilitar RLS en tablas tss_* (ejecutar para cada tabla)
-- ALTER TABLE tss_bronze_ventas ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_bronze_inventario ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_silver_ventas ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_silver_inventario ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_gold_daily_sales ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_gold_abc_ranking ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_gold_alerts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_pipeline_log ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_cuarentena_ventas ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE tss_cuarentena_inventario ENABLE ROW LEVEL SECURITY;

-- Policy: service_role tiene acceso total a tss_*
-- CREATE POLICY "tss_service_role_all" ON tss_bronze_ventas
--   FOR ALL TO service_role USING (true) WITH CHECK (true);

-- Policy: service_role puede leer usr_* (solo SELECT)
-- Nota: las políticas sobre usr_* deben ser coordinadas con el cliente.
```

---

## 6. Matriz de Trazabilidad: SPEC vs PRD

| REQ (PRD) | Componente `[ARC]` | Función / Artefacto | Archivo(s) |
|---|---|---|---|
| `[REQ-01]` | `[ARC-01]`, `[ARC-03]` | `TestClientTableStructure.test_usr_ventas_*` | `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-02]` | `[ARC-01]`, `[ARC-03]` | `TestClientTableStructure.test_usr_inventario_*` | `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-03]` | `[ARC-01]`, `[ARC-03]` | `TestClientTableStructure.test_usr_productos_*` | `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-04]` | `[ARC-01]`, `[ARC-03]` | `TestClientTableStructure.test_usr_sedes_*` | `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-05]` | `[ARC-02]`, `[ARC-03]` | DDL Bronze + `TestTripleSTableStructure` | `docs/database/schema.sql`, `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-06]` | `[ARC-02]`, `[ARC-03]` | DDL Silver + `TestTripleSTableStructure` | `docs/database/schema.sql`, `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-07]` | `[ARC-02]`, `[ARC-03]` | DDL Gold + `TestTripleSTableStructure` | `docs/database/schema.sql`, `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-08]` | `[ARC-02]`, `[ARC-03]` | DDL Log + Cuarentena + `TestTripleSTableStructure` | `docs/database/schema.sql`, `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-09]` | `[ARC-05]`, `[ARC-03]` | `TestRLSPolicies.test_tss_tables_rls_enabled` | `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-10]` | `[ARC-05]`, `[ARC-03]` | `TestRLSPolicies.test_usr_tables_rls_enabled` | `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-11]` | `[ARC-05]`, `[ARC-03]` | `TestPerformanceIndexes.test_required_indexes_exist` | `pipeline/tests/test_infra_connectivity.py` |
| `[REQ-12]` | `[ARC-03]`, `[ARC-06]` | Suite pytest completa + `get_supabase_client()` | `pipeline/tests/test_infra_connectivity.py`, `pipeline/config.py` |
| `[REQ-13]` | `[ARC-04]` | `docs/database/schema.sql` completo | `docs/database/schema.sql` |

---

## 7. Decisiones de Diseño y Justificación

**`[ARC-06]` — Módulo `config.py` como único punto de acceso a credenciales:**
El CLAUDE.md establece "Cero hardcoding" y "Secretos en `.env`". Centralizar la carga de credenciales en un único módulo garantiza que si el mecanismo de carga cambia (ej. de `.env` a AWS Secrets Manager en producción), solo un archivo cambia. Toda la suite de tests importa `config.get_supabase_client()` — nunca accede a variables de entorno directamente.

**`[ARC-03]` — pytest en lugar de scripts de verificación ad-hoc:**
Los scripts de verificación one-off son difíciles de mantener y no producen evidencia reproducible. Una suite pytest genera reportes estandarizados, es re-ejecutable en CI/CD, y falla de forma descriptiva. Coherente con la política TDD universal del CLAUDE.md.

**DDL con `CREATE TABLE IF NOT EXISTS`:**
Permite ejecutar el DDL de forma idempotente — tanto en setup inicial como en verificaciones posteriores. Si la tabla ya existe con el esquema correcto, no hay efecto. Si falta, se crea.

**`src_id TEXT` en Bronze y cuarentena en lugar de UUID:**
Las tablas del cliente usan tipos de PK heterogéneos (UUID, BIGSERIAL, TEXT). Almacenar `src_id` como TEXT permite compatibilidad universal sin casteos riesgosos, preservando el valor original exacto.

**`[ARC-05]` — Índices documentados como comentados en `schema.sql`:**
Los índices en `usr_*` requieren coordinación con el cliente (son sus tablas). Documentarlos como `-- INDEX PENDIENTE` crea un artefacto de verificación sin ejecutar DDL no autorizado. El test de performance reporta como warning, no como fallo, porque `[REQ-11]` tiene prioridad Media.

**MCP Supabase como tarea, no prerrequisito:**
El MCP de Supabase es una mejora de DX que permite al agente introspeccionar la base de datos directamente. Todo el trabajo técnico de producción usa `supabase-py`. El MCP se configura como tarea de toolchain en esta misma etapa, una vez disponibles las credenciales Personal Access Token.
