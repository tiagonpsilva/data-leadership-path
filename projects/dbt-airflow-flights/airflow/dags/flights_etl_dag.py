"""
## Flights ETL DAG

Este DAG extrai dados da API de voos, realiza transformações iniciais
e carrega no banco de dados que será usado pelo dbt.

Escrito por: Tiago Silva
Data: 29/04/2025
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models import Variable
import json
import requests
import pandas as pd
from datetime import datetime

# Definição dos argumentos default
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
    'start_date': datetime(2025, 4, 29),
    'tags': ['flights', 'etl', 'api']
}

# Definição do DAG
dag = DAG(
    'flights_etl',
    default_args=default_args,
    description='ETL pipeline para dados de voos da API',
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    doc_md=__doc__
)

# Funções auxiliares
def fetch_flights_data(**context):
    """
    Extrai dados da API de voos e os retorna como JSON.
    """
    # Em um ambiente real, usaríamos uma API key armazenada no Airflow Variables
    # api_key = Variable.get("aviation_api_key")
    
    # Para simulação, usaremos dados fictícios
    # Num ambiente real:
    # url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}"
    # response = requests.get(url)
    # data = response.json()
    
    # Dados simulados
    data = {
        "pagination": {
            "limit": 100,
            "offset": 0,
            "count": 100,
            "total": 324526
        },
        "data": [
            {
                "flight_date": context['ds'],
                "flight_status": "active",
                "departure": {
                    "airport": "San Francisco International",
                    "timezone": "America/Los_Angeles",
                    "iata": "SFO",
                    "icao": "KSFO",
                    "scheduled": "2025-04-29T08:30:00+00:00",
                    "actual": "2025-04-29T08:35:00+00:00",
                    "delay": 5
                },
                "arrival": {
                    "airport": "John F Kennedy International",
                    "timezone": "America/New_York",
                    "iata": "JFK",
                    "icao": "KJFK",
                    "scheduled": "2025-04-29T17:00:00+00:00",
                    "estimated": "2025-04-29T17:10:00+00:00",
                    "delay": 10
                },
                "airline": {
                    "name": "United Airlines",
                    "iata": "UA",
                    "icao": "UAL"
                },
                "flight": {
                    "number": "UA123",
                    "iata": "UA123",
                    "icao": "UAL123"
                },
                "aircraft": {
                    "registration": "N12345",
                    "iata": "B77W",
                    "icao": "B77W",
                    "model": "Boeing 777-300ER"
                }
            },
            {
                "flight_date": context['ds'],
                "flight_status": "landed",
                "departure": {
                    "airport": "Los Angeles International",
                    "timezone": "America/Los_Angeles",
                    "iata": "LAX",
                    "icao": "KLAX",
                    "scheduled": "2025-04-29T07:00:00+00:00",
                    "actual": "2025-04-29T07:15:00+00:00",
                    "delay": 15
                },
                "arrival": {
                    "airport": "O'Hare International",
                    "timezone": "America/Chicago",
                    "iata": "ORD",
                    "icao": "KORD",
                    "scheduled": "2025-04-29T13:00:00+00:00",
                    "actual": "2025-04-29T13:05:00+00:00",
                    "delay": 5
                },
                "airline": {
                    "name": "American Airlines",
                    "iata": "AA",
                    "icao": "AAL"
                },
                "flight": {
                    "number": "AA456",
                    "iata": "AA456",
                    "icao": "AAL456"
                },
                "aircraft": {
                    "registration": "N67890",
                    "iata": "B738",
                    "icao": "B738",
                    "model": "Boeing 737-800"
                }
            }
        ]
    }
    
    print(f"Extraídos {len(data['data'])} voos para a data {context['ds']}")
    
    return data

def process_flights_data(**context):
    """
    Transforma os dados de voos para formatos adequados para o banco de dados.
    """
    # Recupera os dados extraídos da tarefa anterior
    ti = context['ti']
    data = ti.xcom_pull(task_ids='fetch_flights_data')
    
    # Processamento dos voos
    processed_flights = []
    processed_airports = []
    processed_airlines = []
    
    unique_airports = {}
    unique_airlines = {}
    
    # Execução em data de simulação
    execution_date = context['ds']
    
    for flight in data['data']:
        # Processar dados de aeroporto de partida
        if flight['departure']['iata'] not in unique_airports:
            unique_airports[flight['departure']['iata']] = {
                'iata_code': flight['departure']['iata'],
                'icao_code': flight['departure']['icao'],
                'name': flight['departure']['airport'],
                'timezone': flight['departure']['timezone']
            }
        
        # Processar dados de aeroporto de chegada
        if flight['arrival']['iata'] not in unique_airports:
            unique_airports[flight['arrival']['iata']] = {
                'iata_code': flight['arrival']['iata'],
                'icao_code': flight['arrival']['icao'],
                'name': flight['arrival']['airport'],
                'timezone': flight['arrival']['timezone']
            }
        
        # Processar dados de companhia aérea
        if flight['airline']['iata'] not in unique_airlines:
            unique_airlines[flight['airline']['iata']] = {
                'iata_code': flight['airline']['iata'],
                'icao_code': flight['airline']['icao'],
                'name': flight['airline']['name']
            }
        
        # Processar dados do voo
        processed_flight = {
            'flight_date': flight['flight_date'],
            'flight_status': flight['flight_status'],
            'flight_number': flight['flight']['number'],
            'flight_iata': flight['flight']['iata'],
            'flight_icao': flight['flight']['icao'],
            'airline_iata': flight['airline']['iata'],
            'departure_airport_iata': flight['departure']['iata'],
            'arrival_airport_iata': flight['arrival']['iata'],
            'departure_scheduled': flight['departure']['scheduled'],
            'departure_actual': flight['departure'].get('actual', None),
            'departure_delay': flight['departure'].get('delay', 0),
            'arrival_scheduled': flight['arrival']['scheduled'],
            'arrival_actual': flight['arrival'].get('actual', None),
            'arrival_estimated': flight['arrival'].get('estimated', None),
            'arrival_delay': flight['arrival'].get('delay', 0),
            'aircraft_registration': flight['aircraft'].get('registration', None),
            'aircraft_model': flight['aircraft'].get('model', None),
            'extracted_date': execution_date
        }
        
        processed_flights.append(processed_flight)
    
    # Converter dicionários em listas
    for airport_iata, airport_data in unique_airports.items():
        processed_airports.append(airport_data)
    
    for airline_iata, airline_data in unique_airlines.items():
        processed_airlines.append(airline_data)
    
    # Armazenar resultados processados
    context['ti'].xcom_push(key='processed_flights', value=processed_flights)
    context['ti'].xcom_push(key='processed_airports', value=processed_airports)
    context['ti'].xcom_push(key='processed_airlines', value=processed_airlines)
    
    return {
        'flights_count': len(processed_flights),
        'airports_count': len(processed_airports),
        'airlines_count': len(processed_airlines)
    }

def load_flights_to_postgres(**context):
    """
    Carrega os dados processados no PostgreSQL.
    """
    ti = context['ti']
    processed_data = ti.xcom_pull(task_ids='process_flights_data')
    
    # Recuperar dados processados
    processed_flights = ti.xcom_pull(key='processed_flights')
    processed_airports = ti.xcom_pull(key='processed_airports')
    processed_airlines = ti.xcom_pull(key='processed_airlines')
    
    # Conectar ao PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_flights')
    
    # Funções para inserir registros
    def insert_flights(hook, flights):
        if not flights:
            return 0
        
        rows = []
        for flight in flights:
            rows.append(
                (
                    flight['flight_date'], 
                    flight['flight_status'],
                    flight['flight_number'],
                    flight['flight_iata'],
                    flight['flight_icao'],
                    flight['airline_iata'],
                    flight['departure_airport_iata'],
                    flight['arrival_airport_iata'],
                    flight['departure_scheduled'],
                    flight['departure_actual'],
                    flight['departure_delay'],
                    flight['arrival_scheduled'],
                    flight['arrival_actual'],
                    flight['arrival_estimated'],
                    flight['arrival_delay'],
                    flight['aircraft_registration'],
                    flight['aircraft_model'],
                    flight['extracted_date']
                )
            )
        
        # Preparar query
        insert_query = """
        INSERT INTO raw_flights (
            flight_date, flight_status, flight_number, flight_iata, flight_icao,
            airline_iata, departure_airport_iata, arrival_airport_iata,
            departure_scheduled, departure_actual, departure_delay,
            arrival_scheduled, arrival_actual, arrival_estimated, arrival_delay,
            aircraft_registration, aircraft_model, extracted_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (flight_iata, departure_scheduled) 
        DO UPDATE SET
            flight_status = EXCLUDED.flight_status,
            departure_actual = EXCLUDED.departure_actual,
            departure_delay = EXCLUDED.departure_delay,
            arrival_actual = EXCLUDED.arrival_actual,
            arrival_estimated = EXCLUDED.arrival_estimated,
            arrival_delay = EXCLUDED.arrival_delay
        """
        
        # Executar em batch
        hook.insert_rows(table='raw_flights', rows=rows, target_fields=None, commit_every=100, replace=False)
        
        return len(rows)
    
    def insert_airports(hook, airports):
        if not airports:
            return 0
        
        rows = []
        for airport in airports:
            rows.append(
                (
                    airport['iata_code'],
                    airport['icao_code'],
                    airport['name'],
                    airport['timezone']
                )
            )
        
        # Preparar query
        insert_query = """
        INSERT INTO raw_airports (iata_code, icao_code, name, timezone)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (iata_code) 
        DO UPDATE SET
            name = EXCLUDED.name,
            timezone = EXCLUDED.timezone
        """
        
        # Executar em batch
        hook.insert_rows(table='raw_airports', rows=rows, target_fields=None, commit_every=100, replace=False)
        
        return len(rows)
    
    def insert_airlines(hook, airlines):
        if not airlines:
            return 0
        
        rows = []
        for airline in airlines:
            rows.append(
                (
                    airline['iata_code'],
                    airline['icao_code'],
                    airline['name']
                )
            )
        
        # Preparar query
        insert_query = """
        INSERT INTO raw_airlines (iata_code, icao_code, name)
        VALUES (%s, %s, %s)
        ON CONFLICT (iata_code) 
        DO UPDATE SET
            name = EXCLUDED.name
        """
        
        # Executar em batch
        hook.insert_rows(table='raw_airlines', rows=rows, target_fields=None, commit_every=100, replace=False)
        
        return len(rows)
    
    # Executar inserções
    flights_inserted = insert_flights(pg_hook, processed_flights)
    airports_inserted = insert_airports(pg_hook, processed_airports)
    airlines_inserted = insert_airlines(pg_hook, processed_airlines)
    
    return {
        'flights_inserted': flights_inserted,
        'airports_inserted': airports_inserted,
        'airlines_inserted': airlines_inserted
    }

# Definição das tarefas
create_tables = PostgresOperator(
    task_id='create_tables',
    postgres_conn_id='postgres_flights',
    sql="""
    -- Tabela de aeroportos
    CREATE TABLE IF NOT EXISTS raw_airports (
        iata_code VARCHAR(10) PRIMARY KEY,
        icao_code VARCHAR(10),
        name VARCHAR(200),
        timezone VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabela de companhias aéreas
    CREATE TABLE IF NOT EXISTS raw_airlines (
        iata_code VARCHAR(10) PRIMARY KEY,
        icao_code VARCHAR(10),
        name VARCHAR(200),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Tabela de voos
    CREATE TABLE IF NOT EXISTS raw_flights (
        id SERIAL PRIMARY KEY,
        flight_date DATE,
        flight_status VARCHAR(50),
        flight_number VARCHAR(20),
        flight_iata VARCHAR(20),
        flight_icao VARCHAR(20),
        airline_iata VARCHAR(10),
        departure_airport_iata VARCHAR(10),
        arrival_airport_iata VARCHAR(10),
        departure_scheduled TIMESTAMP,
        departure_actual TIMESTAMP,
        departure_delay INT,
        arrival_scheduled TIMESTAMP,
        arrival_actual TIMESTAMP,
        arrival_estimated TIMESTAMP,
        arrival_delay INT,
        aircraft_registration VARCHAR(20),
        aircraft_model VARCHAR(100),
        extracted_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(flight_iata, departure_scheduled)
    );
    
    -- Índices para melhorar performance de queries
    CREATE INDEX IF NOT EXISTS idx_flights_date ON raw_flights(flight_date);
    CREATE INDEX IF NOT EXISTS idx_flights_airline ON raw_flights(airline_iata);
    CREATE INDEX IF NOT EXISTS idx_flights_departure ON raw_flights(departure_airport_iata);
    CREATE INDEX IF NOT EXISTS idx_flights_arrival ON raw_flights(arrival_airport_iata);
    """,
    dag=dag
)

check_api = HttpSensor(
    task_id='check_api',
    http_conn_id='aviation_api',
    endpoint='status',
    response_check=lambda response: response.status_code == 200,
    poke_interval=60,
    timeout=300,
    mode='reschedule',
    dag=dag
)

fetch_flights_data = PythonOperator(
    task_id='fetch_flights_data',
    python_callable=fetch_flights_data,
    provide_context=True,
    dag=dag
)

process_flights_data = PythonOperator(
    task_id='process_flights_data',
    python_callable=process_flights_data,
    provide_context=True,
    dag=dag
)

load_flights_to_postgres = PythonOperator(
    task_id='load_flights_to_postgres',
    python_callable=load_flights_to_postgres,
    provide_context=True,
    dag=dag
)

# Definição das dependências
# A task de verificação da API é desativada em ambiente de desenvolvimento
# check_api >> fetch_flights_data >> process_flights_data >> load_flights_to_postgres
create_tables >> fetch_flights_data >> process_flights_data >> load_flights_to_postgres
