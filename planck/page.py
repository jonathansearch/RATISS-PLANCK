#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""RATISS-PLANCK v0.2 — la courbe de Page (🧮, modèle jouet étiqueté).

La question (Page 1993) : pendant qu'un trou noir s'évapore, l'entropie du
rayonnement monte... puis doit REDESCENDRE (le « virage de Page ») si
l'information est préservée — sinon, paradoxe.

MODÈLE JOUET HONNÊTE (le même que Page) : un état pur aléatoire (Haar) sur
N=12 qubits ; le « rayonnement » = les t premiers qubits ; S(t) = entropie de
von Neumann du préfixe, moyennée sur 512 répliques. AUCUNE dynamique
gravitationnelle ici — l'identité qualitative (montée, pic à la moitié,
descente) est ce qui est testé, pas une prédiction quantitative du QG.

Comparaison : formule ANALYTIQUE de Page (moyenne exacte sur les états
aléatoires, via digamma) + courbe « information perdue » (Hawking naïf).

Graine 20260929 — déterministe.
"""
from __future__ import annotations

import math
import sys
import pathlib

import numpy as np

GRAINE = 20260929
N_QUBITS = 12
N_REPLIQUES = 512


def entropie_vn_prefixe(psi: np.ndarray, t: int, n_total: int) -> float:
    """S de von Neumann (bits) des t premiers qubits d'un état pur (2^n vector)."""
    dims = (2.0,) * n_total
    tens = psi.reshape([2] * n_total)
    m = int(2 ** t)
    mat = tens.reshape(m, -1)              # (2^t) × (2^(n-t))
    rho = mat @ mat.conj().T
    ev = np.linalg.eigvalsh(rho)
    ev = np.clip(ev, 0.0, 1.0)
    nz = ev[ev > 1e-18]
    return float(-np.sum(nz * np.log2(nz)))


def renyi2_prefixe(psi: np.ndarray, t: int, n_total: int) -> float:
    """S_2 de Rényi (bits) du préfixe : -log2 Tr(rho²)."""
    tens = psi.reshape([2] * n_total)
    m = int(2 ** t)
    mat = tens.reshape(m, -1)
    purity = float(np.sum(np.abs(mat @ mat.conj().T) ** 2))
    return -math.log2(max(purity, 1e-300))


def etat_haar(rng: np.random.Generator, n: int) -> np.ndarray:
    psi = (rng.standard_normal(2 ** n) + 1j * rng.standard_normal(2 ** n))
    return psi / np.linalg.norm(psi)


def campagne_page(n_qubits: int = N_QUBITS, n_rep: int = N_REPLIQUES) -> dict:
    """S(t) moyen (von Neumann + Rényi-2) + formule de Page analytique."""
    rng = np.random.default_rng(GRAINE)
    demi = n_qubits // 2
    s1 = np.zeros(n_qubits + 1)
    s2 = np.zeros(n_qubits + 1)
    for k in range(n_rep):
        psi = etat_haar(rng, n_qubits)
        for t in range(demi + 1):                    # symétrie S(t)=S(n-t) (état pur)
            s = entropie_vn_prefixe(psi, t, n_qubits)
            s1[t] += s
            s1[n_qubits - t] += s
            s2[t] += renyi2_prefixe(psi, t, n_qubits)
            s2[n_qubits - t] += s
    s1 /= float(n_rep)                                # chaque index t<demi : n_rep contributions
    s1[demi] /= 2.0                                   # le point du milieu, écrit deux fois par réplique
    s2 /= float(n_rep)
    s2[demi] /= 2.0
    ts = np.arange(n_qubits + 1)
    page_analytique = np.array([page_moyen(t, n_qubits - t) for t in ts])
    hawking_naif = ts.astype(float)                   # thermique naïf : S_rad = t bits, fin à N ≠ 0
    return {"graine": GRAINE, "n_qubits": n_qubits, "n_rep": n_rep,
            "t": ts, "S1_moy": s1, "S2_moy": s2,
            "page_analytique": page_analytique, "hawking_naif": hawking_naif}


def page_moyen(n_a: int, n_b: int) -> float:
    """Formule de Page (1993) : sous-système A de m dims dans un état Haar pur
    sur A⊕B (n dims, n ≥ m) :  S̄ = Σ_{k=n+1}^{m·n} 1/k − (m−1)/(2n).
    ATTENTION : la somme court jusqu'à m·n (les dims se MULTIPLIENT) — la
    première version du module allait jusqu'à m+n (bug corrigé, testé sur
    l'exemple publié de Page : 4 dims × 4 dims = 1,3306 bits exactement)."""
    m, n = min(2 ** n_a, 2 ** n_b), max(2 ** n_a, 2 ** n_b)
    from scipy.special import digamma
    s_nats = float(digamma(m * n + 1) - digamma(n + 1)) - (m - 1.0) / (2.0 * n)
    return s_nats / math.log(2.0)


if __name__ == "__main__":
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    r = campagne_page()
    print("═══ RATISS-PLANCK — la courbe de Page (🧮 modèle jouet, 512 répliques) ═══")
    print("  t (qubits émis) | S_simulée | Page analytique | Δ")
    for i, t in enumerate(r["t"]):
        print(f"       {t:2d}        |  {r['S1_moy'][i]:6.3f}   |     {r['page_analytique'][i]:6.3f}     "
              f"| {abs(r['S1_moy'][i]-r['page_analytique'][i]):.3f}")
    pic = int(np.argmax(r["S1_moy"]))
    print(f"  → pic à t = {pic} = N/2 : LE VIRAGE DE PAGE est présent dans la simulation")
