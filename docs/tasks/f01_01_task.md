# Lista de Tareas — Constitución del Proyecto (`f01_01`)

> Documento: `docs/tasks/f01_01_task.md`
> Versión: 1.0
> Fecha: 2026-03-27
> Estado: En ejecución
> Elaborado por: Triple S (Sabbia Solutions & Services)
> Trazabilidad: Estas tareas implementan `docs/plans/f01_01_plan.md`.
> Actualiza marcando `[x]` al completar. **NUNCA borres tareas completadas.**

---

## Convenciones de Anotación

- **`(independiente)`** — Sin dependencias, puede iniciar de inmediato.
- **`(depends_on: TSK-1-XX)`** — Espera a que `TSK-1-XX` esté completa.
- **`(parallel_with: TSK-1-XX)`** — Puede ejecutarse simultáneamente con `TSK-1-XX`.

---

## Mapa de Dependencias

```
SECUENCIAL COMPLETO (sin paralelismo — cada artefacto presupone el anterior):

  TSK-1-01 → Inicializar repositorio Git con rama main
  TSK-1-02 → Crear .gitignore conforme a SPEC § 2.1       ← depends_on: TSK-1-01
  TSK-1-03 → Crear estructura de 19 carpetas con .gitkeep  ← depends_on: TSK-1-01
  TSK-1-04 → Crear pipeline/main.py (placeholder)          ← depends_on: TSK-1-03
  TSK-1-05 → Redactar CLAUDE.md con 19 secciones           ← depends_on: TSK-1-01
  TSK-1-06 → Redactar PROJECT_scope.md con 11 secciones    ← depends_on: TSK-1-05
  TSK-1-07 → Verificar estado Aprobado en PROJECT_scope.md ← depends_on: TSK-1-06
  TSK-1-08 → Crear docs/references/architecture.md         ← depends_on: TSK-1-05
  TSK-1-09 → Crear docs/references/tech-stack.md           ← parallel_with: TSK-1-08
  TSK-1-10 → Crear docs/references/dev-commands.md         ← parallel_with: TSK-1-08
  TSK-1-11 → Crear docs/references/incident-protocol.md    ← parallel_with: TSK-1-08
  TSK-1-12 → Crear docs/references/glossary.md             ← parallel_with: TSK-1-08
  TSK-1-13 → Crear docs/references/adr.md                  ← parallel_with: TSK-1-08
  TSK-1-14 → Inicializar docs/lessons/lessons-learned.md   ← depends_on: TSK-1-05
  TSK-1-15 → Crear .claude/skill-router.md                 ← depends_on: TSK-1-05
  TSK-1-16 → Crear docs/reqs/f01_01_prd.md                 ← depends_on: TSK-1-06, TSK-1-15
  TSK-1-17 → Crear docs/specs/f01_01_spec.md               ← depends_on: TSK-1-16
  TSK-1-18 → Crear docs/plans/f01_01_plan.md               ← depends_on: TSK-1-16, TSK-1-17
  TSK-1-19 → Crear PROJECT_handoff.md con 7 secciones      ← depends_on: TSK-1-18
  TSK-1-20 → Crear docs/tasks/f01_01_task.md (este doc)    ← depends_on: TSK-1-18, TSK-1-19
  TSK-1-21 → Verificar estructura completa (ls / find)     ← depends_on: TSK-1-20
  TSK-1-22 → Verificar contenido mínimo de cada documento  ← parallel_with: TSK-1-21
  TSK-1-23 → Ejecutar commit de cierre SDD en main         ← depends_on: TSK-1-21, TSK-1-22
  TSK-1-24 → Ejecutar /stage-audit f01_01                  ← depends_on: TSK-1-23
  TSK-1-25 → Ejecutar /close-stage f01_01                  ← depends_on: TSK-1-24
```

---

## Bloque 1 — Repositorio Git + Estructura + `.gitignore` (B1) ✅ COMPLETADO

- [x] `[TSK-1-01]` Inicializar repositorio Git con `git init` y configurar rama `main` como rama por defecto _(independiente)_
  - **REQ que implementa**: `[REQ-01]`
  - **Componente [ARC]**: `[ARC-01]`
  - **Archivos**: Raíz del repositorio (`.git/`)
  - **DoD**: `git branch` muestra `* main`; `git status` muestra estado de repositorio vacío inicializado.

