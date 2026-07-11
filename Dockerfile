FROM python:3.10-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todos los archivos de tu proyecto al contenedor
COPY . .

# Instalar las librerías necesarias para tus scripts de IA y Datos
RUN pip install --no-cache-dir pandas numpy scikit-learn matplotlib sqlalchemy psycopg2-binary google-cloud-bigquery


# Comando por defecto que ejecutará Render (corre tu modelo de IA)
CMD ["sh", "-c", "python script_1_limpieza.py && python script_2_validacion.py && python script_3_carga_db.py && python script_4_modelo_ia.py"]
