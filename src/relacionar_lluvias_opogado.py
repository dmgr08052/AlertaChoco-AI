
import pandas as pd

# ALERTACHOCO-AI
# Relacion entre lluvias de Opogado e inundaciones de Bojaya

inundaciones = pd.read_csv(
    "data/processed/lluvias_inundaciones_bojaya.csv"
)

lluvias = pd.read_csv(
    "data/processed/precipitacion_opogado_procesada.csv"
)

inundaciones["FECHA"] = pd.to_datetime(
    inundaciones["FECHA"], errors="coerce"
).dt.normalize()

lluvias["Fecha"] = pd.to_datetime(
    lluvias["Fecha"], errors="coerce"
).dt.normalize()

columnas = [
    "Fecha",
    "Valor",
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]

# Una fila por fecha de inundacion
eventos = inundaciones.drop_duplicates(
    subset=["FECHA"]
).copy()

resultado = eventos[["FECHA", "MUNICIPIO"]].merge(
    lluvias[columnas],
    left_on="FECHA",
    right_on="Fecha",
    how="left",
    validate="one_to_one"
)

print("=== ALERTACHOCO-AI: OPOGADO ===")
print("Fechas de inundacion:", len(resultado))

print("=== LLUVIAS PREVIAS ===")
print(resultado[[
    "FECHA",
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]].to_string(index=False))

print("=== COBERTURA EN FECHAS DE INUNDACION ===")
for dias in [3, 7, 15]:
    columna = f"LLUVIA_PREVIA_{dias}_DIAS"
    disponibles = resultado[columna].notna().sum()
    print(f"{dias} dias: {disponibles} de {len(resultado)}")

salida = "data/processed/lluvias_inundaciones_opogado.csv"
resultado.to_csv(salida, index=False)

print("Archivo generado:", salida)
print("Analisis finalizado.")
