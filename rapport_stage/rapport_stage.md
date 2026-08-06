# Rapport de stage: ATLAS
## Conception d'une plateforme décisionnelle de pilotage des investissements territoriaux

**Auteur :** BAMANIA Nicolas  
**Formation :** Data Engineering chez OpenClassrooms  
**Entreprise :  
**Encadrant :** Dominique VOLOT — Directeur des Services Techniques  
**Période :** 15 juillet 2026 → 2 septembre 2026  
**Dépôt :** https://github.com/nic2025-g/ATLAS

---

## Pourquoi ATLAS ?

Au départ, je pensais réaliser un simple tableau de bord Power BI.

Très rapidement, j'ai compris que le véritable problème n'était pas la visualisation, mais l'absence d'un modèle de données cohérent.

Le projet ATLAS est donc progressivement devenu un projet de conception d'un système décisionnel complet.

Cette évolution explique pourquoi une grande partie du stage est consacrée à l'analyse métier et à la modélisation avant même la construction du dashboard.

## Résumé

Ce stage porte sur la conception d'une plateforme décisionnelle — baptisée **ATLAS** (Analyse Territoriale des Liaisons, Aménagements et Subventions) — pour la Communauté de Communes du Grand Avignon.

L'objectif : permettre aux élus et au Directeur des Services Techniques de piloter en temps réel leurs investissements territoriaux — coûts, délais, subventions, performance des services.

Ce document retrace la progression semaine par semaine : d'où je suis parti, ce que j'ai compris, ce que ça a changé dans ma façon de travailler.

---

## D'où je suis parti — état initial

Au début du stage, je savais utiliser des outils de data engineering (Python, SQL, Docker, dbt). Mais je ne savais pas encore comment **partir d'un problème métier réel** pour construire un modèle de données rigoureux.

Ma première approche instinctive aurait été : ouvrir Power BI, importer des fichiers Excel, créer des graphiques. C'est ce que font la plupart des stagiaires — et c'est une erreur.

Ce stage m'a appris à inverser l'ordre : comprendre d'abord, modéliser ensuite, construire en dernier.

---

## La démarche — 5 étapes dans l'ordre

```
Étape 1 — Comprendre le métier        ✅ Semaines 1-2
Étape 2 — Analyser les besoins        ✅ Semaines 2-3
Étape 3 — Comprendre les données      ✅ Semaine 3
Étape 4 — Modéliser (MCD → MLD → SQL) ✅ Semaines 3-4
Étape 5 — Construire le dashboard     ⏳ Semaines 5-7
```

Cette démarche garantit que chaque décision technique est justifiée par un besoin métier réel — pas par ce que l'outil sait faire.

---

## Semaine 1 — 15 au 19 juillet

### D'où je partais
Je connaissais Power BI de nom mais ne l'avais jamais utilisé sur un vrai projet. Je ne savais pas ce qu'était un schéma en étoile ni pourquoi c'était important.

### Ce que j'ai fait
Construction d'un mini-modèle Power BI sur des données de ventes fictives : tables Ventes, Clients, Produits, Calendrier. Correction des erreurs de cardinalités, premières mesures DAX.

### Ce que j'ai compris
**La granularité conditionne tout.** Avant même de penser aux visuels, il faut répondre à : *"une ligne représente quoi ?"* Si la réponse n'est pas claire, le modèle produit des résultats faux.

**Sans dim_calendrier, pas de Time Intelligence.** Les fonctions DAX comme `SAMEPERIODLASTYEAR` ou `DATESYTD` ne fonctionnent pas sans une dimension calendrier correcte. Ce n'est pas un détail — c'est une condition préalable.

**Ce que ça a changé :** j'ai compris que Power BI n'est que la couche de restitution. Le vrai travail est dans le modèle de données, en amont.

---

## Semaine 2 — 22 au 26 juillet

### D'où je partais
Je connaissais les outils data mais pas le domaine métier de l'aménagement territorial. Je ne savais pas ce qu'était la loi MOP, un MOE, un AVP, un marché alloti.

### Ce que j'ai fait
Lecture et analyse des notes de l'encadrant. Compréhension du cycle de vie d'un projet (loi MOP, 5 phases). Production des livrables L00, L01, L02. Première version du modèle de données (11 tables). Initialisation du dépôt GitHub.

### Ce que j'ai compris

**La loi MOP structure directement le modèle de données.** Chaque phase (AVP, PRO, ACT, DET, AOR) produit une estimation budgétaire distincte. Ce n'est pas un choix de modélisation — c'est le reflet du cadre réglementaire. Si je n'avais pas compris la loi MOP, j'aurais mis 5 colonnes dans une seule table et écrasé les valeurs précédentes à chaque phase.

