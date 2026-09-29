#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — le qubit informationnel au mur (🧮).

La question du chef : « puisque la matière, en mesurant, ne passe pas le mur,
envoie un qubit informationnel porteur et regarde ce qui va lui arriver. »

Le cadre honnête (Landauer 1991) : UN QUBIT SANS PORTEUR N'EXISTE PAS.
L'information est physique : l'écrire coûte de l'énergie (≥ kT·ln2 par bit),
la stocker est borné (Bekenstein/Hawking : S = A/(4ℓ_P²)·k_B), la déplacer
exige un porteur matériel. Donc le qubit HÉRITE du mur — et c'est calculable :

  1. Le couloir GUP : Δx ≥ ħ/(2Δp) + ℓ_P²·Δp/ħ  →  largeur minimale √2·ℓ_P
     (numériquement vérifiée) — même une fonction d'onde ne descend pas sous le mur.
  2. La capacité holographique : bits(Δx) = π·(Δx/ℓ_P)²/ln2 — une cellule de
     taille ℓ_P stocke π/ln2 ≈ 4,53 bits. Le qubit (1 bit) passe au mur SANS marge.
  3. L'écume naïve (marche aléatoire σ_ℓ = √(ℓ_P·c·t)) : le qubit micro-onde
     perd 1 rad de phase en ~10¹⁵ ans — l'écume ne le décohère PAS (résultat
     négatif utile, cohérent avec le nul du Holometer).
  4. Le sort du porteur poussé sous le mur : micro-trou noir de masse m_P,
     évaporation de Hawking en 5120π·t_P ≈ 16 085·t_P = 8,7e-40 s,
     T_H = T_P/(8π) = 5,6e30 K. Le qubit ressort-il intact ? PARADOXE NON
     RÉSOLU (synthèse littéraire : Page 1993, Penington 2019, PSSY 2019).

Graine 20260929 — déterministe.
"""
from __future__ import annotations

import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from constantes import C, HBAR, G, Q_E, longueur_planck, temps_planck, masse_planck, energie_planck_j

K_B = 1.380_649e-23
LP = longueur_planck()
TP = temps_planck()
MP = masse_planck()


# ── 1. l'information est physique ────────────────────────────────────────────
def energie_landauer_bit(T: float) -> float:
    """Énergie minimale pour écrire/effacer 1 bit à T : k_B·T·ln2 (Landauer)."""
    return K_B * T * math.log(2.0)


def energie_porteur_photon(delta_x: float) -> float:
    """Le porteur le plus léger pour ten un qubit DANS Δx : E = ħc/Δx."""
    return HBAR * C / delta_x


# ── 2. le couloir GUP (gravité quantique phénoménologique) ───────────────────
def gup_delta_x(delta_p: float) -> float:
    """Δx_min(Δp) = ħ/(2Δp) + ℓ_P²·Δp/ħ (convention β=1 → plancher √2·ℓ_P)."""
    return HBAR / (2.0 * delta_p) + LP ** 2 * delta_p / HBAR


def heisenberg_delta_x(delta_p: float) -> float:
    """Le plancher quantique standard, sans gravité : ħ/(2Δp)."""
    return HBAR / (2.0 * delta_p)


def plancher_gup_numerique() -> float:
    """Trouve le minimum de la courbe GUP par descente (attendu √2·ℓ_P)."""
    p_opt = math.sqrt(HBAR ** 2 / (2.0 * LP ** 2))     # dérivée nulle : Δp = ħ/(√2 ℓ_P)... vérifié numériquement
    bas, haut = p_opt * 0.2, p_opt * 5.0
    for _ in range(200):                                # recherche ternaire (convexe en log)
        m1 = math.sqrt(bas * haut)
        m2 = math.sqrt(bas * m1)
        m3 = math.sqrt(m1 * haut)
        if gup_delta_x(m2) < gup_delta_x(m3):
            haut = m3
        else:
            bas = m2
    return gup_delta_x(math.sqrt(bas * haut))


# ── 3. la capacité holographique ─────────────────────────────────────────────
def bits_stockables(rayon: float) -> float:
    """Bits max dans une sphère de rayon r : S/k_B·ln2 = A/(4ℓ_P²·ln2) = π r²/(ℓ_P² ln2)."""
    return math.pi * (rayon / LP) ** 2 / math.log(2.0)


# ── 4. l'écume (modèle naïf de marche aléatoire, étiqueté comme tel) ─────────
def sigma_longueur_ecume(t_s: float) -> float:
    """Marche aléatoire d'amplitude ℓ_P par temps de Planck : σ_ℓ = √(ℓ_P·c·t)."""
    return math.sqrt(LP * C * t_s)


