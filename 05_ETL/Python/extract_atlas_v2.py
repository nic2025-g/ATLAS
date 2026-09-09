"""
ATLAS - Extraction des données métier vers des fichiers CSV

Objectif
--------
Ce script constitue la première étape du pipeline Data Engineering ATLAS.

Il lit les quatre documents Word utilisés comme sources métier,
extrait les informations utiles au modèle V2, puis génère cinq fichiers CSV :

    - raw_operations.csv
    - raw_budgets.csv
    - raw_lots.csv
    - raw_subventions.csv
    - raw_indicateurs_dd.csv

Ces fichiers CSV pourront ensuite être chargés dans PostgreSQL avec Airbyte,
puis transformés avec dbt avant d'être utilisés dans Power BI.

Important
---------
Le script n'invente pas les données absentes.
Lorsqu'une information n'est pas trouvée dans la source, elle reste vide
ou prend la valeur None.
"""

# ---------------------------------------------------------------------------
# IMPORTS
# ---------------------------------------------------------------------------

# re : permet d'utiliser les expressions régulières pour rechercher
#      des informations dans le texte des documents Word.
import re

# sys : permet notamment d'arrêter proprement le programme en cas d'erreur.
import sys

# Path : permet de manipuler les chemins de fichiers de manière fiable,
#        indépendamment du dossier depuis lequel le script est exécuté.
from pathlib import Path

# python-docx : permet de lire le contenu des fichiers .docx.
import docx

# pandas : utilisé ici uniquement pour construire les tables finales
#          et les exporter en CSV.
import pandas as pd


# ===========================================================================
# 1. CONFIGURATION DES CHEMINS
# ===========================================================================

# Dossier dans lequel se trouve ce fichier Python.
# Ici : C:\Users\Nicolas\STAGE\ATLAS\05_ETL\Python
SCRIPT_DIR = Path(__file__).resolve().parent

# Racine du dépôt ATLAS.
# On remonte de Python -> 05_ETL -> ATLAS
REPO_ROOT = Path(__file__).resolve().parents[2]

# Dossier dans lequel seront générés les fichiers CSV.
# Ici : C:\Users\Nicolas\STAGE\ATLAS\05_ETL\Python\raw
OUTPUT_DIR = SCRIPT_DIR / "raw"

# Fichiers Word sources des quatre opérations pilotes.
FILES = {
    "4243946_2301": REPO_ROOT
    / "04_Donnees"
    / "Projet1_Les_Angles"
    / "notes_brutes"
    / "Notes_brutes_Projet_1_Les_Angles.docx",

    "4243946_2202": REPO_ROOT
    / "04_Donnees"
    / "Projet2_Avignon"
    / "notes_brutes"
    / "Notes_brutes_Projet_2_Avignon.docx",

    "4243946_2203": REPO_ROOT
    / "04_Donnees"
    / "Projet3_Entraigues"
    / "notes_brutes"
    / "Notes_brutes_Projet_3_Entraigues.docx",

    "4243946_2201": REPO_ROOT
    / "04_Donnees"
    / "Projet4_Morieres"
    / "notes_brutes"
    / "Notes_brutes_Projet_4_Morieres.docx",
}

# ===========================================================================
# 2. FONCTIONS UTILITAIRES
# ===========================================================================

def normalize_spaces(value: str) -> str:
    """
    Nettoie les espaces présents dans une valeur texte.

    Les documents Word peuvent contenir plusieurs types d'espaces,
    notamment des espaces insécables ou des espaces fines.

    Exemple :
        "1  850 000 €"  ->  "1 850 000 €"

    Cette normalisation facilite ensuite les recherches avec des regex.
    """
    if value is None:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(value).replace("\u202f", " ")
    ).strip()


def to_int(value):
    """
    Convertit une valeur monétaire ou numérique en entier.

    Exemples :
        "1 850 000 €" -> 1850000
        "250 000"     -> 250000
        ""            -> None

    Toutes les informations non numériques sont supprimées.
    """
    if value is None:
        return None

    value = normalize_spaces(value)

    # On conserve uniquement les chiffres.
    digits = re.sub(r"[^\d]", "", value)

    # Si aucun chiffre n'est trouvé, on retourne None
    # plutôt que d'inventer une valeur égale à zéro.
    return int(digits) if digits else None


