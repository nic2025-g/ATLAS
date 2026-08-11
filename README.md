# ATLAS — Plateforme décisionnelle de pilotage des investissements territoriaux

> **A**nalyse **T**erritoriale des **L**iaisons, **A**ménagements et **S**ubventions

[![Statut](https://img.shields.io/badge/Statut-En%20développement-orange)](.)
[![Modélisation](https://img.shields.io/badge/MCD%20%2F%20MLD-Conçus-1A6B3C)](.)
[![Données](https://img.shields.io/badge/Données-17%20fichiers%20Excel-217346)](.)
[![BI](https://img.shields.io/badge/Power%20BI-Modèle%20relationnel%20construit-F2C811)](.)

---

## Ce projet en une phrase

Concevoir une plateforme décisionnelle qui permet aux élus et au Directeur des Services Techniques de la Communauté de Communes du Grand Avignon de piloter leurs investissements territoriaux en temps réel — sans consolidations manuelles.

---

## D'où je suis parti — où j'en suis (Progression)

```
Semaine 1  →  Découverte de Power BI — modèle simplifié ventes
                ↓ apprentissage : granularité, star schema, dim_calendrier

Semaine 2  →  Analyse métier — loi MOP, cycle de vie, besoins élus
                ↓ apprentissage : le métier structure le modèle, pas l'inverse

Semaine 3  →  Données réelles — 4 projets pilotes, 16 indicateurs DD
                ↓ apprentissage : les données réelles révèlent ce que le modèle théorique rate

Semaine 4  →  MCD Merise complet → MLD → DDL SQL → 17 fichiers Excel
                ↓ apprentissage : méthode d'abord, outils ensuite

Étape actuelle → Mesures DAX et validation des KPI
                 Passer du modèle de données à l'information décisionnelle

Étape suivante → Dashboard
                 Construire des vues adaptées aux élus et au DGST
```

---

## Le problème résolu

Aujourd'hui, les services techniques suivent leurs projets dans des fichiers Excel manuels. Il n'existe pas de vision consolidée. Les élus ne peuvent pas répondre simplement à :

- *Combien avons-nous investi depuis le début du mandat ?*
- *Quel est le reste à charge après subventions ?*
- *Nos projets sont-ils livrés dans les délais et les budgets annoncés ?*

---

## La solution ATLAS

L'objectif opérationnel est de disposer d'une chaîne simple et maîtrisée :

```text
Notes et dossiers métier
        │
        ▼
Analyse et extraction des informations
        │
        ▼
17 fichiers Excel structurés
        │
        ▼
OneDrive / SharePoint
        │
        ▼
Power Query
        │
        ▼
Modèle relationnel Power BI
        │
        ▼
Mesures DAX / KPI
        │
        ▼
Dashboard de pilotage
```

Cette architecture constitue le **périmètre opérationnel du prototype**. Une architecture plus industrialisée est étudiée séparément comme perspective d'évolution ; elle ne doit pas masquer l'objectif prioritaire du stage : valider les données, le modèle et les usages décisionnels.

---

## Le modèle de données — 17 tables en 5 couches

Les 17 fichiers ont été organisés en cinq familles. Cette organisation matérialise le passage des notes métier vers un modèle exploitable dans Power BI.

| Couche | Fichiers | Rôle |
|---|---|---|
| **1 — Référentiels stables** | `Communes`, `Acteurs`, `Entreprises`, `Phase`, `Organismes`, `Type_Travaux` | Décrire les objets de référence partagés |
| **2 — Catalogues** | `Types_Risques`, `Type_Indicateur` | Normaliser les catégories utilisées dans les faits |
| **3 — Objets métier** | `Operations`, `Estimation_Financiere`, `Marche`, `Lots` | Décrire le cœur d'une opération et son évolution financière/contractuelle |
| **4 — Associations** | `Intervenir_Sur`, `Participer_Au_Lot` | Gérer les relations plusieurs-à-plusieurs entre opérations, acteurs, lots et entreprises |
| **5 — Faits métier** | `Subventions`, `Risques`, `Indicateurs_DD` | Porter les événements et mesures analysés dans Power BI |

### Pourquoi 17 fichiers ?

Le découpage ne cherche pas à multiplier artificiellement les sources. Il répond à plusieurs besoins :

- éviter de répéter les mêmes informations dans plusieurs lignes ;
- conserver des référentiels communs ;
- représenter correctement les relations métier ;
- permettre l'ajout de nouvelles opérations sans modifier la structure générale ;
- préparer un modèle Power BI dans lequel les filtres et les agrégations restent maîtrisables.

---

## Décisions de modélisation

### Rôle des acteurs porté par l'association

`ACTEUR` décrit une organisation. Son rôle dans une opération (MOA, MOE, etc.) est porté par `INTERVENIR_SUR`, afin de ne pas figer un rôle qui dépend du contexte de l'opération.

### Historisation des estimations financières

`ESTIMATION_FINANCIERE` est séparée de `OPERATION`. Une estimation devient une observation datée et typée (`budget_programme`, `budget_avp`, `budget_pro`, `prix_marche`, `montant_engage`, `cout_final`) plutôt qu'une succession de colonnes figées dans l'opération.

### Marché distinct de l'opération

`MARCHE` est modélisé comme un objet métier autonome. Une opération peut ainsi être reliée à un ou plusieurs marchés sans confondre le projet d'aménagement avec l'acte contractuel.

### Associations plusieurs-à-plusieurs explicites

`INTERVENIR_SUR` et `PARTICIPER_AU_LOT` permettent de représenter les relations métier N:N sans recourir directement à des relations plusieurs-à-plusieurs ambiguës dans Power BI.

---

## De la source au modèle Power BI

Le travail réalisé peut être résumé en quatre transformations successives :

### 1. Informations métier non structurées

Les quatre dossiers pilotes ont d'abord été considérés comme des **prises de notes métier** et non comme des tables directement exploitables.

### 2. Identification des entités et règles de gestion

L'analyse a permis d'identifier les opérations, communes, acteurs, marchés, lots, estimations financières, subventions, risques, indicateurs et leurs relations.

### 3. Construction du socle Excel

Ces informations ont été réparties dans 17 fichiers reliés par des identifiants (`operation_id`, `commune_id`, `marche_id`, etc.).

### 4. Construction du modèle Power BI

Les fichiers ont été importés dans Power BI et les relations ont été créées. Une table dédiée `_Mesures_ATLAS` centralise désormais les mesures DAX, classées par domaine fonctionnel.

---

## Premiers axes de pilotage

Les mesures DAX sont organisées dans `_Mesures_ATLAS` par domaine :

```text
01_Validation
02_Investissements
03_Subventions
04_Délais
05_Risques
06_Développement_Durable
07_Performance
08_Alertes        (à consolider)
```

Les KPI définitifs ne sont pas considérés comme figés à ce stade. Ils doivent être validés à partir des questions réellement posées par le DGST et les élus.

Les premiers axes étudiés sont :

- **investissements** : budgets, marchés, engagements, évolution des estimations ;
- **financement** : subventions notifiées, taux de financement externe, reste à charge ;
- **délais** : opérations/lots en retard, respect des échéances ;
- **risques** : risques avérés, criticité, opérations nécessitant une attention ;
- **performance** : respect des budgets et délais ;
- **développement durable** : comparaison entre objectifs et valeurs constatées.

---

## État d'avancement au 10 août 2026

| Étape | État | Résultat |
|---|---:|---|
| Compréhension du cas simplifié Ventes / Clients / Produits | ✅ | Granularité, cardinalités et principes de modélisation étudiés |
| Analyse métier des opérations d'aménagement | ✅ | Cycle de vie, acteurs et principaux besoins identifiés |
| Analyse des 4 opérations pilotes | ✅ | Informations métier extraites et comparées |
| MCD / MLD | ✅ | Modèles conçus |
| Dictionnaire de données | ✅ | Structure et signification des champs documentées |
| Construction des 17 fichiers Excel | ✅ | Socle de données constitué |
| Publication OneDrive / SharePoint | ✅ | Sources accessibles à Power BI |
| Import Power BI | ✅ | 17 tables chargées |
| Relations Power BI | ✅ | Modèle relationnel construit |
| Table de mesures DAX | ✅ | `_Mesures_ATLAS` créée et organisée par dossiers |
| Mesures de validation | ✅ | Comptages de contrôle créés |
| KPI financiers, subventions, risques, délais, DD | 🚧 | Premières mesures et alertes en cours de validation |
| Pages décisionnelles Élus / DGST / Projet / Finances | ⏳ | À construire après validation des KPI |
| Tests métier avec l'encadrant | ⏳ | À réaliser progressivement |

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
│   └── SQL/star_schema.sql               ← DDL PostgreSQL complet (571 lignes)
│
├── 06_Dashboard/                   ← Power BI (à venir)
│   ├── KPIs/
│   ├── Mockups/
│   └── Captures/
│
├── 07_Documentation/               ← Annexes et livrables Word
│
├── 08_Modele_PowerBI/
│   └── documentation du modèle relationnel, relations et mesures
│
└── rapport_stage/
    └── rapport_stage.md            ← Rapport vivant — mis à jour chaque semaine
```
---

## Architecture cible — perspective, pas prérequis du prototype

Une généralisation à davantage d'opérations et à plusieurs années pourrait conduire à une architecture plus industrialisée :

```text
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

Kestra : orchestration du pipeline
Docker : environnement technique reproductible
```

Cette architecture est actuellement une **proposition de conception**. Sa mise en œuvre n'est pas nécessaire pour valider le prototype Excel / SharePoint / Power BI.

---

## Logique defini pour les étapes àsuivre

- [x] Comprendre le cas simplifié et les principes de modélisation Power BI
- [x] Analyser les quatre opérations pilotes
- [x] Identifier les entités et principales règles métier
- [x] Produire le MCD et le MLD
- [x] Construire le dictionnaire de données
- [x] Constituer les 17 fichiers Excel
- [x] Publier les fichiers sur OneDrive / SharePoint
- [x] Importer les 17 tables dans Power BI
- [x] Construire les relations du modèle Power BI
- [x] Créer `_Mesures_ATLAS` et les mesures de validation
- [ ] Faire valider avec l'encadrant la structure des 17 fichiers et les règles métier sensibles
- [ ] Créer / intégrer la dimension calendrier adaptée au modèle analytique
- [ ] Finaliser les KPI financiers et de subventions
- [ ] Finaliser les KPI de délais, risques, performance et développement durable
- [ ] Formaliser les règles d'alerte
- [ ] Concevoir la vue de synthèse Élus
- [ ] Concevoir la vue de pilotage DGST
- [ ] Concevoir les vues Projet et Finances
- [ ] Tester les filtres, mesures et agrégations sur chaque opération
- [ ] Tester le dashboard avec l'encadrant
- [ ] Documenter le modèle Power BI et les KPI
- [ ] Finaliser le guide utilisateur
- [ ] Formaliser l'architecture industrielle cible

---

## Périmètre et limites actuelles

ATLAS est actuellement un **prototype construit sur quatre opérations pilotes**.

À ce stade :

- l'extraction initiale depuis les dossiers métier reste manuelle ;
- Excel / OneDrive / SharePoint constitue le socle de données opérationnel ;
- certaines informations de clôture peuvent être absentes ou à confirmer ;
- les KPI sont encore en phase de définition et de validation métier ;
- les résultats ne doivent pas être généralisés à l'ensemble des opérations de la collectivité tant que le modèle n'a pas été testé sur un périmètre plus large ;
- l'architecture PostgreSQL / dbt / Airbyte / Kestra reste une perspective d'industrialisation.

---

## Auteur

**BAMANIA Nathanael Nicolas** — Stagiaire Data Engineering  
Formation OpenClassrooms · CC Grand Avignon  
Encadrant : **Dominique VOLOT** — Directeur des Services Techniques  
Stage : 15 juillet 2026 → 2 septembre 2026
