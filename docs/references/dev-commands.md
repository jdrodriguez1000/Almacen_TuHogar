# Comandos de Desarrollo

## Configuración

```bash
# Instalar dependencias
npm install                      # Frontend (web/)
pip install -r requirements.txt  # Pipeline (pipeline/)

# Variables de entorno
cp .env.example .env.local       # Frontend
cp .env.example .env             # Pipeline (secrets NO trackeados en git)

# Base de datos
# Sincronizar schema: leer docs/database/schema.sql en Supabase console
```

## Ejecutar

```bash
# Frontend (Next.js) — puerto 3000
npm run dev

# Pipeline (validación → ETL → alertas)
python pipeline/main.py --mode validate
python pipeline/main.py --mode etl
python pipeline/main.py --mode alerts
```

## Pruebas

```bash
# Frontend (Jest)
npm test
npm run test:watch

# Pipeline (TDD obligatorio — tests primero)
pytest pipeline/tests/
pytest pipeline/tests/ -v
pytest pipeline/tests/ --cov
pytest pipeline/tests/ -m integration   # Contra Supabase real
```

## Linting y Formateo

```bash
# Frontend
npm run lint
npm run format

# Pipeline
black pipeline/
ruff check pipeline/
ruff check pipeline/ --fix
```

## Database

```bash
cat docs/database/schema.sql
# Logs: tss_pipeline_log | Cuarentena: tss_cuarentena_*
```
