---
name: session-close-handoff
description: "Reescribe PROJECT_handoff.md con el estado macro completo del proyecto y el estado táctico exacto de la sesión. USAR cuando el usuario indique fin de sesión o quiera guardar el estado del proyecto — ya sea explícitamente ('Terminamos', 'Cerramos', 'Hasta luego', 'actualiza el handoff', 'guarda el estado', 'session-close-handoff') o implícitamente (despedida, resumen de lo hecho, pregunta sobre qué falta). No esperar la frase exacta — ante cualquier señal de cierre, ejecutar este protocolo de inmediato."
invocation: user
triggers:
  - terminamos
  - cerramos
  - hasta luego
  - fin de sesión
  - eso es todo
  - listo por hoy
  - done for today
  - that's it
  - bye
  - nos vemos
  - actualiza el handoff
  - guarda el estado
  - session-close-handoff
  - PROJECT_handoff
  - handoff
---

# Skill: /session-close-handoff

Tu objetivo es reescribir `PROJECT_handoff.md` en la raíz del proyecto con el estado completo del proyecto al cierre de sesión. Este archivo es el **único punto de verdad de estado**: la próxima sesión solo necesita leerlo para arrancar con contexto completo.

> Reglas de comportamiento y protocolos: ver **CLAUDE.md**.

---

## Paso 1 — Leer el estado actual

Lee `PROJECT_handoff.md` existente (si existe). Extrae y preserva **íntegramente**:
- La sección **§5 Notas y Decisiones Registradas** — es append-only, jamás se sobrescribe ni se trunca.
- La sección **§2 Hitos del Proyecto** — actualiza solo los ítems que cambiaron en esta sesión.
- La sección **§3 Mapa de Arquitectura** — actualiza solo las filas que cambiaron en esta sesión.
- La sección **§4 Índice SDD** — actualiza estado de documentos si se crearon o completaron en esta sesión.

Si `PROJECT_handoff.md` no existe (primera sesión), inicializa todas las secciones con los valores del proyecto desde `CLAUDE.md` y el contexto disponible.

---

## Paso 2 — Reconstruir el estado de la sesión

Analiza la conversación completa para extraer:

- **Archivos tocados:** ¿Qué archivos se leyeron, crearon o modificaron?
- **Contexto inmediato:** ¿Qué lógica, función o problema se estaba trabajando en los últimos mensajes?
- **Último error o bloqueador:** Clasifica en una de tres categorías:
  - *Error activo:* pegar el mensaje exacto de consola o describir el bug.
  - *Decisión pendiente:* describir qué quedó abierto y las opciones disponibles.
  - *Cierre limpio:* no hubo bloqueador.
- **Próxima acción:** La tarea atómica más pequeña y concreta para iniciar la próxima sesión. Tan específica que un agente pueda ejecutarla sin preguntar nada.
- **Notas nuevas:** Decisiones de arquitectura, cambios de alcance, CCs aprobados, o cualquier hecho relevante ocurrido en esta sesión que deba quedar en el registro histórico. Formato: `- **YYYY-MM-DD** — [hecho concreto]`.

---

## Paso 3 — Mostrar resumen y escribir el archivo

Muestra un resumen breve en el chat antes de escribir:

```
Cerrando sesión — Handoff:
- Fase/Etapa: [fase y etapa]
- Archivos activos: [lista]
- Contexto: [1-2 líneas]
- Bloqueador: [descripción o "Ninguno"]
- Notas nuevas: [cantidad] entrada(s)
- Próxima acción: [tarea concreta]
```

**Si el usuario ya dio una señal clara de cierre, escribe `PROJECT_handoff.md` de inmediato sin esperar confirmación adicional.**
Solo pide confirmación si hay ambigüedad real sobre el estado del trabajo.

Usa exactamente la siguiente estructura al escribir el archivo:

```markdown
# PROJECT_handoff — Estado del Proyecto

> **MANDATO IA:** Este es el único archivo de estado del proyecto. Léelo PRIMERO al iniciar cada sesión — contiene el estado macro (fases, hitos, arquitectura, decisiones históricas) y el estado táctico de la última sesión (qué se hizo, bloqueadores, próxima acción).

---

## 📍 1. Coordenadas Actuales

- **Fase Activa:** `Fase [N] — [Nombre de Fase]`
- **Etapa Activa:** `Etapa [N.N] — [Nombre de Etapa]`
- **Capa Medallón Activa:** `[N/A | Bronze | Silver | Gold]`
- **Progreso Global:** [X]% ([N]/[Total] etapas completadas)
- **Documentos SDD Gobernantes** *(leer antes de decisiones arquitectónicas)*:
  - PRD:    `docs/reqs/f[F]_[E]_prd.md` [✅ Existe | ⬜ Pendiente]
  - SPEC:   `docs/specs/f[F]_[E]_spec.md` [✅ Existe | ⬜ Pendiente]
  - Plan:   `docs/plans/f[F]_[E]_plan.md` [✅ Existe | ⬜ Pendiente]
  - Tareas: `docs/tasks/f[F]_[E]_task.md` [✅ Existe | ⬜ Pendiente] ([X]/[Y] completadas)

---

## 🏁 2. Hitos del Proyecto

### Fase [N] — [Nombre]
- [✅|⬜] **[N.N]** [Descripción del hito]

*(Repetir por cada fase y etapa del proyecto)*

---

## 🏗️ 3. Mapa de Arquitectura (Rutas Clave)

| Componente | Ruta | Estado |
|---|---|---|
| [Nombre] | `[ruta]` | [✅ Existe \| ⬜ Pendiente \| 🔄 En progreso] |

---

## 📚 4. Índice SDD

### Etapa Activa — [Fase N.N]

| Documento | Ruta | Estado |
|---|---|---|
| [Tipo] Etapa [N.N] | `docs/[tipo]/f[F]_[E]_[tipo].md` | [✅ Existe \| ⬜ Pendiente] |

*(Etapas anteriores cerradas: ver resúmenes ejecutivos en `docs/executives/`)*

---

## 📝 5. Notas y Decisiones Registradas

[Preservar todas las entradas anteriores íntegramente. Agregar nuevas al final.]

- **[YYYY-MM-DD]** — [Decisión, hecho o evento relevante del proyecto]

---

## 🎯 6. Estado de Sesión

### Punto de Guardado

- **Última actualización:** [Fecha completa, hora aproximada]
- **Fase / Etapa:** `Fase [N] — Etapa [N.N]`

### Archivos en el Escritorio (Working Set)

- `[ruta/archivo_1]` — [qué se hizo o por qué es relevante]
- `[ruta/archivo_2]` — [qué se hizo o por qué es relevante]

### Contexto Inmediato

[2-4 líneas describiendo exactamente qué se estaba pensando, construyendo o discutiendo al cierre. Suficiente detalle para que un agente retome sin preguntas.]

### Bloqueador / Último Error

[Una de las tres opciones:]
- Error activo: [mensaje exacto de consola o descripción del bug]
- Decisión pendiente: [qué quedó abierto y qué opciones hay]
- Ninguno — la sesión cerró en estado limpio.

### Próxima Acción Inmediata

1. [Acción atómica y concreta — suficientemente específica para ejecutarla sin preguntar]
2. [Segunda acción si aplica]
3. [Tercera acción si aplica]
```

---

## Paso 4 — Confirmación final

Tras escribir el archivo:
1. Confirma: "`PROJECT_handoff.md` actualizado."
2. Muestra en una línea la Próxima Acción registrada para que el usuario la tenga visible al cerrar.

---

## Reglas innegociables

- La sección **§5 Notas y Decisiones Registradas** jamás se sobrescribe — solo se añade al final.
- Si no hay notas nuevas en la sesión, la sección se preserva sin modificar.
- La Próxima Acción debe ser una tarea atómica y específica, nunca genérica como "continuar el desarrollo".
