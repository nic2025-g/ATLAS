-- ============================================================
-- ATLAS — DDL PostgreSQL complet
-- Conception d'une plateforme décisionnelle
-- Pilotage des investissements territoriaux
-- Communauté de Communes du Grand Avignon
-- ============================================================
-- Auteur  : BAMANIA Nathanael Nicolas — Stage Data Engineering 2026
-- Version : 1.0 — Août 2026
-- MCD     : Validé — Méthode Merise
-- Ordre   : Référentiels → Objets métier → Associations → Faits
-- ============================================================

-- ── SCHÉMAS ──────────────────────────────────────────────────
CREATE SCHEMA IF NOT EXISTS raw;      -- Données brutes sources
CREATE SCHEMA IF NOT EXISTS staging;  -- Données nettoyées (dbt)
CREATE SCHEMA IF NOT EXISTS gold;     -- Modèle final (Power BI)

SET search_path = gold;

-- ============================================================
-- COUCHE 1 — RÉFÉRENTIELS STABLES (6 tables)
-- Pas de dépendances externes — créées en premier
-- ============================================================

-- ------------------------------------------------------------
-- COMMUNE
-- Une commune = un territoire géographique de la CC
-- Cardinalité : 1 COMMUNE → 0,N OPERATION
-- ------------------------------------------------------------
CREATE TABLE commune (
    commune_id      SERIAL          PRIMARY KEY,
    nom_commune     VARCHAR(100)    NOT NULL,
    code_insee      VARCHAR(5),
    nom_communaute  VARCHAR(100),
    nom_departement VARCHAR(100),
    nom_region      VARCHAR(100),
    CONSTRAINT uq_commune_insee UNIQUE (code_insee)
);

COMMENT ON TABLE  commune             IS 'Référentiel des communes du territoire CC Grand Avignon';
COMMENT ON COLUMN commune.code_insee  IS 'Code INSEE à 5 chiffres — sert de clé pour la carte choroplèthe Power BI';

-- ------------------------------------------------------------
-- ACTEUR
-- MOA et MOE — le rôle est dans INTERVENIR_SUR, pas ici
-- Cardinalité : 1 ACTEUR → 1,N INTERVENIR_SUR
-- ------------------------------------------------------------
CREATE TABLE acteur (
    acteur_id       SERIAL          PRIMARY KEY,
    raison_sociale  VARCHAR(100)    NOT NULL,
    adresse         VARCHAR(200),
    contact         VARCHAR(100),
    siret           VARCHAR(14),
    CONSTRAINT uq_acteur_siret UNIQUE (siret)
);

COMMENT ON TABLE  acteur              IS 'Référentiel des acteurs (MOA et MOE) — le rôle est dans INTERVENIR_SUR';
COMMENT ON COLUMN acteur.raison_sociale IS 'Dénomination sociale officielle de la structure';
COMMENT ON COLUMN acteur.siret        IS 'Identifiant SIRET 14 chiffres — VARCHAR car peut débuter par 0';

-- ------------------------------------------------------------
-- ENTREPRISE
-- Sociétés BTP — reliées aux lots via PARTICIPER_AU_LOT
-- Cardinalité : 1 ENTREPRISE → 1,N PARTICIPER_AU_LOT
-- ------------------------------------------------------------
CREATE TABLE entreprise (
    entreprise_id   SERIAL          PRIMARY KEY,
    nom             VARCHAR(100)    NOT NULL,
    ville           VARCHAR(100),
    siret           VARCHAR(14),
    type_activite   VARCHAR(60),
    contact         VARCHAR(100),
    CONSTRAINT uq_entreprise_siret UNIQUE (siret)
);

COMMENT ON TABLE  entreprise          IS 'Référentiel des entreprises de travaux BTP';
COMMENT ON COLUMN entreprise.siret    IS 'SIRET en VARCHAR — identifiant administratif pouvant débuter par 0';

