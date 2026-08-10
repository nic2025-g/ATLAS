# Mesures DAX — ATLAS

> Toutes les mesures sont dans la table `_Mesures`.  
> Principe : une mesure = une question métier.

---

## AXE 1 — Comptages (validation du modèle)

```dax
Nb Opérations =
    COUNTROWS(Operations)

Nb Communes =
    COUNTROWS(Communes)

Nb Marchés =
    COUNTROWS(Marche)

Nb Lots =
    COUNTROWS(Lots)

Nb Entreprises =
    COUNTROWS(Entreprises)

Nb Subventions =
    COUNTROWS(Subventions)

Nb Risques =
    COUNTROWS(Risques)

Nb Indicateurs DD =
    COUNTROWS(Indicateurs_DD)
```

---

## AXE 2 — Investissements (questions élus)

```dax
-- Budget voté avant le démarrage des études
Budget Programme =
    CALCULATE(
        SUM(Estimation_Financiere[montant]),
        Estimation_Financiere[type_budget] = "budget_programme"
    )

-- Estimation issue des études AVP (±30%)
Budget AVP =
    CALCULATE(
        SUM(Estimation_Financiere[montant]),
        Estimation_Financiere[type_budget] = "budget_avp"
    )

-- Estimation affinée issue des études PRO (±10%)
Budget PRO =
    CALCULATE(
        SUM(Estimation_Financiere[montant]),
        Estimation_Financiere[type_budget] = "budget_pro"
    )

-- Prix contractuel signé avec les entreprises
Prix Marché =
    CALCULATE(
        SUM(Estimation_Financiere[montant]),
        Estimation_Financiere[type_budget] = "prix_marche"
    )

-- Situations de travaux cumulées (DET)
Montant Engagé =
    CALCULATE(
        SUM(Estimation_Financiere[montant]),
        Estimation_Financiere[type_budget] = "montant_engage"
    )

-- Coût définitif arrêté à la réception (AOR)
Coût Final =
    CALCULATE(
        SUM(Estimation_Financiere[montant]),
        Estimation_Financiere[type_budget] = "cout_final"
    )

-- Référence financière la plus avancée disponible
Coût Référence =
    COALESCE(
        [Coût Final],
        [Prix Marché],
        [Budget PRO],
        [Budget AVP],
        [Budget Programme]
    )
```

---

## AXE 3 — Financement et subventions

```dax
-- Total des subventions notifiées (seule mesure suivie)
Total Subventions =
    SUM(Subventions[montant_notifie])

-- Part restant à financer par la collectivité
Reste à Charge =
    [Coût Référence] - [Total Subventions]

-- Part financée par des organismes externes
Taux Financement Externe =
    DIVIDE(
        [Total Subventions],
        [Coût Référence],
        0
    )

-- Subventions par organisme (utiliser avec slicer Organismes[nom])
Subventions par Organisme =
    SUM(Subventions[montant_notifie])
```

---

## AXE 4 — Performance et délais

```dax
-- Nombre de lots dont la date de fin prévue est dépassée
Nb Lots en Retard =
    CALCULATE(
        COUNTROWS(Lots),
        Lots[date_fin_reelle] = BLANK(),
        Lots[date_fin_prevue] < TODAY()
    )

-- Nombre de lots réceptionnés
Nb Lots Réceptionnés =
    CALCULATE(
        COUNTROWS(Lots),
        Lots[statut] = "Réceptionné"
    )

-- Taux de lots dans les délais
Taux Respect Délais =
    DIVIDE(
        CALCULATE(COUNTROWS(Lots), Lots[statut] = "Réceptionné",
                  NOT ISBLANK(Lots[date_fin_reelle]),
                  Lots[date_fin_reelle] <= Lots[date_fin_prevue]),
        [Nb Lots Réceptionnés],
        0
    )

-- Dépassement budgétaire AVP → Prix marché
Dépassement Budgétaire =
    [Prix Marché] - [Budget AVP]

-- Taux de dérive entre AVP et prix marché
Taux Dérive Budget =
    DIVIDE(
        [Dépassement Budgétaire],
        [Budget AVP],
        0
    )
```

---

## AXE 5 — Risques

```dax
-- Nombre de risques avérés
Nb Risques Avérés =
    CALCULATE(
        COUNTROWS(Risques),
        Risques[statut] = "Avéré"
    )

-- Nombre de risques sous veille (non avérés)
Nb Risques Sous Veille =
    CALCULATE(
        COUNTROWS(Risques),
        Risques[statut] = "Non avéré"
    )

-- Taux de risques avérés
Taux Risques Avérés =
    DIVIDE(
        [Nb Risques Avérés],
        COUNTROWS(Risques),
        0
    )
```

---

## AXE 6 — Développement durable

```dax
-- Nombre d'indicateurs DD conformes ou dépassés
Nb Indicateurs Conformes =
    CALCULATE(
        COUNTROWS(Indicateurs_DD),
        Indicateurs_DD[bilan] IN {"Conforme", "Dépassé"}
    )

-- Nombre d'indicateurs DD en retrait
Nb Indicateurs En Retrait =
    CALCULATE(
        COUNTROWS(Indicateurs_DD),
        Indicateurs_DD[bilan] = "En retrait"
    )

-- Taux global de conformité DD
Taux Conformité DD =
    DIVIDE(
        [Nb Indicateurs Conformes],
        CALCULATE(COUNTROWS(Indicateurs_DD),
                  NOT ISBLANK(Indicateurs_DD[bilan])),
        0
    )
```

---

## Notes d'implémentation

**Où créer les mesures :** toutes dans la table `_Mesures` — jamais directement dans une table de données.

**Ordre de création recommandé :**
1. Comptages (validation)
2. Budgets (AVP, PRO, Prix marché, Coût final)
3. Coût Référence (dépend des précédentes)
4. Total Subventions
5. Reste à Charge (dépend de Coût Référence et Total Subventions)
6. Taux (dépendent des totaux)

---

*Mesures DAX · ATLAS · Août 2026*
