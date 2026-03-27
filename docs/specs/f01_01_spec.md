# SPEC — Constitución del Proyecto (`f01_01`)

> Documento: `docs/specs/f01_01_spec.md`
> Versión: 1.0
> Fecha: 2026-03-27
> Estado: ✅ Aprobado
> Elaborado por: Triple S (Sabbia Solutions & Services)
> Trazabilidad: Este documento implementa los requerimientos de `docs/reqs/f01_01_prd.md`.

---

## 1. Visión de Arquitectura

Esta etapa es de tipo **DOCUMENTACIÓN**. No existe pipeline de datos ni componentes de código de producto. La "arquitectura" es la estructura del repositorio y el grafo de dependencia entre artefactos de gobernanza.

Cada artefacto tiene un propósito funcional exacto y un lector primario definido. Los artefactos se crean en orden de dependencia: el repositorio primero (contenedor), luego las leyes del sistema (`CLAUDE.md`), luego el scope (`PROJECT_scope.md`), luego el estado operativo (`PROJECT_handoff.md`), y finalmente los artefactos de soporte.

### 1.1 Diagrama de Dependencias entre Artefactos

```
INICIO
  ↓
[ARC-01] Repositorio Git + .gitignore + Estructura de carpetas
  ↓
[ARC-02] CLAUDE.md — leyes del sistema (lector: agentes IA + equipo)
  ↓
[ARC-03] PROJECT_scope.md — alcance aprobado (lector: stakeholders + equipo)
  ↓
[ARC-04] PROJECT_handoff.md — estado táctico (lector: agente IA al iniciar sesión)
  ├── [ARC-05] docs/lessons/lessons-learned.md
  ├── [ARC-06] .claude/skill-router.md
  └── [ARC-07] docs/references/ (6 documentos)
  ↓
[ARC-08] Commit inicial en main
  ↓
FIN
```

### 1.2 Componentes de Arquitectura

| ID | Componente | Responsabilidad | Ruta |
|---|---|---|---|
| `[ARC-01]` | Repositorio Git + estructura | Contenedor versionado de todos los artefactos; `.gitignore` define qué no se trackea | Raíz del repositorio |
| `[ARC-02]` | `CLAUDE.md` | Ley suprema de comportamiento de agentes IA; define reglas, límites, estándares, convenciones y protocolos | `CLAUDE.md` (raíz) |
| `[ARC-03]` | `PROJECT_scope.md` | Captura aprobada del alcance, objetivos, entregables y criterios de éxito del proyecto completo | `PROJECT_scope.md` (raíz) |
| `[ARC-04]` | `PROJECT_handoff.md` | Estado táctico inmediato; permite retomar el proyecto sin re-exploración | `PROJECT_handoff.md` (raíz) |
| `[ARC-05]` | `lessons-learned.md` | Registro acumulativo de aprendizajes por etapa; alimenta mejora continua | `docs/lessons/lessons-learned.md` |
| `[ARC-06]` | `skill-router.md` | Mapa de agentes y skills; lector primario de cada skill durante protocolo de inicio | `.claude/skill-router.md` |
| `[ARC-07]` | Referencias técnicas | 6 documentos de referencia base que soportan decisiones técnicas de etapas posteriores | `docs/references/` |
| `[ARC-08]` | Commit inicial | Snapshot inmutable del estado de gobernanza en `main`; punto de restauración y evidencia de completitud | Git history (`main`) |

---

## 2. Especificación de Artefactos

Esta sección define el contenido exacto, estructura interna y convenciones de formato de cada artefacto que debe producirse en la Etapa 1.1. Es la traducción técnica de cada `[REQ]` del PRD.

### 2.1 `[ARC-01]` — Repositorio Git + `.gitignore` + Estructura de Carpetas

**Implementa**: `[REQ-01]`, `[REQ-05]`, `[REQ-08]`

#### Inicialización del repositorio

- Ejecutar `git init` en el directorio raíz del proyecto.
- Rama inicial: `main` (configurar como rama por defecto).
- No se crea rama `feat/*` en esta etapa — solo `main` para el commit de constitución.
- El primer commit en `main` es el commit de gobernanza completo (`[ARC-08]`).

#### Especificación del `.gitignore`

El archivo `.gitignore` debe residir en la raíz del repositorio y contener exactamente los siguientes bloques, en este orden, con comentarios de sección:

