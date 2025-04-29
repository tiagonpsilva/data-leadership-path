{{{
    config(
        materialized='table',
        tags=['finance', 'daily']
    )
}}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders as (
    select * from {{ ref('stg_orders') }}
),

customer_orders as (
    select
        customers.customer_id,
        customers.first_name,
        customers.last_name,
        customers.email,
        min(orders.order_date) as first_order_date,
        max(orders.order_date) as most_recent_order_date,
        count(orders.order_id) as number_of_orders,
        sum(orders.amount) as lifetime_value
    from customers
    left join orders on customers.customer_id = orders.customer_id
    group by 1, 2, 3, 4
)

select * from customer_orders