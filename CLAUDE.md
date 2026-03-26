# CLAUDE.md

Este archivo define las leyes, límites y terreno de juego para cualquier Agente de IA que interactúe con este repositorio. Es de lectura obligatoria y cumplimiento dogmático.

Desarrollado por **Sabbia Solutions & Services (Triple S)**

## Reglas de Comportamiento

### Comunicación
1. **Tono**: Educado y profesional en todas las respuestas.
2. **Concisión**: Respuestas cortas y concisas. Solicita permiso del usuario si necesitas ampliar.

### Ejecución de Trabajo
3. **Revisión de Código**: Después de completar un cambio o feature, lanza uno o dos agentes de revisión para asegurar la calidad.
4. **Uso de Agentes**: Prioriza siempre la construccion, revision y pruebas de código y documentación a través de agentes (subagentes). Utilízalos en paralelo cuando sea posible.

## Límites de Autonomía

- **Prohibido avanzar** a una nueva fase/etapa sin orden explícita del usuario ("Procede", "Siguiente", "Avanza").
- **Prohibido escribir archivos** sin petición o confirmación explícita.
- La proactividad se limita a análisis y sugerencias en el chat.
- **Prohibido proponer o ejecutar trabajo de una nueva etapa** si el documento `docs/executives/f[F]_[E]_executive.md` de la etapa anterior no existe. El Resumen Ejecutivo es prerequisito de avance, no un opcional.

## Desarrollo Spec-Driven

El código es un reflejo **sumiso** de la documentación. Jerarquía documental:
1. **`docs/reqs/f[F]_[E]_prd.md`** — Qué construir (fuente de verdad de negocio).
2. **`docs/specs/f[F]_[E]_spec.md`** — Cómo construirlo (contratos, interfaces, comportamiento).
3. **`docs/plans/f[F]_[E]_plan.md`** — Orden y estrategia de ejecución.
4. **`docs/tasks/f[F]_[E]_task.md`** — Tareas ejecutables.

**Regla de oro**: Si durante la implementación hay algo no contemplado, **DETENER** y solicitar actualización del documento correspondiente antes de continuar. Ante discrepancia entre documentos, la jerarquía PRD → SPEC → Plan → Tareas define quién manda.

## Control de Cambios

Detener toda implementación y ejecutar `/change-control` en dos casos:
1. **Cambio en etapa activa**: Algo necesario no está en los documentos SDD. Prohibido improvisar.
2. **Cambio en etapa cerrada**: Cualquier modificación a código, configuración o documentos ya completados.

Flujo obligatorio: Informar la necesidad → usuario aprueba → crear `docs/changes/CC_XXXXX.md` en estado `Pendiente` → usuario confirma → estado `Aprobado` → ejecutar cambios → informar cierre. Si el usuario rechaza, estado `No Aprobado` y no se toca nada.

## Protocolo de Inicio de Sesión

En orden obligatorio:
1. Leer `CLAUDE.md` — Reglas globales del proyecto.
2. Leer `PROJECT_handoff.md` — Estado macro y táctico: fase/etapa activa, hitos, arquitectura, decisiones históricas, archivos activos, bloqueadores y próxima acción.
3. Leer `docs/lessons/lessons-learned.md` — Solo sección de etapa activa.
4. Leer `docs/changes/` — Solo CCs en estado `✅ Aprobado`.
5. Leer `docs/database/schema.sql` — Esquema actual de Supabase.

Solo después está autorizado a escribir código o ejecutar acciones.

## Protocolo de Cierre de Sesión

Al fin de sesión, **obligatoriamente** reescribe `PROJECT_handoff.md` con:
- Archivos modificados
- Contexto inmediato
- Último error/bloqueador
- Próxima acción concreta

## Estándares y Convenciones de Código

### Arquitectura de Datos (Medallion en Supabase)
- **Bronze** (`tss_bronze_*`): Raw data sin modificar desde tablas cliente (`usr_*`).
- **Silver** (`tss_silver_*`): Datos limpios, validados, timezone convertido a COT.
- **Gold** (`tss_gold_*`): Métricas derivadas, clasificación ABC, indicadores de alertas.

### Validación y Errores
- **Validación obligatoria**: Esquemas Pandera para capas Silver y Gold. Deben reflejar exactamente los Data Contracts.
- **Gestión de errores**: Prohibido `pass`. Mapear a códigos `ERR_MTD_XXX`:
  - `ERR_MTD_001` — Transacción fuera de ventana (8 AM–6 PM COT)
  - `ERR_MTD_002` — SKU no registrado
  - `ERR_MTD_003` — Sede no registrada
  - `ERR_MTD_004` — Registro con fecha T+0 (carga anticipada)
  - `ERR_MTD_005` — Violación de constraint numérico

