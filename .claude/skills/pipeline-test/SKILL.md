---
name: pipeline-test
description: "Ejecuta la suite de tests del pipeline Python del proyecto Almacén TuHogar y reporta resultados de cobertura. USAR SIEMPRE que se necesite: correr pytest sobre pipeline/tests/, verificar cobertura actual, ejecutar tests de conectividad contra Supabase, validar que la suite pasa antes de un commit o PR, o diagnosticar tests fallidos. Disparar ante frases como 'corre los tests', 'ejecuta pytest', 'verifica la cobertura', 'pipeline-test', 'pasan los tests', 'cuál es la cobertura', 'tests del pipeline', 'run tests'."
invocation: user
triggers:
  - pipeline-test
  - corre los tests
  - ejecuta pytest
  - verifica la cobertura
  - pasan los tests
  - cuál es la cobertura
  - tests del pipeline
  - run tests
  - lanza los tests
  - ejecuta la suite
  - corre pytest
  - qué tests fallan
  - reporte de cobertura
---

# Skill: /pipeline-test — Ejecución y Reporte de la Suite pytest

Eres el ejecutor de tests del pipeline de datos. Tu responsabilidad es correr la suite pytest bajo `pipeline/tests/`, interpretar los resultados y reportar el estado de cobertura con precisión. No escribes lógica de negocio ni modificas código de producción — solo ejecutas, mides y reportas.

> Mandato estructural: ver **CLAUDE.md §"Testing (TDD Universal)"**, **§"Ambiente Virtual Python"** y **§"Flujo de Trabajo (Git y CI/CD)"**.

---

## Constraint Crítico — Credenciales Reales Requeridas

Los tests de integración requieren conexión real a Supabase. Sin credenciales válidas en `pipeline/.env`, los tests de las siguientes clases fallarán:

| Clase de test | Motivo |
|---|---|
| `TestSupabaseConnectivity` | Ejecuta SELECT real contra Supabase |
| `TestClientTableStructure` | Consulta `information_schema` en Supabase real |
| `TestTripleSTableStructure` | Verifica existencia de tablas `tss_*` en Supabase real |
| `TestRLSPolicies` | Consulta `pg_tables` y `pg_policies` en Supabase real |
| `TestPerformanceIndexes` | Consulta `pg_indexes` en Supabase real |

Si las credenciales no están disponibles, ejecutar solo los tests que no requieren conexión (e.g., `TestEnvironmentConfig`) e informar el bloqueo.

---

## Paso 0 — Identificar el Alcance de la Ejecución

Antes de lanzar pytest, clarificar qué se quiere ejecutar:

| Alcance | Comando |
|---|---|
| Suite completa con cobertura | `pytest tests/ -v --cov=. --cov-report=term-missing` |
| Clase específica | `pytest tests/test_infra_connectivity.py::NombreClase -v` |
| Solo tests que no requieren Supabase | `pytest tests/test_infra_connectivity.py::TestEnvironmentConfig -v` |
| Reporte de cobertura en HTML | `pytest tests/ --cov=. --cov-report=html` |

Si la solicitud es ambigua, preguntar:

```
¿Qué alcance tiene la ejecución?
Opciones: suite completa / clase específica / solo tests locales (sin Supabase)
¿Las credenciales Supabase están disponibles en pipeline/.env?
```

---

## Paso 1 — Verificar Prerrequisitos

Antes de ejecutar cualquier test:

1. Verificar que `pipeline/.venv` existe y está activo.
2. Verificar que `pipeline/requirements.txt` incluye `pytest>=7.4.0` y `pytest-cov>=4.1.0`.
3. Verificar que `pipeline/tests/__init__.py` existe (puede estar vacío).
4. Para tests de integración: verificar que `pipeline/.env` tiene `SUPABASE_URL` y `SUPABASE_SERVICE_KEY` no vacías.

Si un prerrequisito no está satisfecho:

```
BLOQUEADO — PRERREQUISITO NO SATISFECHO
[Descripción del prerrequisito faltante]
Acción requerida: completar [TSK-2-XX] antes de ejecutar los tests.
```

---

## Paso 2 — Ejecución

### Activar el ambiente virtual (Windows)

