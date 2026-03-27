# Plan de Implementación — Constitución del Proyecto (`f01_01`)

> Documento: `docs/plans/f01_01_plan.md`
> Versión: 1.0
> Fecha: 2026-03-27
> Estado: ✅ Aprobado
> Elaborado por: Triple S (Sabbia Solutions & Services)
> Trazabilidad: Este plan ejecuta `docs/reqs/f01_01_prd.md` según el diseño de `docs/specs/f01_01_spec.md`.

---

## 1. Resumen del Plan

La Etapa 1.1 es de tipo **DOCUMENTACIÓN pura** — no produce código de pipeline ni componentes de interfaz. Su objetivo es establecer el entorno controlado (repositorio, leyes de comportamiento, scope aprobado, estructura y herramientas de agentes) sobre el que operará el proyecto durante los siguientes 3 meses.

La estrategia de ejecución sigue el **grafo de dependencia entre artefactos** definido en `[ARC-01]` a `[ARC-08]` de la SPEC: cada documento depende del anterior porque lo referencia o lo presupone. No hay paralelismo real entre bloques — la cadena es estrictamente secuencial.

**Estado actual al momento de redactar este plan (2026-03-27):**

| Artefacto | Estado |
|---|---|
| `CLAUDE.md` | Completado |
| `PROJECT_scope.md` | Completado |
| `docs/reqs/f01_01_prd.md` | Completado |
| `docs/specs/f01_01_spec.md` | Completado |
| Estructura de carpetas base | Completado |
| `.gitignore` | Completado |
| `docs/references/` (6 documentos) | Completado |
| `docs/lessons/lessons-learned.md` | Completado |
| `.claude/skill-router.md` | Completado |
| `docs/plans/f01_01_plan.md` | **En ejecución** (este documento) |
| `PROJECT_handoff.md` | **Pendiente** |
| `docs/tasks/f01_01_task.md` | **Pendiente** |
| Commit de cierre de etapa (SDD) | **Pendiente** |

**Hitos clave:**
1. Todos los artefactos de gobernanza en el repositorio.
2. `PROJECT_handoff.md` creado — agente puede retomar el proyecto sin re-exploración.
3. Estado limpio en Git: `nothing to commit, working tree clean`.

---

## 2. Ruta Crítica

### 2.1 Diagrama de Dependencias

```
ESTADO INICIAL (2026-03-27)
  │
  │  [Completados previamente]
  │  ✅ B1: Repositorio + estructura + .gitignore
  │  ✅ B2: CLAUDE.md
  │  ✅ B3: PROJECT_scope.md
  │  ✅ B4: Artefactos de soporte (references, lessons, skill-router)
  │  ✅ B5: PRD + SPEC de la etapa (f01_01_prd.md, f01_01_spec.md)
  │
  ↓
[B6: Plan de Implementación] — este documento
  ↓
[B7: PROJECT_handoff.md]
  ↓
[B8: Task List (f01_01_task.md)]
  ↓
[B9: Commit de cierre de etapa SDD]
  ↓
FIN — Etapa lista para /stage-audit y /close-stage
```

### 2.2 Análisis de Ruta Crítica

| Bloque | Descripción | Duración Est. | Dependencias | En Ruta Crítica |
|---|---|---|---|---|
| B1 | Repositorio + estructura + .gitignore | — | Ninguna | ✅ SI (completado) |
| B2 | `CLAUDE.md` | — | B1 | ✅ SI (completado) |
| B3 | `PROJECT_scope.md` | — | B2 | ✅ SI (completado) |
| B4 | References + lessons + skill-router | — | B2 | ✅ SI (completado) |
| B5 | PRD + SPEC de la etapa | — | B3, B4 | ✅ SI (completado) |
| B6 | Plan de Implementación (`f01_01_plan.md`) | 0.5 días | B5 | ✅ SI |
| B7 | `PROJECT_handoff.md` | 0.5 días | B6 | ✅ SI |
| B8 | Task List (`f01_01_task.md`) | 0.5 días | B6, B7 | ✅ SI |
| B9 | Commit de cierre de etapa SDD | 0.25 días | B7, B8 | ✅ SI |

Toda la cadena es ruta crítica — no existe paralelismo viable dado que cada artefacto referencia o presupone el anterior.

