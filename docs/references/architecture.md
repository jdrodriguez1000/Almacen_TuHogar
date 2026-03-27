# Arquitectura del Sistema

## Flujo de Datos End-to-End

```
┌─────────────────────────────────────────────────────────────────┐
│ CLIENTE: Almacén MultiTodo                                      │
│ Carga datos diarios → Supabase (usr_ventas, usr_inventario...) │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ PIPELINE DE DATOS (Python 3:30 AM COT)                          │
│ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ │
│ │ 1. VALIDACIÓN    │→│ 2. ETL           │→│ 3. ALERTAS       │ │
│ │ Cumplen contrato │ │ Limpieza + TZ    │ │ 12 reglas calc.  │ │
│ │ (Data Contract)  │ │ UTC→COT en Silver│ │ Almacenar gold   │ │
│ └──────────────────┘ └──────────────────┘ └──────────────────┘ │
│ Rechazos → tss_cuarentena_* + notificación al cliente           │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ SUPABASE: Medallion Lakehouse                                   │
│ BRONZE (tss_bronze_*)   → Raw data sin modificar               │
│   ↓                                                             │
│ SILVER (tss_silver_*)   → Datos limpios, validados, COT        │
│   ↓                                                             │
│ GOLD (tss_gold_*)       → Métricas, ABC, alertas               │
│ └─ tss_gold_daily_sales  → Ventas diarias por SKU/sede         │
│ └─ tss_gold_abc_ranking  → Clasificación ABC semanal           │
│ └─ tss_gold_alerts       → 12 alertas calculadas               │
│ └─ tss_pipeline_log      → Logs de ejecución                   │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ NEXT.JS API ROUTES (Node.js)                                    │
│ - Lectura desde tss_gold_* (RLS + Supabase Auth)               │
│ - Validación con Zod                                           │
│ - Cacheo con TanStack Query (cliente)                          │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│ DASHBOARD (Next.js + React + TypeScript)                        │
│ - Vista de ventas, inventarios, ABC, alertas                   │
│ - Filtros por sede y categoría                                 │
│ - Datos de T-1 (día anterior cerrado)                          │
│ - Carga <2s, filtros <500ms                                    │
└─────────────────────────────────────────────────────────────────┘
```

## Capas Analíticas (Medallion Architecture)

| Capa | Tabla | Contenido | Origen | Proceso |
|---|---|---|---|---|
| **Bronze** | `tss_bronze_ventas`, `tss_bronze_inventario` | Datos crudos, sin modificar | `usr_*` del cliente | Copia 1:1 después de validación |
| **Silver** | `tss_silver_ventas`, `tss_silver_inventario` | Datos limpios, normalizados | Bronze | Deduplicación, limpieza, conversión UTC→COT |
| **Gold** | `tss_gold_daily_sales`, `tss_gold_abc_ranking`, `tss_gold_alerts` | Métricas derivadas, indicadores | Silver | Agregaciones, cálculos, clasificación ABC, reglas de alerta |

**Validación en cascada**: Pandera schemas en Silver y Gold aseguran conformidad exacta con Data Contract.

## Componentes Principales

1. **Frontend (Next.js + React)** — App Router, Shadcn/ui, TanStack Query, Tailwind CSS.
2. **API (Next.js API Routes + Node.js)** — Rutas `/api/`, validación Zod, Supabase Auth.
3. **Pipeline (Python)** — `main.py --mode [validate|etl|alerts]`, módulos en `pipeline/src/`, orquestadores en `pipeline/pipelines/`.
4. **Base de Datos (PostgreSQL en Supabase)** — RLS, triggers y funciones SQL, Storage, backups automáticos.
5. **Logging** — `tss_pipeline_log`, archivo local `latest`, `tss_cuarentena_*`.

## Ciclo Diario de Operación

```
00:30 COT (05:30 UTC)  → Cliente completa carga de datos en tablas usr_*
03:30 COT (08:30 UTC)  → Pipeline comienza (validación)
03:45 COT              → ETL: Bronze → Silver → Gold
04:00 COT              → Cálculo de 12 alertas
04:15 COT (09:15 UTC)  → Datos listos en Gold, logs en tss_pipeline_log
                       → ⚠️ Si a las 09:00 UTC el pipeline no completó: alerta interna Triple S
08:00 AM COT           → Dashboard muestra datos T-1 (ayer cerrado)
06:00 PM COT           → Almacén cierra
```

**Garantía**: Si el pipeline falla, `tss_cuarentena_*` captura errores y el cliente es notificado. Dashboard no se actualiza hasta que validación pase 100%.
