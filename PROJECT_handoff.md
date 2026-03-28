# PROJECT_handoff — Estado del Proyecto

> **MANDATO IA:** Este es el unico archivo de estado del proyecto. Leelo PRIMERO al iniciar cada sesion — contiene el estado macro (fases, hitos, arquitectura, decisiones historicas) y el estado tactico de la ultima sesion (que se hizo, bloqueadores, proxima accion).

---

## 1. Coordenadas Actuales

- **Fase Activa:** `Fase 1 — Gobernanza y Cimientos`
- **Etapa Activa:** `Etapa 1.2 — Validacion de Infraestructura`
- **Capa Medallon Activa:** `N/A`
- **Progreso Global:** 7.7% (1/13 etapas completadas — `docs/executives/f01_01_executive.md` existe)
- **Documentos SDD Gobernantes** *(leer antes de decisiones arquitectonicas)*:
  - PRD:    `docs/reqs/f01_02_prd.md` [Existe]
  - SPEC:   `docs/specs/f01_02_spec.md` [Existe]
  - Plan:   `docs/plans/f01_02_plan.md` [Existe]
  - Tareas: `docs/tasks/f01_02_task.md` [Existe] (0/17 completadas)

---

## 2. Hitos del Proyecto

### Fase 1 — Gobernanza y Cimientos

- [x] **Etapa 1.1** — Constitucion del Proyecto *(CERRADA — 2026-03-27)*
- [ ] **Etapa 1.2** — Validacion de infraestructura: tablas Supabase, triggers, indices, permisos y conectividad *(ACTIVA — documentacion 100%, implementacion 0%)*
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
| Agente db-manager | `.claude/agents/db-manager.md` | Existe — creado en sesion #3 |
| Skill db-management | `.claude/skills/db-management/SKILL.md` | Existe — creado en sesion #3 |
| Resumen Ejecutivo Etapa 1.1 | `docs/executives/f01_01_executive.md` | Existe (cierre formal) |
| Estado del proyecto (este archivo) | `PROJECT_handoff.md` | Activo |
| Esquema Supabase | `docs/database/schema.sql` | Pendiente — objetivo de Etapa 1.2 |
| Ambiente virtual Python | `pipeline/.venv` | Pendiente — TSK-2-01 |
| Variables de entorno pipeline | `pipeline/.env` | Pendiente — requiere credenciales cliente |

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
| PRD Etapa 1.2 | `docs/reqs/f01_02_prd.md` | Existe (5 OBJ, 13 REQ, 6 DAT, 7 MET, 6 RSK) |
| SPEC Etapa 1.2 | `docs/specs/f01_02_spec.md` | Existe (6 componentes ARC, DDL 10 tablas tss_*) |
| Plan Etapa 1.2 | `docs/plans/f01_02_plan.md` | Existe (5 bloques B1-B5, ruta critica 6 dias) |
| Tasks Etapa 1.2 | `docs/tasks/f01_02_task.md` | Existe (17 tareas TSK-2-01 a TSK-2-17, 0 completadas) |
| Executive Etapa 1.2 | `docs/executives/f01_02_executive.md` | Pendiente |

---

## 5. Notas y Decisiones Registradas

