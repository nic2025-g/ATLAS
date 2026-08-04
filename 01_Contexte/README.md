# 01 — Contexte du projet

## Présentation du stage

**Stage :** Conception d'une plateforme décisionnelle de pilotage des investissements territoriaux  
**Entreprise :** Communauté de Communes du Grand Avignon  
**Période :** 15 juillet → 2 septembre 2025  
**Encadrant :** Dominique VOLOT — Directeur des Services Techniques

## Objectifs

1. Analyser et structurer les données issues des projets d'aménagement territorial
2. Concevoir un modèle de données décisionnel (star schema)
3. Préparer un dataset consolidé
4. Développer un tableau de bord Power BI de suivi des services techniques

## Organisation

La **Communauté de Communes du Grand Avignon** regroupe plusieurs communes du territoire. Elle pilote des projets d'aménagement urbain au bénéfice de l'ensemble des habitants : voirie, réseaux d'eau potable, assainissement, espaces verts, éclairage public.

## Acteurs

| Acteur | Rôle | Dans ATLAS |
|--------|------|-----------|
| **MOA** — Communauté de Communes | Commanditaire et financeur | Client du dashboard |
| **MOE** — Artelia | Maîtrise d'œuvre (conception + supervision) | `dim_moe` |
| **ENT** — SO.TRA.VER, TERRA PAYSAGE SUD, etc. | Réalisent les travaux | `dim_entreprise` |
| **Élus** | Décideurs politiques | Utilisateurs dashboard (vue synthèse) |
| **DGST** | Directeur des Services Techniques | Utilisateur dashboard (vue pilotage) |
| **Chefs de projet** | Suivent chaque opération | Utilisateurs dashboard (vue détail) |

## Fichiers

- [`glossaire.md`](glossaire.md) — 20 termes métier définis
- [`acteurs.md`](acteurs.md) — Description détaillée des acteurs
- [`objectifs.md`](objectifs.md) — Objectifs et périmètre du projet
