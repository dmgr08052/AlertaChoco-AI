
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# Evaluacion exploratoria de umbrales de lluvia en Bojaya

ruta = Path("data/processed/dataset_experimental_bojaya.csv")
df = pd.read_csv(ruta)

variables = {
    3: "LLUVIA_PREVIA_3_DIAS",
    7: "LLUVIA_PREVIA_7_DIAS",
    15: "LLUVIA_PREVIA_15_DIAS"
}

print("=== EVALUACION EXPLORATORIA DE UMBRALES ===")

for dias, columna in variables.items():
    print(f"=== LLUVIA PREVIA DE {dias} DIAS ===")

    umbrales = df[columna].quantile([0.75, 0.90, 0.95])

    for percentil, umbral in umbrales.items():
        supera = df[columna] >= umbral
        reportada = df["INUNDACION_REPORTADA"] == 1

        eventos_detectados = (supera & reportada).sum()
        total_eventos = reportada.sum()
        dias_superan = supera.sum()

        cobertura = (
            eventos_detectados / total_eventos * 100
            if total_eventos else 0
        )

        print(
            f"Percentil {percentil:.0%}: "
            f"umbral={umbral:.2f} mm | "
            f"fechas con reporte sobre umbral="
            f"{eventos_detectados}/{total_eventos} | "
            f"cobertura={cobertura:.1f}% | "
            f"dias que superan={dias_superan}"
        )

print("Analisis finalizado.")
