---
name: pipeline-code
description: "Implementa código Python del pipeline de datos para el proyecto Almacén TuHogar siguiendo TDD estricto (Red → Green → Refactor). USAR SIEMPRE que se necesite: crear o actualizar pipeline/requirements.txt, pipeline/config.py o pipeline/.env.example; escribir tests pytest en pipeline/tests/; implementar módulos en pipeline/src/ o pipeline/pipelines/. Responsable de TSK-2-01 (ambiente virtual), TSK-2-02 (archivos .env), TSK-2-03 (config.py con get_supabase_client()), y TSK-2-10 a TSK-2-13 (suite pytest test_infra_connectivity.py con 24 tests). Disparar ante frases como 'implementa el config', 'crea el requirements', 'escribe los tests de conectividad', 'pipeline-code', 'implementa la suite pytest', 'crea el ambiente virtual'."
invocation: user
triggers:
  - pipeline-code
  - implementa el config
  - crea el requirements
  - escribe los tests de conectividad
  - implementa la suite pytest
  - crea el ambiente virtual
  - configura el pipeline python
  - implementa config.py
  - crea requirements.txt
  - tests de infraestructura
  - suite pytest conectividad
  - crea el .env.example
  - implementa get_supabase_client
---

# Skill: /pipeline-code — Implementación TDD del Pipeline Python

Eres el implementador de código Python del pipeline de datos. Tu dominio exclusivo son los archivos bajo `pipeline/`: configuración de entorno, módulos de código y la suite pytest de conectividad. Todo lo que escribes sigue TDD estricto y las convenciones de `CLAUDE.md`.

> Mandato estructural: ver **CLAUDE.md §"Estándares y Convenciones de Código"**, **§"Testing (TDD Universal)"**, **§"Seguridad y Configuración"** y **§"Ambiente Virtual Python"**.

---

## Constraint Critico — Credenciales Reales Requeridas

Las siguientes tareas ESTAN BLOQUEADAS hasta que las credenciales `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` estén disponibles en `pipeline/.env`:

| Tarea | Motivo del bloqueo |
|---|---|
| `[TSK-2-02]` | Requiere credenciales reales para crear `pipeline/.env` |
| `[TSK-2-10]` | Los tests de configuración leen variables de entorno reales |
| `[TSK-2-11]` | Los tests de estructura conectan contra Supabase real |
| `[TSK-2-12]` | Los tests de RLS ejecutan queries reales a `pg_policies` |
| `[TSK-2-13]` | La suite completa requiere conexión a Supabase activa |

Si las credenciales no están disponibles, este skill puede ejecutar las tareas que NO dependen de ellas: `[TSK-2-01]` (crear `.venv` y `requirements.txt`) y la estructura de archivos de `[TSK-2-03]`. Documentar el bloqueo en `PROJECT_handoff.md` y escalar al responsable antes de continuar.

---

## Paso 0 — Identificar la Tarea Solicitada

Antes de ejecutar, clasifica la solicitud:

| Tarea | Descripción | Bloqueada sin credenciales |
|---|---|---|
| `[TSK-2-01]` | Crear `pipeline/.venv` e instalar dependencias desde `requirements.txt` | No |
| `[TSK-2-02]` | Crear `pipeline/.env` y `pipeline/.env.example` | Si (`pipeline/.env`) |
| `[TSK-2-03]` | Implementar `pipeline/config.py` con `get_supabase_client()` | No (estructura), Si (verificacion) |
| `[TSK-2-10]` | Implementar TDD `TestEnvironmentConfig` + `TestSupabaseConnectivity` | Si |
| `[TSK-2-11]` | Implementar TDD `TestClientTableStructure` (10 tests) | Si |
| `[TSK-2-12]` | Implementar TDD `TestTripleSTableStructure` + `TestRLSPolicies` (8 tests) | Si |
| `[TSK-2-13]` | Implementar `TestPerformanceIndexes` + ejecutar suite completa | Si |

Si la solicitud es ambigua, preguntar:

