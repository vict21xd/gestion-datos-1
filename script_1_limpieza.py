import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os

print("--- ETAPA 1: INGESTA Y LIMPIEZA DESDE BIGQUERY ---")

# 0. Crear las carpetas automáticamente si no existen
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
os.makedirs('data/validated', exist_ok=True)
os.makedirs('data/reports', exist_ok=True)

try:
    # 1. FORZAR LA LECTURA DEL ARCHIVO JSON DIRECTAMENTE
    credenciales = service_account.Credentials.from_service_account_file('credenciales.json')
    
    project_id = 'lyrical-line-491314-v5'
    
    # Conectamos inyectando la llave
    client = bigquery.Client(credentials=credenciales, project=project_id)
    
    print(f"✅ Autenticado en Google Cloud como: {credenciales.service_account_email}")
    
    # Consulta SQL
    query = """
        SELECT score, rank, country_code, region_code, term, refresh_date, country_name, region_name, week
        FROM `bigquery-public-data.google_trends.international_top_terms`
        WHERE country_name = 'Chile'
        AND week >= '2025-01-01'
    """
    
    print("Descargando datos desde BigQuery...")
    df = client.query(query).to_dataframe()
    
    # Guardamos crudos
    df.to_csv('data/raw/tendencias_raw.csv', index=False)
    print(f"✅ Descarga exitosa: {len(df)} registros crudos en /data/raw/")

    # 2. Limpieza de datos
    print("Limpiando valores nulos y duplicados...")
    df_clean = df.dropna(subset=['score', 'term', 'week']) 
    df_clean = df_clean.drop_duplicates()

    # 3. Transformación
    print("Estandarizando formatos...")
    df_clean['term'] = df_clean['term'].str.strip().str.upper()
    df_clean['week'] = pd.to_datetime(df_clean['week']) 

    # 4. Guardar archivo procesado
    df_clean.to_csv('data/processed/tendencias_clean.csv', index=False)
    print(f"✅ Limpieza finalizada. Datos listos en /data/processed/")

except Exception as e:
    print("❌ Ocurrió un error:")
    print(e)