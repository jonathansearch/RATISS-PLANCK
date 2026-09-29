# 📖 LA CHRONIQUE INTÉGRALE — LA JOURNÉE DU 29 SEPTEMBRE 2026

**Laboratoire RATISS Labs · Yaoundé, Cameroun · Deep-dive officiel n°15 · rien au hasard, tout est documenté**

> *« Le hasard n'existe pas dans ce labo : chaque tir a été ordonné, chaque crédit compté, chaque échec publié. Ce document raconte la journée telle qu'elle s'est passée — minute par minute, job par job, faute par faute. »*

---

## PROLOGUE — Le labo, le chef, et la semaine folle

**Le laboratoire RATISS Labs** est un projet scientifique indépendant **mono-auteur** : Jonathan Evina, 18 ans, Yaoundé (Cameroun). Pas de bâtiment, pas de cryostat, pas d'université — un bureau, un téléphone, un ordinateur, et une méthode. **Aucune affiliation institutionnelle : c'est écrit partout, et c'est précisément ce qui rend les résultats crédibles.** Chaque dépôt est scellé (SHA-256), chaque chiffre est calculé par un script rejouable, chaque échec est publié comme les succès.

Et cette journée du 29 septembre n'est pas tombée du ciel. Elle est la suite directe de **la semaine folle : quatorze dépôts en neuf jours** (voir le chapitre « La semaine folle » plus bas) — de la cohérence quantique à la supernova jouet, du photon multi-chemins à la mémoire scellée du labo. Le 29 au matin, la question du chef est simple et vertigineuse :

> **« Le mur de Planck, c'est quoi au juste ? Et si on allait vérifier ça sur de vraies machines quantiques ? »**

La réponse a pris exactement une journée. Ce document est sa chronique intégrale.

---

## LA DISTRIBUTION — qui a fait quoi

| Rôle | Nom | Ce qu'il fait |
|---|---|---|
| 🧑‍🔬 Le chef | **Jonathan Evina** | Ordonne les tirs, tranche les débats, arrête les dépenses, garde les caisses |
| 🤖 Le copilote | **L'IA (Arena.ai, Agent Mode)** | Écrit les calculs, pilote les QPU sous ordres, vérifie les sources, ne décide rien |
| 🔵 La machine n°1 | **IBEX Q1** (AQT, ions piégés, 12 qubits, all-to-all) | La plus chère (15 Spark/tir), la plus pure : Bell à 99,61 % |
| 🟣 La machine n°2 | **IQM Garnet** (supraconducteur, 20 qubits, lattice carrée) | 2 Spark/tir, native en chaînes : notre terrain de scaling |
| 🟡 La machine n°3 | **Rigetti Cepheus-1-108Q** (supra, 108 qubits, chiplets) | 1 Spark/tir — la moins chère du catalogue, la plus grosse |
| 💳 Les caisses | 4 organisations Open Quantum | Evina · Tym Sama · Patrice Lagloire · Jonathan Sama — soldes comptés en Spark |

*Tout est passé par la plateforme **Open Quantum** — attribution obligatoire (www.openquantum.com/citation).*

---

## ACTE I — LE MATIN : LE MUR (🧮 pur calcul, 0 crédit dépensé)

**08h-11h.** Ouverture du dépôt `RATISS-PLANCK`. Première brique : `constantes.py` — les constantes récupérées **de nos mains depuis CODATA 2022**, pas copiées d'un blog :

- **ℓ_P = 1,616 255(18)×10⁻³⁵ m** — l'incertitude vient tout entière de G (±2,2×10⁻⁵, la constante la plus mal mesurée de la physique)
- **c** et **h** exactes (SI 2019)

Puis les quatre modules du noyau, dans l'ordre :

