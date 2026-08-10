# Modèle Logique de Données (MLD) — ATLAS

> Traduction du MCD en schéma relationnel PostgreSQL  
> Schéma cible : `gold` (consommé par Power BI)

---

## Schéma en étoile complet

```
                              dim_territoire
                              (territoire_id PK)
                                    │ 1
                                    │
                                    │ N
                              dim_operation
                              (operation_id PK)
                             /               \
                            / N             N \
                           /                   \
              1            /                     \ 1
    dim_moe ──────────────                        ──────────────
    (moe_id PK)                                                  \
                          /                                       \
                    ┌────┴──────────┐                    ┌────────┴───────┐
                    │               │                    │                │
                    ▼               ▼                    ▼                ▼
            fact_operations  fact_indicateurs_dd  fact_subventions
            (1 op × 1 phase) (1 op × 1 indicateur)(1 subvention)
                    │                    │                    │
               ┌────┤               ┌───┤               ┌────┤
               │    │               │                   │    │
               ▼    ▼               ▼                   ▼    ▼
          dim_phase  dim_calendrier  dim_type_ind  dim_organisme  dim_type_travaux
          dim_statut                _dd
          dim_type_travaux
```

---

## Tables du schéma `gold`

### Dimensions

```sql
-- ── dim_territoire ─────────────────────────────────────────────
gold.dim_territoire (
    territoire_id    SERIAL      PRIMARY KEY,
    nom_commune      VARCHAR(100) NOT NULL,
    code_insee       VARCHAR(5),
    nom_communaute   VARCHAR(100),
    nom_departement  VARCHAR(100),
    code_departement VARCHAR(3),
    nom_region       VARCHAR(100),
    type_zone        VARCHAR(20),    -- urbain / périurbain / rural
    population       INTEGER
)

-- ── dim_moe ────────────────────────────────────────────────────
gold.dim_moe (
    moe_id      SERIAL      PRIMARY KEY,
    nom_moe     VARCHAR(100) NOT NULL,
    type_moe    VARCHAR(50),
    specialite  VARCHAR(100),
    is_actif    BOOLEAN DEFAULT TRUE
)

-- ── dim_operation ──────────────────────────────────────────────
gold.dim_operation (
    operation_id          SERIAL      PRIMARY KEY,
    numero_ref_artelia    VARCHAR(20) NOT NULL UNIQUE,
    intitule              VARCHAR(200) NOT NULL,
    territoire_id         INTEGER REFERENCES gold.dim_territoire,
    moe_id                INTEGER REFERENCES gold.dim_moe,
    responsable_moe       VARCHAR(100),
    responsable_moa       VARCHAR(100),
    complexite            VARCHAR(10),     -- Faible / Moyenne / Élevée
    date_os_moe           DATE,
    date_ouverture_fiche  DATE,
    is_historique         BOOLEAN DEFAULT FALSE
)

-- ── dim_phase ──────────────────────────────────────────────────
gold.dim_phase (
    phase_id     SERIAL     PRIMARY KEY,
    code_phase   VARCHAR(3) NOT NULL UNIQUE,
    libelle      VARCHAR(60),
    ordre        INTEGER,
    budget_ref   VARCHAR(30)
)
-- Données fixes : AVP(1) PRO(2) ACT(3) DET(4) AOR(5)

-- ── dim_statut ─────────────────────────────────────────────────
gold.dim_statut (
    statut_id      SERIAL     PRIMARY KEY,
    libelle        VARCHAR(50) NOT NULL UNIQUE,
    is_actif       BOOLEAN DEFAULT TRUE,
    is_retard      BOOLEAN DEFAULT FALSE,
    is_termine     BOOLEAN DEFAULT FALSE,
    couleur_alerte VARCHAR(10)
)

-- ── dim_type_travaux ───────────────────────────────────────────
gold.dim_type_travaux (
    type_id              SERIAL     PRIMARY KEY,
    libelle              VARCHAR(60) NOT NULL UNIQUE,
    code_standard        VARCHAR(10),
    categorie_dd         VARCHAR(40),
    eligible_subvention  BOOLEAN DEFAULT FALSE,
    indicateur_vert      BOOLEAN DEFAULT FALSE
)
-- 8 catégories : VOI-CH, VOI-SG, EP, AEP, EU, EV, EP-ECL, DIV

-- ── dim_organisme ──────────────────────────────────────────────
gold.dim_organisme (
    organisme_id   SERIAL      PRIMARY KEY,
    nom            VARCHAR(100) NOT NULL UNIQUE,
    code_court     VARCHAR(30),
    type_organisme VARCHAR(30),
    echelon        VARCHAR(20),
    taux_plafond   DECIMAL(5,2)
)
-- 5 organismes : Département 84, Agence Eau RMC, Agence Eau pluvial, Région Sud, DETR

-- ── dim_type_indicateur_dd ─────────────────────────────────────
gold.dim_type_indicateur_dd (
    type_indicateur_id  SERIAL      PRIMARY KEY,
    libelle             VARCHAR(100) NOT NULL UNIQUE,
    categorie           VARCHAR(20),     -- Bas-Carbone / Biodiversité / Social
    unite               VARCHAR(20),
    sens_positif        VARCHAR(20)      -- Plus haut / Plus bas / Oui = conforme
)
-- 16 indicateurs fixes issus des 4 projets pilotes

-- ── dim_calendrier ─────────────────────────────────────────────
gold.dim_calendrier (
    date_id            INTEGER PRIMARY KEY,  -- YYYYMMDD
    date_complete      DATE NOT NULL UNIQUE,
    annee              INTEGER,
    trimestre          VARCHAR(2),
    mois               INTEGER,
    mois_label         VARCHAR(20),
    semaine            INTEGER,
    annee_mandat       INTEGER,              -- 1 à 6
    is_mandat_courant  BOOLEAN DEFAULT FALSE,
    debut_mandat       DATE
)
```

