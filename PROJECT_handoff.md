# PROJECT_handoff — Estado del Proyecto

> Última actualización: 2026-03-27 COT
> Sesión: #2
> Etapa activa: f01_02 — Validación de Infraestructura

> **MANDATO IA:** Este es el unico archivo de estado del proyecto. Leelo PRIMERO al iniciar cada sesion — contiene el estado macro (fases, hitos, arquitectura, decisiones historicas) y el estado tactico de la ultima sesion (que se hizo, bloqueadores, proxima accion).

---

## 1. Coordenadas Actuales

- **Fase Activa:** `Fase 1 — Gobernanza y Cimientos`
- **Etapa Activa:** `Etapa 1.2 — Validacion de Infraestructura`
- **Capa Medallon Activa:** `N/A`
- **Progreso Global:** 7.7% (1/13 etapas completadas — `docs/executives/f01_01_executive.md` existe)
- **Documentos SDD Gobernantes** *(leer antes de decisiones arquitectonicas)*:
  - PRD:    `docs/reqs/f01_02_prd.md` [Pendiente — debe crearse al iniciar f01_02]
  - SPEC:   `docs/specs/f01_02_spec.md` [Pendiente]
  - Plan:   `docs/plans/f01_02_plan.md` [Pendiente]
  - Tareas: `docs/tasks/f01_02_task.md` [Pendiente]

---

## 2. Hitos del Proyecto

### Fase 1 — Gobernanza y Cimientos

- [x] **Etapa 1.1** — Constitucion del Proyecto *(CERRADA — 2026-03-27)*
- [ ] **Etapa 1.2** — Validacion de infraestructura: tablas Supabase, triggers, indices, permisos y conectividad *(ACTIVA)*
- [ ] **Etapa 1.3** — Data Contract: especificacion formal, validaciones y protocolo de rechazo

### Fase 2 — Prototipado y Validacion de Diseno

- [ ] **Etapa 2.1** — Mockup Interactivo: prototipo navegable con datos ficticios para validacion con el cliente

### Fase 3 — Ingenieria de Datos, Integracion y Analitica

- [ ] **Etapa 3.1** — Pipeline de validacion: verificar que datos entrantes cumplen el Data Contract
- [ ] **Etapa 3.2** — ETL Bronze a Silver: ingestion, limpieza, conversion UTC a COT
- [ ] **Etapa 3.3** — Capa Gold: consumo diario, rotacion, clasificacion ABC semanal, margenes
- [ ] **Etapa 3.4** — EDA: patrones de venta, estacionalidad por ciudad/categoria y sede
- [ ] **Etapa 3.5** — Motor de alertas: 12 reglas (6 negativas + 6 positivas) con umbrales calibrados
- [ ] **Etapa 3.6** — Dashboard MVP: ventas, inventarios, ABC, alertas (Next.js + Tailwind)

### Fase 4 — Operacion y Mejora Continua

- [ ] **Etapa 4.1** — Publicacion en produccion: deploy, monitoreo y disponibilidad
- [ ] **Etapa 4.2** — Reporteria avanzada: comparativas inter-sede e inter-categoria
- [ ] **Etapa 4.3** — Mejora continua: feedback del cliente, ajuste de umbrales y nuevas metricas

---

## 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| Repositorio Git + Estructura base | Raiz del repositorio | Existe |
| `.gitignore` | `.gitignore` | Existe |
| Carpetas base (19 carpetas) | `pipeline/`, `web/`, `docs/`, `.claude/` | Existe |
| Pipeline placeholder | `pipeline/main.py` | Existe |
| Ley del proyecto (IA) | `CLAUDE.md` | Existe |
| Alcance del proyecto | `PROJECT_scope.md` | Existe |
| Arquitectura de referencia | `docs/references/architecture.md` | Existe |
| Stack tecnologico | `docs/references/tech-stack.md` | Existe |
| Comandos de desarrollo | `docs/references/dev-commands.md` | Existe |
| Protocolo de incidentes | `docs/references/incident-protocol.md` | Existe |
| Glosario | `docs/references/glossary.md` | Existe |
| Decisiones Arquitectonicas (ADR) | `docs/references/adr.md` | Existe |
| Lecciones aprendidas | `docs/lessons/lessons-learned.md` | Existe |
| Skill router | `.claude/skill-router.md` | Existe |
| Resumen Ejecutivo Etapa 1.1 | `docs/executives/f01_01_executive.md` | Existe (cierre formal) |
| Estado del proyecto (este archivo) | `PROJECT_handoff.md` | Activo |
| Esquema Supabase | `docs/database/schema.sql` | Pendiente — objetivo de Etapa 1.2 |

