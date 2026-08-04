# ATLAS
## Analyse Territoriale des Liaisons, Aménagements et Subventions

> **Plateforme décisionnelle de pilotage des investissements territoriaux**

[![Stage](https://img.shields.io/badge/Stage-Data%20Engineering-2E6DB4)](.)
[![Statut](https://img.shields.io/badge/Projet-En%20développement-orange)](.)
[![Architecture](https://img.shields.io/badge/Architecture-Moderne-success)](.)
[![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)](.)
[![dbt](https://img.shields.io/badge/dbt-Transformation-orange)](.)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-DataWarehouse-blue)](.)
[![Docker](https://img.shields.io/badge/Docker-Containerisation-2496ED)](.)
[![Kestra](https://img.shields.io/badge/Kestra-Orchestration-purple)](.)
[![Licence](https://img.shields.io/badge/Licence-MIT-green)](LICENSE)

---

# Vision

Les collectivités territoriales pilotent chaque année plusieurs dizaines de projets d'aménagement :

- voirie,
- réseaux,
- espaces publics,
- eau potable,
- assainissement,
- espaces verts,
- mobilité,
- transition écologique.

Les données relatives à ces opérations sont souvent réparties dans de nombreux fichiers Excel, comptes-rendus, rapports techniques et documents administratifs.

Cette dispersion rend difficile une vision globale de l'investissement public.

**ATLAS** a pour ambition de devenir une plateforme décisionnelle permettant de structurer ces données afin d'aider les décideurs publics à piloter efficacement leurs investissements.

---

# Pourquoi ATLAS ?

Aujourd'hui, répondre à une simple question peut nécessiter plusieurs heures de recherche :

> Combien avons-nous réellement investi depuis le début du mandat ?

ou encore

> Quel est aujourd'hui le reste à charge de la collectivité après subventions ?

ou encore

> Quels projets présentent un risque de dépassement budgétaire ?

ou encore

> Les objectifs environnementaux fixés au lancement des projets sont-ils réellement atteints ?

ATLAS centralise toutes ces informations afin de fournir une vision unique, fiable et actualisée.

---

# Objectif du projet

L'objectif n'est pas simplement de produire un tableau de bord.

L'objectif est de concevoir un véritable **Système d'Information Décisionnel Territorial** capable:

- de structurer les données métier ;
- de conserver leur historique ;
- d'industrialiser les traitements ;
- de produire automatiquement les indicateurs de pilotage ;
- d'accompagner les élus dans leurs décisions.

---

# Les utilisateurs

Le système est destiné principalement :

- A la Direction Générale des Services Techniques (DGST)
- Aux Directeurs de services
- Aux Chefs de projets
- Aux Élus de la collectivité
- Aux Services financiers

---

# Les principales questions auxquelles ATLAS répond

## Pilotage des investissements

- Quel est le budget global engagé ?
- Quel est le coût réel des opérations ?
- Quel est le reste à charge ?
- Quel est le taux de financement externe ?
- Quels sont les projets les plus coûteux ?

---

## Pilotage des projets

- Combien de projets sont en cours ?
- Combien sont terminés ?
- Quels projets sont en retard ?
- Quels projets présentent des risques ?
- Quels projets dépassent leur budget ?

---

## Performance des services techniques

- Les études sont-elles réalisées dans les délais ?
- Les entreprises respectent-elles leurs engagements ?
- Les projets sont-ils livrés conformément aux objectifs ?

---

## Développement durable

- Surface perméable créée
- Nombre d'arbres plantés
- Economie d'eau
- Economie d'énergie
- Biodiversité
- Mobilité douce
- Part d'économie locale
- Heures d'insertion sociale

---

# Architecture fonctionnelle

```
                    Sources de données

                        SharePoint
                           │
                           ▼
                     Fichiers Excel
                           │
                           ▼
                     Airbyte (ETL)
                           │
                           ▼
                  PostgreSQL (RAW)
                           │
                           ▼
                  dbt (STAGING)
                           │
                           ▼
                    dbt (GOLD)
                           │
                           ▼
                 Power BI (Dashboard)
                           │
                           ▼
                 Décisions des élus
```

---

# Architecture technique cible

| Couche | Technologie | Rôle |
|----------|-------------|------|
| Sources | Excel / SharePoint | Saisie métier |
| Ingestion | Airbyte | Collecte automatisée |
| Stockage | PostgreSQL | Entrepôt de données |
| Transformation | dbt | Nettoyage et modélisation |
| Orchestration | Kestra | Automatisation des pipelines |
| Conteneurisation | Docker | Reproductibilité |
| Visualisation | Power BI | Reporting décisionnel |

---

# Les projets pilotes

Le développement débute sur quatre opérations réelles d'aménagement urbain.

| Projet | Commune | Budget | Complexité |
|---------|----------|------------|------------|
| Requalification avenue de Verdun | Les Angles | 1,85 M€ | Moyenne |
| Rue des Marronniers | Avignon | 1,70 M€ | Faible |
| Quais de la Sorgue | Entraigues | 2,35 M€ | Élevée |
| Avenue du Grès | Morières | 2,10 M€ | Moyenne |

Ces projets permettront de construire un modèle de données générique capable d'être réutilisé sur l'ensemble des futures opérations de la collectivité.

---

# Stack Data Engineering

```
Excel

↓

SharePoint

↓

Airbyte

↓

PostgreSQL (Raw)

↓

dbt (Staging)

↓

dbt (Gold)

↓

Power BI

↓

Kestra

↓

Décision
```

---

# Structure du dépôt

```
ATLAS/

├── 01_Contexte/
├── 02_Analyse_Metier/
├── 03_Modelisation/
│      ├── MCD
│      ├── MLD
│      ├── Star_Schema
│      └── Data_Dictionary
│
├── 04_Donnees/
│      ├── Projet_01
│      ├── Projet_02
│      ├── Projet_03
│      └── Projet_04
│
├── 05_ETL/
│      ├── Python
│      ├── SQL
│      ├── dbt
│      └── Kestra
│
├── 06_Dashboard/
│
├── 07_Documentation/
│
├── decision_book/
│
├── rapport_stage/
│
└── docs/
```

---

# Decision Book

Le dossier **Decision Book** constitue le cœur fonctionnel du projet.

Il ne décrit pas le code.

Il décrit les décisions que le système doit permettre de prendre.

Chaque indicateur y est documenté :

- définition métier ;
- règle de calcul ;
- source de données ;
- fréquence de mise à jour ;
- seuils d'alerte ;
- décision associée.

Cette documentation fait le lien entre les besoins des élus et l'architecture technique.

---

# Livrables

| Code | Livrable | Statut |
|------|-----------|--------|
| L00 | Vision stratégique | ✅ |
| L01 | Étude du besoin | ✅ |
| L02 | Analyse métier | ✅ |
| L03 | Modèle Conceptuel | 🔄 |
| L04 | Modèle Logique | 🔄 |
| L05 | Architecture cible | 🔄 |
| L06 | Dashboard Power BI | ⏳ |
| L07 | Industrialisation | ⏳ |
| L08 | Guide utilisateur | ⏳ |
| L09 | Retour d'expérience | ⏳ |

---

# Ce projet

Ce dépôt est développé dans le cadre d'un stage de **Data Engineering** réalisé auprès de la **Communauté de Communes du Grand Avignon**.

L'objectif pédagogique est de démontrer une démarche complète de conception d'un système décisionnel :

- compréhension du métier ;
- modélisation des données ;
- conception d'un Data Warehouse ;
- industrialisation des traitements ;
- restitution décisionnelle.

---

# Auteur

**Bamania Nathanaël Nicolas**

Stagiaire Data Engineering

Encadrant :
**Dominique Volot**
Direction Générale des Services Techniques

Période :
15 juillet 2026 → 2 septembre 2026

---

> **ATLAS**
>
> *Transformer les données des projets d'aménagement en décisions éclairées pour les collectivités territoriales.*