**Les bordereaux de prix sont incomparables entre MOE.** Chaque cabinet structure ses postes de travaux différemment. Sans normalisation en catégories standardisées (AEP, EU, EP, Voirie…), il est impossible de comparer les coûts entre projets.

**Ce que ça a changé :** j'ai arrêté de penser en colonnes Excel et commencé à penser en entités et relations.

Les échanges avec mon encadrant ces moments-ci m'ont fait comprendre que le tableau de bord ne devait pas répondre à mes questions, mais à celles des élus.

Cette remarque a complètement changé ma façon de construire le modèle.

---

## Semaine 3 — 29 juillet au 6 août

### D'où je partais
J'avais un modèle de données théorique construit depuis une prise de notes. Mais je n'avais pas encore vu les données réelles.

### Ce que j'ai fait
Réunion avec l'encadrant (dimanche 3 août). Réception et analyse des 4 dossiers de projets réels. Restructuration complète du dépôt GitHub en format cabinet de conseil. Découverte des 16 indicateurs de développement durable.

### Ce que j'ai compris
**Un modèle théorique est toujours incomplet.** Les données réelles m'ont révélé une dimension entière que je n'avais pas anticipée : les indicateurs de développement durable (16 par projet, avec cibles et valeurs constatées). J'ai dû ajouter une entité `INDICATEUR_DD` et un référentiel `TYPE_INDICATEUR` qui n'existaient pas dans ma première version.

**Les données brutes parlent si on sait les lire.** En analysant les 4 projets, j'ai observé que les mêmes 6 entreprises interviennent systématiquement, que les mêmes 5 organismes financent les mêmes natures de travaux, que le même MOE (Artelia) pilote les 4 projets. Ce n'est pas de la redondance — c'est le signal que le modèle doit avoir des référentiels stables.

**Ce que ça a changé :** j'ai compris que l'analyse des données réelles n'est pas une étape après la modélisation — c'est une étape pendant la modélisation.

**Chiffres clés des 4 projets pilotes :**
- Budget total programme : 8 000 000 € HT
- Total subventions notifiées : 1 109 000 € HT
- Reste à charge collectivité : ~7 000 000 € HT
- Taux de financement externe : 13,7%

### Difficultés rencontrées
Je pensais initialement modéliser les budgets directement dans **operation**. Après plusieurs échanges, j'ai compris que cette approche empêchait l'historisation.
Cette erreur m'a conduit à créer l'entité **estimation_financiere**.

---

## Semaine 4 — 5 au 9 août

### D'où je partais
J'avais des données structurées et un modèle de données incomplet — construit sans méthode formelle. Je générais des fichiers Excel "au fil de l'eau" en ajoutant des colonnes selon les besoins.

### Ce que j'ai fait
**Décision majeure :** arrêter de générer des fichiers et reprendre depuis le MCD Mérise.

Construction du MCD complet avec la méthode Merise : 17 entités, toutes les cardinalités, toutes les associations. Discussion et validation de chaque choix avec l'encadrant (virtuel). Traduction en MLD. Génération du DDL PostgreSQL (571 lignes). Regénération des 17 fichiers Excel depuis le MCD validé.

**Pourquoi repartir du MCD ?**

Au départ, je construisais progressivement les fichiers Excel en ajoutant des colonnes au fur et à mesure de mes découvertes.

Cette approche fonctionnait avec quatre projets, mais je me suis rapidement rendu compte qu'elle ne garantissait ni la cohérence des données, ni l'évolutivité du modèle.

J'ai donc volontairement arrêté cette construction incrémentale afin de revenir à une démarche d'ingénierie :

Métier
↓

MCD

↓

MLD

↓

Excel

↓

Power BI

Cette décision m'a permis de garantir que chaque fichier Excel représente une entité clairement définie.

### Ce que j'ai compris
**La méthode avant l'outil.** La différence entre un fichier Excel généré "au fil de l'eau" et un fichier Excel traduit depuis un MCD validé est invisible à l'œil nu — mais fondamentale. Le premier sera incohérent dès qu'on ajoute un nouveau projet. Le second est extensible sans modification de la structure.

**Trois décisions de modélisation qui méritent d'être expliquées :**

**1. `type_acteur` n'est pas dans `ACTEUR`.**
MOA et MOE sont structurellement deux organisations similaires (elles ont les mêmes attributs : nom, adresse, contact). Le rôle MOA/MOE n'est pas une propriété de l'organisation — c'est une propriété de sa relation avec une opération. Il est donc dans l'association `INTERVENIR_SUR`. Si demain Artelia devenait MOA sur un projet, il n'y aurait pas à créer une deuxième fiche Artelia.