```
# Python
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/

# Variables de entorno y secretos
.env
.env.local
.env.*.local

# Next.js
.next/
out/
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# DVC
/tmp/
*.dvc/cache/
.dvc/tmp/

# Sistemas operativos
.DS_Store
Thumbs.db
desktop.ini

# IDEs
.vscode/settings.json
.idea/
*.swp
*.swo

# Logs y artefactos locales
logs/
*.log
pipeline/output/
```

#### Especificación de la estructura de carpetas

Crear todas las carpetas con un archivo `.gitkeep` vacío para que sean trackeadas por Git. Las carpetas requeridas son:

```
pipeline/
pipeline/main.py          ← archivo placeholder vacío (no código de producto)
pipeline/pipelines/
pipeline/src/
pipeline/tests/
web/
web/components/
web/app/
web/tests/
docs/
docs/reqs/
docs/specs/
docs/plans/
docs/tasks/
docs/database/
docs/lessons/
docs/executives/
docs/changes/
docs/references/
.claude/
```

Regla de nomenclatura de carpetas: snake_case en inglés, sin espacios, sin mayúsculas.

El archivo `pipeline/main.py` es un placeholder que contendrá solo un comentario de encabezado indicando su propósito futuro. No contiene lógica en esta etapa.

---

### 2.2 `[ARC-02]` — `CLAUDE.md`

**Implementa**: `[REQ-02]`

#### Secciones obligatorias (en este orden)

El documento debe contener las siguientes secciones de nivel `##`. La ausencia de cualquiera de ellas invalida el artefacto:

| N | Sección | Contenido mínimo obligatorio |
|---|---|---|
| 1 | `## Reglas de Comportamiento` | Tono, revisión de código, uso de agentes |
| 2 | `## Límites de Autonomía` | Prohibición de avanzar sin orden, prohibición de escribir sin confirmación, límite de la proactividad, gate del executive |
| 3 | `## Desarrollo Spec-Driven` | Jerarquía documental PRD → SPEC → Plan → Tareas; regla de oro ante gaps |
| 4 | `## Control de Cambios` | Dos casos de uso del CC; flujo completo Pendiente → Aprobado → Ejecutado |
| 5 | `## Protocolo de Inicio de Sesión` | 6 pasos en orden numerado; skill-router primero |
| 6 | `## Protocolo de Cierre de Sesión` | Reescritura de `PROJECT_handoff.md` |
| 7 | `## Estándares y Convenciones de Código` | Subsecciones: Medallion, Validación, Seguridad, Dashboard, Venv, Arquitectura, Web, Testing, Prefijos |
| 8 | `## Flujo de Trabajo (Git y CI/CD)` | Estrategia de ramas, formato de commits, Quality Gate |
| 9 | `## Convenciones de Idioma` | Tabla idioma por contexto |
| 10 | `## Archivos Clave del Proyecto` | Lista de archivos críticos con descripción |
| 11 | `## Estructura de Carpetas` | Árbol ASCII con comentarios |
| 12 | `## Descripción del Proyecto` | Resumen de negocio en 2-3 líneas |
| 13 | `## Fases y Etapas del Proyecto` | Tabla completa de fases y etapas con IDs SDD |
| 14 | `## Indicador de Progreso del Proyecto` | Fórmula `E_total / C` |
| 15 | `## Gobernanza de Datos` | Prefijos `usr_*` vs `tss_*`; Data Contract |
| 16 | `## Política de Migraciones de Base de Datos` | Flujo DDL; `schema.sql` como fuente de verdad |
| 17 | `## Resolución de Conflictos SDD` | Jerarquía de prevalencia |
| 18 | `## Notas del Proyecto` | Cliente, restricción T-1, deadline, presupuesto |
| 19 | `## Referencias` | Links a los 6 documentos de `docs/references/` |

#### Cabecera obligatoria del documento

```markdown
# CLAUDE.md

Este archivo define las leyes, límites y terreno de juego para cualquier Agente de IA
que interactúe con este repositorio. Es de lectura obligatoria y cumplimiento dogmático.

Desarrollado por **Sabbia Solutions & Services (Triple S)**
```

#### Convenciones de formato

- Encabezados de sección: `##` (nivel 2). Subsecciones con `###`.
- Listas de reglas: bullets `- ` con negrita en el término (`**Término**:`).
- Prohibiciones explícitas con `**Prohibido**`.
- Tablas para: fases/etapas, comandos, convenciones de idioma.
- Bloques de código para: árbol de carpetas, fórmulas, ejemplos de commits.

