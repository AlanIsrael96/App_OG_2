"""
views/home.py
--------------
Página de presentación e identidad de la aplicación.
Incluye la placa técnica (nameplate) con los datos del participante,
las tarjetas de los tres ejercicios y un componente interactivo en
JavaScript (contador animado + mensaje dinámico ante un clic).
"""

import streamlit as st
import streamlit.components.v1 as components

from utils.ui_components import nameplate, exercise_card, section_header

# ---------------------------------------------------------------------------
# Datos personalizables del participante.
# EDITAR estos valores con los datos reales antes de publicar la aplicación.
# ---------------------------------------------------------------------------
PARTICIPANTE = "Alan López"          # <-- reemplazar por el nombre completo
TITULO_APP = "App Oil & Gas"    # <-- título de la aplicación
PROGRAMA = "Bootcamp Data Analytics for Oil & Gas"
INSTITUCION = "SPE Ecuador Section"


def render():
    col_logo, col_title = st.columns([1, 5], vertical_alignment="center")
    with col_logo:
        st.image("assets/logo_spe_ecuador.png", width=90)
    with col_title:
        st.markdown(
            f'<div class="section-eyebrow">{INSTITUCION} · {PROGRAMA}</div>'
            f'<div style="font-family:var(--font-display);font-size:1.4rem;'
            f'font-weight:700;color:var(--text-primary);">{TITULO_APP}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        nameplate(
            title=TITULO_APP,
            subtitle=(
                "Aplicación web desarrollada con Streamlit, HTML, CSS y JavaScript "
                "para el cálculo de indicadores técnicos de Producción, Perforación "
                "y Reservorios."
            ),
            rows=[
                ("Participante", PARTICIPANTE),
                ("Programa", PROGRAMA),
                ("Institución", INSTITUCION),
                ("Módulo", "Tarea Evaluativa — Módulo 1"),
            ],
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        section_header(
            eyebrow="PROPÓSITO TÉCNICO",
            title="¿Qué hace esta aplicación?",
            description=(
                "Convierte tres modelos clásicos de ingeniería de yacimientos, "
                "perforación y reservorios en calculadoras interactivas: cada "
                "resultado se recalcula en tiempo real y se acompaña de una "
                "visualización gráfica y un indicador de condición operativa."
            ),
        ),
        unsafe_allow_html=True,
    )

    cards = [
        exercise_card("🛢️", "Producción", "IPR compuesta con punto de burbuja (Vogel).", "Ejercicio 1"),
        exercise_card("⛏️", "Perforación", "Presión hidrostática del lodo vs. presión de formación.", "Ejercicio 2"),
        exercise_card("🪨", "Reservorios", "Estimación volumétrica del POES y volumen recuperable.", "Ejercicio 3"),
    ]
    st.markdown('<div class="exercise-row">' + "".join(cards) + "</div>", unsafe_allow_html=True)

    st.markdown(
        section_header(
            eyebrow="PANEL EN VIVO",
            title="Estado del sistema",
            description="Microinteracción en JavaScript embebida con streamlit.components.v1.html.",
        ),
        unsafe_allow_html=True,
    )
    _render_status_widget()

    st.markdown(
        '<div class="app-footer">'
        f'<span>{INSTITUCION} · {PROGRAMA}</span>'
        '<span>Navegue a "Ejercicios" para acceder a las tres calculadoras técnicas →</span>'
        '</div>',
        unsafe_allow_html=True,
    )


