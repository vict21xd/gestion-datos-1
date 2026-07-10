import pandas as pd
from sqlalchemy import create_engine

print("--- ETAPA 3: CARGA A POSTGRESQL ---")
df = pd.read_csv('data/validated/tendencias_validated.csv')

# 1. Conexión a la Base de Datos PostgreSQL local (Docker)
# Formato: postgresql://usuario:contraseña@host:puerto/nombre_bd
engine = create_engine('postgresql://admin:adminpassword@localhost:5432/google_trends_db')

# 2. Inserción controlada
try:
    # if_exists='replace' sobreescribe la tabla si ya existe, 'append' agrega filas
    df.to_sql('international_top_terms_cl', engine, if_exists='replace', index=False)
    print(f"✅ CARGA EXITOSA: Se insertaron {len(df)} registros validados en PostgreSQL.")
except Exception as e:
    print("❌ Error crítico durante la carga a la base de datos:")
    print(e)