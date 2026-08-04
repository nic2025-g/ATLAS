# Rapport de stage — ATLAS
## Conception d'une plateforme décisionnelle de pilotage des investissements territoriaux

**Auteur :** BAMANIA Nicolas  
**Entreprise :** Communauté de Communes du Grand Avignon  
**Encadrant :** Dominique VOLOT — Directeur des Services Techniques  
**Période :** 15 juillet → 2 septembre 2025

---

## Résumé

Ce stage porte sur la conception et le développement d'une plateforme décisionnelle — baptisée **ATLAS** (Analyse Territoriale des Liaisons, Aménagements et Subventions) — pour la Communauté de Communes du Grand Avignon.

Le projet mobilise l'ensemble des compétences Data Engineering : analyse métier, modélisation dimensionnelle (star schema), pipeline de données (Airbyte, PostgreSQL, dbt, Kestra, Docker) et restitution décisionnelle (Power BI).

---

## Démarche en 5 étapes

```
1. Comprendre le métier     → ✅ Semaines 1-2
2. Analyser les besoins     → ✅ Semaine 2-3
3. Comprendre les données   → 🔄 Semaine 3
4. Construire le modèle     → ⏳ Semaines 3-4
5. Construire le dashboard  → ⏳ Semaines 5-7
```

---

## Semaine 1 (15–19 juillet)

**Thème :** Prise en main de Power BI — modèle simplifié ventes

**Réalisations :** Mini dashboard fonctionnel, compréhension du star schema, correction des cardinalités many-to-many.

**Apprentissages clés :**
- La granularité conditionne tout le modèle
- Une dim_calendrier est obligatoire pour les fonctions Time Intelligence
- Sans PK unique dans les dimensions, Power BI génère des relations incorrectes

---

## Semaine 2 (22–26 juillet)

**Thème :** Analyse du domaine métier — conception du modèle ATLAS

**Réalisations :** Livrables L00, L01, L02 du dossier de conception. Star schema ATLAS (11 tables). Dépôt GitHub initialisé.

**Apprentissages clés :**
- La loi MOP structure directement le modèle de données (5 colonnes budgétaires = 5 phases)
- fact_subventions doit être séparée de fact_operations (granularités différentes → double comptage sinon)
- Les bordereaux de prix des MOE sont incomparables → normalisation en 8 catégories standardisées

**Décisions clés :**
- Granularité : 1 ligne = 1 opération × 1 phase
- Montant notifié uniquement pour les subventions (confirmé encadrant)
- Architecture de démarrage : Excel → SharePoint → Power BI

---

## Semaine 3 (29 juillet – 2 août)

**Thème :** Réunion encadrant + réception et analyse des 4 projets pilotes

**Réalisations :**
- Réunion Teams avec Dominique VOLOT (dimanche 3 août)
- Analyse des 4 dossiers de projets réels transmis par l'encadrant
- Restructuration complète du dépôt GitHub (format cabinet de conseil)
- Script Python d'audit qualité des données (30 lignes subventions, 4 projets)

**Découverte importante :**
Les 4 projets contiennent **16 indicateurs de développement durable** par projet (cibles PRO + valeurs constatées). Une nouvelle table `fact_indicateurs_dd` est ajoutée au modèle.

**Chiffres clés des 4 projets :**
- Budget total programme : 8 000 000 € HT
- Prix total marchés : 8 100 000 € HT
- Total subventions notifiées : 1 109 000 € HT
- Reste à charge collectivité estimé : ~7 000 000 € HT

---

## Semaines 4–8 (5 août – 2 septembre)

> 🔄 À compléter au fil du stage

---

## Structure du dépôt GitHub

```
ATLAS/
├── 01_Contexte/          ← Présentation, glossaire, acteurs
├── 02_Analyse_Metier/    ← Cycle de vie, synthèse 4 projets
├── 03_Modelisation/      ← MCD, MLD, star schema, dictionnaires
├── 04_Donnees/           ← Données par projet
├── 05_ETL/               ← Python, SQL, dbt, Kestra
├── 06_Dashboard/         ← Power BI, mockups, KPIs
├── 07_Documentation/     ← Annexes et livrables
└── rapport_stage/        ← Ce document + journal de bord
```

---

*Rapport de stage ATLAS · BAMANIA Nicolas · 2025 — document vivant, mis à jour chaque semaine*