---

## 4. Indice SDD

### Etapa Cerrada — Fase 1.1

| Documento | Ruta | Estado |
|---|---|---|
| PRD Etapa 1.1 | `docs/reqs/f01_01_prd.md` | Cerrado |
| SPEC Etapa 1.1 | `docs/specs/f01_01_spec.md` | Cerrado |
| Plan Etapa 1.1 | `docs/plans/f01_01_plan.md` | Cerrado |
| Tasks Etapa 1.1 | `docs/tasks/f01_01_task.md` | Cerrado (25/25 completadas) |
| Executive Etapa 1.1 | `docs/executives/f01_01_executive.md` | Existe — cierre formal 2026-03-27 |

### Etapa Activa — Fase 1.2

| Documento | Ruta | Estado |
|---|---|---|
| PRD Etapa 1.2 | `docs/reqs/f01_02_prd.md` | Pendiente |
| SPEC Etapa 1.2 | `docs/specs/f01_02_spec.md` | Pendiente |
| Plan Etapa 1.2 | `docs/plans/f01_02_plan.md` | Pendiente |
| Tasks Etapa 1.2 | `docs/tasks/f01_02_task.md` | Pendiente |
| Executive Etapa 1.2 | `docs/executives/f01_02_executive.md` | Pendiente |

---

## 5. Notas y Decisiones Registradas

- **2026-03-27** — Sesion #1: cadena SDD completa (PRD, SPEC, Plan, Tasks) redactada para la Etapa 1.1. Los bloques B1-B6 completados antes de esta sesion, B7-B9 completados durante la sesion.
- **2026-03-27** — Patron de trabajo con sdd-documenter validado: agente genera contenido markdown completo → orquestador escribe los archivos. El agente sdd-documenter no tiene herramienta Write; este es el flujo correcto.
- **2026-03-27** — La SPEC de la Etapa 1.1 es de tipo DOCUMENTACION pura (sin esquemas Pandera, sin tablas SQL). El skill /stage-audit adapta sus criterios a tipo DOCUMENTACION.
- **2026-03-27** — Sesion #2: Etapa 1.1 cerrada formalmente. Auditoria /stage-audit emitio token CONFORME. Resumen Ejecutivo generado con /close-stage. Progreso del proyecto: 7.7% (1/13 etapas).

---

## 6. Estado de Sesion

### Punto de Guardado

- **Ultima actualizacion:** 2026-03-27, cierre de Sesion #2
- **Fase / Etapa:** `Fase 1 — Etapa 1.2 (recien habilitada)`

### Archivos en el Escritorio (Working Set)

- `docs/executives/f01_01_executive.md` — Resumen Ejecutivo de la Etapa 1.1 creado en esta sesion. Artefacto de cierre formal.
- `PROJECT_handoff.md` — Este archivo, actualizado para reflejar el cierre de f01_01 y la apertura de f01_02.

### Contexto Inmediato

La Etapa 1.1 fue cerrada formalmente con el proceso completo: auditoría (/stage-audit obtuvo token CONFORME), cierre (/close-stage generó el ejecutivo). El gate de avance está satisfecho: `docs/executives/f01_01_executive.md` existe. La Etapa 1.2 está habilitada para iniciar.

Para iniciar la Etapa 1.2 se debe crear primero la cadena SDD: PRD → SPEC → Plan → Tasks. El trabajo técnico de f01_02 consiste en verificar las tablas de Supabase del cliente (`usr_*`), configurar los permisos de acceso, probar la conectividad y documentar el esquema inicial en `docs/database/schema.sql`.

### Bloqueador / Ultimo Error

Ninguno. El proyecto avanza en estado limpio.

### Proxima Accion Inmediata

1. Solicitar al usuario confirmacion para iniciar la Etapa 1.2.
2. Crear `docs/reqs/f01_02_prd.md` usando `/sdd-prd` — requerimientos para validacion de infraestructura Supabase.
3. Completar la cadena SDD f01_02: PRD → SPEC → Plan → Tasks.
4. Prerequisito externo: el equipo debe tener credenciales de Supabase (URL del proyecto, service role key) antes de ejecutar las tareas de conectividad.