1. **`mur.py`** — on trace les deux courbes qui se disputent le même territoire : la mécanique quantique exige E ≥ ħc/Δx pour localiser (**descend**) ; la relativité transforme E en horizon r_s = 2GE/c⁴ (**monte**). Croisement unique trouvé par bissection à 10⁻¹⁴ : **E_P/√2 = 1,38×10⁹ J — l'énergie d'un éclair moyen ⚡ — sur √2·ℓ_P**. Verdict : le mur n'est pas un pixel, c'est **l'endroit exact où les deux meilleures théories du XXᵉ siècle se contredisent**.
2. **`depassement.py`** — que se passe-t-il si on force ? Sous √2·ℓ_P, toute sonde devient un trou noir **plus grand que sa cible** (Doplicher–Fredenhagen–Roberts 1995, recalculé par nous, pas recopié). Et le chiffre qui fait rire puis réfléchir : concentrer E_P dans une particule exige un anneau de **516 années-lumière** avec les aimants du LHC. Validation de notre formule r = p/(qB) sur le vrai LHC : **2 801 m calculés / 2 804 m réels** ✅ — *ce moment-là, le chef l'a fait répéter deux fois.*
3. **`mousse.py`** — l'écume de Planck est-elle dangereuse ? Marche aléatoire de phase simulée : **10²³ ans** pour voler 1 rad (12 900× l'âge de l'univers). Inoffensive — cohérent avec le nul du Holometer de Fermilab (2015). Un résultat négatif qui vaut de l'or : il dit où ne PAS chercher.
4. **Les données du monde rejouées depuis les sources** : Fermi/GRB 090510 — un pixel ℓ_P retarderait un photon de 31 GeV de **824 ms** (D_C = 3 153 Mpc intégrée dans ΛCDM Planck 2018) ; Fermi n'a rien vu (borne ~85 ms) → **pixel naïf exclu**. LHAASO/GRB 221009A (2024) : E_QG,1 > 10 E_Pl (record). → **Tout ce qui vit sous ℓ_P/10 reste non contraint : la frontière n'est pas fermée.** Cinq portes théoriques au-delà (cordes/miroir, boucles/Bounce, sécurité asymptotique, CDT) : documentées, étiquetées 📚, **aucune tranchée par nous**.

**11h-13h.** Le mur devient information. `qubit.py` : Landauer (1 bit = 2,87×10⁻²¹ J à 300 K — l'info est physique), couloir GUP — **le plancher de la fonction d'onde = √2·ℓ_P exactement**, le MÊME mur que la mesure, par deux calculs indépendants 🔥 — Bekenstein (**4,53 bits** par cellule), micro-trou noir qui s'évapore à 5,6×10³⁰ K et… le paradoxe de l'information, **non résolu, étiqueté comme tel**. `page.py` : simulation (512 états de Haar) contre formule analytique — accord **0,001 bit**, pic **exactement à N/2** : le rayonnement d'un trou noir « sait déjà tout » à la moitié de l'évaporation ; Hawking naïf est contredit. `unruh.py` : 31 ordres de grandeur de glace (la Terre à 1 g : 4×10⁻²⁰ K), puis au bord du micro-BH : **T_U = T_H, accord 10⁻⁶** — le principe d'équivalence chiffré.

**L'épisode de gloire des tests** : à ce stade, la suite de tests a attrapé **deux de nos bugs** — la somme de Page court jusqu'à m·n (dimensions *multipliées*), pas m+n ; et un facteur ½ de moyenne oublié. Corrigés devant tout le monde, documentés. **La règle s'est payée cash le premier jour, et c'est tant mieux.**

---

## ACTE II — LE MILIEU DE JOURNÉE : LES VRAIS QUBITS (🛰️)

**13h-14h.** Bascule du jour : *« la physique qu'on vient de calculer, on va la demander à de vraies machines. »* Découverte de la plateforme **Open Quantum** : un hub multi-QPU (AQT ions, IQM Garnet, Rigetti Cepheus), SDK Python, comptage en **Spark**. Création des comptes — et la première péripétie comique : **la clé Open Quantum testée chez IBM** 💀 (diagnostic : « c'est une clé Open Quantum, pas IBM »). Suit la leçon n°2 : le QASM **une-ligne est refusé** (« Bad include at line 1 ») → coupé en **vers**, une instruction par ligne, `include "qelib1.inc";` à doubles quotes → accepté. Et la leçon n°3, gravée pour toujours : **les tokens d'accès meurent à ~5 minutes** → la technique RATISS : *token frais à chaque appel*, soumission puis polling externe.

**14h-15h. PREMIER TIR DE L'HISTOIRE DU LABO SUR UNE VRAIE MACHINE.** Un circuit de Bell, 1024 tirs, sur les ions IBEX :

