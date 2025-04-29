"""
## Financial Data Ingestion Pipeline

Este DAG implementa a ingestão de dados financeiros de várias fontes, incluindo:
- API pública de dados financeiros
- Arquivos CSV com dados históricos
- Banco de dados transacional

Os dados são validados, transformados e carregados no data lake para
processamento posterior pelo pipeline Spark e pelo dbt.

Autor: Tiago Silva
Data: 29/04/2025
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
import json
import csv
import requests
import pandas as pd
import os
from pathlib import Path

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
    'tags': ['finance', 'ingestion', 'etl']
}

# Definição do DAG
dag = DAG(
    'financial_data_ingestion',
    default_args=default_args,
    description='Pipeline de ingestão de dados financeiros',
    schedule_interval='0 6 * * *',  # Executa diariamente às 6h
    catchup=False,
    max_active_runs=1,
    doc_md=__doc__
)

# Funções auxiliares
def _get_current_data_date(**context):
    """
    Determina a data de referência para os dados a serem processados.
    Por padrão, usa a data de execução, mas pode ser sobrescrita por parâmetro.
    """
    # Verificar se há data específica nos parâmetros
    params = context.get('params', {})
    if 'data_date' in params and params['data_date']:
        data_date = params['data_date']
    else:
        # Usar data de execução - 1 dia para garantir dados completos
        data_date = (context['execution_date'] - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Armazenar a data para uso em outras tarefas
    context['ti'].xcom_push(key='data_date', value=data_date)
    return data_date

def _fetch_api_data(**context):
    """
    Busca dados da API financeira.
    Em um cenário real, usaríamos uma chave de API e endpoint real.
    """
    # Obter a data de referência
    data_date = context['ti'].xcom_pull(key='data_date')
    
    # Em um cenário real, teríamos um endpoint e chave de API
    # api_key = Variable.get("finance_api_key", default_var="demo_key")
    # url = f"https://api.financial-data.com/stocks/daily?date={data_date}&apikey={api_key}"
    
    # Simulação de chamada de API
    # response = requests.get(url)
    # api_data = response.json()
    
    # Para este exemplo, simulamos os dados da API
    api_data = {
        "metadata": {
            "date": data_date,
            "symbols": 100,
            "status": "success"
        },
        "data": [
            {
                "symbol": "AAPL",
                "date": data_date,
                "open": 185.21,
                "high": 186.89,
                "low": 184.67,
                "close": 186.45,
                "volume": 56782310,
                "exchange": "NASDAQ"
            },
            {
                "symbol": "MSFT",
                "date": data_date,
                "open": 302.89,
                "high": 306.12,
                "low": 301.54,
                "close": 305.79,
                "volume": 25678124,
                "exchange": "NASDAQ"
            },
            {
                "symbol": "GOOGL",
                "date": data_date,
                "open": 138.45,
                "high": 139.87,
                "low": 138.01,
                "close": 139.62,
                "volume": 18956234,
                "exchange": "NASDAQ"
            }
            # Em um cenário real, teríamos centenas de stocks aqui
        ]
    }
    
    # Salvar os dados para posterior processamento
    output_path = f"/tmp/api_data_{data_date}.json"
    with open(output_path, 'w') as outfile:
        json.dump(api_data, outfile)
    
    # Retornar informações sobre os dados obtidos
    return {
        "data_date": data_date,
        "symbols_count": len(api_data["data"]),
        "output_path": output_path
    }

def _validate_api_data(**context):
    """
    Valida os dados obtidos da API para garantir qualidade.
    """
    # Obter informações da tarefa anterior
    task_info = context['ti'].xcom_pull(task_ids='fetch_api_data')
    data_path = task_info['output_path']
    
    # Carregar os dados
    with open(data_path, 'r') as infile:
        api_data = json.load(infile)
    
    # Validações básicas
    validation_errors = []
    
    # 1. Verificar se há dados
    if len(api_data["data"]) == 0:
        validation_errors.append("Nenhum dado recebido da API")
    
    # 2. Verificar campos obrigatórios
    required_fields = ["symbol", "date", "open", "high", "low", "close", "volume", "exchange"]
    missing_fields = []
    
    for item in api_data["data"]:
        for field in required_fields:
            if field not in item:
                missing_fields.append(f"Campo '{field}' ausente para o símbolo {item.get('symbol', 'UNKNOWN')}")
    
    if missing_fields:
        validation_errors.append("\n".join(missing_fields))
    
    # 3. Verificar valores válidos (exemplo)
    invalid_values = []
    for item in api_data["data"]:
        if "volume" in item and (not isinstance(item["volume"], (int, float)) or item["volume"] <= 0):
            invalid_values.append(f"Volume inválido para {item['symbol']}: {item['volume']}")
    
    if invalid_values:
        validation_errors.append("\n".join(invalid_values))
    
    # Decidir o próximo passo com base na validação
    if validation_errors:
        # Registrar erros
        error_log = f"/tmp/validation_errors_{task_info['data_date']}.log"
        with open(error_log, 'w') as outfile:
            outfile.write("\n".join(validation_errors))
        
        context['ti'].xcom_push(key='validation_status', value='failed')
        context['ti'].xcom_push(key='validation_errors', value=error_log)
        return 'send_validation_failure_notification'
    else:
        context['ti'].xcom_push(key='validation_status', value='success')
        return 'load_to_raw_database'

def _load_data_to_database(**context):
    """
    Carrega os dados validados no banco de dados raw.
    """
    # Obter informações da tarefa de coleta de dados
    task_info = context['ti'].xcom_pull(task_ids='fetch_api_data')
    data_path = task_info['output_path']
    data_date = task_info['data_date']
    
    # Carregar os dados
    with open(data_path, 'r') as infile:
        api_data = json.load(infile)
    
    # Conectar ao PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_pipeline')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # Preparar inserção em lote
    insert_query = """
    INSERT INTO raw_stock_prices 
    (symbol, trading_date, open_price, high_price, low_price, close_price, volume, exchange, ingestion_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (symbol, trading_date) 
    DO UPDATE SET
        open_price = EXCLUDED.open_price,
        high_price = EXCLUDED.high_price,
        low_price = EXCLUDED.low_price,
        close_price = EXCLUDED.close_price,
        volume = EXCLUDED.volume,
        exchange = EXCLUDED.exchange,
        ingestion_date = EXCLUDED.ingestion_date
    """
    
    # Processar e inserir os dados
    records = []
    for item in api_data["data"]:
        records.append((
            item["symbol"],
            item["date"],
            item["open"],
            item["high"],
            item["low"],
            item["close"],
            item["volume"],
            item["exchange"],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
    
    try:
        cursor.executemany(insert_query, records)
        conn.commit()
        
        # Registrar sucesso
        context['ti'].xcom_push(key='load_status', value='success')
        context['ti'].xcom_push(key='records_loaded', value=len(records))
        
        return {
            'data_date': data_date,
            'records_processed': len(records),
            'status': 'success'
        }
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def _process_historical_data(**context):
    """
    Processa dados históricos de CSV para complementar dados da API.
    Em um ambiente real, isso pode ser de fontes externas ou backfill.
    """
    # Obter a data de referência
    data_date = context['ti'].xcom_pull(key='data_date')
    
    # Em um ambiente real, buscaríamos em um local específico
    # Aqui simulamos um arquivo CSV
    historical_data = [
        {"symbol": "AMZN", "date": data_date, "open": 125.67, "high": 126.98, "low": 125.01, "close": 126.45, "volume": 38291045, "exchange": "NASDAQ"},
        {"symbol": "FB", "date": data_date, "open": 201.34, "high": 204.56, "low": 200.87, "close": 203.98, "volume": 28765432, "exchange": "NASDAQ"},
        {"symbol": "TSLA", "date": data_date, "open": 267.89, "high": 270.12, "low": 265.43, "close": 269.75, "volume": 45678912, "exchange": "NASDAQ"}
    ]
    
    # Salvar em CSV temporário
    output_path = f"/tmp/historical_data_{data_date}.csv"
    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ["symbol", "date", "open", "high", "low", "close", "volume", "exchange"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in historical_data:
            writer.writerow(row)
    
    return {
        "data_date": data_date,
        "records_count": len(historical_data),
        "output_path": output_path
    }

def _send_notification(**context):
    """
    Envia notificação de conclusão com estatísticas.
    """
    # Em um ambiente real, enviaríamos email, Slack, etc.
    # Aqui apenas registramos
    api_results = context['ti'].xcom_pull(task_ids='load_to_raw_database')
    historical_results = context['ti'].xcom_pull(task_ids='load_historical_data')
    
    message = f"""
    Pipeline de ingestão de dados financeiros concluído com sucesso.
    
    Data de referência: {context['ti'].xcom_pull(key='data_date')}
    Registros da API processados: {api_results['records_processed']}
    Registros históricos processados: {historical_results['records_count']}
    
    Data/hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    print(message)
    return {"status": "notified", "timestamp": datetime.now().isoformat()}

def _send_error_notification(**context):
    """
    Envia notificação de erro na validação.
    """
    # Em um ambiente real, enviaríamos email, Slack, etc.
    # Aqui apenas registramos
    error_log = context['ti'].xcom_pull(key='validation_errors')
    
    message = f"""
    ERRO: Falha na validação de dados financeiros.
    
    Data de referência: {context['ti'].xcom_pull(key='data_date')}
    Log de erros: {error_log}
    
    Data/hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    print(message)
    return {"status": "error_notified", "timestamp": datetime.now().isoformat()}

def _load_historical_data(**context):
    """
    Carrega dados históricos no banco de dados.
    """
    # Obter informações da tarefa de processamento de dados históricos
    task_info = context['ti'].xcom_pull(task_ids='process_historical_data')
    csv_path = task_info['output_path']
    
    # Carregar o CSV em um DataFrame
    df = pd.read_csv(csv_path)
    
    # Conectar ao PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres_pipeline')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    # Preparar inserção em lote
    insert_query = """
    INSERT INTO raw_stock_prices 
    (symbol, trading_date, open_price, high_price, low_price, close_price, volume, exchange, ingestion_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (symbol, trading_date) 
    DO UPDATE SET
        open_price = EXCLUDED.open_price,
        high_price = EXCLUDED.high_price,
        low_price = EXCLUDED.low_price,
        close_price = EXCLUDED.close_price,
        volume = EXCLUDED.volume,
        exchange = EXCLUDED.exchange,
        ingestion_date = EXCLUDED.ingestion_date
    """
    
    # Processar e inserir os dados
    records = []
    for _, row in df.iterrows():
        records.append((
            row["symbol"],
            row["date"],
            row["open"],
            row["high"],
            row["low"],
            row["close"],
            row["volume"],
            row["exchange"],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
    
    try:
        cursor.executemany(insert_query, records)
        conn.commit()
        return {"records_count": len(records), "status": "success"}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

# Definição das tarefas do DAG

# Tarefa para criar tabela se não existir
create_tables = PostgresOperator(
    task_id='create_tables',
    postgres_conn_id='postgres_pipeline',
    sql="""
    CREATE TABLE IF NOT EXISTS raw_stock_prices (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10) NOT NULL,
        trading_date DATE NOT NULL,
        open_price NUMERIC(10, 2) NOT NULL,
        high_price NUMERIC(10, 2) NOT NULL,
        low_price NUMERIC(10, 2) NOT NULL,
        close_price NUMERIC(10, 2) NOT NULL,
        volume BIGINT NOT NULL,
        exchange VARCHAR(20) NOT NULL,
        ingestion_date TIMESTAMP NOT NULL,
        UNIQUE(symbol, trading_date)
    );
    
    CREATE INDEX IF NOT EXISTS idx_stock_symbol ON raw_stock_prices(symbol);
    CREATE INDEX IF NOT EXISTS idx_stock_date ON raw_stock_prices(trading_date);
    """,
    dag=dag
)

# Obter a data de referência para os dados
get_data_date = PythonOperator(
    task_id='get_data_date',
    python_callable=_get_current_data_date,
    provide_context=True,
    dag=dag
)

# Verificar se a API está disponível
check_api = HttpSensor(
    task_id='check_api',
    http_conn_id='financial_api',
    endpoint='status',
    request_params={},
    response_check=lambda response: response.status_code == 200,
    poke_interval=60,  # verificar a cada 60 segundos
    timeout=600,  # timeout após 10 minutos
    mode='poke',
    dag=dag
)

# Buscar dados da API
fetch_api_data = PythonOperator(
    task_id='fetch_api_data',
    python_callable=_fetch_api_data,
    provide_context=True,
    dag=dag
)

# Validar dados da API
validate_api_data = BranchPythonOperator(
    task_id='validate_api_data',
    python_callable=_validate_api_data,
    provide_context=True,
    dag=dag
)

# Enviar notificação em caso de falha na validação
send_validation_failure_notification = PythonOperator(
    task_id='send_validation_failure_notification',
    python_callable=_send_error_notification,
    provide_context=True,
    dag=dag
)

# Carregar dados validados no banco de dados
load_to_raw_database = PythonOperator(
    task_id='load_to_raw_database',
    python_callable=_load_data_to_database,
    provide_context=True,
    dag=dag
)

# Processar dados históricos complementares
process_historical_data = PythonOperator(
    task_id='process_historical_data',
    python_callable=_process_historical_data,
    provide_context=True,
    dag=dag
)

# Carregar dados históricos no banco de dados
load_historical_data = PythonOperator(
    task_id='load_historical_data',
    python_callable=_load_historical_data,
    provide_context=True,
    dag=dag
)

# Enviar notificação de sucesso
send_success_notification = PythonOperator(
    task_id='send_success_notification',
    python_callable=_send_notification,
    provide_context=True,
    trigger_rule='none_failed',
    dag=dag
)

# Tarefa para acionar o processamento Spark (em um ambiente real)
trigger_spark_processing = BashOperator(
    task_id='trigger_spark_processing',
    bash_command='echo "Triggering Spark job for data processing" && exit 0',
    dag=dag
)

# Definição das dependências do DAG
create_tables >> get_data_date >> check_api >> fetch_api_data >> validate_api_data

validate_api_data >> [load_to_raw_database, send_validation_failure_notification]

load_to_raw_database >> process_historical_data >> load_historical_data >> send_success_notification

send_success_notification >> trigger_spark_processing
