
import pandas as pd
from pathlib import Path

# Proyecto: AlertaChocó AI
# Etapa 1: Exploración inicial del dataset UNGRD

ruta = Path(__file__).resolve().parents[1] / "data" / "raw" / "Emergencias_UNGRD_V2_20261105.csv"

# Cargar el dataset original
df = pd.read_csv(ruta, low_memory=False)

# Información general
print("=== ALERTACHOCÓ AI ===")
print("Dimensiones:", df.shape)

print("\nPrimeros registros:")
print(df.head())

print("\nInformación de columnas:")
df.info()

print("\nValores nulos por columna:")
print(df.isnull().sum())

print("\nFilas duplicadas:")
print(df.duplicated().sum())

print("\nNombres de columnas:")
print(df.columns.tolist())
