# Dictionnaire de données — ATLAS

> Basé sur l'analyse des 4 projets pilotes de la Communauté de Communes du Grand Avignon

---

## fact_operations

**Granularité :** 1 ligne = 1 opération × 1 phase  
**Description :** Table de faits centrale. Contient l'évolution budgétaire à chaque phase du cycle de vie.

| Colonne | Type | Description | Exemple | Nullable |
|---------|------|-------------|---------|----------|
| `operation_phase_id` | INTEGER | Clé primaire | 1 | NON |
| `operation_id` | INTEGER | FK → dim_operation | 1 | NON |
| `phase_id` | INTEGER | FK → dim_phase | 2 (PRO) | NON |
| `date_id` | INTEGER | FK → dim_calendrier (YYYYMMDD) | 20211004 | OUI |
| `statut_id` | INTEGER | FK → dim_statut | 1 | OUI |
| `type_id` | INTEGER | FK → dim_type_travaux | 1 (Voirie) | OUI |
| `budget_avp` | DECIMAL(15,2) | Estimation phase AVP | 1 980 000.00 | OUI |
| `budget_pro` | DECIMAL(15,2) | Estimation phase PRO | 2 050 000.00 | OUI |
| `prix_marche` | DECIMAL(15,2) | Prix signé avec ENT (ACT) | 1 950 000.00 | OUI |
| `montant_engage` | DECIMAL(15,2) | Situations de travaux cumulées (DET) | 850 000.00 | OUI |
| `montant_paye` | DECIMAL(15,2) | Montant réellement mandaté | 620 000.00 | OUI |
| `cout_final` | DECIMAL(15,2) | Coût définitif TTC (AOR) | 2 045 000.00 | OUI |
| `montant_avenant` | DECIMAL(15,2) | Total avenants acceptés | 95 000.00 | OUI |
| `date_debut_phase` | DATE | Date de démarrage de la phase | 2021-03-20 | OUI |
| `date_fin_prevue` | DATE | Date de fin contractuelle | 2023-03-20 | OUI |
| `date_fin_reelle` | DATE | Date de fin effective | NULL | OUI |
| `nb_reserves` | INTEGER | Réserves émises à la réception | 3 | OUI |

---

## fact_subventions

**Granularité :** 1 ligne = 1 subvention notifiée  
**Description :** Faits de financement. Séparée de fact_operations pour éviter le double comptage.

| Colonne | Type | Description | Exemple | Nullable |
|---------|------|-------------|---------|----------|
| `subvention_id` | INTEGER | Clé primaire | 1 | NON |
| `operation_id` | INTEGER | FK → dim_operation | 1 | NON |
| `organisme_id` | INTEGER | FK → dim_organisme | 2 (Agence Eau) | NON |
| `type_id` | INTEGER | FK → dim_type_travaux | 4 (AEP) | OUI |
| `lot_id` | INTEGER | Lot du marché concerné (1, 2, 3) | 1 | OUI |
| `date_id` | INTEGER | FK → dim_calendrier | 20220428 | OUI |
| `montant_notifie` | DECIMAL(15,2) | **Seule mesure financière suivie** | 83 000.00 | NON |
| `taux` | DECIMAL(5,2) | Taux de la subvention en % | 8.00 | OUI |
| `date_notification` | DATE | Date de l'acte de notification | 2022-04-28 | OUI |
| `reference_acte` | VARCHAR(50) | Référence de l'acte | NULL | OUI |
| `sujet` | VARCHAR(200) | Nature des travaux subventionnés | Réseau EU | OUI |

---

## fact_indicateurs_dd

**Granularité :** 1 ligne = 1 indicateur × 1 opération  
**Description :** Indicateurs de développement durable — nouveauté issue des données réelles.

| Colonne | Type | Description | Exemple | Nullable |
|---------|------|-------------|---------|----------|
| `indicateur_id` | INTEGER | Clé primaire | 1 | NON |
| `operation_id` | INTEGER | FK → dim_operation | 1 | NON |
| `type_indicateur_id` | INTEGER | FK → dim_type_indicateur_dd | 1 | NON |
| `valeur_cible` | DECIMAL(12,2) | Valeur cible définie au PRO | 1 200.00 | NON |
| `valeur_constatee` | DECIMAL(12,2) | Valeur mesurée à l'avancement | 1 300.00 | OUI |
| `bilan` | VARCHAR(20) | Dépassé / Conforme / En retrait | Dépassé | OUI |
| `date_mesure` | DATE | Date de la mesure constatée | 2023-06-15 | OUI |

---

