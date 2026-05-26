# 💪 FitLife Rewards: Ecosistema Tecnológico de Fidelización B2C

Solución integral de retención de clientes diseñada para el sector *Fitness & Wellness*. El sistema automatiza el cálculo de rangos de lealtad (Oro, Plata, Bronce) y asigna bonos promocionales de manera transaccional, consolidando la analítica en tiempo real para la Dirección Comercial. 

Cumple con los requerimientos técnicos del **Taller 12 (Dashboard BI)** y el **Taller Final Corte 3 (Ecosistema E2E)**.

## 👥 Ingeniería y Desarrollo
* **María Juliana** (Arquitectura de Base de Datos y Lógica Backend / Analítica)
* **Mariana Carmona** (Diseño de Interfaz Tkinter e Integración Frontend / Modelado DAX)

## 🏗️ Estructura Técnica (Taller Final Corte 3)
* **Capa Backend (`database.py`):** Motor relacional SQLite3 estructurado bajo un Modelo Estrella (`fact_transacciones`, `dim_clientes`, `dim_sedes`). Ejecuta *Data Seeding* de 5 registros iniciales de manera 100% automatizada.
* **Capa Frontend (`app_fitlife.py`):** GUI transaccional construida en `Tkinter`. Módulos CRUD operativos con persistencia directa en base de datos. Implementa lógica de validación con bloques `try-except` y mitigación de errores mediante `messagebox`.
* **Orquestador:** Archivo raíz `main.py` para la ejecución e inicialización del ecosistema.

## 📊 Inteligencia de Negocios (Taller 12)
* **Integración Robusta (`FitLife_Dashboard.pbix`):** Conectado en vivo a la bóveda SQLite mediante un script nativo de Python (`pandas`), garantizando portabilidad sin errores de rutas estáticas.
* **Modelado DAX:** Integra Tabla Calendario para inteligencia de tiempo, Columnas Calculadas (Categorización de clientes) y métricas DAX avanzadas (`DIVIDE`, `SUM`, `CALCULATE`) para auditar la rentabilidad financiera de los bonos entregados.
* **UI/UX y Toma de Decisiones:** Paleta de colores estratégica. Incluye 6 visualizaciones clave (Mapa de calor, Tendencias, KPIs) y una pestaña de **Q&A - Respuestas de Negocio** que resuelve 4 interrogantes gerenciales críticos.

## 🚀 Instrucciones de Despliegue
1. Clonar este repositorio en su entorno local.
2. Ejecutar `python main.py` para activar la interfaz de usuario y autogenerar la base de datos.
3. Utilizar los módulos de la aplicación para registrar nuevas compras (el sistema calculará el bono según la regla de negocio Oro/Plata/Bronce).
4. Abrir Power BI. Dirigirse a *Transformar Datos*, actualizar la variable `ruta_db` en el origen del script de Python apuntando al archivo de su máquina local. Al presionar **Actualizar** en el menú principal, las métricas reflejarán las nuevas transacciones en tiempo real.