- **Validaciones obligatorias del pipeline** (ejecutadas antes de Bronze, en este orden):
  1. `fecha_hora` en `usr_ventas` dentro de ventana operativa: `13:00–23:00 UTC`.
  2. No se aceptan registros con `fecha_hora` del día en curso (T+0).
  3. Todos los `sku` en `usr_ventas` e `usr_inventario` deben existir en `usr_productos`.
  4. Todos los `id_sede` deben existir en `usr_sedes`.
  5. `stock_fisico >= 0`, `cantidad > 0`, `precio > 0`, `costo > 0` (si no es null).

- **Protocolo ante violación del Data Contract** (orden obligatorio):
  1. Registrar el error con código `ERR_MTD_XXX` en `tss_error_log`.
  2. Enviar los registros inválidos a cuarentena en `tss_cuarentena_*`.
  3. Generar alerta interna para el equipo Triple S.
  4. Notificar formalmente al cliente con detalle del error y registros afectados.
  5. Los datos no pasan a Bronze hasta que el cliente corrija y reentregue.

### Seguridad y Configuración
- **Cero hardcoding**: Secretos en `.env` (no trackeado), configuración en `config.yaml`. Prohibido hardcodear en código: IDs de tablas, URLs de endpoints, nombres de columnas, umbrales de alertas, magic numbers, nombres de sedes o SKUs. Todo valor configurable va en `config.yaml` o en variables de entorno.
- **Timezone**: UTC → COT con `pytz` usando `America/Bogota`. Prohibido offsets manuales (`-5`).

### Fuente de Datos del Dashboard
- **Prohibido archivos locales como fuente de visualización**: El dashboard solo puede leer datos desde las tablas `tss_gold_*` en Supabase a través de las API Routes de Next.js. Prohibido leer CSVs, JSONs, SQLite u otros archivos locales para renderizar vistas. Esta regla garantiza que producción y desarrollo local muestren exactamente los mismos datos.

### Ambiente Virtual y Dependencias Python
- **Ambiente virtual obligatorio**: Todo trabajo en `pipeline/` debe ejecutarse dentro de un entorno virtual dedicado. Nombre estándar: `pipeline/.venv`. Nunca instalar dependencias en el Python global del sistema.
- **`requirements.txt` es la fuente de verdad**: Toda dependencia nueva debe agregarse a `pipeline/requirements.txt` antes de usarla en código. Prohibido importar paquetes no declarados en ese archivo.
- **Verificación rápida**:
  ```bash
  # Crear y activar (primera vez)
  python -m venv pipeline/.venv
  source pipeline/.venv/Scripts/activate   # Windows
  source pipeline/.venv/bin/activate        # macOS/Linux
  pip install -r pipeline/requirements.txt

  # Agregar nueva dependencia
  pip install <paquete>
  pip freeze | grep <paquete> >> pipeline/requirements.txt
  ```
- **`.venv` no se trackea en Git**: Asegurarse que `pipeline/.venv/` esté en `.gitignore`.

### Arquitectura de Código
- **Separación de responsabilidades**: Lógica de negocio solo en `src/`. Prohibido en `main.py` o `pipelines/`.
- **Triple persistencia**: Registrar éxito/fallo en: (1) archivo local `latest`, (2) log con timestamp, (3) tabla `tss_pipeline_log`.
- **DVC obligatorio**: Prohibido subir datasets, artefactos pesados o modelos a Git. Todo archivo de datos (CSV, Parquet, pickle, modelos, etc.) debe versionarse con DVC y almacenarse en el remote configurado. Flujo obligatorio: `dvc add <archivo>` → commit del `.dvc` → `dvc push`. El archivo `.dvc` sí se trackea en Git; el dato, nunca.
- **SQL-First**: Transformaciones pesadas en SQL (Supabase), no en Python.

### Testing y Desarrollo
- **TDD obligatorio**: Todo archivo Python creado en el proyecto debe seguir el ciclo: (1) Test primero, (2) código mínimo que lo haga pasar, (3) refactorizar. Sin excepción de módulo, script o archivo de soporte.
  - Tests en `pipeline/tests/` espejando estructura de `pipeline/src/`.
  - Conectores: integration tests contra Supabase real (sin mocks de BD).
  - Ningún archivo Python sin al menos un test de integración.
  - `main.py` y orquestadores en `pipelines/` se testean con tests de integración end-to-end, no unitarios.