- [x] `[TSK-1-02]` Crear `.gitignore` en la raíz con los bloques exactos especificados en SPEC § 2.1 (Python, secretos, Next.js, DVC, SO, IDEs, logs) _(depends_on: TSK-1-01)_
  - **REQ que implementa**: `[REQ-01]`, `[REQ-08]`
  - **Componente [ARC]**: `[ARC-01]`
  - **Archivos**: `.gitignore`
  - **DoD**: Archivo presente en raíz; contiene los 7 bloques de sección con comentarios; `.venv/` y `.env` están en las exclusiones.

- [x] `[TSK-1-03]` Crear las 19 carpetas de la estructura base del repositorio, cada una con un archivo `.gitkeep` vacío _(depends_on: TSK-1-01)_
  - **REQ que implementa**: `[REQ-05]`
  - **Componente [ARC]**: `[ARC-01]`
  - **Archivos**: `pipeline/`, `pipeline/pipelines/`, `pipeline/src/`, `pipeline/tests/`, `web/`, `web/components/`, `web/app/`, `web/tests/`, `docs/`, `docs/reqs/`, `docs/specs/`, `docs/plans/`, `docs/tasks/`, `docs/database/`, `docs/lessons/`, `docs/executives/`, `docs/changes/`, `docs/references/`, `.claude/`
  - **DoD**: `find . -type d` muestra las 19 carpetas; cada una contiene `.gitkeep` o un archivo que la hace trackeable por Git.

- [x] `[TSK-1-04]` Crear `pipeline/main.py` como archivo placeholder con comentario de encabezado (sin lógica de producto) _(depends_on: TSK-1-03)_
  - **REQ que implementa**: `[REQ-05]`
  - **Componente [ARC]**: `[ARC-01]`
  - **Archivos**: `pipeline/main.py`
  - **DoD**: Archivo existe; contiene únicamente un comentario que describe su propósito futuro como gateway/switcher del pipeline; no contiene ninguna línea de código ejecutable.

---

## Bloque 2 — `CLAUDE.md` (B2) ✅ COMPLETADO

- [x] `[TSK-1-05]` Redactar `CLAUDE.md` en la raíz con las 19 secciones obligatorias definidas en SPEC § 2.2 y la cabecera estándar de Triple S _(depends_on: TSK-1-01)_
  - **REQ que implementa**: `[REQ-02]`
  - **Componente [ARC]**: `[ARC-02]`
  - **Archivos**: `CLAUDE.md`
  - **DoD**: Archivo presente en raíz; contiene las 19 secciones `##` en el orden especificado; cabecera incluye referencia a Triple S.

---

## Bloque 3 — `PROJECT_scope.md` (B3) ✅ COMPLETADO

- [x] `[TSK-1-06]` Redactar `PROJECT_scope.md` con las 11 secciones obligatorias definidas en SPEC § 2.3 _(depends_on: TSK-1-05)_
  - **REQ que implementa**: `[REQ-03]`
  - **Componente [ARC]**: `[ARC-03]`
  - **Archivos**: `PROJECT_scope.md`
  - **DoD**: Archivo presente en raíz; contiene las 11 secciones numeradas en orden; cubre cliente (Almacén MultiTodo, 7 sedes, ~100 SKUs), deadline (3 meses) y presupuesto (USD $10,000).

- [x] `[TSK-1-07]` Verificar que `PROJECT_scope.md` contiene `Estado: ✅ Aprobado` en la cabecera de metadatos _(depends_on: TSK-1-06)_
  - **REQ que implementa**: `[REQ-03]`
  - **Componente [ARC]**: `[ARC-03]`
  - **Archivos**: `PROJECT_scope.md`
  - **DoD**: `grep "Estado" PROJECT_scope.md` devuelve línea con exactamente `✅ Aprobado`.

---

## Bloque 4 — Artefactos de Soporte (References + Lessons + Skill-Router) (B4) ✅ COMPLETADO

- [x] `[TSK-1-08]` Crear `docs/references/architecture.md` con las 4 secciones obligatorias: Flujo de Datos General, Arquitectura Medallion, Ciclo Diario de Operación y Componentes del Sistema _(depends_on: TSK-1-05)_
  - **REQ que implementa**: `[REQ-08]`
  - **Componente [ARC]**: `[ARC-07]`
  - **Archivos**: `docs/references/architecture.md`
  - **DoD**: Archivo presente; diagrama ASCII muestra `usr_*` → Bronze → Silver → Gold → API Routes → Dashboard.

