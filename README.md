# 📈 Pipeline DataOps: Análisis de Google Trends

## 1. Descripción del Proyecto
Este proyecto es una demostración práctica de un flujo de trabajo **DataOps**. Implementa un pipeline ETL (Extracción, Transformación y Carga) automatizado en Python que conecta un origen de datos en la nube (BigQuery) con una base de datos local en contenedor (PostgreSQL).

El objetivo es extraer los términos de búsqueda internacionales de Google Trends (filtrados por Chile), aplicar reglas de calidad de datos y cargar la información limpia lista para su análisis.

## 2. Arquitectura y Tecnologías
* **Origen de Datos:** Google Cloud BigQuery (Dataset público `google_trends`).
* **Procesamiento:** Python (Pandas, SQLAlchemy, Google Cloud BigQuery API).
* **Destino:** Base de datos PostgreSQL alojada en un contenedor Docker.
* **Control de Versiones:** Git y GitHub.

## 3. Estructura del Repositorio
La estructura del código refleja las distintas etapas del pipeline:

📦 Gestion-de-datos-ia
 ┣ 📜 script_1_limpieza.py    # (Actividad 2.2.2) Ingesta desde BigQuery, limpieza de nulos y estandarización.
 ┣ 📜 script_2_validacion.py  # (Actividad 2.3.2) Validación semántica (ej. scores entre 0 y 100).
 ┣ 📜 script_3_carga_db.py    # (Actividad 2.4.2) Conexión a Docker e inserción en PostgreSQL.
 ┣ 📜 docker-compose.yml      # Configuración del contenedor de la base de datos local.
 ┣ 📜 .gitignore              # Protección de credenciales JSON y datos locales.
 ┗ 📜 README.md               # Documentación principal.

*(Nota: Las carpetas de datos locales `data/raw`, `data/processed`, `data/validated` y `data/reports` son generadas automáticamente por el Script 1 en tiempo de ejecución para mantener el repositorio limpio de archivos pesados).*

## 4. Instrucciones de Ejecución
Para reproducir este entorno de forma local:

1. Clonar el repositorio.
2. Posicionar su llave de servicio de Google Cloud (`credenciales.json`) en la raíz del proyecto.
3. Levantar la base de datos ejecutando: `docker-compose up -d`
4. Ejecutar el pipeline en orden:
   - `python script_1_limpieza.py`
   - `python script_2_validacion.py`
   - `python script_3_carga_db.py`