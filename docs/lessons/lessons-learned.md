# Lecciones Aprendidas — Almacen MultiTodo

> Este archivo acumula el aprendizaje historico de cada sesion y etapa del proyecto.
> Cada entrada es permanente — nunca se borra, solo se anade.

---

## Fase 1 — Gobernanza y Cimientos

### Etapa 1.1 — Constitucion del Proyecto

#### Sesion: 2026-03-27

**Lo que funciono bien:**
- El flujo PRD a SPEC a Plan a Tasks genero documentacion de alta calidad en una sola sesion. La cadena SDD completa (4 documentos) fue redactada y escrita sin necesidad de revisiones mayores.
- El agente sdd-documenter produce contenido completo y listo para escribir cuando se le da contexto suficiente (scope, decisiones previas, restricciones del proyecto). Con contexto rico, el primer intento de contenido es directo al archivo.
- Los documentos SDD de una etapa de gobernanza (tipo DOCUMENTACION) no requieren esquemas Pandera ni DDL SQL — la SPEC puede ser puramente documental. Esto simplifica la cadena y fue validado sin ambiguedad.
- La estrategia de documentar sobre una etapa parcialmente ejecutada (B1-B6 ya existentes) funciono: los documentos reflejan el estado real del repositorio sin distorsion.

**Lo que no funciono / friccion encontrada:**
- El agente sdd-documenter no tiene herramienta Write. En la primera invocacion entrego el contenido sin escribirlo — se requirio que el agente orquestador tomara el contenido y ejecutara la escritura. Esto anade un paso intermedio pero es el patron correcto y repetible.
- El directorio `docs/lessons/` no existia en disco a pesar de que TSK-1-14 estaba marcada como completada en el task list. Discrepancia entre estado documental y estado real del repositorio — detectado y corregido en el cierre de sesion.
- La ausencia de `PROJECT_handoff.md` al inicio del proyecto (primera sesion) implica que el agente orquestador debe reconstruir el contexto desde CLAUDE.md y PROJECT_scope.md. Esto funciona pero es mas lento que arrancar desde un handoff existente.

**Decisiones clave tomadas:**
- Patron de trabajo con sdd-documenter establecido y validado: agente recibe contexto completo → genera contenido markdown → orquestador escribe con herramienta Write. No improvsar variantes.
- El skill /stage-audit debe recibir el parametro de tipo de etapa (DOCUMENTACION) al auditar 1.1 para no aplicar criterios de etapas de codigo (no hay tests pytest, no hay componentes Next.js).
- La proxima sesion debe iniciar con el commit de cierre SDD antes de cualquier otra accion — el repositorio tiene cambios sin commitear.
