#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK — les figures (🧮, depuis les modules ; fig_4 = schéma conceptuel étiqueté)."""
import math
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from constantes import C, G, HBAR, GEV, longueur_planck, energie_planck_j, energie_planck_gev
from mur import longueur_compton_relativiste, rayon_schwarzschild, rayon_collideur, portee_lhc
from mousse import LIMITES
from depassement import rapport_effondrement, PAYSAGE

MENTHE, AMBRE, ROUGE, GRIS, VIOLET = "#0d7377", "#d9a441", "#c0392b", "#5b6b73", "#6c5b9e"
FIGDIR = pathlib.Path(__file__).resolve().parents[1] / "figures"
LP = longueur_planck()
EP = energie_planck_j()


def _cadre(ax, titre, xs="log", ys="log"):
    ax.set_facecolor("#f7fbfb")
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    ax.grid(True, which="both", alpha=0.25, lw=0.5)
    ax.set_title(titre, fontsize=10, color="#0b3c42", pad=8)
    if xs == "log":
        ax.set_xscale("log")
    if ys == "log":
        ax.set_yscale("log")


def fig_mur():
    """LE mur : Compton λ̄(E) descend, Schwarzschild r_s(E) monte — croisement à E_P/√2."""
    e = np.logspace(math.log10(1e3 * GEV), math.log10(3e20 * GEV), 800)   # joules
    fig, ax = plt.subplots(figsize=(8.6, 6.0))
    ax.plot(e / GEV, longueur_compton_relativiste(e), color=MENTHE, lw=2.4,
            label="λ̄ = ħc/E — ce que la mécanique quantique peut sonder")
    ax.plot(e / GEV, rayon_schwarzschild(e), color=ROUGE, lw=2.4,
            label="r_s = 2GE/c⁴ — le trou noir que fabrique cette énergie")
    e_c, l_c = EP / math.sqrt(2.0), math.sqrt(2.0) * LP
    ax.axvline(EP / GEV, color=GRIS, ls=":", lw=1)
    ax.text(EP / GEV * 1.4, 3e-27, "E_Planck", color=GRIS, fontsize=8.5)
    ax.axhline(LP, color=GRIS, ls=":", lw=0.8)
    ax.text(2e3, LP * 1.6, "ℓ_P = 1,616×10⁻³⁵ m", color=GRIS, fontsize=8.5)
    ax.plot([e_c / GEV], [l_c], "o", ms=9, color=AMBRE, zorder=5)
    ax.annotate("LE MUR\nE = E_P/√2 = 8,6×10¹⁸ GeV (un éclair)\nl = √2·ℓ_P = 2,29×10⁻³⁵ m",
                xy=(e_c / GEV, l_c), xytext=(2e13, 5e-40), fontsize=9, color="#0b3c42",
                arrowprops=dict(arrowstyle="->", color=AMBRE, lw=1.4))
    ax.axvspan(1e3, e_c / GEV, color=MENTHE, alpha=0.05)
    ax.axvspan(e_c / GEV, 3e20 * GEV / GEV, color=ROUGE, alpha=0.06)
    ax.text(3e4, 1e-44, "règne quantique :\nle LHC vit ici, 15 ordres\nsous le mur", fontsize=9, color=MENTHE)
    ax.text(4e19, 1e-29, "au-delà :\ntoute sonde devient\nun TROU NOIR\n(DFR 1995)", fontsize=9, color=ROUGE)
    ax.set_xlim(1e3, 3e20)
    ax.set_ylim(1e-46, 1e-25)
    ax.set_xlabel("énergie de la sonde (GeV)")
    ax.set_ylabel("longueur (m)")
    _cadre(ax, "Le mur de Planck : le croisement des deux équations — pas un mur de matière")
    ax.legend(frameon=False, fontsize=9, loc="upper center")
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig_1_mur.png", dpi=300)
    plt.close(fig)


