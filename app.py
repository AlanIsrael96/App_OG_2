"""
app.py
------
Punto de entrada de la aplicación "Panel Técnico Oil & Gas" (SPE Ecuador
Section — Bootcamp Data Analytics for Oil & Gas, Tarea Evaluativa Módulo 1).

Responsabilidad de este archivo:
  - Configurar la página (título, ícono, layout).
  - Cargar la hoja de estilos personalizada (HTML/CSS).
  - Construir la navegación principal (únicamente Home y Ejercicios).
  - Enrutar hacia las vistas en views/ (Home, o los tres tabs de Ejercicios).

La lógica de cálculo de ingeniería vive en utils/calculations.py y los
componentes visuales reutilizables en utils/ui_components.py, de modo que
este archivo permanece enfocado exclusivamente en el enrutamiento.
"""

import base64
from pathlib import Path

import streamlit as st

from views import home, produccion, perforacion, reservorios
from utils.ui_components import section_header

BASE_DIR = Path(__file__).parent


def _logo_base64() -> str:
    logo_path = BASE_DIR / "assets" / "logo_spe_ecuador.png"
    return base64.b64encode(logo_path.read_bytes()).decode("utf-8")

st.set_page_config(
    page_title="Panel Técnico Oil & Gas | SPE Ecuador Section",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def cargar_css(ruta: str):
    css_path = BASE_DIR / ruta
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


cargar_css("assets/style.css")

# ---------------------------------------------------------------------------
# Navegación principal — únicamente "Home" y "Ejercicios", como exige la guía.
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">'
        f'<img src="data:image/png;base64,{_logo_base64()}" alt="SPE Ecuador Section">'
        '<div class="sidebar-brand-text">DATA ANALYTICS<br>FOR OIL &amp; GAS</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    seccion = st.radio(
        "Navegación",
        options=["🏠  Home", "🛠️  Ejercicios"],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.caption("Bootcamp Data Analytics for Oil & Gas — SPE Ecuador Section")

# ---------------------------------------------------------------------------
# Enrutamiento
# ---------------------------------------------------------------------------
if seccion == "🏠  Home":
    home.render()
else:
    st.markdown(
        section_header(
            eyebrow="MÓDULO TÉCNICO",
            title="Ejercicios",
            description="Seleccione una pestaña para acceder a cada calculadora técnica.",
        ),
        unsafe_allow_html=True,
    )

    tab_prod, tab_perf, tab_res = st.tabs(["🛢️  Producción", "⛏️  Perforación", "🪨  Reservorios"])

    with tab_prod:
        produccion.render()
    with tab_perf:
        perforacion.render()
    with tab_res:
        reservorios.render()
