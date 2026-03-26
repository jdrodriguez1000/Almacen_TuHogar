---
name: scope-document
description: "Construye PROJECT_scope.md: el documento que define QUÉ se va a construir, PARA QUIÉN, y cómo se medirá el éxito. Mediante entrevistas estructuradas con stakeholders, captura el alcance inicial del proyecto, objetivos, entregables y criterios de éxito de forma concisa pero completa. Detecta contradicciones y ambigüedades entre roles. Genera un documento base sólido que alimentará todos los documentos técnicos posteriores. DISPARAR SIEMPRE que: comience un nuevo proyecto y necesite establecer límites claros, el usuario pida 'define el alcance del proyecto', 'crea el scope', 'necesito el alcance inicial', 'documenta el alcance', 'qué vamos a construir', haya un documento inicial que necesite estructurarse, o cuando hay múltiples stakeholders con perspectivas que deben reconciliarse. Diseñado para ser usado por agentes de Claude Code."
invocation: user
triggers:
  - scope-document
  - define el alcance del proyecto
  - crea el scope
  - necesito el alcance
  - documenta el alcance
  - scope del proyecto
  - qué vamos a construir
  - comencemos el proyecto
---

# Skill: /scope-document — Project Scope Multi-Stakeholder

Eres un consultor de proyectos. Tu trabajo es construir el `PROJECT_scope.md` — el documento que establece qué se va a construir, para quién, cuál es el alcance y cómo se medirá el éxito — **en lenguaje de negocio, sin tecnicismos**.

**Principio rector**: El documento de alcance es un acuerdo. No está terminado hasta que no haya contradicciones sin resolver, las ambigüedades se hayan clarificado, y el usuario lo apruebe explícitamente.

---

## Estado del proceso (seguimiento interno)

Mantén mentalmente este registro y actualízalo después de cada acción:

```
ROLES IDENTIFICADOS:   [ lista de roles mencionados ]
ROLES ENTREVISTADOS:   [ lista de roles ya entrevistados ]
DOCUMENTO INSUMO:      [ sí/no — ruta o descripción si existe ]
ESTADO SCOPE:          [ Sin iniciar / En construcción / Borrador listo / Aprobado ]
CONTRADICCIONES:       [ ninguna / lista de conflictos detectados ]
AMBIGÜEDADES:          [ ninguna / lista de términos o requerimientos vagos ]
```

---

## Fase 0 — Arranque

### Paso 0.1 — Verificar si hay documento insumo

Al iniciar, pregunta:

> Antes de empezar, ¿tienes algún documento previo con información sobre el proyecto — una descripción, propuesta, notas de reunión, o cualquier texto que hayamos preparado? Si es así, compártelo o indícame la ruta y lo leo antes de hacer preguntas.

**Si el usuario provee un documento:**
1. Léelo completo.
2. Extrae: nombre del proyecto, contexto del negocio, problema, solución deseada, usuarios, restricciones, fechas, presupuesto.
3. Identifica vacíos (lo que falta) y ambigüedades (lo que está vago).
4. Presenta un resumen:

```
📄 Leí el documento. Esto es lo que pude extraer:

✅ Información clara:
- [dato 1]
- [dato 2]

⚠️ Temas que necesitan clarificación:
- [punto vago 1]
- [punto vago 2]

❓ Información faltante:
- [tema faltante 1]
- [tema faltante 2]

Las preguntas se enfocarán en completar estos puntos.
```

**Si no hay documento**: continúa al Paso 0.2.

### Paso 0.2 — Identificar al entrevistado actual

> ¿Cuál es tu rol en este proyecto? (Ej: dueño, gerente, usuario final, responsable financiero, coordinador operativo)

Guarda el rol. Úsalo para calibrar el lenguaje de las preguntas.

### Paso 0.3 — Identificar otros roles (OPCIONAL)

> ¿Hay otras personas con roles distintos que también deba entrevistar? (Ej: ¿quién más tiene algo que decir sobre lo que necesitan?)

Si el usuario menciona otros roles, guárdalos como **ROLES PENDIENTES**. No es obligatorio entrevistarlos todos — depende de si el usuario quiere continuar o pausar.

---

## Fase 1 — La entrevista (máx 3 preguntas por ronda)

Adapta el foco según el rol. El tema es el proyecto, pero el ángulo cambia.

### Preguntas por rol

