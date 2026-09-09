def validate_outputs(
    df_ops,
    df_budgets,
    df_lots,
    df_subs,
    df_ind,
    expected_refs,
):
    """
    Effectue les contrôles structurels des données extraites.

    Vérifie notamment :
    - le nombre attendu de lots ;
    - l'unicité des opérations ;
    - la cohérence somme des lots = montant MARCHE ;
    - l'absence de références inconnues ;
    - le nombre d'opérations ;
    - le nombre de lignes budgétaires.
    """

    errors = []

    expected_refs = set(expected_refs)
    expected_operations = len(expected_refs)

    # --------------------------------------------------------------
    # Nombre de lots : 3 par opération pilote
    # --------------------------------------------------------------

    expected_lot_rows = expected_operations * 3

    if len(df_lots) != expected_lot_rows:
        errors.append(
            f"raw_lots.csv: {len(df_lots)} lignes "
            f"au lieu de {expected_lot_rows}"
        )

    # --------------------------------------------------------------
    # Unicité des opérations
    # --------------------------------------------------------------

    if df_ops["reference_artelia"].duplicated().any():
        errors.append(
            "Références d'opération dupliquées dans raw_operations.csv"
        )

    # --------------------------------------------------------------
    # Somme des lots = montant du marché
    # --------------------------------------------------------------

    if not df_lots.empty and not df_budgets.empty:

        lots_totaux = (
            df_lots
            .groupby("reference_artelia")["montant_marche_ht"]
            .sum()
        )

        budgets_marche = (
            df_budgets[
                df_budgets["phase"] == "MARCHE"
            ]
            .set_index("reference_artelia")["montant_ht"]
        )

        for reference in expected_refs:

            total_lots = lots_totaux.get(reference, 0)
            montant_marche = budgets_marche.get(reference)

            if montant_marche is None:
                errors.append(
                    f"{reference}: montant MARCHE absent"
                )

            elif total_lots != montant_marche:
                errors.append(
                    f"{reference}: somme des lots = {total_lots} "
                    f"mais montant MARCHE = {montant_marche}"
                )

    # --------------------------------------------------------------
    # Références inconnues
    # --------------------------------------------------------------

    tables = {
        "budgets": df_budgets,
        "lots": df_lots,
        "subventions": df_subs,
        "indicateurs": df_ind,
    }

    for name, df in tables.items():

        if not df.empty and "reference_artelia" in df.columns:

            unknown = (
                set(df["reference_artelia"].dropna())
                - expected_refs
            )

            if unknown:
                errors.append(
                    f"{name}: références inconnues {sorted(unknown)}"
                )

    # --------------------------------------------------------------
    # Nombre d'opérations
    # --------------------------------------------------------------

    if len(df_ops) != expected_operations:
        errors.append(
            f"raw_operations.csv: {len(df_ops)} lignes "
            f"au lieu de {expected_operations}"
        )

    # --------------------------------------------------------------
    # Nombre de budgets : 4 phases par opération
    # --------------------------------------------------------------

    expected_budget_rows = expected_operations * 4

    if len(df_budgets) != expected_budget_rows:
        errors.append(
            f"raw_budgets.csv: {len(df_budgets)} lignes "
            f"au lieu de {expected_budget_rows}"
        )

    return errors