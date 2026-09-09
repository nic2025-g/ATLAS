select
    trim(reference_artelia) as reference_artelia,
    trim(commune) as commune,
    upper(trim(type_subvention)) as type_subvention,
    trim(organisme) as organisme,

    case
        when montant = '' then null
        else montant::numeric
    end as montant

from {{ source('raw', 'subventions') }}