
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# Evaluacion de viabilidad del modelo predictivo

entrada = Path("data/processed/dataset_experimental_bojaya.csv")
df = pd.read_csv(entrada)

variables = [
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]

total = len(df)
positivos = int(df["INUNDACION_REPORTADA"].sum())
sin_reporte = total - positivos

print("=== EVALUACION DE VIABILIDAD DE IA ===")
print("Total de observaciones:", total)
print("Fechas con reporte:", positivos)
print("Fechas sin reporte:", sin_reporte)
print("Proporcion con reporte:", round(positivos / total * 100, 2), "%")

print("Valores faltantes:")
print(df[variables].isna().sum().to_string())

print("=== DIAGNOSTICO ===")

if positivos < 30:
    print("MUESTRA POSITIVA MUY REDUCIDA")
    print("No se recomienda entrenar un modelo predictivo confiable.")
else:
    print("Se requiere validar la calidad de las etiquetas y los datos.")

print("LIMITACIONES:")
print("- Los dias sin reporte no son negativos verificados.")
print("- La lluvia no explica por si sola todas las inundaciones.")
print("- Faltan niveles de rios y otras variables hidrologicas.")
print("- Se necesita validacion temporal y geografica.")

print("RECOMENDACION:")
print("Continuar con un prototipo exploratorio de indicadores de lluvia.")
print("Ampliar los registros antes de validar un modelo de IA.")

print("Evaluacion finalizada.")