---

### 2.3 `[ARC-03]` — `PROJECT_scope.md`

**Implementa**: `[REQ-03]`

#### Secciones obligatorias (en este orden)

| N | Sección | Contenido mínimo obligatorio |
|---|---|---|
| 1 | Cabecera de metadatos | Versión, fecha, estado (`✅ Aprobado`), elaborado por, aprobado por |
| 2 | `## 1. Contexto del Proyecto` | Cliente, industria, problema de negocio que origina el proyecto |
| 3 | `## 2. Objetivo Central` | Una oración que define el propósito del sistema completo |
| 4 | `## 3. Entregables` | Lista numerada de entregables concretos con descripción breve |
| 5 | `## 4. Usuarios del Sistema` | Tabla: rol, descripción, necesidades principales |
| 6 | `## 5. Criterios de Éxito` | Lista numerada de criterios medibles; cada uno con valor objetivo |
| 7 | `## 6. Alcance` | Subsecciones: En Alcance, Fuera de Alcance |
| 8 | `## 7. Restricciones` | Lista de restricciones inamovibles (técnicas, de negocio, de tiempo) |
| 9 | `## 8. Supuestos` | Lista de supuestos sobre los que se diseña el sistema |
| 10 | `## 9. Fases del Proyecto` | Resumen macro de las 4 fases con descripción en una línea |
| 11 | `## 10. Presupuesto y Timeline` | Presupuesto total, deadline, equipo |

#### Cabecera de metadatos requerida

```markdown
> Versión: 1.0
> Fecha: [YYYY-MM-DD]
> Estado: ✅ Aprobado
> Elaborado por: Triple S (Sabbia Solutions & Services)
> Aprobado por: [nombre o cargo del aprobador]
```

#### Criterio de aceptación técnico

El campo `Estado` en la cabecera debe ser exactamente `✅ Aprobado` para que el agente lo reconozca como documento válido. Cualquier otro valor (borrador, en revisión, etc.) lo invalida como prerrequisito para etapas posteriores.

---

### 2.4 `[ARC-04]` — `PROJECT_handoff.md`

**Implementa**: `[REQ-04]`

#### Secciones obligatorias (en este orden)

| N | Sección | Contenido mínimo obligatorio |
|---|---|---|
| 1 | Cabecera de metadatos | Fecha de última actualización, sesión número |
| 2 | `## Estado Macro del Proyecto` | Fase activa, etapa activa, porcentaje de avance |
| 3 | `## Última Sesión` | Qué se hizo, archivos modificados o creados |
| 4 | `## Contexto Inmediato` | Decisiones tomadas que un agente nuevo debe conocer para no repetir exploración |
| 5 | `## Último Error / Bloqueador` | El último error encontrado (o "Ninguno" si no hay) |
| 6 | `## Próxima Acción Concreta` | Acción específica, comando concreto o documento a crear a continuación |
| 7 | `## Archivos Clave Activos` | Lista de archivos que están siendo modificados activamente en la etapa actual |

#### Cabecera de metadatos requerida

```markdown
> Última actualización: [YYYY-MM-DD HH:MM COT]
> Sesión: #[N]
> Etapa activa: f[F]_[E] — [Nombre de la etapa]
```

#### Regla de actualización

Este documento NO es histórico — se **reescribe completamente** en cada cierre de sesión. No acumula secciones por sesión. La información de sesiones previas se pierde intencionalmente (el historial vive en `lessons-learned.md` y Git).

---

### 2.5 `[ARC-05]` — `docs/lessons/lessons-learned.md`

**Implementa**: `[REQ-06]`

#### Estructura del documento

El documento es acumulativo. Cada etapa añade su propia sección sin modificar las secciones previas. La estructura base al inicializarlo en la Etapa 1.1:

```markdown
# Lecciones Aprendidas — Proyecto Almacén MultiTodo

> Mantenido por: Triple S (Sabbia Solutions & Services)
> Actualizar al cerrar cada etapa o sesión significativa.

---

## Etapa 1.1 — Constitución del Proyecto

### Qué funcionó bien
- [Observación inicial: la estructura de gobernanza spec-driven elimina ambigüedad desde el día cero]

### Qué generó fricción
- [Vacío hasta que se complete la etapa]

### Decisiones clave tomadas
- Adopción de arquitectura Medallion (Bronze/Silver/Gold) como estándar de datos.
- Agentes IA operan bajo CLAUDE.md como ley suprema, sin excepción.
- Skill-router como punto de entrada único para todos los flujos de agentes.

### Próximas etapas: alertas tempranas
- [Vacío hasta que se complete la etapa]
```

#### Regla de formato de secciones

Cada etapa usa exactamente cuatro subsecciones `###`:
1. `### Qué funcionó bien`
2. `### Qué generó fricción`
3. `### Decisiones clave tomadas`
4. `### Próximas etapas: alertas tempranas`

Las subsecciones nunca se eliminan aunque estén vacías — se deja el marcador `[Vacío]`.

---

### 2.6 `[ARC-06]` — `.claude/skill-router.md`

**Implementa**: `[REQ-07]`

#### Propósito funcional

Este archivo es el **directorio de ejecución** del sistema de agentes. Todo agente IA lo lee al inicio de sesión (paso 1 del protocolo) para saber qué skill invocar ante cada tipo de solicitud. Prohibido ejecutar flujos de Git, documentación o cierre de etapa con lógica propia sin consultar este archivo primero.

#### Estructura obligatoria del documento

```markdown
# Skill Router — Mapa de Agentes y Skills

> Lectura obligatoria en el Paso 1 del Protocolo de Inicio de Sesión.
> Ante cualquier solicitud del usuario, consultar este archivo primero.

## Convención de Invocación
[Explicar cómo invocar skills: comando + argumento de etapa]

## Tabla de Routing

| Solicitud del usuario | Skill | Comando | Prerrequisitos |
|---|---|---|---|
| ... | ... | ... | ... |

## Catálogo de Skills

### /[nombre-skill]
- **Descripción**: [Qué hace]
- **Disparadores**: [Frases que activan este skill]
- **Prerrequisitos**: [Documentos o condiciones requeridas]
- **Produce**: [Artefacto de salida]
```

#### Skills mínimos que deben documentarse en la inicialización

La tabla de routing debe cubrir al menos los siguientes skills al momento del commit inicial:

| Skill | Propósito |
|---|---|
| `/sdd-prd` | Crear/actualizar PRD de una etapa |
| `/sdd-spec` | Crear/actualizar SPEC de una etapa |
| `/sdd-plan` | Crear/actualizar Plan de una etapa |
| `/sdd-task` | Crear/actualizar Task List de una etapa |
| `/sdd` | Orquestador de la cadena documental completa |
| `/stage-audit` | Auditoría pre-cierre de etapa |
| `/close-stage` | Cierre formal y generación de executive summary |
| `/git-push` | Subir cambios a GitHub respetando el Git Flow |
| `/change-control` | Gestionar control de cambios |
| `/session-close-handoff` | Actualizar PROJECT_handoff.md al cerrar sesión |
| `/session-close-lessons` | Actualizar lessons-learned.md al cerrar sesión |
| `/scope-document` | Construir o actualizar PROJECT_scope.md |

---

### 2.7 `[ARC-07]` — `docs/references/` (6 documentos)

**Implementa**: `[REQ-08]`

Cada documento de referencia tiene un lector primario y un propósito técnico específico. A continuación la especificación de contenido mínimo para cada uno:

#### `docs/references/architecture.md`

**Lector primario**: Agentes IA y desarrolladores al diseñar componentes nuevos.

Secciones obligatorias:
1. `## Flujo de Datos General` — Diagrama ASCII: `usr_*` → Bronze → Silver → Gold → API Routes → Dashboard
2. `## Arquitectura Medallion` — Descripción de cada capa con prefijo de tabla, responsabilidad y SLA
3. `## Ciclo Diario de Operación` — Secuencia de ejecución: cuándo corre el pipeline, cuándo está disponible el dashboard
4. `## Componentes del Sistema` — Tabla con componente, tecnología, responsabilidad y ruta de código

#### `docs/references/tech-stack.md`

**Lector primario**: Desarrolladores al instalar dependencias o configurar entornos.

