
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# Preparacion de precipitaciones de Opogado

entrada = Path("data/raw/precipitacion_opogado_2019_2025.csv")
salida = Path("data/processed/precipitacion_opogado_procesada.csv")

df = pd.read_csv(entrada)

# Seleccionar solamente la estacion Opogado
df = df[
    pd.to_numeric(df["CodigoEstacion"], errors="coerce") == 11090010
].copy()

df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

print("=== ALERTACHOCO-AI: ESTACION OPOGADO ===")
print("Registros:", len(df))
print("Fechas invalidas:", df["Fecha"].isna().sum())
print("Valores nulos:", df["Valor"].isna().sum())
print("Valores negativos:", (df["Valor"] < 0).sum())
print("Fechas duplicadas:", df["Fecha"].duplicated().sum())

# Organizar cronologicamente
df = df.dropna(subset=["Fecha"])
df = df.sort_values("Fecha")

# Crear calendario diario completo
df = df.set_index("Fecha")
calendario = pd.date_range(
    start=df.index.min(),
    end=df.index.max(),
    freq="D"
)

df = df.reindex(calendario)
df.index.name = "Fecha"

print("Dias sin registros:", df["Valor"].isna().sum())

# Calcular lluvia de los dias anteriores
# shift(1) evita incluir la lluvia del dia del evento
for dias in [3, 7, 15]:
    df[f"LLUVIA_PREVIA_{dias}_DIAS"] = (
        df["Valor"]
        .shift(1)
        .rolling(window=dias, min_periods=dias)
        .sum()
    )

df["ANIO"] = df.index.year

# Guardar archivo procesado
salida.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(salida)

print("=== PRIMEROS REGISTROS ===")
print(df[[
    "Valor",
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]].head(20).to_string())

print("Archivo generado:", salida)
print("Analisis finalizado.")
