# ATLAS — Analyse Territoriale des Liaisons, Aménagements et Subventions

> Prototype décisionnel de pilotage d'opérations d'aménagement territorial

**Projet de stage Data Engineering — DDATAS**  
**Périmètre : 4 opérations pilotes**  
**Restitution : Power BI — 3 vues décisionnelles**  
**Pipeline : Python → PostgreSQL → dbt → Power BI**

---

## 1. Présentation

ATLAS est un prototype de plateforme décisionnelle développé dans le cadre d'un stage Data Engineering au sein de **DDATAS**.

Le projet répond à la problématique suivante :

> **Comment transformer des données de suivi de projets territoriaux, initialement dispersées et peu structurées, en un modèle de données fiable et une solution décisionnelle adaptée aux besoins des élus et des services techniques ?**

Le projet s'appuie sur quatre opérations pilotes afin de concevoir et tester une méthode permettant :

- d'extraire les informations présentes dans des documents métier ;
- de structurer les données ;
- de contrôler leur qualité ;
- de centraliser les données dans PostgreSQL ;
- de construire une couche analytique avec dbt ;
- de restituer les indicateurs dans Power BI.

ATLAS est un **prototype**. Il ne vise pas à remplacer les outils métier existants, mais à démontrer comment des informations dispersées peuvent être transformées en données structurées, contrôlées et exploitables pour le pilotage décisionnel.

---

## 2. Architecture

L'architecture mise en œuvre est la suivante :

```text
Documents métier Word
        ↓
Extraction Python
        ↓
Contrôles et validation
        ↓
Fichiers CSV RAW
        ↓
PostgreSQL
   schéma raw
        ↓
dbt
   ├── staging
   └── mart
        ↓
Power Query
        ↓
Power BI
```

Cette architecture sépare :

- l'extraction ;
- la validation ;
- le stockage des données brutes ;
- les transformations ;
- les tests de qualité ;
- la couche analytique ;
- la restitution décisionnelle.

---

## 3. Pipeline Data Engineering

### 3.1 Extraction Python

Les données sources sont contenues dans quatre documents métier Word.

Un traitement Python extrait automatiquement cinq familles de données :

| Données | Lignes extraites |
|---|---:|
| Opérations | 4 |
| Budgets | 16 |
| Lots | 12 |
| Subventions | 24 |
| Indicateurs de développement durable | 64 |

Le traitement Python a d'abord été développé sous forme monolithique, puis refactorisé en modules spécialisés :

```text
05_ETL/Python/
├── main.py
├── utils.py
├── load_raw.py
├── extractors/
│   ├── document.py
│   ├── operations.py
│   ├── budgets.py
│   ├── lots.py
│   ├── subventions.py
│   └── indicateurs_dd.py
├── validators/
│   └── validations.py
└── raw/
```

Cette organisation permet de séparer les responsabilités d'extraction et de validation.

Les informations absentes des documents sources restent volontairement nulles.

---

### 3.2 PostgreSQL

Les fichiers CSV RAW produits par Python sont chargés dans PostgreSQL.

PostgreSQL est exécuté dans **Docker** afin de disposer d'un environnement isolé et reproductible.

Les données brutes sont centralisées dans le schéma :

```text
raw
```

Le chargement est réalisé par Python en conservant la structure des tables afin de préserver les dépendances des traitements situés en aval.

---

### 3.3 Transformations avec dbt

dbt transforme les données PostgreSQL selon trois niveaux :

```text
raw
 ↓
staging
 ↓
mart
```

La couche `staging` prépare et homogénéise les données.

La couche `mart` contient cinq tables analytiques :

```text
dim_operations
fact_budgets
fact_lots
fact_subventions
fact_indicateurs_dd
```

L'exécution finale comprend :

- **5 vues de staging** ;
- **5 tables de mart** ;
- **10 modèles dbt au total**.

---

### 3.4 Qualité des données

Des tests dbt contrôlent la qualité technique et certaines règles métier.

Résultat de la validation finale :

```text
PASS = 14
WARN = 0
ERROR = 0
SKIP = 0
```

**14 tests sur 14 ont été exécutés avec succès.**

Un contrôle métier vérifie notamment la cohérence entre le montant total des lots et le montant du marché correspondant.

La qualité est ainsi contrôlée à plusieurs niveaux :

