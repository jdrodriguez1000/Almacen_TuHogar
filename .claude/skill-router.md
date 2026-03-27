# Skill Router — Enrutador Central de Agentes y Habilidades

Este archivo es el punto de referencia central para la delegación de tareas del proyecto Dashboard BI — Almacén MultiTodo.

Ante cualquier solicitud del usuario, el modelo debe:
1. Identificar la Intención → buscarla en la columna "Escenario".
2. Delegar al Agente Responsable usando el Skill / Comando indicado.
3. No ejecutar la tarea con lógica propia: el Skill es la única fuente de verdad técnica.

---

## Protocolo de Inicio de Sesión

Al iniciar una nueva sesión o ventana de chat, ejecutar en este orden:

1. **Escanear el Router**: Leer este archivo completo para mapear los agentes y skills disponibles en el proyecto.
2. **Identificar el Trigger**: Si el usuario solicita una acción listada en la columna "Escenario / Intención del Usuario", delegar la tarea al agente asociado sin demora.
3. **Prohibición de Improvisación**: Queda prohibido ejecutar flujos de Git, cambios documentales, cierres de etapa, cierres de sesión o documentación SDD con lógica propia del modelo. El Skill asociado es la única fuente de verdad técnica para cada dominio.

---

## Tabla de Enrutamiento

