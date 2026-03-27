# CLAUDE.md

Este archivo define las leyes, límites y terreno de juego para cualquier Agente de IA que interactúe con este repositorio. Es de lectura obligatoria y cumplimiento dogmático.

Desarrollado por **Sabbia Solutions & Services (Triple S)**

## Reglas de Comportamiento

1. **Tono**: Educado y profesional. Respuestas cortas y concisas.
2. **Revisión de Código**: Al completar un cambio, lanza agentes de revisión para asegurar calidad.
3. **Uso de Agentes**: Prioriza construcción, revisión y pruebas a través de subagentes en paralelo.

## Límites de Autonomía

- **Prohibido avanzar** a una nueva fase/etapa sin orden explícita del usuario ("Procede", "Siguiente", "Avanza").
- **Prohibido escribir archivos** sin petición o confirmación explícita.
- La proactividad se limita a análisis y sugerencias en el chat.
- **Prohibido proponer o ejecutar trabajo de una nueva etapa** si el documento `docs/executives/f[F]_[E]_executive.md` de la etapa anterior no existe.

## Desarrollo Spec-Driven

El código es un reflejo **sumiso** de la documentación. Jerarquía documental:
1. **`docs/reqs/f[F]_[E]_prd.md`** — Qué construir.
2. **`docs/specs/f[F]_[E]_spec.md`** — Cómo construirlo.
3. **`docs/plans/f[F]_[E]_plan.md`** — Orden y estrategia.
4. **`docs/tasks/f[F]_[E]_task.md`** — Tareas ejecutables.

**Regla de oro**: Si durante la implementación hay algo no contemplado → **DETENER** y solicitar actualización del documento antes de continuar. Ante discrepancia, PRD → SPEC → Plan → Tareas define quién manda.

## Control de Cambios

Ejecutar `/change-control` en dos casos:
1. **Cambio en etapa activa**: Algo necesario no está en los documentos SDD.
2. **Cambio en etapa cerrada**: Cualquier modificación a código o documentos ya completados.

Flujo: Informar → usuario aprueba → `docs/changes/CC_XXXXX.md` en `Pendiente` → usuario confirma → `Aprobado` → ejecutar → cerrar. Si rechaza: `No Aprobado`, no se toca nada.

## Protocolo de Inicio de Sesión

En orden obligatorio:
1. Leer `CLAUDE.md`
2. Leer `PROJECT_handoff.md` — Estado macro y táctico.
3. Leer `docs/lessons/lessons-learned.md` — Solo sección de etapa activa.
4. Leer `docs/changes/` — Solo CCs en estado `✅ Aprobado`.
5. Leer `docs/database/schema.sql` — Esquema actual de Supabase.

Solo después está autorizado a escribir código o ejecutar acciones.

## Protocolo de Cierre de Sesión

Reescribir `PROJECT_handoff.md` con: archivos modificados, contexto inmediato, último error/bloqueador y próxima acción concreta.

## Estándares y Convenciones de Código

### Arquitectura de Datos (Medallion)
- **Bronze** (`tss_bronze_*`): Raw data sin modificar desde tablas cliente (`usr_*`).
- **Silver** (`tss_silver_*`): Datos limpios, validados, timezone convertido a COT.
- **Gold** (`tss_gold_*`): Métricas derivadas, clasificación ABC, indicadores de alertas.

### Validación y Errores
- **Validación obligatoria**: Esquemas Pandera para Silver y Gold. Deben reflejar exactamente los Data Contracts.
- **Gestión de errores**: Prohibido `pass`. Mapear a códigos `ERR_MTD_XXX`:
  - `ERR_MTD_001` — Transacción fuera de ventana (8 AM–6 PM COT)
  - `ERR_MTD_002` — SKU no registrado
  - `ERR_MTD_003` — Sede no registrada
  - `ERR_MTD_004` — Registro con fecha T+0 (carga anticipada)
  - `ERR_MTD_005` — Violación de constraint numérico

- **Validaciones obligatorias del pipeline** (antes de Bronze, en este orden):
  1. `fecha_hora` en `usr_ventas` dentro de ventana operativa: `13:00–23:00 UTC`.
  2. No se aceptan registros con `fecha_hora` del día en curso (T+0).
  3. Todos los `sku` deben existir en `usr_productos`.
  4. Todos los `id_sede` deben existir en `usr_sedes`.
  5. `stock_fisico >= 0`, `cantidad > 0`, `precio > 0`, `costo > 0` (si no es null).

- **Protocolo ante violación del Data Contract** (orden obligatorio):
  1. Registrar error en `tss_error_log`.
  2. Enviar registros inválidos a `tss_cuarentena_*`.
  3. Generar alerta interna Triple S.
  4. Notificar al cliente con detalle y registros afectados.
  5. Los datos no pasan a Bronze hasta que el cliente corrija y reentregue.

