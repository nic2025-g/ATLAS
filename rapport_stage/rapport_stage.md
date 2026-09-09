# Rapport de stage — ATLAS

## Conception d’une plateforme décisionnelle de pilotage des investissements territoriaux

**Auteur :** BAMANIA Nathanaël Nicolas  
**Formation :** Data Engineering — OpenClassrooms  
**Structure d’accueil :** DDATAS  
**Encadrant :** Dominique VOLOT — Gérant    
**Période :** 15 juillet 2026 → 2 septembre 2026  

---

## 1. Introduction

Ce stage porte sur la conception d’une plateforme décisionnelle de pilotage des investissements territoriaux, baptisée **ATLAS — Analyse Territoriale des Liaisons, Aménagements et Subventions**.

L’objectif initial était de construire un tableau de bord Power BI permettant au Directeur des Services Techniques et aux élus de disposer d’une vision synthétique des opérations d’aménagement suivies par la collectivité.

L’analyse du besoin a cependant rapidement montré que la difficulté principale ne résidait pas dans la création des visualisations.

Les informations utiles au pilotage étaient présentes dans différents dossiers et notes métier et ne constituaient pas directement un jeu de données structuré et exploitable. Avant de construire le dashboard, il fallait donc comprendre le fonctionnement d’une opération d’aménagement, identifier les informations pertinentes, déterminer leur niveau de granularité, définir leurs relations et construire un modèle de données cohérent.

Le stage s’est ainsi progressivement transformé en un travail couvrant plusieurs dimensions d’un projet Data Engineering :

- compréhension du besoin métier ;
- analyse et structuration de données ;
- modélisation conceptuelle et logique ;
- préparation et contrôle des données ;
- construction d’un modèle analytique Power BI ;
- développement de mesures DAX ;
- conception de tableaux de bord décisionnels ;
- validation et adaptation du modèle à partir des retours des utilisateurs métier.

Une première modélisation détaillée a été construite afin de représenter les différents objets du domaine. La confrontation de cette modélisation aux besoins opérationnels a ensuite conduit à une seconde version plus simple et mieux adaptée au prototype attendu.

Cette évolution entre une **V1 détaillée** et une **V2 opérationnelle** constitue l’un des principaux enseignements du stage : la qualité d’un modèle ne dépend pas uniquement de sa rigueur technique, mais également de sa capacité à être compris, alimenté, maintenu et utilisé par les acteurs métier.

---


## 2. Problématique

Les services techniques réalisent et suivent plusieurs opérations d’aménagement pour le compte de la collectivité.

Ces opérations génèrent des informations de différentes natures :

- caractéristiques générales des opérations ;
- budgets prévisionnels ;
- évolution des estimations selon les phases du projet ;
- marchés et lots ;
- entreprises intervenantes ;
- subventions ;
- localisation des travaux ;
- indicateurs environnementaux et sociaux ;
- informations de calendrier et d’avancement lorsqu’elles sont disponibles.

Au début du stage, plusieurs questions de pilotage ont été envisagées :

- combien la collectivité investit-elle ?
- comment les estimations évoluent-elles entre les différentes phases d’un projet ?
- quels sont les montants des marchés ?
- quelles subventions ont été notifiées et par quels organismes ?
- quel est le reste à charge de la collectivité ?
- certaines opérations présentent-elles un dépassement budgétaire ?
- les opérations respectent-elles leurs échéances ?
- quels risques doivent attirer l’attention du DGST ?
- quels résultats environnementaux et sociaux sont associés aux opérations ?
- comment synthétiser ces informations pour les élus ?

L’étude des données disponibles et les échanges avec l’encadrant ont ensuite permis de distinguer les indicateurs réellement calculables de ceux nécessitant des informations supplémentaires.

Par exemple, la notion de retard ne peut être évaluée de manière fiable pour une opération en cours sans disposer des dates prévisionnelles et réelles nécessaires. De même, certains indicateurs financiers de clôture nécessitent de connaître les montants effectivement payés aux entreprises.

Le choix a donc été fait de ne pas produire artificiellement des indicateurs lorsque les données nécessaires n’étaient pas disponibles.

La problématique du stage peut ainsi être formulée de la manière suivante :

> **Comment transformer des données de suivi de projets territoriaux, initialement dispersées et peu structurées, en un modèle de données fiable et une solution décisionnelle adaptée aux besoins des élus et des services techniques ?**

---

## 3. Objectifs du stage

Le projet ATLAS poursuit quatre objectifs principaux.

### 3.1 Comprendre le métier

Le premier objectif consiste à comprendre le fonctionnement d’une opération d’aménagement et son vocabulaire.

Cette étape comprend notamment l’étude :

- de la maîtrise d’ouvrage et de la maîtrise d’œuvre ;
- du cycle de vie d’une opération ;
- des phases FAISA, AVP, PRO, ACT, DET et AOR ;
- des marchés de travaux ;
- des lots ;
- des entreprises intervenantes ;
- des mécanismes de subvention ;
- des indicateurs de développement durable.

Cette compréhension est indispensable pour éviter de construire un modèle techniquement cohérent mais ne représentant pas correctement le fonctionnement métier.

### 3.2 Structurer les données

Le deuxième objectif consiste à transformer les informations issues des quatre opérations pilotes en données homogènes et exploitables.

Il s’agit notamment :

- d’identifier les informations récurrentes ;
- de définir leur granularité ;
- de créer des identifiants cohérents ;
- d’harmoniser les formats ;
- de gérer explicitement les informations absentes ;
- de préparer des données pouvant être chargées et analysées dans Power BI.

### 3.3 Construire un modèle décisionnel

Le troisième objectif est de construire un modèle permettant d’analyser plusieurs opérations dans une même solution.

Une première modélisation détaillée a permis de formaliser le domaine métier.

Elle a ensuite été simplifiée à la suite des retours métier afin d’obtenir une structure plus adaptée au prototype et à son mode d’alimentation.

L’objectif n’est donc pas uniquement de produire un modèle techniquement normalisé, mais de trouver un compromis entre :

- robustesse ;
- simplicité ;
- maintenabilité ;
- qualité des données ;
- besoins décisionnels.

### 3.4 Restituer l’information

Le quatrième objectif consiste à transformer les données structurées en informations directement exploitables par les décideurs.

Le prototype final distingue trois niveaux de restitution :

-  **synthèse destinée aux élus** ;
-  **vue de pilotage destinée au DGST** ;
-  **fiche détaillée permettant d’analyser une opération particulière**.

Cette organisation permet d'adopter le niveau de détail aux besoins de chaque utilisateur et d’éviter de construire une page unique trop chargée.

---

## 4. Démarche générale

La démarche suivie pendant le stage n’a pas été strictement linéaire.

Elle a comporté plusieurs cycles d’analyse, de modélisation, de test et de remise en question.

Elle peut être résumée ainsi :

```text
Compréhension du métier
        ↓
Analyse des besoins décisionnels
        ↓
Étude des quatre opérations pilotes
        ↓
Identification des objets métier
        ↓
MCD / MLD
        ↓
Modélisation détaillée V1
        ↓
17 tables métier
        ↓
Chargement et premiers tests Power BI
        ↓
Confrontation aux besoins opérationnels
        ↓
Retours métier
        ↓
Simplification et refonte du modèle
        ↓
Modèle V2
        ↓
5 tables métier principales
        ↓
Power Query / Power BI
        ↓
Relations et mesures DAX
        ↓
Tests des filtres et agrégations
        ↓
3 pages décisionnelles
        ↓
Prototype ATLAS final
```