-- ------------------------------------------------------------
-- PHASE
-- Cycle de vie réglementé par la loi MOP
-- Valeurs fixes : AVP(1) PRO(2) ACT(3) DET(4) AOR(5)
-- Cardinalité : 1 PHASE → 1,N ESTIMATION_FINANCIERE
-- ------------------------------------------------------------
CREATE TABLE phase (
    phase_id    SERIAL          PRIMARY KEY,
    code_phase  VARCHAR(3)      NOT NULL,
    libelle     VARCHAR(60)     NOT NULL,
    ordre       INT             NOT NULL,
    CONSTRAINT uq_phase_code  UNIQUE (code_phase),
    CONSTRAINT uq_phase_ordre UNIQUE (ordre),
    CONSTRAINT ck_phase_code  CHECK (code_phase IN ('AVP','PRO','ACT','DET','AOR'))
);

COMMENT ON TABLE  phase            IS 'Cycle de vie loi MOP — 5 phases ordonnées AVP→AOR';
COMMENT ON COLUMN phase.ordre      IS 'Ordre chronologique 1→5 — indispensable pour le tri Power BI';
COMMENT ON COLUMN phase.code_phase IS 'AVP=Avant-Projet PRO=Projet ACT=Contrat DET=Travaux AOR=Réception';

-- Données de référence
INSERT INTO phase (code_phase, libelle, ordre) VALUES
    ('AVP', 'Avant-Projet',                   1),
    ('PRO', 'Projet',                         2),
    ('ACT', 'Assistance Contrat Travaux',     3),
    ('DET', 'Direction Exécution Travaux',    4),
    ('AOR', 'Assistance Opération Réception', 5);

-- ------------------------------------------------------------
-- ORGANISME
-- Financeurs de subventions
-- Cardinalité : 1 ORGANISME → 1,N SUBVENTION
-- ------------------------------------------------------------
CREATE TABLE organisme (
    organisme_id    SERIAL          PRIMARY KEY,
    nom             VARCHAR(100)    NOT NULL,
    code_court      VARCHAR(20),
    type            VARCHAR(30),
    echelon         VARCHAR(20),
    taux_plafond    DECIMAL(5,2),
    CONSTRAINT uq_organisme_nom  UNIQUE (nom),
    CONSTRAINT uq_organisme_code UNIQUE (code_court),
    CONSTRAINT ck_organisme_type CHECK (type IN ('État','Collectivité','Agence','Europe')),
    CONSTRAINT ck_organisme_echelon CHECK (echelon IN ('national','régional','départemental','local'))
);

COMMENT ON TABLE  organisme              IS 'Référentiel des organismes verseurs de subventions';
COMMENT ON COLUMN organisme.taux_plafond IS 'Taux plafond indicatif en % — le taux réel est dans SUBVENTION';

-- Données de référence
INSERT INTO organisme (nom, code_court, type, echelon, taux_plafond) VALUES
    ('Département de Vaucluse',              'DEPT84',     'Collectivité', 'départemental', 5.00),
    ('Agence de l''Eau Rhône Méditerranée Corse', 'AERMC-EU', 'Agence',  'national',       8.00),
    ('Agence de l''Eau RMC - volet pluvial', 'AERMC-EP',   'Agence',     'national',       7.00),
    ('Région Sud PACA',                      'REGION-SUD', 'Collectivité','régional',       5.00),
    ('État — DETR',                          'DETR',       'État',        'national',       6.00);

-- ------------------------------------------------------------
-- TYPE_TRAVAUX
-- Nomenclature standardisée — normalise les bordereaux de prix
-- Cardinalité : 1 TYPE_TRAVAUX → 1,N LOT + 0,N SUBVENTION
-- ------------------------------------------------------------
CREATE TABLE type_travaux (
    type_trav_id    SERIAL          PRIMARY KEY,
    code            VARCHAR(10)     NOT NULL,
    libelle         VARCHAR(60)     NOT NULL,
    categorie_dd    VARCHAR(30),
    eligible_subv   BOOLEAN         DEFAULT FALSE,
    indicateur_vert BOOLEAN         DEFAULT FALSE,
    CONSTRAINT uq_type_trav_code UNIQUE (code)
);

