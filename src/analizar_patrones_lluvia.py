
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# Analisis exploratorio de patrones de lluvia en Bojaya

ruta = Path("data/processed/dataset_experimental_bojaya.csv")
df = pd.read_csv(ruta)

variables = [
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]

print("=== ANALISIS DE PATRONES DE LLUVIA ===")

print("Distribucion de reportes:")
print(df["INUNDACION_REPORTADA"].value_counts())

for variable in variables:
    print(f"=== {variable} ===")

    resumen = df.groupby("INUNDACION_REPORTADA")[variable].agg(
        ["count", "mean", "median", "min", "max"]
    )

    print(resumen.round(2).to_string())

    print("Percentiles por grupo:")
    percentiles = df.groupby("INUNDACION_REPORTADA")[
        variable
    ].quantile([0.50, 0.75, 0.90, 0.95])

    print(percentiles.round(2).to_string())

print("Analisis finalizado.")
