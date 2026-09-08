"""
utils/ui_components.py
------------------------
Generadores de bloques HTML/CSS reutilizables (tarjetas de métricas,
indicadores de estado tipo "franja de instrumento" y placa técnica).
Estas funciones sólo construyen strings de HTML; el color y la tipografía
están definidos en assets/style.css. Se usan mediante
st.markdown(html, unsafe_allow_html=True) desde las vistas.
"""

from __future__ import annotations


def _compact(html: str) -> str:
    """
    Colapsa un bloque HTML multilínea/indentado a una sola línea.

    st.markdown() usa un parser de Markdown: cualquier línea indentada con
    4+ espacios se interpreta como un bloque de código preformateado. Como
    las plantillas de este módulo se escriben con sangría por legibilidad,
    hay que aplanarlas antes de pasarlas a unsafe_allow_html para que se
    rendericen como HTML real y no como texto plano.
    """
    return " ".join(line.strip() for line in html.strip().splitlines())


def metric_card(label: str, value: str, unit: str = "", helptext: str = "",
                 accent: str = "default") -> str:
    """Una sola tarjeta de métrica en formato lectura de instrumento."""
    accent_class = f"accent-{accent}" if accent != "default" else ""
    help_html = f'<div class="metric-help">{helptext}</div>' if helptext else ""
    return _compact(f"""
    <div class="metric-card {accent_class}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}<span class="metric-unit">{unit}</span></div>
        {help_html}
    </div>
    """)


def metric_row(cards_html: list[str]) -> str:
    """Envuelve varias metric_card en una fila flexible responsiva."""
    return f'<div class="metric-row">{"".join(cards_html)}</div>'


def status_badge(text: str, kind: str = "neutral") -> str:
    """
    Insignia de estado. kind ∈ {"good", "warn", "bad", "neutral"}
    good  -> verde (condición normal / sobrebalance / flujo lineal)
    warn  -> ámbar (balance aproximado / atención)
    bad   -> rojo  (bajo balance / condición crítica)
    """
    return f'<span class="status-badge status-{kind}">{text}</span>'


def gauge_strip(marker_pct: float, zones: list[tuple[float, str, str]],
                 marker_label: str = "") -> str:
    """
    Franja tipo instrumento (gauge horizontal) con zonas coloreadas y un
    marcador de posición. Se usa para ubicar visualmente el punto operativo
    dentro de un rango físico (p. ej. régimen de flujo o condición de balance).

    Parámetros
    ----------
    marker_pct : posición del marcador en % (0-100), ya calculada por la vista
    zones      : lista de tuplas (ancho_pct, color_css, etiqueta) que deben
                 sumar 100
    marker_label : texto mostrado bajo el marcador
    """
    marker_pct = max(0.0, min(100.0, marker_pct))
    zones_html = "".join(
        f'<div class="gauge-zone" style="width:{w}%;background:{color};"></div>'
        for w, color, _label in zones
    )
    legend_html = "".join(
        f'<span class="gauge-legend-item"><i style="background:{color};"></i>{label}</span>'
        for _w, color, label in zones
    )
    return _compact(f"""
    <div class="gauge-wrap">
        <div class="gauge-track">
            {zones_html}
            <div class="gauge-marker" style="left:{marker_pct}%;">
                <div class="gauge-marker-line"></div>
                <div class="gauge-marker-tag">{marker_label}</div>
            </div>
        </div>
        <div class="gauge-legend">{legend_html}</div>
    </div>
    """)


def nameplate(rows: list[tuple[str, str]], title: str, subtitle: str = "") -> str:
    """
    Bloque tipo 'placa de identificación de equipo' (nameplate) usado en el
    Home: título de la app + pares etiqueta:valor en fuente monoespaciada,
    evocando la placa de datos de un equipo de campo petrolero.
    """
    rows_html = "".join(
        f'<div class="nameplate-row"><span class="nameplate-key">{k}</span>'
        f'<span class="nameplate-val">{v}</span></div>'
        for k, v in rows
    )
    subtitle_html = f'<div class="nameplate-subtitle">{subtitle}</div>' if subtitle else ""
    return _compact(f"""
    <div class="nameplate">
        <div class="nameplate-title">{title}</div>
        {subtitle_html}
        <div class="nameplate-divider"></div>
        {rows_html}
    </div>
    """)


def section_header(eyebrow: str, title: str, description: str = "") -> str:
    """Encabezado de sección con barra de acento lateral (estilo panel técnico)."""
    desc_html = f'<p class="section-desc">{description}</p>' if description else ""
    return _compact(f"""
    <div class="section-header">
        <div class="section-accent-bar"></div>
        <div>
            <div class="section-eyebrow">{eyebrow}</div>
            <h2 class="section-title">{title}</h2>
            {desc_html}
        </div>
    </div>
    """)


def exercise_card(icon: str, title: str, description: str, tag: str) -> str:
    """Tarjeta de presentación de cada ejercicio técnico, usada en el Home."""
    return _compact(f"""
    <div class="exercise-card">
        <div class="exercise-card-top">
            <span class="exercise-icon">{icon}</span>
            <span class="exercise-tag">{tag}</span>
        </div>
        <div class="exercise-title">{title}</div>
        <div class="exercise-desc">{description}</div>
    </div>
    """)
