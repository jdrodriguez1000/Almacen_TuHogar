# Project Scope
## Dashboard de Inteligencia de Negocio — Almacén MultiTodo

**Cliente/Organización:** Almacén MultiTodo
**Elaborado:** 2026-03-26
**Aprobado:** 2026-03-26
**Versión:** 1.0
**Estado:** ✅ Aprobado

---

## 1. Contexto

Almacén MultiTodo es una cadena de comercio minorista con presencia en las principales ciudades de Colombia. Opera **siete sedes activas** distribuidas en Bogotá, Medellín, Cali, Cartagena y Cúcuta, con un horario de atención uniforme de 8:00 AM a 6:00 PM todos los días del año. Su catálogo activo supera los 100 referencias (SKUs), organizados en una jerarquía de familia, categoría y subcategoría.

El negocio genera un volumen importante de transacciones de venta e inventario diariamente en cada sede. La organización cuenta con Supabase como plataforma de base de datos donde carga la información transaccional diariamente. Triple S (Sabbia Solutions & Services) fue contratada para construir una solución que convierta esos datos en decisiones estratégicas, transformando la operación hacia una basada en datos.

---

## 2. Problema u Oportunidad

Hoy, los cuatro gerentes de Almacén MultiTodo toman decisiones sobre inventario, reabastecimiento y estrategia comercial sin información consolidada ni oportuna. Cada gerente accede a los datos de forma fragmentada — o directamente no los accede — lo que genera decisiones reactivas:

- Se descubren los quiebres de stock cuando ya hay pérdida de ventas.
- Los productos con baja rotación se acumulan sin que nadie los detecte a tiempo.
- Las sedes con mejor desempeño no son identificadas como referente para el resto de la red.
- Los márgenes por producto y por sede no se monitorean rutinariamente, dejando expuesta la rentabilidad ante variaciones de costo.

La oportunidad que este proyecto representa es transformar los datos transaccionales que el cliente ya genera y carga diariamente en una fuente de inteligencia de negocio accesible para todos los gerentes, sin necesidad de conocimientos técnicos, y disponible cada mañana antes de que el almacén abra sus puertas.

---

## 3. Objetivo del Proyecto

**Objetivo central:**
Construir un dashboard de inteligencia de negocio que transforme los datos de ventas e inventarios de Almacén MultiTodo en información accionable para la gerencia, de manera que se puedan identificar riesgos y oportunidades de forma sistemática, anticipada y sin dependencia de análisis manuales.

### Objetivos específicos:
- Centralizar y validar la información transaccional diaria de las 7 sedes en una sola plataforma analítica.
- Proveer a los gerentes de una vista consolidada del desempeño de ventas, inventarios y márgenes, filtrable por sede y categoría.
- Clasificar automáticamente los productos según su contribución al ingreso (análisis ABC/Pareto) y actualizar esa clasificación semanalmente.
- Generar alertas automáticas diarias en lenguaje natural que señalen productos en riesgo y oportunidades de crecimiento.
- Garantizar que la información en el dashboard siempre corresponde a jornadas completas y cerradas (datos del día anterior).
- Establecer un contrato formal de datos entre el cliente y Triple S que defina qué información debe entregarse, en qué formato y con qué frecuencia.

---

## 4. Entregables

### Entregable 1: Pipeline de Validación y Procesamiento de Datos

Un proceso automatizado que se ejecuta diariamente a las 3:30 AM hora Colombia (UTC-5, antes de la apertura del almacén) y que recorre tres etapas: validación, transformación y cálculo de indicadores. Este proceso toma los datos cargados por el cliente en la base de datos, verifica que cumplen el contrato de datos acordado, los limpia y estandariza, y calcula todas las métricas que el dashboard necesita mostrar. Si algún dato no cumple el contrato, el proceso lo registra, lo separa del flujo principal y notifica al equipo de Triple S y al cliente con el detalle del problema.

### Entregable 2: Contrato de Datos Cliente–Triple S

