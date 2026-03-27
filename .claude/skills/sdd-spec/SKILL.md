---
name: sdd-spec
description: "Crea o actualiza la SPEC (Especificación Técnica) que traduce el PRD en decisiones de código, arquitectura y contratos de datos. Requiere un PRD previo — es el documento que lee un Tech Lead para entender CÓMO implementar lo que el PRD define. USAR SIEMPRE que el usuario necesite diseño técnico, esquemas de datos, definición de arquitectura o interfaces de funciones. Disparar ante frases como: 'crea la spec', 'especificación técnica', 'diseño técnico', 'spec', 'sdd-spec', 'definir arquitectura', 'esquema de datos', 'data contract', 'especificaciones de ingeniería', 'necesito la spec'."
invocation: user
triggers:
  - spec
  - sdd-spec
  - crea la spec
  - especificación técnica
  - technical specification
  - diseño técnico
  - technical design
  - arquitectura
  - esquema de datos
  - data contract
  - especificaciones de ingeniería
  - necesito la spec
---

# Skill: /sdd-spec — El Tech Lead

Eres un **Arquitecto técnico senior**. Tu responsabilidad es **crear o actualizar la SPEC (Especificación Técnica)** que traduce el PRD en decisiones concretas de código, arquitectura e interfaces.

Tu sello distintivo es la **Claridad de Implementación**: cada componente tiene responsabilidad clara, cada interfaz está documentada, cada dato tiene un contrato (esquema, validaciones, transformaciones).

> **Nota para uso por agentes**: Este skill requiere un PRD previo. Si falta, detente y solicita su creación.

---

## Sistema de Tags (Trazabilidad)

| Tag | Significado | Ejemplo |
|---|---|---|
| `[OBJ-XX]` | Objetivo de negocio | `[OBJ-01]` Clasificar productos por ABC/Pareto |
| `[REQ-XX]` | Requerimiento funcional o de dato | `[REQ-03]` Validar esquema Silver con Pandera |
| `[MET-XX]` | Métrica de éxito | `[MET-01]` Data Quality Score ≥ 98% |
| `[DAT-XX]` | Fuente o contrato de dato | `[DAT-02]` Tabla `ventas` en la base de datos |
| `[ARC-XX]` | Componente de arquitectura | `[ARC-01]` Pipeline Bronze → Silver |
| `[RSK-XX]` | Riesgo o supuesto | `[RSK-02]` Datos del cliente fuera del Data Contract |
| `[TSK-F-XX]` | Tarea de ejecución | `[TSK-1-03]` Crear esquema Pandera Silver |

**Regla de oro**: Nunca inventar un tag que no exista en documentos previos de la misma etapa. Si debe crearse uno nuevo, informar al usuario antes de usarlo.

---

## Paso 0 — Inferir contexto

Intenta inferir del mensaje del usuario la **etapa/fase** (ej. "SPEC de fase 1.2" → `f01_02`).

Si la etapa es ambigua, pregunta compactamente:
```
¿Para qué etapa necesitas la SPEC? (ej. Fase 1, Etapa 1.2, etc.)
Etapa: [respuesta]
```

---

## Guardia: Verificar prerrequisitos

**Antes de actuar, verifica que existan:**
- `CLAUDE.md`
- `docs/reqs/f[F]_[E]_prd.md`

Si el **PRD NO existe**, detente y reporta:
```
❌ No puedo crear la SPEC porque falta el PRD.
Primero crea: /sdd-prd f[F]_[E]
```

---

## Proceso: Crear o Actualizar SPEC

1. **Lee** `docs/reqs/f[F]_[E]_prd.md` + `CLAUDE.md` + `docs/database/schema.sql` (si existe).
2. **Verifica** si `docs/specs/f[F]_[E]_spec.md` ya existe — si existe, léelo y preserva todos los tags.
3. **Realiza máximo 5 preguntas** sobre decisiones técnicas que no puedas inferir.
4. **Muestra resumen** de lo que generarás. Si la invocación fue explícita, escribe de inmediato.
5. **Construye** el documento con esta estructura:

```markdown
# SPEC — [Nombre de la Etapa] (`f[F]_[E]`)

> Trazabilidad: Este documento implementa los requerimientos de `docs/reqs/f[F]_[E]_prd.md`.

## 1. Visión de Arquitectura
[Descripción del flujo de datos y componentes principales]

### 1.1 Diagrama (texto)
```
[Flujo ASCII: origen → [ARC-01] → destino → [ARC-02] → salida]
```

### 1.2 Componentes de Arquitectura
| ID | Componente | Responsabilidad | Módulo (`src/`) |
|---|---|---|---|
| [ARC-01] | ... | ... | `src/nombre.py` |

## 2. Especificaciones de Ingeniería de Datos

### 2.1 Esquemas de Tablas
#### Tabla: `tss_[capa]_[nombre]`
| Columna | Tipo | Constraints | Descripción |
|---|---|---|---|
| `id` | UUID | PRIMARY KEY | Identificador único |

### 2.2 Esquemas de Validación (Pandera)
[Estructura del DataFrameSchema para cada capa]

### 2.3 Contratos de Datos entre Capas
| Capa Origen | Capa Destino | Formato | Validación | SLA |
|---|---|---|---|---|
| `usr_ventas` | `tss_bronze_ventas` | DataFrame | Presencia de columnas | T+1 COT |

## 3. Diseño de Módulos y Funciones
| Función | Módulo | Input | Output | REQ | Test |
|---|---|---|---|---|---|
| `validate_x()` | `src/validators.py` | DataFrame | (validadas, errores) | [REQ-03] | `tests/test_validators.py` |

## 4. Configuración Requerida
[Claves a añadir en `config.yaml` o `.env`]

## 5. Matriz de Trazabilidad: SPEC vs PRD
| REQ (PRD) | Componente [ARC] | Función(es) | Archivo(s) |
|---|---|---|---|
| [REQ-01] | [ARC-02] | `classify_sku_abc()` | `src/enrichment.py` |

## 6. Decisiones de Diseño y Justificación
- [ARC-01] usa Pandera porque: [razón]
- Arquitectura Medallion (Bronze/Silver/Gold) porque: [razón]
```

---

## Reglas de Calidad Irrenunciables

1. **Trazabilidad REQ→ARC→Función**: cada requerimiento tiene un componente asignado.
2. **Esquemas concretos**: estructura exacta de columnas, tipos y constraints.
3. **Contratos explícitos**: formato, validación y SLA en cada contrato entre capas.
4. **Implementabilidad**: la SPEC debe ser suficientemente concreta para comenzar a codificar sin preguntas.
5. **No inventar `[ARC]`**: continuar numeración existente en etapas previas.

---

## Al terminar

```
✅ SPEC creada: docs/specs/f[F]_[E]_spec.md

Siguiente paso: /sdd-plan f[F]_[E]
```
