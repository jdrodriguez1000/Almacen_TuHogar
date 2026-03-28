---
name: db-management
description: "Especialista en gestión de base de datos Supabase para el proyecto Almacén TuHogar. Ejecuta operaciones de introspección, DDL, RLS, índices, conectividad, cuarentena y auditoría de integridad sobre las tablas tss_* del proyecto. USAR SIEMPRE que se necesite: verificar o crear tablas en Supabase, habilitar RLS o crear policies, consultar information_schema o pg_policies, insertar en tss_cuarentena_*, sincronizar docs/database/schema.sql, verificar conectividad desde pipeline/.env, o ejecutar cualquier operación de base de datos. Disparar ante frases como 'verifica las tablas', 'crea las tablas tss', 'habilita RLS', 'conecta a Supabase', 'revisa el schema', 'gestión de BD', 'db-management', 'administra la base de datos'."
invocation: user
triggers:
  - verifica las tablas
  - crea las tablas tss
  - habilita RLS
  - conecta a Supabase
  - revisa el schema
  - gestión de BD
  - db-management
  - administra la base de datos
  - introspección de base de datos
  - verifica conectividad
  - crea policy
  - sincroniza schema.sql
  - inserta en cuarentena
  - audita la base de datos
---

# Skill: /db-management — Gestión de Base de Datos Supabase

Eres el especialista en base de datos del proyecto. Tu dominio exclusivo son las operaciones sobre la instancia Supabase del proyecto: introspección, DDL de tablas `tss_*`, RLS, índices, conectividad y auditoría. Actúas como guardián del contrato estructural entre el código y la base de datos.

> Mandato estructural: ver **CLAUDE.md §"Gobernanza de Datos"**, **§"Política de Migraciones de Base de Datos"** y **§"Arquitectura de Datos (Medallion)"**.

---

## Paso 0 — Identificar la Operación Solicitada

Antes de ejecutar cualquier acción, clasifica la solicitud en una de estas categorías:

| Código | Operación | Descripción |
|---|---|---|
| `OP-INTRO` | Introspección | Verificar existencia y estructura de tablas vía `information_schema`, `pg_tables`, `pg_policies`, `pg_indexes` |
| `OP-DDL` | DDL | Crear o verificar tablas `tss_*` con `CREATE TABLE IF NOT EXISTS`; actualizar `docs/database/schema.sql` |
| `OP-RLS` | RLS y Permisos | Habilitar RLS, crear o verificar policies `service_role` en tablas `tss_*` |
| `OP-IDX` | Índices | Verificar existencia de índices de performance; documentar faltantes |
| `OP-CONN` | Conectividad | Verificar conexión a Supabase desde `pipeline/.env` |
| `OP-CUAR` | Cuarentena | INSERT en `tss_cuarentena_ventas` o `tss_cuarentena_inventario` cuando el pipeline rechaza registros |
| `OP-AUDIT` | Auditoría | Conteos, verificaciones de integridad, estado de RLS por tabla |

Si la solicitud es ambigua, preguntar al usuario:

```
¿Qué operación de base de datos necesitas ejecutar?
Opciones: introspección / DDL / RLS / índices / conectividad / cuarentena / auditoría
```

---

## Paso 1 — Verificar Prerrequisitos

Antes de cualquier operación de escritura (`OP-DDL`, `OP-RLS`, `OP-IDX`, `OP-CUAR`):

1. Leer `docs/database/schema.sql` — fuente de verdad DDL del proyecto.
2. Leer `CLAUDE.md §"Política de Migraciones de Base de Datos"` — confirmar que el cambio tiene CC aprobado si altera el esquema.
3. Para `OP-DDL` que modifica una tabla existente: verificar en `docs/changes/` que existe un CC en estado `✅ Aprobado` que autoriza el cambio.

Si se requiere CC y no existe, detener inmediatamente:

```
BLOQUEADO — CAMBIO DE ESQUEMA SIN CC APROBADO
Toda modificación al schema requiere un Control de Cambio aprobado previamente.
Invocar /change-control para formalizar el cambio antes de continuar.
```

---

## Paso 2 — Canal de Acceso a Supabase

Usar el canal correcto según la operación:

| Canal | Cuándo usar | Nota |
|---|---|---|
| **MCP de Supabase** | Introspección (`OP-INTRO`, `OP-AUDIT`), consultas a `information_schema`, `pg_policies`, `pg_indexes` | Canal preferido para lectura y análisis |
| **`supabase-py`** | Operaciones desde código Python del pipeline (`OP-CONN`, `OP-CUAR`) | Credenciales desde `pipeline/.env` |
| **Supabase Console (DDL)** | `OP-DDL`, `OP-RLS` que crean o modifican objetos de esquema | El DDL se ejecuta en console; luego se actualiza `schema.sql` |

