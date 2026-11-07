
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# FASE 6: ANALISIS DE PRECIPITACIONES IDEAM

BASE = Path(__file__).resolve().parents[1]

archivo = (
    BASE / "data" / "raw"
    / "precipitacion_el_carano_2020_2022.csv"
)

df = pd.read_csv(archivo, sep=None, engine="python")

# Preparar fechas y valores
df["Fecha"] = pd.to_datetime(
    df["Fecha"], errors="coerce"
)

df["Valor"] = pd.to_numeric(
    df["Valor"], errors="coerce"
)

df = df.sort_values("Fecha")

# Evaluar calidad
print("=== CALIDAD DE DATOS IDEAM ===")
print("Registros:", len(df))
print("Fechas invalidas:", df["Fecha"].isna().sum())
print("Valores nulos:", df["Valor"].isna().sum())
print("Fechas duplicadas:", df["Fecha"].duplicated().sum())
print("Valores negativos:", (df["Valor"] < 0).sum())

# Comprobar continuidad diaria
fechas_validas = df["Fecha"].dropna().dt.normalize()

calendario = pd.date_range(
    fechas_validas.min(),
    fechas_validas.max(),
    freq="D"
)

faltantes = calendario.difference(fechas_validas)

print("=== COBERTURA TEMPORAL ===")
print("Fecha inicial:", fechas_validas.min())
print("Fecha final:", fechas_validas.max())
print("Dias sin registro:", len(faltantes))

# Resumen anual
df["ANIO"] = df["Fecha"].dt.year

resumen = df.groupby("ANIO").agg(
    dias_registrados=("Valor", "count"),
    precipitacion_total_mm=("Valor", "sum"),
    precipitacion_maxima_mm=("Valor", "max"),
    precipitacion_promedio_mm=("Valor", "mean")
)

print("=== RESUMEN ANUAL ===")
print(resumen.round(2).to_string())

# Preparar lluvia acumulada
df["LLUVIA_3_DIAS"] = df["Valor"].rolling(
    3, min_periods=3
).sum()

df["LLUVIA_7_DIAS"] = df["Valor"].rolling(
    7, min_periods=7
).sum()

df["LLUVIA_15_DIAS"] = df["Valor"].rolling(
    15, min_periods=15
).sum()

# Guardar resultado
salida = (
    BASE / "data" / "processed"
    / "precipitacion_el_carano_procesada.csv"
)

salida.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(salida, index=False)

print("Archivo generado:", salida)
print("Analisis finalizado correctamente.")
