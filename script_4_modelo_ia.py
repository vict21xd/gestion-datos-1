import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve

# 1. CONEXIÓN A LA BASE DE DATOS DOCKER (Capa Gold)
print("Conectando a PostgreSQL...")
engine = create_engine('postgresql://admin:adminpassword@localhost:5432/google_trends_db')
query = "SELECT * FROM international_top_terms_cl"
df = pd.read_sql(query, engine)

# 2. PREPROCESAMIENTO Y CREACIÓN DE LA VARIABLE OBJETIVO (Fase 2)
# Si el score es mayor a 75, es "Alta Tendencia" (1), sino (0).
df['alta_tendencia'] = np.where(df['score'] > 75, 1, 0)

# Ingeniería de características (Features)
# No podemos usar el 'score' para predecir 'alta_tendencia' porque sería trampa (Data Leakage).
# Usaremos el 'rank' y extraeremos el mes de la fecha para ver si hay estacionalidad.
df['week'] = pd.to_datetime(df['week'])
df['mes'] = df['week'].dt.month
df['largo_termino'] = df['term'].apply(len) # Qué tan larga es la palabra buscada

# 3. ANÁLISIS EXPLORATORIO 
print("\nGenerando Matriz de Correlación...")
columnas_numericas = ['rank', 'mes', 'largo_termino', 'alta_tendencia']
plt.figure(figsize=(8, 6))
sns.heatmap(df[columnas_numericas].corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Matriz de Correlación de Variables")
plt.savefig('matriz_correlacion.png') # Guarda el gráfico para el informe
plt.close()

# 4. ENTRENAMIENTO DEL MODELO 
X = df[['rank', 'mes', 'largo_termino']] # Variables predictoras
y = df['alta_tendencia']                 # Lo que queremos adivinar

# Dividir en datos de entrenamiento (80%) y prueba (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nEntrenando modelo Random Forest...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# 5. PREDICCIONES Y MÉTRICAS DE DESEMPEÑO
y_pred = modelo.predict(X_test)
y_prob = modelo.predict_proba(X_test)[:, 1] # Probabilidades para la Curva ROC

print("\n--- MATRIZ DE CONFUSIÓN ---")
print(confusion_matrix(y_test, y_pred))

print("\n--- REPORTE DE CLASIFICACIÓN (Accuracy, Precision, Recall, F1) ---")
print(classification_report(y_test, y_pred))

# Calcular AUC y Gini
auc = roc_auc_score(y_test, y_prob)
gini = 2 * auc - 1
print(f"\n--- MÉTRICAS AVANZADAS ---")
print(f"AUC (Área bajo la curva ROC): {auc:.3f}")
print(f"Coeficiente de GINI: {gini:.3f}")

# Graficar Curva ROC (Requisito para el informe)
fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'Curva ROC (AUC = {auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('Tasa de Falsos Positivos')
plt.ylabel('Tasa de Verdaderos Positivos (Recall)')
plt.title('Curva ROC del Modelo Predictivo')
plt.legend(loc="lower right")
plt.savefig('curva_roc.png')
plt.close()

print("\n¡Proceso de IA finalizado! Gráficos guardados en tu carpeta.")