### Seguridad y Configuración
- **Cero hardcoding**: Secretos en `.env`, configuración en `config.yaml`. Prohibido hardcodear IDs, URLs, nombres de columnas, umbrales, magic numbers.
- **Timezone**: UTC → COT con `pytz` usando `America/Bogota`. Prohibido offsets manuales.

### Fuente de Datos del Dashboard
- **Prohibido archivos locales**: El dashboard solo lee desde `tss_gold_*` vía API Routes de Next.js.

### Ambiente Virtual Python
- **Ambiente virtual obligatorio**: `pipeline/.venv`. Nunca instalar en Python global.
- **`requirements.txt` es la fuente de verdad**: Agregar dependencia antes de usarla en código.
- **`.venv` no se trackea en Git**.

### Arquitectura de Código
- **Separación de responsabilidades**: Lógica de negocio solo en `src/`.
- **Triple persistencia**: (1) archivo local `latest`, (2) log con timestamp, (3) `tss_pipeline_log`.
- **DVC obligatorio**: Datasets y artefactos con DVC, nunca en Git.
- **SQL-First**: Transformaciones pesadas en SQL, no en Python.

### Testing
- **TDD obligatorio**: Test primero → código mínimo → refactorizar. Sin excepción.
  - Tests en `pipeline/tests/` espejando `pipeline/src/`.
  - Conectores: integration tests contra Supabase real (sin mocks de BD).
  - `main.py` y orquestadores: tests de integración end-to-end.

### Prefijos de Tablas
- **`usr_*`**: Propiedad del cliente (solo lectura). No alterar sin CC aprobado.
- **`tss_*`**: Propiedad de Triple S (Bronze, Silver, Gold, logs, alertas, cuarentena).

## Flujo de Trabajo (Git y CI/CD)

### Estrategia de Ramas
- **`main`** — Producción. Requiere CI Quality Gate + aprobación manual.
- **`feat/*`** — Desarrollo. Merge a `main` solo después que CI pase.

### Commits
Formato atómico en español: `feat:` | `fix:` | `docs:` | `refactor:`

**Ejemplo**: `feat: ETL Bronze to Silver con conversión UTC-COT`

### CI/CD
- Quality Gate en PRs hacia `main`: pytest + npm test + linting (en paralelo).
- Release tags semánticos al mergear: `v1.0.0`.

**Comandos**: `python pipeline/main.py --mode [validate|etl|alerts]` | `npm run dev` | `pytest pipeline/tests/` | `npm test`

## Convenciones de Idioma
- **Código/Archivos/Carpetas**: Inglés (snake_case archivos, CamelCase clases).
- **Documentación/Comentarios/Commits**: Español.
- **Interfaz/Output al Usuario**: Español.

## Archivos Clave del Proyecto

- **`PROJECT_handoff.md`** — Estado macro y táctico del proyecto. Se reescribe al cerrar sesión.
- **`PROJECT_scope.md`** — Alcance, objetivo, entregables y criterios de éxito.
- **`docs/database/schema.sql`** — DDL sincronizado con Supabase. Leer antes de implementar.
- **`docs/changes/`** — CCs formalizados en estado `✅ Aprobado`.

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
    ├── reqs/              # PRD
    ├── specs/             # Especificaciones técnicas
    ├── plans/             # Planes de implementación
    ├── tasks/             # Tareas atómicas ejecutables
    ├── database/          # schema.sql (DDL sincronizado con Supabase)
    ├── lessons/           # lessons-learned.md
    ├── executives/        # Resúmenes ejecutivos (prerrequisito para avanzar)
    ├── changes/           # Control de Cambios (CC_XXXXX.md)
    └── references/        # Documentación de referencia (arquitectura, ADR, glosario, etc.)
