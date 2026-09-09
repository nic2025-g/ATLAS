{{ config(
    materialized='table',
    schema='mart'
) }}

select
    reference_artelia,
    phase,
    montant_ht

from {{ ref('stg_budgets') }}