---

## 3. Backlog de Trabajo (WBS)

Los bloques B1 a B5 están completados. Se documenta su descripción para trazabilidad. Los bloques activos son B6 a B9.

---

### B1 — Repositorio Git + Estructura + `.gitignore` ✅ COMPLETADO

- **Objetivo**: Crear el contenedor versionado con estructura de carpetas y reglas de exclusión Git.
- **Componentes [ARC] relacionados**: `[ARC-01]`
- **Requerimientos que implementa**: `[REQ-01]`, `[REQ-05]`
- **Entregables**: Repositorio inicializado, rama `main`, `.gitignore` conforme, 19 carpetas con `.gitkeep`.
- **Hito de aceptación**:
  - [x] `git status` muestra repositorio limpio
  - [x] `.gitignore` excluye `.venv/`, `.env`, `*.pyc`, `__pycache__/`, `.next/`, `node_modules/`
  - [x] Las 19 carpetas requeridas existen en el repositorio

---

### B2 — `CLAUDE.md` ✅ COMPLETADO

- **Objetivo**: Establecer la ley suprema de comportamiento para todos los agentes IA y miembros del equipo.
- **Componentes [ARC] relacionados**: `[ARC-02]`
- **Requerimientos que implementa**: `[REQ-02]`
- **Entregables**: `CLAUDE.md` en la raíz con 19 secciones obligatorias.
- **Hito de aceptación**:
  - [x] Archivo presente en raíz del repositorio
  - [x] Contiene las 19 secciones especificadas en SPEC § 2.2
  - [x] Cabecera obligatoria presente con referencia a Triple S

---

### B3 — `PROJECT_scope.md` ✅ COMPLETADO

- **Objetivo**: Capturar y aprobar formalmente el alcance del proyecto completo.
- **Componentes [ARC] relacionados**: `[ARC-03]`
- **Requerimientos que implementa**: `[REQ-03]`
- **Entregables**: `PROJECT_scope.md` con 11 secciones y estado `✅ Aprobado`.
- **Hito de aceptación**:
  - [x] Archivo presente en raíz
  - [x] Contiene las 11 secciones requeridas en SPEC § 2.3
  - [x] Cabecera contiene `Estado: ✅ Aprobado`

---

### B4 — Artefactos de Soporte (References + Lessons + Skill-Router) ✅ COMPLETADO

- **Objetivo**: Poblar los documentos de referencia técnica, inicializar el log de lecciones aprendidas y crear el mapa de skills.
- **Componentes [ARC] relacionados**: `[ARC-05]`, `[ARC-06]`, `[ARC-07]`
- **Requerimientos que implementa**: `[REQ-06]`, `[REQ-07]`, `[REQ-08]`
- **Entregables**:
  - `docs/references/architecture.md`
  - `docs/references/tech-stack.md`
  - `docs/references/dev-commands.md`
  - `docs/references/incident-protocol.md`
  - `docs/references/glossary.md`
  - `docs/references/adr.md`
  - `docs/lessons/lessons-learned.md` (inicializado con sección Etapa 1.1)
  - `.claude/skill-router.md` (12 skills documentados)
- **Hito de aceptación**:
  - [x] Los 6 documentos de references existen con contenido conforme a SPEC § 2.7
  - [x] `lessons-learned.md` inicializado con las 4 subsecciones de Etapa 1.1
  - [x] `skill-router.md` cubre los 12 skills mínimos definidos en SPEC § 2.6

---

### B5 — PRD + SPEC de la Etapa ✅ COMPLETADO

- **Objetivo**: Documentar formalmente los requerimientos y el diseño técnico de la Etapa 1.1 en sí misma.
- **Componentes [ARC] relacionados**: Cadena SDD interna de la etapa
- **Requerimientos que implementa**: Prerrequisito documental (no es un `[REQ-XX]` del PRD — es el PRD mismo)
- **Entregables**:
  - `docs/reqs/f01_01_prd.md` (9 requerimientos, 4 objetivos, 5 métricas)
  - `docs/specs/f01_01_spec.md` (8 componentes ARC, especificaciones de cada artefacto)
- **Hito de aceptación**:
  - [x] Ambos documentos existen con estado `✅ Aprobado`
  - [x] Trazabilidad REQ → ARC completa en la SPEC

