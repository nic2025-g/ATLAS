# Modèle Conceptuel de Données (MCD) — ATLAS

> Basé sur l'analyse des 4 projets pilotes  
> Communauté de Communes du Grand Avignon — Août 2025

---

## Diagramme entité-association

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   TERRITOIRE ──────────────── OPÉRATION ────────────────── MOE             │
│   (commune,                  (projet                       (cabinet         │
│    CC, dept)     1    N       d'aménagement)   N    1       technique)      │
│                                    │                                        │
│                           ┌────────┴────────┐                              │
│                           │                 │                              │
│                      1    │            1    │                              │
│                           ▼                 ▼                              │
│                    OPÉRATION          OPÉRATION                            │
│                   ×                  ×                                     │
│                    PHASE              INDICATEUR                           │
│                  (fact_ops)           (fact_dd)                            │
│                      │                    │                               │
│                 N    │               N    │                               │
│                      │                    │                               │
│              ┌───────┤           ┌────────┤                               │
│              │       │           │        │                               │
│              ▼       ▼           ▼        ▼                               │
│           PHASE  SUBVENTION  TYPE_IND  TYPE_TRAVAUX                       │
│         (cycle    (aide       (surface   (Voirie,                         │
│          vie)     externe)    perméable…) AEP, EU…)                       │
│              │       │                                                     │
│              │       ▼                                                     │
│              │    ORGANISME                                                │
│              │   (Agence Eau,                                              │
│              │    Région…)                                                 │
│              │                                                             │
│              ▼                                                             │
│          CALENDRIER                                                        │
│         (jour, mois,                                                       │
│          annee_mandat)                                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Entités et attributs

### OPÉRATION
Entité centrale du modèle. Représente un projet d'aménagement individualisé.

| Attribut | Type | Contrainte | Exemple |
|----------|------|-----------|---------|
| **numero_ref** *(PK)* | Texte | Unique | 4243946_2301 |
| intitule | Texte | Obligatoire | Requalification av. de Verdun |
| complexite | Énuméré | Faible/Moyenne/Élevée | Moyenne |
| date_os_moe | Date | | 01/02/2021 |
| responsable_moa | Texte | | S. Chabert |
| responsable_moe | Texte | | O. Mozol |

**Associations :** se situe dans 1 TERRITOIRE · est suivi par 1 MOE · génère N OPÉRATION×PHASE · génère N OPÉRATION×INDICATEUR

---

### PHASE
Étape du cycle de vie réglementé par la loi MOP.

| Attribut | Type | Contrainte | Exemple |
|----------|------|-----------|---------|
| **code_phase** *(PK)* | Texte | AVP/PRO/ACT/DET/AOR | AVP |
| libelle | Texte | | Avant-Projet |
| ordre | Entier | 1–5 | 1 |
| budget_produit | Texte | | budget_avp |

**Cardinalité avec OPÉRATION :** 1 opération peut traverser 1 à 5 phases · 1 phase peut concerner N opérations → **M-N** résolu par OPÉRATION×PHASE

---

### OPÉRATION × PHASE *(association porteuse)*
Fait central du modèle. Granularité : 1 ligne = 1 opération × 1 phase.

| Attribut | Type | Description |
|----------|------|-------------|
| budget_avp | Décimal | Estimation AVP |
| budget_pro | Décimal | Estimation PRO |
| prix_marche | Décimal | Prix contractuel |
| montant_engage | Décimal | Situations cumulées |
| cout_final | Décimal | Coût définitif AOR |
| montant_avenant | Décimal | Total avenants |
| date_debut | Date | Démarrage de la phase |
| date_fin_prevue | Date | Fin contractuelle |
| date_fin_reelle | Date | Fin effective |

---

### SUBVENTION
Aide financière notifiée par un organisme externe.

| Attribut | Type | Contrainte | Exemple |
|----------|------|-----------|---------|
| **subvention_id** *(PK)* | Entier | Auto-incrémenté | 1 |
| montant_notifie | Décimal | Obligatoire, > 0 | 83 000 |
| taux | Décimal | En % | 8,0 |
| lot | Entier | 1, 2 ou 3 | 1 |
| nature_travaux | Texte | AEP/EU/EP/Aménagement | EU |
| date_notification | Date | | 28/04/2022 |

**Cardinalités :**
- 1 OPÉRATION peut avoir 0 à N SUBVENTIONS
- 1 ORGANISME peut notifier 1 à N SUBVENTIONS
- 1 SUBVENTION concerne 1 TYPE_TRAVAUX

---

### ORGANISME
Entité versant les subventions.

| Attribut | Type | Exemple |
|----------|------|---------|
| **nom** *(PK)* | Texte | Agence de l'Eau RMC |
| type | Texte | Agence / État / Région / Département |
| echelon | Texte | national / régional / départemental |
| taux_plafond | Décimal | 8,0 |

**5 organismes identifiés :** Département de Vaucluse · Agence de l'Eau RMC · Agence de l'Eau RMC - volet pluvial · Région Sud PACA · État-DETR

---

### TYPE_TRAVAUX
Nomenclature standardisée (8 catégories) pour rendre les bordereaux de prix comparables.

| Attribut | Type | Exemple |
|----------|------|---------|
| **code** *(PK)* | Texte | AEP |
| libelle | Texte | Eau potable (AEP) |
| eligible_subvention | Booléen | true |
| indicateur_vert | Booléen | true |

---

### INDICATEUR_DD *(nouveauté issue des données réelles)*
16 indicateurs de développement durable par projet.

| Attribut | Type | Exemple |
|----------|------|---------|
| **type_indicateur_id** *(PK)* | Entier | 1 |
| libelle | Texte | Surface supplémentaire perméable |
| categorie | Texte | Bas-Carbone / Biodiversité / Social |
| unite | Texte | m² |

---

### OPÉRATION × INDICATEUR *(association porteuse)*
Mesures par projet avec cibles et valeurs constatées.

| Attribut | Type | Description |
|----------|------|-------------|
| valeur_cible | Décimal | Valeur définie au PRO |
| valeur_constatee | Décimal | Valeur mesurée à l'avancement |
| bilan | Texte | Dépassé / Conforme / En retrait |

---

### TERRITOIRE *(dimension aplatie — star schema pur)*

| Attribut | Type | Exemple |
|----------|------|---------|
| **territoire_id** *(PK)* | Entier | 1 |
| nom_commune | Texte | Les Angles |
| code_insee | Texte | 30010 |
| nom_communaute | Texte | CC du Grand Avignon |
| nom_departement | Texte | Vaucluse |
| nom_region | Texte | Provence-Alpes-Côte d'Azur |

*Choix d'aplatissement justifié : star schema pur, 1 seule jointure, drill-down natif Power BI.*

---

### MOE

| Attribut | Type | Exemple |
|----------|------|---------|
| **moe_id** *(PK)* | Entier | 1 |
| nom_moe | Texte | Artelia |
| type_moe | Texte | Bureau d'études |
| specialite | Texte | VRD, hydraulique urbaine |

---

### CALENDRIER *(dimension temporelle)*

| Attribut | Type | Spécificité |
|----------|------|-------------|
| **date_id** *(PK)* | Entier YYYYMMDD | |
| date_complete | Date | |
| annee | Entier | |
| annee_mandat | Entier | **1 à 6 — spécifique ATLAS** |
| is_mandat_courant | Booléen | KPI "budget du mandat" |

---

## Règles de gestion

| # | Règle | Impact modèle |
|---|-------|--------------|
| RG-01 | Une subvention = 1 montant notifié uniquement (pas de versements) | Pas de colonne montant_verse |
| RG-02 | Phases dans l'ordre : AVP → PRO → ACT → DET → AOR | Colonne `ordre` dans PHASE |
| RG-03 | Un projet peut avoir 1 à 5 subventions (0 pour le Lot 3 souvent) | fact_subventions nullable |
| RG-04 | Chaque projet a exactement 16 indicateurs DD | Contrainte OPÉRATION×INDICATEUR |
| RG-05 | dim_territoire est aplatie — pas de snowflake | Star schema pur |
| RG-06 | annee_mandat calculé depuis la date de début du mandat | dim_calendrier à seed |

---

*MCD ATLAS · v1.0 · Août 2025 — basé sur l'analyse des 4 projets pilotes*
