# 03 — Modélisation des données

## Architecture du modèle

```
                    dim_operation
                   /             \
                  /               \
       fact_operations        fact_subventions
          │  │  │  │  │            │    │
          │  │  │  │  │            │    │
    dim_phase  │  │  dim_statut   dim_organisme
    dim_territoire  dim_calendrier  dim_type_travaux
               dim_moe
```

## Granularité retenue

**`fact_operations` : 1 ligne = 1 opération × 1 phase (AVP, PRO, ACT, DET, AOR)**

Justification : chaque phase produit un budget distinct. Cette granularité permet de suivre l'évolution budgétaire de l'AVP au coût final sans écraser les valeurs précédentes.

**`fact_subventions` : 1 ligne = 1 subvention notifiée**

Justification : une opération peut recevoir N subventions de N organismes. Séparer les deux tables évite le double comptage des budgets.

## Nouveauté issue des données réelles

Les 4 projets pilotes révèlent une dimension supplémentaire non anticipée : **les indicateurs de développement durable** (16 par projet, avec cibles et valeurs constatées). Une table `fact_indicateurs_dd` sera ajoutée au modèle.

## Fichiers

- [`MCD/mcd.md`](MCD/mcd.md) — Modèle Conceptuel de Données
- [`MLD/mld.md`](MLD/mld.md) — Modèle Logique de Données
- [`Star_Schema/star_schema.sql`](Star_Schema/star_schema.sql) — DDL PostgreSQL complet
- [`Dictionnaires/dictionnaire_donnees.md`](Dictionnaires/dictionnaire_donnees.md) — Dictionnaire de données
- [`Dictionnaires/regles_gestion.md`](Dictionnaires/regles_gestion.md) — Règles de gestion métier