```
¿Qué tarea del pipeline quieres implementar?
Opciones: TSK-2-01 (venv) / TSK-2-02 (env files) / TSK-2-03 (config.py) / TSK-2-10 a TSK-2-13 (pytest suite)
¿Tienes credenciales Supabase disponibles en pipeline/.env?
```

---

## Paso 1 — Verificar Prerrequisitos

Antes de escribir cualquier archivo:

1. Leer `docs/tasks/f01_02_task.md` — confirmar que la tarea solicitada está en el mapa de dependencias.
2. Verificar dependencias de la tarea (ver mapa en el Task doc).
3. Para tareas de código: verificar que `pipeline/.venv` existe y está activo.
4. Para tareas de tests: verificar que `pipeline/config.py` existe (`[TSK-2-03]` completa).

Si una dependencia no está satisfecha:

```
BLOQUEADO — DEPENDENCIA NO SATISFECHA
La tarea [TSK-2-XX] requiere [TSK-2-YY] completada primero.
Completar [TSK-2-YY] antes de continuar.
```

---

## Paso 2 — Ejecucion por Tarea

### TSK-2-01 — Ambiente Virtual y requirements.txt

**Archivos a crear:** `pipeline/requirements.txt`, `pipeline/.venv/`

**Dependencias exactas** (versiones minimas segun SPEC `[ARC-06]`):

```
supabase>=2.0.0
python-dotenv>=1.0.0
pytest>=7.4.0
pytest-cov>=4.1.0
```

**Pasos de implementacion:**

```bash
# 1. Crear requirements.txt
# 2. Crear el ambiente virtual
cd pipeline && python -m venv .venv

# 3. Activar (Windows)
source .venv/Scripts/activate
# O en Linux/Mac:
# source .venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

**Verificar que `.gitignore` contiene `pipeline/.venv`** — si no, agregar la entrada antes de continuar.

**DoD (`[MET-*]`):** `pip list` dentro del `.venv` muestra `supabase`, `python-dotenv`, `pytest`, `pytest-cov` con versiones conformes. `.venv/` listado en `.gitignore`.

---

### TSK-2-02 — Archivos .env

**Archivos a crear:** `pipeline/.env` (credenciales reales), `pipeline/.env.example` (placeholders)

**CONSTRAINT CRITICO:** `pipeline/.env` NUNCA debe aparecer en `git status`. Verificar `.gitignore` antes de crear el archivo.

**Estructura de `pipeline/.env`** (con credenciales reales — NO publicar en Git):

```
SUPABASE_URL=https://[project-id].supabase.co
SUPABASE_SERVICE_KEY=[service-role-key]
```

**Estructura de `pipeline/.env.example`** (con placeholders — SI se versiona en Git):

```
SUPABASE_URL=https://XXXX.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here
```

**Verificacion antes de commitear:**

```bash
git status  # pipeline/.env NO debe aparecer
```

**DoD:** `pipeline/.env` existe localmente y NO aparece en `git status`. `pipeline/.env.example` aparece versionado con placeholders.

---

### TSK-2-03 — pipeline/config.py

**Archivo a crear:** `pipeline/config.py`

**Interfaz obligatoria** (segun SPEC seccion 3.1, componente `[ARC-06]`):

```python
from dotenv import load_dotenv
import os
from supabase import create_client, Client


def get_supabase_client() -> Client:
    """Retorna cliente Supabase autenticado con service_role key.

    Carga SUPABASE_URL y SUPABASE_SERVICE_KEY desde .env con python-dotenv.
    Lanza EnvironmentError si alguna variable falta.
    NUNCA acepta valores hardcodeados.
    """
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")

    if not url:
        raise EnvironmentError(
            "SUPABASE_URL no esta configurada en pipeline/.env"
        )
    if not key:
        raise EnvironmentError(
            "SUPABASE_SERVICE_KEY no esta configurada en pipeline/.env"
        )

    return create_client(url, key)
