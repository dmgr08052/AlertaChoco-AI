
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

print("Primeros registros:")
print(df.head())

print("Información de columnas:")
df.info()

print("Valores nulos por columna:")
print(df.isnull().sum())

print("Filas duplicadas:")
print(df.duplicated().sum())

print("Nombres de columnas:")
print(df.columns.tolist())


# ETAPA 2: ANÁLISIS DE EMERGENCIAS EN EL CHOCÓ


# Filtrar registros del departamento del Chocó
df_choco = df[
    df["DEPARTAMENTO"].astype(str).str.strip().str.upper() == "CHOCO"
].copy()

print("=== EMERGENCIAS EN EL CHOCÓ ===")
print("Total de registros:", len(df_choco))

# Identificar los tipos de eventos registrados
print("Tipos de emergencias:")
print(df_choco["EVENTO"].value_counts())

# Filtrar inundaciones
df_inundaciones = df_choco[
    df_choco["EVENTO"].astype(str).str.strip().str.upper().isin(
        ["INUNDACION", "INUNDACIÓN"]
    )
].copy()

print("=== INUNDACIONES EN EL CHOCÓ ===")
print("Registros de inundaciones:", len(df_inundaciones))

# Identificar municipios afectados
print("Inundaciones por municipio:")
print(df_inundaciones["MUNICIPIO"].value_counts())

# Revisar duplicados sin eliminarlos
print("Filas duplicadas de inundaciones:")
print(df_inundaciones.duplicated().sum())