COMMENT ON TABLE  type_travaux                IS 'Nomenclature standardisée des travaux — 8 catégories';
COMMENT ON COLUMN type_travaux.eligible_subv  IS 'Éligible à une subvention externe — utilisé pour les alertes DAX';
COMMENT ON COLUMN type_travaux.indicateur_vert IS 'Contribue aux objectifs de développement durable';

-- Données de référence
INSERT INTO type_travaux (code, libelle, categorie_dd, eligible_subv, indicateur_vert) VALUES
    ('VOI-CH',  'Voirie — chaussée',             'Mobilité',       FALSE, FALSE),
    ('VOI-SG',  'Voirie — signalisation',         'Mobilité',       FALSE, FALSE),
    ('EP',      'Réseaux eaux pluviales',         'Eau',            TRUE,  TRUE),
    ('AEP',     'Eau potable',                    'Eau',            TRUE,  TRUE),
    ('EU',      'Assainissement',                 'Eau',            TRUE,  TRUE),
    ('EV',      'Espaces verts',                  'Environnement',  TRUE,  TRUE),
    ('ECL',     'Éclairage public',               'Énergie',        FALSE, FALSE),
    ('DIV',     'Divers / Non ventilé',           NULL,             FALSE, FALSE);

-- ============================================================
-- COUCHE 2 — RÉFÉRENTIELS CATALOGUES (2 tables)
-- ============================================================

-- ------------------------------------------------------------
-- TYPE_RISQUE
-- Catalogue des risques génériques
-- Cardinalité : 1 TYPE_RISQUE → 1,N RISQUE
-- ------------------------------------------------------------
CREATE TABLE type_risque (
    type_risque_id  SERIAL          PRIMARY KEY,
    code            VARCHAR(5)      NOT NULL,
    description     TEXT            NOT NULL,
    gravite         VARCHAR(15),
    probabilite_ini INT,
    categorie       VARCHAR(20),
    CONSTRAINT uq_type_risque_code  UNIQUE (code),
    CONSTRAINT ck_type_risque_grav  CHECK (gravite IN ('FAIBLE','MOYENNE','GRAVE','TRÈS GRAVE')),
    CONSTRAINT ck_type_risque_prob  CHECK (probabilite_ini BETWEEN 0 AND 100),
    CONSTRAINT ck_type_risque_cat   CHECK (categorie IN ('Technique','Juridique','Économique','Organisationnel'))
);

COMMENT ON TABLE  type_risque                IS 'Catalogue des types de risques — commun à tous les projets';
COMMENT ON COLUMN type_risque.probabilite_ini IS 'Probabilité initiale générique en % — la probabilité contextualisée est dans RISQUE';

-- Données de référence
INSERT INTO type_risque (code, description, gravite, probabilite_ini, categorie) VALUES
    ('R1',  'Géotechnique (foisonnement remblais, fondations imprévues)',                'GRAVE',       60, 'Technique'),
    ('R2',  'Foncier (servitudes, conventions domaine public fluvial)',                   'MOYENNE',     85, 'Juridique'),
    ('R11', 'Hausse des prix matériaux (acier, granulats, enrobé, carburant)',           'GRAVE',       50, 'Économique'),
    ('R12', 'Aléa chantier imprévu (réseau désaffecté, coactivité, géotechnique DET)',  'TRÈS GRAVE',  80, 'Technique');

-- ------------------------------------------------------------
-- TYPE_INDICATEUR
-- Catalogue des 16 indicateurs de développement durable
-- Cardinalité : 1 TYPE_INDICATEUR → 1,N INDICATEUR_DD
-- ------------------------------------------------------------
CREATE TABLE type_indicateur (
    type_ind_id     SERIAL          PRIMARY KEY,
    libelle         VARCHAR(100)    NOT NULL,
    categorie       VARCHAR(20),
    unite           VARCHAR(15),
    sens_positif    VARCHAR(20),
    CONSTRAINT uq_type_ind_libelle UNIQUE (libelle),
    CONSTRAINT ck_type_ind_cat CHECK (categorie IN ('Bas-Carbone','Biodiversité','Social'))
);