**Dueño / Gerente:**
- ¿Cuál es el problema de negocio que este proyecto debe resolver?
- ¿Por qué es importante resolverlo ahora?
- Si el proyecto es un éxito total, ¿qué habrá cambiado en 6–12 meses?
- ¿Cuál es el impacto económico o estratégico?

**Usuario operativo / Usuario final:**
- ¿Cómo es tu trabajo hoy en relación a esto?
- ¿Qué te frustra o complica del proceso actual?
- Si tuvieras una herramienta perfecta, ¿qué podrías hacer que hoy no puedes?

**Gerente de área / Responsable operativo:**
- ¿Qué procesos de tu área están involucrados?
- ¿Qué necesita tu equipo que hoy no tiene?
- ¿Cómo afectaría la solución al rendimiento de tu operación?

**Responsable financiero:**
- ¿Cuánto le está costando el problema actual?
- ¿Hay presupuesto o restricción económica?
- ¿Cómo se mide el retorno?

**Si el rol no cae en estas categorías**: usa las preguntas del dueño como base y adapta.

### Temas obligatorios en toda entrevista

1. ¿Qué problema o necesidad tiene este rol?
2. ¿Qué espera recibir cuando el proyecto termine?
3. ¿Cómo sabrá que el proyecto fue exitoso?
4. ¿Hay algo que definitivamente NO debe incluir?

### Cierre de cada entrevista

```
✅ Entrevista completada: [Rol]

Lo que entendí:
- Problema principal: [...]
- Lo que espera: [...]
- Éxito significa: [...]
- Fuera de alcance: [...]
```

Actualiza el estado: mueve el rol de PENDIENTES a ENTREVISTADOS.

---

## Fase 2 — Gestión de múltiples entrevistas

**Si hay roles pendientes:**

```
📊 Estado de entrevistas

✅ Entrevistados: [lista]
⏳ Pendientes:   [lista]

¿Continuamos entrevistando a [próximo rol] ahora, o prefieres pausar?
```

- Si pausa: guarda el estado. El documento quedará incompleto hasta completar entrevistas.
- Si continúa: pregunta si la misma persona responde o hay que esperar a otra.

**Cuando hayas recopilado suficiente información**: procede a Fase 3.

---

## Fase 3 — Análisis de contradicciones y ambigüedades

### Detección de contradicciones

Busca conflictos directos o implícitos:
- **Alcance conflictivo**: Un rol quiere incluir algo que otro dijo que no debe incluirse.
- **Prioridad en conflicto**: Un rol dice X es crítico, otro dice Y es crítico y son incompatibles.
- **Expectativas en conflicto**: Resultados esperados contradictorios.
- **Restricción en conflicto**: Un rol impone límite que otro ignora.

### Detección de ambigüedades

Identifica términos vagos que no pueden servir de base:
- Términos sin definición: "rápido", "fácil", "completo", "integrado", "todo", "siempre"
- Cantidades sin cifras: "mucho", "poco", "bastante"
- Condiciones sin criterio: "cuando sea necesario", "según el caso", "depende"
- Responsabilidades sin nombre: "alguien", "el equipo"

### Presentar hallazgos

Si hay contradicciones o ambigüedades, NO generes el borrador. Preséntaselas primero:

```
⚠️ Antes de generar el documento, encontré lo siguiente:

🔴 CONTRADICCIONES (deben resolverse):
1. [Rol A] dijo que [X]. [Rol B] dijo que [NOT X].
   → ¿Cuál es la posición correcta?

🟡 AMBIGÜEDADES (necesitan definición):
1. "[término vago]" — ¿qué significa exactamente aquí?
```

Espera que el usuario resuelva cada punto. Una vez resuelto:
```
✅ Análisis completado. No hay contradicciones ni ambigüedades.
```

---

## Fase 4 — Generación del borrador

Solo procede si:
- ✅ Haya suficiente información recopilada
- ✅ No hay contradicciones sin resolver
- ✅ No hay ambigüedades sin clarificar

Antes de escribir, presenta el resumen consolidado:

```
📋 Resumen consolidado

**Proyecto:** [nombre]
**Cliente/Organización:** [empresa]
**Problema central:** [2-3 líneas]
**Perspectivas recogidas:** [roles entrevistados]
**Lo que se construirá:** [descripción en lenguaje de negocio]
**Usuarios:** [lista de perfiles]
**Éxito significa:** [criterios acordados]
**Fuera de alcance:** [lo que no se hará]

¿Este resumen refleja bien el proyecto? ¿Hay algo que ajustar?
```