| Escenario / Intención del Usuario | Agente Responsable | Skill / Comando | Propósito Principal |
|---|---|---|---|
| Cambio no planificado, algo no contemplado en los documentos SDD de la etapa activa, o edición de etapa cerrada | `change-controller` | `/change-control` | Garantizar trazabilidad de ediciones fuera de plan. Gestiona el ciclo CC completo: crear, aprobar, rechazar, ejecutar. |
| Publicar en GitHub, hacer push, crear PR, configurar remoto, corregir flujo Git | `git-pusher` | `/git-push` | Commits, Push y Pull Requests bajo Git Flow (feat/* → main vía PR con CI). |
| Definir alcance del proyecto, dudas de negocio iniciales, "qué vamos a construir", crear o actualizar PROJECT_scope.md | `scope-documenter` | `/scope-document` | Crear/actualizar PROJECT_scope.md mediante entrevistas estructuradas con stakeholders. |
| Crear PRD, escribir requerimientos, documentar qué construimos en una etapa | `sdd-documenter` | `/sdd-prd` | Genera el PRD de la etapa activa. Punto de entrada de la cadena documental SDD. |
| Crear SPEC, diseño técnico, arquitectura, esquema de datos de una etapa | `sdd-documenter` | `/sdd-spec` | Genera la especificación técnica. Requiere PRD previo. |
| Crear Plan de Implementación, ruta crítica, orden de ejecución, bloques de trabajo | `sdd-documenter` | `/sdd-plan` | Genera el Plan de la etapa. Requiere PRD + SPEC previos. |
| Crear Lista de Tareas, checklist de desarrollo, task list, qué debo programar | `sdd-documenter` | `/sdd-task` | Genera la Lista de Tareas ejecutable. Requiere PRD + SPEC + Plan previos. |
| Documentar toda la etapa (PRD + SPEC + Plan + Tareas en cadena) | `sdd-documenter` | `/sdd-prd` → `/sdd-spec` → `/sdd-plan` → `/sdd-task` | Orquesta la cadena documental SDD completa en secuencia, respetando dependencias. |
| Auditar una etapa, verificar DoD, revisar conformidad, "audita la etapa", check DoD, validar tareas completadas, certificar avance antes del cierre | `stage-auditor` | `/stage-audit` | Cross-check técnico y documental. Gate obligatorio antes de `/close-stage`. Detecta Código Fantasma y emite token de aprobación. |
| Cerrar una etapa, generar resumen ejecutivo, la etapa está terminada, finalizar etapa | `stage-closer` | `/close-stage` | Genera `docs/executives/f[F]_[E]_executive.md`. Gate obligatorio para avanzar a la siguiente etapa. Requiere token de auditoría CONFORME previo. |
| Terminar sesión, cerramos, hasta luego, guardar estado del proyecto, actualizar handoff | `session-closer` | `/session-close-handoff` → `/session-close-lessons` | Ejecuta el cierre en dos fases: reescribe PROJECT_handoff.md y actualiza lessons-learned.md. |
| Registrar lecciones aprendidas, retrospectiva, qué aprendimos esta sesión | `session-closer` | `/session-close-lessons` | Actualiza docs/lessons/lessons-learned.md. Se ejecuta como segunda fase del cierre de sesión. |

---

## Catálogo de Skills

### /change-control
- **Descripción**: Gestiona el ciclo de vida completo de un Control de Cambio (CC): crear, aprobar, rechazar, ejecutar y cerrar.
- **Disparadores**: "cambio no planificado", "esto no está en el spec", "necesito modificar una etapa cerrada", "change control", "CC", "algo no contemplado"
- **Prerrequisitos**: Documento SDD activo de la etapa en curso o etapa cerrada que se desea modificar.
- **Produce**: `docs/changes/CC_XXXXX.md` con estado `Pendiente` → `Aprobado` → `Ejecutado`.

### /git-push
- **Descripción**: Gestiona el ciclo completo de Git: commits, push de ramas y creación de Pull Requests respetando el Git Flow (feat/* → main vía PR con CI).
- **Disparadores**: "sube a GitHub", "push", "subir al repositorio", "configura el remoto", "publicar rama", "crear PR", "abrir pull request", "commit"
- **Prerrequisitos**: Cambios staged o archivos listos para commit; remoto configurado para push.
- **Produce**: Commit en rama activa y/o PR en GitHub.

### /scope-document
- **Descripción**: Construye o actualiza `PROJECT_scope.md` mediante entrevistas estructuradas con stakeholders. Captura QUÉ se construye, PARA QUIÉN y cómo se medirá el éxito.
- **Disparadores**: "define el alcance", "crea el scope", "qué vamos a construir", "documenta el alcance", "PROJECT_scope.md"
- **Prerrequisitos**: Ninguno — es el documento raíz del proyecto.
- **Produce**: `PROJECT_scope.md` con estado `✅ Aprobado`.

### /sdd-prd
- **Descripción**: Crea o actualiza el PRD (Product Requirements Document) de una etapa: QUÉ construir, POR QUÉ y cómo medir el éxito.
- **Disparadores**: "crea el PRD", "escribe los requerimientos", "documenta el alcance de la etapa", "prd", "requerimientos de la etapa"
- **Prerrequisitos**: `PROJECT_scope.md` aprobado.
- **Produce**: `docs/reqs/f[F]_[E]_prd.md`

### /sdd-spec
- **Descripción**: Crea o actualiza la SPEC (Especificación Técnica) de una etapa: CÓMO implementar lo que el PRD define. Incluye arquitectura, esquemas de datos y contratos.
- **Disparadores**: "crea la spec", "especificación técnica", "diseño técnico", "spec", "definir arquitectura", "esquema de datos"
- **Prerrequisitos**: PRD aprobado de la etapa (`docs/reqs/f[F]_[E]_prd.md`).
- **Produce**: `docs/specs/f[F]_[E]_spec.md`

### /sdd-plan
- **Descripción**: Crea o actualiza el Plan de Implementación de una etapa: ORDEN, DEPENDENCIAS y ESTRATEGIA de ejecución. Define bloques de trabajo, ruta crítica y DoD.
- **Disparadores**: "crea el plan", "plan de implementación", "orden de desarrollo", "ruta crítica", "bloques de trabajo", "sdd-plan"
- **Prerrequisitos**: PRD + SPEC aprobados de la etapa.
- **Produce**: `docs/plans/f[F]_[E]_plan.md`

### /sdd-task
- **Descripción**: Crea o actualiza la Lista de Tareas de una etapa: checklist atómico y ejecutable que un desarrollador sigue diariamente.
- **Disparadores**: "crea las tareas", "genera el task list", "qué debo programar", "task list", "checklist de desarrollo", "lista de tareas"
- **Prerrequisitos**: PRD + SPEC + Plan aprobados de la etapa.
- **Produce**: `docs/tasks/f[F]_[E]_task.md`

### /stage-audit
- **Descripción**: Ejecuta la auditoría técnica y documental de una etapa antes de su cierre formal. Verifica DoD, detecta Código Fantasma y emite token CONFORME o BLOQUEADO.
- **Disparadores**: "audita la etapa", "verificar avance", "check DoD", "auditoría de etapa", "validar tareas", "revisar conformidad", "stage-audit"
- **Prerrequisitos**: Los 4 documentos SDD de la etapa deben existir (`prd`, `spec`, `plan`, `task`).
- **Produce**: Reporte de auditoría + token en `.claude/audit-token.md`.

### /close-stage
- **Descripción**: Cierra formalmente una etapa generando el Resumen Ejecutivo en lenguaje de negocio. Gate obligatorio para avanzar a la siguiente etapa.
- **Disparadores**: "cerramos la etapa", "terminamos la etapa", "genera el resumen ejecutivo", "close the stage", "finalizar etapa"
- **Prerrequisitos**: Token CONFORME emitido por `/stage-audit`.
- **Produce**: `docs/executives/f[F]_[E]_executive.md`

### /session-close-handoff
- **Descripción**: Reescribe completamente `PROJECT_handoff.md` con el estado macro y táctico actual del proyecto. Primera fase del protocolo de cierre de sesión.
- **Disparadores**: "terminamos", "cerramos", "hasta luego", "actualiza el handoff", "guarda el estado", fin de sesión implícito o explícito
- **Prerrequisitos**: Ninguno — puede ejecutarse en cualquier momento de la sesión.
- **Produce**: `PROJECT_handoff.md` reescrito con estado actual.

### /session-close-lessons
- **Descripción**: Actualiza `docs/lessons/lessons-learned.md` con las lecciones de la sesión: qué funcionó, qué generó fricción y decisiones clave. Segunda fase del protocolo de cierre.
- **Disparadores**: "registra las lecciones", "lecciones aprendidas", "retrospectiva", "session-close-lessons"
- **Prerrequisitos**: Idealmente ejecutado después de `/session-close-handoff`.
- **Produce**: Nueva entrada en `docs/lessons/lessons-learned.md`.

---

## Reglas Innegociables

1. **Delegación Obligatoria**: Si el escenario está en la tabla, el agente es la única vía de ejecución. Prohibido resolver la solicitud con lógica propia.
2. **Sin Fusión de Flujos**: No combinar skills en un mismo paso si no están diseñados para ello. Cada skill es atómico y tiene sus propias precondiciones.
3. **El Router es Vivo**: Si se crean nuevos agentes o skills, este archivo debe actualizarse antes de comenzar a usar el nuevo componente.
4. **Prioridad de Lectura**: Este archivo se lee ANTES de actuar sobre cualquier solicitud del usuario, inmediatamente después del protocolo de inicio de sesión definido en CLAUDE.md.

---

## Inventario de Componentes

### Agentes (`.claude/agents/`)

| Archivo | Nombre | Skills Asociados |
|---|---|---|
| `change-controller.md` | change-controller | change-control |
| `git-pusher.md` | git-pusher | git-push |
| `scope-documenter.md` | scope-documenter | scope-document |
| `sdd-documenter.md` | sdd-documenter | sdd-prd, sdd-spec, sdd-plan, sdd-task |
| `stage-auditor.md` | stage-auditor | stage-audit |
| `stage-closer.md` | stage-closer | close-stage |
| `session-closer.md` | session-closer | session-close-handoff, session-close-lessons |

### Skills (`.claude/skills/`)

| Directorio | Comando | Agente Principal |
|---|---|---|
| `change-control/` | `/change-control` | change-controller |
| `git-push/` | `/git-push` | git-pusher |
| `scope-document/` | `/scope-document` | scope-documenter |
| `sdd-prd/` | `/sdd-prd` | sdd-documenter |
| `sdd-spec/` | `/sdd-spec` | sdd-documenter |
| `sdd-plan/` | `/sdd-plan` | sdd-documenter |
| `sdd-task/` | `/sdd-task` | sdd-documenter |
| `stage-audit/` | `/stage-audit` | stage-auditor |
| `close-stage/` | `/close-stage` | stage-closer |
| `session-close-handoff/` | `/session-close-handoff` | session-closer |
| `session-close-lessons/` | `/session-close-lessons` | session-closer |