- [x] `[TSK-1-09]` Crear `docs/references/tech-stack.md` con Stack por Capa, Variables de Entorno, Entornos e Instalación Inicial _(parallel_with: TSK-1-08)_
  - **REQ que implementa**: `[REQ-08]`
  - **Componente [ARC]**: `[ARC-07]`
  - **Archivos**: `docs/references/tech-stack.md`
  - **DoD**: Archivo presente; tabla de stack cubre 4 capas; variables de entorno sin valores reales.

- [x] `[TSK-1-10]` Crear `docs/references/dev-commands.md` con las 7 secciones obligatorias _(parallel_with: TSK-1-08)_
  - **REQ que implementa**: `[REQ-08]`
  - **Componente [ARC]**: `[ARC-07]`
  - **Archivos**: `docs/references/dev-commands.md`
  - **DoD**: Archivo presente; los 3 modos del pipeline (`validate`, `etl`, `alerts`) están documentados.

- [x] `[TSK-1-11]` Crear `docs/references/incident-protocol.md` con tabla P1-P4, protocolo por severidad y tabla `ERR_MTD_XXX` _(parallel_with: TSK-1-08)_
  - **REQ que implementa**: `[REQ-08]`
  - **Componente [ARC]**: `[ARC-07]`
  - **Archivos**: `docs/references/incident-protocol.md`
  - **DoD**: Archivo presente; los 5 códigos `ERR_MTD_001` a `ERR_MTD_005` están definidos.

- [x] `[TSK-1-12]` Crear `docs/references/glossary.md` con los términos mínimos: T-1, T+0, COT, Bronze/Silver/Gold, Data Contract, cuarentena, ERR_MTD_001-005, `usr_*`, `tss_*`, SDD, `feat/*` _(parallel_with: TSK-1-08)_
  - **REQ que implementa**: `[REQ-08]`
  - **Componente [ARC]**: `[ARC-07]`
  - **Archivos**: `docs/references/glossary.md`
  - **DoD**: Archivo presente; COT definido como `America/Bogota, UTC-5`.

- [x] `[TSK-1-13]` Crear `docs/references/adr.md` con los 5 ADRs mínimos (ADR-001: Medallion, ADR-002: Supabase, ADR-003: Next.js 14, ADR-004: T-1, ADR-005: TDD) _(parallel_with: TSK-1-08)_
  - **REQ que implementa**: `[REQ-08]`
  - **Componente [ARC]**: `[ARC-07]`
  - **Archivos**: `docs/references/adr.md`
  - **DoD**: Archivo presente; cada ADR contiene los 5 campos obligatorios.

- [x] `[TSK-1-14]` Inicializar `docs/lessons/lessons-learned.md` con la sección `## Etapa 1.1` y sus 4 subsecciones obligatorias _(depends_on: TSK-1-05)_
  - **REQ que implementa**: `[REQ-06]`
  - **Componente [ARC]**: `[ARC-05]`
  - **Archivos**: `docs/lessons/lessons-learned.md`
  - **DoD**: Archivo presente; sección Etapa 1.1 tiene las 4 subsecciones `###`; subsecciones vacías marcadas con `[Vacío]`.

- [x] `[TSK-1-15]` Crear `.claude/skill-router.md` con la tabla de routing y el catálogo de los 12 skills mínimos _(depends_on: TSK-1-05)_
  - **REQ que implementa**: `[REQ-07]`
  - **Componente [ARC]**: `[ARC-06]`
  - **Archivos**: `.claude/skill-router.md`
  - **DoD**: Archivo presente; tabla de routing cubre los 12 skills con descripción, disparadores, prerrequisitos y artefacto de salida.

---

## Bloque 5 — PRD + SPEC de la Etapa (B5) ✅ COMPLETADO

- [x] `[TSK-1-16]` Crear `docs/reqs/f01_01_prd.md` con los 9 requerimientos, 4 objetivos, 5 métricas, 4 riesgos y matriz de trazabilidad _(depends_on: TSK-1-06, TSK-1-15)_
  - **REQ que implementa**: Prerrequisito documental SDD
  - **Componente [ARC]**: Cadena SDD interna
  - **Archivos**: `docs/reqs/f01_01_prd.md`
  - **DoD**: Archivo presente con estado `✅ Aprobado`.

