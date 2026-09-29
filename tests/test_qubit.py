# -*- coding: utf-8 -*-
"""Tests qubit informationnel RATISS-PLANCK — Landauer, GUP, capacité, Hawking, voyage."""
import math
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "planck"))
K_B = 1.380_649e-23
from constantes import longueur_planck, temps_planck, masse_planck
import qubit

LP = longueur_planck()
TP = temps_planck()


def test_landauer_300k():
    # valeur connue : kT·ln2 à 300 K ≈ 2,871e-21 J ≈ 0,0179 eV
    e = qubit.energie_landauer_bit(300.0)
    assert abs(e - K_B * 300.0 * math.log(2.0)) < 1e-40
    assert abs(e / 1.602176634e-19 - 0.01792) < 1e-3


def test_temoin_zero_landauer():
    assert qubit.energie_landauer_bit(0.0) == 0.0


def test_plancher_gup_racine_de_deux():
    # le minimum numérique de la courbe GUP = √2·ℓ_P (cohérent avec le mur DFR)
    p = qubit.plancher_gup_numerique()
    assert abs(p / (math.sqrt(2.0) * LP) - 1.0) < 1e-6, f"{p/LP}"


def test_gup_retrouve_heisenberg_au_dessous():
    # pour Δp petit, GUP ≈ Heisenberg (la gravité ne se voit pas)
    p = 1.0e-30
    assert abs(qubit.gup_delta_x(p) / qubit.heisenberg_delta_x(p) - 1.0) < 1e-30


def test_capacite_holographique_cellule_planck():
    # sphère de rayon ℓ_P : π/ln2 ≈ 4,53 bits
    n = qubit.bits_stockables(LP)
    assert abs(n - math.pi / math.log(2.0)) < 1e-12
    assert 4.0 < n < 5.0


def test_capacite_temoin_zero_et_quadratique():
    assert qubit.bits_stockables(0.0) == 0.0
    # quadratique : 2× le rayon → 4× les bits
    assert abs(qubit.bits_stockables(2 * LP) / qubit.bits_stockables(LP) - 4.0) < 1e-12


def test_ecume_dans_le_passe():
    # sur l'âge de l'univers, la marche aléatoire naïve : σ_ℓ = √(ℓ_P·c·t) ≈ 4,6e-5 m
    t_univ = 1.38e10 * 3.156e7
    s = qubit.sigma_longueur_ecume(t_univ)
    attendu = math.sqrt(1.616255e-35 * 2.99792458e8 * t_univ)
    assert abs(s / attendu - 1.0) < 1e-5
    assert 1e-6 < s < 1e-3   # ~46 µm : gros cumul, MAIS...


def test_decoherence_ecume_tres_lente():
    # le résultat négatif clé : 1 rad de déphase en ≫ l'âge de l'univers (5 GHz :
    # la longueur d'onde ~6 cm est 10¹² × plus grande que la fluctuation cumulée)
    t = qubit.temps_decoherence_ecume(5e9)
    t_univ = 1.38e10 * 3.156e7
    assert t > 1e12 * t_univ


def test_evaporation_planck_5120pi():
    # identité analytique : t_evap(m_P) = 5120π·t_P
    t = qubit.temps_evaporation_hawking(masse_planck())
    assert abs(t / (5120.0 * math.pi * TP) - 1.0) < 1e-12
    assert abs(t / TP - 16084.95) < 0.1


def test_temperature_hawking_planck():
    # T_H(m_P) = T_P/(8π) ≈ 5,64e30 K
    t = qubit.temperature_hawking(masse_planck())
    t_p = 1.416784e32
    assert abs(t / (t_p / (8.0 * math.pi)) - 1.0) < 1e-3


def test_voyage_zones_monotones():
    # mm → LIBRE ; mur → AU MUR ; dessous → TROU NOIR
    assert qubit.voyage(1e-3)["zone"] == "LIBRE"
    assert qubit.voyage(math.sqrt(2.0) * LP * 1.0001)["zone"] == "AU MUR"
    assert qubit.voyage(0.5 * LP)["zone"] == "TROU NOIR"
    # et juste au-dessus du mur on est déjà en zone serrée, jamais LIBRE
    assert qubit.voyage(2.0 * LP)["zone"] == "AU MUR"


def test_porteur_photon_mur_donne_energie_planck():
    # le porteur minimal pour tenir dans ℓ_P porte E = E_P : le mur est auto-cohérent
    e = qubit.energie_porteur_photon(LP)
    from constantes import energie_planck_j
    assert abs(e / energie_planck_j() - 1.0) < 1e-12


if __name__ == "__main__":
    for nom, fn in sorted({k: v for k, v in globals().items() if k.startswith("test_")}.items()):
        fn()
        print(f"OK {nom}")
    print("TOUS LES TESTS PASSENT")
