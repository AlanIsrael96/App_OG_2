"""
utils/calculations.py
----------------------
Lógica de cálculo de ingeniería para los tres ejercicios técnicos:
  1. Producción  -> IPR compuesta con punto de burbuja (Vogel)
  2. Perforación -> Presión hidrostática del lodo
  3. Reservorios -> Estimación volumétrica del POES

Este módulo NO contiene código de interfaz (Streamlit, HTML, CSS, etc.).
Cada función recibe parámetros numéricos, valida su consistencia física
y devuelve un diccionario con los resultados. Los errores de validación
se comunican mediante ValueError con un mensaje claro en español, que la
capa de vistas (views/*) captura y muestra al usuario.
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# 1. PRODUCCIÓN — IPR compuesta con punto de burbuja (Vogel)
# ---------------------------------------------------------------------------

def _caudal_vogel(pr: float, pb: float, j: float, pwf: float) -> float:
    """Caudal según el modelo IPR compuesto (lineal + Vogel)."""
    qb = j * (pr - pb)
    if pwf >= pb:
        return j * (pr - pwf)
    ratio = pwf / pb
    return qb + (j * pb / 1.8) * (1 - 0.2 * ratio - 0.8 * ratio ** 2)


def calcular_ipr(pr: float, pb: float, j: float, pwf: float) -> dict:
    """
    Calcula el caudal de petróleo para un yacimiento subsaturado usando
    el modelo IPR compuesto: comportamiento lineal por encima de Pb y
    modelo de Vogel por debajo de Pb.

    Parámetros
    ----------
    pr  : presión promedio del reservorio [psi]
    pb  : presión de burbuja [psi]
    j   : índice de productividad [STB/d/psi]
    pwf : presión de fondo fluyente [psi]

    Retorna
    -------
    dict con qo, qb, qo_max, regimen y los parámetros validados.
    """
    if pr <= 0 or pb <= 0 or j <= 0:
        raise ValueError("Pᵣ, Pᵦ y J deben ser valores positivos mayores que cero.")
    if pwf < 0:
        raise ValueError("Pwf no puede ser negativa.")
    if pb >= pr:
        raise ValueError("Se requiere un reservorio subsaturado: Pᵦ debe ser menor que Pᵣ.")
    if pwf > pr:
        raise ValueError("Pwf no puede ser mayor que la presión de reservorio Pᵣ.")

    qb = j * (pr - pb)
    qo_max = qb + (j * pb) / 1.8
    qo = _caudal_vogel(pr, pb, j, pwf)
    regimen = "Flujo lineal (Pwf ≥ Pᵦ)" if pwf >= pb else "Flujo Vogel (Pwf < Pᵦ)"

    return {
        "pr": pr, "pb": pb, "j": j, "pwf": pwf,
        "qo": qo, "qb": qb, "qo_max": qo_max,
        "regimen": regimen,
        "sobre_burbuja": pwf >= pb,
    }


def curva_ipr(pr: float, pb: float, j: float, n_puntos: int = 60) -> tuple[np.ndarray, np.ndarray]:
    """Genera la curva IPR completa (Pwf de 0 a Pr) para graficar."""
    pwf_arr = np.linspace(0, pr, n_puntos)
    q_arr = np.array([_caudal_vogel(pr, pb, j, p) for p in pwf_arr])
    return pwf_arr, q_arr


# ---------------------------------------------------------------------------
# 2. PERFORACIÓN — Presión hidrostática del lodo
# ---------------------------------------------------------------------------

def calcular_presion_hidrostatica(mw: float, md: float, tvd: float, pform: float) -> dict:
    """
    Calcula el gradiente y la presión hidrostática de la columna de lodo,
    y la compara contra la presión de formación para determinar la
    condición de balance del pozo.

    Parámetros
    ----------
    mw    : peso del lodo [ppg]
    md    : profundidad medida [ft]
    tvd   : profundidad vertical verdadera [ft]
    pform : presión de formación [psi]
    """
    if mw <= 0:
        raise ValueError("El peso del lodo (MW) debe ser positivo.")
    if md <= 0 or tvd <= 0:
        raise ValueError("MD y TVD deben ser mayores que cero.")
    if tvd > md:
        raise ValueError("TVD no puede ser mayor que MD (la vertical verdadera no excede la medida).")
    if pform < 0:
        raise ValueError("La presión de formación no puede ser negativa.")

    gh = 0.052 * mw
    ph = 0.052 * mw * tvd
    dp = ph - pform

    # Margen de tolerancia para considerar "balance aproximado" (~1% de Ph, min 25 psi)
    tolerancia = max(25.0, 0.01 * ph)
    if dp > tolerancia:
        condicion = "Sobrebalance"
    elif dp < -tolerancia:
        condicion = "Bajo balance"
    else:
        condicion = "Balance aproximado"

    return {
        "mw": mw, "md": md, "tvd": tvd, "pform": pform,
        "gh": gh, "ph": ph, "dp": dp, "condicion": condicion,
        "tolerancia": tolerancia,
    }


def curva_presion_hidrostatica(mw: float, tvd_max: float, n_puntos: int = 60) -> tuple[np.ndarray, np.ndarray]:
    """Genera la curva de presión hidrostática vs TVD, de 0 a tvd_max."""
    tvd_arr = np.linspace(0, tvd_max, n_puntos)
    ph_arr = 0.052 * mw * tvd_arr
    return tvd_arr, ph_arr


# ---------------------------------------------------------------------------
# 3. RESERVORIOS — Estimación volumétrica del POES
# ---------------------------------------------------------------------------

def calcular_poes(a: float, h: float, ntg: float, phi: float,
                   swi: float, boi: float, fr: float) -> dict:
    """
    Estimación volumétrica del Petróleo Original en Sitio (POES) y del
    volumen recuperable estimado a partir de un factor de recobro.

    Parámetros
    ----------
    a   : área del reservorio [acres]
    h   : espesor bruto [ft]
    ntg : relación net-to-gross [fracción 0-1]
    phi : porosidad efectiva [fracción 0-1]
    swi : saturación inicial de agua [fracción 0-1]
    boi : factor volumétrico inicial del petróleo [rb/STB]
    fr  : factor de recobro asumido [fracción 0-1]
    """
    if a <= 0 or h <= 0:
        raise ValueError("El área (A) y el espesor (h) deben ser mayores que cero.")
    if boi <= 0:
        raise ValueError("Boi debe ser mayor que cero.")
    for nombre, valor in (("NTG", ntg), ("φ (porosidad)", phi), ("FR", fr)):
        if not (0 < valor <= 1):
            raise ValueError(f"{nombre} debe expresarse como fracción entre 0 y 1.")
    if not (0 <= swi < 1):
        raise ValueError("Swi debe expresarse como fracción entre 0 y 1 (y menor que 1).")

    hn = h * ntg
    poes_stb = (7758 * a * hn * phi * (1 - swi)) / boi
    poes_mmstb = poes_stb / 1e6
    recuperable_stb = poes_stb * fr
    recuperable_mmstb = recuperable_stb / 1e6

    return {
        "a": a, "h": h, "ntg": ntg, "phi": phi, "swi": swi, "boi": boi, "fr": fr,
        "hn": hn,
        "poes_stb": poes_stb, "poes_mmstb": poes_mmstb,
        "recuperable_stb": recuperable_stb, "recuperable_mmstb": recuperable_mmstb,
    }
