
import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración general
st.set_page_config(
    page_title="AlertaChoco-AI",
    page_icon="🌧️",
    layout="wide"
)

BASE = Path(__file__).resolve().parent
RUTA_DATOS = BASE / "data" / "processed" / "dataset_experimental_bojaya.csv"
CARPETA_GRAFICOS = BASE / "reports" / "figures"

# Menú lateral
with st.sidebar:
    st.title("🌧️ AlertaChoco-AI")
    st.caption("Análisis histórico de inundaciones")
    st.divider()

    pagina = st.radio(
        "Navegación",
        [
            "🏠 Inicio",
            "📊 Inundaciones en el Chocó",
            "🌧️ Precipitaciones en Bojayá",
            "📚 Metodología y conclusiones"
        ]
    )

    st.divider()
    st.caption("Proyecto académico | Ingeniería de Sistemas")

# Aviso general
st.info(
    "Proyecto académico de ciencia de datos. "
    "Los resultados son exploratorios y no constituyen "
    "alertas oficiales ni predicciones validadas."
)

# --------------------------------------------------
# PÁGINA 1: INICIO
# --------------------------------------------------
if pagina == "🏠 Inicio":

    st.title("🌧️ AlertaChoco-AI")
    st.subheader("Análisis histórico de inundaciones en el Chocó")

    st.write(
        "AlertaChoco-AI es un proyecto de Ingeniería de Sistemas "
        "que utiliza ciencia de datos para estudiar registros "
        "históricos de inundaciones y precipitaciones en el "
        "departamento del Chocó, Colombia."
    )

    st.header("Objetivo del proyecto")
    st.write(
        "Analizar información histórica de fuentes oficiales "
        "para identificar patrones de precipitación y su "
        "relación con las inundaciones reportadas."
    )

    st.header("Componentes desarrollados")
    st.markdown(
        """
        - Procesamiento y limpieza de datos históricos.
        - Análisis de emergencias reportadas por la UNGRD.
        - Estudio de precipitaciones del IDEAM en Bojayá.
        - Comparación de lluvias acumuladas en 3, 7 y 15 días.
        - Visualización interactiva de resultados.
        - Evaluación preliminar de viabilidad de inteligencia artificial.
        """
    )

    st.success("Proyecto en desarrollo: dashboard exploratorio funcional.")

# --------------------------------------------------
# PÁGINA 2: INUNDACIONES EN EL CHOCÓ
# --------------------------------------------------
elif pagina == "📊 Inundaciones en el Chocó":

    st.title("📊 Inundaciones históricas en el Chocó")

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

    ruta_historica = CARPETA_GRAFICOS / graficos_choco[tipo_analisis]

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

# --------------------------------------------------
# PÁGINA 3: PRECIPITACIONES EN BOJAYÁ
# --------------------------------------------------
elif pagina == "🌧️ Precipitaciones en Bojayá":

    st.title("🌧️ Análisis de precipitaciones en Bojayá")

    if RUTA_DATOS.exists():
        df = pd.read_csv(RUTA_DATOS)

        total_dias = len(df)
        dias_reportados = int(df["INUNDACION_REPORTADA"].sum())
        dias_sin_reporte = total_dias - dias_reportados

        st.header("Indicadores del estudio")

        col1, col2, col3 = st.columns(3)

        col1.metric("Días analizados", f"{total_dias:,}")
        col2.metric("Fechas con reporte", dias_reportados)
        col3.metric("Días sin reporte", f"{dias_sin_reporte:,}")

        st.caption(
            "Los días sin reporte no equivalen necesariamente "
            "a días sin inundación."
        )

        st.divider()
        st.header("Vista previa del dataset")
        st.dataframe(df.head(20), width="stretch")

    else:
        st.error("No se encontró el dataset experimental de Bojayá.")

    st.divider()
    st.header("Patrones históricos de precipitación")

    st.write(
        "Comparación exploratoria de las lluvias acumuladas "
        "en días con y sin reportes de inundación en Bojayá."
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

    ruta_grafico = CARPETA_GRAFICOS / graficos[periodo]

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

# --------------------------------------------------
# PÁGINA 4: METODOLOGÍA Y CONCLUSIONES
# --------------------------------------------------
elif pagina == "📚 Metodología y conclusiones":

    st.title("📚 Metodología y conclusiones")

    st.header("Fuentes de información")
    st.write(
        "UNGRD: registros históricos de emergencias. "
        "IDEAM: datos de precipitación de estaciones meteorológicas."
    )

    st.header("Metodología aplicada")
    st.markdown(
        """
        1. Recolección de datos históricos.
        2. Exploración y evaluación de calidad.
        3. Limpieza y preparación de los datasets.
        4. Integración temporal de precipitaciones e inundaciones.
        5. Análisis estadístico y visualización.
        6. Evaluación preliminar de umbrales de precipitación.
        7. Evaluación de viabilidad de modelos de IA.
        """
    )

    st.header("Hallazgos preliminares")
    st.write(
        "En Bojayá se observaron diferencias en la distribución "
        "de las precipitaciones acumuladas entre fechas con "
        "reportes de inundación y fechas sin reportes."
    )

    st.header("Limitaciones")
    st.warning(
        "La cantidad de fechas con inundación reportada es reducida. "
        "Además, no se dispone de una verificación completa de "
        "los días sin inundación ni de todas las variables "
        "hidrológicas necesarias. Por ello, todavía no se "
        "dispone de un modelo predictivo validado."
    )

    st.header("Próximos pasos")
    st.write(
        "Ampliar las fuentes de información, evaluar la calidad "
        "de nuevos datos y continuar mejorando el dashboard."
    )

st.divider()
st.caption("AlertaChoco-AI | Proyecto de Ingeniería de Sistemas")
