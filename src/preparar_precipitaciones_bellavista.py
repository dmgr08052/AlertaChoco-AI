
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# Preparacion de precipitaciones de Bellavista

entrada = Path("data/raw/precipitacion_bellavista_2019_2025.csv")
salida = Path("data/processed/precipitacion_bellavista_procesada.csv")

df = pd.read_csv(entrada, sep=None, engine="python")

df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

df = df.dropna(subset=["Fecha", "Valor"])
df = df.sort_values("Fecha")

# Verificar fechas duplicadas antes de procesar
if df["Fecha"].duplicated().any():
    raise ValueError("Existen fechas duplicadas. Revisar antes de continuar.")

# Crear calendario diario completo
df = df.set_index("Fecha").asfreq("D")

# Calcular acumulados anteriores a cada fecha
for dias in [3, 7, 15]:
    df[f"LLUVIA_PREVIA_{dias}_DIAS"] = (
        df["Valor"]
        .shift(1)
        .rolling(window=dias, min_periods=dias)
        .sum()
    )

df = df.reset_index()
df["ANIO"] = df["Fecha"].dt.year

salida.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(salida, index=False)

print("=== PRECIPITACIONES BELLAVISTA ===")
print("Registros:", len(df))
print("Dias sin datos:", df["Valor"].isna().sum())
print("Columnas:", df.columns.tolist())
print("Primeros registros:")
print(df[[
    "Fecha", "Valor",
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]].head(20).to_string(index=False))

print("Archivo generado:", salida)