---

### B6 — Plan de Implementación (`f01_01_plan.md`) — EN EJECUCIÓN

- **Objetivo**: Documentar el orden, dependencias y estrategia de ejecución de la etapa para guiar el cierre.
- **Componentes [ARC] relacionados**: Cadena SDD interna de la etapa
- **Requerimientos que implementa**: Prerrequisito documental para `f01_01_task.md`
- **Entregables**: `docs/plans/f01_01_plan.md` (este documento)
- **Duración estimada**: 0.5 días
- **Dependencias**: B5 completado
- **Hito de aceptación**:
  - [ ] Archivo escrito en `docs/plans/f01_01_plan.md`
  - [ ] Refleja el estado real de la etapa (parcialmente ejecutada)
  - [ ] Ruta crítica documentada con bloques B1 a B9
  - [ ] DoD de la etapa definida en sección 5

---

### B7 — `PROJECT_handoff.md` — PENDIENTE

- **Objetivo**: Crear el documento de estado táctico que permite retomar el proyecto en cualquier sesión futura sin re-exploración.
- **Componentes [ARC] relacionados**: `[ARC-04]`
- **Requerimientos que implementa**: `[REQ-04]`
- **Entregables**: `PROJECT_handoff.md` en la raíz con 7 secciones conforme a SPEC § 2.4.
- **Duración estimada**: 0.5 días
- **Dependencias**: B6 (el plan debe existir para que el handoff referencie el estado correcto)
- **Hito de aceptación**:
  - [ ] Archivo presente en raíz del repositorio
  - [ ] Contiene las 7 secciones: estado macro, última sesión, contexto inmediato, último error/bloqueador, próxima acción concreta, archivos clave activos
  - [ ] Cabecera con fecha, número de sesión y etapa activa `f01_01`
  - [ ] "Próxima acción concreta" apunta a `/sdd-task f01_01` o al paso siguiente correcto

---

### B8 — Task List (`f01_01_task.md`) — PENDIENTE

- **Objetivo**: Generar el checklist granular y ejecutable de todas las tareas de la Etapa 1.1 (incluyendo las completadas, para trazabilidad histórica).
- **Componentes [ARC] relacionados**: Cadena SDD interna de la etapa
- **Requerimientos que implementa**: Prerrequisito para `/stage-audit` y `/close-stage`
- **Entregables**: `docs/tasks/f01_01_task.md`
- **Duración estimada**: 0.5 días
- **Dependencias**: B6 + B7
- **Hito de aceptación**:
  - [ ] Archivo existe en `docs/tasks/f01_01_task.md`
  - [ ] Las tareas de bloques B1-B5 están marcadas `[x]` como completadas
  - [ ] Las tareas de B7-B9 están como `[ ]` pendientes
  - [ ] Cada tarea tiene anotación de dependencia (`independiente`, `depends_on`, `parallel_with`)
  - [ ] Mapa de dependencias presente al inicio del documento

---

### B9 — Commit de Cierre de Etapa SDD — PENDIENTE

- **Objetivo**: Crear un snapshot inmutable en `main` con todos los documentos SDD de la etapa (`prd`, `spec`, `plan`, `task`) y el `PROJECT_handoff.md`.
- **Componentes [ARC] relacionados**: `[ARC-08]` (extensión del commit inicial para los documentos SDD)
- **Requerimientos que implementa**: `[REQ-09]` (cierre del conjunto documental)
- **Entregables**: Commit en `main` con los documentos SDD de cierre.
- **Duración estimada**: 0.25 días
- **Dependencias**: B7 + B8
- **Estrategia**: Invocar `/git-push` para subir los cambios respetando el Git Flow del proyecto.
- **Hito de aceptación**:
  - [ ] `git status` devuelve `nothing to commit, working tree clean`
  - [ ] `git log --oneline -1` muestra commit con los documentos SDD incluidos
  - [ ] Los 4 documentos SDD (`prd`, `spec`, `plan`, `task`) y `PROJECT_handoff.md` están en `main`

---

## 4. Estrategia de Pruebas

Esta etapa es de tipo DOCUMENTACIÓN — no hay suite de tests automatizados. La "prueba" es verificación documental y estructural.

