# Rapport de stage — ATLAS

## Conception d’une plateforme décisionnelle de pilotage des investissements territoriaux

**Auteur :** BAMANIA Nathanaël Nicolas  
**Formation :** Data Engineering — OpenClassrooms  
**Structure d’accueil :** Collectivité territoriale — Services Techniques  
**Encadrant :** Dominique VOLOT — Directeur des Services Techniques  
**Période :** 15 juillet 2026 → 2 septembre 2026  

---

## 1. Introduction

Ce stage porte sur la conception d’une plateforme décisionnelle de pilotage des investissements territoriaux, baptisée **ATLAS — Analyse Territoriale des Liaisons, Aménagements et Subventions**.

L’objectif initial pouvait sembler simple : construire un tableau de bord Power BI permettant au Directeur des Services Techniques et aux élus de suivre les opérations d’aménagement.

L’analyse du besoin a cependant montré que la difficulté principale ne résidait pas dans la création des graphiques. Les informations utiles étaient d’abord présentes dans des dossiers métier narratifs et différents supports de suivi. Il fallait donc comprendre le métier, identifier les objets à suivre, structurer les informations, définir les relations entre elles et seulement ensuite construire la restitution décisionnelle.

Le stage est ainsi devenu un travail complet allant de **l’analyse métier à la modélisation des données, puis à leur préparation pour Power BI**.

---

## 2. Problématique

Les services techniques réalisent et suivent plusieurs opérations d’aménagement pour le compte de la collectivité. Pour assurer le pilotage et le reporting, il faut pouvoir répondre simplement à des questions telles que :

- combien la collectivité investit-elle ?
- comment les estimations évoluent-elles entre les différentes phases d’un projet ?
- quels sont les montants des marchés ?
- quelles subventions ont été notifiées et par quels organismes ?
- quel est le reste à charge de la collectivité ?
- quelles opérations présentent un risque de dépassement budgétaire ?
- quelles opérations sont en retard ?
- quels risques doivent attirer l’attention du DGST ?
- quels résultats environnementaux et sociaux sont associés aux opérations ?
- comment synthétiser l’ensemble de ces informations pour les élus ?

La problématique du stage peut donc être formulée ainsi :

> **Comment transformer des informations métier dispersées sur plusieurs opérations d’aménagement en un système de données cohérent permettant un pilotage fiable et synthétique dans Power BI ?**

---

## 3. Objectifs du stage

Le projet poursuit quatre objectifs principaux.

### 3.1 Comprendre le métier

Comprendre le fonctionnement d’une opération d’aménagement, ses acteurs, son cycle de vie et son vocabulaire : MOA, MOE, AVP, PRO, ACT, DET, AOR, marché, lot, subvention, risque, etc.

### 3.2 Structurer les données

Transformer les informations contenues dans les dossiers des opérations pilotes en données homogènes et réutilisables.

### 3.3 Construire un modèle décisionnel

Définir un modèle suffisamment robuste pour accueillir de nouvelles opérations sans reconstruire l’ensemble du système.

### 3.4 Restituer l’information

Construire dans Power BI des indicateurs adaptés aux différents niveaux de décision, notamment le DGST et les élus.

---

## 4. Démarche générale

La démarche suivie pendant le stage est progressive :

```text
Compréhension métier
        ↓
Analyse des besoins décisionnels
        ↓
Analyse des opérations pilotes
        ↓
Identification des objets métier
        ↓
MCD
        ↓
MLD
        ↓
17 fichiers Excel structurés
        ↓
OneDrive / SharePoint
        ↓
Power Query
        ↓
Modèle Power BI
        ↓
Mesures DAX
        ↓
Dashboard décisionnel
```

Une architecture plus industrialisée pourra ensuite être proposée comme perspective :

```text
Excel / SharePoint
        ↓
Airbyte
        ↓
PostgreSQL
        ↓
dbt
        ↓
Power BI
        ↑
      Kestra
```

Cette deuxième architecture constitue à ce stade une **cible d’industrialisation** et non l’architecture opérationnelle du prototype.

---

# 5. Progression du stage

## Semaine 1 — Prise en main de Power BI et compréhension de la granularité

### Situation initiale

Je connaissais plusieurs outils de Data Engineering, mais je n’avais pas encore construit de modèle Power BI sur un cas métier réel.

### Travail réalisé

Un cas simplifié de ventes m’a permis de travailler sur :

- les tables de faits et de dimensions ;
- les relations entre tables ;
- les cardinalités ;
- la granularité ;
- les premières mesures DAX ;
- le principe d’une dimension calendrier.

