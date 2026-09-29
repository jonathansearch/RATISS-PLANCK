# 🧱 RATISS-PLANCK — Vérifier le mur de Planck

**Mission (29/09/2026, Jonathan Evina, RATISS Labs) :**
> « vérifier le mur de Planck dans notre univers et ce qui se passe exactement
> si tu peux dépasser, pour voir si c'est la frontière de notre univers virtuel
> ou s'il y a des fluctuations encore plus petites »

**Type de campagne : 🧮 in silico + bases réelles. Zéro matériel, zéro promesse.**
**40/40 tests verts · 7 figures · graine 20260929 · étiquettes calcul/synthèse jamais mélangées.**

---

## 📏 La base réelle (CODATA 2022, NIST — récupérée le jour J)

Tout le mur tient sur trois constantes. Deux sont **exactes** (c, h — SI 2019),
une seule est **floue** : G (±2,2×10⁻⁵). C'est elle qui rend la position du mur incertaine.

| Grandeur | Notre calcul | CODATA 2022 |
|---|---|---|
| ℓ_P | 1,616255×10⁻³⁵ m | 1,616255(18)×10⁻³⁵ m ✔ |
| t_P | 5,391246×10⁻⁴⁴ s | 5,391247×10⁻⁴⁴ s ✔ |
| m_P | 2,176434×10⁻⁸ kg | 2,176434×10⁻⁸ kg ✔ |
| E_P | 1,2209×10¹⁹ GeV = 1,956×10⁹ J | 1,2209×10¹⁹ GeV ✔ |
| T_P | 1,4168×10³² K | — |

**La position du mur n'est connue qu'à ±0,0011 % — et l'incertitude vient de G, la constante la plus mal mesurée de la physique.**

---

## ❓ Question 1 — Le mur existe-t-il ? Est-ce la frontière pixel de l'univers ?

**Réponse calculée (`mur.py`, `figures/fig_1_mur.png`) : NON — ce n'est pas un mur de matière, et rien ne prouve que ce soit une frontière.**

Le « mur » est le **croisement de deux équations** :
- la mécanique quantique : sonder Δx exige λ̄ = ħc/Δx — **plus c'est petit, plus il faut d'énergie** (courbe qui descend) ;
- la relativité générale : cette énergie fabrique un trou noir r_s = 2GE/c⁴ — **plus il y a d'énergie, plus ça s'effondre** (courbe qui monte).

Ces deux courbes se croisent **une seule fois**, à E = E_P/√2 = **1,38×10⁹ J** (l'énergie d'un éclair moyen) sur une longueur de **√2·ℓ_P = 2,29×10⁻³⁵ m**. Trouvé par balayage log + bissection (précision relative < 10⁻¹⁴, testé).

**Le mur est le point où nos deux meilleures théories se contredisent — pas un mur que l'univers aurait construit.** ℓ_P est une **échelle de croisement**, comme dit la littérature ; l'idée qu'elle soit un « pixel » de l'espace est une hypothèse, pas une donnée. (La partie Q3 montre que la version naïve du pixel est déjà exclue.)

**La validation par la réalité : notre formule de collideur, testée sur le vrai LHC, retrouve 2 801 m pour 2 804 m réels (7 TeV/c, 8,33 T — test automatisé).** Et le même calcul dit : pour AMENER une particule à E_P, il faut un anneau de **516 années-lumière de rayon** (fig_2) — le mur n'est pas un problème d'énergie (un éclair !), c'est un problème de **concentration** : mettre un éclair entier dans une particule.

## 🚪 Question 2 — Que se passe-t-il si on dépasse ?

**Réponse calculée (`depassement.py`, `figures/fig_4_depassement.png`) : la traversée naïve est BARRÉE par un trou noir — pas par un gardien, par la géométrie.**

- Pour voir Δx, il faut λ̄ ≤ Δx, donc E ≥ ħc/Δx. Mais r_s = 2GE/c⁴ = 2ℓ_P²/Δx.
- **Le trou noir fabriqué dépasse la cible dès que Δx < √2·ℓ_P** : en dessous, sonder = fabriquer un trou noir PLUS GRAND que ce qu'on voulait observer (Doplicher–Fredenhagen–Roberts 1995 — recalculé ici, testé).
- Δx = ℓ_P → r_s/Δx = 1. Δx = 0,5 ℓ_P → r_s/Δx = 4. Dépasser ne montre rien : ça NOIE la cible dans son propre horizon.

**Et « après la barrière » ? Cinq portes théoriques** (fig_4 droite — **étiqueté SYNTHÈSE LITTÉRAIRE : aucune donnée, aucune décision**) : RG naïve = passage bouché ; cordes = miroir T-dualité (R ↔ ℓ_P²/R — « en dessous » = « au-dessus », la question perd son sens) ; boucles = espace quantique + Big Bounce ; sécurité asymptotique = pas de mur du tout ; CDT = le continu émerge du discret. **Aucune n'est décidable aujourd'hui — RATISS documente, ne tranche pas.**

