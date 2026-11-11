
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# FASE 8: RELACION ENTRE LLUVIAS E INUNDACIONES EN BOJAYA

ruta_inundaciones = Path("data/processed/inundaciones_choco_consolidado.csv")
ruta_lluvias = Path("data/processed/precipitacion_bellavista_procesada.csv")

inundaciones = pd.read_csv(ruta_inundaciones)
lluvias = pd.read_csv(ruta_lluvias)

inundaciones["FECHA"] = pd.to_datetime(
    inundaciones["FECHA"], errors="coerce"
).dt.normalize()

lluvias["Fecha"] = pd.to_datetime(
    lluvias["Fecha"], errors="coerce"
).dt.normalize()

# Seleccionar inundaciones de Bojaya
municipios = ["BOJAYA", "BOJAYÁ"]

bojaya = inundaciones[
    inundaciones["MUNICIPIO"]
    .astype(str)
    .str.strip()
    .str.upper()
    .isin(municipios)
].copy()

# Evitar contar varias veces la misma fecha
eventos = bojaya.drop_duplicates(subset=["FECHA"]).copy()

# Relacionar fechas de inundaciones con lluvias
resultado = eventos.merge(
    lluvias[[
        "Fecha",
        "Valor",
        "LLUVIA_PREVIA_3_DIAS",
        "LLUVIA_PREVIA_7_DIAS",
        "LLUVIA_PREVIA_15_DIAS"
    ]],
    left_on="FECHA",
    right_on="Fecha",
    how="left"
)

columnas = [
    "FECHA",
    "MUNICIPIO",
    "Valor",
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]

print("=== ALERTACHOCO-AI: BOJAYA ===")
print("Registros originales:", len(bojaya))
print("Fechas distintas:", len(eventos))
print("=== LLUVIAS ANTERIORES A INUNDACIONES ===")
print(resultado[columnas].to_string(index=False))

# Guardar resultado
salida = Path("data/processed/lluvias_inundaciones_bojaya.csv")
salida.parent.mkdir(parents=True, exist_ok=True)

resultado[columnas].to_csv(salida, index=False)

print("Archivo generado:", salida)