Un documento técnico y operativo que especifica con precisión qué tablas debe mantener el cliente, qué campos debe incluir cada registro, qué restricciones de integridad deben cumplirse y en qué ventana horaria deben estar disponibles los datos. Este contrato es el fundamento de toda la cadena de valor: sin datos que cumplan el contrato, el pipeline rechaza la información y el dashboard no se actualiza. El documento incluye también el protocolo de qué pasa cuando hay una violación.

### Entregable 3: Dashboard Web de Inteligencia de Negocio

Una aplicación web accesible desde cualquier navegador que muestra, cada mañana, el estado consolidado del negocio con datos del día anterior. El encabezado siempre indica la fecha exacta a la que corresponden los datos. Los gerentes podrán filtrar la información por sede y categoría, ver el ranking de productos por ventas, identificar los artículos clasificados como A, B o C según su contribución al ingreso, y leer las alertas del día en lenguaje natural y sin tecnicismos. La aplicación carga en menos de 2 segundos y los filtros responden en menos de medio segundo.

### Entregable 4: Sistema de Alertas Inteligentes

Un conjunto de 12 reglas de alerta (6 de riesgo y 6 de oportunidad) que se calculan automáticamente cada día sobre datos de T-1 y se presentan en el dashboard en lenguaje natural. La ventana de análisis por defecto es 7 días completos cerrados (T-1 a T-7). Cada alerta incluye el nombre del producto o sede afectada, el dato que la disparó y una recomendación de acción concreta.

**Alertas Negativas (Riesgos)** — se muestran primero, ordenadas por severidad (Crítico → Alto → Medio):

| Código | Nombre | Condición de activación |
|---|---|---|
| `ALT_NEG_001` | Stock Crítico | `stock_físico < promedio_venta_7d × 3` |
| `ALT_NEG_002` | Rotación Lenta (Clase A/B) | SKU Clase A o B con ventas en 7d < 30% del promedio de su categoría |
| `ALT_NEG_003` | Caída Anómala de Ventas | Ventas del último día < 50% del promedio del mismo día de semana en las últimas 4 semanas |
| `ALT_NEG_004` | Desabastecimiento | `stock_físico = 0` en SKU Clase A o B — **Crítico** |
| `ALT_NEG_005` | Producto Obsoleto | Sin ventas en los últimos 30 días con `stock_físico > 0` |
| `ALT_NEG_006` | Margen Comprimido (Clase A) | `(precio - costo) / precio < 15%` en SKU Clase A |

**Alertas Positivas (Oportunidades)** — se muestran en sección separada "Oportunidades del Día":

| Código | Nombre | Condición de activación |
|---|---|---|
| `ALT_POS_001` | Alta Rotación | Ventas últimos 7d > 150% del promedio histórico del SKU |
| `ALT_POS_002` | Categoría en Crecimiento | Ventas de categoría en 7d > 20% vs mismo período del mes anterior |
| `ALT_POS_003` | Reabastecimiento Exitoso | SKU pasó de stock crítico (<3 días) a saludable (>7 días) en las últimas 24h |
| `ALT_POS_004` | Producto Estratégico | Clase A + margen > 35% + rotación dentro del promedio |
| `ALT_POS_005` | Sede de Alto Rendimiento | Margen operativo de sede > promedio general en 15% |
| `ALT_POS_006` | Equilibrio Óptimo | Clase A + margen > 35% + stock entre 7 y 14 días |

---

## 5. Usuarios

| Perfil | Descripción | Necesidad principal |
|---|---|---|
| Gerente General | Máxima autoridad de la organización. Supervisa el desempeño global de todas las sedes. | Visión consolidada del negocio para decisiones estratégicas y de asignación de recursos. |
| Gerente de Ventas | Responsable del rendimiento comercial de la red de sedes. | Identificar qué productos y sedes están creciendo o decayendo, y actuar antes de perder ventas. |
| Gerente Financiero | Responsable de la rentabilidad y salud financiera del negocio. | Control de márgenes por producto y sede, y visibilidad del capital inmovilizado en inventario. |
| Gerente de Operaciones | Responsable de la eficiencia logística y disponibilidad de producto. | Anticipar quiebres de stock y planificar reabastecimiento antes de que afecte las ventas. |

