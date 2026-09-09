from utils import first_match, to_int


def extract_budgets(full_text: str):
    """
    Extrait les montants budgétaires des différentes phases
    d'une opération ATLAS.

    Les phases actuellement reconnues sont :
        - PROGRAMME
        - AVP
        - PRO
        - MARCHE
    """

    programme_raw = first_match(
        [
            r"Enveloppe budgétaire.*?([\d\s\u202f]+)\s*€\s*HT\s*de travaux",
            r"budget.*?(?:FAISA|faisabilité).*?([\d\s\u202f]+)\s*€\s*HT",
        ],
        full_text,
    )

    avp_raw = first_match(
        [
            r"réévaluation.*?à\s+(?:environ\s+)?([\d\s\u202f]+)\s*€\s*HT\s*\(hors études",
            r"estimation.*?ramenée à\s+([\d\s\u202f]+)\s*€\s*HT\s*\(hors études",
        ],
        full_text,
    )

    pro_raw = first_match(
        [
            r"coût prévisionnel des travaux.*?à\s+([\d\s\u202f]+)\s*€\s*HT\s*\(hors études",
        ],
        full_text,
    )

    marche_raw = first_match(
        [
            r"Montant du marché de travaux notifié\s*:\s*([\d\s\u202f]+)\s*€\s*HT",
        ],
        full_text,
    )

    return {
        "PROGRAMME": to_int(programme_raw),
        "AVP": to_int(avp_raw),
        "PRO": to_int(pro_raw),
        "MARCHE": to_int(marche_raw),
    }