### Prefijos de Tablas en Supabase
- **`usr_*`**: Propiedad del cliente (solo lectura). No alterar sin CC aprobado.
- **`tss_*`**: Propiedad de Triple S (Bronze, Silver, Gold, logs, alertas, cuarentena).

## Flujo de Trabajo (Git y CI/CD)

### Estrategia de Ramas

**Simplificado:**
- **`main`** — Rama principal. Contiene documentación (SDD, CLAUDE.md, resúmenes ejecutivos) y código de producción. Requiere protección: CI Quality Gate + aprobación manual.
- **`feat/*`** — Ramas de desarrollo. Cada feature o cambio en su propia rama. Merge a `main` solo después que CI pase.

### Commits

Formato atómico en español con prefijos:
- `feat:` — Nueva funcionalidad
- `fix:` — Corrección de errores
- `docs:` — Documentación (SDD, CLAUDE.md, comentarios)
- `refactor:` — Cambios sin nuevas funciones ni correcciones

**Ejemplo**: `feat: ETL Bronze to Silver con conversión UTC-COT`

### CI/CD (GitHub Actions)

**Quality Gate** — Corre en PRs hacia `main`. Ejecuta en paralelo:
- Tests del pipeline: `pytest pipeline/tests/`
- Tests del dashboard: `npm test`
- Linting y validación de código

**Protección de Ramas**:
- `main`: CI Quality Gate + aprobación humana obligatoria
- `feat/*`: libre (sin restricciones)

**Release** — Tags semánticos al mergear a `main`. Formato: `v1.0.0`.

### Comandos Recurrentes

**Pipeline**: `python pipeline/main.py --mode [validate|etl|alerts]`
**Web**: `npm run dev`
**Tests**: `pytest pipeline/tests/` | `npm test`

## Convenciones de Idioma

- **Código/Archivos/Carpetas**: Inglés (snake_case para archivos, CamelCase para clases).
- **Documentación/Comentarios/Commits**: Español.
- **Interfaz/Output al Usuario**: Español.

## Archivos Clave del Proyecto

- **`PROJECT_handoff.md`** — Único archivo de estado del proyecto. Combina el estado macro (fases, hitos, arquitectura, decisiones históricas) y el estado táctico de sesión (working set, contexto, bloqueadores, próxima acción). Se reescribe al cerrar cada sesión.

## Estructura de Carpetas

```
├── pipeline/               # Procesos de datos (Python)
│   ├── main.py            # Gateway/Switcher (validate, etl, alerts)
│   ├── pipelines/         # Orquestadores
│   ├── src/               # Lógica atómica (validadores, transformaciones, métricas)
│   └── tests/             # Pruebas unitarias e integrales
│
├── web/                   # Frontend (Next.js)
│   ├── components/        # Componentes UI, gráficos, tarjetas de alerta
│   ├── app/               # Rutas del dashboard (App Router)
│   └── tests/             # Pruebas de componentes y E2E
│
└── docs/                  # Documentación técnica y gobernanza
    ├── reqs/              # PRD (Product Requirements Documents)
    ├── specs/             # Especificaciones técnicas
    ├── plans/             # Planes de implementación
    ├── tasks/             # Tareas atómicas ejecutables
    ├── database/          # schema.sql (DDL sincronizado con Supabase)
    ├── lessons/           # lessons-learned.md (acumulativo por etapa)
    ├── executives/        # Resúmenes ejecutivos (prerrequisito para avanzar)
    └── changes/           # Control de Cambios (CC_XXXXX.md)
```

**Convención de nombres SDD**: `f[Fase]_[Etapa]_[tipo].md` (ej. `f01_02_prd.md`)


## Descripción del Proyecto

Dashboard de inteligencia de negocio para Almacén MultiTodo (7 sedes, ~100 SKUs activos en Colombia). El proyecto transforma datos transaccionales diarios en decisiones estratégicas mediante un pipeline automatizado (validación → ETL → cálculo de métricas), una capa analítica con clasificación ABC/Pareto y alertas determinísticas, y un dashboard accesible que muestra datos del día anterior antes de la apertura del almacén (8 AM COT).

**Fuente de verdad**: [PROJECT_scope.md](./PROJECT_scope.md) — contexto, problema, objetivo, entregables, usuarios, criterios de éxito y alcance. **No repetir detalles en CLAUDE.md; referenciar el scope.**

## Fases y Etapas del Proyecto

**Mandato**: El avance entre fases y etapas requiere orden explícita del usuario. Cada etapa tiene su propio conjunto de documentos SDD (`f[F]_[E]_*.md`).

**Dashboard Transversal**: La construcción de `web/` no es exclusiva de ninguna fase. Se desarrolla en paralelo a medida que cada etapa produce datos o contratos verificables.

