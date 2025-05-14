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

# Mensaje CSV

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

# Cargar CSV

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

# Estilo para los selectbox

st.markdown("""

<style>
.stSelectbox {
background-color: #FFFFFF;
border: 2px solid #4c8146;
border-radius: 10px;
padding: 12px 18px;
font-size: 1rem;
color: #4E5B4E;
font-weight: 600;
cursor: pointer;
transition: border-color 0.3s ease, background-color 0.3s ease;
}

    .stSelectbox:focus {
        outline: none;
        box-shadow: 0 0 8px rgba(76, 175, 80, 0.6);
        border-color: #76C76D;
        background-color: #F0F8F0;
    }

    .stSelectbox:hover {
        background-color: #e8f4e8;
        border-color: #76C76D;
    }

    </style>

""", unsafe_allow_html=True)

# Datos de ubicación EAFIT

eafit_location = pd.DataFrame({
'lat': [6.2006],
'lon': [-75.5783],
'location': ['Universidad EAFIT']
})

# Título ubicación

st.markdown('<p class="location-title">📍 Ubicación de los Sensores - Universidad EAFIT</p>', unsafe_allow_html=True)

# Mapa

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
            st.markdown("""
               <h2 style='font-family: "Segoe UI", "Trebuchet MS", sans-serif; font-size: 2rem; font-weight: 700;color: #265121; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.25);'>Visualización de datos</h2>
               """, unsafe_allow_html=True)
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
            st.markdown("""
               <h2 style='font-family: "Segoe UI", "Trebuchet MS", sans-serif; font-size: 2rem; font-weight: 700;color: #265121; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.25);'>Análisis Estadístico</h2>
               """, unsafe_allow_html=True)
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
            st.markdown("""
               <h2 style='font-family: "Segoe UI", "Trebuchet MS", sans-serif; font-size: 2rem; font-weight: 700;color: #265121; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.25);'>Filtros de Datos</h2>
               """, unsafe_allow_html=True)
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
            st.markdown("""
               <h2 style='font-family: "Segoe UI", "Trebuchet MS", sans-serif; font-size: 2rem; font-weight: 700;color: #265121; text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.25);'>Información del Sitio de Medición</h2>
               """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <h3 style='color:#265121; font-size:1.3rem; margin-bottom:0.5rem;'>Ubicación del Sensor</h3>
                """, unsafe_allow_html=True)

                st.markdown("""
                <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>
                <strong>📍 Universidad EAFIT</strong></h4>
                """, unsafe_allow_html=True)

                st.markdown("""
                <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>🌎 Latitud: 6.2006</h4>
                """, unsafe_allow_html=True)

                st.markdown("""
                <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>🌍 Longitud: -75.5783</h4>
                """, unsafe_allow_html=True)

                st.markdown("""
                <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>⛰️ Altitud: ~1,495 metros sobre el nivel del mar</h4>
                """, unsafe_allow_html=True)

            with col2:
               st.markdown("""
               <h3 style='color:#265121; font-size:1.3rem; margin-bottom:0.5rem;'>Detalles del Sensor</h3>
               """, unsafe_allow_html=True)
    
               st.markdown("""
               <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>🔧 Tipo: ESP32</h4>
               """, unsafe_allow_html=True)
    
               st.markdown("""
               <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>📏 Variables medidas:</h4>
               <ul style='color:#4E5B4E; font-size:1.05rem; margin:0 0 0.5rem 1.2rem;'>
                   <li>🌡️ Temperatura (°C)</li>
                   <li>💧 Humedad (%)</li>
               </ul>
               """, unsafe_allow_html=True)
    
               st.markdown("""
               <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>⏱️ Frecuencia: Según configuración</h4>
               """, unsafe_allow_html=True)
    
               st.markdown("""
               <h4 style='color:#4E5B4E; font-size:1.1rem; margin:0.2rem 0;'>🏫 Ubicación: Campus universitario</h4>
               """, unsafe_allow_html=True)

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