Cette démarche illustre un principe important rencontré pendant le stage :

La modélisation n’est pas une fin en soi. Elle doit évoluer lorsque la confrontation aux données et aux usages montre qu’une autre structure est plus adaptée.
---

### 4.1 Architecture effectivement mise en œuvre

Au cours du stage, l'architecture d'ATLAS a progressivement évolué.

Une première version du prototype reposait sur des données structurées dans des fichiers Excel, chargées dans Power BI à l'aide de Power Query. Cette approche a permis de valider rapidement le modèle métier, les relations entre les données, les mesures DAX et les besoins de restitution.

Dans un second temps, le travail a été prolongé par la mise en place d'une chaîne de traitement davantage orientée Data Engineering.

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

#### Extraction des données avec Python

Les informations relatives aux quatre opérations pilotes étaient initialement contenues dans des documents métier Word.

Un premier script d'extraction a permis de valider la faisabilité du traitement. Le code a ensuite été refactorisé afin de séparer les différentes responsabilités dans plusieurs modules :

lecture des documents ;
extraction des opérations ;
extraction des budgets ;
extraction des lots ;
extraction des subventions ;
extraction des indicateurs de développement durable ;
fonctions utilitaires ;
contrôles de validation.

Cette organisation permet de rendre le traitement plus lisible, maintenable et évolutif.

L'extraction produit cinq jeux de données :

4 opérations ;
16 lignes budgétaires ;
12 lots ;
24 subventions ;
64 indicateurs de développement durable.

Des contrôles sont exécutés avant la génération des fichiers CSV afin de détecter certaines incohérences de structure ou de volumétrie.

#### Centralisation dans PostgreSQL

Les fichiers CSV produits constituent la couche RAW du pipeline.

Un script Python dédié assure leur chargement dans PostgreSQL, dans le schéma raw.

La base est exécutée dans un environnement Docker afin de faciliter la reproductibilité de l'environnement technique.

Cette étape permet de sortir d'une architecture reposant uniquement sur des fichiers et de disposer d'une base centralisée pouvant servir de source aux traitements analytiques.

#### Transformation avec dbt

Les données présentes dans PostgreSQL sont ensuite transformées avec dbt.

Deux niveaux ont été distingués :
```
raw
 ↓
staging
 ↓
mart
```

La couche staging prépare et homogénéise les données issues de la couche brute, notamment les types et certains formats.

La couche mart fournit les tables destinées à l'analyse décisionnelle :

- `dim_operations` ;
- `fact_budgets` ;
- `fact_lots` ;
- `fact_subventions` ;
- `fact_indicateurs_dd`.

Au total, dix modèles dbt sont exécutés : cinq vues de staging et cinq tables de mart.

La qualité du pipeline est également contrôlée par des tests dbt. Lors de la validation finale, les 14 tests exécutés ont été réussis sans erreur.

Un contrôle métier vérifie notamment la cohérence entre les montants des lots et le montant du marché correspondant.

#### Connexion avec Power BI

Les cinq tables du schéma mart ont été connectées à Power BI via le connecteur PostgreSQL et leur contenu a été vérifié dans Power Query.

Le dashboard Power BI V2 avait auparavant été construit et validé à partir du jeu de données structuré utilisé pendant la phase de prototypage. Il comprend le modèle relationnel, les mesures DAX et les trois niveaux de restitution destinés aux élus, au DGST et à l'analyse détaillée d'une opération.

La dernière étape consiste donc à finaliser le raccordement de ce modèle sémantique V2 existant aux nouvelles tables mart.

Cette migration est distincte de la conception du dashboard lui-même : elle vise à remplacer progressivement son alimentation historique par la nouvelle chaîne PostgreSQL/dbt.

### 4.2 Choix d'architecture et perspectives d'industrialisation

Plusieurs outils et architectures ont été étudiés au cours du projet.

Airbyte a notamment été expérimenté comme solution possible d'ingestion. Dans le contexte de l'environnement local disponible et du périmètre du prototype, il n'a toutefois pas été retenu dans la chaîne opérationnelle finale.

L'ingestion vers PostgreSQL est donc assurée par Python.

L'architecture effectivement réalisée peut être résumée ainsi :
```
Documents métier
        ↓
Python
        ↓
CSV RAW
        ↓
PostgreSQL
        ↓
dbt
        ↓
Power BI
```

Cette architecture sépare désormais clairement :
- l'extraction ;
- le stockage des données brutes ;
- les transformations ;
- les contrôles de qualité ;
- la couche analytique ;
- la restitution.

Dans une perspective d'industrialisation, une solution d'orchestration telle que Kestra pourrait être ajoutée afin de déclencher et superviser automatiquement les différentes étapes du pipeline.

L'industrialisation pourrait également inclure une alimentation plus automatisée des données sources, une gestion centralisée des secrets, une supervision des traitements et des mécanismes de reprise en cas d'échec.
---


## 5. Progression du stage

### 5.1 Semaine 1 : Prise en main de Power BI et compréhension de la granularité

#### Situation initiale

Je connaissais plusieurs outils de Data Engineering, mais je n’avais pas encore construit de modèle Power BI sur un cas métier réel.

#### Travail réalisé

Un cas simplifié de ventes m’a permis de travailler sur :

- les tables de faits et de dimensions ;
- les relations entre tables ;
- les cardinalités ;
- la granularité ;
- les premières mesures DAX ;
- le principe d’une dimension calendrier.

#### Enseignement principal

La première question à poser avant de créer un indicateur est :

> **Que représente exactement une ligne de ma table ?**

Cette notion de granularité est devenue essentielle pour la suite du projet.

J’ai également compris que Power BI constitue la couche de restitution : la fiabilité du dashboard dépend avant tout de la qualité du modèle situé en amont.

---

### 5.2 Semaine 2 — Compréhension du métier

#### Situation initiale

Le domaine de l’aménagement territorial m’était encore largement inconnu.

#### Travail réalisé

J’ai étudié les notes et les informations mises à ma disposition afin de comprendre :

- les rôles de la maîtrise d’ouvrage et de la maîtrise d’œuvre ;
- le cycle d’une opération ;
- les phases FAISA, AVP, PRO, ACT, DET et AOR ;
- les marchés de travaux ;
- les lots ;
- les entreprises ;
- les subventions ;
- les indicateurs de développement durable ;
- les attentes du DGST et des élus.

#### Évolution de ma réflexion

Au départ, je raisonnais principalement en termes de données à afficher.

Les échanges avec mon encadrant ont progressivement déplacé la question vers le besoin décisionnel :

> **Que cherchent les élus et le Directeur des Services Techniques à comprendre à partir des données disponibles ?**

Cette question est devenue l’un des fils directeurs du projet.

---

### 5.3 Semaine 3 — Analyse des quatre opérations pilotes

Quatre opérations pilotes ont été étudiées :

- Les Angles ;
- Avignon ;
- Entraigues-sur-la-Sorgue ;
- Morières-lès-Avignon.

Les informations disponibles constituaient davantage une source métier narrative qu’une base de données directement exploitable.

Il a donc fallu identifier les informations récurrentes :

- opération ;
- commune ;
- acteurs ;
- entreprises ;
- phases ;
- estimations financières ;
- marchés ;
- lots ;
- organismes financeurs ;
- subventions ;
- risques ;
- types de travaux ;
- indicateurs de développement durable.

#### Découverte des indicateurs de développement durable

L’analyse des opérations a notamment fait apparaître une famille d’indicateurs environnementaux et sociaux qui n’avait pas été suffisamment prise en compte dans la première réflexion.

