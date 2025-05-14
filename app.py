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

    .upload-file {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4E5B4E;
        text-align: center;
        margin-top: 20px;
    }

    .warning-message {
        font-size: 1.2rem;
        font-weight: bold;
        color: #D9534F;
        text-align: center;
        margin-top: 20px;
    }

    .stFileUploader > label {
        background-color: #D9F7D9;
        border: 2px solid #4E5B4E;
        border-radius: 5px;
        padding: 10px;
        font-size: 1.1rem;
        color: #4E5B4E;
        cursor: pointer;
    }

    .stFileUploader > label:hover {
        background-color: #B9E2B9;
    }

    .location-title {
        font-family: "Segoe UI", "Trebuchet MS", sans-serif;
        font-size: 1.5rem;
        font-weight: bold;
        color: #265121;
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        letter-spacing: 1px;
        text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.25);
    }

    .stMap {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
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
        recolectados por