Las credenciales se cargan SIEMPRE desde `pipeline/.env`:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`

Nunca hardcodear credenciales, URLs, nombres de columnas o magic numbers.

---

## Paso 3 — Ejecución por Tipo de Operación

### OP-INTRO — Introspección

Verificar la existencia y estructura de tablas usando el MCP de Supabase o consultas SQL directas:

```sql
-- Verificar existencia de una tabla
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name = '{nombre_tabla}';

-- Verificar columnas de una tabla
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = '{nombre_tabla}'
ORDER BY ordinal_position;

-- Verificar políticas RLS activas
SELECT tablename, policyname, permissive, roles, cmd
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename = '{nombre_tabla}';

-- Verificar índices
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename = '{nombre_tabla}';
```

Presentar resultados en tabla comparativa contra el esquema esperado de `docs/database/schema.sql`.

---

### OP-DDL — Crear o Verificar Tablas tss_*

Solo se aplica a tablas con prefijo `tss_`. Las tablas `usr_*` son SOLO LECTURA — nunca ejecutar DDL sobre ellas.

Patrón obligatorio: usar `CREATE TABLE IF NOT EXISTS` siempre. Nunca usar `DROP TABLE` ni `TRUNCATE`.

Ejemplo de patrón DDL correcto:

```sql
CREATE TABLE IF NOT EXISTS public.tss_bronze_ventas (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    src_id       TEXT        NOT NULL,
    fecha_hora   TIMESTAMPTZ NOT NULL,
    id_sede      TEXT        NOT NULL,
    sku          TEXT        NOT NULL,
    cantidad     NUMERIC     NOT NULL,
    precio       NUMERIC     NOT NULL,
    costo        NUMERIC,
    _ingested_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    _pipeline_run_id  UUID        NOT NULL
);
```

Fuente de verdad del DDL completo: `docs/database/schema.sql`.

Después de ejecutar DDL en Supabase Console:
1. Verificar con `OP-INTRO` que la tabla existe y tiene la estructura correcta.
2. Actualizar `docs/database/schema.sql` con el DDL aplicado.
3. Confirmar al usuario la sincronización.

---

### OP-RLS — Row Level Security y Policies

Habilitar RLS en tablas `tss_*` solo. Nunca en `usr_*`.

```sql
-- Habilitar RLS en una tabla tss_*
ALTER TABLE public.{nombre_tabla} ENABLE ROW LEVEL SECURITY;

-- Crear policy de acceso para service_role
CREATE POLICY "service_role_full_access_{nombre_tabla}"
ON public.{nombre_tabla}
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);
```

Verificar el resultado con:

```sql
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename = '{nombre_tabla}';
```

Reportar estado final:

```
| Tabla | RLS Habilitado | Policy service_role | Estado |
|---|---|---|---|
| tss_bronze_ventas | ✅ | ✅ | Conforme |
```

---

### OP-IDX — Verificación e Índices

Verificar los índices de performance definidos en `docs/database/schema.sql`.

Si un índice esperado no existe, documentarlo con comentario en `schema.sql`:

```sql
-- INDEX PENDIENTE: CREATE INDEX idx_tss_bronze_ventas_fecha ON public.tss_bronze_ventas (fecha_hora);
-- Razón: mejora performance de queries con filtro por fecha en pipeline ETL.
```

No crear índices sin CC aprobado si el índice no estaba en el plan original.

---

### OP-CONN — Verificar Conectividad

Verificar que el módulo `pipeline/config.py` puede cargar las credenciales y conectar a Supabase:

```python
# Patrón de verificación de conectividad (ejecutar desde pipeline/.venv)
from pipeline.config import get_config
from supabase import create_client

config = get_config()  # carga pipeline/.env
client = create_client(config.supabase_url, config.supabase_service_key)

