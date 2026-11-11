
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

# ALERTACHOCO-AI
# Visualizacion exploratoria de lluvias en Bojaya

entrada = Path("data/processed/dataset_experimental_bojaya.csv")
salida = Path("reports/figures")
salida.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(entrada)

variables = {
    3: "LLUVIA_PREVIA_3_DIAS",
    7: "LLUVIA_PREVIA_7_DIAS",
    15: "LLUVIA_PREVIA_15_DIAS"
}

for dias, columna in variables.items():

    sin_reporte = df.loc[
        df["INUNDACION_REPORTADA"] == 0, columna
    ].dropna()

    con_reporte = df.loc[
        df["INUNDACION_REPORTADA"] == 1, columna
    ].dropna()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(
        [sin_reporte, con_reporte],
        tick_labels=["Sin reporte", "Con reporte"],
        showfliers=False
    )

    ax.set_title(
        f"Bojaya: precipitacion previa de {dias} dias"
    )
    ax.set_ylabel("Precipitacion acumulada (mm)")
    ax.set_xlabel("Estado del reporte de inundacion")
    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()

    archivo = salida / f"patrones_lluvia_{dias}_dias.png"
    fig.savefig(archivo, dpi=150)
    plt.close(fig)

    print("Grafico generado:", archivo)

print("Visualizaciones finalizadas.")