def first_match(patterns, text, flags=re.I | re.S):
    """
    Teste plusieurs expressions régulières sur un même texte
    et renvoie la première valeur trouvée.

    Cette fonction permet de prendre en compte plusieurs formulations
    possibles dans les documents Word.

    Exemple :
        une même information AVP peut être décrite avec
        "réévaluation à..." ou "estimation ramenée à...".
    """
    for pattern in patterns:
        match = re.search(pattern, text, flags)

        if match:
            return match.group(1)

    return None


def get_table_as_dict(doc, table_index=0):
    """
    Transforme un tableau Word de type clé / valeur en dictionnaire Python.

    Exemple dans le document :

        Commune de rattachement | Avignon
        Type de complexité      | Complexe

    devient :

        {
            "Commune de rattachement": "Avignon",
            "Type de complexité": "Complexe"
        }

    Si le tableau demandé n'existe pas, la fonction retourne
    simplement un dictionnaire vide.
    """
    if len(doc.tables) <= table_index:
        return {}

    result = {}

    for row in doc.tables[table_index].rows:
        # Une ligne doit contenir au minimum une clé et une valeur.
        if len(row.cells) < 2:
            continue

        key = normalize_spaces(row.cells[0].text)
        value = normalize_spaces(row.cells[1].text)

        if key:
            result[key] = value

    return result


# ===========================================================================
# 3. EXTRACTION D'UN DOCUMENT WORD
# ===========================================================================