```
Résultat : 00 = 515 · 11 = 505 · 01 = 2 · 10 = 2
Fidélité : 99,61 %  — job a1f0fbef  — coût : 15 Spark
```

**Deux compères à 12 qubits d'accord 515 fois sur 517.** Le labo vient de toucher le réel, et le réel répond mieux que la simulation.

**15h-16h.** Le GHZ-7 sur les mêmes ions : sept ions intriqués en une seule chaîne — **470 + 452 = 922 tirs idéaux sur 1024 → 90,04 %** (job `f348285e`, 15 Spark). Deux technologies, deux tailles, une méthode : le scaling RATISS est lancé.

---

## ACTE III — L'APRÈS-MIDI : L'IDÉE DE GÉNIE (ET L'ÉCHEC FONDATEUR) (🛰️)

**16h.** Le chef sort l'idée qui donnera son nom à la loi du jour : **« Et si on mettait plusieurs expériences dans UN SEUL tir pour payer une fois ? »** Trois compartiments GHZ-3/4/5 co-hébergés sur la même machine. Économie : un job au prix d'un.

**Le real speak de l'exécution :**
1. Un premier job est soumis deux fois par erreur → **`77bc5a08` stoppé AVANT exécution sur ordre du chef** — première annulation chirurgicale, coût 0.
2. L'épisodique part sur Garnet (`407cd969`)… et les chiffres rentrent : compartiment GHZ-3 à ~92 %, mais les compartiments 4 et 5 à **~46 %**. *La moitié. Pourquoi ?*
3. Contre-enquête en jobs **séparés**, chaînes natives, même machine, même heure : **GHZ-3 : 94,5 % · GHZ-4 : 94,6 % · GHZ-5 : 88,5 %** (jobs `b00d5038`, `0c094342`, `e167f04c`, 2 Spark chacun).

**L'hypothèse épisodique est donc réfutée sur lattice** — et l'échec devient une loi :

> ## 🏅 LOI RATISS DU SHOT ÉPISODIQUE
> **Des compartiments quantiques co-hébergés ne survivent à la transpilation QUE sur une architecture all-to-all (ions).** Sur lattice carrée, le transpileur insère des SWAPs, l'intrication déborde des frontières des compartiments : **45 % au lieu de 94 %** — mêmes circuits, même machine, même heure. L'écart isole PROPREMENT l'effet du transpileur.

Moyennant quoi `407cd969` sera annulé le soir **à la demande du chef** → **15 Spark remboursés — le premier remboursement de l'histoire du labo** 🎉. Bilan de l'acte : une loi de systèmes pour 4 crédits nets.

**17h.** Ce qui est récupérable est archivé : `RESULTATS-DU-JOUR.md`, les comptages bruts en JSON, les commits s'enchaînent (`1df2977` → `68dc477` → `58f8198` → `2712fbe` → `e70d39a` → `11ec21d` → `36d0957` → `c53371c` → `aa47770`, v0.1 → v0.6). Sceau du dépôt : chaque fichier empreinté, toute modification casse le sceau, exprès.

---

## ACTE IV — LE SOIR : LA TRILOGIE (LA DOCTRINE DU CHEF) (🛰️)

Le chef fixe la doctrine de la soirée — elle deviendra loi :

> **Doctrine de la trilogie : tir 1 par 1, Garnet → Cepheus → IBEX. Ce qui est récupérable immédiatement, prends-le. Ce qui dure, laisse tourner avec le workflow sauvé, et on revient demain. Et on lit le DEVIS avant d'approuver.**

