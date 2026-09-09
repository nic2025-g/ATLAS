{{ config(
    materialized='table',
    schema='mart'
) }}

select
    reference_artelia,
    commune,
    nature,
    complexite,
    moe,
    responsable_moe,
    responsable_moa,
    os_moe,
    ouverture_fiche

from {{ ref('stg_operations') }}