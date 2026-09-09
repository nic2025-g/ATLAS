with lots as (

    select
        reference_artelia,
        sum(montant_marche_ht) as total_lots

    from {{ ref('stg_lots') }}

    group by reference_artelia
),

marche as (

    select
        reference_artelia,
        montant_ht as budget_marche

    from {{ ref('stg_budgets') }}

    where phase = 'MARCHE'
)

select
    l.reference_artelia,
    l.total_lots,
    m.budget_marche

from lots l

join marche m
    on l.reference_artelia = m.reference_artelia

where l.total_lots <> m.budget_marche