### Enseignement principal

La première question à poser avant de créer un indicateur est :

> **Que représente exactement une ligne de ma table ?**

Cette notion de granularité est devenue essentielle pour la suite du projet.

J’ai également compris que Power BI constitue la couche de restitution : la fiabilité du dashboard dépend avant tout de la qualité du modèle situé en amont.

---

## Semaine 2 — Compréhension du métier

### Situation initiale

Le domaine de l’aménagement territorial m’était encore largement inconnu.

### Travail réalisé

J’ai étudié les notes de mon encadrant afin de comprendre :

- les rôles de la maîtrise d’ouvrage et de la maîtrise d’œuvre ;
- le cycle d’une opération ;
- les phases AVP, PRO, ACT, DET et AOR ;
- les marchés de travaux ;
- les lots ;
- les entreprises ;
- les subventions ;
- les attentes du DGST et des élus.

### Évolution de ma réflexion

Au départ, je raisonnais principalement en termes de données à afficher.

Les échanges avec mon encadrant ont déplacé la question vers le besoin décisionnel :

> **Que cherchent les élus à savoir ou à comprendre de l’activité des services techniques ?**

Cette question est devenue l’un des fils directeurs du projet.

---

## Semaine 3 — Analyse des quatre opérations pilotes, Modélisation et constitution du socle Excel

### Travail réalisé

Quatre dossiers d’opérations pilotes ont été étudiés. Ces documents constituaient davantage une source métier narrative qu’une base de données directement exploitable.

J’ai donc dû identifier dans ces documents les informations récurrentes :

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

### Découverte importante

L’analyse des dossiers a fait apparaître **16 indicateurs de développement durable**, qui n’avaient pas été prévus dans le premier modèle.

Cela a conduit à introduire :

- `TYPE_INDICATEUR` ;
- `INDICATEUR_DD`.

Cette étape a montré qu’un modèle théorique doit être confronté aux données métier avant d’être considéré comme stable.

### Données pilotes

Sur les quatre opérations étudiées, les informations disponibles permettent notamment de suivre les budgets, les prix de marché et les subventions notifiées.

Les valeurs utilisées dans le prototype devront toutefois être distinguées des données définitivement validées par le métier.

---

### Limite de la première approche

Ma première approche consistait à créer progressivement des fichiers Excel en ajoutant les colonnes nécessaires au fur et à mesure.

Cette méthode fonctionnait sur quelques projets, mais elle présentait un risque : construire les fichiers en fonction des exemples disponibles plutôt qu’en fonction d’un modèle métier stable.

### Changement de méthode

J’ai donc repris le travail dans l’ordre suivant :

```text
Métier → MCD → MLD → fichiers Excel → Power BI
```

### Modèle obtenu

Le modèle comprend actuellement **17 fichiers répartis en cinq groupes**.

#### Référentiels stables

- Communes
- Acteurs
- Entreprises
- Phase
- Organismes
- Type_Travaux

#### Référentiels catalogues

- Types_Risques
- Type_Indicateur

#### Objets métier

- Operations
- Estimation_Financiere
- Marche
- Lots

#### Associations

- Intervenir_Sur
- Participer_Au_Lot

#### Faits métier

- Subventions
- Risques
- Indicateurs_DD

### Trois décisions de modélisation importantes

#### 1. Séparer l’acteur de son rôle

Le rôle d’un acteur est porté par son intervention sur une opération plutôt que directement par l’entité `ACTEUR`.

Cela permet de ne pas dupliquer une même organisation lorsque son rôle varie selon le contexte.

#### 2. Historiser les estimations financières

Au lieu de placer plusieurs colonnes budgétaires directement dans `OPERATION`, l’entité `ESTIMATION_FINANCIERE` permet de conserver plusieurs valeurs et plusieurs dates.

L’objectif est de suivre l’évolution financière plutôt que de conserver uniquement la dernière valeur connue.

#### 3. Modéliser le marché comme un objet métier

Le marché possède sa propre identité, ses dates, son montant et ses lots. Il est donc traité comme un objet distinct de l’opération.

### Résultat

Les quatre dossiers pilotes ont été transformés en un **socle structuré de 17 fichiers Excel reliés par des identifiants**.

Ces fichiers constituent actuellement l’interface entre la connaissance métier et Power BI.

---

## Semaine 4 — Passage du modèle métier au modèle Power BI

### Travail réalisé

Les 17 fichiers Excel ont été déposés sur OneDrive / SharePoint puis chargés dans Power BI.