### Fase 1 — Gobernanza y Cimientos

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **1.1** | Constitución del proyecto: CLAUDE.md, PROJECT_handoff.md, estructura de carpetas y repositorio | `f01_01_*.md` |
| **1.2** | Validación de infraestructura: verificar tablas Supabase, triggers, índices, permisos y conectividad | `f01_02_*.md` |
| **1.3** | Data Contract: especificación formal del contrato de datos cliente–Triple S, validaciones y protocolo de rechazo | `f01_03_*.md` |

### Fase 2 — Prototipado y Validación de Diseño

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **2.1** | Mockup Interactivo: prototipo visual navegable con datos ficticios para validación temprana de diseño con el cliente | `f02_01_*.md` |

### Fase 3 — Ingeniería de Datos, Integración y Analítica

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **3.1** | Pipeline de validación: verificar que los datos entrantes cumplen el Data Contract antes de la ingestión | `f03_01_*.md` |
| **3.2** | ETL Bronze → Silver: ingestión, limpieza, conversión UTC → COT y persistencia en capas de Supabase | `f03_02_*.md` |
| **3.3** | Capa Gold: cálculos derivados (consumo diario, rotación, clasificación ABC semanal, márgenes) | `f03_03_*.md` |
| **3.4** | EDA: análisis de patrones de venta, estacionalidad por ciudad/categoría y comportamiento por sede | `f03_04_*.md` |
| **3.5** | Motor de alertas: implementación de las 12 reglas (6 negativas + 6 positivas) con umbrales calibrados | `f03_05_*.md` |
| **3.6** | Dashboard MVP: visualización de ventas, inventarios, clasificación ABC y alertas (Next.js + Tailwind) | `f03_06_*.md` |

### Fase 4 — Operación y Mejora Continua

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **4.1** | Publicación en producción: deploy, monitoreo de calidad de datos y disponibilidad del dashboard | `f04_01_*.md` |
| **4.2** | Reportería avanzada: análisis de escenarios, comparativas inter-sede e inter-categoría | `f04_02_*.md` |
| **4.3** | Mejora continua: feedback del cliente, ajuste de umbrales de alertas y nuevas métricas | `f04_03_*.md` |

## Indicador de Progreso del Proyecto

**Cálculo de Avance (siempre dinámico):**

```
E_total = Σ etapas de todas las fases definidas en la sección "Fases y Etapas" de este archivo
C       = número de archivos docs/executives/f*_executive.md existentes

Peso por etapa = 100% / E_total          ← se recalcula si cambia la estructura
Progreso Total = (C / E_total) × 100%
```

- **Fuente de verdad de la estructura**: la tabla "Fases y Etapas" en este mismo archivo.
- **Fuente de verdad de cierre**: existencia de `docs/executives/f[F]_[E]_executive.md`.
- **Nunca hardcodear** el total de etapas ni el peso — siempre contarlos desde la tabla.

**Nota sobre cambios de alcance**: Si se agregan nuevas fases o etapas, `E_total` sube y el progreso puede bajar. El próximo resumen ejecutivo debe incluir nota explicativa:

> ⚠️ **Nota de Alcance**: El avance bajó de X% a Y% porque se incorporaron Z etapas nuevas. El trabajo completado no cambió — el alcance del proyecto se expandió.

## Arquitectura

### Flujo de Datos End-to-End

