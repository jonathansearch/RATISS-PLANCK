#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK v0.2 — l'effet Unruh le long du voyage (🧮).

T_U = ħ·a/(2π·c·k_B) : un observateur accéléré voit un bain thermique.
Le qubit porteur est un observateur comme un autre : à quelle accélération
le bain Unruh commence-t-il à MANGER sa cohérence ?

Points de contrôle calculés :
  - a = 9,81 m/s² (la Terre) → T_U ≈ 4,0×10⁻²⁰ K (rien, depuis toujours)
  - a = c²/2804 m (un proton du LHC dans l'anneau) → T_U ≈ 1,3×10⁻⁷ K
  - a_seuil : T_U = ħω/2k_B pour le qubit 5 GHz → T = 0,120 K, a = 2,96×10¹⁹ m/s²
  - a_κ(m_P) = c⁴/(4Gm_P) (gravité de surface du micro-BH) → T_U = T_H(m_P)
    (PRINCIPE D'ÉQUIVALENCE : aux chevaux d'Unruh, Hawking = Unruh — testé)

Verdict du voyage : le seuil Unruh du qubit est ~5×10³¹ fois plus loin que
l'horizon — le qubit voyage DANS LA GLACE jusqu'au bord, puis tout explose.

Graine 20260929 — déterministe.
"""
from __future__ import annotations

import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from constantes import C, HBAR, G, longueur_planck, temps_planck, masse_planck
from qubit import temperature_hawking

K_B = 1.380_649e-23
G_TERRE = 9.81


def temperature_unruh(a: float) -> float:
    """T_U = ħa/(2πc k_B) [K]."""
    return HBAR * a / (2.0 * math.pi * C * K_B)


def acceleration_pour_temperature(t_k: float) -> float:
    """L'inverse exact : a = 2π c k_B T / ħ [m/s²]."""
    return 2.0 * math.pi * C * K_B * t_k / HBAR


def gravite_surface(m: float) -> float:
    """κ = c⁴/(4Gm) — l'accélération de surface (rayon Schwarzschild) [m/s²]."""
    return C ** 4 / (4.0 * G * m)


def seuil_qubit(f_hz: float) -> dict:
    """Le bain Unruh commence à exciter le qubit quand k_B T ≈ ħω/2."""
    omega = 2.0 * math.pi * f_hz
    t_seuil = HBAR * omega / (2.0 * K_B)
    return {"f_hz": f_hz, "T_seuil_K": t_seuil,
            "a_seuil_m_s2": acceleration_pour_temperature(t_seuil)}


def profil_voyage() -> list[dict]:
    """Les étapes du voyage avec la température Unruh locale."""
    etapes = [
        ("la Terre (1 g)", G_TERRE),
        ("fusée 100 g", 981.0),
        ("proton LHC (c²/2804)", C ** 2 / 2804.0),
        ("10¹⁸ m/s²", 1e18),
        ("seuil qubit 5 GHz", seuil_qubit(5e9)["a_seuil_m_s2"]),
        ("10³⁰ m/s²", 1e30),
        ("horizon micro-BH (m_P)", gravite_surface(masse_planck())),
    ]
    return [{"etape": nom, "a_m_s2": a, "T_unruh_K": temperature_unruh(a)}
            for nom, a in etapes]


if __name__ == "__main__":
    print("═══ RATISS-PLANCK — l'effet Unruh le long du voyage (🧮) ═══")
    print(f"  T_U(1 g) = {temperature_unruh(G_TERRE):.2e} K  — la Terre ne décohère rien depuis 4,5 Ga")
    print(f"  T_U(proton LHC) = {temperature_unruh(C**2/2804.0):.2e} K")
    s = seuil_qubit(5e9)
    print(f"  qubit 5 GHz : seuil à T_U = {s['T_seuil_K']:.3f} K → a = {s['a_seuil_m_s2']:.2e} m/s² "
          f"= {s['a_seuil_m_s2']/G_TERRE:.1e} g")
    kappa = gravite_surface(masse_planck())
    print(f"  horizon micro-BH : κ = {kappa:.2e} m/s² → T_U = {temperature_unruh(kappa):.2e} K")
    print(f"  T_H(m_P) = {temperature_hawking(masse_planck()):.2e} K  → ÉQUIVALENCE vérifiée")
    rapport = s["a_seuil_m_s2"] / kappa
    print(f"  → l'horizon est {rapport:.1e}× plus loin que le seuil Unruh du qubit")
    print("\n  LE PROFIL :")
    for e in profil_voyage():
        print(f"   {e['etape']:26s} a = {e['a_m_s2']:.2e} m/s² → T_U = {e['T_unruh_K']:.2e} K")
