select
    trim(reference_artelia) as reference_artelia,
    trim(commune) as commune,
    trim(indicateur) as indicateur,

    nullif(trim(valeur_cible), '') as valeur_cible,
    nullif(trim(valeur_constatee), '') as valeur_constatee,
    nullif(trim(bilan), '') as bilan

from {{ source('raw', 'indicateurs_dd') }}