```

**Restricciones absolutas:**
- Prohibido hardcodear URL, keys o cualquier valor de credencial.
- Prohibido usar `os.environ[]` directamente sin `load_dotenv()` primero.
- La funcion debe lanzar `EnvironmentError` (no `ValueError`, no `Exception`) con mensaje descriptivo.

**DoD:** `python -c "from config import get_supabase_client; c = get_supabase_client(); print('OK')"` ejecutado desde `pipeline/` retorna `OK` sin errores.

---

### TSK-2-10 — TestEnvironmentConfig + TestSupabaseConnectivity

**Archivo:** `pipeline/tests/test_infra_connectivity.py`
**Tambien crear:** `pipeline/tests/__init__.py` (vacio)

**TDD obligatorio:** Escribir el test primero → ejecutar (debe FALLAR porque config.py no existe aun o env no esta configurado) → implementar codigo minimo → ejecutar (debe PASAR).

**Fixture de sesion** (compartido por toda la suite, una sola conexion):

```python
import pytest
import time
from pipeline.config import get_supabase_client  # ajustar import segun estructura


@pytest.fixture(scope="session")
def client():
    return get_supabase_client()
```

**Clases y tests a implementar** (segun SPEC seccion 3.2, componentes `[ARC-03]`, `[ARC-06]`):

```python
class TestEnvironmentConfig:
    def test_supabase_url_present(self):
        """SUPABASE_URL existe en .env y no esta vacia."""

    def test_supabase_service_key_present(self):
        """SUPABASE_SERVICE_KEY existe en .env y no esta vacia."""

    def test_supabase_client_instantiates(self):
        """get_supabase_client() retorna cliente sin excepciones."""

    def test_missing_variable_raises_environment_error(self):
        """EnvironmentError si falta una variable requerida."""


class TestSupabaseConnectivity:
    def test_connection_select_one(self, client):
        """Ejecuta SELECT contra Supabase. Retorna resultado."""

    def test_connection_latency(self, client):
        """Tiempo de round-trip al servidor < 3000ms."""
```

**DoD:** `pytest tests/test_infra_connectivity.py::TestEnvironmentConfig tests/test_infra_connectivity.py::TestSupabaseConnectivity -v` → 5/5 pasan, exit code 0.

---

### TSK-2-11 — TestClientTableStructure

**Archivo:** `pipeline/tests/test_infra_connectivity.py` (agregar a la suite existente)

**Helper obligatorio** (segun SPEC seccion 3.3, componente `[ARC-01]`):

```python
def get_table_columns(client, table_name: str) -> list[str]:
    """
    Retorna lista de nombres de columnas via information_schema.
    Usa supabase-py para ejecutar la query SQL.
    """
    result = client.table("information_schema.columns").select("column_name").eq(
        "table_schema", "public"
    ).eq("table_name", table_name).execute()
    return [row["column_name"] for row in result.data]
```

**Tests a implementar** (10 tests, componentes `[ARC-01]`, `[ARC-03]`):

```python
class TestClientTableStructure:
    # Columnas esperadas segun SPEC seccion 2.1
    EXPECTED_COLUMNS = {
        "usr_ventas":      ["id", "fecha_hora", "id_sede", "sku", "cantidad", "precio", "costo"],
        "usr_inventario":  ["id", "fecha_hora", "id_sede", "sku", "stock_fisico"],
        "usr_productos":   ["sku", "nombre", "familia", "categoria", "subcategoria"],
        "usr_sedes":       ["id_sede", "nombre", "ciudad"],
    }

    def test_usr_ventas_exists(self, client): ...
    def test_usr_ventas_required_columns(self, client): ...
    def test_usr_inventario_exists(self, client): ...
    def test_usr_inventario_required_columns(self, client): ...
    def test_usr_productos_exists(self, client): ...
    def test_usr_productos_required_columns(self, client): ...
    def test_usr_productos_has_records(self, client): ...       # COUNT >= 1
    def test_usr_sedes_exists(self, client): ...
    def test_usr_sedes_required_columns(self, client): ...
    def test_usr_sedes_has_exactly_seven_records(self, client): ...  # COUNT == 7
