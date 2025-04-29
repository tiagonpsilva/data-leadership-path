with source_data as (
    select
        id as order_id,
        customer_id,
        order_date,
        status,
        amount
    from raw_orders
)

select * from source_data