Cette découverte a confirmé qu’un modèle théorique doit être confronté aux données réelles avant d’être considéré comme stable.

---

### 5.4 Construction d’une première modélisation — V1

#### Limite de l’approche initiale

Ma première approche consistait à créer progressivement les fichiers Excel en ajoutant les colonnes nécessaires au fur et à mesure de l’analyse des opérations.

Cette méthode permettait d’avancer rapidement, mais présentait un risque : construire la structure à partir des exemples disponibles plutôt qu’à partir d’un modèle métier explicite.

J’ai donc repris le travail selon la démarche suivante :

```text
Métier → MCD → MLD → données structurées → Power BI
```
#### Construction du MCD et du MLD

Une première modélisation détaillée a été réalisée afin de représenter les principaux objets du domaine et leurs relations.

Cette V1 comprenait 17 tables organisées en cinq familles :

- **Référentiels stables** : Communes, Acteurs, Entreprises, Phase, Organismes, Type_Travaux ;
- **Catalogues** : Types_Risques, Type_Indicateur ;
- **Objets métier** : Operations, Estimation_Financiere, Marche, Lots ;
- **Associations** : Intervenir_Sur, Participer_Au_Lot ;
- **Faits métier** : Subventions, Risques, Indicateurs_DD.

Cette première modélisation avait pour objectif de représenter le métier de manière structurée et de limiter les redondances.

#### Principales décisions de modélisation V1

Plusieurs choix ont notamment été effectués :

- séparer les acteurs de leur rôle dans une opération ;
- historiser les estimations financières ;
- représenter le marché comme un objet métier distinct ;
- utiliser des associations explicites pour certaines relations plusieurs-à-plusieurs ;
- créer des référentiels pour normaliser certaines catégories.

#### Apport de cette V1

Même si elle n’a finalement pas été retenue telle quelle pour le prototype final, cette modélisation n’a pas constitué un travail inutile.
Elle a permis :

- de formaliser le vocabulaire métier ;
- d’identifier les relations entre les objets ;
- de réfléchir aux granularités ;
- de détecter les informations manquantes ;
- de construire un premier dictionnaire de données ;
- de disposer d’une base structurée pour les échanges avec l’encadrant.

La V1 a donc constitué une étape d’analyse et de conception nécessaire avant la simplification du modèle.

### 5.5 Passage de la V1 dans Power BI

Les données structurées ont été déposées sur OneDrive / SharePoint puis chargées dans Power BI.

Les relations ont été construites et différentes mesures DAX ont été développées dans une table dédiée : _Mesures_ATLAS

Les premiers travaux ont porté sur plusieurs familles :

- validation du modèle ;
- investissements ;
- subventions ;
- délais ;
- risques ;
- développement durable ;
- performance ;
- alertes.

Cette étape a permis de tester concrètement la modélisation.

Elle a également confirmé une distinction importante :

**Le MCD cherche à représenter le métier ; le modèle analytique doit avant tout permettre une analyse fiable, compréhensible et maintenable.**

La construction des premières mesures et visualisations a ainsi permis de confronter le modèle théorique à son utilisation réelle.

### 5.6 Confrontation du modèle aux besoins métier

À l’approche de la restitution finale, les échanges avec mon encadrant ont conduit à réexaminer le niveau de complexité du modèle et la pertinence des indicateurs envisagés.

Cette étape a constitué un tournant important du projet.

La question n’était plus uniquement :

**Le modèle est-il techniquement correct ?**

mais également :

**Les informations demandées sont-elles réellement disponibles, maintenables et utiles à la décision ?**

Plusieurs constats ont alors été faits.

#### Les risques

Une modélisation des risques avait été prévue dans la V1.

Cependant, la structure nécessaire pour les saisir, les maintenir et les exploiter correctement ajoutait une complexité importante au prototype.

Il a donc été décidé de ne pas intégrer les risques dans le périmètre final du dashboard.

#### Les délais

Les premières réflexions envisageaient des indicateurs de retard sur les opérations et les lots.

Les quatre opérations pilotes étant encore en cours et certaines dates réelles n’étant pas disponibles, un tel indicateur aurait pu donner une interprétation trompeuse.

La notion de retard a donc été écartée du suivi des opérations en cours.

Pour une opération terminée, une analyse de délai pourra ultérieurement être calculée à partir des dates prévues et réelles lorsque ces données seront disponibles.

#### Les données financières

Le besoin métier a conduit à privilégier une lecture simple de l’évolution financière : 
**FAISA → AVP → PRO → Marché**

Pour les opérations terminées, une étape supplémentaire pourrait comparer le montant du marché aux montants réellement payés aux entreprises.

Ces données de paiement n’étant pas disponibles dans les sources pilotes, elles n’ont pas été inventées.

Dans la chaîne Data Engineering développée ultérieurement, les libellés des phases ont été alignés sur ceux effectivement extraits des documents sources. La phase initialement désignée comme FAISA dans le prototype Power BI correspond ainsi à la phase `PROGRAMME` dans les données du pipeline. Cette différence de terminologie devra être harmonisée lors du raccordement définitif du modèle Power BI aux marts PostgreSQL.

#### Les indicateurs de développement durable

Les indicateurs de développement durable ont été conservés, mais leur structure a été simplifiée.

L’objectif était de conserver directement les informations nécessaires à l’analyse sans multiplier les tables de référence lorsque cette normalisation n’apportait pas de bénéfice immédiat au prototype.

### 5.7 Refonte du modèle — V2

À la suite de ces constats, une seconde version du modèle a été construite.

L’objectif n’était plus de représenter de manière exhaustive tous les objets possibles du métier, mais de disposer d’une structure :

- suffisamment robuste pour l’analyse ;
- simple à comprendre ;
- compatible avec une alimentation Excel ;
- adaptée aux données réellement disponibles ;
- directement exploitable dans Power BI.

Le modèle V2 repose principalement sur cinq tables.

**V2_Operations**

Cette table centralise les principales caractéristiques d’une opération :

- référence ;
- commune ;
- intitulé ;
- maîtrise d’œuvre ;
- responsable ;
- statut ;
- dates disponibles ;
- localisation des travaux.

**V2_Budgets**

Cette table permet de suivre la trajectoire financière à travers :

- FAISA ;
- AVP ;
- PRO ;
- montant du marché ;
- coût final lorsque disponible.

**V2_Lots**

Cette table regroupe les informations relatives aux lots :

- numéro et libellé ;
- montant du marché ;
- entreprise mandataire ;
- cotraitants ;
- informations de planning disponibles ;
- montant payé lorsque cette donnée sera disponible.

**V2_Subventions**

C'est la table qui regroupe les subventions par opération, organisme et type de financement.

**V2_Indicateurs_DD**

Cette dernière table regroupe les indicateurs de développement durable, leurs unités, leurs objectifs et leurs valeurs constatées.

#### Un compromis assumé

**La V2 est moins normalisée que la V1.**

Ce choix est volontaire.

Dans le contexte du prototype, la simplicité de saisie, de compréhension et de maintenance a été considérée comme prioritaire par rapport à une normalisation plus poussée.

Cette refonte m’a permis de comprendre qu’en ingénierie des données, la meilleure architecture n’est pas nécessairement la plus complexe.

Elle est celle qui répond correctement au besoin tout en restant adaptée aux contraintes du contexte.

### 5.8 Reconstruction et validation du modèle Power BI V2

Les cinq tables V2 ont été chargées dans Power BI à partir du fichier Excel structuré.

Les relations ont ensuite été reconstruites autour de la table des opérations.

Des tests ont été réalisés afin de vérifier :