COMMENT ON TABLE  type_indicateur             IS 'Catalogue des 16 indicateurs DD — commun à tous les projets';
COMMENT ON COLUMN type_indicateur.sens_positif IS 'Plus haut = mieux / Plus bas = mieux / Oui = conforme';

-- Données de référence
INSERT INTO type_indicateur (libelle, categorie, unite, sens_positif) VALUES
    ('Surface perméable supplémentaire', 'Bas-Carbone',  'm²',      'Plus haut'),
    ('Réemploi de matériaux',            'Bas-Carbone',  'm³',      'Plus haut'),
    ('Matériaux recyclés incorporés',    'Bas-Carbone',  'm³',      'Plus haut'),
    ('Matériaux vertueux',               'Bas-Carbone',  '€',       'Plus haut'),
    ('Espaces verts créés',              'Bas-Carbone',  'm²',      'Plus haut'),
    ('Arbres plantés',                   'Bas-Carbone',  'U',       'Plus haut'),
    ('Économie électrique annuelle',     'Bas-Carbone',  'kWh/an',  'Plus haut'),
    ('Économie eau annuelle',            'Bas-Carbone',  'm³/an',   'Plus haut'),
    ('Renouvellement réseaux',           'Bas-Carbone',  'ml',      'Plus haut'),
    ('Réduction îlot de chaleur',        'Biodiversité', 'Oui/Non', 'Oui = conforme'),
    ('Actions biodiversité',             'Biodiversité', 'Nb',      'Plus haut'),
    ('Aménagements accessibilité',       'Social',       'Nb',      'Plus haut'),
    ('Modes doux aménagés',              'Bas-Carbone',  'ml',      'Plus haut'),
    ('Mobilier urbain installé',         'Social',       'Nb',      'Plus haut'),
    ('Heures d''insertion',              'Social',       'h',       'Plus haut'),
    ('Part économie locale',             'Bas-Carbone',  '%',       'Plus haut');

-- ============================================================
-- COUCHE 3 — OBJETS MÉTIER PRINCIPAUX (4 tables)
-- Dépendent des référentiels
-- ============================================================

-- ------------------------------------------------------------
-- OPERATION
-- Entité centrale — tout gravite autour d'elle
-- Dépend de : COMMUNE
-- Cardinalité : 1 OPERATION → 1,N (ESTIMATION, MARCHE,
--               SUBVENTION, RISQUE, INDICATEUR_DD, INTERVENIR_SUR)
-- ------------------------------------------------------------
CREATE TABLE operation (
    operation_id        SERIAL          PRIMARY KEY,
    reference_artelia   VARCHAR(20)     NOT NULL,
    intitule            VARCHAR(200)    NOT NULL,
    nature_travaux      VARCHAR(100),
    commune_id          INT             NOT NULL    REFERENCES commune(commune_id),
    complexite          VARCHAR(10),
    date_os_moe         DATE,
    date_ouverture      DATE,
    statut_courant      VARCHAR(30),
    CONSTRAINT uq_operation_ref  UNIQUE (reference_artelia),
    CONSTRAINT ck_operation_cplx CHECK (complexite IN ('Faible','Moyenne','Élevée'))
);

COMMENT ON TABLE  operation                    IS 'Entité centrale — projet d''aménagement individualisé';
COMMENT ON COLUMN operation.reference_artelia  IS 'Référence interne Artelia — ex: 4243946_2301';
COMMENT ON COLUMN operation.commune_id         IS 'FK vers COMMUNE — la commune bénéficiaire des travaux';
COMMENT ON COLUMN operation.statut_courant     IS 'Statut le plus récent — dénormalisé pour performance';

CREATE INDEX idx_operation_commune ON operation(commune_id);

-- ------------------------------------------------------------
-- ESTIMATION_FINANCIERE
-- Évolution budgétaire phase par phase
-- Dépend de : OPERATION, PHASE
-- Cardinalité : N ESTIMATION → 1 OPERATION, 1 PHASE
-- ------------------------------------------------------------
CREATE TABLE estimation_financiere (
    estim_id        SERIAL          PRIMARY KEY,
    operation_id    INT             NOT NULL    REFERENCES operation(operation_id),
    phase_id        INT             NOT NULL    REFERENCES phase(phase_id),
    type_budget     VARCHAR(25)     NOT NULL,
    montant         DECIMAL(15,2)   NOT NULL,
    date_estimation DATE,
    CONSTRAINT ck_estim_type CHECK (type_budget IN (
        'budget_programme','budget_avp','budget_pro',
        'prix_marche','montant_engage','cout_final'
    ))
);