- [x] `[TSK-1-17]` Crear `docs/specs/f01_01_spec.md` con los 8 componentes `[ARC-01]` a `[ARC-08]` y matriz de trazabilidad SPEC vs PRD _(depends_on: TSK-1-16)_
  - **REQ que implementa**: Prerrequisito documental SDD
  - **Componente [ARC]**: Cadena SDD interna
  - **Archivos**: `docs/specs/f01_01_spec.md`
  - **DoD**: Archivo presente con estado `✅ Aprobado`.

---

## Bloque 6 — Plan de Implementación (B6) ✅ COMPLETADO

- [x] `[TSK-1-18]` Crear `docs/plans/f01_01_plan.md` con ruta crítica B1-B9, WBS completo, estrategia de pruebas y DoD de la etapa _(depends_on: TSK-1-16, TSK-1-17)_
  - **REQ que implementa**: Prerrequisito documental SDD
  - **Componente [ARC]**: Cadena SDD interna
  - **Archivos**: `docs/plans/f01_01_plan.md`
  - **DoD**: Archivo presente con estado `✅ Aprobado`.

---

## Bloque 7 — `PROJECT_handoff.md` (B7) ✅ COMPLETADO

- [x] `[TSK-1-19]` Crear `PROJECT_handoff.md` en la raíz con las 7 secciones obligatorias definidas en SPEC § 2.4 _(depends_on: TSK-1-18)_
  - **REQ que implementa**: `[REQ-04]`
  - **Componente [ARC]**: `[ARC-04]`
  - **Archivos**: `PROJECT_handoff.md`
  - **DoD**: Archivo presente en raíz; cabecera contiene `Última actualización`, número de sesión y `Etapa activa: f01_01`; sección "Próxima Acción Concreta" apunta al paso correcto; las 7 secciones están presentes.

---

## Bloque 8 — Task List (B8) ✅ COMPLETADO

- [x] `[TSK-1-20]` Crear `docs/tasks/f01_01_task.md` con el checklist completo marcando `[x]` las completadas y `[ ]` las pendientes _(depends_on: TSK-1-18, TSK-1-19)_
  - **REQ que implementa**: Prerrequisito para `/stage-audit` y `/close-stage`
  - **Componente [ARC]**: Cadena SDD interna
  - **Archivos**: `docs/tasks/f01_01_task.md`
  - **DoD**: Archivo presente; mapa de dependencias completo; tareas B1-B6 marcadas `[x]`; anotaciones de dependencia explícitas en cada tarea.

---

## Bloque 9 — Verificación y Commit de Cierre SDD (B9)

- [x] `[TSK-1-21]` Verificar existencia y estructura de todos los artefactos: `ls` sobre cada ruta listada en SPEC § 2.8 y confirmar las 19 carpetas _(depends_on: TSK-1-20)_
  - **REQ que implementa**: `[MET-01]`, `[MET-02]`
  - **Componente [ARC]**: Verificación de `[ARC-01]` a `[ARC-08]`
  - **DoD**: Ningún archivo retorna error de ruta; `find . -type d` muestra las 19 carpetas requeridas.

- [x] `[TSK-1-22]` Verificar contenido mínimo de cada documento: secciones obligatorias, estado de aprobación en `PROJECT_scope.md` y cabeceras de metadatos _(parallel_with: TSK-1-21)_
  - **REQ que implementa**: `[MET-01]`, `[MET-04]`, `[MET-05]`
  - **Componente [ARC]**: Verificación de `[ARC-02]` a `[ARC-07]`
  - **DoD**: `grep "Estado" PROJECT_scope.md` retorna `✅ Aprobado`; `skill-router.md` tiene los 12 skills.

- [ ] `[TSK-1-23]` Ejecutar commit de cierre SDD en `main` con todos los documentos SDD de la etapa y `PROJECT_handoff.md` usando `/git-push` _(depends_on: TSK-1-21, TSK-1-22)_
  - **REQ que implementa**: `[REQ-09]`
  - **Componente [ARC]**: `[ARC-08]`
  - **DoD**: `git status` devuelve `nothing to commit, working tree clean`; los 4 documentos SDD + handoff están en `main`.

---

## Cierre de Etapa — Auditoría y Cierre Formal

- [ ] `[TSK-1-24]` Ejecutar `/stage-audit f01_01` para verificar conformidad documental completa antes del cierre formal _(depends_on: TSK-1-23)_
  - **REQ que implementa**: `[MET-01]`, `[MET-02]`, `[MET-03]`
  - **DoD**: Skill reporta 0 gaps críticos; si hay gaps, resolverlos antes de proceder.