- le filtrage d’une opération vers ses budgets ;
- le filtrage vers ses lots ;
- le filtrage vers ses subventions ;
- le filtrage vers ses indicateurs de développement durable ;
- la cohérence des agrégations globales ;
- la cohérence des résultats lors de la sélection d’une opération.

Les mesures DAX nécessaires aux pages finales ont été regroupées dans des dossiers dédiés de _Mesures_ATLAS, notamment :

- 12_Synthese_Elus
- 13_Pilotage_DGST
- 14_Fiche_Operation

Les mesures développées au cours des premières versions ont été conservées dans le fichier Power BI pour assurer la traçabilité du travail, mais seules les mesures pertinentes pour la V2 sont utilisées dans les pages finales.

### 5.9 Construction des trois vues décisionnelles finales

Le prototype final comprend trois pages complémentaires.

#### Une page - Synthèse Élus

Cette page fournit une vision globale et volontairement synthétique.

Elle présente notamment :

- le nombre d’opérations ;
- la proportion d’opérations en cours et terminées ;
- le budget de référence FAISA ;
- le montant des subventions ;
- la localisation des opérations ;
- les principaux indicateurs de développement durable ;
- des filtres par commune et opération.

La page ne comporte volontairement pas de tableau central détaillé afin de conserver une lecture rapide.

#### Une page — Pilotage DGST

Cette page permet une analyse financière plus détaillée du portefeuille.

Elle présente notamment :

- les montants FAISA, AVP, PRO et Marché ;
- l’évolution financière des opérations ;
- le plan de financement ;
- les subventions ;
- le reste à charge ;
- les montants des marchés par lot et par opération.

Cette page permet de passer d’une vision politique synthétique à une vision de pilotage destinée aux services techniques.

#### Une page — Fiche détaillée de l’opération

Cette page repose sur la sélection d’une opération.

Elle rassemble :

- la commune ;
- la maîtrise d’œuvre ;
- le responsable MOE ;
- le statut ;
- la localisation ;
- la trajectoire financière ;
- l’écart entre le montant du marché et le budget FAISA ;
- les lots et leurs entreprises ;
- les cotraitants lorsqu’ils sont renseignés ;
- les indicateurs détaillés de développement durable.

Les interactions entre le filtre d’opération et les différents visuels ont été testées afin de vérifier que l’ensemble de la fiche reste cohérent.

### 5.10 Mise en place du pipeline Data Engineering

Après la validation du modèle V2 et la construction du prototype Power BI, le projet a été prolongé par la mise en place d'une chaîne de traitement permettant de mieux séparer l'extraction, le stockage, la transformation et la restitution des données.

Cette étape avait pour objectif de faire évoluer ATLAS d'un prototype principalement alimenté par des fichiers vers une architecture davantage conforme aux pratiques du Data Engineering.

#### Extraction automatisée des documents métier

Les quatre documents métier utilisés comme sources contiennent des informations semi-structurées : caractéristiques des opérations, budgets, lots, subventions et indicateurs de développement durable.

Un traitement Python a été développé afin d'extraire automatiquement ces informations.

Une première version monolithique du programme a permis de valider les règles d'extraction. Le code a ensuite été refactorisé en plusieurs modules spécialisés afin de séparer les responsabilités et de faciliter sa maintenance.

Les données extraites sont réparties en cinq jeux de données :

- 4 opérations ;
- 16 lignes budgétaires ;
- 12 lots ;
- 24 subventions ;
- 64 indicateurs de développement durable.

Cette étape a également permis d'enrichir certaines informations disponibles dans les sources, notamment la nature des opérations, la maîtrise d'ouvrage et les dates disponibles au niveau des lots.

Les informations non présentes dans les documents sources restent volontairement nulles. C'est notamment le cas de certaines dates réelles de fin et des montants effectivement payés.

#### Chargement dans PostgreSQL

Les résultats de l'extraction sont enregistrés dans des fichiers CSV constituant une couche de données brutes.

Un second traitement Python charge ensuite ces fichiers dans PostgreSQL, dans un schéma `raw`.

Le chargement a été conçu de manière à conserver la structure des tables tout en renouvelant leur contenu, ce qui permet de préserver les dépendances créées par les traitements situés en aval.

PostgreSQL est exécuté dans Docker, ce qui permet de disposer d'un environnement de base de données isolé et reproductible.

#### Transformation avec dbt

dbt est utilisé pour transformer les données brutes en données adaptées à l'analyse.

Deux couches ont été mises en place :

- `staging`, destinée au nettoyage, au typage et à la préparation des données ;
- `mart`, destinée à fournir les tables directement exploitables par la couche décisionnelle.

La couche `mart` contient cinq tables principales :

- `dim_operations` ;
- `fact_budgets` ;
- `fact_lots` ;
- `fact_subventions` ;
- `fact_indicateurs_dd`.

L'exécution finale de dbt comprend dix modèles : cinq vues dans la couche `staging` et cinq tables dans la couche `mart`.

#### Tests et qualité des données

Des tests dbt ont été ajoutés afin de vérifier plusieurs propriétés du modèle et certaines règles métier.

Lors de la validation finale du pipeline, les 14 tests exécutés ont été réussis :

`PASS = 14 — WARN = 0 — ERROR = 0 — SKIP = 0`

Un test spécifique contrôle notamment la cohérence entre le montant total des lots et le montant du marché correspondant.

Cette étape permet de déplacer une partie du contrôle de qualité en amont du dashboard plutôt que de détecter les incohérences uniquement lors de la restitution.

#### Connexion à Power BI

Les cinq tables du schéma `mart` ont finalement été connectées à Power BI à partir de PostgreSQL.

Leur structure et leur contenu ont été vérifiés dans Power Query.

Le modèle Power BI V2 et ses trois pages décisionnelles ayant été construits précédemment, la dernière étape consiste à finaliser le raccordement de ce modèle sémantique aux nouvelles tables issues de PostgreSQL/dbt.

Cette évolution permet de conserver le travail de conception décisionnelle réalisé dans Power BI tout en faisant évoluer progressivement son alimentation vers une architecture Data Engineering plus robuste.

### 5.11 Résultat de la progression

La progression du stage ne peut donc pas être résumée à la seule construction d’un dashboard.

Elle correspond plutôt au chemin suivant :
```text
Données métier dispersées
        ↓
Compréhension métier
        ↓
Modélisation détaillée V1
        ↓
Tests Power BI
        ↓
Retours métier
        ↓
Simplification V2
        ↓
Dashboard décisionnel
        ↓
Extraction Python
        ↓
PostgreSQL — RAW
        ↓
dbt — staging / mart
        ↓
Tests de qualité
        ↓
Connexion des marts à Power BI
```

Le passage de la V1 à la V2 constitue l’un des résultats importants du stage.

Il montre que la conception d’une solution décisionnelle est un processus itératif dans lequel les retours métier, la disponibilité réelle des données et la simplicité d’utilisation peuvent conduire à faire évoluer profondément une première architecture.

La dernière phase du projet a prolongé cette démarche en déplaçant progressivement la préparation et le contrôle des données vers une chaîne Data Engineering dédiée. Le dashboard n'est ainsi plus considéré comme le lieu principal de transformation des données, mais comme la couche de restitution d'un système dont la fiabilité doit être construite en amont.
---

## 6. Du suivi des projets au pilotage décisionnel

L’un des principaux enseignements du stage est qu’un tableau de bord ne doit pas simplement reproduire les données disponibles. Il doit sélectionner, organiser et présenter les informations en fonction des décisions auxquelles elles doivent contribuer.