```

**DoD:** `pytest tests/test_infra_connectivity.py::TestClientTableStructure -v` → 10/10 pasan, exit code 0.

---

### TSK-2-12 — TestTripleSTableStructure + TestRLSPolicies

**Archivo:** `pipeline/tests/test_infra_connectivity.py` (agregar a la suite existente)

**Lista completa de tablas tss_*** (segun SPEC seccion 3.2, componente `[ARC-02]`):

```python
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
```

**Tests a implementar** (8 tests, componentes `[ARC-03]`, `[ARC-05]`):

```python
class TestTripleSTableStructure:
    def test_all_tss_tables_exist(self, client):
        """Las 10 tablas tss_* existen. Falla con lista de faltantes."""

    def test_tss_pipeline_log_columns(self, client):
        """Columnas: run_id, run_at, mode, status, records_processed,
           records_quarantined, errors, duration_s, error_detail."""

    def test_tss_bronze_ventas_columns(self, client):
        """Columnas: id, src_id, fecha_hora, id_sede, sku, cantidad,
           precio, costo, _ingested_at, _pipeline_run_id."""

    def test_tss_cuarentena_ventas_columns(self, client):
        """Columnas: id, src_id, _error_code, _error_detail,
           _quarantined_at, _pipeline_run_id."""


class TestRLSPolicies:
    def test_usr_tables_rls_enabled(self, client):
        """RLS habilitado en las 4 tablas usr_*. Consulta pg_tables.rowsecurity."""

    def test_tss_tables_rls_enabled(self, client):
        """RLS habilitado en las 10 tablas tss_*. Consulta pg_tables.rowsecurity."""

    def test_service_role_can_read_usr_ventas(self, client):
        """service_role puede SELECT en usr_ventas sin error."""

    def test_service_role_can_write_tss_pipeline_log(self, client):
        """service_role puede INSERT en tss_pipeline_log.
           OBLIGATORIO: limpiar (DELETE) el registro de prueba al finalizar."""
```

**Restriccion critica para `test_service_role_can_write_tss_pipeline_log`:**
El test debe limpiar el registro insertado. Usar `try/finally` o fixture con teardown para garantizar que no queden datos de prueba en `tss_pipeline_log`.

**DoD:** `pytest tests/test_infra_connectivity.py::TestTripleSTableStructure tests/test_infra_connectivity.py::TestRLSPolicies -v` → 8/8 pasan. Verificar con SELECT que no quedan registros de prueba en `tss_pipeline_log`.

---

### TSK-2-13 — TestPerformanceIndexes + Ejecucion Suite Completa

**Archivo:** `pipeline/tests/test_infra_connectivity.py` (agregar a la suite existente)

**Tests a implementar** (1 test, componentes `[ARC-03]`, `[ARC-05]`):

```python
class TestPerformanceIndexes:
    REQUIRED_INDEXES = [
        ("usr_ventas",     "fecha_hora"),
        ("usr_ventas",     "sku"),
        ("usr_ventas",     "id_sede"),
        ("usr_inventario", "sku"),
        ("usr_inventario", "id_sede"),
    ]

    def test_required_indexes_exist(self, client):
        """Verifica cada indice en pg_indexes.
        IMPORTANTE: usar logging.warning para indices faltantes — NUNCA pytest.fail.
        Los indices son Media prioridad segun PRD [REQ-11]."""
```

**Convencion critica:** `TestPerformanceIndexes` usa `logging.warning` cuando falta un indice, NO `pytest.fail`. El test debe pasar aunque falten indices — solo emite advertencias.

**Comando de ejecucion de cierre** (ejecutar tras implementar los 24 tests):

```bash
cd pipeline && source .venv/Scripts/activate
pytest tests/test_infra_connectivity.py -v --cov=. --cov-report=term-missing
```

**DoD ([MET-03]):** exit code 0, 0 FAILs, tiempo total < 30 s, cobertura >= 90%.

---

## Paso 3 — Patron TDD Obligatorio

Para cada test nuevo, seguir este ciclo sin excepcion:

```
1. RED   → Escribir el test. Ejecutar: debe FALLAR (NameError, ImportError o AssertionError).
           Si pasa en verde sin codigo implementado, el test es invalido — revisar.

2. GREEN → Implementar el codigo minimo para que el test pase.
           No agregar logica extra. Solo lo que el test exige.

3. REFACTOR → Limpiar el codigo sin romper el test.
              Revisar: nombres claros, sin duplicacion, sin magic numbers.
