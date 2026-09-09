{{ config(
    materialized='table',
    schema='mart'
) }}

select
    reference_artelia,
    commune,
    type_subvention,
    organisme,
    montant

from {{ ref('stg_subventions') }}