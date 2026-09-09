select
    trim(reference_artelia) as reference_artelia,
    trim(lot_id_source) as lot_id_source,

    case
        when numero_lot = '' then null
        else numero_lot::integer
    end as numero_lot,

    trim(libelle_lot) as libelle_lot,

    case
        when montant_marche_ht = '' then null
        else montant_marche_ht::numeric
    end as montant_marche_ht,

    nullif(trim(entreprise_mandataire), '') as entreprise_mandataire,
    nullif(trim(cotraitants), '') as cotraitants,

    case
        when montant_paye = '' then null
        else montant_paye::numeric
    end as montant_paye,

    case
        when date_debut_travaux = '' then null
        else to_date(date_debut_travaux, 'DD/MM/YYYY')
    end as date_debut_travaux,

    case
        when date_fin_prevue = '' then null
        else to_date(date_fin_prevue, 'DD/MM/YYYY')
    end as date_fin_prevue,

    case
        when date_fin_reelle = '' then null
        else to_date(date_fin_reelle, 'DD/MM/YYYY')
    end as date_fin_reelle

from {{ source('raw', 'lots') }}