| Tipo | Qué se verifica | Método | Criterio de Éxito | Bloque |
|---|---|---|---|---|
| Verificación estructural | Existencia de archivos requeridos | `ls` / `find` de cada ruta listada en SPEC § 2.8 | Todos los archivos existen sin errores de ruta | B1-B5 (completado) |
| Verificación de contenido | Secciones obligatorias de cada documento | Lectura manual / `grep` de encabezados de sección | Cada documento contiene las secciones definidas en SPEC § 2.2–2.7 | B1-B5 (completado) |
| Verificación de aprobación | `PROJECT_scope.md` con estado correcto | `grep "Estado" PROJECT_scope.md` | Retorna línea con `✅ Aprobado` | B3 (completado) |
| Verificación Git | Estado limpio del repositorio | `git status` | `nothing to commit, working tree clean` | B9 |
| Verificación de commit | Mensaje correcto en `main` | `git log --oneline -1` | Muestra el mensaje de commit esperado | B9 |
| Auditoría de etapa | Conformidad documental completa antes de cierre | `/stage-audit f01_01` | Skill reporta 0 gaps y todos los DoD satisfechos | Post B9 |

---

## 5. Definition of Done (DoD)

La Etapa 1.1 se considera completada cuando se cumplen **todos** los siguientes criterios:

### Artefactos de gobernanza
- [ ] `CLAUDE.md` presente en raíz con 19 secciones
- [ ] `PROJECT_scope.md` presente con estado `✅ Aprobado`
- [ ] `PROJECT_handoff.md` presente con 7 secciones y etapa activa `f01_01`
- [ ] `.gitignore` conforme a SPEC § 2.1
- [ ] 19 carpetas de la estructura base existen (con `.gitkeep` donde corresponde)

### Artefactos de soporte
- [ ] `docs/lessons/lessons-learned.md` inicializado con sección Etapa 1.1
- [ ] `.claude/skill-router.md` con los 12 skills mínimos documentados
- [ ] 6 documentos de referencias presentes en `docs/references/`

### Cadena documental SDD de la etapa
- [ ] `docs/reqs/f01_01_prd.md` — Estado `✅ Aprobado`
- [ ] `docs/specs/f01_01_spec.md` — Estado `✅ Aprobado`
- [ ] `docs/plans/f01_01_plan.md` — Estado `✅ Aprobado` (este documento)
- [ ] `docs/tasks/f01_01_task.md` — Creado y con estado inicial

### Estado del repositorio
- [ ] `git status` retorna `nothing to commit, working tree clean`
- [ ] `git log` muestra el commit de constitución con mensaje exacto: `feat: constitución inicial del proyecto — gobernanza, scope y herramientas Claude`
- [ ] Los documentos SDD de la etapa (plan + task + handoff) están en `main`

### Auditoría pre-cierre
- [ ] `/stage-audit f01_01` ejecutado sin gaps críticos reportados
- [ ] `docs/executives/f01_01_executive.md` generado por `/close-stage f01_01`

---

## 6. Matriz de Trazabilidad: Plan vs SPEC vs PRD

| Bloque | Componentes [ARC] | REQ Implementados | MET Verificada |
|---|---|---|---|
| B1 | `[ARC-01]` | `[REQ-01]`, `[REQ-05]` | `[MET-02]`, `[MET-03]` |
| B2 | `[ARC-02]` | `[REQ-02]` | `[MET-01]`, `[MET-05]` |
| B3 | `[ARC-03]` | `[REQ-03]` | `[MET-04]` |
| B4 | `[ARC-05]`, `[ARC-06]`, `[ARC-07]` | `[REQ-06]`, `[REQ-07]`, `[REQ-08]` | `[MET-01]` |
| B5 | Cadena SDD interna | (PRD y SPEC son el B5 mismo) | `[MET-01]` |
| B6 | Cadena SDD interna | (Plan es el B6 mismo) | `[MET-01]` |
| B7 | `[ARC-04]` | `[REQ-04]` | `[MET-01]`, `[MET-05]` |
| B8 | Cadena SDD interna | (Task List cierra la cadena SDD) | `[MET-01]` |
| B9 | `[ARC-08]` | `[REQ-09]` | `[MET-03]` |
