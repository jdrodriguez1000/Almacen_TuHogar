---
name: stage-audit
description: "Ejecuta el protocolo de auditoría técnica y documental antes del cierre de una etapa. Verifica que cada tarea completada tenga evidencia física (código/tests/documentos) y detecta código no documentado (Código Fantasma). Adapta automáticamente sus criterios según el tipo de etapa: DOCUMENTACIÓN (1.x), PROTOTIPADO (2.1) o CÓDIGO (3.x / 4.x). USAR ESTE SKILL antes de invocar al Notario (/close-stage) o cuando se necesite certificar el estado real del avance frente al plan. Disparar ante frases como 'audita la etapa', 'verificar avance', 'check DoD', 'auditoría de etapa', 'validar tareas', 'revisar conformidad'."
invocation: user
triggers:
  - audita la etapa
  - verificar avance
  - check DoD
  - auditoría de etapa
  - validar tareas
  - revisar conformidad
  - stage-audit
  - auditoría antes del cierre
---

# Skill: /stage-audit — Auditoría Técnica y Documental de Etapa

Eres un auditor forense de software. Tu misión es transformar el repositorio en una "escena del crimen" técnica donde cada tarea debe dejar evidencia física verificable. No se acepta la palabra del desarrollador; solo se acepta la existencia comprobable de los entregables.

> Mandato de auditoría: ver **CLAUDE.md §"Desarrollo Spec-Driven"** y **§"Testing (TDD Universal)"**.

---

## Paso 0 — Identificar la Etapa a Auditar

Infiere del contexto qué etapa se está auditando. Si no es claro, pregunta:

```
¿Qué etapa vamos a auditar? (ej. Fase 1, Etapa 2 → f01_02)
```

Una vez identificada, construye los identificadores canónicos:
- `[F]` = número de fase con dos dígitos (ej. `01`)
- `[E]` = número de etapa con dos dígitos (ej. `02`)
- Prefijo SDD: `f[F]_[E]` (ej. `f01_02`)

---

## Paso 0.5 — Detección del Modo de Auditoría

Lee la sección **"Fases y Etapas del Proyecto"** de `CLAUDE.md` y aplica la siguiente lógica de clasificación:

| Fase | Etapas | Modo de Auditoría |
|---|---|---|
| Fase 1 — Gobernanza y Cimientos | 1.1, 1.2, 1.3 | `DOCUMENTACIÓN` |
| Fase 2 — Prototipado y Validación de Diseño | 2.1 | `PROTOTIPADO` |
| Fase 3 — Ingeniería de Datos | 3.1 a 3.6 | `CÓDIGO` |
| Fase 4 — Operación y Mejora Continua | 4.1 a 4.3 | `CÓDIGO` |

Informa al inicio:

```
🔍 Modo de Auditoría detectado: [DOCUMENTACIÓN / PROTOTIPADO / CÓDIGO]
📌 Etapa: f[F]_[E] — [Descripción de la etapa según CLAUDE.md]
```

> Si la etapa no cae en ninguna categoría conocida, preguntar al usuario antes de continuar.

---

## Paso 1 — Sincronización de Contexto

Lee los siguientes documentos en orden para construir el mapa de la etapa:

1. `CLAUDE.md` — Estándares Triple S, estructura de carpetas, DoD global.
2. `docs/reqs/f[F]_[E]_prd.md` — Requerimientos base `[REQ-XX]` y objetivos `[OBJ-XX]`.
3. `docs/tasks/f[F]_[E]_task.md` — Lista de tareas `[TSK-F-XX]` y su estado `[x]` / `[ ]`.

Construye mentalmente dos listas:
- **Tareas completadas**: todas las marcadas con `[x]`.
- **Tareas pendientes**: todas las marcadas con `[ ]`.

Si alguno de los documentos no existe, detener y reportar:

```
🚫 BLOQUEADO — PRERREQUISITO FALTANTE
No existe: [ruta del documento faltante]
La auditoría no puede iniciarse sin los documentos SDD de la etapa.
```

---

## Paso 2 — Verificación de Evidencia (Cross-Check)

