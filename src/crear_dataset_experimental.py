
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# Construccion del dataset experimental de Bojaya

base = Path("data/processed")

lluvias = pd.read_csv(
    base / "precipitacion_bellavista_procesada.csv"
)

eventos = pd.read_csv(
    base / "lluvias_inundaciones_bojaya.csv"
)

lluvias["Fecha"] = pd.to_datetime(
    lluvias["Fecha"], errors="coerce"
).dt.normalize()

eventos["FECHA"] = pd.to_datetime(
    eventos["FECHA"], errors="coerce"
).dt.normalize()

columnas = [
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]

# Conservar dias con mediciones completas
datos = lluvias.dropna(
    subset=["Fecha"] + columnas
).copy()

# Identificar fechas de inundacion reportada
fechas_eventos = set(eventos["FECHA"].dropna())

datos["INUNDACION_REPORTADA"] = (
    datos["Fecha"].isin(fechas_eventos).astype(int)
)

# Seleccionar variables
datos = datos[
    ["Fecha"] + columnas + ["INUNDACION_REPORTADA"]
].sort_values("Fecha")

salida = base / "dataset_experimental_bojaya.csv"
datos.to_csv(salida, index=False)

print("=== DATASET EXPERIMENTAL BOJAYA ===")
print("Total de registros:", len(datos))
print("Fechas con inundacion reportada:",
      datos["INUNDACION_REPORTADA"].sum())
print("Fechas sin reporte:",
      (datos["INUNDACION_REPORTADA"] == 0).sum())

print("Primeros registros:")
print(datos.head().to_string(index=False))

print("Archivo generado:", salida)
print("Proceso finalizado.")
