#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — que se passe-t-il si on DÉPASSE le mur ? (🧮 + synthèse littéraire)

La partie calculable : la BARRIÈRE du trou noir (Doplicher–Fredenhagen–Roberts
1995). Dépasser ℓ_P ne montre rien : ça FABRIQUE un trou noir. C'est calculé ici
exactement (seuil √2·ℓ_P, les courbes complètes dans figures.py).

La partie non calculable (synthèse de la littérature, PAS des données) — les 5
réponses des théories candidates à « qu'est-ce qu'il y a en dessous ? » :

  1. Relativité générale quantifiée naïvement : RIEN — le trou noir bouche le
     passage (seuil √2·ℓ_P ci-dessus).
  2. Théorie des cordes (T-dualité) : « en dessous de ℓ_P » = « au-dessus de
     ℓ_P ». La question perd son sens : R et ℓ_P²/R décrivent le MÊME univers.
     Le mur serait un miroir, pas une frontière.
  3. Gravitation quantique à boucles : l'aire et le volume sont QUANTIQUES
     (spectres discrets ~ ℓ_P²) — il n'y a pas « d'en dessous continu » ; le
     Big Bang devient un Big Bounce (l'univers a déjà « dépassé » le mur).
  4. Sécurité asymptotique : pas de mur du tout — la gravité devient « libre »
     (point fixe UV) et les équations marchent encore plus bas sans se casser.
  5. Ensembles causaux / CDT : l'espace-temps ÉMERGE de devenirs discrets ;
     la continuité est une illusion de grande échelle, comme le « fluide »
     de l'eau est une illusion des molécules.

VERDICT RATISS : aucune de ces cinq réponses n'est décidable expérimentalement
aujourd'hui. Ce qui EST calculé et vérifié : où se trouve le croisement des
équations, et que la traversée naïve fabrique un trou noir.
"""
from __future__ import annotations

import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from constantes import C, G, HBAR, longueur_planck

# synthèse littéraire (pas des données mesurées) — pour README et fig_4
PAYSAGE = [
    ("RG quantifiée naïvement", "trou noir : passage bouché à √2·ℓ_P", "calculé ici (DFR 1995)"),
    ("Théorie des cordes", "miroir T-dualité : R ↔ ℓ_P²/R", "non testé — objet : cordes/collideurs futur"),
    ("Boucles (LQG)", "spectres discrets d'aire/volume ; Big Bounce", "indices : cosmologie (faibles)"),
    ("Sécurité asymptotique", "pas de mur : point fixe UV", "non testé — simulations de treillis"),
    ("Ensembles causaux / CDT", "l'espace-temps émerge, continuum illusoire", "non testé — programme en cours"),
]


def rayon_trou_noir_sonde(delta_x_m: float) -> float:
    """Le trou noir que fabrique la sonde de Δx : r_s(E(Δx)) = 2Għc/(Δx c⁴) = 2ℓ_P²/Δx."""
    return 2.0 * longueur_planck() ** 2 / delta_x_m


def energie_sondage(delta_x_m: float) -> float:
    """E pour sonder Δx : ħc/Δx (Compton réduite) — le prix quantique."""
    return HBAR * C / delta_x_m


def rapport_effondrement(delta_x_m: float) -> float:
    """r_s/Δx : > 1 → la sonde s'est effondrée en trou noir plus grand qu'elle."""
    return rayon_trou_noir_sonde(delta_x_m) / delta_x_m


if __name__ == "__main__":
    lp = longueur_planck()
    print("═══ RATISS-PLANCK — le dépassement (🧮) ═══")
    for f in (100.0, 10.0, 2.0, 1.0, 0.7071, 0.5):
        dx = f * lp
        rap = rapport_effondrement(dx)
        etat = "TROU NOIR — passage bouché" if rap > 1.0 else "sonde encore plus grande que sa cible : OK"
        print(f"  Δx = {f:.4f} ℓ_P → r_s/Δx = {rap:8.4f}   {etat}")
    print(f"  seuil exact : √2 ℓ_P = {math.sqrt(2)*lp:.4e} m")