def temps_decoherence_ecume(f_qubit_hz: float, sigma_phi_cible: float = 1.0) -> float:
    """Temps pour que l'écume naïve déphase le qubit de sigma_phi_cible rad.

    ω = 2π f ; σ_φ(t) = ω·σ_ℓ(t)/c = ω·√(ℓ_P·c·t)/c = ω·√(ℓ_P·t/c)
    → t_cible = (sigma_phi_cible·c/(ω·√ℓ_P))²/c  = σ²·c²/(ω²·ℓ_P).
    """
    omega = 2.0 * math.pi * f_qubit_hz
    return sigma_phi_cible ** 2 * C ** 2 / (omega ** 2 * LP)


# ── 5. le sort du porteur sous le mur ────────────────────────────────────────
def temps_evaporation_hawking(m: float) -> float:
    """t_evap = 5120·π·G²·m³/(ħ·c⁴)."""
    return 5120.0 * math.pi * G ** 2 * m ** 3 / (HBAR * C ** 4)


def temperature_hawking(m: float) -> float:
    """T_H = ħc³/(8πG·m·k_B)."""
    return HBAR * C ** 3 / (8.0 * math.pi * G * m * K_B)


def rapport_effondrement_porteur(delta_x: float) -> float:
    """r_s(E(Δx))/Δx = 2ℓ_P²/Δx² — le mur, côté porteur (cf. depassement.py)."""
    return 2.0 * LP ** 2 / delta_x ** 2


def voyage(delta_x: float) -> dict:
    """Le verdict du voyage selon la taille visée — LA réponse à la mission.

    Zones : TROU NOIR (Δx < √2 ℓ_P) · AU MUR (approche du plancher GUP,
    capacité holographique affichée si le stockage devient serré) ·
    LIBRE (au-dessus de 100 ℓ_P, écume naïve incapable de décohérer).
    """
    rap = rapport_effondrement_porteur(delta_x)
    bits = bits_stockables(delta_x) if delta_x > 0 else 0.0
    if rap > 1.0:
        return {"zone": "TROU NOIR", "etat": f"porteur effondré : micro-BH, "
                f"évaporation en {temps_evaporation_hawking(MP)/TP:.0f}·t_P, "
                f"T_H = {temperature_hawking(MP):.2e} K — le sort du qubit = paradoxe non résolu",
                "coherence": "NON APPLICABLE — l'horizon a avalé le porteur"}
    if delta_x > 100.0 * LP:
        return {"zone": "LIBRE", "etat": "voyageur ordinaire, phase préservée",
                "coherence": f"écume naïve : 1 rad en {temps_decoherence_ecume(5e9):.1e} s"}
    stockage = (f"capacité de la cellule : {bits:.2f} bits pour 1 bit à loger"
                + (" — SERRÉ, sans marge" if bits < 2.0 else ""))
    return {"zone": "AU MUR", "etat": f"porteur au plancher GUP (√2·ℓ_P) ; {stockage}",
            "coherence": "phase encore définie, mais plus rien en dessous"}


if __name__ == "__main__":
    print("═══ RATISS-PLANCK — le qubit informationnel au mur (🧮) ═══")
    e_bit = energie_landauer_bit(300.0)
    print(f"  1 bit à 300 K coûte  {e_bit:.3e} J = {e_bit/Q_E:.4f} eV  (Landauer : l'info EST physique)")
    print(f"  porteur photon pour Δx = 1 nm  :  {energie_porteur_photon(1e-9)/Q_E:.0f} eV")
    plancher = plancher_gup_numerique()
    print(f"  plancher GUP (numérique) :  {plancher/LP:.6f}·ℓ_P  (analytique : √2 = {math.sqrt(2):.6f})")
    print(f"  bits dans une sphère ℓ_P :  {bits_stockables(LP):.2f} bits (π/ln2)")
    t_dc = temps_decoherence_ecume(5e9)
    print(f"  qubit 5 GHz vs écume naïve :  1 rad en {t_dc:.2e} s = {t_dc/3.156e7:.1e} ans "
          f"({t_dc/3.156e7/1.38e10:.0f}× l'âge de l'univers)")
    print(f"  micro-BH à m_P : évaporation {temps_evaporation_hawking(MP)/TP:.0f}·t_P "
          f"= {temps_evaporation_hawking(MP):.2e} s · T_H = {temperature_hawking(MP):.3e} K")
    print("\n  LE VOYAGE :")
    for dx, nom in ((1e-3, "1 mm"), (1e-9, "1 nm"), (1e-15, "1 fm"), (30*LP, "30 ℓ_P"),
                    (math.sqrt(2)*LP, "√2 ℓ_P (le mur)"), (0.5*LP, "0,5 ℓ_P"), (0.1*LP, "0,1 ℓ_P")):
        v = voyage(dx)
        print(f"   Δx = {nom:14s} → [{v['zone']:9s}] {v['etat']}")
