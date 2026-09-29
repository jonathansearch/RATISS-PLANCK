#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — figure du qubit informationnel (🧮, depuis qubit.py)."""
import math
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from constantes import longueur_planck
from qubit import (gup_delta_x, heisenberg_delta_x, bits_stockables,
                   rapport_effondrement_porteur, temps_decoherence_ecume,
                   temps_evaporation_hawking, temperature_hawking, temps_planck)

MENTHE, AMBRE, ROUGE, GRIS, VIOLET = "#0d7377", "#d9a441", "#c0392b", "#5b6b73", "#6c5b9e"
FIGDIR = pathlib.Path(__file__).resolve().parents[1] / "figures"
LP = longueur_planck()


def main():
    FIGDIR.mkdir(exist_ok=True)
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11.6, 5.2))

    # (1) le couloir GUP : la fonction d'onde ne descend pas sous √2 ℓ_P
    p = np.logspace(math.log10(1e-12 / LP), math.log10(1e8 / LP), 600) * 1.0   # Δp en unités ħ/ℓ_P → Ω
    # gup(Δp) = ħ/(2Δp) + ℓ_P² Δp/ħ : en unités de ℓ_P avec Δp = x·ħ/ℓ_P : 1/(2x) + x
    x = np.logspace(-3.0, 6.0, 600)
    dx_gup = 1.0 / (2.0 * x) + x
    dx_heis = 1.0 / (2.0 * x)
    ax.loglog(x, dx_heis, color=GRIS, lw=1.6, ls="--", label="Heisenberg seul : ħ/2Δp (pas de plancher)")
    ax.loglog(x, dx_gup, color=MENTHE, lw=2.4, label="avec gravité (GUP) : + ℓ_P²Δp/ħ")
    ax.axhline(math.sqrt(2.0), color=ROUGE, ls="--", lw=1.4)
    ax.axvline(1.0 / math.sqrt(2.0), color=ROUGE, ls="--", lw=1.0)
    ax.plot([1.0 / math.sqrt(2.0)], [math.sqrt(2.0)], "o", ms=9, color=AMBRE, zorder=5)
    ax.annotate("plancher EXACT : √2 ℓ_P\n(= le mur DFR — bissection numérique confirmée à 10⁻⁶)",
                xy=(1 / math.sqrt(2), math.sqrt(2)), xytext=(4e-1, 3e1), fontsize=8.5, color="#0b3c42",
                arrowprops=dict(arrowstyle="->", color=AMBRE, lw=1.2))
    ax.text(2e-3, 2e-4, "même une FONCTION D'ONDE\nne passe pas le mur", fontsize=9, color=ROUGE)
    ax.set_xlabel("impulsion de confinement Δp (unités de ħ/ℓ_P)")
    ax.set_ylabel("largeur du paquet d'onde Δx (unités de ℓ_P)")
    ax.set_facecolor("#f7fbfb")
    ax.grid(True, which="both", alpha=0.25, lw=0.5)
    ax.set_title("Le couloir du qubit : sa largeur minimale EST le mur", fontsize=10, color="#0b3c42", pad=8)
    ax.legend(frameon=False, fontsize=8.5, loc="upper right")

    # (2) la carte du voyage : capacité holographique + barrière, zones verdicts
    dx = np.logspace(math.log10(0.05), 3.0, 500)          # Δx en unités ℓ_P
    bits = np.pi * dx ** 2 / math.log(2.0)
    rap = 2.0 / dx ** 2
    ax2.axvspan(0.05, math.sqrt(2), color=ROUGE, alpha=0.10)
    ax2.axvspan(math.sqrt(2), 100.0, color=AMBRE, alpha=0.10)
    ax2.axvspan(100.0, 1000.0, color="#2ecc71", alpha=0.10)
    ax2.loglog(dx, rap, color=ROUGE, lw=2.2, label="effondrement r_s/Δx = 2ℓ_P²/Δx²")
    ax2.loglog(dx, bits, color=VIOLET, lw=2.2, label="capacité holographique (bits) = πΔx²/(ℓ_P² ln2)")
    ax2.axhline(1.0, color=VIOLET, ls=":", lw=1.2)
    ax2.axhline(1.0, color=ROUGE, ls="--", lw=1.4, alpha=0.0)  # garde la légende propre
    ax2.text(0.055, 2.2, "1 bit", fontsize=8, color=VIOLET)
    ax2.text(0.055, 80, "TROU NOIR :\nle porteur devient un micro-BH\n(évaporation 16 085 t_P,\nT_H = 5,6×10³⁰ K —\nsort du qubit : paradoxe non résolu)",
             fontsize=8, color=ROUGE)
    ax2.text(2.2, 4e-3, "AU MUR :\nplancher GUP √2 ℓ_P —\n9,1 bits de marge pour 1 qubit",
             fontsize=8, color="#7a5c1e")
    ax2.text(180, 4e-3, "LIBRE :\nl'écume naïve met 10²³ ans\nà voler 1 rad de phase\n(12 900× l'âge de l'univers)",
             fontsize=8, color="#1e7a34")
    ax2.set_xlim(0.05, 1000)
    ax2.set_ylim(1e-4, 1e4)
    ax2.set_xlabel("taille visée Δx (unités de ℓ_P)")
    ax2.set_ylabel("r_s/Δx (rouge) · bits stockables (violet)")
    ax2.set_facecolor("#f7fbfb")
    ax2.grid(True, which="both", alpha=0.25, lw=0.5)
    ax2.set_title("Le voyage du porteur : trois zones, trois sorts", fontsize=10, color="#0b3c42", pad=8)
    ax2.legend(frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncols=2)

    fig.suptitle("Le qubit informationnel au mur de Planck (calcul · graine 20260929) — l'information est physique, elle hérite du mur",
                 fontsize=11, color="#0b3c42")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(FIGDIR / "fig_5_qubit.png", dpi=300)
    plt.close(fig)
    print("OK fig_5_qubit")


main()
