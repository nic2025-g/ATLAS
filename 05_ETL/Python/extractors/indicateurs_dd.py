from utils import normalize_spaces


def extract_indicateurs_dd(doc):
    """
    Extrait les indicateurs de développement durable.

    Dans les documents pilotes ATLAS, les indicateurs DD
    sont stockés dans le troisième tableau Word.
    """

    indicateurs = []

    if len(doc.tables) <= 2:
        return indicateurs

    for row in doc.tables[2].rows[1:]:

        cells = [
            normalize_spaces(cell.text)
            for cell in row.cells
        ]

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

    return indicateurs