- [ ] `[TSK-1-25]` Ejecutar `/close-stage f01_01` para generar `docs/executives/f01_01_executive.md` y cerrar formalmente la Etapa 1.1 _(depends_on: TSK-1-24)_
  - **REQ que implementa**: Gate obligatorio para avanzar a Etapa 1.2
  - **Archivos**: `docs/executives/f01_01_executive.md`
  - **DoD**: Archivo existe; habilita el inicio de la Etapa 1.2 según `CLAUDE.md` § Límites de Autonomía.

---

## Resumen de Estado

| Bloque | Descripción | Tareas | Estado |
|---|---|---|---|
| B1 | Repositorio Git + Estructura + `.gitignore` | TSK-1-01 a TSK-1-04 | ✅ Completado |
| B2 | `CLAUDE.md` | TSK-1-05 | ✅ Completado |
| B3 | `PROJECT_scope.md` | TSK-1-06, TSK-1-07 | ✅ Completado |
| B4 | References + Lessons + Skill-Router | TSK-1-08 a TSK-1-15 | ✅ Completado |
| B5 | PRD + SPEC de la etapa | TSK-1-16, TSK-1-17 | ✅ Completado |
| B6 | Plan de Implementación | TSK-1-18 | ✅ Completado |
| B7 | `PROJECT_handoff.md` | TSK-1-19 | Pendiente |
| B8 | Task List | TSK-1-20 | Pendiente |
| B9 | Verificación + Commit de cierre SDD | TSK-1-21 a TSK-1-23 | Pendiente |
| Cierre | Auditoría + Cierre Formal | TSK-1-24, TSK-1-25 | Pendiente |

**Progreso**: 17 de 25 tareas completadas (68%)

---

## Matriz de Trazabilidad: Tareas vs Plan vs PRD

| TSK | Bloque Plan | REQ / MET | Componente [ARC] |
|---|---|---|---|
| TSK-1-01 | B1 | `[REQ-01]` | `[ARC-01]` |
| TSK-1-02 | B1 | `[REQ-01]`, `[REQ-08]` | `[ARC-01]` |
| TSK-1-03 | B1 | `[REQ-05]` | `[ARC-01]` |
| TSK-1-04 | B1 | `[REQ-05]` | `[ARC-01]` |
| TSK-1-05 | B2 | `[REQ-02]` | `[ARC-02]` |
| TSK-1-06 | B3 | `[REQ-03]` | `[ARC-03]` |
| TSK-1-07 | B3 | `[REQ-03]`, `[MET-04]` | `[ARC-03]` |
| TSK-1-08 | B4 | `[REQ-08]` | `[ARC-07]` |
| TSK-1-09 | B4 | `[REQ-08]` | `[ARC-07]` |
| TSK-1-10 | B4 | `[REQ-08]` | `[ARC-07]` |
| TSK-1-11 | B4 | `[REQ-08]` | `[ARC-07]` |
| TSK-1-12 | B4 | `[REQ-08]` | `[ARC-07]` |
| TSK-1-13 | B4 | `[REQ-08]` | `[ARC-07]` |
| TSK-1-14 | B4 | `[REQ-06]` | `[ARC-05]` |
| TSK-1-15 | B4 | `[REQ-07]` | `[ARC-06]` |
| TSK-1-16 | B5 | PRD (autodocumental) | Cadena SDD |
| TSK-1-17 | B5 | SPEC (autodocumental) | Cadena SDD |
| TSK-1-18 | B6 | Plan (autodocumental) | Cadena SDD |
| TSK-1-19 | B7 | `[REQ-04]` | `[ARC-04]` |
| TSK-1-20 | B8 | Task List (autodocumental) | Cadena SDD |
| TSK-1-21 | B9 | `[MET-01]`, `[MET-02]` | `[ARC-01]`–`[ARC-08]` |
| TSK-1-22 | B9 | `[MET-01]`, `[MET-04]`, `[MET-05]` | `[ARC-02]`–`[ARC-07]` |
| TSK-1-23 | B9 | `[REQ-09]`, `[MET-03]` | `[ARC-08]` |
| TSK-1-24 | Cierre | `[MET-01]`–`[MET-03]` | Todos |
| TSK-1-25 | Cierre | Gate de avance a Etapa 1.2 | `[ARC-08]` |
