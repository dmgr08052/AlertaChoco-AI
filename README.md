# 🌧️ AlertaChoco-AI
### Sistema de análisis de inundaciones en el departamento del Chocó mediante ciencia de datos e inteligencia artificial

**Estado del proyecto:** En desarrollo | Análisis exploratorio y construcción del panel interactivo

## 📌 Descripción del proyecto

**AlertaChoco-AI** es un proyecto tecnológico desarrollado con Python y técnicas de ciencia de datos, cuyo propósito es analizar el comportamiento histórico de las inundaciones en el departamento del Chocó, Colombia, mediante la integración de información meteorológica y registros oficiales de emergencias.

El sistema utiliza datos del Instituto de Hidrología, Meteorología y Estudios Ambientales (IDEAM) y de la Unidad Nacional para la Gestión del Riesgo de Desastres (UNGRD), con el objetivo de identificar patrones de precipitación asociados a eventos de inundación y evaluar la viabilidad de implementar modelos de aprendizaje automático.

Actualmente, el proyecto se encuentra en una etapa de análisis exploratorio, con un estudio inicial enfocado en el municipio de Bojayá y registros de las estaciones meteorológicas Bellavista y Opogadó.

## 🎯 Objetivo general

Desarrollar una solución basada en ciencia de datos que permita analizar información histórica de precipitaciones e inundaciones en el departamento del Chocó, identificar patrones relevantes y evaluar las condiciones necesarias para construir futuros modelos predictivos.

## 🔍 Metodología de desarrollo

El proyecto se desarrolla mediante las siguientes etapas:

1. **Recolección:** obtención de información oficial del IDEAM y la UNGRD.
2. **Exploración:** identificación de variables, registros duplicados y problemas de calidad.
3. **Procesamiento:** limpieza, normalización y organización de conjuntos de datos.
4. **Integración:** relación entre fechas de inundaciones y precipitaciones históricas.
5. **Análisis estadístico:** evaluación de acumulados de lluvia de 3, 7 y 15 días.
6. **Visualización:** generación de gráficos comparativos y análisis de distribuciones.
7. **Evaluación de IA:** revisión de la viabilidad de entrenar modelos predictivos.
8. **Desarrollo web:** construcción de un panel interactivo con Streamlit.

## 🛠️ Tecnologías utilizadas

- **Python:** procesamiento y análisis de información.
- **Pandas y NumPy:** manipulación de datos y operaciones estadísticas.
- **Matplotlib:** visualización de resultados.
- **Git y GitHub:** control de versiones y seguimiento del desarrollo.
- **GitHub Codespaces:** entorno de programación en la nube.
- **Streamlit:** tecnología seleccionada para desarrollar el panel interactivo.

## 📊 Resultados preliminares

En el análisis experimental de Bojayá se obtuvieron los siguientes resultados:

| Indicador | Resultado |
|---|---|
| Observaciones meteorológicas completas | 2.495 |
| Fechas con inundación reportada | 14 |
| Días sin reporte registrado | 2.481 |
| Mediana de lluvia previa de 15 días con reporte | 307 mm |
| Mediana de lluvia previa de 15 días sin reporte | 215 mm |
| Diferencia entre medianas | 92 mm |

Los resultados sugieren diferencias en las precipitaciones acumuladas entre fechas con y sin reportes de inundación. No obstante, estas observaciones son exploratorias y no constituyen una validación predictiva.

## 🧠 Evaluación de inteligencia artificial

La evaluación inicial identificó limitaciones relacionadas con la cantidad de eventos reportados y la disponibilidad de etiquetas verificadas.

Por esta razón, todavía no se considera adecuado presentar un modelo predictivo como confiable.

Se plantea ampliar los registros históricos e incorporar variables hidrológicas adicionales, especialmente niveles de los ríos, antes de desarrollar y validar modelos de aprendizaje automático.

## 🚀 Próximas etapas

- Desarrollar el panel interactivo utilizando Streamlit.
- Integrar las visualizaciones estadísticas.
- Ampliar la cobertura geográfica y temporal.
- Incorporar nuevas fuentes de información hidrológica.
- Evaluar modelos de aprendizaje automático cuando los datos permitan una validación adecuada.

## ⚠️ Alcance y limitaciones

AlertaChoco-AI es actualmente un proyecto de investigación y desarrollo tecnológico. Sus resultados tienen carácter exploratorio y no deben interpretarse como alertas oficiales, pronósticos validados o recomendaciones operativas de gestión del riesgo.

## 👨‍💻 Desarrollo

**Daniel Mauricio Guerrero Rengifo**  
Ingeniero de Sistemas

Proyecto orientado a la aplicación de ciencia de datos, análisis estadístico e inteligencia artificial para contribuir al estudio de las inundaciones en el departamento del Chocó, Colombia.
