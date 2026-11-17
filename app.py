
import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración general
st.set_page_config(
    page_title="AlertaChoco-AI",
    page_icon="🌧️",
    layout="wide"
)

# Encabezado
st.title("🌧️ AlertaChoco-AI")
st.subheader("Análisis histórico de inundaciones en el Chocó")

st.info(
    "Proyecto académico de ciencia de datos. "
    "Los resultados son exploratorios y no constituyen "
    "alertas oficiales ni predicciones validadas."
)

st.divider()

# Cargar información experimental
ruta = (
    Path(__file__).resolve().parent
    / "data"
    / "processed"
    / "dataset_experimental_bojaya.csv"
)

if ruta.exists():
    df = pd.read_csv(ruta)

    total_dias = len(df)
    dias_reportados = int(df["INUNDACION_REPORTADA"].sum())
    dias_sin_reporte = total_dias - dias_reportados

    st.header("Indicadores del estudio en Bojayá")

    col1, col2, col3 = st.columns(3)

    col1.metric("Días analizados", f"{total_dias:,}")
    col2.metric("Fechas con reporte", dias_reportados)
    col3.metric("Días sin reporte", f"{dias_sin_reporte:,}")

    st.divider()

    st.header("Vista previa del dataset")
    st.dataframe(df.head(20), width="stretch")

else:
    st.error("No se encontró el dataset experimental de Bojayá.")

st.divider()
st.caption("AlertaChoco-AI | Proyecto de Ingeniería de Sistemas")


# Gráficos del análisis de precipitaciones
st.divider()
st.header("🌧️ Patrones históricos de precipitación")

st.write(
    "Comparación exploratoria de las lluvias acumuladas "
    "en días con y sin reportes de inundación en Bojayá."
)

carpeta_graficos = (
    Path(__file__).resolve().parent
    / "reports"
    / "figures"
)

graficos = {
    "3 días": "patrones_lluvia_3_dias.png",
    "7 días": "patrones_lluvia_7_dias.png",
    "15 días": "patrones_lluvia_15_dias.png"
}

periodo = st.selectbox(
    "Selecciona el periodo de precipitación:",
    list(graficos.keys())
)

ruta_grafico = carpeta_graficos / graficos[periodo]

if ruta_grafico.exists():
    st.image(
        str(ruta_grafico),
        caption=f"Análisis de precipitación acumulada de {periodo}",
        width="stretch"
    )
else:
    st.warning("No se encontró el gráfico seleccionado.")

st.info(
    "Estos gráficos muestran asociaciones históricas. "
    "No representan un modelo predictivo validado."
)


# Análisis histórico de inundaciones en el Chocó
st.divider()
st.header("📊 Inundaciones históricas en el Chocó")

st.write(
    "Visualización exploratoria de los registros históricos "
    "de inundaciones reportadas en el departamento del Chocó."
)

graficos_choco = {
    "Inundaciones por año": "inundaciones_por_anio.png",
    "Inundaciones por municipio": "inundaciones_por_municipio.png",
    "Personas afectadas por año": "personas_afectadas_por_anio.png"
}

tipo_analisis = st.selectbox(
    "Selecciona el análisis histórico:",
    list(graficos_choco.keys())
)

ruta_historica = carpeta_graficos / graficos_choco[tipo_analisis]

if ruta_historica.exists():
    st.image(
        str(ruta_historica),
        caption=tipo_analisis,
        width="stretch"
    )
else:
    st.warning("No se encontró el gráfico histórico seleccionado.")

st.caption(
    "Fuente: registros históricos de emergencias de la UNGRD. "
    "Los resultados dependen de la cobertura y calidad de los datos."
)

