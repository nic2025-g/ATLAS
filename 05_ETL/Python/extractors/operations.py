import re

from utils import normalize_spaces


def extract_operation(meta: dict, full_text: str, reference: str):
    """
    Extrait les informations générales d'une opération ATLAS
    présentes dans les métadonnées du document source.
    """

    commune = meta.get(
        "Commune de rattachement",
        "",
    )

    complexite = meta.get(
        "Type de complexité",
        "",
    )

    nature = meta.get(
        "Nature de l'opération",
        "",
    )

    moa = meta.get(
        "Maître d'ouvrage (MOA)",
        "",
    )

    responsable_match = re.search(
        r"responsable de mission\s*:\s*([A-Z]\.\s*[A-Za-zÀ-ÿ\-]+)",
        full_text,
        re.I,
    )

    operation = {
        "reference_artelia": reference,
        "commune": commune,
        "nature": nature,
        "moe": "Artelia",
        "responsable_moe": (
            normalize_spaces(responsable_match.group(1))
            if responsable_match
            else ""
        ),
        "responsable_moa": moa,
        "complexite": complexite,
        "os_moe": meta.get(
            "Ordre de service (démarrage mission MOE)",
            "",
        ),
        "ouverture_fiche": meta.get(
            "Date d'ouverture de la fiche dossier",
            "",
        ),
    }

    return operation