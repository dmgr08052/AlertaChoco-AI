
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ALERTACHOCO-AI
# FASE 5: ANALISIS Y VISUALIZACION


BASE = Path(__file__).resolve().parents[1]
ARCHIVO = BASE / "data" / "processed" / "inundaciones_choco_consolidado.csv"
SALIDA = BASE / "reports" / "figures"

SALIDA.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(ARCHIVO, low_memory=False)

# Trabajar con registros no marcados como duplicados
df["DUPLICADO_POTENCIAL"] = (
    df["DUPLICADO_POTENCIAL"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("true")
)

df = df[~df["DUPLICADO_POTENCIAL"]].copy()

# Preparar fechas y cifras
df["FECHA"] = pd.to_datetime(df["FECHA"], errors="coerce")
df["ANIO"] = df["FECHA"].dt.year

df["PERSONAS"] = pd.to_numeric(
    df["PERSONAS"], errors="coerce"
)

sns.set_theme(style="whitegrid")

print("=== ALERTACHOCO-AI: VISUALIZACIONES ===")
print("Registros analizados:", len(df))


# GRAFICO 1: INUNDACIONES POR ANIO


por_anio = df.groupby("ANIO").size()

plt.figure(figsize=(10, 5))
por_anio.plot(kind="bar", color="steelblue")

plt.title("Registros de inundaciones en Choco por año")
plt.xlabel("Año")
plt.ylabel("Numero de registros")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(SALIDA / "inundaciones_por_anio.png", dpi=300)
plt.close()


# GRAFICO 2: MUNICIPIOS


municipios = df["MUNICIPIO"].value_counts().head(10)

plt.figure(figsize=(11, 6))
sns.barplot(
    x=municipios.values,
    y=municipios.index,
    color="steelblue"
)

plt.title("10 municipios con mas registros de inundaciones")
plt.xlabel("Numero de registros")
plt.ylabel("Municipio")
plt.tight_layout()

plt.savefig(SALIDA / "inundaciones_por_municipio.png", dpi=300)
plt.close()


# GRAFICO 3: PERSONAS AFECTADAS


personas = df.groupby("ANIO")["PERSONAS"].sum(min_count=1)

plt.figure(figsize=(10, 5))
personas.plot(kind="bar", color="darkorange")

plt.title("Personas afectadas reportadas por año")
plt.xlabel("Año")
plt.ylabel("Personas reportadas")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(SALIDA / "personas_afectadas_por_anio.png", dpi=300)
plt.close()

print("=== RESULTADOS ===")
print("Registros por año:")
print(por_anio)

print("Municipios con más registros:")
print(municipios)

print("Personas afectadas por año:")
print(personas)

print("Graficos guardados en:", SALIDA)
print("Proceso finalizado correctamente.")
