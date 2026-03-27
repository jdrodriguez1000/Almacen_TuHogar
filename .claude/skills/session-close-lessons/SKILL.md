---
name: session-close-lessons
description: "Actualiza docs/lessons/lessons-learned.md con las lecciones aprendidas de la sesión: qué funcionó, qué generó fricción y decisiones clave tomadas. USAR al cerrar una sesión de trabajo o cuando el usuario quiera registrar aprendizajes explícitamente. Disparar ante frases como 'registra las lecciones', 'lecciones aprendidas', 'qué aprendimos', 'retrospectiva', 'session-close-lessons'. También invocar automáticamente como segundo paso del protocolo de cierre de sesión, después de /session-close-handoff."
invocation: user
triggers:
  - registra las lecciones
  - lecciones aprendidas
  - qué aprendimos
  - retrospectiva
  - session-close-lessons
  - lessons
---

# Skill: /session-close-lessons

Tu objetivo es registrar en `docs/lessons/lessons-learned.md` las lecciones de la sesión. Este archivo es el **acumulador histórico de aprendizaje del proyecto**: cada entrada hace al equipo más hábil en las etapas siguientes.

> Reglas de comportamiento y protocolos: ver **CLAUDE.md**.

---

## Paso 1 — Leer o inicializar el archivo

Lee `docs/lessons/lessons-learned.md`. Si no existe, créalo con la siguiente estructura base:

```markdown
# Lecciones Aprendidas — Almacén MultiTodo

> Este archivo acumula el aprendizaje histórico de cada sesión y etapa del proyecto.
> Cada entrada es permanente — nunca se borra, solo se añade.

---

## Fase 1 — Gobernanza y Cimientos

### Etapa 1.1 — Constitución del Proyecto

*(Sin sesiones registradas aún)*
```

---

## Paso 2 — Localizar la sección de Fase/Etapa activa

Del contexto de la conversación, determina la Fase y Etapa activa (ej. Fase 1, Etapa 1.2).

Busca la sección correspondiente en el archivo con el patrón `## Fase [N]` y `### Etapa [N.N]`. Si la sección de fase o etapa no existe aún, créala al final del archivo respetando la jerarquía `##` para fase y `###` para etapa.

---

## Paso 3 — Añadir entrada de sesión

Al final de la sección de la Etapa activa, añade la siguiente entrada. Sé honesto y concreto — estas notas son datos valiosos para futuras etapas, no una formalidad:

```markdown
### Sesión: [fecha actual en formato YYYY-MM-DD]

**✅ Lo que funcionó bien:**
- [Decisiones, herramientas o enfoques que resultaron positivos y vale la pena repetir]

**⚠️ Lo que no funcionó / fricción encontrada:**
- [Errores cometidos, malentendidos, pasos repetidos o decisiones que se revirtieron]

**💡 Decisiones clave tomadas:**
- [Decisiones de diseño, arquitectura o gobernanza que no están en otro documento]
```

Si la sesión no tuvo fricción o no se tomaron decisiones relevantes, aún así registra la entrada con una línea breve como `- Sin incidentes.` — la consistencia del registro importa más que el contenido en sesiones tranquilas.

---

## Paso 4 — Resumen de etapa (solo si la etapa se cierra)

Si en esta sesión se completaron **todas** las tareas de la etapa activa (verificar que todas estén `[x]` en `docs/tasks/f[F]_[E]_task.md`), añade un bloque de resumen al final de la sección de la etapa:

```markdown
### 📋 Resumen de la Etapa [N.N]

**Lecciones más valiosas para etapas futuras:**
1. [La lección más impactante — algo que cambiaría el enfoque en otra etapa]
2. [Segunda lección más valiosa]
3. [Tercera lección más valiosa]

**Decisiones que no deben revertirse:**
- [Decisión arquitectónica o de gobernanza que quedó establecida para siempre]
```

Solo genera este bloque cuando la etapa esté 100% completada. No lo generes por anticipado.

---

## Paso 5 — Confirmación

Confirma con una línea: `` `docs/lessons/lessons-learned.md` actualizado — Sesión [fecha] registrada en Etapa [N.N]. ``

---

## Reglas innegociables

- Jamás eliminar entradas anteriores — este archivo solo crece, nunca se recorta.
- Registrar fricciones con honestidad: los errores documentados evitan que se repitan.
- El Resumen de Etapa se genera **únicamente** cuando la etapa está 100% completada según el task list.
- Si no puedes determinar la Fase/Etapa activa del contexto, pregunta antes de escribir en la sección equivocada.
