select
    trim(reference_artelia) as reference_artelia,
    trim(commune) as commune,
    nullif(trim(nature), '') as nature,
    trim(complexite) as complexite,
    trim(moe) as moe,
    trim(responsable_moe) as responsable_moe,
    nullif(trim(responsable_moa), '') as responsable_moa,

    case
        when os_moe = '' then null
        else to_date(os_moe, 'DD/MM/YYYY')
    end as os_moe,

    case
        when ouverture_fiche = '' then null
        else to_date(ouverture_fiche, 'DD/MM/YYYY')
    end as ouverture_fiche

from {{ source('raw', 'operations') }}