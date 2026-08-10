"""
ATLAS — Script de nettoyage et structuration des données
Projet : Communauté de Communes du Grand Avignon
Auteur : BAMANIA Nathanael Nicolas — Stage Data Engineering 2026

Ce script transforme les données brutes des projets (Excel généré à partir des prises de note en word) en DataFrames
structurés prêts pour l'ingestion dans PostgreSQL via Airbyte ou chargement direct.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# ─── DONNÉES DES 4 PROJETS PILOTES ───────────────────────────────────────────
# Source : notes brutes transmises par l'encadrant (Dominique VOLOT)

# ── 1. OPÉRATIONS ──────────────────────────────────────────────────────────
operations_raw = [
    {
        "numero_ref_artelia": "4243946_2301",
        "ref_interne":        "ph_test-V2 – Projet 1",
        "intitule":           "Requalification av. de Verdun et place du 8-Mai",
        "commune":            "Les Angles",
        "complexite":         "Moyenne",
        "nom_moe":            "Artelia",
        "responsable_moe":    "O. Mozol",
        "responsable_moa":    "S. Chabert",
        "date_os_moe":        "2021-02-01",
        "date_ouverture_fiche": "2021-02-07",
    },
    {
        "numero_ref_artelia": "4243946_2202",
        "ref_interne":        "ph_test-V2 – Projet 2",
        "intitule":           "Réaménagement rue des Marronniers",
        "commune":            "Avignon",
        "complexite":         "Faible",
        "nom_moe":            "Artelia",
        "responsable_moe":    "C. Laffile",
        "responsable_moa":    "J. Ferrand",
        "date_os_moe":        "2022-06-01",
        "date_ouverture_fiche": "2022-06-10",
    },
    {
        "numero_ref_artelia": "4243946_2203",
        "ref_interne":        "ph_test-V2 – Projet 3",
        "intitule":           "Requalification quais de la Sorgue et place du Marché",
        "commune":            "Entraigues-sur-la-Sorgue",
        "complexite":         "Élevée",
        "nom_moe":            "Artelia",
        "responsable_moe":    "C. Laffile",
        "responsable_moa":    "L. Bressy",
        "date_os_moe":        "2023-02-01",
        "date_ouverture_fiche": "2023-02-08",
    },
    {
        "numero_ref_artelia": "4243946_2201",
        "ref_interne":        "ph_test-V2 – Projet 4",
        "intitule":           "Requalification av. du Grès et place des Micocouliers",
        "commune":            "Morières-lès-Avignon",
        "complexite":         "Moyenne",
        "nom_moe":            "Artelia",
        "responsable_moe":    "C. Laffile",
        "responsable_moa":    "T. Roussel",
        "date_os_moe":        "2023-05-18",
        "date_ouverture_fiche": "2023-06-01",
    },
]

# ── 2. BUDGETS PAR PHASE ──────────────────────────────────────────────────
budgets_raw = [
    # Projet 1 — Les Angles
    {"ref": "4243946_2301", "phase": "AVP", "budget_avp": 1_980_000, "date_phase": "2021-05-25"},
    {"ref": "4243946_2301", "phase": "PRO", "budget_pro": 2_050_000, "date_phase": "2021-10-10"},
    {"ref": "4243946_2301", "phase": "ACT", "prix_marche": 1_950_000, "date_phase": "2022-04-28"},
    {"ref": "4243946_2301", "phase": "DET", "date_debut": "2022-05-01", "date_fin_prevue": "2023-03-20"},

    # Projet 2 — Avignon
    {"ref": "4243946_2202", "phase": "AVP", "budget_avp": 1_820_000, "date_phase": "2022-09-15"},
    {"ref": "4243946_2202", "phase": "PRO", "budget_pro": 1_850_000, "date_phase": "2022-12-25"},
    {"ref": "4243946_2202", "phase": "ACT", "prix_marche": 1_790_000, "date_phase": "2023-07-08"},
    {"ref": "4243946_2202", "phase": "DET", "date_debut": "2023-07-20", "date_fin_prevue": "2024-12-20"},

    # Projet 3 — Entraigues
    {"ref": "4243946_2203", "phase": "AVP", "budget_avp": 1_980_000, "date_phase": "2023-05-20"},
    {"ref": "4243946_2203", "phase": "PRO", "budget_pro": 2_050_000, "date_phase": "2023-09-01"},
    {"ref": "4243946_2203", "phase": "ACT", "prix_marche": 2_180_000, "date_phase": "2024-02-05"},
    {"ref": "4243946_2203", "phase": "DET", "date_debut": "2024-02-20", "date_fin_prevue": "2025-05-15"},

    # Projet 4 — Morières
    {"ref": "4243946_2201", "phase": "AVP", "budget_avp": 1_980_000, "date_phase": "2023-10-08"},
    {"ref": "4243946_2201", "phase": "PRO", "budget_pro": 2_050_000, "date_phase": "2024-01-20"},
    {"ref": "4243946_2201", "phase": "ACT", "prix_marche": 2_180_000, "date_phase": "2024-07-08"},
    {"ref": "4243946_2201", "phase": "DET", "date_debut": "2024-07-20", "date_fin_prevue": "2026-03-20"},
]

# ── 3. SUBVENTIONS ─────────────────────────────────────────────────────────
subventions_raw = [
    # Projet 1 — Les Angles
    {"ref": "4243946_2301", "lot": 1, "nature": "AEP", "organisme": "Département de Vaucluse",      "montant": 85_000},
    {"ref": "4243946_2301", "lot": 1, "nature": "AEP", "organisme": "État-DETR",                    "montant": 30_000},
    {"ref": "4243946_2301", "lot": 1, "nature": "EU",  "organisme": "Agence de l'Eau RMC",          "montant": 83_000},
    {"ref": "4243946_2301", "lot": 1, "nature": "EU",  "organisme": "État-DETR",                    "montant": 25_000},
    {"ref": "4243946_2301", "lot": 1, "nature": "EP",  "organisme": "Région Sud PACA",              "montant":  5_000},
    {"ref": "4243946_2301", "lot": 1, "nature": "EP",  "organisme": "Agence de l'Eau RMC - pluvial","montant": 15_000},
    {"ref": "4243946_2301", "lot": 1, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant": 10_000},
    {"ref": "4243946_2301", "lot": 2, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant": 50_000},

    # Projet 2 — Avignon
    {"ref": "4243946_2202", "lot": 1, "nature": "AEP", "organisme": "Département de Vaucluse",      "montant": 55_000},
    {"ref": "4243946_2202", "lot": 1, "nature": "AEP", "organisme": "État-DETR",                    "montant": 25_000},
    {"ref": "4243946_2202", "lot": 1, "nature": "EU",  "organisme": "Agence de l'Eau RMC",          "montant": 65_000},
    {"ref": "4243946_2202", "lot": 1, "nature": "EU",  "organisme": "État-DETR",                    "montant": 22_000},
    {"ref": "4243946_2202", "lot": 1, "nature": "EP",  "organisme": "Agence de l'Eau RMC - pluvial","montant": 10_000},
    {"ref": "4243946_2202", "lot": 1, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant":  8_000},
    {"ref": "4243946_2202", "lot": 2, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant": 25_000},

    # Projet 3 — Entraigues
    {"ref": "4243946_2203", "lot": 1, "nature": "AEP", "organisme": "Département de Vaucluse",      "montant": 98_000},
    {"ref": "4243946_2203", "lot": 1, "nature": "AEP", "organisme": "État-DETR",                    "montant": 35_000},
    {"ref": "4243946_2203", "lot": 1, "nature": "EU",  "organisme": "Agence de l'Eau RMC",          "montant": 45_000},
    {"ref": "4243946_2203", "lot": 1, "nature": "EU",  "organisme": "État-DETR",                    "montant": 25_000},
    {"ref": "4243946_2203", "lot": 1, "nature": "EP",  "organisme": "Région Sud PACA",              "montant":  5_000},
    {"ref": "4243946_2203", "lot": 1, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant": 25_000},
    {"ref": "4243946_2203", "lot": 2, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant": 60_000},

    # Projet 4 — Morières
    {"ref": "4243946_2201", "lot": 1, "nature": "AEP", "organisme": "Département de Vaucluse",      "montant": 85_000},
    {"ref": "4243946_2201", "lot": 1, "nature": "AEP", "organisme": "État-DETR",                    "montant": 30_000},
    {"ref": "4243946_2201", "lot": 1, "nature": "EU",  "organisme": "Agence de l'Eau RMC",          "montant": 83_000},
    {"ref": "4243946_2201", "lot": 1, "nature": "EU",  "organisme": "État-DETR",                    "montant": 25_000},
    {"ref": "4243946_2201", "lot": 1, "nature": "EP",  "organisme": "Région Sud PACA",              "montant":  5_000},
    {"ref": "4243946_2201", "lot": 1, "nature": "EP",  "organisme": "Agence de l'Eau RMC - pluvial","montant": 15_000},
    {"ref": "4243946_2201", "lot": 1, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant": 10_000},
    {"ref": "4243946_2201", "lot": 2, "nature": "Aménagement", "organisme": "Région Sud PACA",      "montant": 50_000},
]

# ─── TRANSFORMATION ──────────────────────────────────────────────────────────

def build_dataframes():
    """Construit les DataFrames structurés depuis les données brutes."""

    df_operations = pd.DataFrame(operations_raw)
    df_operations['date_os_moe'] = pd.to_datetime(df_operations['date_os_moe'])
    df_operations['date_ouverture_fiche'] = pd.to_datetime(df_operations['date_ouverture_fiche'])

    df_budgets = pd.DataFrame(budgets_raw)

    df_subventions = pd.DataFrame(subventions_raw)
    df_subventions['montant'] = df_subventions['montant'].astype(float)

    return df_operations, df_budgets, df_subventions


def audit_qualite(df_operations, df_budgets, df_subventions):
    """Rapport d'audit qualité des données."""

    print("=" * 60)
    print("AUDIT QUALITÉ — ATLAS — 4 projets pilotes")
    print("=" * 60)

    print(f"\n✓ Opérations : {len(df_operations)} projets")
    print(f"  Communes : {df_operations['commune'].unique().tolist()}")

    print(f"\n✓ Budgets : {len(df_budgets)} lignes (phases)")
    print(f"  Phases présentes : {df_budgets['phase'].unique().tolist()}")

    print(f"\n✓ Subventions : {len(df_subventions)} lignes")
    print(f"  Total notifié tous projets : {df_subventions['montant'].sum():,.0f} €")
    print(f"  Par organisme :")
    by_org = df_subventions.groupby('organisme')['montant'].sum().sort_values(ascending=False)
    for org, total in by_org.items():
        print(f"    {org}: {total:,.0f} €")

    print(f"\n✓ Par projet :")
    by_proj = df_subventions.groupby('ref')['montant'].sum()
    for ref, total in by_proj.items():
        print(f"    {ref}: {total:,.0f} €")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    df_ops, df_budgets, df_subv = build_dataframes()
    audit_qualite(df_ops, df_budgets, df_subv)
    print("\n✓ DataFrames prêts pour ingestion PostgreSQL")