```
┌─────────────────────────────────────────────────────────────────┐
│ CLIENTE: Almacén MultiTodo                                      │
│ Carga datos diarios → Supabase (usr_ventas, usr_inventario...) │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ PIPELINE DE DATOS (Python 3:30 AM COT)                          │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │ 1. VALIDACIÓN    │→│ 2. ETL           │→│ 3. ALERTAS       │ │
│ │ Cumplen contrato │ │ Limpieza + TZ    │ │ 12 reglas calc.  │ │
│ │ (Data Contract)  │ │ UTC→COT en Silver│ │ Almacenar gold   │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
│ Rechazos → tss_cuarentena_* + notificación al cliente           │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ SUPABASE: Medallion Lakehouse                                   │
│                                                                  │
│ BRONZE (tss_bronze_*)        → Raw data sin modificar          │
│   ↓                                                             │
│ SILVER (tss_silver_*)        → Datos limpios, validados, COT   │
│   ↓                                                             │
│ GOLD (tss_gold_*)            → Métricas, ABC, alertas          │
│ └─ tss_gold_daily_sales      → Ventas diarias por SKU/sede     │
│ └─ tss_gold_abc_ranking      → Clasificación ABC semanal       │
│ └─ tss_gold_alerts           → 12 alertas calculadas           │
│ └─ tss_pipeline_log          → Logs de ejecución               │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ NEXT.JS API ROUTES (Node.js)                                    │
│ - Lectura desde tss_gold_* (RLS + Supabase Auth)               │
│ - Validación con Zod                                           │
│ - Cacheo con TanStack Query (cliente)                          │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ DASHBOARD (Next.js + React + TypeScript)                        │
│ - Vista de ventas, inventarios, ABC, alertas                   │
│ - Filtros por sede y categoría                                 │
│ - Datos de T-1 (día anterior cerrado)                          │
│ - Carga <2s, filtros <500ms                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Capas Analíticas (Medallion Architecture)

| Capa | Tabla | Contenido | Origen | Proceso |
|---|---|---|---|---|
| **Bronze** | `tss_bronze_ventas`, `tss_bronze_inventario` | Datos crudos, sin modificar | `usr_*` del cliente | Copia 1:1 después de validación |
| **Silver** | `tss_silver_ventas`, `tss_silver_inventario` | Datos limpios, normalizados | Bronze | Deduplicación, limpieza, conversión UTC→COT |
| **Gold** | `tss_gold_daily_sales`, `tss_gold_abc_ranking`, `tss_gold_alerts` | Métricas derivadas, indicadores | Silver | Agregaciones, cálculos, clasificación ABC, reglas de alerta |

**Validación en cascada**: Pandera schemas en Silver y Gold aseguran conformidad exacta con Data Contract.

### Componentes Principales

1. **Frontend (Next.js + React)**
   - App Router para navegación optimizada
   - Componentes reutilizables con Shadcn/ui
   - Estado con TanStack Query (caché inteligente)
   - Estilos con Tailwind CSS

2. **API (Next.js API Routes + Node.js)**
   - Rutas `/api/` para lectura de datos Gold
   - Validación Zod en entrada
   - Autenticación Supabase Auth

3. **Pipeline (Python)**
   - Entrada: `main.py --mode [validate|etl|alerts]`
   - Módulos atómicos en `pipeline/src/`
   - Orquestadores en `pipeline/pipelines/`
   - Tests de integración contra Supabase real

4. **Base de Datos (PostgreSQL en Supabase)**
   - RLS (Row Level Security) para acceso controlado
   - Triggers y funciones SQL para reglas críticas
   - Storage para archivos (reportes, auditoría)
   - Backups automáticos

5. **Logging y Monitoreo**
   - `tss_pipeline_log` — Cada ejecución registra éxito/fallo
   - Archivo local `latest` — Estado de última corrida
   - `tss_cuarentena_*` — Datos rechazados con motivo

### Ciclo Diario de Operación

```
00:30 COT (05:30 UTC)  → Cliente completa carga de datos en tablas usr_*
03:30 COT (08:30 UTC)  → Pipeline comienza (validación)
03:45 COT              → ETL: Bronze → Silver → Gold
04:00 COT              → Cálculo de 12 alertas
04:15 COT (09:15 UTC)  → Datos listos en Gold, logs en tss_pipeline_log
                       → ⚠️ Si a las 09:00 UTC el pipeline no completó: alerta interna Triple S
08:00 AM COT           → Dashboard muestra datos T-1 (ayer cerrado)
                       → Gerentes acceden al dashboard
06:00 PM COT           → Almacén cierra
```

**Garantía**: Si el pipeline falla, `tss_cuarentena_*` captura errores y el cliente es notificado. Dashboard no se actualiza hasta que validación pase 100%.

## Comandos de Desarrollo

### Configuración
```bash
# Instalar dependencias
npm install                      # Frontend (web/)
pip install -r requirements.txt  # Pipeline (pipeline/)

# Variables de entorno
cp .env.example .env.local       # Frontend
cp .env.example .env             # Pipeline (secrets NO trackeados en git)

# Base de datos
# Sincronizar schema: leer docs/database/schema.sql en Supabase console
```

### Ejecutar
```bash
# Frontend (Next.js) — puerto 3000
npm run dev

# Backend Python (FastAPI) — puerto 8000
python pipeline/main.py --mode validate

# Pipeline completo (validación → ETL → alertas)
python pipeline/main.py --mode etl
python pipeline/main.py --mode alerts
```

### Pruebas
```bash
# Frontend (Jest)
npm test                         # Ejecutar una vez
npm run test:watch              # Modo watch (reejecutar en cambios)

# Pipeline (TDD obligatorio — tests primero)
pytest pipeline/tests/           # Todos los tests
pytest pipeline/tests/ -v        # Verbose
pytest pipeline/tests/ --cov     # Con coverage

