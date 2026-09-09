import re


def normalize_spaces(value: str) -> str:
    """
    Normalise les espaces d'une chaîne de caractères.
    """
    if value is None:
        return ""

    return re.sub(r"\s+", " ", str(value)).strip()


def to_int(value):
    """
    Convertit une valeur monétaire ou numérique textuelle en entier.
    Les espaces classiques et insécables sont supprimés.
    """
    if value is None:
        return None

    cleaned = (
        str(value)
        .replace(" ", "")
        .replace("\u202f", "")
        .replace("\xa0", "")
        .strip()
    )

    if not cleaned:
        return None

    try:
        return int(cleaned)
    except ValueError:
        return None


def first_match(patterns, text, flags=re.I | re.S):
    """
    Teste plusieurs expressions régulières et renvoie
    le premier groupe capturé trouvé.
    """
    for pattern in patterns:
        match = re.search(pattern, text, flags)

        if match:
            return match.group(1)

    return None