def parse_doc(path: Path, reference: str):
    """
    Lit un document Word correspondant à une opération
    et extrait les informations utiles au modèle V2.

    La fonction renvoie un dictionnaire contenant cinq familles de données :

        - operation
        - budgets
        - lots
        - subventions
        - indicateurs
    """

    # -----------------------------------------------------------------------
    # 3.1 Lecture du fichier Word
    # -----------------------------------------------------------------------

    doc = docx.Document(path)

    # On récupère tous les paragraphes non vides.
    paragraphs = [
        normalize_spaces(p.text)
        for p in doc.paragraphs
        if p.text.strip()
    ]

    # On récupère également le contenu des tableaux.
    # Cela permet de rechercher une information même si elle n'est pas
    # située dans un paragraphe classique.
    table_text = []

    for table in doc.tables:
        for row in table.rows:
            table_text.append(
                " | ".join(
                    normalize_spaces(cell.text)
                    for cell in row.cells
                )
            )

    # Tous les textes du document sont regroupés dans une seule chaîne.
    # Cette chaîne sera utilisée pour les recherches par expressions régulières.
    full_text = "\n".join(paragraphs + table_text)

    # Le premier tableau est utilisé comme tableau de métadonnées.
    meta = get_table_as_dict(doc, 0)


    # -----------------------------------------------------------------------
    # 3.2 Extraction des budgets
    # -----------------------------------------------------------------------

    # Le budget FAISA peut être décrit avec plusieurs formulations.
    # On teste donc plusieurs expressions régulières.
    faisa_raw = first_match(
        [
            r"Enveloppe budgétaire.*?([\d\s\u202f]+)\s*€\s*HT\s*de travaux",
            r"budget.*?(?:FAISA|faisabilité).*?([\d\s\u202f]+)\s*€\s*HT",
        ],
        full_text,
    )

    # Même principe pour le budget AVP.
    avp_raw = first_match(
        [
            r"réévaluation.*?à\s+(?:environ\s+)?([\d\s\u202f]+)\s*€\s*HT\s*\(hors études",
            r"estimation.*?ramenée à\s+([\d\s\u202f]+)\s*€\s*HT\s*\(hors études",
        ],
        full_text,
    )

    # Budget de la phase PRO.
    pro_raw = first_match(
        [
            r"coût prévisionnel des travaux.*?à\s+([\d\s\u202f]+)\s*€\s*HT\s*\(hors études",
        ],
        full_text,
    )

    # Montant du marché notifié.
    marche_raw = first_match(
        [
            r"Montant du marché de travaux notifié\s*:\s*([\d\s\u202f]+)\s*€\s*HT",
        ],
        full_text,
    )

    # Les valeurs sont converties en entiers afin de faciliter
    # les calculs ultérieurs dans PostgreSQL, dbt et Power BI.
    budgets = {
        "PROGRAMME": to_int(faisa_raw),
        "AVP": to_int(avp_raw),
        "PRO": to_int(pro_raw),
        "MARCHE": to_int(marche_raw),
    }


    # -----------------------------------------------------------------------
    # 3.3 Extraction des indicateurs de développement durable
    # -----------------------------------------------------------------------

    indicateurs = []

    # Dans les fichiers pilotes, les indicateurs DD se trouvent
    # dans le troisième tableau du document.
    #
    # On vérifie d'abord que ce tableau existe pour éviter une erreur.
    if len(doc.tables) > 2:

        # La première ligne correspond normalement aux en-têtes,
        # d'où l'utilisation de rows[1:].
        for row in doc.tables[2].rows[1:]:

            cells = [
                normalize_spaces(cell.text)
                for cell in row.cells
            ]

            # Si aucune colonne exploitable n'est trouvée,
            # la ligne est ignorée.
            if len(cells) < 3 or not cells[0]:
                continue

            indicateurs.append(
                {
                    "indicateur": cells[0],
                    "valeur_cible": cells[1] if len(cells) > 1 else "",
                    "valeur_constatee": cells[2] if len(cells) > 2 else "",
                    "bilan": cells[3] if len(cells) > 3 else "",
                }
            )


    # -----------------------------------------------------------------------
    # 3.4 Extraction des subventions
    # -----------------------------------------------------------------------

    subventions = []

    # Dans les notes métier, certaines subventions apparaissent
    # dans des paragraphes proches des lots.
    #
    # Cependant, dans le modèle V2 validé, une subvention est rattachée
    # à l'opération et non au lot.
    #
    # Le numéro de lot sert donc uniquement à repérer la donnée dans
    # le document source : il n'est pas exporté dans raw_subventions.csv.
    for lot_match in re.finditer(
        r"Lot\s+(\d+)\s*:\s*([^\n]+)",
        full_text,
        re.I
    ):

        content = normalize_spaces(lot_match.group(2))

        # Si la source indique explicitement qu'il n'existe aucune subvention,
        # on ne crée aucune ligne.
        if "aucune subvention" in content.lower():
            continue

        # Plusieurs subventions peuvent être séparées par des points-virgules.
        for segment in content.split(";"):

            segment = segment.strip()

            # Exemple de structure recherchée :
            #
            # AEP 115 000 €
            # (Département 85 000 € + État-DETR 30 000 €)
            outer = re.match(
                r"([A-ZÀ-Ý0-9/\-]+)\s+[\d\s]+€\s*\((.*)\)",
                segment,
                re.I,
            )

            if outer:
                type_subvention = normalize_spaces(outer.group(1))
                inside = outer.group(2)

                # On extrait ensuite chaque financeur et son montant.
                for sm in re.finditer(
                    r"([A-Za-zÀ-ÿ0-9\-\s/]+?)\s+([\d\s]+)\s*€",
                    inside,
                ):

                    organisme = normalize_spaces(sm.group(1))
                    montant = to_int(sm.group(2))

                    if organisme and montant is not None:
                        subventions.append(
                            {
                                "type_subvention": type_subvention,
                                "organisme": organisme,
                                "montant": montant,
                            }
                        )

            else:
                # Cas plus simple :
                # "subvention 50 000 € (Département)"
                simple = re.search(
                    r"subvention.*?(\d[\d\s]+)\s*€\s*\(([^)]+)\)",
                    segment,
                    re.I,
                )

                if simple:
                    subventions.append(
                        {
                            "type_subvention": "Aménagement",
                            "organisme": normalize_spaces(simple.group(2)),
                            "montant": to_int(simple.group(1)),
                        }
                    )


    # -----------------------------------------------------------------------
    # 3.5 Extraction des lots du marché
    # -----------------------------------------------------------------------

    lots = []

    # -------------------------------------------------------------------
    # Cas 1 : lot avec mandataire + co-traitant + total de lot
    # -------------------------------------------------------------------

    pattern_groupement = re.compile(
        r"Lot\s+(\d+)\s*"
        r"\(([^)]+)\)\s*:\s*"
        r"mandataire\s+(.+?)\s*"
        r"—\s*([\d\s\u202f]+)\s*€\s*HT\s*;\s*"
        r"co-traitant\s+(.+?)\s*"
        r"—\s*([\d\s\u202f]+)\s*€\s*HT\s*;\s*"
        r"total\s+lot\s+([\d\s\u202f]+)\s*€\s*HT",
        re.I
    )

    for match in pattern_groupement.finditer(full_text):

        numero_lot = int(match.group(1))
        libelle_lot = normalize_spaces(match.group(2))

        mandataire = normalize_spaces(match.group(3))
        cotraitant = normalize_spaces(match.group(5))

        montant_total = to_int(match.group(7))

        lots.append(
            {
                "lot_id_source": f"{reference}_L{numero_lot}",
                "numero_lot": numero_lot,
                "libelle_lot": libelle_lot,
                "montant_marche_ht": montant_total,
                "entreprise_mandataire": mandataire,
                "cotraitants": cotraitant,
                "montant_paye": None,
            }
        )


    # -------------------------------------------------------------------
    # Cas 2 : lot attribué à une entreprise seule
    # -------------------------------------------------------------------

    pattern_entreprise_seule = re.compile(
        r"Lot\s+(\d+)\s*"
        r"\(([^)]+)\)\s*:\s*"
        r"(.+?),\s*seule\s*"
        r"\(pas de co-traitant\)\s*"
        r"—\s*([\d\s\u202f]+)\s*€\s*HT",
        re.I
    )

    for match in pattern_entreprise_seule.finditer(full_text):

        numero_lot = int(match.group(1))

        # Evite de créer un doublon si le lot a déjà été trouvé
        if any(
            lot["numero_lot"] == numero_lot
            for lot in lots
        ):
            continue

        libelle_lot = normalize_spaces(match.group(2))
        mandataire = normalize_spaces(match.group(3))
        montant_total = to_int(match.group(4))

        lots.append(
            {
                "lot_id_source": f"{reference}_L{numero_lot}",
                "numero_lot": numero_lot,
                "libelle_lot": libelle_lot,
                "montant_marche_ht": montant_total,
                "entreprise_mandataire": mandataire,
                "cotraitants": "",
                "montant_paye": None,
            }
        )


    # -----------------------------------------------------------------------
    # 3.6 Extraction des informations générales de l'opération
    # -----------------------------------------------------------------------

    commune = meta.get(
        "Commune de rattachement",
        ""
    )

    complexite = meta.get(
        "Type de complexité",
        ""
    )

    # Exemple recherché :
    # responsable de mission : C. Laffile
    responsable_match = re.search(
        r"responsable de mission\s*:\s*([A-Z]\.\s*[A-Za-zÀ-ÿ\-]+)",
        full_text,
        re.I,
    )

    operation = {
        "reference_artelia": reference,
        "commune": commune,
        "complexite": complexite,
        "moe": "Artelia",

        "responsable_moe": (
            normalize_spaces(responsable_match.group(1))
            if responsable_match
            else ""
        ),

        "os_moe": meta.get(
            "Ordre de service (démarrage mission MOE)",
            ""
        ),

        "ouverture_fiche": meta.get(
            "Date d'ouverture de la fiche dossier",
            ""
        ),
    }

    # La fonction renvoie toutes les familles de données extraites.
    return {
        "operation": operation,
        "budgets": budgets,
        "lots": lots,
        "subventions": subventions,
        "indicateurs": indicateurs,
    }