```text
Documents métier
        ↓
Validation Python
        ↓
PostgreSQL
        ↓
Tests dbt
        ↓
Power BI
        ↓
Contrôle des mesures et de la restitution
```

---

## 4. Modélisation : de la V1 à la V2

### V1 — Modèle détaillé

Une première modélisation relationnelle a été construite afin de formaliser le domaine métier.

Elle comprend notamment :

- opérations ;
- communes ;
- acteurs ;
- entreprises ;
- marchés ;
- lots ;
- estimations financières ;
- subventions ;
- risques ;
- indicateurs de développement durable ;
- tables d'association.

Cette étape a permis de travailler sur :

- les granularités ;
- les cardinalités ;
- les règles de gestion ;
- le MCD ;
- le MLD ;
- le dictionnaire de données.

### V2 — Modèle décisionnel simplifié

La confrontation de la V1 aux besoins opérationnels a conduit à une V2 plus simple.

Le modèle V2 repose principalement sur cinq tables :

```text
V2_Operations
V2_Budgets
V2_Lots
V2_Subventions
V2_Indicateurs_DD
```

Cette évolution illustre un principe important du projet :

> **Un modèle techniquement correct doit également être compréhensible, alimentable, maintenable et adapté aux usages réels.**

---

## 5. Dashboard Power BI

Le prototype Power BI V2 comprend trois vues décisionnelles.

### 01 — Synthèse Élus

Vue synthétique du portefeuille permettant notamment de suivre :

- le nombre d'opérations ;
- leur statut ;
- le budget de référence ;
- les subventions ;
- leur localisation ;
- les principaux indicateurs de développement durable.

### 02 — Pilotage DGST

Vue destinée au pilotage financier permettant notamment d'analyser :

```text
FAISA → AVP → PRO → Marché
```

ainsi que :

- l'évolution des estimations ;
- les marchés ;
- les subventions ;
- le reste à charge ;
- les montants par lot.

### 03 — Fiche Opération

Vue détaillée filtrée sur une opération :

- identité et commune ;
- maîtrise d'œuvre ;
- statut ;
- localisation ;
- trajectoire financière ;
- lots ;
- entreprises mandataires ;
- cotraitants ;
- indicateurs de développement durable.

---

## 6. Raccordement PostgreSQL → Power BI

Les cinq tables du schéma `mart` ont été connectées à Power BI via PostgreSQL.

Leur structure et leur contenu ont été vérifiés dans Power Query.

Le dashboard V2, son modèle relationnel et ses mesures DAX avaient été construits précédemment pendant la phase de prototypage.

Le travail restant consiste à **finaliser le raccordement du modèle sémantique Power BI V2 existant aux nouvelles tables `mart`**.

Il faut donc distinguer :

- **dashboard Power BI V2 : réalisé et validé** ;
- **pipeline Python → PostgreSQL → dbt : réalisé et testé** ;
- **connexion des marts dans Power Query : validée** ;
- **raccordement définitif du modèle sémantique V2 aux marts : à finaliser**.

---

## 7. Données manquantes et données de démonstration

Certaines informations ne sont pas disponibles dans les documents sources, notamment :

- certaines dates réelles de fin ;
- les montants effectivement payés aux entreprises ;
- certaines données de clôture des opérations.

Ces informations ne sont pas inventées : elles restent nulles lorsqu'aucune source ne permet de les renseigner.

Des montants payés simulés ont été créés séparément afin de tester certaines fonctionnalités du prototype.

Ils sont explicitement identifiés comme **données de démonstration** et ne doivent pas être interprétés comme des données financières réelles.

---

## 8. Technologies utilisées

| Domaine | Technologies |
|---|---|
| Extraction | Python |
| Manipulation des données | Python / pandas |
| Sources | Documents Word |
| Format intermédiaire | CSV |
| Base de données | PostgreSQL |
| Conteneurisation | Docker |
| Transformation | dbt |
| Tests de données | Python / dbt |
| Business Intelligence | Power BI |
| Préparation BI | Power Query |
| Mesures | DAX |
| Versionnement | Git / GitHub |

### Technologies étudiées

**Airbyte** a été expérimenté comme solution d'ingestion.

Dans le contexte local du prototype, l'ingestion Python a finalement été retenue afin de disposer d'une solution plus légère et directement maîtrisable.

**Kestra** constitue une perspective pour l'orchestration automatique du pipeline.

---

## 9. Structure du dépôt

