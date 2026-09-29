#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK v0.2 — figures Page (fig_6) et Unruh (fig_7) (🧮)."""
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from page import campagne_page
from unruh import profil_voyage, temperature_unruh, seuil_qubit, gravite_surface
from qubit import temperature_hawking
from constantes import C, masse_planck

MENTHE, AMBRE, ROUGE, GRIS, VIOLET = "#0d7377", "#d9a441", "#c0392b", "#5b6b73", "#6c5b9e"
FIGDIR = pathlib.Path(__file__).resolve().parents[1] / "figures"


def fig_page():
    r = campagne_page()
    fig, ax = plt.subplots(figsize=(8.8, 5.8))
    t = r["t"]
    ax.plot(t, r["hawking_naif"], color=GRIS, lw=1.6, ls=":",
            label="Hawking naïf : rayonnement thermique à jamais (info DÉTRUITE)")
    ax.plot(t, r["page_analytique"], color=GRIS, lw=2.2, ls="--",
            label="Page analytique (formule exacte, digamma)")
    ax.plot(t, r["S2_moy"], color=VIOLET, lw=1.4, marker="s", ms=4, alpha=0.8,
            label="Simulation S₂ Rényi (pureté)")
    ax.plot(t, r["S1_moy"], color=MENTHE, lw=2.6, marker="o", ms=5,
            label="Simulation S von Neumann (512 répliques, graine 20260929)")
    ax.axvline(6.0, color=AMBRE, ls="--", lw=1.4)
    ax.text(6.12, 1.0, "TEMPS DE PAGE\nt = N/2 : le rayonnement\nsait déjà tout", fontsize=9, color="#7a5c1e")
    ax.annotate(f"écart max sim ↔ Page : 0,001 bit", xy=(6, 5.278), xytext=(7.0, 6.1),
                fontsize=8.5, color=MENTHE,
                arrowprops=dict(arrowstyle="->", color=MENTHE, lw=1.1))
    ax.set_xlabel("qubits émis (temps d'évaporation discret, N = 12)")
    ax.set_ylabel("entropie du rayonnement (bits)")
    ax.set_ylim(0, 7.0)
    ax.set_facecolor("#f7fbfb")
    ax.grid(True, alpha=0.25, lw=0.5)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    ax.set_title("La courbe de Page : l'information ressort AVANT la fin — le virage calculé",
                 fontsize=10.5, color="#0b3c42", pad=8)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    fig.text(0.5, 0.008, "MODÈLE JOUET (états de Haar, Page 1993) — pas de dynamique gravitationnelle : "
             "l'identité qualitative est testée, pas une prédiction QG",
             ha="center", fontsize=7.5, color=ROUGE, style="italic")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(FIGDIR / "fig_6_page.png", dpi=300)
    plt.close(fig)
    print("OK fig_6_page")


def fig_unruh():
    a = np.logspace(0.0, 52.0, 600)
    t_u = temperature_unruh(a)
    fig, ax = plt.subplots(figsize=(9.2, 5.8))
    ax.loglog(a, t_u, color=MENTHE, lw=2.6, label="T_Unruh = ħa/(2πck_B)")
    seuils = [(2.725, "fond cosmique (2,7 K)", GRIS),
              (0.010, "frigo à dilution (10 mK)", GRIS),
              (seuil_qubit(5e9)["T_seuil_K"], "seuil du qubit 5 GHz (0,12 K)", AMBRE),
              (temperature_hawking(masse_planck()), "T_Hawking du micro-BH (5,6×10³⁰ K)", ROUGE)]
    for temp, nom, coul in seuils:
        ax.axhline(temp, color=coul, ls="--", lw=1.1)
        ax.text(2e0, temp * 1.6, nom, fontsize=8, color=coul)
    # les étapes du voyage
    for e in profil_voyage():
        ax.plot([e["a_m_s2"]], [e["T_unruh_K"]], "o", ms=6, color=VIOLET, zorder=5)
    ax.annotate("la Terre (1 g)", xy=(9.81, temperature_unruh(9.81)), xytext=(1e3, 1e-24),
                fontsize=8.5, color=VIOLET, arrowprops=dict(arrowstyle="->", color=VIOLET, lw=1))
    ax.annotate("proton du LHC", xy=(C**2/2804, temperature_unruh(C**2/2804)), xytext=(1e6, 1e-12),
                fontsize=8.5, color=VIOLET, arrowprops=dict(arrowstyle="->", color=VIOLET, lw=1))
    ax.annotate("seuil qubit 5 GHz", xy=(seuil_qubit(5e9)["a_seuil_m_s2"], 0.12),
                xytext=(1e12, 1e2), fontsize=8.5, color=AMBRE,
                arrowprops=dict(arrowstyle="->", color=AMBRE, lw=1.1))
    ax.annotate("horizon du micro-BH :\nUnruh = Hawking (équivalence, testé)",
                xy=(gravite_surface(masse_planck()), temperature_hawking(masse_planck())),
                xytext=(1e28, 1e18), fontsize=8.5, color=ROUGE,
                arrowprops=dict(arrowstyle="->", color=ROUGE, lw=1.1))
    ax.axvspan(seuil_qubit(5e9)["a_seuil_m_s2"], 1e52, color=ROUGE, alpha=0.05)
    ax.set_xlabel("accélération du porteur (m/s²)")
    ax.set_ylabel("température du bain Unruh (K)")
    ax.set_facecolor("#f7fbfb")
    ax.grid(True, which="both", alpha=0.25, lw=0.5)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    ax.set_title("Le voyage d'Unruh : 31 ordres de grandeur de glace, puis l'horizon flambe",
                 fontsize=10.5, color="#0b3c42", pad=8)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig_7_unruh.png", dpi=300)
    plt.close(fig)
    print("OK fig_7_unruh")


fig_page()
fig_unruh()