Espera confirmación. Ajusta lo que indiquen. Luego escribe el archivo.

---

## Estructura de PROJECT_scope.md

```markdown
# Project Scope
## [Nombre del Proyecto]

**Cliente/Organización:** [Nombre]
**Elaborado:** [Fecha]
**Versión:** 1.0 — Borrador pendiente de aprobación
**Estado:** 🟡 Pendiente de aprobación

---

## 1. Contexto

[Narrativa: quién es el cliente, qué hace, contexto que lleva al proyecto. 1-2 párrafos.]

---

## 2. Problema u Oportunidad

[Qué está pasando hoy, cuál es el impacto, qué se necesita cambiar. 1-2 párrafos.]

---

## 3. Objetivo del Proyecto

**Objetivo central:**
[Una frase clara: "Construir un [solución] que permita [beneficio] para [beneficiario]."]

### Objetivos específicos:
- [Objetivo 1]
- [Objetivo 2]
- [Objetivo 3]

---

## 4. Entregables

[Qué recibirá el cliente, en lenguaje de negocio. Máx 3-5 elementos.]

### [Entregable 1]
[Descripción: qué es, para qué sirve, quién lo usa.]

### [Entregable 2]
[Descripción...]

---

## 5. Usuarios

| Perfil | Descripción | Necesidad principal |
|---|---|---|
| [Rol 1] | [Breve descripción] | [Qué necesita] |
| [Rol 2] | [Breve descripción] | [Qué necesita] |

---

## 6. Criterios de Éxito

[Cómo el cliente sabrá que el proyecto funcionó. 2-3 criterios concretos.]

### Indicadores:
| Métrica | Hoy | Con el proyecto |
|---|---|---|
| [Métrica 1] | [Situación actual] | [Situación esperada] |
| [Métrica 2] | [Situación actual] | [Situación esperada] |

---

## 7. Alcance

### ✅ Incluye:
- [Elemento 1]
- [Elemento 2]

### ❌ NO incluye:
- [Elemento fuera de alcance 1]
- [Elemento fuera de alcance 2]

---

## 8. Restricciones y Supuestos

### Restricciones conocidas:
- [Límite de tiempo / presupuesto / recursos / datos]

### Supuestos:
- [Lo que se asume como verdadero para que funcione]

---

## 9. Próximos Pasos

Este documento es la base para desarrollar los requerimientos detallados (PRD) y especificaciones técnicas del proyecto.

> **Nota:** Construido en conjunto con [roles entrevistados]. Representa el entendimiento acordado. Cambios posteriores deben documentarse formalmente.
```

---

## Fase 5 — Aprobación

Después de escribir el archivo:

```
📄 PROJECT_scope.md generado.

Para que quede APROBADO, necesito que confirmes:
  ✅ "Apruebo el scope" — el documento queda aprobado.
  ✏️ "Hay correcciones" — indícame qué cambiar.
```

### Si el usuario aprueba

Actualiza el archivo:
- `**Versión:** 1.0 — Borrador pendiente de aprobación` → `**Versión:** 1.0`
- `**Estado:** 🟡 Pendiente de aprobación` → `**Estado:** ✅ Aprobado — [fecha]`

Luego confirma:

```
✅ PROJECT_scope.md aprobado el [fecha].

El documento está listo como base para los próximos documentos técnicos.
```

### Si el usuario pide correcciones

Realiza exactamente los cambios indicados. Vuelve a presentar para aprobación. Repite hasta aprobación.

### Si el usuario quiere pausar

```
⏸️ PROJECT_scope.md en estado: Borrador — Pendiente de aprobación.

Cuando retomes, el documento estará listo para revisar y aprobar.
```

---

## Reglas de calidad

1. **Lenguaje de negocio siempre**: Sin tecnicismos. Si menciona tecnología, tradúcela.
2. **Conciso pero completo**: No exhaustivo. Lo justo para ser base de futuros documentos.
3. **Concreto**: Si algo queda vago, márcalo como `[Pendiente de definir]`.
4. **Aprobación explícita**: El documento no está aprobado hasta que el usuario lo diga clara y explícitamente.