```

**Convención SDD**: `f[Fase]_[Etapa]_[tipo].md` (ej. `f01_02_prd.md`)

## Descripción del Proyecto

Dashboard de inteligencia de negocio para Almacén MultiTodo (7 sedes, ~100 SKUs activos en Colombia). Pipeline automatizado (validación → ETL → métricas), capa analítica con clasificación ABC/Pareto y alertas determinísticas, dashboard con datos del día anterior antes de la apertura (8 AM COT).

**Fuente de verdad**: [PROJECT_scope.md](./PROJECT_scope.md)

## Fases y Etapas del Proyecto

**Mandato**: El avance requiere orden explícita del usuario. Cada etapa tiene su propio conjunto SDD (`f[F]_[E]_*.md`).

**Dashboard Transversal**: `web/` se desarrolla en paralelo a medida que cada etapa produce datos verificables.

### Fase 1 — Gobernanza y Cimientos

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **1.1** | Constitución del proyecto: CLAUDE.md, PROJECT_handoff.md, estructura y repositorio | `f01_01_*.md` |
| **1.2** | Validación de infraestructura: tablas Supabase, triggers, índices, permisos y conectividad | `f01_02_*.md` |
| **1.3** | Data Contract: especificación formal, validaciones y protocolo de rechazo | `f01_03_*.md` |

### Fase 2 — Prototipado y Validación de Diseño

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **2.1** | Mockup Interactivo: prototipo navegable con datos ficticios para validación con el cliente | `f02_01_*.md` |

### Fase 3 — Ingeniería de Datos, Integración y Analítica

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **3.1** | Pipeline de validación: verificar que datos entrantes cumplen el Data Contract | `f03_01_*.md` |
| **3.2** | ETL Bronze → Silver: ingestión, limpieza, conversión UTC → COT | `f03_02_*.md` |
| **3.3** | Capa Gold: consumo diario, rotación, clasificación ABC semanal, márgenes | `f03_03_*.md` |
| **3.4** | EDA: patrones de venta, estacionalidad por ciudad/categoría y sede | `f03_04_*.md` |
| **3.5** | Motor de alertas: 12 reglas (6 negativas + 6 positivas) con umbrales calibrados | `f03_05_*.md` |
| **3.6** | Dashboard MVP: ventas, inventarios, ABC, alertas (Next.js + Tailwind) | `f03_06_*.md` |

### Fase 4 — Operación y Mejora Continua

| Etapa | Descripción | Docs SDD |
|---|---|---|
| **4.1** | Publicación en producción: deploy, monitoreo y disponibilidad | `f04_01_*.md` |
| **4.2** | Reportería avanzada: comparativas inter-sede e inter-categoría | `f04_02_*.md` |
| **4.3** | Mejora continua: feedback del cliente, ajuste de umbrales y nuevas métricas | `f04_03_*.md` |

## Indicador de Progreso del Proyecto

```
E_total = Σ etapas de todas las fases (contar desde la tabla anterior)
C       = número de archivos docs/executives/f*_executive.md existentes
Progreso Total = (C / E_total) × 100%
```

- **Nunca hardcodear** E_total — siempre contar desde la tabla.
- **Fuente de verdad de cierre**: existencia de `docs/executives/f[F]_[E]_executive.md`.

## Gobernanza de Datos

- Tablas `usr_*` — Solo lectura. Fuente de verdad del cliente. No alterar.
- Tablas `tss_*` — Propiedad de Triple S. Bronze (raw), Silver (limpio), Gold (métricas).
- Data Contract (`docs/specs/f01_03_spec.md`) — Si cliente incumple, pipeline rechaza y notifica.
- **Cliente** responsable de calidad, puntualidad e integridad de `usr_*`. Triple S garantiza la ingestión y transformación correcta.

## Política de Migraciones de Base de Datos

1. `docs/database/schema.sql` es la fuente de verdad — siempre refleja el estado actual.
2. Toda modificación al schema requiere CC aprobado antes de ejecutar.
3. Tablas `usr_*` intocables. Solo Triple S altera `tss_*`.
4. Sin migraciones automáticas — aplicar DDL en Supabase console y actualizar `schema.sql`.

Flujo: CC aprobado → DDL en dev → `pytest -m integration` → actualizar `schema.sql` → commit → ejecutar en producción.

## Resolución de Conflictos SDD

```
PROJECT_scope.md  >  PRD  >  SPEC  >  Plan  >  Tasks
```

El documento de mayor jerarquía prevalece. Contradicción spec vs. código: el spec gana. Ambigüedad = gap → DETENER y solicitar actualización. Conflicto scope vs. spec → escalar al usuario.

## Notas del Proyecto

- **Cliente**: Almacén MultiTodo, 7 sedes en Colombia. Operación 8 AM–6 PM COT.
- **Restricción inamovible**: Dashboard solo muestra datos T-1. Nunca T+0.
- **Deadline**: 3 meses para go-live. Presupuesto: USD $10,000.

## Referencias

- [Arquitectura del sistema](docs/references/architecture.md) — Flujo de datos, Medallion, ciclo diario.
- [Comandos de desarrollo](docs/references/dev-commands.md) — Setup, ejecución, pruebas, linting.
- [Stack tecnológico](docs/references/tech-stack.md) — Stack, versiones, variables de entorno, entornos.
- [Protocolo de fallos P1–P4](docs/references/incident-protocol.md) — Severidades y pasos de respuesta.
- [Glosario](docs/references/glossary.md) — T-1, COT, Bronze/Silver/Gold, ERR_MTD_XXX, etc.
- [Decisiones Arquitectónicas (ADR)](docs/references/adr.md) — ADR-001 a ADR-005.
