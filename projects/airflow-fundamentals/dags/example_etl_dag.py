"""
### Example ETL DAG

Este DAG exemplifica um pipeline ETL básico com Apache Airflow.
O pipeline extrai dados de uma API externa, realiza transformações
e carrega os dados em um data lake.

Conceitos demonstrados:
- Estrutura básica de um DAG
- Uso de diferentes tipos de operators
- Definição de dependências entre tasks
- Passagem de dados entre tasks com XComs
- Tratamento de erros e retentativas
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.hooks.base import BaseHook
import json
import pandas as pd
from io import StringIO

# Definição dos argumentos default
default_args = {
    'owner': 'data_team',                         # Proprietário do DAG
    'depends_on_past': False,                     # Não depende de execuções passadas
    'email': ['alerts@example.com'],              # Email para notificações
    'email_on_failure': True,                     # Enviar email em caso de falha
    'email_on_retry': False,                      # Não enviar email em caso de retry
    'retries': 3,                                 # Número de tentativas em caso de falha
    'retry_delay': timedelta(minutes=5),          # Tempo de espera entre retries
    'execution_timeout': timedelta(hours=1),      # Tempo máximo de execução
    'start_date': datetime(2025, 4, 29),          # Data de início do DAG
    'tags': ['etl', 'example', 'financial_data']  # Tags para organização
}

# Definição do DAG
dag = DAG(
    'financial_data_etl',                         # ID único do DAG
    default_args=default_args,                    # Argumentos padrão
    description='Pipeline ETL para dados financeiros', # Descrição
    schedule_interval='0 6 * * *',                # Executar diariamente às 6h (cron)
    catchup=False,                                # Não executar para datas passadas
    max_active_runs=1,                            # Máximo de execuções simultâneas
    doc_md=__doc__                                # Documentação do DAG
)

# Funções para as tasks do pipeline
def extract_data(**context):
    """
    Extrai dados da API e retorna como JSON.
    """
    # Simulação de dado recebido da API
    api_data = {
        'date': context['execution_date'].strftime('%Y-%m-%d'),
        'financial_data': [
            {'asset': 'STOCK_A', 'price': 100.5, 'volume': 10000},
            {'asset': 'STOCK_B', 'price': 203.4, 'volume': 5000},
            {'asset': 'STOCK_C', 'price': 54.12, 'volume': 12000}
        ]
    }
    
    # Log para facilitar debugging
    print(f"Dados extraídos: {json.dumps(api_data, indent=2)}")
    
    # Retorna os dados para serem utilizados em etapas futuras
    return api_data

def transform_data(**context):
    """
    Transforma os dados extraídos aplicando regras de negócio.
    """
    # Recupera os dados da task anterior via XCom
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='extract_financial_data')
    
    # Transformação dos dados para o formato desejado
    transformed_data = []
    for item in data['financial_data']:
        # Calcula o valor total transacionado
        total_value = item['price'] * item['volume']
        
        # Adiciona informação de data e valor total
        transformed_item = {
            'date': data['date'],
            'asset': item['asset'],
            'price': item['price'],
            'volume': item['volume'],
            'total_value': total_value,
            'processed_at': datetime.now().isoformat()
        }
        transformed_data.append(transformed_item)
    
    print(f"Dados transformados: {json.dumps(transformed_data, indent=2)}")
    return transformed_data

def load_to_s3(**context):
    """
    Carrega os dados em um bucket S3 no formato parquet.
    """
    # Recupera os dados transformados
    task_instance = context['task_instance']
    data = task_instance.xcom_pull(task_ids='transform_financial_data')
    execution_date = context['execution_date'].strftime('%Y-%m-%d')
    
    # Converte para DataFrame do pandas
    df = pd.DataFrame(data)
    
    # Converte para parquet
    parquet_buffer = StringIO()
    df.to_parquet(parquet_buffer)
    
    # Define o caminho no S3
    s3_path = f"financial_data/date={execution_date}/financial_data.parquet"
    
    # Simulação de carregamento para S3 (em produção usaria S3Hook)
    print(f"Dados carregados em s3://example-bucket/{s3_path}")
    
    # Retorna o caminho do arquivo para referência futura
    return {
        "s3_path": s3_path, 
        "record_count": len(data)
    }

def notify_completion(**context):
    """
    Notifica a conclusão do pipeline com estatísticas.
    """
    # Recupera informações do carregamento
    task_instance = context['task_instance']
    load_result = task_instance.xcom_pull(task_ids='load_to_s3')
    
    # Prepara mensagem de notificação
    message = (
        f"ETL pipeline concluído com sucesso!\n"
        f"Data de execução: {context['execution_date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Arquivo gerado: {load_result['s3_path']}\n"
        f"Registros processados: {load_result['record_count']}"
    )
    
    print(message)
    return message

# Definição das tasks
check_api_availability = HttpSensor(
    task_id='check_api_availability',
    http_conn_id='financial_api',
    endpoint='status',
    response_check=lambda response: response.status_code == 200,
    poke_interval=60,  # verificar a cada 60 segundos
    timeout=600,       # timeout após 10 minutos
    mode='poke',
    dag=dag
)

extract_financial_data = PythonOperator(
    task_id='extract_financial_data',
    python_callable=extract_data,
    provide_context=True,
    dag=dag
)

transform_financial_data = PythonOperator(
    task_id='transform_financial_data',
    python_callable=transform_data,
    provide_context=True,
    dag=dag
)

load_to_s3 = PythonOperator(
    task_id='load_to_s3',
    python_callable=load_to_s3,
    provide_context=True,
    dag=dag
)

notify_completion = PythonOperator(
    task_id='notify_completion',
    python_callable=notify_completion,
    provide_context=True,
    dag=dag
)

# Define o fluxo de execução das tasks
check_api_availability >> extract_financial_data >> transform_financial_data >> load_to_s3 >> notify_completion
