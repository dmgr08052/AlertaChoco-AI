
import pandas as pd
from pathlib import Path

# ALERTACHOCO-AI
# Comparacion de precipitaciones entre Bellavista y Opogado

ruta = Path("data/processed")

bellavista = pd.read_csv(
    ruta / "lluvias_inundaciones_bojaya.csv"
)

opogado = pd.read_csv(
    ruta / "lluvias_inundaciones_opogado.csv"
)

bellavista["FECHA"] = pd.to_datetime(bellavista["FECHA"])
opogado["FECHA"] = pd.to_datetime(opogado["FECHA"])

columnas = [
    "LLUVIA_PREVIA_3_DIAS",
    "LLUVIA_PREVIA_7_DIAS",
    "LLUVIA_PREVIA_15_DIAS"
]

# Seleccionar y renombrar las variables
b = bellavista[["FECHA"] + columnas].copy()
o = opogado[["FECHA"] + columnas].copy()

b = b.rename(columns={
    c: f"BELLAVISTA_{c}" for c in columnas
})

o = o.rename(columns={
    c: f"OPOGADO_{c}" for c in columnas
})

# Unir ambas estaciones por fecha
comparacion = b.merge(
    o,
    on="FECHA",
    how="outer",
    validate="one_to_one"
).sort_values("FECHA")

print("=== ALERTACHOCO-AI: COMPARACION DE ESTACIONES ===")
print("Fechas analizadas:", len(comparacion))

for dias in [3, 7, 15]:
    col_b = f"BELLAVISTA_LLUVIA_PREVIA_{dias}_DIAS"
    col_o = f"OPOGADO_LLUVIA_PREVIA_{dias}_DIAS"

    validos = comparacion[[col_b, col_o]].dropna()

    print(f"=== ACUMULADOS DE {dias} DIAS ===")
    print("Fechas con ambas estaciones:", len(validos))

    if not validos.empty:
        print("Promedio Bellavista:", round(validos[col_b].mean(), 2))
        print("Promedio Opogado:", round(validos[col_o].mean(), 2))
        print(
            "Diferencia promedio absoluta:",
            round((validos[col_b] - validos[col_o]).abs().mean(), 2)
        )

salida = ruta / "comparacion_estaciones_bojaya.csv"
comparacion.to_csv(salida, index=False)

print("Archivo generado:", salida)
print("Analisis finalizado.")