```

Si en cualquier paso el test pasa inesperadamente antes de implementar codigo, detener y reportar al usuario — puede indicar un test mal diseñado o una condicion ya satisfecha por codigo existente.

---

## Paso 4 — Convenciones Criticas de Implementacion

### Imports y estructura del archivo de tests

```python
# pipeline/tests/test_infra_connectivity.py
import os
import logging
import time
import pytest
from dotenv import load_dotenv

# Ajustar segun estructura de modulos del proyecto
# Si se ejecuta desde pipeline/: from config import get_supabase_client
# Si se ejecuta desde raiz:       from pipeline.config import get_supabase_client

load_dotenv("pipeline/.env")  # o load_dotenv() si se ejecuta desde pipeline/
```

### Fixture de sesion (una sola conexion por ejecucion)

```python
@pytest.fixture(scope="session")
def client():
    """Una sola instancia de cliente Supabase por ejecucion completa."""
    return get_supabase_client()
```

### Queries a information_schema via supabase-py

Las queries a `information_schema`, `pg_tables`, `pg_policies` y `pg_indexes` se ejecutan con SQL directo via `supabase-py`:

```python
# Ejemplo: verificar si una tabla existe
result = client.rpc("query_via_sql", {"sql": "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'usr_ventas'"}).execute()

# Alternativa usando el cliente directo (si la API lo permite):
result = client.from_("information_schema.tables").select("table_name").eq("table_schema", "public").eq("table_name", "usr_ventas").execute()
```

Si `supabase-py` no permite queries directas a `information_schema`, usar el metodo `postgrest_client.rpc()` o construir la query via `client.postgrest`.

### Prohibiciones absolutas

- **Prohibido** usar `pytest.fail` en `TestPerformanceIndexes` — solo `logging.warning`.
- **Prohibido** dejar registros de prueba en `tss_pipeline_log` tras `test_service_role_can_write_tss_pipeline_log`.
- **Prohibido** hardcodear credenciales, URLs o IDs en los tests.
- **Prohibido** instalar dependencias en Python global — siempre `pipeline/.venv`.
- **Prohibido** escribir logica de negocio en los tests — los tests verifican infraestructura, no implementan ETL.

---

## Paso 5 — Reporte Final

Al completar una tarea, presentar:

```
TAREA: [TSK-2-XX] — [nombre]
ESTADO: Completado / Bloqueado / Parcial
COMPONENTE [ARC]: [ARC-XX]

| Archivo creado/modificado | Accion | Resultado |
|---|---|---|
| pipeline/[archivo] | Creado / Modificado | OK / ERROR |

Tests: [N]/[N] pasan
Cobertura: [X]%
Proxima tarea sugerida: [TSK-2-XX]
```

Si la tarea esta bloqueada por credenciales:

```
BLOQUEADO — CREDENCIALES REQUERIDAS
[TSK-2-XX] requiere SUPABASE_URL y SUPABASE_SERVICE_KEY en pipeline/.env.
Accion requerida: obtener credenciales del cliente y configurar pipeline/.env.
Documentar bloqueo en PROJECT_handoff.md.
```

---

## Referencia de Componentes ARC

| Componente | Archivo | Tareas |
|---|---|---|
| `[ARC-01]` | `pipeline/tests/test_infra_connectivity.py` | TSK-2-11 |
| `[ARC-02]` | `docs/database/schema.sql` | TSK-2-06, TSK-2-07, TSK-2-08 (gestionado por `/db-management`) |
| `[ARC-03]` | `pipeline/tests/test_infra_connectivity.py` | TSK-2-10, TSK-2-11, TSK-2-12, TSK-2-13 |
| `[ARC-04]` | `docs/database/schema.sql` | TSK-2-14 (gestionado por `/db-management`) |
| `[ARC-05]` | `pipeline/tests/test_infra_connectivity.py` | TSK-2-12, TSK-2-13 |
| `[ARC-06]` | `pipeline/config.py` | TSK-2-01, TSK-2-02, TSK-2-03 |

> Las tareas de DDL y schema.sql (`[ARC-02]`, `[ARC-04]`) son responsabilidad del skill `/db-management`, no de este skill.
