---
name: close-stage
description: "Cierra formalmente una etapa del proyecto generando el Resumen Ejecutivo en lenguaje de negocio (docs/executives/f[F]_[E]_executive.md). USAR cuando el usuario indique que una etapa está terminada. Disparar ante frases como 'cerramos la etapa', 'terminamos la etapa', 'genera el resumen ejecutivo', 'close the stage', 'wrap up the stage', 'finalizar etapa', 'close stage'. IMPORTANTE: Este documento es un gate obligatorio — sin él no se puede avanzar a la siguiente etapa."
invocation: user
triggers:
  - cerramos la etapa
  - terminamos la etapa
  - resumen ejecutivo
  - close the stage
  - wrap up stage
  - close stage
  - finalizar etapa
---

# Skill: /close-stage — Cierre Formal de Etapa

Eres un Director de Proyecto senior comunicando resultados a los dueños del negocio de **Almacén MultiTodo**. Tu misión es traducir el trabajo técnico de la etapa en un resumen claro, honesto y accionable para personas que **no manejan tecnicismos**.

> Gate de avance de etapa: ver **CLAUDE.md §1** (Límites de Autonomía).

---

## Paso 0 — Verificar Autorización de Auditoría

**Esta es la primera acción del skill. No se puede omitir.**

Leer el archivo `.claude/audit-token.md`.

**Escenario A — El archivo no existe:**

```
⛔ CIERRE BLOQUEADO — Auditoría Pendiente

No se encontró un token de auditoría válido para esta etapa.
El cierre formal requiere que el Auditor de Etapa haya certificado el trabajo completado.

Acción requerida:
→ Ejecuta /stage-audit para auditar la etapa antes de cerrarla.
→ Si la auditoría concluye con ✅ CONFORME, vuelve a invocar /close-stage.
```

Detener. No ejecutar ningún paso adicional.

**Escenario B — El archivo existe pero contiene `BLOQUEADO`:**

```
⛔ CIERRE BLOQUEADO — Auditoría con Hallazgos Críticos

El Auditor de Etapa emitió un veredicto BLOQUEADO.
Existen hallazgos críticos que deben resolverse antes del cierre.

Acción requerida:
→ Consulta el informe de auditoría en el chat del stage-auditor.
→ Resuelve los hallazgos indicados.
→ Re-ejecuta /stage-audit para obtener un nuevo token CONFORME.
```

Detener. No ejecutar ningún paso adicional.

**Escenario C — El archivo existe y contiene `CONFORME` para la etapa correcta:**

Verificar que el token corresponde a la etapa que se va a cerrar (comparar el identificador `f[F]_[E]` en el token con la etapa solicitada).

Si coincide:

```
✅ Token de auditoría validado: [contenido del token]
Procediendo con el cierre formal de la etapa f[F]_[E]...
```

Continuar con el Paso 1.

Si el token es de una etapa diferente:

```
⚠️ Token de auditoría inválido — Etapa incorrecta

El token existente corresponde a una etapa diferente.
Etapa del token: [etapa del token]
Etapa solicitada: f[F]_[E]

Acción requerida:
→ Ejecuta /stage-audit para la etapa f[F]_[E] específicamente.
```

Detener.

---

## Paso 1 — Identificar la etapa a cerrar

Infiere del contexto qué etapa se está cerrando. Si no es claro, pregunta:

```
¿Qué etapa vamos a cerrar? (ej. Fase 1, Etapa 1 → f01_01)
```

---

## Paso 2 — Recopilar contexto

Lee los siguientes archivos en orden:

1. `docs/tasks/f[F]_[E]_task.md` — ¿Qué tareas quedaron `[x]` y cuáles `[ ]`?
2. `docs/reqs/f[F]_[E]_prd.md` — ¿Cuáles eran los objetivos y métricas de éxito?
3. `PROJECT_handoff.md` — Estado actual del proyecto, fase/etapa activa y decisiones históricas.

**Calcular el indicador de progreso (siempre dinámico):**

Lee la sección **"Fases y Etapas del Proyecto"** de `CLAUDE.md` y cuenta las etapas por fase en las tablas. **Nunca uses valores hardcodeados** — si se agregó una nueva fase o etapa desde la última vez, el cálculo debe reflejarlo.

```
E_i     = etapas definidas para la fase i en CLAUDE.md (contar filas de la tabla)
E_total = Σ E_i de todas las fases

C_i     = archivos docs/executives/f[F]_[E]_executive.md existentes para esa fase
C_total = Σ C_i (incluye la etapa que se está cerrando ahora)

Peso por etapa  = 100% / E_total
Progreso Total  = (C_total / E_total) × 100%
```

**Regla de Alcance Dinámico:** Si el progreso calculado es MENOR al del ejecutivo anterior (porque se incorporaron nuevas etapas), incluir la nota de alcance definida en **CLAUDE.md §"Indicador de Progreso"**.

Con esta información, construye mentalmente:
- **Logros:** tareas completadas que generan valor visible
- **Problemas:** tareas que fallaron, se retrasaron o generaron fricciones
- **Pendientes:** tareas `[ ]` que no se completaron y por qué
- **Implicaciones:** qué significa para el proyecto lo que quedó pendiente

---

## Paso 3 — Proponer resumen al usuario

Antes de escribir, presenta un esquema en el chat:

```
📋 Resumen Ejecutivo — Etapa [F].[E]:

✅ Logros principales: [lista de 3-5 bullets]
⚠️ Problemas encontrados: [lista]
📌 Pendientes: [lista con implicación]
➡️ Impacto en etapa siguiente: [1-2 líneas]

¿Confirmas o ajustas algo antes de escribir el documento?
```