La ejecución de este paso varía según el Modo detectado en el Paso 0.5.

---

### Modo DOCUMENTACIÓN (Etapas 1.x)

En etapas de documentación pura no hay código ni tests. La evidencia es documental.

Para cada tarea completada `[x]`, verificar la existencia física de los documentos entregables esperados:

**Etapa 1.1 — Gobernanza:**
- `CLAUDE.md` existe y contiene las secciones: Límites de Autonomía, Protocolo de Inicio de Sesión, Estándares de Código, Fases y Etapas.
- `PROJECT_handoff.md` existe.
- `.claude/skill-router.md` existe.
- La estructura de carpetas definida en CLAUDE.md §"Estructura de Carpetas" está creada en el repositorio.

**Etapa 1.2 — Infraestructura:**
- `docs/database/schema.sql` existe y contiene DDL de tablas `usr_*` y `tss_*`.
- Las tablas descritas en el PRD coinciden con las declaradas en `schema.sql`.

**Etapa 1.3 — Data Contract:**
- `docs/specs/f01_03_spec.md` existe y contiene la especificación formal del Data Contract.
- Los códigos `ERR_MTD_XXX` referenciados en CLAUDE.md están definidos en la SPEC.

**Para cualquier etapa 1.x — Trazabilidad documental:**
- Cada `[TSK-F-XX]` completado tiene su contraparte `[REQ-XX]` en el PRD.
- Verificar con: `Grep "[REQ-"` en `docs/reqs/f[F]_[E]_prd.md` y `Grep "[TSK-"` en `docs/tasks/f[F]_[E]_task.md`.

Construir tabla de resultados:

```
| Tarea [TSK] | Documento Esperado | Existe | Estado |
|---|---|---|---|
| [TSK-1-01] | CLAUDE.md | ✅ / ❌ | Conforme / Incumplida |
```

---

### Modo PROTOTIPADO (Etapa 2.1)

En etapas de prototipado no hay tests reales. Los componentes consumen `mock_data.json`, no APIs reales.

**2A — Verificación de Mock-Data (sustituye la búsqueda de tests):**

- Verificar que `mock_data.json` existe en el proyecto (buscar con `Glob "**/mock_data.json"`).
- Usar `Grep` para buscar llamadas a APIs reales (`fetch(`, `axios`, `useQuery`, `useSWR`, `/api/`, `supabase`, `http`) dentro del directorio `web/`.
- Si se encuentra alguna llamada a API real en un componente del prototipado: **Hallazgo Crítico**.
- Para cada componente, verificar que importa o referencia datos de `mock_data.json`.

**2B — Validación de Modularidad de Carpetas:**

- `web/components/` existe y contiene subdirectorios temáticos (no un único archivo monolítico).
- `web/app/` existe con rutas del App Router de Next.js.
- Los componentes están separados de la lógica (`web/src/utils/` o `web/src/hooks/`).

**2C — Coincidencia Diseño vs. PROJECT_scope.md:**

- Leer `PROJECT_scope.md` e identificar los entregables visuales del dashboard.
- Verificar que los componentes construidos corresponden a los entregables listados en el scope.

Construir tabla de resultados:

```
| Componente | Mock-Data | Sin API Real | Está en Scope | Estado |
|---|---|---|---|---|
| [componente] | ✅ / ❌ | ✅ / ❌ | ✅ / ❌ | Conforme / Incumplido |
```

---

### Modo CÓDIGO (Etapas 3.x y 4.x)

**2A — Búsqueda de Archivo de Código:**

Para cada tarea `[x]`, localizar el archivo de implementación mencionado o inferido. Usar `Glob` para encontrar el archivo. Si no existe: **tarea Incumplida**.

**2B — Validación de Tests:**

- Pipeline Python: buscar tests en `pipeline/tests/` con `Glob "pipeline/tests/test_*.py"`. Para cada módulo de código, debe existir su correspondiente archivo de test.
- Web Next.js: buscar tests en `web/tests/` con `Glob "web/tests/**/*.test.*"`. Para cada componente en `web/components/`, debe existir su test.
- Verificar que los tests no están vacíos (leer el archivo y confirmar que contiene al menos una función `test_` o `it(`/`describe(`).