Secciones obligatorias:
1. `## Stack por Capa` — Tabla: capa (Pipeline / Web / BD / Infra), tecnología, versión, propósito
2. `## Variables de Entorno` — Lista de todas las variables requeridas en `.env` con descripción y ejemplo (sin valores reales)
3. `## Entornos` — Tabla: dev / staging / producción, con diferencias clave
4. `## Instalación Inicial` — Comandos de setup del entorno virtual Python y del proyecto Next.js

Versiones mínimas a documentar en la inicialización:
- Python: 3.11+
- Next.js: 14+ (App Router)
- Supabase SDK (Python): `supabase` (última estable)
- Pandera: 0.18+
- Pytest: 7+
- pytz: 2024+
- Node.js: 20+ LTS

#### `docs/references/dev-commands.md`

**Lector primario**: Agentes IA y desarrolladores al ejecutar tareas cotidianas.

Secciones obligatorias:
1. `## Setup Inicial` — Clonar repo, crear venv, instalar deps
2. `## Pipeline Python` — Comandos para correr el pipeline en cada modo (`validate`, `etl`, `alerts`)
3. `## Tests Backend` — `pytest` con cobertura
4. `## Tests Frontend` — `npm run test`, `npm run test:watch`, `npm run e2e`
5. `## Linting` — `npm run lint`
6. `## Dev Local` — `npm run dev`
7. `## Git Flow` — Secuencia estándar de trabajo en ramas `feat/*`

Formato de cada comando: bloque de código con el comando exacto y comentario de propósito.

#### `docs/references/incident-protocol.md`

**Lector primario**: Equipo de operaciones y agentes al detectar fallas en producción.

Secciones obligatorias:
1. `## Clasificación de Severidades` — Tabla P1/P2/P3/P4 con criterio de clasificación y tiempo de respuesta objetivo
2. `## Protocolo por Severidad` — Pasos de respuesta para cada nivel de severidad
3. `## Canales de Comunicación` — Cómo y a quién escalar según severidad
4. `## Códigos de Error del Pipeline` — Tabla con todos los `ERR_MTD_XXX` y su significado
5. `## Post-Mortem` — Template mínimo de análisis post-incidente

Clasificación de severidades mínima:
| Nivel | Criterio | Tiempo de Respuesta |
|---|---|---|
| P1 | Dashboard caído o datos incorrectos en producción | < 1 hora |
| P2 | Pipeline fallando, datos T-1 no disponibles a las 8 AM COT | < 2 horas |
| P3 | Alerta falsa o métrica incorrecta detectada | < 4 horas |
| P4 | Mejora no urgente o ajuste estético | Próxima sesión |

#### `docs/references/glossary.md`

**Lector primario**: Todo agente y stakeholder — es el vocabulario compartido del proyecto.

Secciones obligatorias:
1. `## Términos de Negocio` — Definiciones de términos del cliente (SKU, sede, stock físico, etc.)
2. `## Términos Técnicos del Pipeline` — T-1, COT, Bronze/Silver/Gold, Data Contract, cuarentena
3. `## Códigos de Error` — Todos los `ERR_MTD_XXX` con su definición exacta
4. `## Convenciones de Nomenclatura` — Prefijos de tablas, convención SDD, formato de commits

Términos mínimos que deben estar definidos al inicializar:
- T-1, T+0
- COT (Colombia Time, America/Bogota, UTC-5)
- Bronze / Silver / Gold
- Data Contract
- Cuarentena (`tss_cuarentena_*`)
- ERR_MTD_001 a ERR_MTD_005
- `usr_*` / `tss_*`
- SDD (Software Design Document)
- `feat/*`

#### `docs/references/adr.md`

**Lector primario**: Arquitectos y agentes al tomar nuevas decisiones técnicas — para no repetir debates pasados.

Formato de cada ADR (Architecture Decision Record):

```markdown
### ADR-001 — [Título de la decisión]

- **Estado**: Aceptado
- **Fecha**: [YYYY-MM-DD]
- **Contexto**: [Por qué surgió esta decisión]
- **Decisión**: [Qué se decidió exactamente]
- **Consecuencias**: [Qué implica esta decisión — ventajas y compromisos]
```

ADRs mínimos a documentar en la inicialización:

| ADR | Decisión |
|---|---|
| ADR-001 | Arquitectura Medallion (Bronze/Silver/Gold) como estándar de capa de datos |
| ADR-002 | Supabase como backend de base de datos (PostgreSQL gestionado) |
| ADR-003 | Next.js 14 con App Router para el dashboard |
| ADR-004 | Restricción T-1: el dashboard nunca muestra datos del día en curso |
| ADR-005 | TDD universal: ningún código de producto sin test previo que falle |