**Nota importante:** Los cuatro gerentes tienen acceso exactamente a la misma información. No hay restricciones por rol: todos ven el mismo dashboard sin diferenciación de vistas. Esta decisión fue tomada intencionalmente para simplificar la solución y porque la información es estratégica para todos los perfiles de la gerencia por igual.

---

## 6. Criterios de Éxito

El proyecto se considera exitoso cuando los gerentes de Almacén MultiTodo pueden, cada mañana antes de la apertura del almacén, tomar decisiones de reabastecimiento, gestión comercial y control financiero basadas en el dashboard — sin necesidad de solicitar reportes adicionales ni hacer análisis manuales.

### Indicadores:

| Métrica | Situación actual | Situación esperada |
|---|---|---|
| Visibilidad de desempeño de ventas | Fragmentada o inexistente | Dashboard consolidado disponible cada mañana antes de las 8:00 AM COT |
| Detección de quiebres de stock | Reactiva (cuando ya ocurrió) | Anticipada: alerta con ≥3 días de antelación según stock actual y ritmo de ventas |
| Clasificación de productos por importancia | No existe / manual | Clasificación ABC automática recalculada cada lunes sobre los últimos 90 días |
| Tiempo para identificar los 5 SKUs en mayor riesgo | Desconocido / alto | Menos de 1 minuto en el dashboard |
| Reducción de desabastecimiento no planeado | Baseline actual | Reducción del 40% vs. baseline al cierre del proyecto |
| Reducción de productos obsoletos (sin venta >30 días) | Baseline actual | Reducción del 25% vs. baseline al cierre del proyecto |
| Satisfacción de los gerentes con la herramienta | No aplica | Calificación ≥ 4.0/5.0 en encuesta post-implementación |
| Velocidad de carga del dashboard | No aplica | Menos de 2 segundos (P95) |
| Disponibilidad de datos frescos | No aplica | Datos del día anterior disponibles antes de las 8:00 AM COT todos los días |
| Data Quality Score | No aplica | ≥ 98% de registros diarios pasan validaciones sin intervención manual |

---

## 7. Alcance

### ✅ Incluye:
- Pipeline de datos automatizado con tres modos de operación: validación, transformación (ETL) y cálculo de alertas.
- Validación formal de los datos del cliente contra un contrato de datos antes de procesarlos.
- Transformación y almacenamiento de datos en tres capas: Bronze (datos crudos), Silver (datos limpios con zona horaria Colombia) y Gold (métricas e indicadores derivados).
- Clasificación ABC/Pareto automática de productos, recalculada cada lunes sobre los últimos 90 días: Clase A = top 20% de SKUs por valor acumulado de ventas (~80% del revenue); Clase B = siguientes 30% de SKUs (~15% del revenue); Clase C = restantes 50% de SKUs (~5% del revenue).
- 12 reglas de alerta determinísticas (6 negativas + 6 positivas) en lenguaje natural, calculadas diariamente.
- Dashboard web accesible desde navegador con filtros por sede y categoría.
- Monitoreo de márgenes por producto y sede.
- Cobertura de las 7 sedes activas de Almacén MultiTodo en Colombia.
- Gestión de un catálogo de ~100 SKUs con jerarquía familia–categoría–subcategoría.
- Pipeline programado para ejecutarse automáticamente a las 3:30 AM COT todos los días.
- Documentación técnica completa (SDD: PRD, SPEC, Plan, Tareas) por cada etapa del proyecto.
- Registro de errores y cuarentena de datos inválidos con notificación formal al cliente.
- Infraestructura de CI/CD en GitHub Actions para garantizar la calidad del código en cada cambio.