COMMENT ON TABLE  estimation_financiere           IS 'Évolution budgétaire — 1 ligne par opération × type de budget';
COMMENT ON COLUMN estimation_financiere.type_budget IS 'budget_programme|budget_avp|budget_pro|prix_marche|montant_engage|cout_final';
COMMENT ON COLUMN estimation_financiere.montant     IS 'Montant HT en euros';

CREATE INDEX idx_estim_operation ON estimation_financiere(operation_id);
CREATE INDEX idx_estim_phase     ON estimation_financiere(phase_id);

-- ------------------------------------------------------------
-- MARCHE
-- Acte contractuel — passage de ACT aux travaux
-- Dépend de : OPERATION
-- Cardinalité : 1 MARCHE → 1,N LOT
-- ------------------------------------------------------------
CREATE TABLE marche (
    marche_id           SERIAL          PRIMARY KEY,
    operation_id        INT             NOT NULL    REFERENCES operation(operation_id),
    ref_administrative  VARCHAR(30),
    date_notification   DATE,
    montant_total_ht    DECIMAL(15,2),
    statut              VARCHAR(20),
    CONSTRAINT ck_marche_statut CHECK (statut IN ('En cours','Réceptionné','Résilié'))
);

COMMENT ON TABLE  marche                     IS 'Marché public — acte contractuel entre MOA et ENT';
COMMENT ON COLUMN marche.montant_total_ht    IS 'Montant total HT signé — peut différer de la somme des lots';
COMMENT ON COLUMN marche.ref_administrative  IS 'Référence administrative de l''acte de notification';

CREATE INDEX idx_marche_operation ON marche(operation_id);

-- ------------------------------------------------------------
-- LOT
-- Division d'un marché en lots techniques
-- Dépend de : MARCHE, TYPE_TRAVAUX
-- Cardinalité : 1 LOT → 0,N PARTICIPER_AU_LOT + 0,N SUBVENTION
-- ------------------------------------------------------------
CREATE TABLE lot (
    lot_id          SERIAL          PRIMARY KEY,
    marche_id       INT             NOT NULL    REFERENCES marche(marche_id),
    num_lot         INT             NOT NULL,
    libelle         VARCHAR(60)     NOT NULL,
    type_trav_id    INT                         REFERENCES type_travaux(type_trav_id),
    montant_ht      DECIMAL(15,2),
    date_os_travaux DATE,
    date_fin_prevue DATE,
    date_fin_reelle DATE,
    statut          VARCHAR(20),
    CONSTRAINT uq_lot_marche_num UNIQUE (marche_id, num_lot),
    CONSTRAINT ck_lot_statut     CHECK (statut IN ('En cours','Réceptionné','Suspendu')),
    CONSTRAINT ck_lot_dates      CHECK (
        date_fin_reelle IS NULL
        OR date_fin_reelle >= date_os_travaux
    )
);

COMMENT ON TABLE  lot                   IS 'Lot de marché — division technique d''un marché';
COMMENT ON COLUMN lot.date_fin_reelle   IS 'NULL si lot en cours — différent de zéro (convention explicite)';
COMMENT ON COLUMN lot.type_trav_id      IS 'Nature générale du lot — plus fin dans SUBVENTION';

CREATE INDEX idx_lot_marche     ON lot(marche_id);
CREATE INDEX idx_lot_type_trav  ON lot(type_trav_id);

-- ============================================================
-- COUCHE 4 — ASSOCIATIONS N:N PORTEUSES (2 tables)
-- Dépendent des objets métier
-- ============================================================