---

### 2.8 `[ARC-08]` — Commit inicial en `main`

**Implementa**: `[REQ-09]`

#### Mensaje de commit exacto

```
feat: constitución inicial del proyecto — gobernanza, scope y herramientas Claude
```

#### Archivos que deben estar incluidos en el commit

El commit es válido si y solo si incluye **todos** los siguientes archivos. La ausencia de cualquiera invalida la métrica `[MET-03]`:

```
CLAUDE.md
PROJECT_scope.md
PROJECT_handoff.md
.gitignore
docs/reqs/f01_01_prd.md
docs/lessons/lessons-learned.md
docs/references/architecture.md
docs/references/tech-stack.md
docs/references/dev-commands.md
docs/references/incident-protocol.md
docs/references/glossary.md
docs/references/adr.md
.claude/skill-router.md
pipeline/.gitkeep  (o pipeline/main.py con placeholder)
pipeline/src/.gitkeep
pipeline/tests/.gitkeep
pipeline/pipelines/.gitkeep
web/components/.gitkeep
web/app/.gitkeep
web/tests/.gitkeep
docs/specs/.gitkeep
docs/plans/.gitkeep
docs/tasks/.gitkeep
docs/database/.gitkeep
docs/executives/.gitkeep
docs/changes/.gitkeep
```

#### Verificación post-commit

Inmediatamente después del commit, verificar:
1. `git status` devuelve `nothing to commit, working tree clean`
2. `git log --oneline -1` muestra el mensaje exacto definido arriba
3. `git branch` muestra `* main`

---

## 3. Diseño de Módulos y Funciones

Esta etapa no produce módulos de código Python ni componentes Next.js. No aplica esta sección en el sentido de funciones de software.

Las "funciones" de esta etapa son procedimientos humanos/agente:

| Procedimiento | Responsable | Input | Output | REQ |
|---|---|---|---|---|
| Inicializar repositorio | Agente / dev | Directorio vacío | Repo Git con `main` activa | `[REQ-01]` |
| Crear `.gitignore` | Agente / dev | Spec 2.1 | `.gitignore` conforme | `[REQ-01]` |
| Crear estructura de carpetas | Agente / dev | Spec 2.1 | 19 carpetas + `.gitkeep` | `[REQ-05]` |
| Redactar `CLAUDE.md` | Agente / dev | Spec 2.2 + `[DAT-03]` | `CLAUDE.md` con 19 secciones | `[REQ-02]` |
| Redactar `PROJECT_scope.md` | Agente / dev | Spec 2.3 + `[DAT-01]` | `PROJECT_scope.md` aprobado | `[REQ-03]` |
| Redactar `PROJECT_handoff.md` | Agente / dev | Spec 2.4 | `PROJECT_handoff.md` inicial | `[REQ-04]` |
| Inicializar `lessons-learned.md` | Agente / dev | Spec 2.5 | Archivo con sección Etapa 1.1 | `[REQ-06]` |
| Crear `skill-router.md` | Agente / dev | Spec 2.6 | Mapa de 12+ skills documentados | `[REQ-07]` |
| Crear 6 documentos de referencias | Agente / dev | Spec 2.7 | 6 archivos `.md` en `docs/references/` | `[REQ-08]` |
| Ejecutar commit inicial | Agente / dev | Spec 2.8 | Commit en `main` con mensaje exacto | `[REQ-09]` |

---

## 4. Configuración Requerida

Esta etapa no requiere `config.yaml` ni `.env` — no hay código de pipeline ni conexiones a Supabase.

La "configuración" de esta etapa son las convenciones que quedan fijadas en `CLAUDE.md` para uso en etapas posteriores. Las siguientes claves se anticipan como variables de entorno requeridas desde la Etapa 1.2 en adelante (documentadas en `docs/references/tech-stack.md`):

| Variable | Etapa en que se usa | Descripción |
|---|---|---|
| `SUPABASE_URL` | 1.2+ | URL del proyecto Supabase |
| `SUPABASE_ANON_KEY` | 1.2+ | Clave pública anónima de Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | 1.2+ | Clave de servicio (solo pipeline, nunca frontend) |
| `NEXT_PUBLIC_SUPABASE_URL` | 3.6+ | URL expuesta al cliente Next.js |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | 3.6+ | Clave anónima expuesta al cliente Next.js |

