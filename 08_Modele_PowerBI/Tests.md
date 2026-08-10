# Tests — Validation du modèle Power BI ATLAS

> Page de validation créée avant tout dashboard.  
> Principe : si les comptages sont corrects, le modèle est correct.

## Méthode de validation

Avant de créer le moindre visuel métier, on valide que chaque table contient le bon nombre de lignes. Une carte Power BI avec `COUNTROWS` sur chaque table suffit.

## Résultats attendus vs constatés

| Table | Lignes attendues | Lignes constatées | Statut |
|-------|-----------------|------------------|--------|
| Communes | 4 | | ⏳ |
| Acteurs | 2 | | ⏳ |
| Entreprises | 6 | | ⏳ |
| Phase | 5 | | ⏳ |
| Organismes | 5 | | ⏳ |
| Type_Travaux | 8 | | ⏳ |
| Types_Risques | 4 | | ⏳ |
| Type_Indicateur | 16 | | ⏳ |
| Operations | 4 | | ⏳ |
| Estimation_Financiere | 24 | | ⏳ |
| Marche | 4 | | ⏳ |
| Lots | 12 | | ⏳ |
| Intervenir_Sur | 8 | | ⏳ |
| Participer_Au_Lot | 23 | | ⏳ |
| Subventions | 30 | | ⏳ |
| Risques | 16 | | ⏳ |
| Indicateurs_DD | 64 | | ⏳ |
| **TOTAL** | **235** | | ⏳ |

## Mesures DAX de comptage

```dax
Nb Opérations = COUNTROWS(Operations)
Nb Communes = COUNTROWS(Communes)
Nb Marchés = COUNTROWS(Marche)
Nb Lots = COUNTROWS(Lots)
Nb Entreprises = COUNTROWS(Entreprises)
Nb Subventions = COUNTROWS(Subventions)
Nb Risques = COUNTROWS(Risques)
Nb Indicateurs DD = COUNTROWS(Indicateurs_DD)
```

## Tests de cohérence relationnelle

| Test | Formule DAX | Résultat attendu |
|------|------------|-----------------|
| Chaque opération a un marché | `COUNTROWS(Operations)` = `COUNTROWS(Marche)` | 4 = 4 |
| Chaque marché a 3 lots | `COUNTROWS(Lots)` = `COUNTROWS(Marche)` × 3 | 12 = 4 × 3 |
| Total subventions notifiées | `SUM(Subventions[montant_notifie])` | 1 109 000 € |
| Indicateurs par opération | `COUNTROWS(Indicateurs_DD)` / `COUNTROWS(Operations)` | 16 |
| Risques avérés | `CALCULATE(COUNTROWS(Risques), Risques[statut]="Avéré")` | 4 |

---

*Tests validation · ATLAS · Août 2026*