```text
ATLAS/
│
├── README.md
│
├── 01_Contexte/
│   ├── README.md
│   └── glossaire.md
│
├── 02_Analyse_Metier/
│   ├── README.md
│   └── synthese_4_projets.md
│
├── 03_Modelisation/
│   ├── MCD/
│   ├── MLD/
│   ├── Dictionnaires/
│   ├── V1/
│   └── V2/
│
├── 04_Donnees/
│   ├── Projet1_Les_Angles/
│   ├── Projet2_Avignon/
│   ├── Projet3_Entraigues/
│   ├── Projet4_Morieres/
│   └── V2_Collecte/
│
├── 05_ETL/
│   ├── Python/
│   │   ├── extractors/
│   │   ├── validators/
│   │   ├── main.py
│   │   ├── load_raw.py
│   │   └── utils.py
│   │
│   └── atlas_dbt/
│       ├── models/
│       ├── seeds/
│       ├── tests/
│       └── dbt_project.yml
│
├── 06_Dashboard/
│   ├── Captures/
│   ├── KPIs/
│   └── Mockups/
│
├── 07_Documentation/
│   ├── Decisions/
│   └── Livrables/
│
├── 08_Modele_PowerBI/
│   ├── Dashboard.md
│   ├── Mesures_DAX.md
│   ├── Relations.md
│   └── Tests.md
│
└── rapport_stage/
    └── rapport_stage.md
```

---

## 10. État du projet

| Composant | État |
|---|---|
| Analyse métier | ✅ Réalisée |
| Analyse des 4 opérations pilotes | ✅ Réalisée |
| MCD / MLD V1 | ✅ Réalisés |
| Dictionnaire de données | ✅ Réalisé |
| Modèle simplifié V2 | ✅ Réalisé |
| Dashboard Power BI V2 | ✅ Réalisé |
| 3 vues décisionnelles | ✅ Réalisées |
| Extraction Python | ✅ Réalisée |
| Refactorisation Python modulaire | ✅ Réalisée |
| Génération CSV RAW | ✅ Réalisée |
| PostgreSQL sous Docker | ✅ Réalisé |
| Chargement dans le schéma `raw` | ✅ Réalisé |
| dbt `staging` | ✅ Réalisé |
| dbt `mart` | ✅ Réalisé |
| 5 tables analytiques | ✅ Réalisées |
| Tests dbt | ✅ 14/14 réussis |
| PostgreSQL → Power Query | ✅ Validé |
| Vérification des 5 marts | ✅ Réalisée |
| Raccordement sémantique Power BI V2 → marts | 🔄 À finaliser |
| Orchestration automatique | 🔭 Perspective |

---

## 11. Perspectives

Les principales évolutions possibles sont :

1. finaliser le raccordement du modèle Power BI V2 aux tables `mart` ;
2. intégrer davantage d'opérations ;
3. intégrer des opérations terminées pour disposer de données réelles de clôture ;
4. standardiser davantage les données sources ;
5. orchestrer automatiquement le pipeline ;
6. mettre en place journalisation, supervision et alertes ;
7. renforcer la gestion des secrets et la traçabilité des traitements.

Une évolution possible de l'architecture serait :

```text
Documents métier
        ↓
Extraction Python
        ↓
PostgreSQL
        ↓
dbt
        ↓
Power BI

Kestra → orchestration
```

---

## 12. Principaux enseignements

ATLAS m'a permis de travailler sur plusieurs dimensions du métier de Data Engineer :

- compréhension du besoin métier ;
- analyse de données semi-structurées ;
- modélisation MCD / MLD ;
- définition des granularités ;
- Python ;
- PostgreSQL ;
- SQL ;
- Docker ;
- dbt ;
- tests de qualité ;
- Power Query ;
- modélisation Power BI ;
- DAX ;
- conception de tableaux de bord ;
- Git et GitHub ;
- documentation technique.

Le principal enseignement du projet est que la qualité d'un dashboard ne dépend pas uniquement de ses visualisations.

Elle dépend de toute la chaîne qui précède la restitution :

> **comprendre la donnée, la structurer, la contrôler, la transformer et seulement ensuite la présenter.**

---

## 13. Auteur

**BAMANIA Nathanaël Nicolas**  
Stagiaire Data Engineering  
Formation **OpenClassrooms**

**Entreprise d'accueil : DDATAS**  
**Encadrant : Dominique VOLOT — Gérant**

Stage : **15 juillet 2026 → 2 septembre 2026**