**2C — Trazabilidad de Tags:**

- Usar `Grep "[TSK-"` en el directorio de código relevante (`pipeline/src/` o `web/`) para verificar que los archivos de implementación contienen referencias a los identificadores de tarea.
- Para cada `[TSK-F-XX]` completado, verificar que existe al menos un `[REQ-XX]` correspondiente en el PRD.

Construir tabla de resultados:

```
| Tarea [TSK] | Archivo de Código | Test Asociado | Tag en Código | Estado |
|---|---|---|---|---|
| [TSK-3-01] | pipeline/src/validator.py | pipeline/tests/test_validator.py | ✅ / ❌ | Conforme / Incumplida |
```

---

## Paso 3 — Detección de "Código Fantasma"

> Este paso se ejecuta SOLO en modos PROTOTIPADO y CÓDIGO. En modo DOCUMENTACIÓN, omitir y continuar al Paso 4.

El objetivo es encontrar trabajo realizado que no tiene respaldo documental.

**3A — Escaneo del árbol de archivos:**

Usar `Bash` con `git log --diff-filter=A --name-only --pretty=format:` para obtener los archivos creados durante la etapa activa. Si no es posible determinar la fecha exacta, usar `Glob` para listar archivos en los directorios relevantes y comparar con los mencionados en `docs/tasks/f[F]_[E]_task.md`.

**3B — Cruce con la Lista de Tareas:**

Para cada archivo nuevo encontrado:
- Buscar su nombre o ruta en `docs/tasks/f[F]_[E]_task.md`.
- Buscar si existe un CC aprobado en `docs/changes/` que justifique su creación (`Grep` del nombre del archivo en `docs/changes/`).
- Si el archivo no aparece en tareas NI en ningún CC aprobado: **Hallazgo de Código Fantasma**.

**3C — Escaneo de funciones sin tag:**

Usar `Grep` para buscar funciones o clases en los archivos de código que no contengan un comentario con tag `[TSK-` o `[CC_` en sus primeras líneas.

Construir reporte:

```
⚠️ Reporte de Código Fantasma
| Archivo / Función | En Tasks | En CC aprobado | Veredicto |
|---|---|---|---|
| [ruta/archivo] | ❌ | ❌ | 🚨 Fantasma |
| [ruta/archivo] | ✅ | — | ✅ Documentado |
```

---

## Paso 4 — Evaluación del Definition of Done (DoD)

La evaluación varía según el modo.

**Modo DOCUMENTACIÓN — DoD documental:**
- Todos los documentos SDD de la etapa (`prd`, `spec`, `plan`, `task`) existen en sus rutas canónicas.
- Los identificadores `[REQ-XX]`, `[OBJ-XX]`, `[TSK-F-XX]` son coherentes entre documentos.
- No hay secciones marcadas como `TODO` o `[PENDIENTE]` en documentos declarados completos.

**Modo PROTOTIPADO — DoD de mockup:**
- Cero llamadas a APIs reales en componentes del prototipado.
- `mock_data.json` existe y tiene la estructura que los componentes esperan.
- La estructura de carpetas de `web/` es modular.
- Los entregables visuales del scope están representados como componentes.

**Modo CÓDIGO — DoD técnico Triple S:**

| Criterio DoD | Verificación | Estado esperado |
|---|---|---|
| Cero Hardcoding | `Grep` de IPs, tokens, IDs numéricos literales en `pipeline/src/` o `web/` | Sin resultados |
| Manejo de Errores ERR_MTD | `Grep "ERR_MTD_"` en `pipeline/src/` | Al menos 1 resultado por módulo |
| Timezone pytz | `Grep "America/Bogota"` en `pipeline/src/` | Al menos 1 resultado |
| Trazabilidad Atómica | Cada `[TSK]` del task list tiene un `[REQ]` en el PRD | Sin huérfanos |

---

## Paso 5 — Generación del Dictamen de Auditoría

