import pandas as pd
import os

print("--- ETAPA 2: VALIDACIÓN SEMÁNTICA ---")
df = pd.read_csv('data/processed/tendencias_clean.csv')

# 1. Reglas de Validación Semántica
# - El score debe estar entre 0 y 100
# - El rank debe ser mayor a 0
condicion_valida = (df['score'].between(0, 100)) & (df['rank'] > 0)

datos_validos = df[condicion_valida]
errores = df[~condicion_valida]

# 2. Generar Reporte de Errores
if not errores.empty:
    errores.to_csv('data/reports/reporte_errores.csv', index=False)
    print(f"¡Alerta! Se encontraron {len(errores)} registros inválidos. Reporte generado en /data/reports/reporte_errores.csv")
else:
    print("No se encontraron errores semánticos.")

# 3. Guardar datos estrictamente validados
datos_validos.to_csv('data/validated/tendencias_validated.csv', index=False)
print(f"Validación exitosa. {len(datos_validos)} registros listos para la base de datos.")