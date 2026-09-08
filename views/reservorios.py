"""
views/reservorios.py
----------------------
Ejercicio 3. Reservorios — Estimación volumétrica del POES.
La lógica de cálculo vive en utils/calculations.py.
"""

import streamlit as st
import plotly.graph_objects as go

from utils.calculations import calcular_poes
from utils.ui_components import metric_card, metric_row, section_header

PLOT_BG = "#10293A"
PAPER_BG = "#10293A"
GRID_COLOR = "#22415A"
BAR_COLORS = ["#D9822B", "#4FAE7C"]
TEXT_COLOR = "#EAF2F6"


def render():
    st.markdown(
        section_header(
            eyebrow="EJERCICIO 3 · RESERVORIOS",
            title="Estimación volumétrica del POES",
            description=(
                "Petróleo Original en Sitio mediante el método volumétrico, "
                "junto con una estimación simple del volumen recuperable a "
                "partir de un factor de recobro definido por el usuario."
            ),
        ),
        unsafe_allow_html=True,
    )

    col_in, col_out = st.columns([1, 1.5], gap="large")

    with col_in:
        with st.container(border=True):
            st.markdown("##### Parámetros de entrada")
            a = st.number_input("Área del reservorio A [acres]", min_value=0.0, value=850.0, step=10.0)
            h = st.number_input("Espesor bruto h [ft]", min_value=0.0, value=45.0, step=1.0)
            ntg = st.slider("Relación net-to-gross NTG [fracción]", 0.01, 1.0, 0.75, step=0.01)
            phi = st.slider("Porosidad efectiva φ [fracción]", 0.01, 0.40, 0.18, step=0.01)
            swi = st.slider("Saturación inicial de agua Swi [fracción]", 0.0, 0.90, 0.25, step=0.01)
            boi = st.number_input("Factor volumétrico inicial Boi [rb/STB]", min_value=0.01, value=1.30, step=0.01, format="%.2f")
            fr = st.slider("Factor de recobro FR [fracción]", 0.01, 1.0, 0.30, step=0.01)

    with col_out:
        with st.container(border=True):
            st.markdown("##### Resultados")
            try:
                res = calcular_poes(a, h, ntg, phi, swi, boi, fr)
            except ValueError as e:
                st.error(f"⚠️ {e}")
                return

            cards = [
                metric_card("Espesor neto hₙ", f'{res["hn"]:.1f}', "ft"),
                metric_card("POES", f'{res["poes_mmstb"]:.2f}', "MMSTB", accent="good"),
                metric_card("Volumen recuperable", f'{res["recuperable_mmstb"]:.2f}', "MMSTB", accent="good"),
            ]
            st.markdown(metric_row(cards), unsafe_allow_html=True)

            cards2 = [
                metric_card("POES (detalle)", f'{res["poes_stb"]:,.0f}', "STB"),
                metric_card("Recuperable (detalle)", f'{res["recuperable_stb"]:,.0f}', "STB"),
            ]
            st.markdown(metric_row(cards2), unsafe_allow_html=True)

    # --- Gráfico comparativo POES vs volumen recuperable ---
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["POES", "Volumen recuperable"],
        y=[res["poes_mmstb"], res["recuperable_mmstb"]],
        marker_color=BAR_COLORS,
        text=[f'{res["poes_mmstb"]:.2f} MMSTB', f'{res["recuperable_mmstb"]:.2f} MMSTB'],
        textposition="outside",
        width=0.5,
    ))
    fig.update_layout(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(color=TEXT_COLOR, family="Inter, sans-serif"),
        yaxis=dict(title="Volumen [MMSTB]", gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        xaxis=dict(gridcolor=GRID_COLOR),
        margin=dict(l=10, r=10, t=30, b=10),
        height=380,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f'Factor de recobro aplicado: {res["fr"]*100:.0f}% · '
        "Validaciones activas: A y h > 0, Boi > 0, NTG/φ/Swi/FR expresados como fracción entre 0 y 1."
    )