# ===========================================================================
# 4. CONTROLES DE QUALITE
# ===========================================================================

def validate_outputs(
    df_ops,
    df_budgets,
    df_lots,
    df_subs,
    df_ind
):
    """
    Effectue quelques contrôles simples avant d'utiliser les CSV.

    L'objectif n'est pas encore de réaliser tous les tests de qualité
    possibles : une partie de ces contrôles sera ensuite prise en charge
    par dbt.

    Ici, on vérifie surtout :
        - l'unicité des références d'opération ;
        - la présence des quatre opérations ;
        - la présence des quatre phases budgétaires par opération ;
        - l'absence de références inconnues.
    """

    errors = []
    
    # -----------------------------------------------------------------------
    # Vérification du nombre de lots
    # -----------------------------------------------------------------------

    expected_lot_rows = len(FILES) * 3

    if len(df_lots) != expected_lot_rows:
        errors.append(
            f"raw_lots.csv: {len(df_lots)} lignes "
            f"au lieu de {expected_lot_rows}"
        )

    # -----------------------------------------------------------------------
    # Vérification de l'unicité des opérations
    # -----------------------------------------------------------------------

    if df_ops["reference_artelia"].duplicated().any():
        errors.append(
            "Références d'opération dupliquées dans raw_operations.csv"
        )

    # Ensemble des références attendues.
    expected_refs = set(FILES.keys())
    
    # -----------------------------------------------------------------------
    # Vérification de la cohérence :
    # somme des lots = montant du marché
    # -----------------------------------------------------------------------

    if not df_lots.empty and not df_budgets.empty:

        # Montant total des lots par opération
        lots_totaux = (
            df_lots
            .groupby("reference_artelia")["montant_marche_ht"]
            .sum()
        )

        # Montant MARCHE extrait dans la table budgets
        budgets_marche = (
            df_budgets[
                df_budgets["phase"] == "MARCHE"
            ]
            .set_index("reference_artelia")["montant_ht"]
        )

        for reference in FILES.keys():

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

    # -----------------------------------------------------------------------
    # Vérification des références dans toutes les tables
    # -----------------------------------------------------------------------

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

    # -----------------------------------------------------------------------
    # Vérification du nombre d'opérations
    # -----------------------------------------------------------------------

    if len(df_ops) != len(FILES):

        errors.append(
            f"raw_operations.csv: {len(df_ops)} lignes "
            f"au lieu de {len(FILES)}"
        )

    # -----------------------------------------------------------------------
    # Vérification du nombre de lignes budgétaires
    # -----------------------------------------------------------------------
    #
    # 4 opérations x 4 phases :
    # FAISA, AVP, PRO, MARCHE
    #
    expected_budget_rows = len(FILES) * 4

    if len(df_budgets) != expected_budget_rows:

        errors.append(
            f"raw_budgets.csv: {len(df_budgets)} lignes "
            f"au lieu de {expected_budget_rows}"
        )

    return errors


