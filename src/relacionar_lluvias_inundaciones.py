
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

ruta_inundaciones = BASE / "data/processed/inundaciones_choco_consolidado.csv"
ruta_lluvias = BASE / "data/processed/precipitacion_el_carano_procesada.csv"

inundaciones = pd.read_csv(ruta_inundaciones, low_memory=False)
lluvias = pd.read_csv(ruta_lluvias, low_memory=False)

print("=== ALERTACHOCO-AI: CRUCE DE DATOS ===")

print("Columnas de inundaciones:")
print(inundaciones.columns.tolist())

print("Columnas de precipitaciones:")
print(lluvias.columns.tolist())

print("Total de registros de inundaciones:", len(inundaciones))
print("Total de registros de lluvia:", len(lluvias))


# FASE 7 - PASO 2: FILTRAR QUIBDO


# Convertir fechas
inundaciones["FECHA"] = pd.to_datetime(
    inundaciones["FECHA"], errors="coerce"
)

lluvias["Fecha"] = pd.to_datetime(
    lluvias["Fecha"], errors="coerce"
)

# Filtrar inundaciones de Quibdo
inundaciones_quibdo = inundaciones[
    inundaciones["MUNICIPIO"]
    .astype(str)
    .str.strip()
    .str.upper()
    .isin(["QUIBDO", "QUIBDÓ"])
].copy()

# Filtrar periodo disponible del IDEAM
inundaciones_quibdo = inundaciones_quibdo[
    inundaciones_quibdo["FECHA"].between(
        "2020-01-01", "2022-12-31"
    )
]

print("=== INUNDACIONES EN QUIBDO (2020-2022) ===")
print("Total de registros:", len(inundaciones_quibdo))

print("Registros por año:")
print(inundaciones_quibdo["FECHA"].dt.year.value_counts().sort_index())

print("Fechas de inundaciones:")
print(
    inundaciones_quibdo[
        ["FECHA", "MUNICIPIO", "PERSONAS", "FAMILIAS"]
    ].sort_values("FECHA").to_string(index=False)
)

print("Posibles duplicados:")
print(inundaciones_quibdo["DUPLICADO_POTENCIAL"].value_counts(dropna=False))



# FASE 7 - PASO 3: LLUVIAS ANTES DE INUNDACIONES


# Obtener fechas únicas de inundaciones
fechas_eventos = (
    inundaciones_quibdo["FECHA"]
    .dt.normalize()
    .dropna()
    .drop_duplicates()
    .sort_values()
)

# Preparar las fechas de lluvia
lluvias["Fecha"] = lluvias["Fecha"].dt.normalize()

print("=== LLUVIAS ASOCIADAS A FECHAS DE INUNDACION ===")

for fecha in fechas_eventos:
    registro = lluvias[lluvias["Fecha"] == fecha]

    print(f"Fecha de inundacion: {fecha.date()}")

    if registro.empty:
        print("No hay mediciones de lluvia para esta fecha.")
        continue

    fila = registro.iloc[0]

    print("Lluvia del dia:", fila["Valor"], "mm")
    print("Lluvia acumulada 3 dias:", fila["LLUVIA_3_DIAS"], "mm")
    print("Lluvia acumulada 7 dias:", fila["LLUVIA_7_DIAS"], "mm")
    print("Lluvia acumulada 15 dias:", fila["LLUVIA_15_DIAS"], "mm")

    

# FASE 7 - PASO 4: LLUVIAS PREVIAS


print("=== PRECIPITACIONES ANTERIORES A CADA EVENTO ===")

for fecha in fechas_eventos:
    print(f"Fecha de inundacion: {fecha.date()}")

    for dias in [3, 7, 15]:
        inicio = fecha - pd.Timedelta(days=dias)

        periodo = lluvias[
            (lluvias["Fecha"] >= inicio) &
            (lluvias["Fecha"] < fecha)
        ]

        if len(periodo) == dias and periodo["Valor"].notna().all():
            acumulado = periodo["Valor"].sum()
            print(f"Lluvia previa de {dias} dias: {acumulado:.2f} mm")
        else:
            print(f"Lluvia previa de {dias} dias: datos incompletos")



# FASE 7 - PASO 5: COMPARACION GENERAL


print("=== DISTRIBUCION DE LLUVIAS DIARIAS ===")

print("Promedio diario:", round(lluvias["Valor"].mean(), 2), "mm")
print("Mediana diaria:", round(lluvias["Valor"].median(), 2), "mm")

print("Percentiles de lluvia diaria:")
print(
    lluvias["Valor"].quantile([0.50, 0.75, 0.90, 0.95, 0.99])
)

print("Dias con precipitacion mayor a 100 mm:")
print((lluvias["Valor"] > 100).sum())


# FASE 7 - PASO 6: COMPARAR LLUVIAS ACUMULADAS


print("=== PERCENTILES DE LLUVIAS ACUMULADAS ===")

# Ordenar registros por fecha
lluvias_ordenadas = lluvias.sort_values("Fecha").copy()

for dias in [3, 7, 15]:

    # Excluir el dia actual
    acumulados = (
        lluvias_ordenadas["Valor"]
        .shift(1)
        .rolling(window=dias, min_periods=dias)
        .sum()
        .dropna()
    )

    print(f"Acumulados previos de {dias} dias:")
    print("Mediana:", round(acumulados.median(), 2), "mm")
    print("Percentil 90:", round(acumulados.quantile(0.90), 2), "mm")
    print("Percentil 95:", round(acumulados.quantile(0.95), 2), "mm")
    print("Percentil 99:", round(acumulados.quantile(0.99), 2), "mm")
