
import pandas as pd

# ALERTACHOCO-AI
# Comparacion de dias con y sin inundaciones

lluvias = pd.read_csv(
    "data/processed/precipitacion_bellavista_procesada.csv"
)

eventos = pd.read_csv(
    "data/processed/lluvias_inundaciones_bojaya.csv"
)

lluvias["Fecha"] = pd.to_datetime(lluvias["Fecha"]).dt.normalize()
eventos["FECHA"] = pd.to_datetime(eventos["FECHA"]).dt.normalize()

# Fechas unicas de inundacion
fechas_inundacion = set(eventos["FECHA"].dropna())

# Identificar dias con y sin inundacion reportada
lluvias["INUNDACION_REPORTADA"] = (
    lluvias["Fecha"].isin(fechas_inundacion)
)

columnas = [
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]

print("=== COMPARACION DE LLUVIAS EN BOJAYA ===")

print("Dias con inundacion reportada:",
      lluvias["INUNDACION_REPORTADA"].sum())

print("Dias sin inundacion reportada:",
      (~lluvias["INUNDACION_REPORTADA"]).sum())

for columna in columnas:
    print(f"=== {columna} ===")

    resumen = lluvias.groupby(
        "INUNDACION_REPORTADA"
    )[columna].agg(["count", "mean", "median"])

    print(resumen.round(2).to_string())

print("Analisis finalizado.")
