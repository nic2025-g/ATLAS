import re

from utils import normalize_spaces, to_int


def extract_lots(full_text: str, reference: str):
    """
    Extrait les lots de marché d'une opération ATLAS.

    Deux structures de marché sont reconnues :
    - groupement mandataire + co-traitant ;
    - entreprise seule.

    Un second passage extrait les dates de travaux :
    - date de démarrage issue de l'OS du lot ;
    - date de fin prévisionnelle ;
    - date de fin réelle, laissée à None si absente des sources.
    """

    lots = []

    # ------------------------------------------------------------------
    # Cas 1 : mandataire + co-traitant + montant total du lot
    # ------------------------------------------------------------------

    pattern_groupement = re.compile(
        r"Lot\s+(\d+)\s*"
        r"\(([^)]+)\)\s*:\s*"
        r"mandataire\s+(.+?)\s*"
        r"—\s*([\d\s\u202f]+)\s*€\s*HT\s*;\s*"
        r"co-traitant\s+(.+?)\s*"
        r"—\s*([\d\s\u202f]+)\s*€\s*HT\s*;\s*"
        r"total\s+lot\s+([\d\s\u202f]+)\s*€\s*HT",
        re.I,
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
                "date_debut_travaux": None,
                "date_fin_prevue": None,
                "date_fin_reelle": None,
            }
        )

    # ------------------------------------------------------------------
    # Cas 2 : entreprise seule
    # ------------------------------------------------------------------

    pattern_entreprise_seule = re.compile(
        r"Lot\s+(\d+)\s*"
        r"\(([^)]+)\)\s*:\s*"
        r"(.+?),\s*seule\s*"
        r"\(pas de co-traitant\)\s*"
        r"—\s*([\d\s\u202f]+)\s*€\s*HT",
        re.I,
    )

    for match in pattern_entreprise_seule.finditer(full_text):

        numero_lot = int(match.group(1))

        # Évite un doublon si le lot a déjà été extrait.
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
                "date_debut_travaux": None,
                "date_fin_prevue": None,
                "date_fin_reelle": None,
            }
        )

    # ------------------------------------------------------------------
    # Dates de travaux par lot
    # ------------------------------------------------------------------

    pattern_dates = re.compile(
        r"Lot\s+(\d+)\s*"
        r"\([^)]+\)\s*:\s*"
        r"OS\s+notifié\s+le\s+"
        r"(\d{2}/\d{2}/\d{4}),\s*"
        r"fin\s+prévisionnelle\s+"
        r"(\d{2}/\d{2}/\d{4})",
        re.I,
    )

    dates_par_lot = {}

    for match in pattern_dates.finditer(full_text):
        numero_lot = int(match.group(1))

        dates_par_lot[numero_lot] = {
            "date_debut_travaux": match.group(2),
            "date_fin_prevue": match.group(3),
        }

    # Rattachement des dates au lot correspondant.
    for lot in lots:
        dates = dates_par_lot.get(lot["numero_lot"])

        if dates:
            lot["date_debut_travaux"] = dates["date_debut_travaux"]
            lot["date_fin_prevue"] = dates["date_fin_prevue"]

    return lots