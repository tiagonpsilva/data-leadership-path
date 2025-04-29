with source_data as (
    select
        id as customer_id,
        first_name,
        last_name,
        email,
        created_at
    from raw_customers
)

select * from source_data