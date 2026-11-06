
import pandas as pd
from pathlib import Path

# Proyecto: AlertaChoco-AI
# Etapa 4: Comparación de datasets UNGRD

carpeta = Path(__file__).resolve().parents[1] / "data" / "raw"

archivo_historico = carpeta / "Emergencias_UNGRD._20261105.csv"
archivo_2025 = carpeta / "Emergencias_UNGRD_V2_20261105.csv"

df_historico = pd.read_csv(archivo_historico, low_memory=False)
df_2025 = pd.read_csv(archivo_2025, low_memory=False)

print("=== COMPARACIÓN DE DATASETS UNGRD ===")

print("Dataset histórico:")
print("Filas:", len(df_historico))
print("Columnas:", len(df_historico.columns))

print("Dataset 2025:")
print("Filas:", len(df_2025))
print("Columnas:", len(df_2025.columns))

columnas_historico = set(df_historico.columns)
columnas_2025 = set(df_2025.columns)

print("Columnas en común:")
print(sorted(columnas_historico & columnas_2025))

print("Columnas exclusivas del histórico:")
print(sorted(columnas_historico - columnas_2025))

print("Columnas exclusivas de 2025:")
print(sorted(columnas_2025 - columnas_historico))



# ETAPA 5: COLUMNAS COMPARTIDAS


columnas_comunes = sorted(
    columnas_historico & columnas_2025
)

print("=== RESUMEN DE COMPATIBILIDAD ===")
print("Total de columnas comunes:", len(columnas_comunes))

print("Columnas compartidas:")
for columna in columnas_comunes:
    print("-", columna)



# ETAPA 6: VARIABLES IMPORTANTES


palabras_clave = [
    "FECHA",
    "MUNICIPIO",
    "EVENTO",
    "PERSONAS",
    "FAMILIAS",
    "DEPARTAMENTO"
]

print("=== VARIABLES IMPORTANTES ===")

for palabra in palabras_clave:
    print(f"Variable: {palabra}")

    print("Histórico:")
    for columna in df_historico.columns:
        if palabra in columna.upper():
            print(" -", repr(columna))

    print("2025:")
    for columna in df_2025.columns:
        if palabra in columna.upper():
            print(" -", repr(columna))



# ETAPA 7: VERIFICACIÓN DE TIPOS DE DATOS


variables = [
    "FECHA",
    "MUNICIPIO",
    "DEPARTAMENTO",
    "EVENTO",
    "PERSONAS",
    "FAMILIAS"
]

print("=== TIPOS DE DATOS ===")

for variable in variables:
    print(f"Variable: {variable}")

    print("Histórico:", df_historico[variable].dtype)
    print("2025:", df_2025[variable].dtype)

    print("Ejemplo histórico:",
          df_historico[variable].dropna().head(3).tolist())

    print("Ejemplo 2025:",
          df_2025[variable].dropna().head(3).tolist())



# ETAPA 8: VALIDACION DE CONVERSIONES


for nombre, df in [
    ("Historico", df_historico),
    ("2025", df_2025)
]:
    print(f"=== VALIDACION: {nombre} ===")

    fechas = pd.to_datetime(
        df["FECHA"],
        errors="coerce",
        dayfirst=True
    )

    print("Fechas no interpretables:", fechas.isna().sum())
    print("Fecha minima:", fechas.min())
    print("Fecha maxima:", fechas.max())

    for columna in ["PERSONAS", "FAMILIAS"]:
        valores = df[columna].astype("string").str.strip()
        numeros = pd.to_numeric(valores, errors="coerce")

        invalidos = (
            valores.notna()
            & valores.ne("")
            & numeros.isna()
        )

        print(f"{columna}:")
        print("Valores no convertibles:", invalidos.sum())
        print("Ejemplos:", valores[invalidos].head(5).tolist())



# ETAPA 9: REVISION DE FORMATOS NUMERICOS


for nombre, df in [
    ("Historico", df_historico),
    ("2025", df_2025)
]:
    print(f"=== FORMATOS NUMERICOS: {nombre} ===")

    for columna in ["PERSONAS", "FAMILIAS"]:
        valores = df[columna].astype("string").str.strip()

        con_coma = valores.str.contains(",", regex=False, na=False)

        formato_miles = valores.str.fullmatch(
            r"\d{1,3}(,\d{3})+",
            na=False
        )

        print(f"Columna: {columna}")
        print("Valores con coma:", con_coma.sum())
        print("Formato de miles:", formato_miles.sum())
        print(
            "Otros formatos con coma:",
            (con_coma & ~formato_miles).sum()
        )
        print(
            "Ejemplos de otros formatos:",
            valores[con_coma & ~formato_miles].head(5).tolist()
        )