Le prototype ATLAS distingue ainsi trois niveaux de lecture.

### 6.1 Niveau Élus — vision stratégique

La page `01_Synthese_Elus` privilégie une lecture rapide du portefeuille.

Elle permet notamment de visualiser :

- le nombre d’opérations ;
- la part des opérations en cours et terminées ;
- le budget de référence FAISA ;
- le montant des subventions ;
- la localisation des opérations ;
- plusieurs résultats environnementaux et sociaux.

Cette page est volontairement synthétique.

Elle ne comporte pas de tableau détaillé central et évite les indicateurs qui nécessiteraient une interprétation technique importante.

#### Aperçu de la synthèse destinée aux élus

![Synthèse des opérations territoriales destinée aux élus](.../06_Dashboard/Captures/01_Synthese_Elus.png)

*Figure 1 — Vue de synthèse ATLAS destinée aux élus : situation des opérations, budget FAISA, subventions, localisation et principaux indicateurs de développement durable.*

### 6.2 Niveau DGST — vision de pilotage

La page `02_Pilotage_DGST` apporte un niveau d’analyse supplémentaire.

Elle permet notamment de comparer la trajectoire financière : `FAISA → AVP → PRO → Marché`

et d’analyser :

- l’évolution des estimations ;
- les montants des marchés ;
- le plan de financement ;
- les subventions ;
- le reste à charge ;
- la répartition des montants par lot.

L’objectif est de permettre au Directeur des Services Techniques de comprendre l’évolution financière des opérations et d’identifier les écarts nécessitant une analyse plus détaillée.

#### Aperçu de la vue de pilotage DGST

![Vue de pilotage financier DGST](.../06_Dashboard/Captures/02_Pilotage_DGST.png)

*Figure 2 — Vue de pilotage DGST : évolution financière des opérations entre FAISA, AVP, PRO et Marché, plan de financement et analyse des montants de marché par lot.*


### 6.3 Niveau opération — vision détaillée

La page `03_Fiche_Operation` permet de descendre au niveau d’une opération particulière.

Le choix d’une opération filtre l’ensemble de la page.

La fiche rassemble notamment :

- l’identité de l’opération ;
- la commune ;
- la maîtrise d’œuvre ;
- le responsable MOE ;
- le statut ;
- la localisation des travaux ;
- la trajectoire financière ;
- les lots ;
- les entreprises mandataires ;
- les cotraitants ;
- les indicateurs de développement durable.

Cette organisation permet de passer progressivement d’une vision globale à une explication détaillée.

##### Aperçu d'une fiche opération