## dim_operation

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `operation_id` | INTEGER | Clé primaire | 1 |
| `numero_ref_artelia` | VARCHAR(20) | Référence Artelia | 4243946_2301 |
| `intitule` | VARCHAR(200) | Nom de l'opération | Requalification av. de Verdun |
| `territoire_id` | INTEGER | FK → dim_territoire | 1 |
| `moe_id` | INTEGER | FK → dim_moe | 1 |
| `responsable_moe` | VARCHAR(100) | Nom du responsable mission | O. Mozol |
| `responsable_moa` | VARCHAR(100) | Nom du chargé d'opérations DGST | S. Chabert |
| `complexite` | VARCHAR(10) | Faible / Moyenne / Élevée | Moyenne |
| `date_os_moe` | DATE | Ordre de service démarrage MOE | 2021-02-01 |
| `date_ouverture_fiche` | DATE | Date d'ouverture du dossier | 2021-02-07 |
| `is_historique` | BOOLEAN | Données incomplètes (avant système) | false |

---

## dim_phase

| Colonne | Type | Description | Valeurs |
|---------|------|-------------|---------|
| `phase_id` | INTEGER | Clé primaire | 1–5 |
| `code_phase` | VARCHAR(3) | Code court | AVP, PRO, ACT, DET, AOR |
| `libelle_phase` | VARCHAR(60) | Nom complet | Avant-Projet |
| `ordre` | INTEGER | Ordre chronologique | 1–5 |
| `budget_ref` | VARCHAR(30) | Colonne budget produite | budget_avp |

---

## dim_territoire

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `territoire_id` | INTEGER | Clé primaire | 1 |
| `nom_commune` | VARCHAR(100) | Nom de la commune | Les Angles |
| `code_insee` | VARCHAR(5) | Code INSEE | 30010 |
| `nom_communaute` | VARCHAR(100) | Nom de la CC | Communauté de Communes du Grand Avignon |
| `nom_departement` | VARCHAR(100) | Département | Vaucluse |
| `code_departement` | VARCHAR(3) | Code département | 84 |
| `nom_region` | VARCHAR(100) | Région | Provence-Alpes-Côte d'Azur |

---

## dim_organisme

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `organisme_id` | INTEGER | Clé primaire | 1 |
| `nom` | VARCHAR(100) | Nom de l'organisme | Agence de l'Eau Rhône Méditerranée Corse |
| `code_court` | VARCHAR(20) | Code court | Agence Eau RMC |
| `type_organisme` | VARCHAR(30) | État / Région / Département / Agence | Agence |
| `echelon` | VARCHAR(20) | national / régional / départemental | national |
| `nature_eligible` | VARCHAR(100) | Travaux éligibles | Réseau EU |
| `taux_plafond` | DECIMAL(5,2) | Taux plafond indicatif | 8.00 |

---

## dim_type_travaux

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `type_id` | INTEGER | Clé primaire | 4 |
| `libelle` | VARCHAR(60) | Libellé standardisé | Eau potable (AEP) |
| `code_standard` | VARCHAR(10) | Code court | AEP |
| `categorie_dd` | VARCHAR(40) | Catégorie développement durable | Eau |
| `eligible_subvention` | BOOLEAN | Éligible à subvention | true |
| `indicateur_vert` | BOOLEAN | Indicateur environnemental | true |

---

## dim_moe

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `moe_id` | INTEGER | Clé primaire | 1 |
| `nom_moe` | VARCHAR(100) | Nom du cabinet | Artelia |
| `type_moe` | VARCHAR(50) | Type d'intervenant | Bureau d'études |
| `specialite` | VARCHAR(100) | Spécialité principale | VRD, hydraulique urbaine |

---

## dim_type_indicateur_dd

*Nouveauté issue des données réelles — 16 indicateurs identifiés*

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `type_indicateur_id` | INTEGER | Clé primaire | 1 |
| `libelle` | VARCHAR(100) | Libellé de l'indicateur | Surface supplémentaire perméable |
| `categorie` | VARCHAR(20) | Bas-Carbone / Biodiversité / Social | Bas-Carbone |
| `unite` | VARCHAR(20) | Unité de mesure | m² |
| `sens_positif` | VARCHAR(10) | Plus haut = mieux / Plus bas = mieux | Plus haut |

---

## dim_calendrier

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `date_id` | INTEGER | PK format YYYYMMDD | 20210201 |
| `date_complete` | DATE | Date complète | 2021-02-01 |
| `annee` | INTEGER | Année | 2021 |
| `trimestre` | VARCHAR(2) | T1–T4 | T1 |
| `mois` | INTEGER | Mois 1–12 | 2 |
| `mois_label` | VARCHAR(20) | Nom du mois | Février |
| `annee_mandat` | INTEGER | Année du mandat 1–6 | 2 |
| `is_mandat_courant` | BOOLEAN | Appartient au mandat actuel | true |

---

*Dictionnaire de données ATLAS · v1.1 · Août 2025 — mis à jour après analyse des 4 projets pilotes*
