---
name: git-push
description: "Sube el repositorio a GitHub respetando el Git Flow del proyecto (feat/* → main vía PR con CI). Maneja tanto la configuración inicial del remoto como pushes de ramas individuales y creación de Pull Requests. USAR cuando el usuario quiera subir código a GitHub, configurar el remoto por primera vez, crear una PR, o seguir el flujo de ramas definido en CLAUDE.md §6. Disparar ante frases como 'sube a GitHub', 'push', 'subir al repositorio', 'configura el remoto', 'publicar rama', 'crear PR', 'abrir pull request'."
invocation: user
triggers:
  - git push
  - push
  - subir a github
  - sube a github
  - subir al repositorio
  - publicar rama
  - configurar remoto
  - setup github
  - crear pr
  - abrir pull request
  - pull request
---

# Skill: /git-push

Gestiona el push al repositorio GitHub respetando estrictamente el **Git Flow de Triple S** definido en `CLAUDE.md §6`.

---

## Reglas de Oro (leer antes de ejecutar cualquier paso)

Este proyecto usa un flujo de **dos ramas permanentes**. La simplicidad es intencional: reduce fricción operativa y mantiene `main` siempre en estado desplegable.

| Rama | Tipo | Regla clave |
|---|---|---|
| `main` | Principal | Recibe merges solo desde `feat/*` vía PR + CI aprobado. Código ejecutable solo entra por PR, nunca por push directo. |
| `feat/*` | Desarrollo | Una rama por feature o cambio. Push libre. Merge a `main` solo después de que el CI Quality Gate pase. |

**Flujo único permitido:** `feat/*` → PR → CI ✅ → merge a `main`

**Formato de commits (en español):**
- `feat:` nueva funcionalidad
- `fix:` corrección de errores
- `docs:` documentación (SDD, CLAUDE.md, resúmenes ejecutivos)
- `refactor:` cambios sin nuevas funciones ni correcciones

---

## Paso 1 — Diagnóstico del repositorio

Ejecuta estos comandos para entender el estado actual antes de hacer cualquier cosa:

```bash
git remote -v
git branch -a
git status
git log --oneline -5
```

Con los resultados, determina:

- **¿Existe el remoto `origin`?** → Si no, ir a **Paso 2A**. Si sí, ir a **Paso 2B**.
- **¿Qué rama está activa?** → Validar contra las reglas de oro.
- **¿Hay cambios sin commitear?** → Si los hay, alertar y detenerse. No hacer push con working tree sucio.

---

## Paso 2A — Configuración inicial (remoto no existe)

> Usar cuando el repositorio nunca ha sido subido a GitHub.

**2A.1 — Solicitar URL del repositorio:**

```
¿Cuál es la URL del repositorio GitHub?
Ejemplo: https://github.com/usuario/nombre-repo.git
```

**2A.2 — Agregar el remoto y verificar ramas:**

```bash
git remote add origin [URL_PROPORCIONADA]
git branch
```

Solo se necesitan dos ramas permanentes: `main` (debe existir) y `feat/*` (se crean según necesidad). No crear ramas adicionales.

**2A.3 — Push inicial:**

Solicitar confirmación explícita antes de ejecutar:

```
Estoy por subir las siguientes ramas a GitHub origin:
  → main  (rama principal: docs + código de producción)

¿Confirmas?
```

```bash
git push -u origin main
```

> Si hay ramas `feat/*` activas, preguntar al usuario si también desea subirlas.

---

## Paso 2B — Push a repositorio ya configurado

> Usar cuando `origin` ya existe.

**2B.1 — Identificar la rama activa y validar:**

| Rama activa | Acción | Consideración |
|---|---|---|
| `main` | Push directo permitido | Solo si los cambios son **documentación o gobernanza** (`docs:` commits). Si hay código ejecutable, debe venir por PR. |
| `feat/*` | Push a remota | Normal. Luego crear PR hacia `main` si el trabajo está listo. |

**2B.2 — Si la rama es `feat/*` y el trabajo está listo para integrar:**

Antes de crear la PR, verificar que el branch está actualizado:

```bash
git fetch origin
git rebase origin/main   # o git merge origin/main si se prefiere merge commit
```

Luego crear la Pull Request:

```bash
gh pr create \
  --base main \
  --title "[feat/fix/docs/refactor]: descripción breve" \
  --body "$(cat <<'EOF'
## Qué hace este cambio
[Descripción en 2-3 líneas]

## Cómo probarlo
- [ ] pytest pipeline/tests/
- [ ] npm test
- [ ] Verificar en local con npm run dev

🤖 Generado con Claude Code
EOF
)"
```

> El CI Quality Gate corre automáticamente al abrir la PR. El merge a `main` requiere que CI pase y que haya aprobación humana.

**2B.3 — Ejecutar el push:**

```bash
git push origin [rama-activa]
```

Si la rama no tiene upstream configurado:

```bash
git push -u origin [rama-activa]
```

---

## Paso 3 — Verificación post-push

Después de cada push exitoso:

```bash
git log --oneline origin/[rama] -3
```

Confirmar al usuario:

```
✅ Push completado.
   Rama:               [nombre]
   Último commit:      [hash] [mensaje]
   URL remoto:         [url]
   [Si es feat/*]:     ¿Quieres abrir una PR hacia main ahora?
```

---

## Paso 4 — Errores comunes y resolución

| Error | Causa | Solución |
|---|---|---|
| `rejected — non-fast-forward` | El remoto tiene commits que no tienes localmente | Ejecutar `git pull origin [rama] --rebase` primero. **Nunca usar `--force` sin confirmar con el usuario.** |
| `fatal: remote origin already exists` | El remoto ya está configurado | Verificar con `git remote -v` y usar la URL existente |
| `error: src refspec [rama] does not match any` | La rama no existe localmente | Crearla con `git checkout -b [rama]` primero |
| `Permission denied (publickey)` | Autenticación SSH fallida | Verificar clave SSH en GitHub, o cambiar a HTTPS |
| `gh: command not found` | GitHub CLI no instalado | Usar la interfaz web de GitHub para crear la PR manualmente |

---

## Restricciones absolutas

- **Prohibido** usar `git push --force` hacia `main` sin advertencia explícita al usuario y su aprobación.
- **Prohibido** hacer push directo de código ejecutable (Python, JS, etc.) a `main`. Siempre vía PR.
- **Prohibido** mergear `feat/*` → `main` sin que el CI Quality Gate haya pasado.
- Si el usuario pide saltarse el flujo, mostrar la advertencia y esperar confirmación antes de proceder.
