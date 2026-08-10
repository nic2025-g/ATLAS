# Relations — Modèle Power BI ATLAS

> 17 relations créées manuellement — toutes les relations automatiques de Power BI ont été supprimées et recréées depuis la matrice des relations validée.

## Principe

Toutes les relations sont **unidirectionnelles** (sens unique) — de la table parent (côté 1) vers la table enfant (côté \*). Aucun filtre bidirectionnel — cela évite les ambiguïtés de calcul dans les mesures DAX.

## Les 17 relations

| # | Table parent | Clé parent | Table enfant | Clé enfant | Cardinalité | Statut |
|---|-------------|-----------|-------------|-----------|------------|--------|
| 1 | Communes | commune_id | Operations | commune_id | 1 → \* | ✅ |
| 2 | Phase | phase_id | Estimation_Financiere | phase_id | 1 → \* | ✅ |
| 3 | Operations | operation_id | Estimation_Financiere | operation_id | 1 → \* | ✅ |
| 4 | Operations | operation_id | Marche | operation_id | 1 → \* | ✅ |
| 5 | Marche | marche_id | Lots | marche_id | 1 → \* | ✅ |
| 6 | Type_Travaux | type_trav_id | Lots | type_trav_id | 1 → \* | ✅ |
| 7 | Lots | lot_id | Participer_Au_Lot | lot_id | 1 → \* | ✅ |
| 8 | Entreprises | entreprise_id | Participer_Au_Lot | entreprise_id | 1 → \* | ✅ |
| 9 | Acteurs | acteur_id | Intervenir_Sur | acteur_id | 1 → \* | ✅ |
| 10 | Operations | operation_id | Intervenir_Sur | operation_id | 1 → \* | ✅ |
| 11 | Operations | operation_id | Subventions | operation_id | 1 → \* | ✅ |
| 12 | Organismes | organisme_id | Subventions | organisme_id | 1 → \* | ✅ |
| 13 | Type_Travaux | type_trav_id | Subventions | type_trav_id | 1 → \* | ✅ |
| 14 | Operations | operation_id | Risques | operation_id | 1 → \* | ✅ |
| 15 | Types_Risques | type_risque_id | Risques | type_risque_id | 1 → \* | ✅ |
| 16 | Operations | operation_id | Indicateurs_DD | operation_id | 1 → \* | ✅ |
| 17 | Type_Indicateur | type_ind_id | Indicateurs_DD | type_ind_id | 1 → \* | ✅ |

## Relation écartée

| Relation | Raison |
|----------|--------|
| Lots → Subventions (lot_id) | Chemin ambigu détecté par Power BI — deux chemins vers Operations via Lots→Marche→Operations et via Operations→Subventions direct. Écarté pour éviter le double comptage. |

## Règles appliquées

- **Sens unique partout** — jamais de filtre bidirectionnel
- **Operations est le hub central** — 6 relations partent d'elle
- **Pas de relation directe entre deux tables de faits** — Subventions et Risques et Indicateurs_DD ne sont jamais reliées entre elles directement

---

*Relations · ATLAS · Août 2026*
