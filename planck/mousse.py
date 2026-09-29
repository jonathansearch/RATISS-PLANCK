#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — la mousse quantique : y a-t-il des fluctuations plus petites ? (🧮)

Si l'espace était « pixelisé » (univers calculé, mousse quantique), la lumière
ne voyagerait pas exactement à c : sa vitesse dépendrait de l'énergie
(dispersion) et/ou la distance flotterait (bruit holographique, marche aléatoire).

Paramétrisation standard (cf. Fermi-LAT PRD 87, 122001) :
    Δt = s_n · (1+n)/(2n) · (E_h^n − E_l^n)/E_QG,n · D/c
avec n=1 (linéaire, échelle « naturelle » E_Pl) et n=2 (quadratique).

CONTRAINTES RÉELLES (mesurées, pas inventées — sources dans DONNEES/) :
  - Fermi/GRB 090510 (2009, Science)   : E_QG,1 > 1,2 E_Pl   (pas de retard > ~85 ms)
  - Fermi-LAT 4 GRBs (2013, PRD)       : E_QG,1 > 7,6 E_Pl ; E_QG,2 > 1,3e11 GeV
  - LHAASO/GRB 221009A (2024, PRL)     : E_QG,1 > 10 E_Pl    (record actuel)
  - LHAASO (2024, JCAP)                : E_QG,1 > 14,7e19 GeV ≈ 12 E_Pl (subluminal)
  - Holometer Fermilab (2015)          : zéro bruit holographique corrélé
    → le modèle « univers pixelisé » de Hogan est exclu à haute signification.

Ici on RECALCULE la chaîne complète : distance comobile de GRB 090510 (intégrée
numériquement dans ΛCDM), retard prédit pour un pixel de taille ℓ_P, taille
maximale du pixel non exclue. Graine 20260929.
"""
from __future__ import annotations

import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from constantes import C, HBAR, longueur_planck, energie_planck_gev, GEV

# cosmologie Planck 2018
H0 = 67.4e3 / 3.0857e22      # s⁻¹
OMEGA_M, OMEGA_L = 0.315, 0.685
MPC = 3.0857e22

# ── les contraintes publiées (à jour 29/09/2026) ────────────────────────────
LIMITES = {
    "Fermi 2009 (GRB 090510, Science)":      {"n": 1, "E_QG_GeV": 1.2 * 1.2209e19},
    "Fermi-LAT 2013 (4 GRBs, PRD)":          {"n": 1, "E_QG_GeV": 7.6 * 1.2209e19},
    "LHAASO 2024 (GRB 221009A, PRL)":        {"n": 1, "E_QG_GeV": 10.0 * 1.2209e19},
    "LHAASO 2024 (GRB 221009A, JCAP)":       {"n": 1, "E_QG_GeV": 14.7e19},
    "Fermi-LAT 2013 — quadratique":          {"n": 2, "E_QG_GeV": 1.3e11},
    "LHAASO 2024 — quadratique":             {"n": 2, "E_QG_GeV": 12.0e11},
}


def distance_comobile(z: float, n_pas: int = 4000) -> float:
    """D_C = c/H0 · ∫dz/E(z), E(z)=√(Ωm(1+z)³+ΩΛ) — intégration des trapèzes."""
    integrale, h = 0.0, z / n_pas
    for i in range(n_pas + 1):
        zz = i * h
        e_z = math.sqrt(OMEGA_M * (1.0 + zz) ** 3 + OMEGA_L)
        poids = 0.5 if i in (0, n_pas) else 1.0
        integrale += poids / e_z
    return C / H0 * integrale * h


def retard_liv(E_h_GeV: float, E_qg_GeV: float, d_m: float, n: int = 1,
               s: float = 1.0) -> float:
    """Retard prédit (s) pour le photon le plus énergétique (E_l négligeable)."""
    facteur = (1.0 + n) / (2.0 * n)
    return s * facteur * (E_h_GeV / E_qg_GeV) ** n * d_m / C


def pixel_max_non_exclu(E_photon_GeV: float, retard_max_s: float, d_m: float,
                        n: int = 1) -> float:
    """Taille maximale d'un « pixel » dont la dispersion resterait invisible.

    Un réseau de pas a produit une échelle E_QG ~ ħc/a (ordre de grandeur) →
    a_max = ħc·(retard_max·c/D)^(1/n) / E_photon^n · (facteur).
    """
    facteur = (1.0 + n) / (2.0 * n)
    a = HBAR * C / E_photon_GeV / GEV * (retard_max_s * C / d_m / facteur) ** (1.0 / n)
    return a


if __name__ == "__main__":
    lp = longueur_planck()
    z_grb, e_phot, retard_max = 0.903, 31.0, 0.085   # GRB 090510 : 31 GeV, ~85 ms
    d = distance_comobile(z_grb)
    print("═══ RATISS-PLANCK — la mousse quantique (🧮) ═══")
    print(f"  D_C(z=0,903) = {d/MPC:.0f} Mpc = {d/MPC/1000:.2f} Gpc = {d/9.461e15*1e-9:.1f} milliards d'années-lumière")
    dt = retard_liv(e_phot, energie_planck_gev(), d)
    print(f"  retard prédit (31 GeV, E_QG = 1 E_Pl) : {dt*1e3:.0f} ms — Fermi n'en voit AUCUN (> {retard_max*1e3:.0f} ms exclu)")
    a_max = pixel_max_non_exclu(e_phot, retard_max, d)
    print(f"  pixel maximal non exclu (GRB) : {a_max:.2e} m = {a_max/lp:.2f} ℓ_P")
    print(f"  → un pixel de taille ℓ_P est EXCLU par les données ; s'il existe, il est < ℓ_P/10 et sans signature linéaire")
    print(f"\n  limites publiées en unités de E_Pl :")
    for nom, v in LIMITES.items():
        if v["n"] == 1:
            print(f"   · {nom:42s} E_QG,1 > {v['E_QG_GeV']/energie_planck_gev():5.1f} E_Pl")
        else:
            print(f"   · {nom:42s} E_QG,2 > {v['E_QG_GeV']/energie_planck_gev():.1e} E_Pl (quadratique)")