Les relations entre les tables ont été créées et contrôlées afin de reproduire les dépendances définies lors de la modélisation.

Cette étape m’a fait comprendre une distinction importante :

> **Le MCD décrit le métier ; le modèle Power BI doit être optimisé pour l’analyse.**

Il n’est donc pas nécessaire que le modèle analytique soit une reproduction graphique exacte du MCD.

### Table de mesures

Une table dédiée, `_Mesures_ATLAS`, a été créée afin de centraliser les mesures DAX.

Les mesures sont organisées par thèmes :

```text
01_Validation
02_Investissements
03_Subventions
04_Délais
05_Risques
06_Developpement_Durable
07_Performance
```

Cette organisation facilite la maintenance du modèle et prépare l’augmentation future du nombre d’indicateurs.

### Premières mesures de validation

Avant de construire le dashboard final, des mesures simples ont été créées pour contrôler le modèle :

- nombre d’opérations ;
- nombre de communes ;
- nombre de marchés ;
- nombre de lots ;
- nombre d’entreprises ;
- nombre de subventions ;
- nombre de risques ;
- nombre d’indicateurs DD.

Ces mesures permettent de vérifier que les relations et les filtres produisent des résultats cohérents.

### Premiers indicateurs de pilotage

Le travail s’est ensuite étendu à plusieurs familles d’indicateurs :

- investissements ;
- subventions ;
- délais ;
- risques ;
- développement durable ;
- performance des services techniques.

Des indicateurs d’alerte ont également commencé à être construits afin d’identifier rapidement les situations nécessitant une attention particulière.

---

# 6. Du suivi des projets au pilotage décisionnel

L’un des enseignements importants du stage est que le dashboard ne doit pas simplement reproduire les données disponibles.

Il doit transformer ces données en information utile à la décision.

Trois niveaux de lecture se dessinent.

### Niveau Élus — vision stratégique

L’objectif est de répondre rapidement à des questions telles que :

- combien avons-nous investi ?
- quelle part est financée par des subventions ?
- quels projets nécessitent une attention particulière ?
- les engagements financiers et calendaires sont-ils globalement maîtrisés ?
- quels résultats territoriaux, environnementaux ou sociaux sont obtenus ?

### Niveau DGST — vision de pilotage

Le DGST doit pouvoir identifier :

- les opérations en retard ;
- les dépassements budgétaires ;
- les risques critiques ;
- les écarts entre estimations successives ;
- les projets nécessitant une intervention.

### Niveau opérationnel — vision détaillée

Une vue détaillée doit permettre de revenir à une opération et d’expliquer l’origine d’un indicateur ou d’une alerte.

Cette logique évite de construire un dashboard unique surchargé pour tous les utilisateurs.

---

# 7. Qualité des données

La construction du prototype a également fait apparaître un enjeu important de gouvernance.

Les fichiers destinés à Power BI doivent respecter plusieurs règles :

- unicité des identifiants ;
- cohérence des clés étrangères ;
- formats homogènes ;
- référentiels partagés ;
- valeurs contrôlées ;
- absence de cellules fusionnées ;
- traçabilité des données absentes ou incertaines.

L’objectif n’est donc pas uniquement de produire dix-sept fichiers Excel, mais de définir **comment ces fichiers devront être alimentés et maintenus lorsque de nouvelles opérations seront ajoutées**.

---

# 8. Points à valider avec l’encadrant

La prochaine étape ne consiste pas uniquement à créer davantage de graphiques.

Avant de poursuivre, plusieurs questions métier doivent être confirmées :

1. Les 17 fichiers représentent-ils correctement les informations que les services techniques devront réellement maintenir ?
2. Qui sera responsable de la saisie ou de la mise à jour de chaque famille de données ?
3. À quelle fréquence les informations seront-elles mises à jour ?
4. Quels champs doivent être obligatoires lors de la création d’une nouvelle opération ?
5. Quels sont les indicateurs réellement prioritaires pour les élus ?
6. Quels indicateurs sont prioritaires pour le DGST ?
7. Quelles règles doivent déclencher une alerte budgétaire, de délai ou de risque ?
8. Comment définit-on officiellement qu’une opération est « en retard » ?
9. Comment définit-on officiellement un « dépassement budgétaire » : budget programme, AVP, PRO ou prix du marché ?
10. Les indicateurs de développement durable doivent-ils rester une famille spécifique ou être intégrés à une vision plus large de la performance des services techniques ?
11. Le modèle doit-il dès maintenant prévoir plusieurs mandats ?
12. Les futurs projets disposeront-ils des mêmes informations que les quatre projets pilotes ?

