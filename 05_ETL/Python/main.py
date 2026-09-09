import sys
from pathlib import Path

import pandas as pd

from extractors.document import read_document
from extractors.operations import extract_operation
from extractors.budgets import extract_budgets
from extractors.lots import extract_lots
from extractors.subventions import extract_subventions
from extractors.indicateurs_dd import extract_indicateurs_dd
from validators.validations import validate_outputs


# ===========================================================================
# CONFIGURATION
# ===========================================================================

PYTHON_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PYTHON_DIR.parent.parent

OUTPUT_DIR = PYTHON_DIR / "raw"

FILES = {
    "4243946_2301": (
        PROJECT_ROOT
        / "04_Donnees"
        / "Projet1_Les_Angles"
        / "notes_brutes"
        / "Notes_brutes_Projet_1_Les_Angles.docx"
    ),
    "4243946_2202": (
        PROJECT_ROOT
        / "04_Donnees"
        / "Projet2_Avignon"
        / "notes_brutes"
        / "Notes_brutes_Projet_2_Avignon.docx"
    ),
    "4243946_2203": (
        PROJECT_ROOT
        / "04_Donnees"
        / "Projet3_Entraigues"
        / "notes_brutes"
        / "Notes_brutes_Projet_3_Entraigues.docx"
    ),
    "4243946_2201": (
        PROJECT_ROOT
        / "04_Donnees"
        / "Projet4_Morieres"
        / "notes_brutes"
        / "Notes_brutes_Projet_4_Morieres.docx"
    ),
}


# ===========================================================================
# EXECUTION PRINCIPALE
# ===========================================================================

def main():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_ops = []
    all_budgets = []
    all_lots = []
    all_subventions = []
    all_indicateurs = []

    # -----------------------------------------------------------------------
    # Lecture des quatre opérations pilotes
    # -----------------------------------------------------------------------

    for reference, path in FILES.items():

        if not path.exists():
            print(f"ERREUR - fichier introuvable : {path}")
            sys.exit(1)

        print(f"Lecture : {path.name}")

        # Une seule lecture physique du document.
        document = read_document(path)

        doc = document["doc"]
        full_text = document["full_text"]
        meta = document["meta"]

        # -------------------------------------------------------------------
        # Extraction par domaine métier
        # -------------------------------------------------------------------

        operation = extract_operation(
            meta,
            full_text,
            reference,
        )

        budgets = extract_budgets(
            full_text,
        )

        lots = extract_lots(
            full_text,
            reference,
        )

        subventions = extract_subventions(
            full_text,
        )

        indicateurs = extract_indicateurs_dd(
            doc,
        )

        # -------------------------------------------------------------------
        # Operations
        # -------------------------------------------------------------------

        all_ops.append(operation)

        # -------------------------------------------------------------------
        # Budgets
        # -------------------------------------------------------------------

        for phase, montant in budgets.items():

            all_budgets.append(
                {
                    "reference_artelia": reference,
                    "phase": phase,
                    "montant_ht": montant,
                }
            )

        # -------------------------------------------------------------------
        # Lots
        # -------------------------------------------------------------------

        for lot in lots:

            all_lots.append(
                {
                    "reference_artelia": reference,
                    **lot,
                }
            )

        # -------------------------------------------------------------------
        # Subventions
        # -------------------------------------------------------------------

        for subvention in subventions:

            all_subventions.append(
                {
                    "reference_artelia": reference,
                    "commune": operation["commune"],
                    **subvention,
                }
            )

        # -------------------------------------------------------------------
        # Indicateurs DD
        # -------------------------------------------------------------------

        for indicateur in indicateurs:

            all_indicateurs.append(
                {
                    "reference_artelia": reference,
                    "commune": operation["commune"],
                    **indicateur,
                }
            )

    # ===========================================================================
    # CREATION DES DATAFRAMES
    # ===========================================================================

    df_ops = pd.DataFrame(all_ops)
    df_budgets = pd.DataFrame(all_budgets)
    df_lots = pd.DataFrame(all_lots)
    df_subs = pd.DataFrame(all_subventions)
    df_ind = pd.DataFrame(all_indicateurs)

    # ===========================================================================
    # VALIDATION
    # ===========================================================================

    errors = validate_outputs(
        df_ops,
        df_budgets,
        df_lots,
        df_subs,
        df_ind,
        expected_refs=FILES.keys(),
    )

    # ===========================================================================
    # EXPORT CSV
    # ===========================================================================

    df_ops.to_csv(
        OUTPUT_DIR / "raw_operations.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df_budgets.to_csv(
        OUTPUT_DIR / "raw_budgets.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df_lots.to_csv(
        OUTPUT_DIR / "raw_lots.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df_subs.to_csv(
        OUTPUT_DIR / "raw_subventions.csv",
        index=False,
        encoding="utf-8-sig",
    )

    df_ind.to_csv(
        OUTPUT_DIR / "raw_indicateurs_dd.csv",
        index=False,
        encoding="utf-8-sig",
    )

    # ===========================================================================
    # COMPTE-RENDU
    # ===========================================================================

    print("\nCSV générés :")
    print(f"  operations       : {len(df_ops)}")
    print(f"  budgets          : {len(df_budgets)}")
    print(f"  lots             : {len(df_lots)}")
    print(f"  subventions      : {len(df_subs)}")
    print(f"  indicateurs DD   : {len(df_ind)}")

    if errors:

        print("\nATTENTION - contrôles à vérifier :")

        for error in errors:
            print(f"  - {error}")

        sys.exit(2)

    print("\nOK - extraction terminée sans erreur structurelle.")


if __name__ == "__main__":
    main()