- **2026-03-27** — Sesion #1: cadena SDD completa (PRD, SPEC, Plan, Tasks) redactada para la Etapa 1.1. Los bloques B1-B6 completados antes de esta sesion, B7-B9 completados durante la sesion.
- **2026-03-27** — Patron de trabajo con sdd-documenter validado: agente genera contenido markdown completo → orquestador escribe los archivos. El agente sdd-documenter no tiene herramienta Write; este es el flujo correcto.
- **2026-03-27** — La SPEC de la Etapa 1.1 es de tipo DOCUMENTACION pura (sin esquemas Pandera, sin tablas SQL). El skill /stage-audit adapta sus criterios a tipo DOCUMENTACION.
- **2026-03-27** — Sesion #2: Etapa 1.1 cerrada formalmente. Auditoria /stage-audit emitio token CONFORME. Resumen Ejecutivo generado con /close-stage. Progreso del proyecto: 7.7% (1/13 etapas).
- **2026-03-28** — Sesion #3: Cadena SDD completa de Etapa 1.2 redactada en esta sesion. PRD con 5 OBJ y 13 REQ, SPEC con DDL de 10 tablas tss_* y diseno de suite pytest, Plan con 5 bloques y ruta critica 6 dias, Tasks con 17 tareas atomicas TSK-2-01 a TSK-2-17.
- **2026-03-28** — Agente db-manager y skill db-management creados. El agente db-manager es el unico autorizado para operaciones de BD. 7 operaciones definidas: OP-INTRO, OP-DDL, OP-RLS, OP-IDX, OP-CONN, OP-CUAR, OP-AUDIT.
- **2026-03-28** — Credenciales Supabase: SUPABASE_URL y SUPABASE_SERVICE_KEY van en `pipeline/.env`. El Personal Access Token de Supabase (distinto al SERVICE_KEY) es necesario para el MCP — su configuracion es TSK-2-15, no un prerequisito de sesion.
- **2026-03-28** — MCP de Supabase es el canal preferido para introspeccion de BD una vez configurado. El agente db-manager lo usara post-configuracion. Mientras no este configurado, se opera via psycopg2 o supabase-py con SERVICE_KEY.
- **2026-03-28** — Planes futuros registrados (pendientes de ejecucion): crear agentes pipeline-tester, pipeline-coder, pipeline-reviewer (item 5 de ajustes.txt); crear agentes web-tester, web-coder, web-reviewer (item 6); crear agente code-debugger (item 8).

---

## 6. Estado de Sesion

### Punto de Guardado

- **Ultima actualizacion:** 2026-03-28, cierre de Sesion #3
- **Fase / Etapa:** `Fase 1 — Etapa 1.2 (documentacion completa, implementacion pendiente)`

### Archivos en el Escritorio (Working Set)

- `docs/reqs/f01_02_prd.md` — PRD creado en esta sesion. 5 OBJ, 13 REQ, 6 DAT, 7 MET, 6 RSK.
- `docs/specs/f01_02_spec.md` — SPEC creada en esta sesion. DDL de 10 tablas tss_*, diseno suite pytest, 6 componentes arquitectonicos.
- `docs/plans/f01_02_plan.md` — Plan creado en esta sesion. 5 bloques B1-B5, ruta critica 6 dias.
- `docs/tasks/f01_02_task.md` — Task list creada en esta sesion. 17 tareas TSK-2-01 a TSK-2-17, ninguna completada.
- `.claude/agents/db-manager.md` — Agente especialista en Supabase creado en esta sesion.
- `.claude/skills/db-management/SKILL.md` — Skill con 7 operaciones de BD creado en esta sesion.

### Contexto Inmediato

La cadena SDD de la Etapa 1.2 esta 100% redactada. El ecosistema de agentes de BD (db-manager + skill db-management) fue creado y registrado en el skill-router. La implementacion tecnica aun no inicio: ninguna tarea TSK-2-* ha sido ejecutada. El bloqueador actual es la ausencia de credenciales de Supabase en `pipeline/.env`.

La primera tarea ejecutable es TSK-2-01 (crear .venv en pipeline/ e instalar dependencias: supabase-py, psycopg2-binary, python-dotenv, pytest, pandera). Esta tarea puede ejecutarse sin credenciales. La segunda tarea TSK-2-02 (verificar conectividad) si requiere SUPABASE_URL y SUPABASE_SERVICE_KEY.

### Bloqueador / Ultimo Error

Credenciales pendientes: SUPABASE_URL y SUPABASE_SERVICE_KEY del proyecto Supabase del cliente no han sido entregadas ni configuradas en `pipeline/.env`. Sin ellas, las tareas de conectividad (TSK-2-02 en adelante) no pueden ejecutarse.

### Proxima Accion Inmediata

1. Solicitar al usuario que entregue SUPABASE_URL y SUPABASE_SERVICE_KEY para configurar `pipeline/.env`.
2. Ejecutar TSK-2-01: crear `pipeline/.venv` y instalar dependencias (supabase-py, psycopg2-binary, python-dotenv, pytest, pandera) via `cd pipeline && python -m venv .venv && .venv/Scripts/activate && pip install -r requirements.txt`.
3. Con credenciales disponibles, ejecutar TSK-2-02: probar conectividad Supabase y documentar resultado en log.