---

### Tables de faits

```sql
-- ── fact_operations ────────────────────────────────────────────
-- Granularité : 1 ligne = 1 opération × 1 phase
gold.fact_operations (
    operation_phase_id  SERIAL  PRIMARY KEY,
    -- Clés étrangères
    operation_id        INTEGER NOT NULL REFERENCES gold.dim_operation,
    phase_id            INTEGER NOT NULL REFERENCES gold.dim_phase,
    date_id             INTEGER          REFERENCES gold.dim_calendrier,
    statut_id           INTEGER          REFERENCES gold.dim_statut,
    type_id             INTEGER          REFERENCES gold.dim_type_travaux,
    -- Mesures (NULL = phase pas encore atteinte)
    budget_avp          DECIMAL(15,2),
    budget_pro          DECIMAL(15,2),
    prix_marche         DECIMAL(15,2),
    montant_engage      DECIMAL(15,2),
    montant_paye        DECIMAL(15,2),
    cout_final          DECIMAL(15,2),
    montant_avenant     DECIMAL(15,2) DEFAULT 0,
    -- Dates
    date_debut_phase    DATE,
    date_fin_prevue     DATE,
    date_fin_reelle     DATE,
    -- Attribut dégénéré
    nb_reserves         INTEGER DEFAULT 0,
    -- Contrainte unicité
    CONSTRAINT uq_op_phase UNIQUE (operation_id, phase_id)
)

-- ── fact_subventions ───────────────────────────────────────────
-- Granularité : 1 ligne = 1 subvention notifiée
gold.fact_subventions (
    subvention_id      SERIAL  PRIMARY KEY,
    -- Clés étrangères
    operation_id       INTEGER NOT NULL REFERENCES gold.dim_operation,
    organisme_id       INTEGER NOT NULL REFERENCES gold.dim_organisme,
    type_id            INTEGER          REFERENCES gold.dim_type_travaux,
    date_id            INTEGER          REFERENCES gold.dim_calendrier,
    -- Mesure unique (décision encadrant)
    montant_notifie    DECIMAL(15,2) NOT NULL,
    taux               DECIMAL(5,2),
    lot                INTEGER,             -- 1, 2 ou 3
    -- Métadonnées
    date_notification  DATE,
    reference_acte     VARCHAR(50),
    sujet              VARCHAR(200)
)

-- ── fact_indicateurs_dd ────────────────────────────────────────
-- Granularité : 1 ligne = 1 indicateur × 1 opération
-- Nouveauté issue de l'analyse des 4 projets pilotes
gold.fact_indicateurs_dd (
    indicateur_id       SERIAL  PRIMARY KEY,
    -- Clés étrangères
    operation_id        INTEGER NOT NULL REFERENCES gold.dim_operation,
    type_indicateur_id  INTEGER NOT NULL REFERENCES gold.dim_type_indicateur_dd,
    -- Mesures
    valeur_cible        DECIMAL(12,2) NOT NULL,
    valeur_constatee    DECIMAL(12,2),
    bilan               VARCHAR(20),         -- Dépassé / Conforme / En retrait
    date_mesure         DATE,
    -- Contrainte unicité
    CONSTRAINT uq_ind_op UNIQUE (operation_id, type_indicateur_id)
)
```

