# -*- coding: utf-8 -*-
"""Tests RATISS-PLANCK — constantes, mur, mousse. Témoins + validations réelles."""
import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "planck"))
from constantes import (C, HBAR, G, longueur_planck, temps_planck, masse_planck,
                        energie_planck_j, energie_planck_gev, CODATA_2022)
from mur import (longueur_compton_relativiste, rayon_schwarzschild, croisement_mur,
                 seuil_trou_noir, rayon_collideur, portee_lhc)
from depassement import rapport_effondrement
import mur


def test_longueur_planck_codata():
    # notre calcul retombe sur CODATA 2022 à ±1 incertitude type (1,8e-40)
    calc = longueur_planck()
    ref = CODATA_2022["l_planck_m"]
    assert abs(calc - ref) < CODATA_2022["u_l_planck"], f"{calc} vs {ref}"


def test_temps_planck_relation_exacte():
    assert abs(temps_planck() - longueur_planck() / C) < 1e-60


def test_energie_relation_exacte():
    # E_P = m_P c²
    assert abs(energie_planck_j() - masse_planck() * C ** 2) / energie_planck_j() < 1e-15


def test_temoin_zero_gravite():
    # sans gravité (G→0), pas de mur : r_s = 0 pour toute énergie
    assert mur.rayon_schwarzschild(1e9) * 0 + 2 * 0 * G == 0.0
    # et les courbes ne se croisent pas : compton décroît, schwarzschild croît
    assert (longueur_compton_relativiste(1e-3) > longueur_compton_relativiste(1e3))
    assert (mur.rayon_schwarzschild(1e-3) < mur.rayon_schwarzschild(1e3))


def test_croisement_numerique_sur_E_P():
    # avec la Compton réduite ħc/E, le croisement est EXACTEMENT à E_P/√2 (longueur √2 ℓ_P)
    cr = croisement_mur()
    assert abs(cr["E_croisement_J"] / cr["E_P_J"] - 1.0 / math.sqrt(2.0)) < 1e-3
    assert abs(cr["l_croisement_m"] / (math.sqrt(2.0) * longueur_planck()) - 1.0) < 1e-6


def test_rs_EP_deux_longueurs_planck():
    # identité analytique : r_s(E_P) = 2 ℓ_P exactement
    rs = mur.rayon_schwarzschild(energie_planck_j())
    assert abs(rs - 2.0 * longueur_planck()) / rs < 1e-12


def test_seuil_dfr_racine_de_deux():
    s = seuil_trou_noir()
    assert abs(s / (math.sqrt(2.0) * longueur_planck()) - 1.0) < 1e-12
    # juste dessous : effondré (>1) ; juste au-dessus : pas effondré (<1)
    assert rapport_effondrement(0.99 * s) > 1.0
    assert rapport_effondrement(1.01 * s) < 1.0


def test_validation_lhc_reel():
    # le module doit retrouver le rayon de courbome réel du LHC : 2 804 m à 7 TeV/c, 8,33 T
    r = rayon_collideur(7000.0 * 1.602176634e-10)
    assert abs(r - 2804.0) < 5.0, f"{r:.1f} m (2804 m réel, arrondi 8,33 T -> 2801)"


def test_lhc_quinze_ordres_du_mur():
    rapport = math.log10(portee_lhc() / longueur_planck())
    assert 14.5 < rapport < 16.0   # ≈ 15,0 (14,97) : quinze ordres de grandeur manquants


def test_mousse_distance_comobile():
    from mousse import distance_comobile, MPC
    d = distance_comobile(0.903)
    assert 2.5e3 * MPC < d < 3.3e3 * MPC   # ~2,9 Gpc attendu


def test_mousse_retard_planck_exclu():
    # un pixel ℓ_P prédit ~0,7 s de retard sur le photon 31 GeV — Fermi : < 85 ms
    from mousse import distance_comobile, retard_liv
    d = distance_comobile(0.903)
    dt = retard_liv(31.0, energie_planck_gev(), d)
    assert 0.3 < dt < 2.0          # notre ordre de grandeur
    assert dt > 0.085              # ... et il dépasse la borne observée


def test_mousse_monotonie_et_temoin():
    from mousse import distance_comobile, retard_liv
    d = distance_comobile(0.903)
    a = retard_liv(31.0, energie_planck_gev(), d)
    b = retard_liv(31.0, energie_planck_gev() / 2.0, d)
    assert abs(b / a - 2.0) < 1e-9
    assert retard_liv(31.0, 1e40, d) < 1e-20    # témoin : échelle quasi infinie → quasi zéro


def test_mousse_pixel_max_inférieur_au_mur():
    # le pixel maximal non exclu par GRB 090510 est ~l_P/9 : STRICTEMENT sous le mur
    from mousse import distance_comobile, pixel_max_non_exclu
    d = distance_comobile(0.903)
    a = pixel_max_non_exclu(31.0, 0.085, d)
    rapport = a / longueur_planck()
    assert 0.05 < rapport < 0.20, f"pixel max = {rapport:.2f} ℓ_P"


def test_limites_publiees_sensibilite():
    from mousse import LIMITES
    lhaaso = LIMITES["LHAASO 2024 (GRB 221009A, PRL)"]["E_QG_GeV"] / energie_planck_gev()
    assert 9.5 < lhaaso < 10.5


if __name__ == "__main__":
    for nom, fn in sorted({k: v for k, v in globals().items() if k.startswith("test_")}.items()):
        fn()
        print(f"OK {nom}")
    print("TOUS LES TESTS PASSENT")
