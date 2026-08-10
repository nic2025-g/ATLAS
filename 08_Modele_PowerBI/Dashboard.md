# Dashboard — Conception sur papier

> **Principe :** chaque visuel répond à une question précise d'un utilisateur précis.  
> On conçoit d'abord, on construit ensuite.

---

## Les utilisateurs et leurs questions

| Profil | Contexte d'utilisation | Fréquence |
|--------|----------------------|-----------|
| **Élus** | Conseil communautaire — présentation publique | Mensuelle |
| **DGST** | Pilotage quotidien — détection des risques | Hebdomadaire |
| **Chef de projet** | Suivi de son opération | Quotidienne |

---

## Page 1 — Synthèse mandat (Élus)

> *"Qu'avons-nous réalisé pour les habitants depuis le début du mandat ?"*

### Question 1 — Combien avons-nous investi ?
- **Visuel :** Carte KPI
- **Mesure :** `Prix Marché`
- **Format :** 8 100 000 €
- **Titre :** Investissements engagés

### Question 2 — Quelle commune concentre le plus d'investissements ?
- **Visuel :** Carte géographique choroplèthe
- **Axe :** `Communes[nom_commune]`
- **Valeur :** `Prix Marché`
- **Couleur :** dégradé bleu — plus foncé = plus investi

### Question 3 — Où va l'argent des subventions ?
- **Visuel :** Treemap
- **Groupe :** `Organismes[nom]`
- **Valeur :** `Total Subventions`
- **Titre :** Subventions par organisme financeur

### Question 4 — Quel est le reste à charge ?
- **Visuel :** Carte KPI double
- **Mesure 1 :** `Total Subventions` → 1 109 000 €
- **Mesure 2 :** `Reste à Charge` → 6 991 000 €
- **Titre :** Financement externe vs charge collectivité

### Question 5 — Quelle est la répartition par nature de travaux ?
- **Visuel :** Graphique en barres empilées
- **Axe X :** `Operations[reference_artelia]`
- **Légende :** `Type_Travaux[libelle]`
- **Valeur :** `Prix Marché`

### Mise en page Page 1
```
┌─────────────────────────────────────────────────────────┐
│  ATLAS — Synthèse des investissements · Mandat 2020-2026│
├──────────────┬──────────────┬──────────────┬────────────┤
│ Investi      │ Subventions  │ Reste charge │ Nb projets │
│ 8 100 000 €  │ 1 109 000 €  │ 6 991 000 €  │     4      │
├──────────────┴──────────────┴──────────────┴────────────┤
│                                                         │
│  Carte choroplèthe communes    │  Treemap organismes    │
│                                │                        │
├────────────────────────────────┴────────────────────────┤
│         Barres empilées — Budget par nature de travaux  │
└─────────────────────────────────────────────────────────┘
```

---

## Page 2 — Pilotage opérationnel (DGST)

> *"Quels projets risquent de déraper ? Quels signaux d'alerte dois-je traiter ?"*

### Question 6 — Quels projets sont en retard ?
- **Visuel :** Tableau avec mise en forme conditionnelle
- **Colonnes :** Opération · Lot · Date fin prévue · Statut
- **Règle :** rouge si `date_fin_prevue < TODAY()` et `date_fin_reelle = BLANK()`

### Question 7 — Quel projet risque de déraper budgétairement ?
- **Visuel :** Graphique en barres — dépassement budgétaire
- **Axe :** `Operations[intitule]`
- **Valeur :** `Taux Dérive Budget`
- **Couleur :** vert si < 5%, orange si 5-15%, rouge si > 15%

### Question 8 — Quels risques sont avérés ?
- **Visuel :** Tableau des risques avérés
- **Colonnes :** Opération · Code risque · Gravité · Date avènement · Commentaire
- **Filtre :** `Risques[statut] = "Avéré"`

### Question 9 — Quels projets sont presque terminés ?
- **Visuel :** Jauge (gauge)
- **Mesure :** `Nb Lots Réceptionnés` / `Nb Lots total`
- **Une jauge par opération** via slicer

### Alertes en haut de page (cartes colorées)
```
┌──────────────┬──────────────┬──────────────┬────────────┐
│ 🔴 Lots      │ 🔴 Risques   │ 🟡 Dérive    │ ✅ Lots    │
│ en retard    │ avérés       │ budget       │ réceptionnés│
│     0        │     4        │    +0,6%     │     3      │
└──────────────┴──────────────┴──────────────┴────────────┘
```