Estas variables se definen en `.env` en la raíz del proyecto. El `.gitignore` ya las excluye por la regla `.env`.

---

## 5. Matriz de Trazabilidad: SPEC vs PRD

| REQ (PRD) | Componente [ARC] | Procedimiento / Artefacto | Sección SPEC |
|---|---|---|---|
| `[REQ-01]` | `[ARC-01]` | Repositorio Git + `.gitignore` | § 2.1 |
| `[REQ-02]` | `[ARC-02]` | `CLAUDE.md` con 19 secciones | § 2.2 |
| `[REQ-03]` | `[ARC-03]` | `PROJECT_scope.md` con 11 secciones | § 2.3 |
| `[REQ-04]` | `[ARC-04]` | `PROJECT_handoff.md` con 7 secciones | § 2.4 |
| `[REQ-05]` | `[ARC-01]` | 19 carpetas con `.gitkeep` | § 2.1 |
| `[REQ-06]` | `[ARC-05]` | `lessons-learned.md` inicializado | § 2.5 |
| `[REQ-07]` | `[ARC-06]` | `skill-router.md` con 12 skills | § 2.6 |
| `[REQ-08]` | `[ARC-07]` | 6 documentos de referencias técnicas | § 2.7 |
| `[REQ-09]` | `[ARC-08]` | Commit con mensaje exacto en `main` | § 2.8 |

---

## 6. Criterios de Aceptación Técnicos Verificables

Estos criterios son la traducción técnica de las métricas `[MET-XX]` del PRD a acciones de verificación concretas.

| MET | Verificación | Comando / Acción | Resultado esperado |
|---|---|---|---|
| `[MET-01]` | 100% artefactos presentes | `ls` de cada ruta listada en § 2.8 | Todos los archivos existen, sin errores |
| `[MET-02]` | Estructura de carpetas conforme | `find . -type d` en la raíz | Las 19 carpetas requeridas aparecen en el output |
| `[MET-03]` | Repo Git en estado limpio | `git status` | Devuelve `nothing to commit, working tree clean` |
| `[MET-04]` | `PROJECT_scope.md` aprobado | `grep "Estado" PROJECT_scope.md` | Devuelve línea con `✅ Aprobado` |
| `[MET-05]` | Onboarding de agente < 5 min | Verificación cualitativa | Agente lee `CLAUDE.md` + `PROJECT_handoff.md` y no hace preguntas sobre estructura |

---

## 7. Decisiones de Diseño y Justificación

- **`[ARC-02]` `CLAUDE.md` en la raíz del repositorio**: Ubicación estándar para instrucciones de agentes IA en el ecosistema Claude Code. Garantiza que sea el primer archivo leído en cualquier sesión.

- **Uso de `.gitkeep` en carpetas vacías**: Git no trackea directorios vacíos. `.gitkeep` es la convención establecida para incluir directorios sin contenido en el commit inicial, preservando la estructura de carpetas sin generar confusión con archivos de configuración.

- **`PROJECT_handoff.md` se reescribe completamente (no acumula)**: El contexto de sesiones pasadas degrada la señal/ruido para un agente nuevo. El historial vive en Git y en `lessons-learned.md`. El handoff es siempre el estado AHORA, no el historial.

- **`skill-router.md` como paso 1 del protocolo de inicio**: Garantiza que el agente sepa ANTES de leer cualquier otro archivo qué herramientas tiene disponibles. Previene que el agente improvise flujos propios para tareas que tienen skill dedicado.

- **Documentar variables de entorno en `tech-stack.md` sin valores reales**: Permite que cualquier miembro del equipo sepa exactamente qué configurar sin exponer secretos en el repositorio. El `.gitignore` protege el `.env` con los valores reales.

- **Mensaje de commit exacto como criterio de aceptación de `[REQ-09]`**: Un mensaje exacto (no aproximado) permite verificar con `git log --grep` de forma determinística. Elimina ambigüedad sobre qué commit es el de constitución.

- **ADR-004 documentado desde la Etapa 1.1**: La restricción T-1 es la restricción de negocio más crítica del proyecto. Documentarla como ADR desde el día cero previene que cualquier agente o desarrollador la cuestione o la viole sin leer el contexto de la decisión.
