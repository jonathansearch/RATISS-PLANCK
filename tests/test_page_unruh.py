# -*- coding: utf-8 -*-
"""Tests courbe de Page + Unruh (🧮) — témoins, virage, équivalence."""
import math
import sys
import pathlib

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "planck"))
from constantes import HBAR, G, C, masse_planck, temps_planck
import page
import unruh

K_B = 1.380_649e-23


# ── entropies élémentaires ───────────────────────────────────────────────────
def test_temoin_etat_pur_prefixe_total():
    # le préfixe = tout l'état → S = 0 (état pur global)
    rng = np.random.default_rng(1)
    psi = page.etat_haar(rng, 6)
    assert page.entropie_vn_prefixe(psi, 6, 6) < 1e-9


def test_temoin_bell_prefixe_un_qubit():
    # Bell sur 2 qubits : S(1 qubit) = 1 bit exactement
    bell = np.zeros(4, dtype=complex)
    bell[0] = bell[3] = 1.0 / math.sqrt(2.0)
    assert abs(page.entropie_vn_prefixe(bell, 1, 2) - 1.0) < 1e-12
    # et Rényi-2 pareil
    assert abs(page.renyi2_prefixe(bell, 1, 2) - 1.0) < 1e-12


def test_symetrie_prefixe_suffixe():
    # identité de Schmidt EXACTE : S(préfixe t) = S(SUFFIXE N−t) (pas préfixe-préfixe !)
    rng = np.random.default_rng(2)
    psi = page.etat_haar(rng, 8)
    s3 = page.entropie_vn_prefixe(psi, 3, 8)
    rev = psi.reshape([2] * 8).transpose(tuple(range(7, -1, -1))).flatten()
    s5_suffixe = page.entropie_vn_prefixe(rev, 5, 8)
    assert abs(s3 - s5_suffixe) < 1e-8, f"{s3} vs {s5_suffixe}"


# ── la courbe de Page ────────────────────────────────────────────────────────
def test_virage_page_present():
    r = page.campagne_page(n_qubits=12, n_rep=128)
    pic = int(np.argmax(r["S1_moy"]))
    assert pic == 6, f"pic à {pic}"
    # le pic ≈ 6 bits (la moitié de 12)
    assert 5.0 < r["S1_moy"][pic] <= 6.5
    # la montée et la descente existent vraiment
    assert r["S1_moy"][3] < r["S1_moy"][6]
    assert r["S1_moy"][9] < r["S1_moy"][6]


def test_simulation_colle_page_analytique():
    r = page.campagne_page(n_qubits=12, n_rep=256)
    ecarts = np.abs(r["S1_moy"] - r["page_analytique"])
    assert float(ecarts.max()) < 0.15, f"écart max {ecarts.max():.3f}"


def test_page_analytique_exemple_publie():
    # l'exemple CALIBRE de Page (1993) : 4 dims × 4 dims → 0,9223 nats = 1,3306 bits
    s = page.page_moyen(2, 2)
    assert abs(s - 1.3306) < 5e-4, f"{s:.4f}"

def test_page_analytique_demi_partage():
    # N=12, t=6 : S̄ ≈ 5,28 bits (6 − correction 0,72)
    s = page.page_moyen(6, 6)
    assert 5.15 < s < 5.45, f"{s:.3f}"


def test_reproductibilite_graine():
    a = page.campagne_page(n_qubits=10, n_rep=32)
    b = page.campagne_page(n_qubits=10, n_rep=32)
    assert np.array_equal(a["S1_moy"], b["S1_moy"])


# ── Unruh ────────────────────────────────────────────────────────────────────
def test_temoin_zero_acceleration():
    assert unruh.temperature_unruh(0.0) == 0.0


def test_valeur_terrestre_connue():
    # T_U(1 g) ≈ 4,0×10⁻²⁰ K (valeur de référence)
    t = unruh.temperature_unruh(9.81)
    assert abs(t / 4.0e-20 - 1.0) < 0.05


def test_linearite_en_acceleration():
    rapport = unruh.temperature_unruh(2e10) / unruh.temperature_unruh(1e10)
    assert abs(rapport - 2.0) < 1e-12


def test_equivalence_hawking_unruh():
    # aux chevaux d'Unruh : T_U(κ(m_P)) = T_H(m_P) — le principe d'équivalence chiffré
    kappa = unruh.gravite_surface(masse_planck())
    t_u = unruh.temperature_unruh(kappa)
    t_h = unruh.temperature_hawking(masse_planck())
    assert abs(t_u / t_h - 1.0) < 1e-6


def test_seuil_qubit_5ghz():
    s = unruh.seuil_qubit(5e9)
    assert abs(s["T_seuil_K"] - 0.120) < 0.005          # ~0,12 K
    assert 2e19 < s["a_seuil_m_s2"] < 4e19              # ~3e19 m/s²


def test_lhc_inoffensif():
    # le proton du LHC (a = c²/2804 ≈ 3,2e13 m/s²) : bain Unruh ≈ 1,3e-7 K
    t = unruh.temperature_unruh(C ** 2 / 2804.0)
    assert 0.5e-7 < t < 3e-7


def test_horizon_beaucoup_plus_loin_que_seuil():
    s = unruh.seuil_qubit(5e9)
    rapport = s["a_seuil_m_s2"] / unruh.gravite_surface(masse_planck())
    assert 1e-32 < rapport < 1e-30   # ~5e-31 : 31 ordres de glace avant l'horizon


if __name__ == "__main__":
    for nom, fn in sorted({k: v for k, v in globals().items() if k.startswith("test_")}.items()):
        fn()
        print(f"OK {nom}")
    print("TOUS LES TESTS PASSENT")
