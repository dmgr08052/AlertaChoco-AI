
import pandas as pd
from pathlib import Path

# PROYECTO ALERTACHOCO-AI
# FASE 8: CALIDAD DE DATOS DE BELLAVISTA

ruta = Path("data/raw/precipitacion_bellavista_2019_2025.csv")

df = pd.read_csv(ruta, sep=None, engine="python")

df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

print("=== CALIDAD DE DATOS IDEAM: BELLAVISTA ===")

print("Registros:", len(df))
print("Fechas invalidas:", df["Fecha"].isna().sum())
print("Valores nulos:", df["Valor"].isna().sum())
print("Fechas duplicadas:", df["Fecha"].duplicated().sum())
print("Valores negativos:", (df["Valor"] < 0).sum())

print("=== COBERTURA TEMPORAL ===")

inicio = df["Fecha"].min()
fin = df["Fecha"].max()

print("Fecha inicial:", inicio)
print("Fecha final:", fin)

dias_esperados = pd.date_range(inicio, fin, freq="D")
dias_registrados = pd.DatetimeIndex(df["Fecha"].dropna().unique())
dias_faltantes = dias_esperados.difference(dias_registrados)

print("Dias sin registro:", len(dias_faltantes))
print("Fechas faltantes:", dias_faltantes.tolist())

print("=== RESUMEN ANUAL ===")

df["ANIO"] = df["Fecha"].dt.year

resumen = df.groupby("ANIO").agg(
    dias_registrados=("Fecha", "nunique"),
    precipitacion_total_mm=("Valor", "sum"),
    precipitacion_maxima_mm=("Valor", "max"),
    precipitacion_promedio_mm=("Valor", "mean")
)

print(resumen.round(2).to_string())

print("Analisis finalizado.")
