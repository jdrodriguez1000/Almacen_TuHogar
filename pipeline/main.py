# pipeline/main.py
#
# Gateway / Switcher del Pipeline de Datos — Almacén MultiTodo
# Desarrollado por: Triple S (Sabbia Solutions & Services)
#
# Este archivo es el punto de entrada principal del pipeline. En etapas posteriores
# recibirá un argumento --mode con uno de tres valores:
#
#   validate  → Ejecuta el pipeline de validación del Data Contract (Etapa 3.1)
#   etl       → Ejecuta el ETL Bronze → Silver (Etapa 3.2) y Silver → Gold (Etapa 3.3)
#   alerts    → Ejecuta el motor de alertas determinísticas (Etapa 3.5)
#
# Ejemplo de uso (futuro):
#   python pipeline/main.py --mode validate
#   python pipeline/main.py --mode etl
#   python pipeline/main.py --mode alerts
#
# IMPORTANTE: Este archivo no contiene lógica de negocio. La lógica atómica
# reside en pipeline/src/. Los orquestadores en pipeline/pipelines/.
#
# Etapa de implementación: 3.1 (validate), 3.2-3.3 (etl), 3.5 (alerts)
# Estado actual: PLACEHOLDER — sin código ejecutable (Etapa 1.1)