-- ------------------------------------------------------------
-- INTERVENIR_SUR
-- Association ACTEUR ↔ OPERATION (N:N)
-- Attributs porteurs : role, responsable, date_debut
-- Le rôle MOA/MOE est ici, PAS dans ACTEUR
-- ------------------------------------------------------------
CREATE TABLE intervenir_sur (
    interv_id       SERIAL          PRIMARY KEY,
    acteur_id       INT             NOT NULL    REFERENCES acteur(acteur_id),
    operation_id    INT             NOT NULL    REFERENCES operation(operation_id),
    role            VARCHAR(10)     NOT NULL,
    responsable     VARCHAR(60),
    date_debut      DATE,
    CONSTRAINT uq_interv_acteur_op_role UNIQUE (acteur_id, operation_id, role),
    CONSTRAINT ck_interv_role           CHECK (role IN ('MOA','MOE'))
);

COMMENT ON TABLE  intervenir_sur            IS 'Association N:N ACTEUR ↔ OPERATION — porte le rôle MOA/MOE';
COMMENT ON COLUMN intervenir_sur.role       IS 'MOA=Maître d''Ouvrage MOE=Maître d''Œuvre — décision de modélisation';
COMMENT ON COLUMN intervenir_sur.responsable IS 'Nom du responsable de mission côté acteur';

CREATE INDEX idx_interv_acteur    ON intervenir_sur(acteur_id);
CREATE INDEX idx_interv_operation ON intervenir_sur(operation_id);

-- ------------------------------------------------------------
-- PARTICIPER_AU_LOT
-- Association ENTREPRISE ↔ LOT (N:N)
-- Attributs porteurs : role, montant_attribue, date_debut
-- ------------------------------------------------------------
CREATE TABLE participer_au_lot (
    part_id             SERIAL          PRIMARY KEY,
    lot_id              INT             NOT NULL    REFERENCES lot(lot_id),
    entreprise_id       INT             NOT NULL    REFERENCES entreprise(entreprise_id),
    role                VARCHAR(15)     NOT NULL,
    montant_attribue    DECIMAL(15,2),
    date_debut          DATE,
    CONSTRAINT uq_part_lot_ent  UNIQUE (lot_id, entreprise_id),
    CONSTRAINT ck_part_role     CHECK (role IN ('Mandataire','Co-traitant'))
);

COMMENT ON TABLE  participer_au_lot              IS 'Association N:N ENTREPRISE ↔ LOT — groupement avec rôles';
COMMENT ON COLUMN participer_au_lot.role         IS 'Mandataire=leader signataire Co-traitant=associé technique';
COMMENT ON COLUMN participer_au_lot.montant_attribue IS 'Part du montant lot attribuée à cette entreprise';

CREATE INDEX idx_part_lot        ON participer_au_lot(lot_id);
CREATE INDEX idx_part_entreprise ON participer_au_lot(entreprise_id);

-- ============================================================
-- COUCHE 5 — FAITS MÉTIER (3 tables)
-- Dépendent des objets métier et des référentiels
-- ============================================================

-- ------------------------------------------------------------
-- SUBVENTION
-- Aide financière notifiée — 1 seule mesure : montant_notifie
-- Dépend de : OPERATION, LOT, ORGANISME, TYPE_TRAVAUX
-- ------------------------------------------------------------
CREATE TABLE subvention (
    subvention_id       SERIAL          PRIMARY KEY,
    operation_id        INT             NOT NULL    REFERENCES operation(operation_id),
    lot_id              INT                         REFERENCES lot(lot_id),
    organisme_id        INT             NOT NULL    REFERENCES organisme(organisme_id),
    type_trav_id        INT                         REFERENCES type_travaux(type_trav_id),
    montant_notifie     DECIMAL(15,2)   NOT NULL,
    taux                DECIMAL(5,2),
    date_notification   DATE,
    CONSTRAINT ck_subv_montant  CHECK (montant_notifie > 0),
    CONSTRAINT ck_subv_taux     CHECK (taux IS NULL OR taux BETWEEN 0 AND 100)
);