def _render_status_widget():
    """
    Componente HTML/JS embebido (streamlit.components.v1.html).
    Interacción 1: contador animado que cuenta de 0 al valor final al cargar.
    Interacción 2: al hacer clic en el botón, el mensaje de estado cambia
    dinámicamente sin recargar la página (microinteracción por evento).
    """
    html = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@500&display=swap');
        .sw-wrap {
            font-family: 'Inter', sans-serif;
            display: flex; gap: 0.9rem; flex-wrap: wrap; align-items: stretch;
        }
        .sw-card {
            flex: 1 1 140px;
            background: #10293A;
            border: 1px solid #22415A;
            border-radius: 10px;
            padding: 0.9rem 1rem;
        }
        .sw-label {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem; letter-spacing: 0.05em; text-transform: uppercase;
            color: #6C8494; margin-bottom: 0.3rem;
        }
        .sw-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.6rem; font-weight: 600; color: #EAF2F6;
        }
        .sw-msgbox {
            flex: 2 1 260px;
            background: linear-gradient(160deg,#10293A 0%,#0D2130 100%);
            border: 1px solid #22415A; border-left: 4px solid #D9822B;
            border-radius: 10px; padding: 0.9rem 1.1rem;
            display: flex; flex-direction: column; justify-content: center;
        }
        .sw-msg-text {
            font-family: 'Space Grotesk', sans-serif; font-weight: 600;
            font-size: 0.95rem; color: #EAF2F6; margin-bottom: 0.6rem;
            transition: opacity 0.2s ease;
        }
        .sw-btn {
            align-self: flex-start;
            background: #D9822B; color: #14202A; border: none; border-radius: 8px;
            font-family: 'Space Grotesk', sans-serif; font-weight: 600;
            font-size: 0.82rem; padding: 0.4rem 0.9rem; cursor: pointer;
            transition: filter 0.15s ease, transform 0.15s ease;
        }
        .sw-btn:hover { filter: brightness(1.12); transform: translateY(-1px); }
    </style>

    <div class="sw-wrap">
        <div class="sw-card">
            <div class="sw-label">Módulos técnicos</div>
            <div class="sw-value" id="sw-count-modulos">0</div>
        </div>
        <div class="sw-card">
            <div class="sw-label">Ecuaciones implementadas</div>
            <div class="sw-value" id="sw-count-ecuaciones">0</div>
        </div>
        <div class="sw-card">
            <div class="sw-label">Validaciones activas</div>
            <div class="sw-value" id="sw-count-validaciones">0</div>
        </div>
        <div class="sw-msgbox">
            <div class="sw-msg-text" id="sw-msg">Sistema listo para recibir parámetros de entrada.</div>
            <button class="sw-btn" id="sw-btn" onclick="swCycleMessage()">Ver estado técnico</button>
        </div>
    </div>

    <script>
        // --- Interacción 1: contador animado al cargar el componente ---
        function swAnimateCount(id, target, duration) {
            const el = document.getElementById(id);
            const start = performance.now();
            function tick(now) {
                const progress = Math.min((now - start) / duration, 1);
                const value = Math.floor(progress * target);
                el.textContent = value;
                if (progress < 1) requestAnimationFrame(tick);
                else el.textContent = target;
            }
            requestAnimationFrame(tick);
        }
        swAnimateCount('sw-count-modulos', 3, 900);
        swAnimateCount('sw-count-ecuaciones', 6, 1200);
        swAnimateCount('sw-count-validaciones', 12, 1500);

        // --- Interacción 2: mensaje dinámico controlado por evento de clic ---
        const swMessages = [
            "Sistema listo para recibir parámetros de entrada.",
            "Producción: modelo IPR compuesto (lineal + Vogel) activo.",
            "Perforación: comparación de presión hidrostática vs. formación activa.",
            "Reservorios: cálculo volumétrico de POES activo.",
            "Todos los módulos validan rangos físicos antes de calcular."
        ];
        let swIndex = 0;
        function swCycleMessage() {
            swIndex = (swIndex + 1) % swMessages.length;
            const el = document.getElementById('sw-msg');
            el.style.opacity = 0;
            setTimeout(() => {
                el.textContent = swMessages[swIndex];
                el.style.opacity = 1;
            }, 150);
        }
    </script>
    """
    components.html(html, height=170)
