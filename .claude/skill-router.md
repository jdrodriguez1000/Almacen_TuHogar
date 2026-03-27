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