### Mise en page Page 2
```
┌─────────────────────────────────────────────────────────┐
│  ATLAS — Pilotage opérationnel · DGST                   │
├──────────┬──────────┬──────────┬────────────────────────┤
│ Lots     │ Risques  │ Dérive   │ Lots réceptionnés      │
│ retard   │ avérés   │ budget   │                        │
├──────────┴──────────┴──────────┴────────────────────────┤
│  Tableau lots en retard        │  Barres dérive budget  │
├────────────────────────────────┴────────────────────────┤
│  Tableau risques avérés        │  Jauges avancement     │
└─────────────────────────────────────────────────────────┘
```

---

## Page 3 — Suivi par opération (Chef de projet)

> *"Où en est mon projet ? Quelle est ma situation financière ?"*

### Slicer en haut
- **Visuel :** Slicer liste déroulante
- **Champ :** `Operations[intitule]`
- Toute la page se filtre sur l'opération sélectionnée

### Question 10 — Où en est l'évolution budgétaire ?
- **Visuel :** Graphique cascade (waterfall)
- **Étapes :** Budget programme → AVP → PRO → Prix marché → Coût final
- **Titre :** Évolution budgétaire de l'AVP au coût final

### Question 11 — Quelles subventions ai-je obtenu ?
- **Visuel :** Tableau
- **Colonnes :** Organisme · Nature travaux · Lot · Montant notifié · Taux
- **Total :** `Total Subventions`

### Question 12 — Quels sont mes indicateurs DD ?
- **Visuel :** Tableau avec mise en forme conditionnelle
- **Colonnes :** Indicateur · Catégorie · Cible · Constaté · Bilan
- **Couleur bilan :** vert=Dépassé, bleu=Conforme, rouge=En retrait

### Mise en page Page 3
```
┌─────────────────────────────────────────────────────────┐
│  ATLAS — Suivi opération  [Slicer : choisir projet]     │
├──────────────┬──────────────┬──────────────┬────────────┤
│ Prix marché  │ Subventions  │ Reste charge │ Phase      │
├──────────────┴──────────────┴──────────────┴────────────┤
│  Cascade budgétaire AVP → Coût final                    │
├────────────────────────────────┬────────────────────────┤
│  Tableau subventions           │  Tableau indicateurs DD│
└────────────────────────────────┴────────────────────────┘
```

---

## Page 4 — Analyse financière (DGST / Élus)

> *"Comment est financé l'ensemble du programme ?"*

### Question 13 — Quel est le taux de financement externe global ?
- **Visuel :** Jauge
- **Mesure :** `Taux Financement Externe` → 13,7%
- **Cible :** 20% (objectif du mandat)

### Question 14 — Quel organisme finance le plus ?
- **Visuel :** Graphique en barres horizontales
- **Axe :** `Organismes[nom]`
- **Valeur :** `Total Subventions`

### Question 15 — Quelle nature de travaux est la plus subventionnée ?
- **Visuel :** Donut
- **Légende :** `Type_Travaux[libelle]`
- **Valeur :** `Total Subventions`

### Question 16 — Budget vs subventions par projet ?
- **Visuel :** Graphique barres groupées
- **Axe :** `Operations[intitule]`
- **Barres :** Prix marché · Total subventions · Reste à charge

---

## Récapitulatif — Questions → Visuels

| # | Question | Profil | Visuel | Mesure clé |
|---|----------|--------|--------|-----------|
| 1 | Combien avons-nous investi ? | Élus | Carte KPI | Prix Marché |
| 2 | Quelle commune concentre les investissements ? | Élus | Carte choroplèthe | Prix Marché |
| 3 | Où vont les subventions ? | Élus | Treemap | Total Subventions |
| 4 | Quel est le reste à charge ? | Élus | Carte KPI | Reste à Charge |
| 5 | Quels projets sont en retard ? | DGST | Tableau conditionnel | Nb Lots en Retard |
| 6 | Quel projet risque de déraper ? | DGST | Barres colorées | Taux Dérive Budget |
| 7 | Quels risques sont avérés ? | DGST | Tableau filtré | Nb Risques Avérés |
| 8 | Quels projets sont presque terminés ? | DGST | Jauge | Nb Lots Réceptionnés |
| 9 | Où en est l'évolution budgétaire ? | Chef projet | Waterfall | Budget AVP → Coût Final |
| 10 | Quelles subventions ai-je obtenu ? | Chef projet | Tableau | Total Subventions |
| 11 | Quels sont mes indicateurs DD ? | Chef projet | Tableau conditionnel | Taux Conformité DD |
| 12 | Quel est le taux de financement externe ? | DGST / Élus | Jauge | Taux Financement Externe |
| 13 | Quel organisme finance le plus ? | DGST / Élus | Barres horizontales | Total Subventions |
| 14 | Quelle nature de travaux est subventionnée ? | DGST | Donut | Total Subventions |
| 15 | Budget vs subventions par projet ? | DGST / Élus | Barres groupées | Prix Marché + Subventions |

---

*Dashboard conception papier · ATLAS · Août 2026*
