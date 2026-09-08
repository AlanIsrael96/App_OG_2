"""
views/produccion.py
---------------------
Ejercicio 1. Producción — IPR compuesta con punto de burbuja (Vogel).
La lógica de cálculo vive en utils/calculations.py; este módulo sólo
construye la interfaz (entradas, tarjetas de resultados, gráfico y
franja indicadora del régimen de flujo).
"""

import streamlit as st
import plotly.graph_objects as go

from utils.calculations import calcular_ipr, curva_ipr
from utils.ui_components import metric_card, metric_row, status_badge, gauge_strip, section_header

PLOT_BG = "#10293A"
PAPER_BG = "#10293A"
GRID_COLOR = "#22415A"
LINE_COLOR = "#D9822B"
POINT_COLOR = "#4FAE7C"
TEXT_COLOR = "#EAF2F6"


def render():
    st.markdown(
        section_header(
            eyebrow="EJERCICIO 1 · PRODUCCIÓN",
            title="IPR compuesta con punto de burbuja",
            description=(
                "Modelo de afluencia (IPR) para un reservorio subsaturado: "
                "comportamiento lineal por encima de Pᵦ y modelo de Vogel "
                "por debajo del punto de burbuja."
            ),
        ),
        unsafe_allow_html=True,
    )

    col_in, col_out = st.columns([1, 1.5], gap="large")

    with col_in:
        with st.container(border=True):
            st.markdown("##### Parámetros de entrada")
            pr = st.number_input("Presión de reservorio Pᵣ [psi]", min_value=0.0, value=3200.0, step=50.0)
            pb = st.number_input("Presión de burbuja Pᵦ [psi]", min_value=0.0, value=2100.0, step=50.0)
            j = st.number_input("Índice de productividad J [STB/d/psi]", min_value=0.0, value=1.20, step=0.05, format="%.2f")
            pwf = st.number_input("Presión de fondo fluyente Pwf [psi]", min_value=0.0, value=1500.0, step=50.0)
            calcular = st.button("Calcular IPR", use_container_width=True)

    with col_out:
        with st.container(border=True):
            st.markdown("##### Resultados")
            try:
                res = calcular_ipr(pr, pb, j, pwf)
            except ValueError as e:
                st.error(f"⚠️ {e}")
                return

            badge_kind = "good" if res["sobre_burbuja"] else "warn"
            st.markdown(status_badge(res["regimen"], badge_kind), unsafe_allow_html=True)
            st.write("")

            cards = [
                metric_card("Caudal qₒ", f'{res["qo"]:.1f}', "STB/d", accent="good"),
                metric_card("Caudal en Pᵦ, qᵦ", f'{res["qb"]:.1f}', "STB/d"),
                metric_card("Caudal máx. teórico", f'{res["qo_max"]:.1f}', "STB/d"),
            ]
            st.markdown(metric_row(cards), unsafe_allow_html=True)

            # Franja indicadora del régimen de flujo (posición de Pwf en [0, Pr], umbral en Pb)
            pb_pct = 100 * (1 - pb / pr)  # Pwf se posiciona sobre un eje "caudal creciente"; usamos escala de Pwf invertida
            pwf_pct = 100 * (1 - pwf / pr)
            zones = [
                (100 - pb_pct, "rgba(224,185,77,0.35)", "Vogel (Pwf < Pᵦ)"),
                (pb_pct, "rgba(79,174,124,0.35)", "Lineal (Pwf ≥ Pᵦ)"),
            ]
            st.caption("Posición de Pwf respecto al punto de burbuja (eje: 0 = Pwf máx. → Pᵣ = Pwf mín.)")
            st.markdown(
                gauge_strip(marker_pct=pwf_pct, zones=zones, marker_label=f'Pwf = {pwf:.0f} psi'),
                unsafe_allow_html=True,
            )

    # --- Curva IPR completa ---
    pwf_arr, q_arr = curva_ipr(res["pr"], res["pb"], res["j"])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=q_arr, y=pwf_arr, mode="lines", name="Curva IPR",
        line=dict(color=LINE_COLOR, width=3),
    ))
    fig.add_trace(go.Scatter(
        x=[res["qo"]], y=[res["pwf"]], mode="markers", name="Punto operativo",
        marker=dict(color=POINT_COLOR, size=13, line=dict(color=TEXT_COLOR, width=1.5)),
    ))
    fig.add_hline(y=res["pb"], line=dict(color=GRID_COLOR, dash="dash"),
                  annotation_text="Pᵦ", annotation_font_color=TEXT_COLOR)
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_COLOR, family="Inter, sans-serif"),
        xaxis=dict(title="Caudal qₒ [STB/d]", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(title="Pwf [psi]", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        legend=dict(orientation="h", y=1.1),
        margin=dict(l=10, r=10, t=40, b=10),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Validaciones activas: Pᵣ > Pᵦ (reservorio subsaturado), Pwf ≤ Pᵣ, "
        "y todos los parámetros deben ser positivos."
    )
