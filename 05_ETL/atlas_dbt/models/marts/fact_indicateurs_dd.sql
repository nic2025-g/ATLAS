{{ config(
    materialized='table',
    schema='mart'
) }}

select
    reference_artelia,
    commune,
    indicateur,
    valeur_cible,
    valeur_constatee,
    bilan

from {{ ref('stg_indicateurs_dd') }}