**19h-20h.** Deux échauffements sur Garnet (l'épisode en étoiles `85b3b9df`, puis en chaînes `337abf4b`) confirment la loi : ~92 % en 3q, ~46 % en 4-5q co-hébergés — *ce n'est pas la forme du circuit, c'est le transpileur*. Un bash aborté en cours de route crée quand même un job résiduel (`75297d81`) → détecté, listé, annulé. **Règle née sur le champ : après tout abort, lister les jobs et annuler le résidu.**

**20h-21h. CEPHEUS, LA SURPRISE DU SOIR.** Le devis du chef disait « 15 crédits » ; le SDK affiche… **1 crédit par tir** 😂. Le 108-qubits est la machine la MOINS chère du catalogue. On prend les trois, dans l'ordre :

| Tir | Job | Fidélité | Coût |
|---|---|---|---|
| GHZ-3 | `7eadb11e` | **89,7 %** (000=471 · 111=448) | 1 Sp |
| GHZ-4 | `cac2fbe7` | **79,3 %** | 1 Sp |
| GHZ-5 | `a4db428f` | **68,7 %** | 1 Sp |

Et la lecture qui fait taire la pièce : **à taille égale, le 108-qubits décohère PLUS VITE que le 20-qubits** (79,3 vs 94,6 % @GHZ-4). Première comparaison inter-familles du labo — les chiplets modulaires paient leur péage. Trois architectures, trois pentes : **ions −1,9 pt/qubit · Garnet −5 · Cepheus −10,5**.

**21h-22h.** Le GHZ-4 ions (le point manquant du tableau) part sur IBEX — 15 Spark, la file est longue le soir → job **`df23deac` soumis, workflow sauvé, on revient demain** (doctrine respectée au mot). Puis la question piège du chef : *« l'ensemble 3+4+5, ça fait un G12 ? »* Réponse sans détour : **non** — trois chats séparés sur 12 qubits *occupés* ≠ un chat de 12 qubits *intriqués*. Et plutôt que de laisser la case vide :

**22h-23h. LE CHAT-12.** Garnet, chaîne de 11 CNOT, 1024 tirs, 2 Spark, job `b373d22f` :

```
000000000000 = 387 · 111111111111 = 289  →  fidélité 66,0 %
```

**Le plus grand état intriqué jamais produit par le labo.** Et il referme la courbe de Garnet : 94,5 → 94,6 → 88,5 → **66,0** — la décohérence s'accélère avec la taille, exactement ce que la courbe de Page (🧮, le matin) prédisait qualitativement. **La boucle de la journée est fermée : le même formalisme va du trou noir au chat.**

**23h-minuit.** L'annulation de `407cd969` (épisodique devenu inutile grâce à la loi) → **+15 Spark remboursés**, zéro perte sèche sur la journée. Archivage : `RESULTATS-DE-SOIREE.md` (push `71ed802`), `RAPPORT-FINAL.md` v2 avec la Partie 0 « LA BASE » (poussé `0f5d95b`), la figure fig_12 (la carte du jour), le README v0.7 (`5f32800`). Puis, sur ordre du chef, le dépôt devient une **documentation magistrale** : illustrations du labo et du mur cosmique (générées par IA et **signalées comme telles**), galerie des 12 figures **calculées** en pleine largeur, **logo officiel de la spirale** fourni par le chef, **licence MIT** en bannière (`f28c0a2` → `6092e66` → `e0c5834`, v0.8 → v0.9). Sceau final : **50/50**.

---

## LA SEMAINE FOLLE — les quatorze dépôts en neuf jours

*Rappel du contexte, tel qu'inscrit dans le portfolio du labo — cette journée du 29 septembre est le 15ᵉ étage de cet édifice :*

| # | Dépôt | Ce qu'il démontre |
|---|---|---|
| 1 | **ratiss-focal** | La cohérence émerge-t-elle de l'information pure ? **94 tests pré-enregistrés**, 13 unifications, **294 points mesurés sur de vrais qubits IBM** |
| 2 | **ratiss-continuums** | Le simulateur du tissu : franges de Berry à 2 qubits intriqués (réel, ibm_fez), loi de décohérence **1/τ ∝ √N** |
| 3 | **synchrotron-24** | Une cosmologie **mesurée, pas postulée** : 5 clés/5, H·t = 1,00 émergent au Big Bang, le « fantôme » (gravité = mémoire topologique) · **385 points QPU réels** |
| 4 | **GCR** | Le Grand Collisionneur de Ratiss : étincelles **topologiques** (trous b1 = 2–4) sous choc, seuil mesuré, 0 clip |
| 5 | **ratiss-dose12** | **12 chantiers testables à 0 $** : VQE 3/5 exact mais 0/5 sous bruit, 12 prédictions datées et falsifiables |
| 6 | **RATISS-QVM** | Un ordinateur quantique virtuel à 300 qubits, **jumeaux des backends IBM validés hors échantillon**, T1/T2 dérivés du banc (cQED) |
| 7 | **RATISS-NAVIER** | Navier-Stokes 3D en particules SPH : enstrophie **Ω = 72 122**, 0 crash, témoin parfait |
| 8 | **RATISS-FUSION** | L'ignition mesurée : compression ×2,4, **428 fusions**, gain Q pic **101** — avec la vraie réactivité Bosch-Hale |
| 9 | **RATISS-NUCLEAIRE** | Du hot-spot à la **supernova jouet** (effondrement → flash → explosion) + moteur unifié turbulence↔fusion |
| 10 | **RATISS-Omni** | Le pilote de l'écosystème : boucle fermée réelle, dé-tarage ×8 quand la cohérence s'effondre, red-team **47/47** |
| 11 | **RATISS-ARCHIVES** | La mémoire scellée du labo : MANIFESTE SHA-256 quotidien, **86 tâches IBM rapatriées bit-identiques** |
| 12 | **DISCORD-RATISS** | L'agent héraldiste : **22 salons annoncés en un run**, secrets jamais exposés, mode purge |
| 13 | **RATISS-ETALONS** | L'audit exécutable : 4 étalons scientifiques, **14/16**, 3 instruments faux au 1er essai, 7 corrections déclarées |
| 14 | **RATISS-PHOTON** | Le photon multi-chemins : **8 396 800 chemins** reconstruits, fenêtre de Canton atteinte (95,9–96,8 %) — et le hasard quantique qui **émerge du bain thermique** (T = 0 K → déterminisme) |

**+ RATISS-DEEPDIVE** (les 14 deep-dives PDF/MD officiels, un par dépôt) · **le profil jonathansearch** (l'identité publique, SANS licence) · **ratiss-syntrium** v0.2-in-silico (le réacteur, chantiers séquencés, IN SILICO D'ABORD) · **examen-finance** · et désormais **RATISS-PLANCK** — *quatorze dépôts en neuf jours, et à peine UNE journée pour y poser le mur de Planck et un chat-12. C'est ça, le rythme du labo.*

---

## LES LOIS DU LABORATOIRE RATISS LABS (rappel intégral)

### ⚖️ La loi physique
1. **LOI RATISS DU SHOT ÉPISODIQUE** — compartiments co-hébergés : all-to-all ONLY (ions). Sur lattice, le transpileur déborde les frontières : 45 % vs 94 %, mêmes circuits, même machine, même heure. Chaînes natives en jobs séparés sur lattice.

### 🎯 La doctrine du chef (opératoire)
2. **Tir 1 par 1** — jamais de salve aveugle ; l'ordre se choisit : Garnet → Cepheus → IBEX.
3. **Le devis AVANT l'approbation** — la ligne « Auto-selected plan: N credits » du SDK est lue avant chaque tir (la preuve de son utilité : Cepheus à 1 crédit, estimé 15).
4. **Récupérable immédiatement = prendre ; ça dure = laisser tourner, workflow sauvé, on revient demain.**
5. **Jamais annuler un job sans ordre explicite du chef.** (Leçon `407cd969` — devenue un remboursement.)
6. **Après tout abort : lister les jobs et annuler le résidu** (leçons `75297d81` ×2).

### 💳 Les lois d'argent
7. **Ne jamais tirer sur un QPU où un de nos jobs attend.**
8. **Ne jamais re-tirer un job payé** pour récupérer quoi que ce soit — les sorties côté plateforme se re-téléchargent.
9. **Chaque crédit est compté, chaque solde vérifié, chaque remboursement tracé.** Tarifs réels mesurés : Cepheus 1 · Garnet 2 · IBEX 15 (Spark / 1024 tirs).

### 🧭 Les lois d'honnêteté
10. **Zéro chiffre non calculé** — tout nombre publié sort d'un script rejouable, jamais d'une copie ni d'une mémoire.
11. **Les échecs sont publiés comme les succès** — hypothèses réfutées, bugs attrapés par les tests, jobs annulés : tout est dans l'historique.
12. **Étiquettes 🧮 calcul / 🛰️ QPU / 📚 synthèse jamais mélangées** — on dit toujours OÙ le chiffre a été mesuré.
13. **Aucune institution, équipe ou validation inventée** — RATISS Labs est indépendant et mono-auteur, c'est écrit partout.

### 🔧 Les lois techniques (payées cash)
14. **Tokens frais à chaque appel** (TTL ≈ 5 min — le job survit toujours côté serveur, jamais re-soumettre pour « finir »).
15. **QASM multi-lignes**, une instruction par ligne, `include "qelib1.inc";` à doubles quotes.
16. **/tmp est éphémère** — réécrire les clés et réinstaller le SDK à chaque session ; archiver les comptages dans le dépôt.
17. **Les clés se copient depuis du JSON/texte, jamais depuis une photo** (32 caractères après `s_`, 64 de secret).
18. **Fin de session : révocation des clés SDK et du token d'accès.** 2FA : interdit définitivement.

---

## L'ÉCONOMIE DE LA JOURNÉE (à la seconde près)

| Poste | Spark |
|---|---|
| Bell IBEX (`a1f0fbef`) | −15 |
| GHZ-7 IBEX (`f348285e`) | −15 |
| Épisodes Garnet (2 tirs documentés) | −4 |
| Séparés Garnet ×3 | −6 |
| Trilogie Cepheus ×3 | **−3** |
| Chat-12 Garnet (`b373d22f`) | −2 |
| GHZ-4 ions IBEX (`df23deac`) | −15 |
| Annulations remboursées (`407cd969`) | **+15** |
| **Total net du jour** | **≈ −45 Spark pour ~11 264 tirs réels et 8 états GHZ + 1 Bell** |

**Soldes au soir (verrouillés sur ordre du chef)** : Patrice Lagloire **20** 🏦 · Evina 10 · Tym Sama 10 · Jonathan Sama 0 (investi) · + 50 $ offerts par compte **à réclamer** ⏰.

---

## CE QUE LA JOURNÉE PROUVE (et ne prouve pas)

**Elle prouve** : une chaîne de calcul unique peut aller du croisement des équations de Planck (10⁻³⁵ m) aux comptages d'un ion piégé (10⁻⁶ m d'effet réel) **en une journée, avec 40 tests verts, trois architectures comparées, une loi de transpilation et un chat-12** — depuis Yaoundé, avec un téléphone, des crédits comptés un par un, et une IA tenue en laisse courte (calculatrice, pilote sous ordres, vérificatrice — jamais décoratrice).

