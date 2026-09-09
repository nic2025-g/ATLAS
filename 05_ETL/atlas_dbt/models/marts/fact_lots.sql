{{ config(
    materialized='table',
    schema='mart'
) }}

select
    l.reference_artelia,
    l.lot_id_source,
    l.numero_lot,
    l.libelle_lot,
    l.montant_marche_ht,
    l.entreprise_mandataire,
    l.cotraitants,

    -- Montant réel issu de la source métier.
    l.montant_paye,

    -- Dates réellement extraites des documents métier.
    l.date_debut_travaux,
    l.date_fin_prevue,
    l.date_fin_reelle,

    -- Valeur arbitraire utilisée uniquement pour la démonstration.
    p.montant_paye_simule,

    case
        when p.montant_paye_simule is not null then true
        else false
    end as montant_paye_est_simule

from {{ ref('stg_lots') }} l

left join {{ ref('paiements_lots_simules') }} p
    on l.lot_id_source = p.lot_id_source