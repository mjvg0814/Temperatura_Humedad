import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    layout="wide"
)

# Estilos de fondo y elementos
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/mjvg0814/Temperatura_Humedad/main/Fondo_plantas2.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }

    .location-title {
        font-family: "Segoe UI", "Trebuchet MS", sans-serif;
        font-size: 5rem;
        font-weight: bold;
        color: #265121;
        text-align: left;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        letter-spacing: 1px;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.25);
    }
    
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
    <h1 style='
        font-family: "Segoe UI", "Trebuchet MS", sans-serif;
        font-size: 3rem;
        font-weight: 900;
        color: #265121;
        text-align: center;
        letter-spacing: 1.5px;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.25);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    '>
        Análisis de datos de Sensores en Mi Ciudad
    </h1>
""", unsafe_allow_html=True)

# Descripción
st.markdown("""
    <h3 style='
        font-family: "Segoe UI", "Trebuchet MS", sans-serif;
        font-size: 1rem;
        color: #4E5B4E;
        text-align: center;
        margin-top: -1rem;
        margin-bottom: 1rem;
    '>
        Esta aplicación permite analizar datos de temperatura y humedad
        recolectados por sensores ESP32 en diferentes puntos de la ciudad.
    </h3>
""", unsafe_allow_html=True)

#Mensaje CSV
st.markdown("""
<style>
.warning-message {
    font-size: 1rem;
    color: #D9534F;
    background-color: #FDECEA;
    border-left: 4px solid #D9534F;
    padding: 8px 12px;
    width: fit-content;
    border-radius: 4px;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

#Cargar CSV
st.markdown("""
<style>
.upload-label {
    display: inline-block;
    background-color: #D9F7D9;
    border: 2px solid #4E5B4E;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 1.05rem;
    color: #4E5B4E;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
}
</style>
""", unsafe_allow_html=True)

#Pestañas
# Estilo para los selectbox
st.markdown("""
    <style>
        /* Estilo de selectbox */
        .stSelectbox select {
            background-color: #D9F7D9;
            color: #4E5B4E;
            border: 2px solid #4E5B4E;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 1rem;
            font-weight: bold;
            font-family: "Segoe UI", "Trebuchet MS", sans-serif;
            transition: background-color 0.3s ease, color 0.3s ease;
        }

        /* Hover (cuando el mouse está sobre el selectbox) */
        .stSelectbox select:hover {
            background-color: #bdebbd;
            color: #265121;
        }

        /* Selectbox seleccionado */
        .stSelectbox select:focus {
            background-color: #4E5B4E;
            color: white;
            border-color: #265121;
        }

        /* Estilo cuando el selectbox es deshabilitado */
        .stSelectbox select:disabled {
            background-color: #f0f0f0;
            color: #c0c0c0;
            border-color: #c0c0c0;
        }
    </style>
""", unsafe_allow_html=True)

""", unsafe_allow_html=True)


# Datos de ubicación EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

# Título personalizado para la sección de ubicación
st.markdown('<p class="location-title">📍 Ubicación de los Sensores - Universidad EAFIT</p>', unsafe_allow_html=True)

# Mapa estilizado
st.map(eafit_location, zoom=15)

# File uploader
st.markdown('<label class="upload-label">📂 Seleccione archivo CSV</label>', unsafe_allow_html=True)
uploaded_file = st.file_uploader('', type=['csv'])


if uploaded_file is not None:
    try:
        df1 = pd.read_csv(uploaded_file)

        column_mapping = {
            'temperatura {device="ESP32", name="Sensor 1"}': 'temperatura',
            'humedad {device="ESP32", name="Sensor 1"}': 'humedad'
        }
        df1 = df1.rename(columns=column_mapping)

        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "🗺️ Información del Sitio"])

        with tab1:
            st.subheader('Visualización de Datos')
            variable = st.selectbox("Seleccione variable a visualizar", ["temperatura", "humedad", "Ambas variables"])
            chart_type = st.selectbox("Seleccione tipo de gráfico", ["Línea", "Área", "Barra"])

            if variable == "Ambas variables":
                st.write("### Temperatura")
                if chart_type == "Línea":
                    st.line_chart(df1["temperatura"])
                elif chart_type == "Área":
                    st.area_chart(df1["temperatura"])
                else:
                    st.bar_chart(df1["temperatura"])

                st.write("### Humedad")
                if chart_type == "Línea":
                    st.line_chart(df1["humedad"])
                elif chart_type == "Área":
                    st.area_chart(df1["humedad"])
                else:
                    st.bar_chart(df1["humedad"])
            else:
                if chart_type == "Línea":
                    st.line_chart(df1[variable])
                elif chart_type == "Área":
                    st.area_chart(df1[variable])
                else:
                    st.bar_chart(df1[variable])

            if st.checkbox('Mostrar datos crudos'):
                st.write(df1)

        with tab2:
            st.subheader('Análisis Estadístico')
            stat_variable = st.radio("Seleccione variable para estadísticas", ["temperatura", "humedad"])
            stats_df = df1[stat_variable].describe()

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(stats_df)
            with col2:
                if stat_variable == "temperatura":
                    st.metric("Temperatura Promedio", f"{stats_df['mean']:.2f}°C")
                    st.metric("Temperatura Máxima", f"{stats_df['max']:.2f}°C")
                    st.metric("Temperatura Mínima", f"{stats_df['min']:.2f}°C")
                else:
                    st.metric("Humedad Promedio", f"{stats_df['mean']:.2f}%")
                    st.metric("Humedad Máxima", f"{stats_df['max']:.2f}%")
                    st.metric("Humedad Mínima", f"{stats_df['min']:.2f}%")

        with tab3:
            st.subheader('Filtros de Datos')
            filter_variable = st.selectbox("Seleccione variable para filtrar", ["temperatura", "humedad"])
            col1, col2 = st.columns(2)

            with col1:
                min_val = st.slider(f'Valor mínimo de {filter_variable}',
                                    float(df1[filter_variable].min()),
                                    float(df1[filter_variable].max()),
                                    float(df1[filter_variable].mean()),
                                    key="min_val")
                filtrado_df_min = df1[df1[filter_variable] > min_val]
                st.write(f"Registros con {filter_variable} superior a {min_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_min)

            with col2:
                max_val = st.slider(f'Valor máximo de {filter_variable}',
                                    float(df1[filter_variable].min()),
                                    float(df1[filter_variable].max()),
                                    float(df1[filter_variable].mean()),
                                    key="max_val")
                filtrado_df_max = df1[df1[filter_variable] < max_val]
                st.write(f"Registros con {filter_variable} inferior a {max_val}{'°C' if filter_variable == 'temperatura' else '%'}:")
                st.dataframe(filtrado_df_max)

            if st.button('Descargar datos filtrados'):
                csv = filtrado_df_min.to_csv().encode('utf-8')
                st.download_button("Descargar CSV", csv, "datos_filtrados.csv", "text/csv")

        with tab4:
            st.subheader("Información del Sitio de Medición")
            col1, col2 = st.columns(2)

            with col1:
                st.write("### Ubicación del Sensor")
                st.write("**Universidad EAFIT**")
                st.write("- Latitud: 6.2006")
                st.write("- Longitud: -75.5783")
                st.write("- Altitud: ~1,495 metros sobre el nivel del mar")

            with col2:
                st.write("### Detalles del Sensor")
                st.write("- Tipo: ESP32")
                st.write("- Variables medidas:")
                st.write("  * Temperatura (°C)")
                st.write("  * Humedad (%)")
                st.write("- Frecuencia de medición: Según configuración")
                st.write("- Ubicación: Campus universitario")

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')

else:
    st.markdown('<div class="warning-message">⚠️ Por favor, cargue un archivo CSV para comenzar el análisis.</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <hr style="border-top: 2px solid #4E5B4E; margin-top: 20px; margin-bottom: 15px;">
    <div style="font-family: 'Segoe UI', 'Trebuchet MS', sans-serif; font-size: 1rem; color: #4E5B4E; text-align: center; margin-top: 0px; margin-bottom: -150px; line-height: 1.2;">
        <p><strong>Desarrollado para el análisis de datos de sensores urbanos</strong></p>
        <strong>Universidad EAFIT</strong>, Medellín, Colombia</p>
        <p><strong>Tomas Arcila, Joel Diaz y Maria Jose Vallejo</strong></p>
    </div>
""", unsafe_allow_html=True)
