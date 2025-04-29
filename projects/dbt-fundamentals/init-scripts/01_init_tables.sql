-- Criação das tabelas de exemplo para o projeto dbt

-- Tabela de clientes
CREATE TABLE raw_customers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de pedidos
CREATE TABLE raw_orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES raw_customers(id),
    order_date DATE,
    status VARCHAR(20),
    amount DECIMAL(10,2)
);

-- Inserir dados de exemplo em clientes
INSERT INTO raw_customers (first_name, last_name, email)
VALUES
('John', 'Doe', 'john.doe@example.com'),
('Jane', 'Smith', 'jane.smith@example.com'),
('Robert', 'Johnson', 'robert.johnson@example.com'),
('Emily', 'Williams', 'emily.williams@example.com'),
('Michael', 'Brown', 'michael.brown@example.com');

-- Inserir dados de exemplo em pedidos
INSERT INTO raw_orders (customer_id, order_date, status, amount)
VALUES
(1, '2025-01-15', 'completed', 120.50),
(1, '2025-02-20', 'completed', 75.00),
(2, '2025-01-10', 'shipped', 65.75),
(3, '2025-03-05', 'completed', 220.00),
(4, '2025-02-28', 'cancelled', 30.25),
(5, '2025-03-10', 'placed', 185.50),
(1, '2025-03-15', 'shipped', 97.30),
(3, '2025-03-20', 'completed', 155.90),
(2, '2025-03-25', 'placed', 45.20),
(5, '2025-03-30', 'shipped', 210.75);

-- Criar o schema para dbt
CREATE SCHEMA IF NOT EXISTS dbt_demo;