# Integración (contra Supabase real — sin mocks de BD)
pytest pipeline/tests/ -m integration
```

### Linting y Formateo
```bash
# Frontend
npm run lint                     # ESLint
npm run format                   # Prettier (auto-fix)

# Pipeline
black pipeline/                  # Formateo Python
ruff check pipeline/             # Linting Python
ruff check pipeline/ --fix       # Auto-fix violaciones
```

### Database
```bash
# Ver schema actual (referencia)
cat docs/database/schema.sql

# Logs y cuarentena en Supabase:
# - tss_pipeline_log — Registros de ejecución
# - tss_cuarentena_* — Datos rechazados por validación
```

## Stack Tecnológico

### Capa de Presentación (Frontend)
- **Framework**: Next.js (React) con App Router para optimizar navegación y SEO.
- **Lenguaje**: TypeScript. Interfaces globales para sincronización exacta de datos.
- **Gestión de Estado**: TanStack Query (React Query). Caché en cliente, manejo elegante de estados.
- **Estilos**: Tailwind CSS + Shadcn/ui. Interfaces consistentes, accesibles y modernas.

### Capa de Lógica y Procesamiento (Backend)
- **API**: Node.js (Next.js API Routes). Lógica de negocio inmediata, validaciones, envíos, integraciones.
- **Microservicios**: Python (FastAPI). Ciencia de Datos, Machine Learning, cálculos pesados.
- **Validación de Datos**: Zod. Garantiza que datos cumplan esquema antes de llegar a BD.

### Capa de Datos y Seguridad (Persistence)
- **DBMS**: PostgreSQL (en Supabase). Consultas complejas, JOINs, integridad referencial.
- **Seguridad**: Row Level Security (RLS). Control de acceso a nivel de fila en la BD.
- **Lógica en BD**: SQL/RPC (Stored Procedures). Reglas críticas e inalterables.
- **Storage**: Almacenamiento de archivos (PDFs, imágenes, reportes) con políticas integradas.

### Ecosistema de Soporte (DevOps)
- **Autenticación**: Supabase Auth (Magic Links, Google, usuario/contraseña).
- **Hosting**: Vercel (Edge Network) para frontend y APIs global.
- **Monitoreo**: Sentry (opcional) para errores en tiempo real.
- **CI/CD**: GitHub Actions para pruebas y despliegues automatizados.

## Archivos y Directorios Clave

**Puntos de entrada críticos**:
- `PROJECT_handoff.md` — Único archivo de estado del proyecto: fase/etapa activa, hitos, arquitectura, decisiones históricas, bloqueadores y próxima acción.
- `PROJECT_scope.md` — Alcance, objetivo, entregables y criterios de éxito.
- `docs/database/schema.sql` — DDL sincronizado con Supabase (obligatorio leer antes de implementar).
- `docs/changes/` — Control de cambios formalizados (CC_XXXXX.md) en estado `✅ Aprobado`.

## Notas Importantes

### Contexto del Cliente y Restricciones
- **Cliente**: Almacén MultiTodo (cadena minorista con 7 sedes en Colombia).
- **Operación**: 8:00 AM – 6:00 PM COT todos los días. Pipeline ejecuta 3:30 AM COT.
- **Restricción inamovible**: Dashboard solo muestra datos de jornadas cerradas (T-1 hacia atrás). Nunca datos del día en curso (T+0).
- **Deadline**: 3 meses para go-live. Presupuesto: USD $10,000.

### Principio Rector
**Regla de Oro** (línea 29): Si durante implementación hay algo no contemplado en documentos SDD → **DETENER** y solicitar actualización antes de continuar. Prohibido improvisar.

### Gobernanza de Datos
- Tablas cliente (`usr_*`) — Solo lectura, sin alteraciones. Fuente de verdad del cliente.
- Tablas Triple S (`tss_*`) — Propiedad exclusiva. Bronze (raw), Silver (limpio), Gold (métricas).
- Data Contract (`docs/specs/f01_03_spec.md`) — Documento vinculante. Si cliente incumple, pipeline rechaza y notifica.
- **Responsabilidades de datos**: El cliente es el único responsable de la calidad, puntualidad e integridad de los datos en tablas `usr_*`. Triple S garantiza la correcta ingestión, transformación y visualización de los datos entregados conforme al Data Contract. Los problemas originados en datos incorrectos del cliente se documentan en `tss_error_log` y se notifican formalmente.

### Validación y Manejo de Errores
- Obligatorio esquemas Pandera (Silver y Gold) que reflejen exactamente Data Contracts.
- Códigos de error `ERR_MTD_XXX` mapean a violaciones específicas (ver líneas 68–73).
- Triple persistencia: archivo local + log con timestamp + tabla `tss_pipeline_log`.

## Recursos Externos

### Stack Documentación
- [Supabase Docs](https://supabase.com/docs) — PostgreSQL, Auth, RLS, Storage.
- [Next.js Docs](https://nextjs.org/docs) — App Router, API Routes, deployment.
- [FastAPI Docs](https://fastapi.tiangolo.com/) — Python microservicios.
- [Pandera Docs](https://pandera.readthedocs.io/) — Validación de esquemas de datos.

### Herramientas del Proyecto
- GitHub — Control de versión y CI/CD (GitHub Actions).
- Vercel — Hosting frontend (Next.js deployment).
- Supabase — Base de datos PostgreSQL + Auth + Storage.

**Nota**: Agregar referencias específicas del cliente (Jira, Confluence, Slack, reuniones grabadas) cuando esté disponible.

## Variables de Entorno Requeridas

### Pipeline (`pipeline/.env`)
```env
# Supabase
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_SERVICE_KEY=<service_role_key>   # Solo pipeline (permisos totales)

