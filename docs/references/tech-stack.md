# Stack Tecnológico

## Capa de Presentación (Frontend)
- **Framework**: Next.js (React) con App Router.
- **Lenguaje**: TypeScript.
- **Gestión de Estado**: TanStack Query (React Query).
- **Estilos**: Tailwind CSS + Shadcn/ui.

## Capa de Lógica y Procesamiento (Backend)
- **API**: Node.js (Next.js API Routes).
- **Microservicios**: Python (FastAPI). Ciencia de Datos, cálculos pesados.
- **Validación de Datos**: Zod.

## Capa de Datos y Seguridad (Persistence)
- **DBMS**: PostgreSQL (en Supabase).
- **Seguridad**: Row Level Security (RLS).
- **Lógica en BD**: SQL/RPC (Stored Procedures).
- **Storage**: Almacenamiento de archivos (PDFs, reportes).

## Ecosistema de Soporte (DevOps)
- **Autenticación**: Supabase Auth (Magic Links, Google, usuario/contraseña).
- **Hosting**: Vercel (Edge Network).
- **CI/CD**: GitHub Actions.
- **Monitoreo**: Sentry (opcional).

## Versiones Mínimas de Runtime

| Tecnología | Versión mínima |
|---|---|
| Python | 3.11+ |
| Node.js | 18 LTS+ |
| npm | 9+ |
| Next.js | 14+ |
| PostgreSQL | 15+ (Supabase) |

```bash
python --version   # >= 3.11
node --version     # >= 18
npm --version      # >= 9
```

## Variables de Entorno

### Pipeline (`pipeline/.env`)
```env
SUPABASE_URL=https://<project>.supabase.co
SUPABASE_SERVICE_KEY=<service_role_key>
NOTIFICATION_EMAIL=<email_tripleS>
PIPELINE_TIMEZONE=America/Bogota
PIPELINE_SCHEDULE=03:30
```

### Frontend (`web/.env.local`)
```env
NEXT_PUBLIC_SUPABASE_URL=https://<project>.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=<anon_key>
```

**Regla**: Nunca commitear `.env` ni `.env.local`. Usar `.env.example` como plantilla.

## Entornos

| Variable | Desarrollo | Producción |
|---|---|---|
| Supabase | Proyecto `dev` | Proyecto `prod` |
| Pipeline schedule | Manual o cron local | GitHub Actions (3:30 AM COT) |
| Frontend URL | `localhost:3000` | Vercel (dominio del cliente) |
| Tests | Contra Supabase dev | CI en GitHub Actions |

**Regla**: Nunca usar `SUPABASE_SERVICE_KEY` de producción en máquina local salvo emergencia P1 aprobada.

## Recursos Externos

- [Supabase Docs](https://supabase.com/docs) — PostgreSQL, Auth, RLS, Storage.
- [Next.js Docs](https://nextjs.org/docs) — App Router, API Routes, deployment.
- [FastAPI Docs](https://fastapi.tiangolo.com/) — Python microservicios.
- [Pandera Docs](https://pandera.readthedocs.io/) — Validación de esquemas de datos.
- GitHub — Control de versión y CI/CD.
- Vercel — Hosting frontend.
