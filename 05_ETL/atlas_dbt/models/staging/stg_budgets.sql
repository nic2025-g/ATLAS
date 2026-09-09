select
    trim(reference_artelia) as reference_artelia,
    upper(trim(phase)) as phase,

    case
        when montant_ht = '' then null
        else montant_ht::numeric
    end as montant_ht

from {{ source('raw', 'budgets') }}