#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — les constantes du mur (🧮 calcul, CODATA 2022).

Toutes les valeurs dérivées de c, h (EXACTES dans le SI 2019) et G (la SEULE
constante mal connue : ±2,2e-5 relatif — c'est LUI qui floute la position du mur).
Sources : CODATA 2022 (NIST, arXiv:2409.03787), récupéré le 29/09/2026.
"""
from __future__ import annotations

import math

# ── CODATA 2022 ──────────────────────────────────────────────────────────────
C = 299_792_458.0            # m/s      (exact, SI 2019)
H = 6.626_070_15e-34         # J·s      (exact, SI 2019)
HBAR = H / (2.0 * math.pi)
G = 6.674_30e-11             # m³/kg/s² (CODATA 2022, u_r = 2.2e-5)
U_R_G = 2.2e-5
Q_E = 1.602_176_634e-19      # C        (exact)
GEV = 1.602_176_634e-10      # J par GeV

# ── les unités de Planck, calculées (pas copiées) ───────────────────────────
def longueur_planck() -> float:
    """ℓ_P = √(ħG/c³)"""
    return math.sqrt(HBAR * G / C ** 3)

def temps_planck() -> float:
    """t_P = ℓ_P/c"""
    return longueur_planck() / C

def masse_planck() -> float:
    """m_P = √(ħc/G)"""
    return math.sqrt(HBAR * C / G)

def energie_planck_j() -> float:
    return masse_planck() * C ** 2

def energie_planck_gev() -> float:
    return energie_planck_j() / GEV

def temperature_planck() -> float:
    """T_P = E_P/k_B (k_B CODATA 2022, exact en e/k)"""
    K_B = 1.380_649e-23     # exact, SI 2019
    return energie_planck_j() / K_B

def incertitude_relative_longueur() -> float:
    """l_P ∝ √G : la moitié de l'incertitude relative de G."""
    return U_R_G / 2.0

# ── valeurs CODATA 2022 publiées (pour validation, pas pour le calcul) ──────
CODATA_2022 = {
    "l_planck_m": 1.616_255e-35,
    "u_l_planck": 0.000_018e-35,
    "t_planck_s": 5.391_247e-44,
    "m_planck_kg": 2.176_434e-8,
    "E_planck_GeV": 1.220_89e19,
}


if __name__ == "__main__":
    print("═══ RATISS-PLANCK — les unités du mur (CODATA 2022) ═══")
    lp, tp = longueur_planck(), temps_planck()
    ep = energie_planck_gev()
    print(f"  l_P  = {lp:.6e} m   (CODATA : {CODATA_2022['l_planck_m']:.6e} ± {CODATA_2022['u_l_planck']:.0e})")
    print(f"  t_P  = {tp:.6e} s   (CODATA : {CODATA_2022['t_planck_s']:.6e})")
    print(f"  m_P  = {masse_planck():.6e} kg (CODATA : {CODATA_2022['m_planck_kg']:.6e})")
    print(f"  E_P  = {ep:.4e} GeV (CODATA : {CODATA_2022['E_planck_GeV']:.4e})")
    print(f"  T_P  = {temperature_planck():.4e} K")
    print(f"  incertitude sur la POSITION du mur : ±{incertitude_relative_longueur()*100:.1e} % (dominée par G)")
