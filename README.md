# ATLAS — Plateforme décisionnelle de pilotage des investissements territoriaux

> **A**nalyse **T**erritoriale des **L**iaisons, **A**ménagements et **S**ubventions

[![Stage](https://img.shields.io/badge/Stage-Data%20Engineering-2E6DB4)](.)
[![Statut](https://img.shields.io/badge/Statut-En%20cours-orange)](.)
[![Stack](https://img.shields.io/badge/Stack-PostgreSQL%20%7C%20dbt%20%7C%20Power%20BI-blue)](.)
[![Licence](https://img.shields.io/badge/Licence-MIT-green)](LICENSE)

---

## Présentation

ATLAS est une **plateforme décisionnelle** conçue pour la **Communauté de Communes du Grand Avignon**. Elle permet aux élus et au Directeur des Services Techniques (DGST) de piloter en temps réel leurs investissements territoriaux : coûts, délais, subventions, performance des services techniques.

Ce projet est réalisé dans le cadre d'un **stage Data Engineering** (15 juillet → 2 septembre 2025) et documenté comme un livrable de cabinet de conseil.

---

## Le problème

Le suivi des projets d'aménagement repose aujourd'hui sur des fichiers Excel manuels. Il n'existe pas de vision consolidée. Les élus ne peuvent pas répondre simplement à :

- *Combien avons-nous investi depuis le début du mandat ?*
- *Quel est notre reste à charge après subventions ?*
- *Nos projets sont-ils livrés dans les délais et les budgets prévus ?*

---

## La solution ATLAS

```
Sources Excel (SharePoint)
        │
        ▼
   Airbyte (ingestion)
        │
        ▼
 PostgreSQL — raw → staging → gold
        │
        ▼
    dbt (transformations)
        │
        ▼
  Power BI (dashboard)
        │
   Kestra (orchestration)
```

---

## Structure du dépôt

```
ATLAS/
├── README.md
├── 01_Contexte/              ← Présentation, objectifs, acteurs, glossaire
├── 02_Analyse_Metier/        ← Cycle de vie, processus, besoins, indicateurs
├── 03_Modelisation/          ← MCD, MLD, Star Schema, dictionnaires
│   ├── MCD/
│   ├── MLD/
│   ├── Star_Schema/
│   └── Dictionnaires/
├── 04_Donnees/               ← Données par projet (notes, Excel, sources, nettoyage)
│   ├── Projet1_Les_Angles/
│   ├── Projet2_Avignon/
│   ├── Projet3_Entraigues/
│   └── Projet4_Morieres/
├── 05_ETL/                   ← Pipeline de données
│   ├── Python/               ← Scripts de transformation
│   ├── SQL/                  ← DDL et requêtes
│   ├── dbt/                  ← Modèles dbt
│   └── Kestra/               ← Workflows d'orchestration
├── 06_Dashboard/             ← Power BI, mockups, KPIs, captures
│   ├── Mockups/
│   ├── KPIs/
│   └── Captures/
├── 07_Documentation/         ← Annexes et livrables du dossier de conception
├── rapport_stage/            ← Rapport de stage et journal de bord
└── docs/                     ← Documentation technique
```

---

## Les 4 projets pilotes

| # | Projet | Commune | Budget programme | Complexité | MOE |
|---|--------|---------|-----------------|-----------|-----|
| 1 | Requalification av. de Verdun + place du 8-Mai | Les Angles | 1 850 000 € HT | Moyenne | Artelia |
| 2 | Réaménagement rue des Marronniers | Avignon (Monclar) | 1 700 000 € HT | Faible | Artelia |
| 3 | Requalification quais de la Sorgue + place du Marché | Entraigues-sur-la-Sorgue | 2 350 000 € HT | Élevée | Artelia |
| 4 | Requalification av. du Grès + place des Micocouliers | Morières-lès-Avignon | 2 100 000 € HT | Moyenne | Artelia |

---

## Stack technique

| Couche | Outil | Rôle |
|--------|-------|------|
| Sources | Excel / SharePoint | Données saisies par les chefs de projet |
| Ingestion | Airbyte | Connecteurs sources → PostgreSQL |
| Stockage | PostgreSQL | Entrepôt (raw → staging → gold) |
| Transformation | dbt | Modèles SQL versionés et testés |
| Orchestration | Kestra | Pipeline end-to-end automatisé |
| Environnement | Docker | Stack conteneurisée |
| Restitution | Power BI | Dashboard décisionnel |

---

## KPIs principaux

**Axe 1 — Investissements**
- Budget total engagé sur le mandat
- Coût total réalisé
- Total subventions notifiées
- **Reste à charge** = Coût réalisé − Subventions notifiées
- Taux de financement externe

**Axe 2 — Performance des services techniques**
- Taux de respect des délais
- Taux de dépassement budgétaire
- Nombre d'opérations en retard
- Écart AVP vs coût final

**Axe 3 — Développement durable** *(données réelles disponibles)*
- Surface perméable créée (m²)
- Arbres plantés (U)
- Économie électrique (kWh/an)
- Heures d'insertion (h)
- Part d'économie locale (%)

---

## Dossier de conception ATLAS

| Livrable | Description | Statut |
|---------|-------------|--------|
| L00 — Vision | Problème, solution, périmètre | ✅ |
| L01 — Étude du besoin | Profils, KPIs, alertes | ✅ |
| L02 — Analyse métier | Loi MOP, processus AS-IS/TO-BE | ✅ |
| L03 — Modèle Conceptuel | MCD, entités, relations | 🔄 |
| L04 — Modèle Logique | Star schema, dictionnaire | 🔄 |
| L05 — Architecture | Pipeline, justifications | ⏳ |
| L06 — Spécifications Dashboard | KPIs, DAX, wireframes | ⏳ |
| L07 — Industrialisation | dbt, Kestra, gouvernance | ⏳ |
| L08 — Guide utilisateur | Mode d'emploi | ⏳ |
| L09 — Retour d'expérience | Bilan, recommandations | ⏳ |

---

## Auteur

**BAMANIA Nicolas** — Stagiaire Data Engineering  
Communauté de Communes du Grand Avignon  
Encadrant : **Dominique VOLOT** — Directeur des Services Techniques  
Stage : 15 juillet → 2 septembre 2025

---

*ATLAS — Analyse Territoriale des Liaisons, Aménagements et Subventions*
