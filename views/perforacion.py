"""
views/perforacion.py
----------------------
Ejercicio 2. Perforación — Presión hidrostática del lodo.
La lógica de cálculo vive en utils/calculations.py.
"""

import streamlit as st
import plotly.graph_objects as go

from utils.calculations import calcular_presion_hidrostatica, curva_presion_hidrostatica
from utils.ui_components import metric_card, metric_row, status_badge, gauge_strip, section_header

PLOT_BG = "#10293A"
PAPER_BG = "#10293A"
GRID_COLOR = "#22415A"
LINE_COLOR = "#D9822B"
POINT_COLOR = "#4FAE7C"
REF_COLOR = "#9FB4C2"
TEXT_COLOR = "#EAF2F6"

_BADGE_KIND = {"Sobrebalance": "good", "Balance aproximado": "warn", "Bajo balance": "bad"}


def render():
    st.markdown(
        section_header(
            eyebrow="EJERCICIO 2 · PERFORACIÓN",
            title="Presión hidrostática del lodo",
            description=(
                "Gradiente y presión hidrostática de la columna de lodo, "
                "comparada contra la presión de formación para determinar "
                "la condición de balance del pozo."
            ),
        ),
        unsafe_allow_html=True,
    )

    col_in, col_out = st.columns([1, 1.5], gap="large")

    with col_in:
        with st.container(border=True):
            st.markdown("##### Parámetros de entrada")
            mw = st.number_input("Peso del lodo MW [ppg]", min_value=0.0, value=10.5, step=0.1, format="%.1f")
            md = st.number_input("Profundidad medida MD [ft]", min_value=0.0, value=9500.0, step=100.0)
            tvd = st.number_input("Profundidad vertical verdadera TVD [ft]", min_value=0.0, value=8800.0, step=100.0)
            pform = st.number_input("Presión de formación Pform [psi]", min_value=0.0, value=4000.0, step=50.0)

    with col_out:
        with st.container(border=True):
            st.markdown("##### Resultados")
            try:
                res = calcular_presion_hidrostatica(mw, md, tvd, pform)
            except ValueError as e:
                st.error(f"⚠️ {e}")
                return

            kind = _BADGE_KIND[res["condicion"]]
            st.markdown(status_badge(res["condicion"], kind), unsafe_allow_html=True)
            st.write("")

            cards = [
                metric_card("Gradiente hidrostático Gₕ", f'{res["gh"]:.3f}', "psi/ft"),
                metric_card("Presión hidrostática Pₕ", f'{res["ph"]:.0f}', "psi", accent="good"),
                metric_card("Diferencial ΔP", f'{res["dp"]:+.0f}', "psi", accent=kind),
            ]
            st.markdown(metric_row(cards), unsafe_allow_html=True)

            # Franja de balance: escala simétrica centrada en Pform (ΔP = 0)
            escala = max(res["tolerancia"] * 4, abs(res["dp"]) * 1.3, 200)
            dp_pct = 50 + 50 * max(-1, min(1, res["dp"] / escala))
            tol_pct = 50 * (res["tolerancia"] / escala)
            zones = [
                (50 - tol_pct, "rgba(209,84,74,0.35)", "Bajo balance"),
                (2 * tol_pct, "rgba(224,185,77,0.35)", "Balance aprox."),
                (50 - tol_pct, "rgba(79,174,124,0.35)", "Sobrebalance"),
            ]
            st.caption("Posición de ΔP respecto a la presión de formación (centro = balance)")
            st.markdown(
                gauge_strip(marker_pct=dp_pct, zones=zones, marker_label=f'ΔP = {res["dp"]:+.0f} psi'),
                unsafe_allow_html=True,
            )

    # --- Gráfico presión hidrostática vs TVD ---
    tvd_arr, ph_arr = curva_presion_hidrostatica(res["mw"], max(res["tvd"] * 1.15, res["tvd"] + 500))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tvd_arr, y=ph_arr, mode="lines", name="Pₕ vs TVD",
        line=dict(color=LINE_COLOR, width=3),
    ))
    fig.add_trace(go.Scatter(
        x=[res["tvd"]], y=[res["ph"]], mode="markers", name="Profundidad ingresada",
        marker=dict(color=POINT_COLOR, size=13, line=dict(color=TEXT_COLOR, width=1.5)),
    ))
    fig.add_hline(y=res["pform"], line=dict(color=REF_COLOR, dash="dash"),
                  annotation_text="Pform", annotation_font_color=TEXT_COLOR)
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_COLOR, family="Inter, sans-serif"),
        xaxis=dict(title="TVD [ft]", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(title="Presión hidrostática Pₕ [psi]", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        legend=dict(orientation="h", y=1.1),
        margin=dict(l=10, r=10, t=40, b=10),
        height=420,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Validaciones activas: MW > 0, MD y TVD > 0, TVD ≤ MD, Pform ≥ 0."
    )