## 🌊 Question 3 — Y a-t-il des fluctuations encore plus petites ?

**Réponse : les données réelles interdisent déjà le pixel naïf dispersif de taille ℓ_P — mais ce qui vit SOUS ℓ_P/10 reste, lui, totalement non contraint. La porte est encore ouverte.**

Recalcul complet (`mousse.py`) : distance comobile de GRB 090510 intégrée numériquement dans la cosmologie Planck 2018 (**3 153 Mpc = 10,3 milliards d'al**), retard prédit par un pixel de taille ℓ_P sur le photon de 31 GeV : **824 ms**. Fermi a vu : **aucun retard** (borne ≈ 85 ms sous hypothèses conservatrices). → un pixel dispersif de taille ℓ_P est **exclu** ; le pixel maximal non exclu est **< ℓ_P/10** (1,67×10⁻³⁶ m — calculé, testé).

| Limite réelle publiée | E_QG,1 (unités de E_P) |
|---|---|
| Fermi 2009 (GRB 090510, *Nature/Science*) | > 1,2 |
| Fermi-LAT 2013 (4 GRBs, *PRD 87, 122001*) | > 7,6 |
| LHAASO 2024 (GRB 221009A, *PRL*) | **> 10** ← record |
| LHAASO 2024 (GRB 221009A, *JCAP*) | > 12 |

Et les effets **quadratiques** (doux) ne sont exclus qu'à E_QG,2 > 10¹² GeV = 10⁻⁷ E_P : **la fenêtre quadratique reste grand ouverte** (fig_3 droite). Côté labo : le Holometer de Fermilab (2015) n'a vu **aucun** bruit holographique corrélé — le premier modèle testable d'« univers pixelisé » est exclu à haute signification. LIGO, lui, exclut déjà un bruit de métrique d'amplitude Planck **sans** le caractère transverse holographique spécifique.

## 🔵 Question 4 (mission v0.1 du soir) — le qubit informationnel au mur

**La mission du chef : « puisque la matière, en le mesurant, ne passe pas le mur, envoie un qubit informationnel porteur et regarde ce qui va lui arriver. »** (`qubit.py`, `figures/fig_5_qubit.png`)

Prémisse calculée (Landauer) : **un qubit sans porteur n'existe pas** — l'information est physique (1 bit à 300 K = 2,87×10⁻²¹ J), elle hérite donc du mur :

- **Le couloir GUP** : la relation d'incertitude gravitationnelle Δx ≥ ħ/(2Δp) + ℓ_P²Δp/ħ a un plancher **exactement à √2·ℓ_P** — retrouvé par descente numérique à 10⁻⁶ (12e test vert). **Même une fonction d'onde ne passe pas le mur : sa propre largeur minimale EST le mur.**
- **La capacité holographique** : une cellule de taille ℓ_P stocke π/ln2 = **4,53 bits** ; au plancher (√2 ℓ_P de rayon), il reste **9,1 bits de marge pour loger 1 qubit** — ça passe au mur, sans plus.
- **L'écume naïve ne le décohère pas** (résultat NÉGATIF, cohérent avec le nul du Holometer) : il faudrait **10²³ ans** au bruit de marche aléatoire de Planck pour voler 1 rad de phase à un qubit micro-onde 5 GHz — 12 900× l'âge de l'univers. (Et si l'écume cumule ~46 µm sur l'âge de l'univers, la longueur d'onde de 6 cm du qubit s'en moque.)
- **Le sort du porteur poussé sous le mur** : micro-trou noir de masse m_P, évaporation de Hawking en **16 085 t_P = 8,7×10⁻⁴⁰ s** à T_H = 5,6×10³⁰ K. Et là : **le qubit ressort-il intact de l'évaporation ? PARADOXE DE L'INFORMATION — NON RÉSOLU** (Page 1993 → île/formule de Page 2019). Le calcul s'arrête exactement où la physique s'arrête, étiquette « synthèse littéraire » sur la suite.