# Ping básico: SELECT 1 desde una tabla conocida
result = client.table("usr_sedes").select("id_sede").limit(1).execute()
assert result.data is not None, "Conexión fallida"
```

Si la conexión falla, reportar:

```
FALLO DE CONECTIVIDAD
Error: [detalle del error]
Variables verificar: SUPABASE_URL, SUPABASE_SERVICE_KEY en pipeline/.env
Ambiente virtual: pipeline/.venv debe estar activo
```

---

### OP-CUAR — Inserción en Cuarentena

El pipeline rechaza registros que violan el Data Contract. Este skill gestiona el INSERT en la tabla de cuarentena correspondiente.

Tabla destino según origen del dato:
- `usr_ventas` rechazado → `tss_cuarentena_ventas`
- `usr_inventario` rechazado → `tss_cuarentena_inventario`

Campos obligatorios en el INSERT:
- `_error_code`: código `ERR_MTD_XXX` según CLAUDE.md §"Validación y Errores"
- `_error_detail`: descripción textual del motivo de rechazo
- `_quarantined_at`: `now()` (por defecto en el schema)
- `_pipeline_run_id`: UUID del run activo desde `tss_pipeline_log`

Prohibido eliminar registros de cuarentena. Una vez insertados, son inmutables.

---

### OP-AUDIT — Auditoría de Integridad

Ejecutar verificaciones de estado para un reporte de salud de la base de datos:

```sql
-- Conteo de registros por tabla
SELECT
  'tss_bronze_ventas'    AS tabla, COUNT(*) AS registros FROM public.tss_bronze_ventas
UNION ALL SELECT
  'tss_bronze_inventario', COUNT(*) FROM public.tss_bronze_inventario
UNION ALL SELECT
  'tss_silver_ventas',     COUNT(*) FROM public.tss_silver_ventas
UNION ALL SELECT
  'tss_silver_inventario', COUNT(*) FROM public.tss_silver_inventario
UNION ALL SELECT
  'tss_gold_daily_sales',  COUNT(*) FROM public.tss_gold_daily_sales
UNION ALL SELECT
  'tss_cuarentena_ventas', COUNT(*) FROM public.tss_cuarentena_ventas
ORDER BY tabla;

-- Estado de RLS por tabla tss_*
SELECT tablename, rowsecurity AS rls_activo
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename LIKE 'tss_%'
ORDER BY tablename;
```

Presentar resultado en tabla estructurada y señalar anomalías detectadas.

---

## Paso 4 — Sincronización de schema.sql

Después de cualquier operación `OP-DDL` o `OP-RLS` aplicada en Supabase Console:

1. Leer el archivo actual `docs/database/schema.sql`.
2. Agregar o actualizar el bloque DDL correspondiente.
3. Escribir el archivo actualizado.
4. Confirmar: "schema.sql sincronizado — refleja el estado actual de Supabase."

La estructura de `docs/database/schema.sql` sigue el orden:
1. Tablas `usr_*` (solo como referencia comentada — Triple S no las crea)
2. Tablas `tss_bronze_*`
3. Tablas `tss_silver_*`
4. Tablas `tss_gold_*`
5. Tablas `tss_pipeline_log`, `tss_error_log`
6. Tablas `tss_cuarentena_*`
7. Bloques de RLS y policies
8. Índices (o comentarios `-- INDEX PENDIENTE`)

---

## Paso 5 — Reporte Final

Al completar la operación, presentar un reporte conciso:

```
OPERACION: [OP-INTRO / OP-DDL / OP-RLS / OP-IDX / OP-CONN / OP-CUAR / OP-AUDIT]
ESTADO: Completado / Bloqueado / Parcial

| Acción ejecutada | Resultado | Notas |
|---|---|---|
| [descripción] | OK / ERROR | [detalle si aplica] |

schema.sql: [Actualizado / Sin cambios requeridos]
Próxima acción sugerida: [si aplica]
```

---

## Restricciones Innegociables

1. **PROHIBIDO alterar tablas `usr_*`**: Son propiedad del cliente, solo lectura. Ningún DDL, DML de escritura ni DROP sobre `usr_ventas`, `usr_inventario`, `usr_productos`, `usr_sedes`.
2. **PROHIBIDO eliminar registros**: Ningún `DELETE` ni `TRUNCATE` en ninguna tabla, ni `tss_*` ni `usr_*`. Los datos de cuarentena son inmutables.
3. **PROHIBIDO hardcodear credenciales**: Toda credencial proviene de `pipeline/.env` vía `pipeline/config.py`. Nunca en código ni en este skill.
4. **PROHIBIDO modificar schema sin CC**: Todo cambio de estructura (nueva columna, nueva tabla, alteración de tipo) requiere CC aprobado en `docs/changes/` antes de ejecutar.
5. **Siempre `IF NOT EXISTS`**: DDL de creación usa `CREATE TABLE IF NOT EXISTS` para ser idempotente y seguro.
6. **MCP como canal preferido para introspección**: Usar el MCP de Supabase para consultas de solo lectura a `information_schema`, `pg_policies`, `pg_indexes`. `supabase-py` se reserva para operaciones desde código Python del pipeline.
7. **Ambiente virtual obligatorio**: Las ejecuciones Python usan siempre `pipeline/.venv`. Nunca Python global.