def fig_collideur():
    """Le collideur du mur : r = p/(qB) avec les aimants du LHC."""
    e = np.logspace(math.log10(13e3 * GEV), math.log10(EP) * 1.02, 400)
    r = rayon_collideur(e)
    fig, ax = plt.subplots(figsize=(8.6, 5.6))
    ax.plot(e / GEV, r / 9.461e15, color=MENTHE, lw=2.4,
            label="rayon de courbure à 8,33 T (aimants LHC)")
    r_lhc = rayon_collideur(6500.0 * GEV)
    ax.plot([6500.0], [r_lhc / 9.461e15], "o", ms=8, color=GRIS)
    ax.annotate(f"LHC (6,5 TeV/faisceau)\nr = {r_lhc/1000:.1f} km", xy=(6500.0, r_lhc / 9.461e15),
                xytext=(1e6, 1e-9), fontsize=9, color=GRIS,
                arrowprops=dict(arrowstyle="->", color=GRIS, lw=1.1))
    r_p = rayon_collideur(EP)
    ax.plot([EP / GEV], [r_p / 9.461e15], "o", ms=9, color=AMBRE)
    ax.annotate(f"LE MUR : E_P\nr = {r_p/9.461e15:.0f} années-lumière\ndiamètre ≈ 1 % de la Voie lactée",
                xy=(EP / GEV, r_p / 9.461e15), xytext=(3e11, 3e0), fontsize=9, color="#0b3c42",
                arrowprops=dict(arrowstyle="->", color=AMBRE, lw=1.4))
    ax.axhline(52850.0, color=VIOLET, ls="--", lw=1.2)
    ax.text(1e8, 7e4, "rayon de la Voie lactée ≈ 52 850 al", fontsize=8.5, color=VIOLET)
    ax.set_xlabel("énergie par particule (GeV)")
    ax.set_ylabel("rayon de l'anneau (années-lumière)")
    _cadre(ax, "Le prix du mur : un anneau PLUS GRAND QU'UNE GALAXIE — et l'énergie, elle, tient dans un éclair")
    ax.legend(frameon=False, fontsize=9, loc="center left")
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig_2_collideur.png", dpi=300)
    plt.close(fig)


def fig_mousse():
    """Les vraies limites publiées : la mousse naïve à ℓ_P est déjà exclue."""
    lineaires = [(n.split(" —")[0], v["E_QG_Gev"] if "E_QG_Gev" in v else v["E_QG_GeV"])
                 for n, v in LIMITES.items() if v["n"] == 1]
    quadratiques = [(n.split(" —")[0], v["E_QG_GeV"])
                    for n, v in LIMITES.items() if v["n"] == 2]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.6, 4.8))

    noms = [n for n, _ in lineaires][::-1]
    vals = [v / energie_planck_gev() for _, v in lineaires][::-1]
    couls = [MENTHE if v < 1 else "#2ecc71" for v in vals]
    ax1.barh(noms, vals, color=couls, alpha=0.85)
    ax1.axvline(1.0, color=ROUGE, ls="--", lw=1.6)
    ax1.text(1.05, -0.35, "E_Planck", color=ROUGE, fontsize=9)
    ax1.set_xscale("log")
    ax1.set_xlabel("E_QG,1 (unités de E_Planck) — dispersion linéaire")
    _cadre(ax1, "Toutes les limites sont AU-DESSUS du mur :\nun pixel ℓ_P qui disperse est EXCLU", xs="log", ys="linear")
    for i, v in enumerate(vals):
        ax1.text(v * 1.1, i, f"> {v:.1f} E_P", va="center", fontsize=8.5, color="#0b3c42")
    ax1.set_xlim(0.5, 60)

    qn = [n.split(" (")[0] + "\n(quadratique)" for n, _ in quadratiques]
    qv = [v for _, v in quadratiques]
    ax2.barh(qn, qv, color=VIOLET, alpha=0.85)
    ax2.axvline(energie_planck_gev(), color=ROUGE, ls="--", lw=1.6)
    ax2.text(energie_planck_gev() * 1.5, -0.3, "E_Planck", color=ROUGE, fontsize=9)
    ax2.set_xscale("log")
    ax2.set_xlabel("E_QG,2 (GeV) — dispersion quadratique")
    _cadre(ax2, "Ici la porte est ENCORE OUVERSE :\nles effets doux (n=2) restent non exclus", xs="log", ys="linear")
    for i, v in enumerate(qv):
        ax2.text(v * 1.3, i, f"> {v:.1e} GeV", va="center", fontsize=8.5, color="#0b3c42")
    ax2.set_xlim(1e10, 1e22)
    fig.suptitle("La mousse quantique face aux données réelles (Fermi 2009-2013, LHAASO 2024) — calcul RATISS, sources dans DONNEES/",
                 fontsize=10.5, color="#0b3c42")
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(FIGDIR / "fig_3_mousse.png", dpi=300)
    plt.close(fig)


