"""
load_raw.py — Chargement des CSV bruts dans le schéma `raw` de PostgreSQL.

Principe :
la couche RAW conserve les données issues des CSV sans transformation métier.
Les conversions de types, nettoyages et normalisations seront réalisés avec dbt
dans la couche `staging`.

Usage :
    python load_raw.py
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


# ---------------------------------------------------------------------------
# 1. Configuration
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")


# Vérification des variables indispensables
required_variables = {
    "POSTGRES_USER": DB_USER,
    "POSTGRES_PASSWORD": DB_PASSWORD,
    "POSTGRES_DB": DB_NAME,
}

missing = [name for name, value in required_variables.items() if not value]

if missing:
    raise RuntimeError(
        f"Variables d'environnement manquantes : {', '.join(missing)}"
    )


# Construction sécurisée de l'URL SQLAlchemy
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=int(DB_PORT),
    database=DB_NAME,
)


# ---------------------------------------------------------------------------
# 2. Fichiers CSV RAW
# ---------------------------------------------------------------------------

RAW_DIR = Path(__file__).resolve().parent / "raw"

CSV_FILES = {
    "raw_operations.csv": "operations",
    "raw_lots.csv": "lots",
    "raw_budgets.csv": "budgets",
    "raw_subventions.csv": "subventions",
    "raw_indicateurs_dd.csv": "indicateurs_dd",
}

TARGET_SCHEMA = "raw"


# ---------------------------------------------------------------------------
# 3. Chargement PostgreSQL
# ---------------------------------------------------------------------------

def main() -> None:

    engine = create_engine(DATABASE_URL)

    # Test de connexion et création du schéma RAW
    with engine.begin() as conn:
        conn.execute(
            text(f"CREATE SCHEMA IF NOT EXISTS {TARGET_SCHEMA};")
        )

    print(f"[OK] Connexion reussie -- schema '{TARGET_SCHEMA}' pret.\n")

    for csv_name, table_name in CSV_FILES.items():

        csv_path = RAW_DIR / csv_name

        if not csv_path.exists():
            print(f"[X] Fichier introuvable : {csv_path} -- ignore.")
            continue

        # RAW : toutes les colonnes restent textuelles.
        # Les transformations seront effectuées ultérieurement avec dbt.
        df = pd.read_csv(
            csv_path,
            dtype=str,
            keep_default_na=False,
            encoding="utf-8",
        )

        # La table RAW est conservée afin de ne pas casser
        # les vues dbt qui en dépendent.
        with engine.begin() as conn:
            conn.execute(
                text(
                    f'TRUNCATE TABLE "{TARGET_SCHEMA}"."{table_name}";'
                )
            )

        # Recharge les nouvelles données sans supprimer la table.
        df.to_sql(
            name=table_name,
            con=engine,
            schema=TARGET_SCHEMA,
            if_exists="append",
            index=False,
        )

        print(
            f"[OK] {csv_name:28} "
            f"-> {TARGET_SCHEMA}.{table_name:16} "
            f"({len(df)} lignes)"
        )

    engine.dispose()

    print("\n[TERMINE] Chargement termine.")


if __name__ == "__main__":
    main()