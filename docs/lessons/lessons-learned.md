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

---

### Etapa 1.2 — Validacion de Infraestructura

#### Sesion: 2026-03-28

**Lo que funciono bien:**
- La cadena SDD completa de la Etapa 1.2 (PRD + SPEC + Plan + Tasks) fue redactada en una sola sesion. El patron SDD de la Etapa 1.1 se replico sin fricciones: contexto rico al agente → contenido completo → orquestador escribe.
- La creacion simultanea del ecosistema de agentes (db-manager + skill db-management) junto con la cadena SDD fue eficiente: los artefactos de gobernanza y los artefactos de ejecucion quedaron alineados en la misma sesion.
- La distincion entre SUPABASE_SERVICE_KEY (para conexion de pipeline via supabase-py/psycopg2) y Personal Access Token de Supabase (para MCP de introspección) fue clarificada y documentada antes de iniciar implementacion. Esto evito confusion potencial en tareas futuras.
- Registrar en el task list la configuracion del MCP como una tarea explicita (TSK-2-15) en lugar de tratarla como prerequisito previo fue una decision correcta: desbloquea el inicio de la etapa sin depender de una configuracion externa.

**Lo que no funciono / friccion encontrada:**
- Las credenciales de Supabase (SUPABASE_URL + SUPABASE_SERVICE_KEY) no fueron entregadas por el cliente antes del cierre de sesion. Esto bloquea todas las tareas de conectividad (TSK-2-02 en adelante). La sesion cerro con documentacion completa pero implementacion en 0%.
- El skill-router no estaba actualizado con el nuevo agente db-manager al momento de su creacion — requirio actualizacion manual como paso adicional al flujo de creacion de agentes.

**Decisiones clave tomadas:**
- Credenciales Supabase van en `pipeline/.env` con las variables SUPABASE_URL y SUPABASE_SERVICE_KEY. El archivo .env ya esta en .gitignore — no hay riesgo de exposicion.
- El agente db-manager es el unico autorizado para operaciones de BD en el proyecto. Ninguna logica de BD debe ejecutarse fuera de este agente o su skill asociado.
- MCP de Supabase es el canal preferido para introspección una vez configurado. Mientras no este disponible, se opera con supabase-py o psycopg2 directamente.
- TSK-2-01 (crear .venv e instalar dependencias) puede ejecutarse sin credenciales — es el primer paso ejecutable al iniciar la proxima sesion.
- Los planes de agentes futuros (pipeline-tester, pipeline-coder, pipeline-reviewer, web-tester, web-coder, web-reviewer, code-debugger) fueron registrados en el handoff para no perder el contexto del usuario — se ejecutaran en etapas correspondientes.