**Verdict du voyage (3 zones, fig_5 droite) :** LIBRE au-dessus de 100 ℓ_P (l'écume est inoffensive) · AU MUR entre √2 et 100 ℓ_P (9,1 bits de marge au plancher) · TROU NOIR en dessous (porteur effondré, sort du qubit = question ouverte n°1 du domaine). **Le porteur d'information va aussi loin que la matière — pas plus loin — mais il va plus loin que la QUESTION : le paradoxe qu'il ouvre est le vrai chantier.**

## 🌊 v0.2 — les options (a) et (b) du chef : Page et Unruh (🧮)

### (a) La courbe de Page — `page.py` + `fig_6_page.png` : l'information RESSORT

Question : pendant l'évaporation, où passe l'information du trou noir ? **Modèle jouet de Page (étiqueté comme tel)** : 512 états purs de Haar sur N=12 qubits, entropie du rayonnement en fonction des qubits émis.

- La simulation colle la **formule analytique de Page à 0,001 bit** sur tout le parcours (testée, y compris sur l'exemple calibré publié de Page : 4×4 dims = 1,3306 bits exactement).
- **Le virage est là** : l'entropie monte (0 → 5,28 bits), pic EXACTEMENT à N/2, redescend (→ 0). Hawking naïf (thermique à jamais, ligne pointillée) est contredit : **le rayonnement « sait déjà tout » à la moitié de l'évaporation**.
- ⚠️ Deux bugs attrapés par nos propres tests en route : la somme de Page va jusqu'à **m·n** (dims multipliées — ma première version avait m+n) et un facteur ½ dans la moyenne. Corrigés, testés, documentés — l'honnêteté RATISS inclut nos propres erreurs.

### (b) L'effet Unruh — `unruh.py` + `fig_7_unruh.png` : 31 ordres de glace, puis le flambage

Le qubit porteur est un observateur accéléré : T_U = ħa/(2πck_B).

| Étape du voyage | a (m/s²) | T_Unruh |
|---|---|---|
| la Terre (1 g) | 9,81 | 4,0×10⁻²⁰ K |
| proton du LHC | 3,2×10¹³ | 1,3×10⁻⁷ K |
| **seuil du qubit 5 GHz** | 3,0×10¹⁹ | **0,12 K** |
| horizon du micro-BH | 1,4×10⁵¹ | **5,6×10³⁰ K = T_H** |

- **Le principe d'équivalence, chiffré et TESTÉ** : à la gravité de surface du micro-trou noir (κ = c⁴/4Gm_P), le bain Unruh = la température de Hawking exactement (accord < 10⁻⁶).
- **Verdict du voyage** : entre le seuil de décohérence du qubit (0,12 K à 3×10¹⁹ m/s²) et l'horizon (1,4×10⁵¹ m/s²), il y a **31 ordres de grandeur** — le porteur voyage DANS LA GLACE jusqu'au bord, puis tout flambe d'un coup. La décohérence Unruh n'est pas un frein du voyage : c'est la DÉFINITION du mur.

## 🎯 Verdict de la mission (en 3 lignes)

1. **Le mur existe comme croisement des équations, pas comme pixel** — le prouver « frontière » est impossible avec les données actuelles, et les données DISPOULAIENT déjà la version naïve.
2. **Dépasser = fabriquer un trou noir** (calculé, √2 ℓ_P, testé) — ou payer un anneau de 516 années-lumière.
3. **Oui, il peut y avoir des fluctuations plus petites que ℓ_P** : tout ce qui est sous ℓ_P/10 sans dispersion linéaire n'est pas encore contraint. La quête continue à une échelle sous le mur.

## 🔬 Reproduire (une commande, graine 20260929)

```bash
python3 planck/constantes.py    # les unités du mur vs CODATA
python3 planck/mur.py           # croisement, seuil √2 ℓ_P, collideur
python3 planck/mousse.py        # GRB 090510, retards, pixel maximal
python3 planck/depassement.py   # la barrière de trou noir
python3 planck/qubit.py         # le qubit informationnel au mur
python3 planck/page.py          # la courbe de Page (modèle jouet)
python3 planck/unruh.py         # l'effet Unruh le long du voyage
python3 planck/figures.py       # les 4 figures
python3 tests/test_planck.py    # 14/14
```

## 📁 Structure

```
RATISS-PLANCK/
├── planck/       constantes · mur · mousse · depassement · qubit · figures
├── figures/      fig_1_mur · fig_2_collideur · fig_3_mousse · fig_4_depassement · fig_5_qubit
├── tests/        test_planck.py (14) · test_qubit.py (12)
├── DONNEES/      bases_externes.json (CODATA, Fermi, LHAASO, Holometer — sources datées)
├── outils/       manifeste.py (sceau SHA-256)
└── MANIFESTE.json
```

## 🧭 Étiquettes RATISS (jamais mélangées)

- **🧮 calcul** : unités de Planck, croisement/bissection, seuil √2 ℓ_P, rayon de courbure, D_C(z), retards LIV, pixel maximal — tout testé, tout rejouable.
- **📚 synthèse littéraire** : les 5 portes théoriques, l'interprétation « pixel » — explicitement étiquetées, jamais présentées comme des données.

*RATISS Labs · Jonathan Evina (18 ans, Yaoundé) · MIT · le labo qui mesure sa portée avant de rêver plus loin.*