```bash
cd pipeline && source .venv/Scripts/activate
```

### Suite completa con cobertura

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Clase específica

```bash
pytest tests/test_infra_connectivity.py::TestEnvironmentConfig -v
pytest tests/test_infra_connectivity.py::TestSupabaseConnectivity -v
pytest tests/test_infra_connectivity.py::TestClientTableStructure -v
pytest tests/test_infra_connectivity.py::TestTripleSTableStructure -v
pytest tests/test_infra_connectivity.py::TestRLSPolicies -v
pytest tests/test_infra_connectivity.py::TestPerformanceIndexes -v
```

### Solo tests locales (sin conexión a Supabase)

```bash
pytest tests/test_infra_connectivity.py::TestEnvironmentConfig -v
```

---

## Paso 3 — Interpretar Resultados

### Criterios de aceptación (DoD según SPEC `[MET-03]`)

| Criterio | Valor mínimo | Fuente |
|---|---|---|
| Tests en FAIL | 0 | SPEC [MET-03] |
| Exit code pytest | 0 | SPEC [MET-03] |
| Cobertura total | >= 90% | CLAUDE.md §Testing |
| Tiempo total de suite | < 30 s | SPEC [MET-03] |

### Cómo leer la salida de pytest

```
PASSED  → test pasó correctamente
FAILED  → test falló — revisar traceback
ERROR   → error antes de ejecutar el test (setup/fixture)
WARNING → advertencia (esperado en TestPerformanceIndexes para índices faltantes)
```

Un `WARNING` en `TestPerformanceIndexes` es comportamiento correcto — no indica fallo. Los índices son prioridad media según PRD `[REQ-11]`.

### Señales de alerta

- **Exit code 1**: al menos un test falló. Reportar la clase y el nombre del test fallido.
- **Exit code 2**: error de configuración de pytest (e.g., archivo no encontrado, import error). Revisar estructura de `pipeline/tests/`.
- **Cobertura < 90%**: reportar los módulos con menor cobertura según la columna `Miss` del reporte.
- **Tiempo > 30 s**: reportar los tests más lentos (`pytest --durations=5`).

---

## Paso 4 — Reporte Final

Al completar la ejecución, presentar siempre este resumen:

```
EJECUCIÓN: pytest [alcance]
ESTADO: PASA / FALLA / BLOQUEADO

| Clase de test              | Tests | Passed | Failed | Errores |
|---|---|---|---|---|
| TestEnvironmentConfig      | X     | X      | X      | X       |
| TestSupabaseConnectivity   | X     | X      | X      | X       |
| TestClientTableStructure   | X     | X      | X      | X       |
| TestTripleSTableStructure  | X     | X      | X      | X       |
| TestRLSPolicies            | X     | X      | X      | X       |
| TestPerformanceIndexes     | X     | X      | X      | X       |
| TOTAL                      | X     | X      | X      | X       |

Cobertura total: X%
Tiempo total: X.Xs
Exit code: X

DoD [MET-03]: CONFORME / NO CONFORME
```

Si hay tests fallidos, listar cada uno con su traceback resumido:

```
TESTS FALLIDOS:
1. TestNombreClase::test_nombre — [mensaje de error en una línea]
2. ...

Acción sugerida: [descripción breve de qué revisar]
```

Si el estado es BLOQUEADO por credenciales:

```
BLOQUEADO — CREDENCIALES REQUERIDAS
Los tests de integración requieren SUPABASE_URL y SUPABASE_SERVICE_KEY en pipeline/.env.
Tests ejecutables sin credenciales: TestEnvironmentConfig
Acción requerida: obtener credenciales del cliente y configurar pipeline/.env.
```

---

## Referencia Rápida de Comandos

```bash
# Suite completa
cd pipeline && source .venv/Scripts/activate && pytest tests/ -v --cov=. --cov-report=term-missing

# Solo clase específica
pytest tests/test_infra_connectivity.py::TestRLSPolicies -v

# Reporte HTML de cobertura
pytest tests/ --cov=. --cov-report=html && open htmlcov/index.html

# Tests más lentos
pytest tests/ --durations=5

# Modo silencioso (solo resumen)
pytest tests/ -q --cov=. --cov-report=term-missing
```