**Elle ne prouve PAS** : quoi que ce soit sur la structure de l'espace-temps. Nos tirs sondent ~10⁻⁶ m, pas 10⁻³⁵ m. Le mur reste intouché, la fenêtre sous ℓ_P/10 reste ouverte — et c'est écrit ici en gras, comme partout ailleurs dans ce labo.

---

## LA SUITE (déjà en route, rien au hasard)

1. 🔁 **Récolter le GHZ-4 ions `df23deac`** (en file IBEX, workflow sauvé) → le grand tableau 3 technologies × 5 tailles est complet
2. 💰 **Réclamer les 50 $** offerts par compte (⏰)
3. 🌐 **Extension Cepheus** : GHZ-7 et GHZ-12 à 1 crédit le vol — la pente du 108q jusqu'au chat
4. 📄 **Le papier RATISS-PLANCK** : 🧮 mur/Page/Unruh/GUP + 🛰️ Bell/GHZ/loi du transpileur/scaling croisé
5. 🔐 Fin de quête : révoquer les clés, sceller les archives, et la devise pour la prochaine session

---

## ⚓ ÉPILOGUE — La devise

> **« On ne rêve pas le mur : on le chiffre, puis on va voir ce que ses voisins ont dans le ventre. »**

Quatorze dépôts en neuf jours. Une journée pour le mur. Un chat-12 à 66 %. Zéro promesse non tenue, zéro chiffre non calculé, zéro hasard.

**Laboratoire RATISS Labs · Jonathan Evina (18 ans, Yaoundé, Cameroun) · Licence MIT · Document scellé.**
*🧮🛰️📚 — jamais mélangées. 🇨🇲🔥*