# ===========================================================================
# 5. EXECUTION PRINCIPALE
# ===========================================================================

def main():
    """
    Fonction principale du script.

    Elle :
        1. crée le dossier de sortie ;
        2. parcourt les quatre documents Word ;
        3. appelle parse_doc() ;
        4. construit les cinq tables ;
        5. effectue les contrôles ;
        6. exporte les CSV.
    """

    # Création du dossier raw s'il n'existe pas déjà.
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Ces listes vont accumuler les lignes extraites
    # avant leur transformation en DataFrames pandas.
    all_ops = []
    all_budgets = []
    all_lots = []
    all_subventions = []
    all_indicateurs = []

    # -----------------------------------------------------------------------
    # Parcours des quatre opérations pilotes
    # -----------------------------------------------------------------------

    for reference, path in FILES.items():

        # On arrête immédiatement le programme si une source manque.
        # Il est préférable de signaler clairement une erreur plutôt que
        # de générer silencieusement un jeu de données incomplet.
        if not path.exists():

            print(
                f"ERREUR - fichier introuvable : {path}"
            )

            sys.exit(1)

        print(
            f"Lecture : {path.name}"
        )

        # Extraction du document.
        data = parse_doc(
            path,
            reference
        )

        # -------------------------------------------------------------------
        # Table opérations
        # -------------------------------------------------------------------

        all_ops.append(
            data["operation"]
        )

        # -------------------------------------------------------------------
        # Table budgets
        # -------------------------------------------------------------------
        #
        # La table est volontairement verticale :
        #
        # référence | phase  | montant
        # ----------|--------|---------
        # 2301      | FAISA  | ...
        # 2301      | AVP    | ...
        # 2301      | PRO    | ...
        # 2301      | MARCHE | ...
        #
        # Cette structure sera pratique pour dbt et Power BI.
        for phase, montant in data["budgets"].items():

            all_budgets.append(
                {
                    "reference_artelia": reference,
                    "phase": phase,
                    "montant_ht": montant,
                }
            )

        # -------------------------------------------------------------------
        # Table lots
        # -------------------------------------------------------------------

        for lot in data["lots"]:

            all_lots.append(
                {
                    "reference_artelia": reference,
                    **lot,
                }
            )

        # -------------------------------------------------------------------
        # Table subventions
        # -------------------------------------------------------------------
        #
        # Les subventions sont rattachées à l'opération.
        for subvention in data["subventions"]:

            all_subventions.append(
                {
                    "reference_artelia": reference,
                    "commune": data["operation"]["commune"],
                    **subvention,
                }
            )

        # -------------------------------------------------------------------
        # Table indicateurs DD
        # -------------------------------------------------------------------

        for indicateur in data["indicateurs"]:

            all_indicateurs.append(
                {
                    "reference_artelia": reference,
                    "commune": data["operation"]["commune"],
                    **indicateur,
                }
            )


    # ===========================================================================
    # 6. CREATION DES DATAFRAMES
    # ===========================================================================

    # Chaque liste devient une table pandas.
    df_ops = pd.DataFrame(all_ops)
    df_budgets = pd.DataFrame(all_budgets)
    df_lots = pd.DataFrame(all_lots)
    df_subs = pd.DataFrame(all_subventions)
    df_ind = pd.DataFrame(all_indicateurs)


    # ===========================================================================
    # 7. VALIDATION DES DONNEES
    # ===========================================================================

    errors = validate_outputs(
        df_ops,
        df_budgets,
        df_lots,
        df_subs,
        df_ind
    )


    # ===========================================================================
    # 8. EXPORT DES CSV
    # ===========================================================================

    # utf-8-sig permet notamment une ouverture correcte des caractères accentués
    # dans Excel sous Windows.
    df_ops.to_csv(
        OUTPUT_DIR / "raw_operations.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_budgets.to_csv(
        OUTPUT_DIR / "raw_budgets.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_lots.to_csv(
        OUTPUT_DIR / "raw_lots.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_subs.to_csv(
        OUTPUT_DIR / "raw_subventions.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_ind.to_csv(
        OUTPUT_DIR / "raw_indicateurs_dd.csv",
        index=False,
        encoding="utf-8-sig"
    )


    # ===========================================================================
    # 9. COMPTE-RENDU D'EXECUTION
    # ===========================================================================

    print("\nCSV générés :")

    print(
        f"  operations       : {len(df_ops)}"
    )

    print(
        f"  budgets          : {len(df_budgets)}"
    )

    print(
        f"  lots             : {len(df_lots)}"
    )

    print(
        f"  subventions      : {len(df_subs)}"
    )

    print(
        f"  indicateurs DD   : {len(df_ind)}"
    )

    # Si les contrôles ont détecté un problème,
    # les CSV sont tout de même générés afin de pouvoir les examiner,
    # mais le script retourne un code d'erreur.
    if errors:

        print(
            "\nATTENTION - contrôles à vérifier :"
        )

        for error in errors:

            print(
                f"  - {error}"
            )

        sys.exit(2)

    # Si aucune erreur structurelle n'a été détectée.
    print(
        "\nOK - extraction terminée sans erreur structurelle."
    )


# ===========================================================================
# 10. POINT D'ENTREE DU SCRIPT
# ===========================================================================

# Cette condition signifie :
#
# "Exécuter main() uniquement lorsque ce fichier est lancé directement."
#
# Elle permet également d'importer les fonctions de ce fichier
# dans un futur script de test sans déclencher automatiquement l'extraction.
if __name__ == "__main__":
    main()