Ces validations sont essentielles car elles détermineront la signification des futurs KPI.

---

# 9. Difficultés rencontrées et décisions prises

## Comprendre avant de construire

La principale difficulté n’a pas été technique. Elle a consisté à comprendre suffisamment le métier pour éviter de construire un modèle techniquement correct mais métierement faux.

## Passer de documents narratifs à des données structurées

Les quatre dossiers reçus ne constituaient pas des tables prêtes à importer. Il a fallu identifier les objets récurrents et reconstruire une structure commune.

## Ne pas confondre prototype et architecture cible

Une autre difficulté a été de distinguer :

- ce qui doit réellement fonctionner pendant le stage ;
- ce qui constitue une proposition d’industrialisation future.

Le prototype actuel reste volontairement simple :

```text
Excel → OneDrive / SharePoint → Power BI
```

L’architecture PostgreSQL/dbt/Airbyte/Kestra est conservée comme perspective d’évolution.

---

# 10. Livrables et état d’avancement

| Livrable | État |
|---|---|
| Analyse du besoin | ✅ Réalisée |
| Analyse métier | ✅ Réalisée |
| Analyse des 4 opérations pilotes | ✅ Réalisée |
| Glossaire métier | ✅ Réalisé |
| MCD | ✅ Conçu |
| MLD | ✅ Conçu |
| Dictionnaire de données | ✅ Première version |
| 17 fichiers Excel | ✅ Construits |
| Publication OneDrive / SharePoint | ✅ Réalisée |
| Chargement Power BI | ✅ Réalisé |
| Relations du modèle Power BI | ✅ Créées |
| Table `_Mesures_ATLAS` | ✅ Créée |
| Mesures de validation | ✅ Créées |
| KPI financiers / subventions / risques / délais | 🔄 En cours |
| Alertes | 🔄 Premiers prototypes |
| Dashboard Élus | ⏳ À construire |
| Dashboard DGST | ⏳ À construire |
| Vue opération détaillée | ⏳ À construire |
| Architecture industrielle cible | 🔄 À formaliser |
| Guide utilisateur | ⏳ À produire |

---

# 11. Prochaines étapes

La suite du travail est organisée dans l’ordre suivant :

1. faire valider par l’encadrant le socle des 17 fichiers et les règles de gestion ;
2. finaliser les mesures DAX prioritaires ;
3. définir précisément les seuils des alertes ;
4. construire une dimension calendrier adaptée à l’analyse temporelle ;
5. concevoir la page de synthèse destinée aux élus ;
6. construire la vue de pilotage DGST ;
7. ajouter une vue détaillée par opération ;
8. tester le dashboard sur les quatre opérations pilotes ;
9. vérifier que le modèle accepte de nouvelles opérations sans modification structurelle ;
10. documenter le processus d’alimentation des fichiers ;
11. formaliser l’architecture cible d’industrialisation ;
12. finaliser le guide utilisateur et le bilan du stage.

---

# 12. Bilan intermédiaire

Ce stage m’a permis de comprendre qu’un projet Data Engineering ne commence pas nécessairement par Python, SQL ou un pipeline.

Dans ce projet, le premier travail d’ingénierie a été de transformer une connaissance métier dispersée en un modèle explicite et exploitable.

La progression peut être résumée ainsi :

```text
Au départ :
« Comment construire un dashboard Power BI ? »

Puis :
« Quelles données faut-il pour construire ce dashboard ? »

Ensuite :
« Comment représenter correctement le métier dans les données ? »

Aujourd’hui :
« Comment transformer ce modèle en outil de pilotage réellement utile aux décideurs ? »
```

Cette évolution constitue l’un des principaux apprentissages du stage.

Le prochain enjeu est désormais de vérifier que le modèle construit n’est pas seulement cohérent techniquement, mais qu’il correspond bien au fonctionnement réel des services et aux décisions que le DGST et les élus doivent prendre.

---

## 13. Journal de progression à poursuivre

Pour chaque nouvelle étape, je noterai :

- **ce que je voulais faire ;**
- **ce que j’ai réellement fait ;**
- **le problème rencontré ;**
- **la décision prise ;**
- **pourquoi cette décision a été prise ;**
- **ce que j’ai appris ;**
- **ce qu’il reste à valider.**

Cette méthode permettra de transformer le journal technique du stage en matière exploitable pour le rapport final et la soutenance.

---

*Rapport de stage ATLAS · BAMANIA Nathanaël Nicolas · Data Engineering · 2026*  
*Document vivant — mis à jour au fil du stage*
