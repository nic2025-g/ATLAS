# ATLAS — Plateforme décisionnelle de pilotage des investissements territoriaux

> **A**nalyse **T**erritoriale des **L**iaisons, **A**ménagements et **S**ubventions

[![Statut](https://img.shields.io/badge/Statut-En%20développement-orange)](.)
[![Modélisation](https://img.shields.io/badge/MCD%20%2F%20MLD-Conçus-1A6B3C)](.)
[![Données](https://img.shields.io/badge/Données-17%20fichiers%20Excel-217346)](.)
[![BI](https://img.shields.io/badge/Power%20BI-En%20cours-F2C811)](.)

## Ce projet en une phrase

ATLAS vise à fournir au Directeur des Services Techniques et aux élus une vision consolidée et régulièrement actualisée des opérations d’aménagement : budgets, marchés, subventions, délais, risques et performance environnementale et sociale.

## Contexte

Les informations relatives aux projets d’aménagement sont initialement présentes dans des dossiers métier narratifs et dans différents supports de suivi.

La première mission du projet consiste donc à transformer ces informations non structurées en un socle de données homogène, contrôlé et réutilisable.

ATLAS repose actuellement sur quatre opérations pilotes, structurées dans dix-sept fichiers Excel publiés sur OneDrive / SharePoint et destinés à alimenter Power BI.

Le modèle est conçu pour intégrer progressivement de nouvelles opérations sans remettre en cause sa structure générale.

## D'où je suis parti — où j'en suis

```
Semaine 1  →  Découverte de Power BI — modèle simplifié ventes
                ↓ apprentissage : granularité, star schema, dim_calendrier

Semaine 2  →  Analyse métier — loi MOP, cycle de vie, besoins élus
                ↓ apprentissage : le métier structure le modèle, pas l'inverse

Semaine 3  →  Données réelles — 4 projets pilotes, 16 indicateurs DD
                ↓ apprentissage : les données réelles révèlent ce que le modèle théorique rate

Semaine 4  →  MCD Merise complet → MLD → DDL SQL → 17 fichiers Excel
                ↓ apprentissage : méthode d'abord, outils ensuite

Semaine 5+ →  Power BI dashboard — en cours
```

---

## Le problème résolu

Aujourd'hui, les services techniques suivent leurs projets dans des fichiers Excel manuels. Il n'existe pas de vision consolidée. Les élus ne peuvent pas répondre simplement à :

- *Combien avons-nous investi depuis le début du mandat ?*
- *Quel est le reste à charge après subventions ?*
- *Nos projets sont-ils livrés dans les délais et les budgets annoncés ?*

---

## La solution ATLAS
```
L'architecture opérationnelle actuelle est :

Notes métier des opérations
          │
          ▼
Extraction et structuration manuelles
          │
          ▼
17 fichiers Excel normalisés
          │
          ▼
OneDrive / SharePoint
          │
          ▼
Power Query
          │
          ▼
Modèle analytique Power BI
          │
          ▼
Dashboard élus / DGST


La version industrielle sera une architecture cible :

Excel / SharePoint
        │
        ▼
      Airbyte
        │
        ▼
 PostgreSQL — raw
        │
        ▼
 dbt — staging / marts
        │
        ▼
     Power BI
        ▲
        │
      Kestra
```
---

## État actuel du projet

### Réalisé

```
- Analyse de quatre opérations pilotes ;
- extraction et structuration des informations issues des notes métier ;
- conception du MCD et du MLD ;
- création de 17 fichiers Excel reliés par des identifiants ;
- dépôt des fichiers sur OneDrive / SharePoint ;
- préparation du dictionnaire de données ;
- conception préliminaire du DDL PostgreSQL.
```
### En cours

```
- contrôle de la qualité et de l’intégrité référentielle des fichiers ;
- connexion des fichiers à Power BI ;
- adaptation du modèle conceptuel au modèle analytique Power BI ;
- création des mesures DAX et des premières pages du dashboard.
```

### Perspective d’industrialisation

```
- ingestion avec Airbyte ;
- stockage dans PostgreSQL ;
- transformations avec dbt ;
- orchestration avec Kestra ;
- conteneurisation avec Docker.
```
---
## Le modèle de données — 17 tables en 5 couches

```
Couche 1 — Référentiels stables   (6)
    COMMUNE · ACTEUR · ENTREPRISE · PHASE · ORGANISME · TYPE_TRAVAUX

Couche 2 — Référentiels catalogues(2)
    TYPE_RISQUE · TYPE_INDICATEUR

Couche 3 — Objets métier          (4)
    OPERATION · ESTIMATION_FINANCIERE · MARCHE · LOT

Couche 4 — Associations N:N       (2)
    INTERVENIR_SUR · PARTICIPER_AU_LOT

Couche 5 — Faits métier           (3)
    SUBVENTION · RISQUE · INDICATEUR_DD
```

**3 décisions de modélisation importantes :**

`type_acteur` n'est pas dans `ACTEUR` — le rôle MOA/MOE est dans l'association `INTERVENIR_SUR`. Artelia est une organisation — son rôle dépend de sa relation avec le projet.

`ESTIMATION_FINANCIERE` est une entité séparée — pas 5 colonnes dans `OPERATION`. Chaque estimation est une ligne avec sa date. L'historique est conservé de l'AVP au coût final.

`MARCHE` est une entité à part entière — acte juridique distinct de l'opération, avec sa propre cardinalité (1 opération → N marchés possibles).

---

## Les 4 projets pilotes

| # | Commune | Budget programme | Prix marché | Subventions | Reste à charge |
|---|---------|-----------------|-------------|-------------|----------------|
| 1 | Les Angles | 1 850 000 € | 1 950 000 € | 303 000 € | 1 647 000 € |
| 2 | Avignon (Monclar) | 1 700 000 € | 1 790 000 € | 210 000 € | 1 580 000 € |
| 3 | Entraigues-sur-la-Sorgue | 2 350 000 € | 2 180 000 € | 293 000 € | 1 887 000 € |
| 4 | Morières-lès-Avignon | 2 100 000 € | 2 180 000 € | 303 000 € | 1 877 000 € |
| **Total** | | **8 000 000 €** | **8 100 000 €** | **1 109 000 €** | **6 991 000 €** |

---

## Structure du dépôt

```
ATLAS/
├── README.md                       ← Ce fichier — point d'entrée
│
├── 01_Contexte/                    ← Présentation, acteurs, glossaire
│   ├── README.md
│   └── glossaire.md                ← 25 termes métier définis
│
├── 02_Analyse_Metier/              ← Cycle de vie, besoins, processus
│   ├── README.md                   ← Cycle générique AVP→AOR
│   └── synthese_4_projets.md       ← Comparatif des 4 projets pilotes
│
├── 03_Modelisation/                ← MCD, MLD, SQL, dictionnaire
│   ├── MCD/mcd.md                  ← Modèle Conceptuel Merise validé
│   ├── MLD/mld.md                  ← Modèle Logique — 17 tables
│   ├── Star_Schema/                ← (Power BI — à venir)
│   └── Dictionnaires/
│       └── dictionnaire_donnees.md ← Chaque colonne documentée
│
├── 04_Donnees/                     ← Données brutes par projet
│   ├── Projet1_Les_Angles/notes_brutes/
│   ├── Projet2_Avignon/notes_brutes/
│   ├── Projet3_Entraigues/notes_brutes/
│   └── Projet4_Morieres/notes_brutes/
│
├── 05_ETL/                         ← Pipeline de données
│   ├── Python/structuration_donnees.py   ← Audit qualité des données
│   └── SQL/star_schema.sql               ← DDL PostgreSQL complet (Le projet est documenté sous la forme d’un dossier de conception comprenant l’analyse du besoin, le modèle de données, les règles de gestion, les spécifications du dashboard et les perspectives d’industrialisation.)
│
├── 06_Dashboard/                   ← Power BI (à venir)
│
├── 07_Documentation/               ← Annexes et livrables Word
│
└── rapport_stage/
    └── rapport_stage.md            ← Rapport vivant — mis à jour chaque semaine
```

---

## Stack technique

| Couche | Phase 1 (en cours) | Phase 2 (conçue) |
|--------|-------------------|-----------------|
| Sources | 17 fichiers Excel | Excel / SharePoint |
| Ingestion | — | Airbyte |
| Stockage | — | PostgreSQL (DDL prêt) |
| Transformation | — | dbt |
| Orchestration | — | Kestra |
| Restitution | Power BI | Power BI |

---

## Démarche suivie:

1. **Acculturation BI**  
   Étude d’un cas simplifié afin de maîtriser la granularité, les relations et le schéma en étoile.

2. **Analyse métier**  
   Compréhension du cycle de vie des opérations, des besoins du DGST et des attentes des élus.

3. **Analyse des cas pilotes**  
   Extraction des informations présentes dans quatre dossiers d’aménagement.

4. **Conception des données**  
   Élaboration du MCD, du MLD, du dictionnaire et des règles de gestion.

5. **Construction du socle Excel**  
   Création de 17 fichiers normalisés et publication sur OneDrive / SharePoint.

6. **Restitution décisionnelle**  
   Construction en cours du modèle Power BI, des KPI et des pages utilisateurs.

7. **Projection industrielle**  
   Conception d’une architecture cible PostgreSQL, dbt, Airbyte, Kestra et Docker.

---

## Périmètre et limites actuelles

La première version d’ATLAS constitue un prototype décisionnel construit à partir de quatre opérations pilotes.

À ce stade :

- les informations sont extraites manuellement depuis des notes métier ;
- les fichiers Excel constituent le système de collecte et de stockage ;
- certaines données de clôture sont absentes, notamment les coûts définitifs et les dates réelles de réception ;
- les indicateurs sont calculés sur un échantillon limité ;
- l’architecture PostgreSQL, dbt et Kestra est conçue comme une perspective et n’est pas encore déployée.

Le modèle a toutefois été pensé pour accueillir progressivement de nouvelles opérations.

---

## Qualité et gouvernance des données

ATLAS repose sur plusieurs règles de qualité :

- unicité des clés primaires ;
- contrôle des clés étrangères ;
- utilisation de référentiels communs ;
- formats homogènes pour les dates et les montants ;
- absence de cellules fusionnées dans les fichiers sources ;
- listes contrôlées pour les phases, risques, organismes et types de travaux ;
- traçabilité des informations manquantes ou à confirmer.

Un script d’audit permet de détecter les doublons, les références orphelines et les valeurs obligatoires absentes.

---

## Prochaines étapes

- [x] Analyser les quatre opérations pilotes
- [x] Définir les entités et les règles métier
- [x] Produire le MCD et le MLD
- [x] Construire les 17 fichiers Excel
- [x] Publier les fichiers sur OneDrive / SharePoint
- [ ] Contrôler l’intégrité des relations
- [ ] Construire le modèle analytique Power BI
- [ ] Créer la dimension calendrier
- [ ] Développer les KPI financiers
- [ ] Développer les KPI de délais et de risques
- [ ] Concevoir les vues Élus, DGST, Projet et Finances
- [ ] Tester le dashboard avec l’encadrant
- [ ] Finaliser le guide utilisateur
- [ ] Formaliser l’architecture industrielle cible
---

## Auteur

**BAMANIA Nicolas** — Stagiaire Data Engineering  
Formation OpenClassrooms · CC Grand Avignon  
Encadrant : **Dominique VOLOT** — Directeur des Services Techniques  
Stage : 15 juillet → 2 septembre 2026