---

## Relations et cardinalités

| Table source | Cardinalité | Table cible | Direction filtre Power BI |
|-------------|------------|-------------|--------------------------|
| dim_operation | 1 → N | fact_operations | dim → faits ✓ |
| dim_operation | 1 → N | fact_subventions | dim → faits ✓ |
| dim_operation | 1 → N | fact_indicateurs_dd | dim → faits ✓ |
| dim_territoire | 1 → N | dim_operation | dim → dim ✓ |
| dim_moe | 1 → N | dim_operation | dim → dim ✓ |
| dim_phase | 1 → N | fact_operations | dim → faits ✓ |
| dim_statut | 1 → N | fact_operations | dim → faits ✓ |
| dim_type_travaux | 1 → N | fact_operations | dim → faits ✓ |
| dim_type_travaux | 1 → N | fact_subventions | dim → faits ✓ |
| dim_organisme | 1 → N | fact_subventions | dim → faits ✓ |
| dim_type_indicateur_dd | 1 → N | fact_indicateurs_dd | dim → faits ✓ |
| dim_calendrier | 1 → N | fact_operations | dim → faits ✓ |
| dim_calendrier | 1 → N | fact_subventions | dim → faits ✓ |

> **Règle absolue :** Tous les filtres sont unidirectionnels (dim → faits). Les 3 tables de faits ne sont jamais reliées directement entre elles.

---

## Couches PostgreSQL

```
raw/        ← Données brutes telles qu'elles arrivent d'Airbyte
             (tables préfixées raw_)

staging/    ← Données nettoyées et typées par dbt
             (tables préfixées stg_)

gold/       ← Star schema final consommé par Power BI
             (dims + facts)
```

---

## Index

```sql
-- Performance des jointures Power BI
CREATE INDEX idx_fact_ops_op     ON gold.fact_operations(operation_id);
CREATE INDEX idx_fact_ops_phase  ON gold.fact_operations(phase_id);
CREATE INDEX idx_fact_ops_date   ON gold.fact_operations(date_id);
CREATE INDEX idx_fact_ops_statut ON gold.fact_operations(statut_id);
CREATE INDEX idx_fact_subv_op    ON gold.fact_subventions(operation_id);
CREATE INDEX idx_fact_subv_org   ON gold.fact_subventions(organisme_id);
CREATE INDEX idx_fact_dd_op      ON gold.fact_indicateurs_dd(operation_id);
CREATE INDEX idx_dim_op_terr     ON gold.dim_operation(territoire_id);
CREATE INDEX idx_dim_op_moe      ON gold.dim_operation(moe_id);
```

---

*MLD ATLAS · v1.0 · Août 2026 — 3 tables de faits, 8 dimensions, 11 tables au total*
