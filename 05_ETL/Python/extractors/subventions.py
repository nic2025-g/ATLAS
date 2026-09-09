import re

from utils import normalize_spaces, to_int


def extract_subventions(full_text: str):
    """
    Extrait les subventions mentionnées dans le document.

    Le numéro de lot sert uniquement à localiser l'information
    dans le document source. La subvention reste rattachée
    à l'opération dans le modèle ATLAS.
    """

    subventions = []

    for lot_match in re.finditer(
        r"Lot\s+(\d+)\s*:\s*([^\n]+)",
        full_text,
        re.I,
    ):

        content = normalize_spaces(lot_match.group(2))

        if "aucune subvention" in content.lower():
            continue

        for segment in content.split(";"):

            segment = segment.strip()

            # Cas :
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

                # Cas simple :
                # subvention 50 000 € (Département)
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

    return subventions