COMMENT ON TABLE  subvention                  IS 'Subventions notifiées — montant_notifie = seule mesure (décision encadrant)';
COMMENT ON COLUMN subvention.montant_notifie  IS 'Montant signé entre organisme et collectivité — pas de flux trésorerie';
COMMENT ON COLUMN subvention.lot_id           IS 'Nullable — subvention peut couvrir l''opération entière';
COMMENT ON COLUMN subvention.type_trav_id     IS 'Nature précise des travaux subventionnés (AEP, EU, EP…)';

CREATE INDEX idx_subv_operation ON subvention(operation_id);
CREATE INDEX idx_subv_organisme ON subvention(organisme_id);
CREATE INDEX idx_subv_lot       ON subvention(lot_id);

-- ------------------------------------------------------------
-- RISQUE
-- Occurrence d'un risque sur une opération
-- Dépend de : OPERATION, TYPE_RISQUE
-- ------------------------------------------------------------
CREATE TABLE risque (
    risque_id           SERIAL          PRIMARY KEY,
    operation_id        INT             NOT NULL    REFERENCES operation(operation_id),
    type_risque_id      INT             NOT NULL    REFERENCES type_risque(type_risque_id),
    probabilite_pct     INT,
    statut              VARCHAR(15)     NOT NULL    DEFAULT 'Non avéré',
    date_avenement      DATE,
    commentaire         TEXT,
    CONSTRAINT ck_risque_prob   CHECK (probabilite_pct IS NULL OR probabilite_pct BETWEEN 0 AND 100),
    CONSTRAINT ck_risque_statut CHECK (statut IN ('Avéré','Non avéré')),
    CONSTRAINT ck_risque_dates  CHECK (
        statut = 'Non avéré'
        OR date_avenement IS NOT NULL
    )
);

COMMENT ON TABLE  risque                  IS 'Occurrence d''un risque sur une opération — contextualisé vs catalogue';
COMMENT ON COLUMN risque.probabilite_pct  IS 'Probabilité contextualisée — peut différer de type_risque.probabilite_ini';
COMMENT ON COLUMN risque.date_avenement   IS 'NULL si Non avéré — contrainte CHECK encodée';

CREATE INDEX idx_risque_operation   ON risque(operation_id);
CREATE INDEX idx_risque_type_risque ON risque(type_risque_id);

-- ------------------------------------------------------------
-- INDICATEUR_DD
-- Mesure de développement durable par opération
-- Dépend de : OPERATION, TYPE_INDICATEUR
-- Contrainte : 1 seule mesure par opération × type (UNIQUE)
-- ------------------------------------------------------------
CREATE TABLE indicateur_dd (
    ind_id              SERIAL          PRIMARY KEY,
    operation_id        INT             NOT NULL    REFERENCES operation(operation_id),
    type_ind_id         INT             NOT NULL    REFERENCES type_indicateur(type_ind_id),
    valeur_cible        DECIMAL(12,2)   NOT NULL,
    valeur_constatee    DECIMAL(12,2),
    bilan               VARCHAR(15),
    date_mesure         DATE,
    CONSTRAINT uq_ind_op_type   UNIQUE (operation_id, type_ind_id),
    CONSTRAINT ck_ind_bilan     CHECK (bilan IN ('Dépassé','Conforme','En retrait'))
);

COMMENT ON TABLE  indicateur_dd                IS '16 indicateurs DD par opération — UNIQUE(operation_id, type_ind_id)';
COMMENT ON COLUMN indicateur_dd.valeur_cible   IS 'Valeur cible définie à la phase PRO';
COMMENT ON COLUMN indicateur_dd.valeur_constatee IS 'NULL si opération en cours — mesure non encore disponible';
COMMENT ON COLUMN indicateur_dd.bilan          IS 'Calculé par dbt : Dépassé / Conforme / En retrait';

CREATE INDEX idx_ind_operation ON indicateur_dd(operation_id);
CREATE INDEX idx_ind_type      ON indicateur_dd(type_ind_id);

-- ============================================================
-- VUES UTILES
-- ============================================================

