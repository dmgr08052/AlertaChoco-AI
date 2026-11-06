
import pandas as pd
from pathlib import Path


# ALERTACHOCO-AI
# FASE 4: PREPARACION E INTEGRACION DE DATOS


BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
PROCESSED = BASE / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)

archivos = {
    "Historico_2019_2022": RAW / "Emergencias_UNGRD._20261105.csv",
    "UNGRD_2025": RAW / "Emergencias_UNGRD_V2_20261105.csv",
}

columnas = [
    "FECHA",
    "DEPARTAMENTO",
    "MUNICIPIO",
    "EVENTO",
    "PERSONAS",
    "FAMILIAS",
    "FALLECIDOS",
    "DESAPARECIDOS",
]

resultados = []

for fuente, ruta in archivos.items():

    print(f"=== PROCESANDO {fuente} ===")

    df = pd.read_csv(ruta, dtype=str, low_memory=False)

    # Comprobar columnas requeridas
    faltantes = set(columnas) - set(df.columns)
    if faltantes:
        raise ValueError(
            f"Columnas faltantes en {fuente}: {faltantes}"
        )

    # Seleccionar columnas y conservar procedencia
    df = df[columnas].copy()
    df["FUENTE"] = fuente

    # Normalizar texto para identificar registros
    departamento = (
        df["DEPARTAMENTO"]
        .fillna("")
        .str.strip()
        .str.upper()
    )

    evento = (
        df["EVENTO"]
        .fillna("")
        .str.strip()
        .str.upper()
    )

    # Filtrar inundaciones en Choco
    df = df[
        departamento.isin(["CHOCO", "CHOCÓ"])
        & evento.isin(["INUNDACION", "INUNDACIÓN"])
    ].copy()

    print("Registros filtrados:", len(df))

    # Convertir fechas
    df["FECHA"] = pd.to_datetime(
        df["FECHA"],
        errors="coerce",
        dayfirst=True
    )

    # Convertir valores numericos
    numericas = [
        "PERSONAS",
        "FAMILIAS",
        "FALLECIDOS",
        "DESAPARECIDOS",
    ]

    for columna in numericas:
        valores = (
            df[columna]
            .astype("string")
            .str.strip()
            .str.replace(",", "", regex=False)
        )

        df[columna] = pd.to_numeric(
            valores,
            errors="coerce"
        )

    # Normalizar municipios
    df["MUNICIPIO"] = (
        df["MUNICIPIO"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    # Identificar duplicados sin eliminarlos
    duplicados = df.duplicated(
        subset=columnas,
        keep="first"
    )

    df["DUPLICADO_POTENCIAL"] = duplicados

    print("Duplicados potenciales:", duplicados.sum())
    print("Fechas invalidas:", df["FECHA"].isna().sum())

    resultados.append(df)

# Integrar los dos periodos
consolidado = pd.concat(
    resultados,
    ignore_index=True
)

# Ordenar cronologicamente
consolidado = consolidado.sort_values(
    "FECHA",
    na_position="last"
).reset_index(drop=True)

# Guardar archivo procesado
salida = PROCESSED / "inundaciones_choco_consolidado.csv"

consolidado.to_csv(
    salida,
    index=False,
    encoding="utf-8-sig"
)

print("=== RESUMEN FINAL ===")
print("Total de registros:", len(consolidado))
print("Duplicados potenciales:",
      consolidado["DUPLICADO_POTENCIAL"].sum())
print("Municipios:", consolidado["MUNICIPIO"].nunique())
print("Fecha inicial:", consolidado["FECHA"].min())
print("Fecha final:", consolidado["FECHA"].max())
print("Archivo generado:", salida)