# Notificaciones
NOTIFICATION_EMAIL=<email_tripleS>        # Receptor de alertas de fallo

# Configuración operativa
PIPELINE_TIMEZONE=America/Bogota
PIPELINE_SCHEDULE=03:30                   # Hora de ejecución COT
```

### Frontend (`web/.env.local`)
```env
# Supabase (solo anon key — acceso público restringido por RLS)
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
```

**Regla**: Nunca commitear `.env` ni `.env.local`. Usar `.env.example` como plantilla trackeada en git.

---

## Versiones Mínimas de Runtime

| Tecnología | Versión mínima | Notas |
|---|---|---|
| Python | 3.11+ | f-strings, tomllib nativo, type hints modernos |
| Node.js | 18 LTS+ | Fetch nativo, App Router estable en Next.js 14 |
| npm | 9+ | Workspace support |
| Next.js | 14+ | App Router obligatorio |
| PostgreSQL | 15+ | En Supabase (gestionado por plataforma) |

**Verificación rápida**:
```bash
python --version   # >= 3.11
node --version     # >= 18
npm --version      # >= 9
```

---

## Protocolo de Fallo en Producción

### Niveles de Severidad

| Nivel | Descripción | Tiempo de respuesta |
|---|---|---|
| **P1 — Crítico** | Pipeline falló, dashboard sin datos frescos antes de 8 AM | Inmediato |
| **P2 — Alto** | Pipeline corrió pero datos en cuarentena > 5% del volumen | < 2 horas |
| **P3 — Medio** | Pipeline corrió, alertas no se calcularon | < 4 horas |
| **P4 — Bajo** | Anomalía en logs, sin impacto visible | Próximo día hábil |

### Pasos ante Fallo P1

1. **Detectar** — Revisar `tss_pipeline_log` (columna `status = 'ERROR'`) y archivo local `latest`.
2. **Diagnosticar** — Leer log con timestamp para identificar módulo y error exacto.
3. **Notificar** — Informar al cliente: dashboard mostrará datos de T-2 hasta resolución.
4. **Corregir** — Si es dato del cliente: notificar con código `ERR_MTD_XXX`. Si es bug interno: hotfix en rama `fix/*`.
5. **Reejecutar** — `python pipeline/main.py --mode etl` manualmente una vez corregido.
6. **Cerrar** — Actualizar `tss_pipeline_log` con resolución y registrar en `docs/lessons/lessons-learned.md`.

**Regla**: Nunca silenciar errores con `pass`. Nunca reejecutar sin diagnóstico previo.

---

## Política de Migraciones de Base de Datos

### Reglas

1. **`docs/database/schema.sql` es la fuente de verdad** — Siempre refleja el estado actual de Supabase.
2. **Toda modificación al schema requiere CC aprobado** (Control de Cambios) antes de ejecutar en Supabase.
3. **Tablas `usr_*` son intocables** — Solo Triple S puede alterar `tss_*`.
4. **Sin migraciones automáticas** — Aplicar DDL manualmente en Supabase console y luego actualizar `schema.sql`.

### Flujo de Migración

```
1. Crear CC_XXXXX.md describiendo el cambio de schema
2. Usuario aprueba CC
3. Ejecutar DDL en Supabase console (entorno dev primero)
4. Verificar con pytest pipeline/tests/ -m integration
5. Actualizar docs/database/schema.sql con el DDL final
6. Commit: docs: actualizar schema.sql con migración CC_XXXXX
7. Ejecutar en producción
```

**Nunca** modificar Supabase directamente sin actualizar `schema.sql` en el mismo commit.

---

## Entornos

| Variable | Desarrollo | Producción |
|---|---|---|
| Supabase | Proyecto separado (`dev`) | Proyecto producción (`prod`) |
| Pipeline schedule | Manual o cron local | GitHub Actions (3:30 AM COT) |
| Frontend URL | `localhost:3000` | Vercel (dominio del cliente) |
| Logs | Archivo local + Supabase dev | Supabase prod + notificaciones activas |
| Tests | Contra Supabase dev | CI en GitHub Actions (antes de deploy) |

**Regla**: Jamás ejecutar el pipeline con `SUPABASE_SERVICE_KEY` de producción en máquina local salvo emergencia P1 explícitamente aprobada.

---

## Glosario de Términos

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
| **ERR_MTD_XXX** | Códigos de error del pipeline. Ver sección "Validación y Errores" para la lista completa. |
| **SDD** | Software Design Document. Jerarquía: PRD → SPEC → Plan → Tasks. |
| **CC** | Control de Cambios (`CC_XXXXX.md`). Requerido antes de modificar cualquier etapa activa o cerrada. |
| **Triple S** | Sabbia Solutions & Services. Proveedor del proyecto. Propietario de tablas `tss_*`. |
| **Triple Persistencia** | Patrón obligatorio: registrar éxito/fallo en (1) archivo local `latest`, (2) log con timestamp, (3) `tss_pipeline_log`. |

---

## Decisiones Arquitectónicas (ADR)

### ADR-001 — SQL-First para transformaciones pesadas
**Decisión**: Las transformaciones de datos se implementan en SQL (Supabase stored procedures), no en Python.
**Razón**: PostgreSQL ejecuta transformaciones 10-100x más rápido que pandas en el mismo dataset. Reduce latencia del pipeline y costo de cómputo.
**Consecuencia**: Python orquesta y valida; SQL transforma y agrega.

### ADR-002 — Medallion Architecture (Bronze/Silver/Gold)
**Decisión**: Tres capas de datos con propósitos distintos en lugar de transformación directa.
**Razón**: Trazabilidad completa. Si Gold tiene un error, se puede reprocessar desde Silver sin tocar los datos crudos del cliente.
**Consecuencia**: Mayor uso de storage en Supabase, pero auditoría perfecta de cada transformación.

### ADR-003 — Sin RBAC (todos los gerentes ven lo mismo)
**Decisión**: El dashboard no tiene restricciones de acceso por rol.
**Razón**: Decisión explícita del cliente (ver PROJECT_scope.md §5). Simplifica arquitectura y mantenimiento.
**Consecuencia**: Si en el futuro se requiere RBAC, es un CC que afecta múltiples capas.

### ADR-004 — Alertas determinísticas (sin ML)
**Decisión**: Las 12 alertas son reglas basadas en umbrales fijos, no modelos predictivos.
**Razón**: Fuera de alcance del proyecto (ver PROJECT_scope.md §7). Reduce complejidad y tiempo de go-live.
**Consecuencia**: Umbrales deben calibrarse manualmente en Fase 3.5 con datos reales.

### ADR-005 — T-1 obligatorio (sin datos del día en curso)
**Decisión**: El dashboard nunca muestra datos de la jornada en curso.
**Razón**: Jornada incompleta genera métricas engañosas (e.g., ventas a las 9 AM vs. cierre de día).
**Consecuencia**: Los gerentes siempre trabajan con información de ayer, no de hoy.

---

## Resolución de Conflictos SDD

Cuando hay contradicción entre documentos, la jerarquía de precedencia es:

```
PROJECT_scope.md          ← Decisión de negocio (más alta)
    ↓
docs/reqs/f[F]_[E]_prd.md ← Qué construir
    ↓
docs/specs/f[F]_[E]_spec.md ← Cómo construirlo
    ↓
docs/plans/f[F]_[E]_plan.md ← Orden de ejecución
    ↓
docs/tasks/f[F]_[E]_task.md ← Tareas atómicas (más baja)
```

### Reglas de Resolución

1. **El documento de mayor jerarquía prevalece siempre.**
2. **Si hay contradicción entre un spec y el código**: el spec gana. El código se corrige.
3. **Si un spec está desactualizado vs. la realidad construida**: DETENER. Abrir CC para actualizar el spec antes de continuar.
4. **Si el scope contradice un spec**: Escalar al usuario. No resolver autónomamente.
5. **Ambigüedad no es contradicción**: Si algo no está especificado, es un gap → DETENER y solicitar actualización del documento correspondiente (Regla de Oro).
