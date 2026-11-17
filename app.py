
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
    st.dataframe(df.head(20), use_container_width=True)

else:
    st.error("No se encontró el dataset experimental de Bojayá.")

st.divider()
st.caption("AlertaChoco-AI | Proyecto de Ingeniería de Sistemas")