def fig_depassement():
    """La barrière DFR (données) + les 5 portes théoriques (schéma conceptuel étiqueté)."""
    fig = plt.figure(figsize=(11.2, 6.2))
    gs = fig.add_gridspec(1, 2, width_ratios=(1.0, 1.15))

    ax = fig.add_subplot(gs[0])
    dx = np.logspace(math.log10(0.02 * LP), math.log10(30 * LP), 500)
    rap = 2.0 * LP ** 2 / dx ** 2     # r_s/Δx analytique (cohérent depassement.py)
    ax.plot(dx / LP, rap, color=MENTHE, lw=2.4)
    ax.axhline(1.0, color=ROUGE, ls="--", lw=1.4)
    ax.axvline(math.sqrt(2.0), color=ROUGE, ls="--", lw=1.4)
    ax.fill_between(dx / LP, 0.01, 100, where=(rap >= 1.0), color=ROUGE, alpha=0.10)
    ax.text(0.12, 12, "ZONE TROU NOIR :\nla sonde s'effondre\nsur elle-même", fontsize=9.5, color=ROUGE)
    ax.text(11.0, 0.02, "zone sondable", fontsize=9.5, color=MENTHE)
    ax.plot([math.sqrt(2.0)], [1.0], "o", ms=9, color=AMBRE)
    ax.annotate("√2 ℓ_P = 2,29×10⁻³⁵ m\n(bissection num. = 1e-14)", xy=(math.sqrt(2.0), 1.0),
                xytext=(5.0, 3.0), fontsize=8.5, color="#0b3c42",
                arrowprops=dict(arrowstyle="->", color=AMBRE, lw=1.2))
    ax.set_xlabel("taille visée Δx (unités de ℓ_P)")
    ax.set_ylabel("rayon du trou noir fabriqué / Δx")
    _cadre(ax, "Dépasser le mur = fabriquer un trou noir\n(calcul DFR — vérifié numériquement)")

    ax2 = fig.add_subplot(gs[1])
    ax2.axis("off")
    ax2.set_title("Et APRÈS la barrière ? 5 portes — SYNTHÈSE LITTÉRAIRE (aucune donnée, aucune décision)",
                  fontsize=10, color="#0b3c42", pad=8)
    y = 0.92
    for nom, reponse, statut in PAYSAGE:
        ax2.add_patch(plt.Rectangle((0.01, y - 0.145), 0.98, 0.135, facecolor="#e8f4f4",
                                    edgecolor=MENTHE, lw=1.2, alpha=0.9))
        ax2.text(0.03, y - 0.045, nom, fontsize=9.5, color="#0b3c42", weight="bold")
        ax2.text(0.03, y - 0.105, reponse + "  ·  " + statut, fontsize=8.2, color=GRIS)
        y -= 0.185
    ax2.text(0.48, 0.01, "Aucune n'est décidable aujourd'hui — RATISS documente, ne tranche pas.",
             ha="center", fontsize=8, color=ROUGE, style="italic")
    fig.tight_layout()
    fig.savefig(FIGDIR / "fig_4_depassement.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    FIGDIR.mkdir(exist_ok=True)
    fig_mur(); print("OK fig_1_mur")
    fig_collideur(); print("OK fig_2_collideur")
    fig_mousse(); print("OK fig_3_mousse")
    fig_depassement(); print("OK fig_4_depassement")