-- Vue : résumé financier par opération
CREATE VIEW v_synthese_financiere AS
SELECT
    o.operation_id,
    o.reference_artelia,
    o.intitule,
    c.nom_commune,
    o.complexite,
    MAX(CASE WHEN ef.type_budget = 'budget_programme' THEN ef.montant END) AS budget_programme,
    MAX(CASE WHEN ef.type_budget = 'budget_avp'       THEN ef.montant END) AS budget_avp,
    MAX(CASE WHEN ef.type_budget = 'budget_pro'       THEN ef.montant END) AS budget_pro,
    MAX(CASE WHEN ef.type_budget = 'prix_marche'      THEN ef.montant END) AS prix_marche,
    MAX(CASE WHEN ef.type_budget = 'cout_final'       THEN ef.montant END) AS cout_final,
    COALESCE(SUM(s.montant_notifie), 0)                                    AS total_subventions,
    COALESCE(MAX(CASE WHEN ef.type_budget = 'prix_marche' THEN ef.montant END), 0)
        - COALESCE(SUM(s.montant_notifie), 0)                              AS reste_a_charge
FROM operation o
JOIN commune c                  ON c.commune_id     = o.commune_id
LEFT JOIN estimation_financiere ef ON ef.operation_id = o.operation_id
LEFT JOIN subvention s          ON s.operation_id   = o.operation_id
GROUP BY o.operation_id, o.reference_artelia, o.intitule,
         c.nom_commune, o.complexite;

COMMENT ON VIEW v_synthese_financiere IS 'Vue KPI — budget, subventions et reste à charge par opération';

-- Vue : risques avérés par opération
CREATE VIEW v_risques_averes AS
SELECT
    o.reference_artelia,
    o.intitule,
    c.nom_commune,
    tr.code          AS code_risque,
    tr.description,
    tr.gravite,
    r.probabilite_pct,
    r.date_avenement,
    r.commentaire
FROM risque r
JOIN operation    o  ON o.operation_id    = r.operation_id
JOIN commune      c  ON c.commune_id      = o.commune_id
JOIN type_risque  tr ON tr.type_risque_id = r.type_risque_id
WHERE r.statut = 'Avéré'
ORDER BY r.date_avenement;

COMMENT ON VIEW v_risques_averes IS 'Vue alerte — risques avérés avec contexte opération';

-- Vue : bilan indicateurs DD par opération
CREATE VIEW v_bilan_dd AS
SELECT
    o.reference_artelia,
    c.nom_commune,
    ti.categorie,
    COUNT(*)                                    AS nb_indicateurs,
    SUM(CASE WHEN i.bilan = 'Dépassé'    THEN 1 ELSE 0 END) AS nb_depasses,
    SUM(CASE WHEN i.bilan = 'Conforme'   THEN 1 ELSE 0 END) AS nb_conformes,
    SUM(CASE WHEN i.bilan = 'En retrait' THEN 1 ELSE 0 END) AS nb_en_retrait,
    ROUND(
        100.0 * SUM(CASE WHEN i.bilan IN ('Dépassé','Conforme') THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0), 1
    ) AS taux_conformite_pct
FROM indicateur_dd i
JOIN operation       o  ON o.operation_id = i.operation_id
JOIN commune         c  ON c.commune_id   = o.commune_id
JOIN type_indicateur ti ON ti.type_ind_id = i.type_ind_id
WHERE i.bilan IS NOT NULL
GROUP BY o.reference_artelia, c.nom_commune, ti.categorie
ORDER BY o.reference_artelia, ti.categorie;

COMMENT ON VIEW v_bilan_dd IS 'Vue DD — taux de conformité des indicateurs par opération et catégorie';

-- ============================================================
-- RÉSUMÉ DU SCHÉMA
-- ============================================================
-- Tables référentiels  (6) : commune, acteur, entreprise, phase, organisme, type_travaux
-- Tables catalogues    (2) : type_risque, type_indicateur
-- Tables objets métier (4) : operation, estimation_financiere, marche, lot
-- Tables associations  (2) : intervenir_sur, participer_au_lot
-- Tables faits         (3) : subvention, risque, indicateur_dd
-- Vues                 (3) : v_synthese_financiere, v_risques_averes, v_bilan_dd
-- Total tables         : 17
-- Total index          : 14
-- ============================================================
