#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — le mur lui-même (🧮).

La question du chef : « le mur de Planck, c'est la frontière de l'univers ? »
Réponse calculée ici : le mur est le point où les DEUX grandes équations de la
physique se contredisent.

  1. La mécanique quantique dit : pour sonder une longueur Δx, il faut
     E_compton(Δx) = ħc/(2Δx)      (plus c'est petit, plus il faut d'énergie).
  2. La relativité générale dit : une énergie E concentrée crée un trou noir
     de rayon  r_s(E) = 2GE/c⁴     (plus il y a d'énergie, plus ça s'effondre).

Ces deux courbes se CROISENT exactement à l'échelle de Planck. En dessous du
croisement, sonder = fabriquer un trou noir PLUS GRAND que ce qu'on veut voir
(Doplicher–Fredenhagen–Roberts 1995). Le mur n'est donc pas un mur de matière :
c'est le croisement de nos deux meilleures théories, calculé au micron près.

Bonus du module : le collideur du mur (rayon de courbure à champ LHC) et les
comparaisons d'échelle honnêtes. Graine 20260929, déterministe.
"""
from __future__ import annotations

import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from constantes import (C, HBAR, G, Q_E, GEV, longueur_planck, temps_planck,
                        energie_planck_j, energie_planck_gev)


def longueur_compton_relativiste(E_j: float) -> float:
    """La longueur sondable par une énergie E : λ̄ = ħc/E (Compton réduite)."""
    return HBAR * C / E_j


def rayon_schwarzschild(E_j: float) -> float:
    """Le trou noir créé par E : r_s = 2GE/c⁴."""
    return 2.0 * G * E_j / C ** 4


def croisement_mur() -> dict:
    """Trouve numériquement le croisement λ̄(E) = r_s(E) : grille log + bissection."""
    e_p_calc = energie_planck_j()
    es = math.log10(e_p_calc) - 6.0
    ee = math.log10(e_p_calc) + 6.0
    graine_e = [10.0 ** (es + i * (ee - es) / 12000.0) for i in range(12001)]
    meilleur, delta_min = None, float("inf")
    for e in graine_e:
        delta = abs(math.log10(longueur_compton_relativiste(e))
                    - math.log10(rayon_schwarzschild(e)))
        if delta < delta_min:
            delta_min, meilleur = delta, e
    # bissection : g(E) = log λ̄(E) − log r_s(E) est strictement décroissante
    bas, haut = graine_e[max(meilleur and graine_e.index(meilleur) - 2, 0)], \
        graine_e[min(graine_e.index(meilleur) + 2, len(graine_e) - 1)]

    def g(e):
        return math.log10(longueur_compton_relativiste(e)) - math.log10(rayon_schwarzschild(e))
    for _ in range(80):
        milieu = math.sqrt(bas * haut)   # moyenne géométrique (échelle log)
        if g(milieu) > 0.0:
            bas = milieu
        else:
            haut = milieu
    e_cross = math.sqrt(bas * haut)
    return {"E_croisement_J": e_cross,
            "E_P_J": e_p_calc,
            "ecart_log10": abs(g(e_cross)),
            "l_croisement_m": longueur_compton_relativiste(e_cross)}


def seuil_trou_noir() -> float:
    """Seuil DFR exact : en dessous de √2·ℓ_P, la sonde devient un trou noir.

    Mesurer d exige λ̄ = ħc/E ≤ d ET r_s = 2GE/c⁴ ≤ d. Combinaison :
    d² ≥ 2Għ/c³ = 2 ℓ_P²  →  d ≥ √2·ℓ_P (Doplicher–Fredenhagen–Roberts 1995).
    """
    return math.sqrt(2.0) * longueur_planck()


def rayon_collideur(E_j: float, b_tesla: float = 8.33) -> float:
    """Rayon de courbure r = p/(qB) — mêmes aimants que le LHC (8,33 T).

    Formule pratique : r[m] = p[GeV/c] / (0,3·B[T]).
    """
    p_gev = (E_j / GEV)          # E ≈ pc pour une particule ultra-relativiste
    return p_gev / (0.3 * b_tesla)


def portee_lhc() -> float:
    """La plus petite longueur sondable par le LHC (13 TeV) : λ = ħc/E."""
    return HBAR * C / (13_000.0 * GEV)


if __name__ == "__main__":
    lp = longueur_planck()
    ep_j = energie_planck_j()
    crois = croisement_mur()
    print("═══ RATISS-PLANCK — le mur (🧮) ═══")
    print(f"  croisement numérique λ(E)=r_s(E) : E = {crois['E_croisement_J']:.4e} J "
          f"(E_P = {ep_j:.4e} J, écart log10 = {crois['ecart_log10']:.2e})")
    print(f"  seuil DFR (sonde → trou noir)    : √2·ℓ_P = {seuil_trou_noir():.4e} m")
    print(f"  E_P en joules = {ep_j:.3e} J  ≈ {ep_j/4.184e9:.2f} tonne(s) de TNT ≈ UN ÉCLAIR moyen")
    print(f"  E_P dans UNE particule.")
    r_lhc = rayon_collideur(7000.0 * GEV)
    r_planck = rayon_collideur(ep_j)
    print(f"  validate LHC : r(7 TeV/c, 8,33 T) = {r_lhc:.0f} m (réel : 2 804 m)")
    print(f"  collideur du mur : r = {r_planck:.3e} m = {r_planck/9.461e15:.0f} années-lumière de rayon")
    print(f"  portée du LHC : {portee_lhc():.2e} m → il manque {math.log10(portee_lhc()/lp):.1f} ordres de grandeur")