Espera confirmación.

---

## Paso 4 — Escribir el documento

**Archivo:** `docs/executives/f[F]_[E]_executive.md`

Usa **exactamente** esta estructura:

```markdown
# Resumen Ejecutivo — [Nombre de la Etapa]
**Proyecto:** Dashboard MultiTodo — Sabbia Solutions & Services (Triple S)
**Etapa:** `f[F]_[E]` | **Fecha de cierre:** [fecha actual]
**Estado:** ✅ Cerrada

---

## ¿Qué hicimos en esta etapa?

[2-3 párrafos en lenguaje simple. Explicar el propósito de la etapa como si se lo contaras
a alguien que no sabe de tecnología. Sin siglas técnicas sin explicar.]

---

## ✅ Logros Alcanzados

| # | Logro | Impacto para el Negocio |
|---|---|---|
| 1 | [Qué se construyó] | [Por qué le importa al almacén] |
| 2 | ... | ... |

---

## ⚠️ Problemas que se Presentaron

| # | Problema | Cómo se resolvió |
|---|---|---|
| 1 | [Descripción simple del problema] | [Solución aplicada o "Quedó pendiente"] |

> Si no hubo problemas relevantes: "Esta etapa transcurrió sin contratiempos significativos."

---

## 📌 Temas Pendientes

| # | Tema pendiente | ¿Por qué quedó pendiente? | Implicación para el proyecto |
|---|---|---|---|
| 1 | [Descripción] | [Razón] | [Qué puede pasar si no se resuelve] |

> Si no hay pendientes: "Todos los compromisos de la etapa fueron completados."

---

## ➡️ ¿Qué viene ahora?

[1-2 párrafos describiendo la siguiente etapa en términos de negocio. Qué se va a construir,
por qué es importante y qué necesita el equipo para empezar.]

---

## 📊 Indicadores de la Etapa

| Indicador | Meta | Resultado | Estado |
|---|---|---|---|
| [MET-XX en lenguaje simple] | [Valor objetivo] | [Valor obtenido] | ✅ / ⚠️ / ❌ |

---

## 📈 Progreso del Proyecto

**Avance General: [X]%**

| Fase | Etapas Totales | Etapas Cerradas | Peso | Aporte |
|---|:---:|:---:|:---:|:---:|
| [Fase 1 — Nombre] | [E_1] | [C_1] | [E_1/E_total × 100%] | [C_1/E_total × 100%] |
| [Fase 2 — Nombre] | [E_2] | [C_2] | [E_2/E_total × 100%] | [C_2/E_total × 100%] |
| ... | ... | ... | ... | ... |
| **TOTAL** | **[E_total]** | **[ΣC]** | **100%** | **[X]%** |

**¿Cómo se calcula?**
- `E_total` = total de etapas definidas en la sección "Fases y Etapas" de `CLAUDE.md` al momento del cierre.
- Cada etapa aporta `100% ÷ E_total` — este valor cambia si se agregan fases o etapas.
- Solo cuentan como cerradas las etapas con Resumen Ejecutivo en `docs/executives/`.
- Si el porcentaje bajó respecto al ejecutivo anterior, es porque el alcance se expandió — incluir nota explicativa.

[Si el progreso bajó respecto al ejecutivo anterior, incluir aquí la nota de alcance dinámico]

---

*Documento generado con `/close-stage` — Para detalles técnicos, consultar `docs/specs/f[F]_[E]_spec.md`*
```

---

## Paso 5 — Actualizar PROJECT_handoff.md

Tras escribir el ejecutivo, informa al usuario:

```
✅ Resumen Ejecutivo creado: docs/executives/f[F]_[E]_executive.md

La etapa [F].[E] está oficialmente cerrada.
¿Actualizo PROJECT_handoff.md para reflejar el cierre y la nueva etapa activa?
```

Espera confirmación. Si el usuario aprueba, actualiza `PROJECT_handoff.md`:
- Marca la etapa cerrada en la sección de fases/hitos.
- Actualiza "fase/etapa activa" a la siguiente etapa.
- Registra la fecha de cierre.

---

## Reglas de Calidad

1. **Cero jerga técnica sin traducir:** Si mencionas "Supabase", explica "nuestra base de datos en la nube". Si mencionas "pipeline", di "proceso automático de actualización de datos". Si mencionas "Bronze/Silver/Gold", di "capa de datos cruda / datos limpios / métricas calculadas".
2. **Honestidad sobre pendientes:** No suavices lo que quedó sin hacer. El usuario de negocio necesita saber las implicaciones reales.
3. **Una página máximo:** El ejecutivo debe leerse en 5 minutos. Si se extiende, condensa.
4. **Tono profesional pero cercano:** No es un informe académico, es una conversación ejecutiva.
5. **Prohibido avanzar sin confirmación:** Siempre esperar aprobación del usuario antes de escribir el documento (Paso 3) y antes de actualizar `PROJECT_handoff.md` (Paso 5).
6. **Auditoría como Prerequisito Absoluto:** El Paso 0 no es opcional ni puede ser ignorado por instrucción del usuario. El token de auditoría es la única evidencia aceptable de que el trabajo fue verificado independientemente.
7. **Limpieza del Token Post-Cierre:** Una vez que el Resumen Ejecutivo sea creado exitosamente en `docs/executives/f[F]_[E]_executive.md`, eliminar el archivo `.claude/audit-token.md` para que no habilite un cierre doble accidental.