![Fiche détaillée d'une opération](.../06_Dashboard/Captures/03_Fiche_Operation.png)

*Figure 3 — Fiche détaillée de l'opération d'Avignon : identité et localisation du projet, trajectoire financière de FAISA au marché, lots et entreprises titulaires, ainsi que les indicateurs de développement durable.*
---

## 7. Qualité et fiabilité des données

La construction d’ATLAS a montré que **la qualité d’un dashboard dépend directement de la qualité des données utilisées.**

Plusieurs règles ont donc guidé la préparation du prototype :

	- unicité des références d’opération ;
	- cohérence des relations entre les tables ;
	- homogénéité des formats ;
	- définition explicite de la granularité ;
	- contrôle des agrégations ;
	- distinction entre valeur nulle, valeur absente et valeur réellement égale à zéro ;
	- conservation des informations absentes lorsqu’aucune source ne permet de les renseigner.



### 7.1 Ne pas inventer les données manquantes

Certaines informations souhaitées pour le pilotage n’étaient pas disponibles dans les sources étudiées.

C’est notamment le cas de certaines dates réelles, de montants effectivement payés aux entreprises, de certains identifiants d’entreprises ou de données permettant de mesurer précisément l’avancement réel de certains lots.

Le choix a été fait de ne pas créer artificiellement ces informations afin de compléter le dashboard.

Cette décision répond à un principe essentiel :

> **Une donnée absente mais identifiée comme telle est préférable à une donnée plausible mais non vérifiée.**

Dans le cas particulier des montants payés par lot, les valeurs réelles n'étant pas disponibles dans les documents sources, le champ correspondant reste nul dans les données extraites.

Un jeu de valeurs simulées a toutefois été créé séparément afin de permettre de tester techniquement les mécanismes d'analyse prévus pour de futures opérations terminées. Ces valeurs sont explicitement identifiées comme simulées et ne doivent pas être interprétées comme des données financières réelles de la collectivité.

Cette séparation permet de tester une fonctionnalité du prototype sans confondre données métier et données de démonstration.

### 7.2 Contrôles lors de l'extraction

La qualité des données est d'abord contrôlée lors de leur extraction depuis les documents métier.

Le programme Python comporte une couche de validation distincte des modules d'extraction. Elle permet notamment de vérifier la structure et les volumes attendus avant la production des fichiers destinés au chargement.

Sur les quatre opérations pilotes, l'extraction validée produit :

- 4 opérations ;
- 16 lignes budgétaires ;
- 12 lots ;
- 24 subventions ;
- 64 indicateurs de développement durable.

La séparation entre extraction et validation facilite également l'évolution du pipeline : une nouvelle règle de contrôle peut être ajoutée sans modifier directement la logique d'extraction des données.

### 7.3 Contrôles avec dbt

Une seconde couche de contrôle est réalisée après le chargement dans PostgreSQL.

dbt permet d'associer les transformations de données à des tests reproductibles. Les contrôles ne reposent donc plus uniquement sur une vérification visuelle dans Power BI.

Lors de la validation finale du pipeline :

`PASS = 14 — WARN = 0 — ERROR = 0 — SKIP = 0`

Les 14 tests dbt ont ainsi été exécutés avec succès.

Parmi ces contrôles figure notamment une règle métier vérifiant la cohérence entre le montant total des lots et le montant du marché correspondant.

Cette approche permet de détecter certaines incohérences avant que les données n'atteignent la couche de restitution.

### 7.4 Validation dans Power BI

La dernière couche de contrôle concerne la restitution décisionnelle.

Les mesures DAX et les relations du modèle V2 ont été testées à plusieurs niveaux.

Les résultats globaux ont été comparés aux résultats obtenus lorsqu'une opération particulière était sélectionnée.

Ces tests ont notamment permis de contrôler :

- les budgets ;
- les montants des marchés ;
- les subventions ;
- le reste à charge ;
- les montants par lot ;
- les indicateurs de développement durable.

Les interactions entre les filtres et les visuels ont également été vérifiées afin d'éviter qu'un indicateur global soit présenté dans une fiche censée représenter une seule opération.

La qualité est ainsi contrôlée à plusieurs niveaux du projet :

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

## 8. Difficultés rencontrées et décisions prises

### 8.1 Comprendre un métier nouveau

La première difficulté n’a pas été technique.

Le domaine de l’aménagement territorial comportait un vocabulaire, des phases, des acteurs et des règles que je ne maîtrisais pas au début du stage.

Avant de modéliser les données, il a donc fallu comprendre suffisamment le métier pour donner un sens aux informations disponibles.

Cette étape m’a montré qu’un Data Engineer ne peut pas toujours se limiter à la structure technique des données : il doit également comprendre ce qu’elles représentent.

### 8.2 Transformer des documents narratifs en données

Les informations reçues ne constituaient pas directement des tables prêtes à être chargées dans un outil BI.

Il a fallu identifier les informations récurrentes, déterminer leur granularité et construire une structure commune aux quatre opérations pilotes.

Ce passage de documents métier vers des données structurées a constitué une partie importante du travail.

### 8.3 Éviter la sur-modélisation

La V1 a permis de représenter le métier de manière détaillée, mais les échanges avec l’encadrant ont montré qu’une partie de cette complexité n’était pas nécessaire pour le prototype final.

La difficulté a alors été d’accepter de simplifier une architecture techniquement cohérente.

Cette décision a conduit à la V2.

Elle constitue pour moi un apprentissage important :

> **Simplifier un modèle après analyse n’est pas revenir en arrière ; c’est parfois améliorer son adéquation au besoin.**

### 8.4 Distinguer données disponibles et indicateurs souhaités

Plusieurs KPI semblaient intéressants en théorie, notamment autour des délais, des risques ou des montants réellement payés.

Cependant, un indicateur ne peut être fiable que si les données nécessaires à son calcul sont elles-mêmes disponibles et fiables.

Le périmètre du dashboard a donc été adapté aux données réellement exploitables.

Lorsque certaines fonctionnalités devaient néanmoins être testées, comme l'analyse des montants payés par lot, les valeurs de démonstration ont été isolées et explicitement identifiées comme simulées afin de ne pas les confondre avec les données métier réelles.

### 8.5 Faire évoluer le prototype vers une chaîne Data Engineering

Une difficulté importante du projet a consisté à faire évoluer progressivement l'architecture sans remettre en cause le travail de modélisation et de restitution déjà réalisé.

La première version opérationnelle reposait principalement sur des fichiers structurés, Power Query et Power BI. Cette solution était suffisante pour valider les besoins métier, le modèle V2, les mesures DAX et les trois vues décisionnelles.

Dans un second temps, l'objectif a été de déplacer davantage la préparation, la transformation et le contrôle des données en amont de Power BI.

Cette évolution a conduit à mettre en place la chaîne suivante :

```text
Documents métier
        ↓
Python
        ↓
CSV RAW
        ↓
PostgreSQL
        ↓
dbt
        ↓
Power BI
```
Cette évolution a nécessité plusieurs choix techniques.

Le code Python d'extraction a notamment été refactorisé en modules spécialisés afin d'éviter de conserver un traitement monolithique difficile à maintenir.

Le chargement dans PostgreSQL a également dû être adapté afin de renouveler les données de la couche raw sans supprimer les tables dont dépendent les vues dbt.

Enfin, les transformations ont été réparties entre une couche staging, destinée à préparer les données, et une couche mart, destinée à l'analyse décisionnelle.

Cette étape m'a permis de comprendre qu'industrialiser un prototype ne consiste pas nécessairement à reconstruire l'ensemble de la solution. Il est possible de conserver une couche de restitution déjà validée tout en faisant évoluer progressivement les composants situés en amont.


### 8.6 Intégrer de nouveaux outils sans complexifier inutilement l'architecture

Plusieurs technologies ont été envisagées ou expérimentées au cours du projet.

Airbyte a été étudié comme solution d'ingestion vers PostgreSQL. Son utilisation a toutefois introduit des contraintes supplémentaires dans l'environnement local du prototype, notamment en matière de ressources et de déploiement.

Le choix final a donc été de conserver une ingestion Python plus légère et directement maîtrisable dans le contexte du stage.

Cette décision ne signifie pas qu'Airbyte serait inadapté à une architecture de production. Elle traduit plutôt la nécessité d'adapter les choix technologiques au volume de données, aux ressources disponibles et au niveau d'industrialisation réellement nécessaire.

De la même manière, une solution d'orchestration telle que Kestra présente un intérêt pour automatiser l'enchaînement des traitements, mais son intégration n'était pas indispensable pour valider le pipeline dans le périmètre du prototype.

Cette expérience m'a appris qu'une architecture Data Engineering ne doit pas être évaluée au nombre d'outils qu'elle contient. Chaque composant doit répondre à un besoin identifié et apporter un bénéfice suffisant par rapport à la complexité qu'il introduit.
---

## 9. Résultats et livrables

À l'issue du stage, le projet ATLAS comprend à la fois des livrables d'analyse métier, de modélisation, de Data Engineering et de Business Intelligence.

| Livrable | État |
|---|---|
| Analyse du besoin | ✅ Réalisée |
| Analyse métier | ✅ Réalisée |
| Analyse des 4 opérations pilotes | ✅ Réalisée |
| Glossaire métier | ✅ Réalisé |
| MCD / MLD V1 | ✅ Réalisés |
| Dictionnaire de données | ✅ Réalisé |
| Modélisation détaillée V1 | ✅ Réalisée |
| Modèle simplifié V2 | ✅ Réalisé |
| Jeu de données pilote V2 | ✅ Structuré |
| Prototype Power BI V2 | ✅ Réalisé |
| Modèle relationnel Power BI V2 | ✅ Réalisé |
| Mesures DAX finales | ✅ Réalisées |
| Tests des relations et filtres Power BI | ✅ Réalisés |
| `01_Synthese_Elus` | ✅ Réalisée |
| `02_Pilotage_DGST` | ✅ Réalisée |
| `03_Fiche_Operation` | ✅ Réalisée |
| Extraction automatisée des documents métier avec Python | ✅ Réalisée |
| Refactorisation modulaire du traitement Python | ✅ Réalisée |
| Génération des fichiers CSV RAW | ✅ Réalisée |
| Environnement PostgreSQL sous Docker | ✅ Réalisé |
| Chargement Python vers PostgreSQL | ✅ Réalisé |
| Schéma PostgreSQL `raw` | ✅ Réalisé |
| Couche dbt `staging` | ✅ Réalisée |
| Couche dbt `mart` | ✅ Réalisée |
| 5 tables analytiques `mart` | ✅ Réalisées |
| Tests dbt | ✅ 14/14 réussis |
| Connexion PostgreSQL → Power Query | ✅ Validée |
| Vérification des 5 marts dans Power Query | ✅ Réalisée |
| Raccordement définitif du modèle Power BI V2 aux marts | 🔄 À finaliser |
| Documentation du projet | ✅ Réalisée |
| Orchestration automatisée du pipeline | 🔭 Perspective |

### 9.1 Résultat du pipeline de données

La chaîne Data Engineering permet de transformer les informations issues des quatre documents métier en cinq ensembles de données analytiques.

Les volumes obtenus lors de la validation finale sont :

| Données | Nombre de lignes |
|---|---:|
| Opérations | 4 |
| Budgets | 16 |
| Lots | 12 |
| Subventions | 24 |
| Indicateurs de développement durable | 64 |

Ces volumes ont été retrouvés à chaque niveau pertinent du pipeline et les cinq tables finales du schéma `mart` ont été générées avec succès.

L'exécution dbt finale a produit cinq vues de staging et cinq tables de mart sans erreur.

Les tests associés ont également été validés :

`PASS = 14 — WARN = 0 — ERROR = 0 — SKIP = 0`

Ces résultats constituent un point de contrôle reproductible permettant de vérifier l'intégrité de la chaîne avant la restitution dans Power BI.

### 9.2 Résultat décisionnel

Le prototype Power BI V2 constitue la couche de restitution du projet.

Il permet de passer d'une vision globale du portefeuille à une analyse détaillée d'une opération à travers trois pages complémentaires :

- une synthèse destinée aux élus ;
- une vue de pilotage destinée au DGST ;
- une fiche détaillée par opération.

Le raccordement des nouvelles tables PostgreSQL/dbt au modèle Power BI V2 constitue la dernière étape de migration de l'architecture. Les cinq marts ont déjà été connectés et contrôlés dans Power Query ; le travail restant concerne principalement leur substitution aux anciennes sources du modèle sémantique existant.

Le projet permet ainsi de distinguer deux résultats complémentaires :

**un prototype décisionnel fonctionnel**, permettant de valider les usages et les indicateurs ;

et **une chaîne Data Engineering opérationnelle jusqu'à la couche analytique**, permettant de préparer une alimentation plus robuste de cette restitution.

---

## 10. Limites du prototype

ATLAS reste un prototype construit et validé à partir de quatre opérations pilotes. La mise en place du pipeline Data Engineering améliore la structuration et la fiabilité des traitements, mais plusieurs limites subsistent avant une éventuelle généralisation.

### 10.1 Taille du jeu de données

Le prototype repose sur quatre opérations :

- Les Angles ;
- Avignon ;
- Entraigues-sur-la-Sorgue ;
- Morières-lès-Avignon.

Ce périmètre a permis de concevoir et de tester le modèle, mais il ne couvre pas nécessairement toutes les situations susceptibles d'être rencontrées sur un portefeuille plus important.

L'intégration de nouvelles opérations sera donc nécessaire pour éprouver davantage la robustesse des règles d'extraction, du modèle de données et des indicateurs.

### 10.2 Opérations actuellement en cours

Les quatre opérations pilotes étudiées sont encore en cours.

Certaines analyses de clôture ne peuvent donc pas être réalisées à partir de données réelles, notamment :

- le délai final d'une opération ;
- l'écart entre durée prévue et durée réelle ;
- le montant total effectivement payé ;
- l'écart final entre le marché signé et les dépenses réelles.

Le modèle prévoit néanmoins la possibilité d'accueillir certaines de ces informations lorsqu'elles seront disponibles.

### 10.3 Données absentes des documents sources

Le pipeline automatise l'extraction des informations présentes dans les documents métier, mais il ne peut pas produire une information qui n'existe pas dans la source.

Certaines valeurs restent donc volontairement nulles, notamment certaines dates réelles et les montants réellement payés aux entreprises.

Lorsque des valeurs simulées sont utilisées pour tester une fonctionnalité analytique, elles sont conservées séparément et explicitement identifiées comme données de démonstration.

Cette distinction évite de transformer une absence de données en information artificiellement présentée comme réelle.

### 10.4 Dépendance à la structure des documents sources

L'extraction Python repose sur la structure actuellement observée dans les documents métier étudiés.

Une modification importante de leur organisation, de leurs tableaux ou de leur terminologie pourrait nécessiter une adaptation des règles d'extraction.

La généralisation d'ATLAS nécessiterait donc de stabiliser davantage le format des données d'entrée ou de définir une procédure formelle de collecte.

### 10.5 Raccordement du modèle Power BI

Le dashboard Power BI V2 a été construit et validé lors de la phase de prototypage.

Parallèlement, les cinq tables analytiques produites par PostgreSQL et dbt ont été connectées et vérifiées dans Power Query.

Le raccordement définitif du modèle sémantique V2 à ces nouvelles tables reste cependant à finaliser.

Le fichier Power BI conserve en effet plusieurs requêtes issues des différentes phases de prototypage, dont certaines dépendent encore d'anciens fichiers locaux.

Cette situation n'affecte pas la validation du pipeline jusqu'aux marts ni le travail de conception du dashboard V2, mais elle montre l'intérêt de séparer plus clairement, dans une version industrialisée, les sources historiques de la couche de restitution finale.

### 10.6 Orchestration et automatisation

Les différentes briques du pipeline ont été mises en œuvre et testées, mais leur exécution n'est pas encore orchestrée automatiquement de bout en bout.

L'extraction Python, le chargement PostgreSQL et les traitements dbt sont aujourd'hui déclenchés séparément.

Une industrialisation nécessiterait notamment :

- l'orchestration des différentes étapes ;
- la gestion des erreurs ;
- la journalisation des exécutions ;
- la supervision du pipeline ;
- la planification des mises à jour ;
- la gestion sécurisée des paramètres et secrets.

Cette limite n'empêche pas la validation de l'architecture, mais constitue une étape importante avant son utilisation dans un contexte de production.

---

## 11. Perspectives d'évolution

Le prototype ATLAS permet désormais de distinguer plusieurs axes d'évolution : extension du périmètre métier, amélioration de la collecte, finalisation de l'intégration BI et industrialisation du pipeline.

### 11.1 Étendre le périmètre des opérations

La première évolution consisterait à intégrer davantage d'opérations.

Cette extension permettrait de vérifier le comportement du pipeline sur des documents plus variés, d'identifier de nouveaux cas métier et de confirmer la capacité du modèle à fonctionner à l'échelle d'un portefeuille plus important.

### 11.2 Formaliser la collecte des données

La fiabilité du pipeline reste directement dépendante de la qualité des informations présentes dans les documents sources.

Une généralisation d'ATLAS nécessiterait donc de définir plus précisément :

- les responsables de chaque donnée ;
- les champs obligatoires ;
- les formats attendus ;
- les fréquences de mise à jour ;
- les règles de contrôle ;
- les procédures de clôture d'une opération.

Une meilleure standardisation des sources réduirait également la complexité de l'extraction.

### 11.3 Intégrer des opérations terminées

L'intégration d'opérations clôturées permettrait de compléter les analyses avec des indicateurs actuellement impossibles à valider sur les quatre opérations pilotes.

Il deviendrait notamment possible d'étudier :

- le respect du délai final ;
- l'écart entre durée prévue et durée réelle ;
- le montant réellement payé par lot ;
- l'écart entre marché signé et dépenses réelles ;
- le coût final d'une opération.

Ces données permettraient d'enrichir les indicateurs de pilotage sans recourir à des valeurs de démonstration.

### 11.4 Finaliser le raccordement Power BI

Une évolution immédiate consiste à finaliser le raccordement du modèle Power BI V2 aux cinq tables analytiques du schéma `mart`.

L'objectif est de conserver les mesures, les relations utiles et les trois vues décisionnelles déjà conçues tout en remplaçant leur alimentation historique par les données préparées dans PostgreSQL et dbt.

Cette étape permettra d'aboutir à une chaîne cohérente de bout en bout :

Documents métier → Python → PostgreSQL → dbt → Power BI.

### 11.5 Orchestrer le pipeline

L'étape suivante d'industrialisation consisterait à automatiser l'enchaînement des traitements.

Une solution d'orchestration telle que Kestra pourrait notamment piloter :

1. l'extraction des documents ;
2. les contrôles Python ;
3. le chargement dans PostgreSQL ;
4. l'exécution des modèles dbt ;
5. les tests de qualité ;
6. le déclenchement ou la préparation de l'actualisation de la couche décisionnelle.

L'intérêt d'une telle orchestration serait également de disposer d'un suivi des exécutions et d'une gestion plus structurée des échecs.

### 11.6 Renforcer la supervision et la traçabilité

Dans une architecture destinée à la production, plusieurs mécanismes supplémentaires pourraient être introduits :

- journalisation centralisée ;
- suivi des exécutions ;
- alertes en cas d'échec ;
- contrôle de fraîcheur des données ;
- historisation de certaines transformations ;
- gestion centralisée des secrets ;
- documentation automatisée du modèle.

L'objectif ne serait plus seulement de produire les données nécessaires au dashboard, mais de garantir dans le temps leur disponibilité, leur qualité et leur traçabilité.

## 12. Compétences mobilisées et acquises

Le stage m'a permis de mobiliser et de développer des compétences à la fois en Data Engineering, en Business Intelligence et dans l'analyse d'un besoin métier.

L'évolution progressive d'ATLAS, depuis l'étude des documents métier jusqu'à la mise en place d'un pipeline de données, m'a également permis de mieux comprendre la complémentarité entre ces différents domaines.

### 12.1 Compétences Data Engineering

Le projet m'a permis de travailler concrètement sur :

- l'analyse de sources de données semi-structurées ;
- la définition des granularités ;
- la conception d'un MCD et d'un MLD ;
- la construction d'un dictionnaire de données ;
- l'extraction de données à partir de documents métier avec Python ;
- la modularisation et la refactorisation d'un traitement Python ;
- la génération et la validation de données RAW ;
- le chargement de données dans PostgreSQL ;
- l'utilisation de PostgreSQL comme couche de stockage centralisée ;
- l'utilisation de Docker pour disposer d'un environnement reproductible ;
- la transformation de données avec dbt ;
- la séparation des traitements en couches `raw`, `staging` et `mart` ;
- la création de modèles analytiques ;
- la mise en place de tests de qualité avec dbt ;
- l'implémentation de contrôles métier reproductibles ;
- la gestion de l'évolution d'un schéma de données sans casser ses dépendances ;
- la réflexion sur l'orchestration et l'industrialisation d'un pipeline.

Cette dernière phase du projet m'a notamment permis de mieux comprendre l'intérêt de séparer les responsabilités dans une architecture de données.

La donnée brute, sa transformation, son contrôle et sa restitution ne doivent pas nécessairement être gérés dans le même outil.

### 12.2 Compétences Business Intelligence

Le projet m'a également permis d'approfondir :

- Power Query ;
- la modélisation Power BI ;
- les relations entre tables ;
- les cardinalités et la propagation des filtres ;
- DAX ;
- la construction de KPI ;
- les interactions entre visuels ;
- la conception de dashboards selon différents profils utilisateurs ;
- les tests des mesures et des agrégations ;
- la connexion de Power BI à PostgreSQL.

La construction des trois pages du prototype m'a également appris à adapter le niveau d'information au profil de l'utilisateur : une synthèse destinée aux élus ne répond pas aux mêmes besoins qu'une vue de pilotage du DGST ou qu'une fiche détaillée d'opération.

### 12.3 Compétences métier et méthodologiques

Le stage m'a appris à :

- découvrir rapidement un domaine métier nouveau ;
- comprendre le vocabulaire de l'aménagement territorial ;
- reformuler un besoin utilisateur ;
- identifier la granularité correcte d'une donnée ;
- questionner la pertinence d'un indicateur ;
- distinguer besoin théorique et donnée réellement disponible ;
- ne pas transformer une donnée absente en donnée supposée ;
- documenter les décisions de conception ;
- accepter de refactoriser une solution lorsque le besoin évolue ;
- distinguer prototype, validation technique et industrialisation ;
- adapter un choix technologique aux contraintes réelles du projet ;
- expliquer des choix techniques à partir de contraintes métier.

### 12.4 Compétences de conception et d'évolution d'une architecture

L'un des principaux apprentissages du stage concerne l'évolution progressive d'une architecture.

ATLAS n'a pas été conçu dès le premier jour sous sa forme finale.

Le projet est passé successivement par plusieurs niveaux :

```text
Compréhension métier
        ↓
Modélisation V1
        ↓
Prototype Power BI
        ↓
Simplification V2
        ↓
Validation décisionnelle
        ↓
Pipeline Python
        ↓
PostgreSQL
        ↓
dbt
        ↓
Raccordement à la couche BI
```
Cette progression m'a appris qu'une architecture de données peut évoluer par étapes.

Un prototype permet d'abord de valider le besoin. Les composants peuvent ensuite être progressivement séparés et renforcés lorsque les usages, les contraintes et les données sont mieux compris.
---
## 13. Bilan final

Ce stage m'a permis de comprendre qu'un projet Data Engineering ne commence pas nécessairement par la mise en place d'une architecture complexe.

Dans ATLAS, le premier travail d'ingénierie a consisté à transformer une connaissance métier dispersée en données structurées, compréhensibles et exploitables.

Ma réflexion a progressivement évolué.

Au départ, je me demandais :

> **« Comment construire un dashboard Power BI ? »**

Puis :

> **« Quelles données faut-il pour construire ce dashboard ? »**

Ensuite :

> **« Comment représenter correctement le métier dans les données ? »**

La confrontation du modèle au besoin métier m'a ensuite conduit à me demander :

> **« Le modèle que j'ai construit est-il réellement adapté aux utilisateurs qui devront l'exploiter ? »**

Le passage de la V1 à la V2 a apporté une première réponse à cette question.

La V1 m'a permis de formaliser le domaine métier et d'appliquer les principes de la modélisation relationnelle.

La V2 m'a appris qu'une solution destinée à être utilisée dans un contexte réel doit également tenir compte de la simplicité d'alimentation, de la disponibilité des données et des besoins prioritaires des utilisateurs.

Une dernière question est alors apparue :

> **« Comment rendre cette alimentation plus fiable, reproductible et indépendante de la couche de restitution ? »**

Cette réflexion a conduit à prolonger le prototype par la construction d'une chaîne Data Engineering :

```text
Documents métier
        ↓
Python
        ↓
PostgreSQL
        ↓
dbt
        ↓
Power BI
```

Python permet d'extraire et de contrôler les informations issues des documents métier.

PostgreSQL fournit une couche de stockage centralisée.

dbt sépare la préparation des données de leur modélisation analytique et permet d'associer les transformations à des tests reproductibles.

Power BI retrouve alors son rôle principal : restituer et analyser des données préparées en amont.

Cette évolution constitue pour moi l'un des principaux enseignements du stage.

J'ai commencé le projet en considérant principalement le dashboard comme le résultat à construire. J'ai progressivement compris que la qualité de cette restitution dépend d'un ensemble de décisions prises bien avant l'affichage des indicateurs : compréhension du métier, granularité, qualité des sources, modélisation, transformation et contrôle des données.

Le résultat du stage ne se limite donc pas aux trois pages Power BI.

Il comprend également :

- une analyse du besoin et du métier ;
- une formalisation des données ;
- une modélisation détaillée V1 ;
- une démarche de validation et de simplification ;
- un modèle décisionnel V2 ;
- un prototype Power BI adapté à plusieurs niveaux de décision ;
- une extraction automatisée des documents métier ;
- un traitement Python modulaire ;
- une base PostgreSQL structurée en couche RAW ;
- des transformations staging et mart avec dbt ;
- des contrôles de qualité automatisés ;
- cinq tables analytiques destinées à la restitution ;
- une documentation permettant de comprendre et de reproduire les principaux choix réalisés.

ATLAS reste un prototype. Le raccordement définitif du modèle Power BI V2 aux nouvelles tables analytiques, l'intégration d'un plus grand nombre d'opérations et l'orchestration automatique du pipeline constituent les principales étapes suivantes.

Cependant, le projet démontre qu'il est possible de passer de documents métier dispersés à une chaîne de données structurée et contrôlée, puis à une restitution décisionnelle adaptée aux utilisateurs.

Ce stage a ainsi fait évoluer ma compréhension du rôle du Data Engineer.

Il ne s'agit pas seulement de déplacer ou de transformer des données, ni de multiplier les outils techniques.

Il s'agit de construire une chaîne dans laquelle les données peuvent progressivement devenir fiables, traçables, compréhensibles et réellement utiles à la décision.


Rapport de stage ATLAS · BAMANIA Nathanaël Nicolas · Data Engineering · Juillet–Septembre 2026