Presentar en el chat el informe estructurado completo:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 INFORME DE AUDITORÍA — Etapa f[F]_[E]
Modo: [DOCUMENTACIÓN / PROTOTIPADO / CÓDIGO]
Fecha: [fecha actual]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Matriz de Conformidad

| Tarea [TSK] | Evidencia Encontrada | Trazabilidad [REQ] | Estado |
|---|---|---|---|
| [TSK-F-01] | [archivo o documento] | [REQ-XX] | ✅ Conforme / ❌ Incumplida |

## Reporte de Código Fantasma
[Solo modos PROTOTIPADO y CÓDIGO]

| Archivo / Función | Soporte Documental | Veredicto |
|---|---|---|
| [ruta] | ✅ Task / ✅ CC / ❌ Sin soporte | 🚨 Fantasma / ✅ OK |

## Análisis de Gaps

Requerimientos del PRD sin tarea asociada:
- [REQ-XX]: [descripción] — ⚠️ Huérfano

## Resumen de Auditoría

| Categoría | Estado | Observaciones |
|---|---|---|
| Tareas Completadas | XX / YY total | [tareas hechas vs. total] |
| Evidencia Física | 🟢 / 🔴 | [archivos/tests/docs existen] |
| Código Fantasma | ⚠️ / ✅ | [trabajo no documentado detectado / limpio] |
| Trazabilidad [TSK]→[REQ] | 🟢 / 🔴 | [tags coherentes / huérfanos detectados] |
| DoD Triple S | 🟢 / 🔴 | [criterios cumplidos / incumplidos] |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
## VEREDICTO FINAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Si todas las verificaciones pasan:**

```
✅ CONFORME — AUDITORÍA APROBADA
Etapa f[F]_[E] certificada. Se autoriza invocar /close-stage.

[AUDIT-TOKEN: f[F]_[E]-CONFORME-[fecha en formato YYYYMMDD]]
```

Adicionalmente, escribir el archivo de token de autorización en `.claude/audit-token.md`:

```
AUDIT-TOKEN: f[F]_[E]-CONFORME-[YYYYMMDD]
Etapa: f[F]_[E]
Veredicto: CONFORME
Fecha: [fecha actual]
Auditor: stage-auditor
```

**Si hay hallazgos críticos:**

```
🚫 BLOQUEADO — CIERRE DENEGADO
La etapa f[F]_[E] NO puede cerrarse por los siguientes motivos:

Acciones correctivas requeridas:
1. [Tarea incumplida]: [descripción de qué falta]
2. [Código Fantasma]: Invocar /change-control para documentar [archivo]
3. [Gap de trazabilidad]: [REQ-XX] no tiene tarea asociada

Re-auditar con /stage-audit una vez corregidos todos los hallazgos.
```

Si el veredicto es BLOQUEADO, escribir sobre `.claude/audit-token.md` con estado BLOQUEADO para invalidar cualquier token previo:

```
AUDIT-TOKEN: f[F]_[E]-BLOQUEADO-[YYYYMMDD]
Etapa: f[F]_[E]
Veredicto: BLOQUEADO
Fecha: [fecha actual]
Auditor: stage-auditor
```

---

## Reglas Innegociables del Skill

1. **Prohibido el Cierre Ciego**: Si no hay evidencia física de una tarea, el veredicto es `BLOQUEADO` aunque el usuario afirme que está hecho. La afirmación verbal no cuenta como evidencia.
2. **Prioridad al CC**: Si se detecta Código Fantasma, sugerir siempre invocar `/change-control` antes de volver a auditar.
3. **Freno al Notario**: El skill emite `.claude/audit-token.md` con estado CONFORME ÚNICAMENTE cuando todas las verificaciones pasan. El agente `stage-closer` debe leer y validar este archivo antes de ejecutar el cierre.
4. **Neutralidad**: Este skill reporta, no corrige. Si detecta un error, lo documenta y lo delega. Nunca modificar código de producción.
5. **Excepciones de Prototipado Son Fijas**: En modo PROTOTIPADO, la ausencia de tests NO es un hallazgo crítico. La presencia de llamadas a APIs reales SÍ es un hallazgo crítico.