### ❌ NO incluye:
- Modelos de machine learning, pronósticos estadísticos ni predicciones de demanda. Las alertas son reglas determinísticas basadas en umbrales, no inteligencia artificial.
- Captura o generación de datos transaccionales. El cliente es el único responsable de cargar la información en Supabase. Triple S solo consume y procesa los datos entregados.
- Restricciones de acceso por rol de usuario (sin RBAC). Todos los gerentes ven exactamente la misma información.
- Datos del día en curso (T+0). El sistema opera exclusivamente con jornadas cerradas (datos de T-1 hacia atrás).
- Integración con sistemas ERP, POS o cualquier sistema externo del cliente. La única fuente de datos es Supabase.
- Aplicación móvil nativa. El dashboard es una aplicación web responsiva.
- Modificación de las tablas del cliente (`usr_*`). Triple S opera en modo lectura sobre esas tablas.
- Análisis de rentabilidad con datos externos de mercado o benchmarks de industria.

---

## 8. Restricciones y Supuestos

### Restricciones conocidas:
- **Retraso intencional de 24 horas:** Por diseño del sistema, el dashboard nunca muestra datos del día en curso. Solo jornadas completamente cerradas (T-1). Esta restricción es inamovible y protege la integridad de las métricas.
- **Zona horaria Colombia (UTC-5):** Todo el sistema opera en `America/Bogota`. Las conversiones de UTC a COT son obligatorias en cada capa.
- **Prefijos de tablas no negociables:** Tablas del cliente con prefijo `usr_*` (solo lectura para Triple S); tablas internas con prefijo `tss_*` (propiedad y responsabilidad de Triple S).
- **Sin predicciones:** El sistema no incluirá ningún componente de machine learning ni pronóstico estadístico en ninguna de sus fases.
- **Presupuesto:** USD $10,000 para el proyecto completo.
- **Timeline:** 3 meses para go-live en producción.

### Supuestos:
- El cliente tiene acceso a Supabase y puede cargar datos en las tablas `usr_ventas`, `usr_inventario`, `usr_productos` y `usr_sedes` diariamente antes de las 5:30 AM UTC (12:30 AM COT).
- Los datos que el cliente carga corresponden a transacciones reales del almacén, sin duplicados ni manipulaciones externas al sistema del cliente.
- El cliente se compromete a cumplir el contrato de datos definido en la Etapa 1.3 del proyecto como condición de operación del sistema.
- Los cuatro gerentes tienen acceso a internet y a un navegador web moderno para usar el dashboard.
- Las 7 sedes operan bajo el mismo horario (8:00 AM – 6:00 PM COT) sin excepciones relevantes que requieran tratamiento diferenciado en el pipeline.
- El catálogo de productos (~100 SKUs) tiene una tasa de cambio baja y el cliente notifica a Triple S cuando hay altas, bajas o modificaciones significativas.
- El proyecto sigue el modelo de desarrollo por fases y etapas definido en CLAUDE.md, con avance controlado y aprobación explícita del cliente en cada gate.

---

## 9. Próximos Pasos

Este documento es la base para desarrollar los requerimientos detallados (PRD) y especificaciones técnicas del proyecto. La implementación procederá por fases según el cronograma:

- **Fase 1:** Gobernanza y Cimientos (3 etapas)
- **Fase 2:** Prototipado y Validación de Diseño (1 etapa)
- **Fase 3:** Ingeniería de Datos, Integración y Analítica (6 etapas)
- **Fase 4:** Operación y Mejora Continua (3 etapas)

**Timeline estimado:** 3 meses para puesta en producción (go-live).

> **Nota:** Este documento ha sido construido en conjunto con los cuatro gerentes de Almacén MultiTodo (General, Ventas, Financiero y Operaciones). Representa el entendimiento acordado entre Triple S y el cliente. Cambios posteriores a la aprobación deben documentarse formalmente en Control de Cambios.

---

## Firmas de Aprobación

**Por Triple S (Sabbia Solutions & Services):**
Project Manager Triple S
Fecha: _______________

**Por Almacén MultiTodo:**
Gerente General, Almacén MultiTodo
Fecha: _______________