**2. `ESTIMATION_FINANCIERE` est une entité séparée.**
L'alternative naïve : mettre `budget_avp`, `budget_pro`, `prix_marche`, `montant_engage`, `cout_final` comme 5 colonnes dans `OPERATION`. Le problème : une opération peut avoir plusieurs marchés successifs. Et `montant_engage` évolue chaque mois — on veut historiser, pas écraser. Avec `ESTIMATION_FINANCIERE`, chaque valeur est une ligne avec sa date.

**3. `MARCHE` est une entité à part entière.**
Un marché est un acte juridique distinct de l'opération. Il a ses propres attributs (référence administrative, date de notification, montant total) et une cardinalité différente (1 opération → N marchés possibles). Sans cette entité, il est impossible de modéliser une résiliation suivie d'un nouveau marché.

### Le MCD final — 17 tables en 5 couches

```
Couche 1 — Référentiels stables   (6) : COMMUNE, ACTEUR, ENTREPRISE, PHASE, ORGANISME, TYPE_TRAVAUX
Couche 2 — Référentiels catalogues(2) : TYPE_RISQUE, TYPE_INDICATEUR
Couche 3 — Objets métier          (4) : OPERATION, ESTIMATION_FINANCIERE, MARCHE, LOT
Couche 4 — Associations N:N       (2) : INTERVENIR_SUR, PARTICIPER_AU_LOT
Couche 5 — Faits métier           (3) : SUBVENTION, RISQUE, INDICATEUR_DD
```

**Ce que ça a changé :** je ne génère plus de fichiers au fil de l'eau. Chaque fichier Excel est maintenant la traduction physique d'une entité validée dans le MCD.

Avec le recul, je pense qu'il aurait été plus efficace de commencer par une matrice d'extraction des données avant de construire les premiers fichiers Excel.
Cette matrice aurait permis de mieux identifier les objets métier récurrents.

### Questions ouvertes

```
Faut-il une entité **calendrier** ?

Le planning doit-il rester une entité ?

**marche** est-il indispensable ?

Comment adapter le modèle à plusieurs mandats ?
```

### Ce que j'ai compris aujourd'hui:

```
- Aujourd'hui j'ai compris que le MCD ne sert pas seulement à dessiner des boîtes. Il sert à définir ce qui existe réellement dans le métier.
- j'ai aussi compris qu'une entreprise ne "fait pas partie" d'une opération. Elle intervient sur un lot
- Aujourd'hui j'ai compris pourquoi les associations N:N existent.
```

### Les prochaines hypotheses a verifier:

**Hypothèse 1:** Le modèle est-il capable d'intégrer 50 projets ?

**Hypothèse 2:** Les 17 fichiers sont-ils suffisants ?

**Hypothèse 3:** Power BI aura-t-il besoin d'un Star Schema différent du MCD ?

**Hypothèse 4:** Quels KPI les élus utiliseront-ils réellement ?
---


## Semaines 5–8 — À venir

> 🔄 À compléter au fil du stage

---

## Bilan à mi-parcours — Ce que ce stage m'a appris

### Sur la méthode
Un projet data engineering ne commence pas par les outils. Il commence par le métier. Comprendre la loi MOP m'a pris 3 jours — mais ces 3 jours ont déterminé l'architecture de tout le reste.

### Sur la modélisation
La différence entre un bon modèle et un mauvais modèle n'est pas visible dans les données — elle est visible quand les données changent. Un modèle conçu depuis un MCD Merise validé est extensible. Un modèle construit "au fil de l'eau" accumule de la dette technique.

### Sur le travail d'analyste
Analyser 4 dossiers de projets réels m'a appris à lire des données comme un métier les lit — pas comme un ingénieur. Ce que j'aurais appelé "redondance" (les mêmes entreprises, les mêmes organismes, les mêmes phases), un chef de projet appelle "stabilité opérationnelle".

---

## Livrables produits

| Livrable | Description | Statut |
|---------|-------------|--------|
| L00 — Vision | Problème, solution, périmètre | ✅ |
| L01 — Étude du besoin | Profils, KPIs, alertes | ✅ |
| L02 — Analyse métier | Loi MOP, processus AS-IS/TO-BE | ✅ |
| MCD Merise | 17 entités, cardinalités, associations | ✅ |
| MLD complet | Tables, FK, contraintes, index | ✅ |
| DDL SQL PostgreSQL | 571 lignes, 17 tables, 3 vues | ✅ |
| 17 fichiers Excel | Données des 4 projets pilotes | ✅ |
| Dépôt GitHub | Structure cabinet de conseil | ✅ |
| Dashboard Power BI | 4 pages, KPIs élus et DGST | ⏳ |

---

*Rapport de stage ATLAS · BAMANIA Nicolas · Data Engineering 2025*  
*Document vivant — mis à jour chaque semaine*
