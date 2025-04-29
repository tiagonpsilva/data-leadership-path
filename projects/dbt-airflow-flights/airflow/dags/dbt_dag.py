"""
## dbt Integration DAG

Este DAG executa modelos dbt para transformação e análise de dados de voos.
Ele depende da conclusão bem-sucedida do DAG flights_etl.

Escrito por: Tiago Silva
Data: 29/04/2025
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
import os
import json

# Definição dos argumentos default
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=1),
    'start_date': datetime(2025, 4, 29),
    'tags': ['dbt', 'flights', 'transformation']
}

# Definição do DAG
dag = DAG(
    'dbt_flights_transformations',
    default_args=default_args,
    description='Executa transformações dbt em dados de voos',
    schedule_interval='0 10 * * *',  # Executa às 10h, após o ETL
    catchup=False,
    max_active_runs=1,
    doc_md=__doc__
)

# Variáveis de ambiente
DBT_PROJECT_DIR = '/opt/airflow/dbt'  # Caminho para o projeto dbt no container
DBT_PROFILES_DIR = '/opt/airflow/dbt/profiles'
DBT_TARGET = 'prod'

# Funções auxiliares
def check_flights_data_availability(**context):
    """
    Verifica se há dados de voos disponíveis para a data de execução.
    """
    execution_date = context['ds']
    
    # Conexão com o banco
    pg_hook = PostgresHook(postgres_conn_id='postgres_flights')
    
    # Consulta para verificar dados para a data atual
    query = f"""
    SELECT COUNT(*) as flight_count 
    FROM raw_flights 
    WHERE flight_date = '{execution_date}'
    """
    
    result = pg_hook.get_first(query)
    flight_count = result[0]
    
    print(f"Encontrados {flight_count} voos para {execution_date}")
    
    # Se tiver dados, prossegue com o dbt
    if flight_count > 0:
        return 'dbt_run'
    else:
        return 'no_data_available'

def run_dbt_tests(**context):
    """
    Executa testes dbt e decide se deve continuar o pipeline ou não.
    """
    # Em um ambiente real, avaliaria os resultados do comando `dbt test`
    # e tomaria uma decisão baseada nos resultados.
    
    # Para simplificar este exemplo, consideramos que os testes passaram
    tests_passed = True
    
    if tests_passed:
        return 'generate_docs'
    else:
        return 'send_test_failure_notification'

def generate_dbt_docs(**context):
    """
    Gera documentação dbt a partir dos resultados das transformações.
    """
    # Em um ambiente real, processaria o resultado da geração de documentação
    # e armazenaria métricas ou informações relevantes.
    
    print("Documentação dbt gerada com sucesso")
    
    # Retorna informações sobre a documentação
    return {
        'docs_generated': True,
        'docs_path': '/opt/airflow/dbt/target/index.html',
        'generated_at': datetime.now().isoformat()
    }

def log_run_results(**context):
    """
    Processa e registra os resultados da execução do dbt.
    """
    task_instance = context['task_instance']
    
    # Em um ambiente real, processaria o arquivo run_results.json gerado pelo dbt
    # Para este exemplo, simularemos o resultado
    run_results = {
        'execution_time': 45.2,  # segundos
        'models_executed': 8,
        'models_success': 8,
        'models_error': 0,
        'models_skipped': 0
    }
    
    print(f"Execução dbt concluída: {run_results['models_success']} modelos com sucesso em {run_results['execution_time']:.1f}s")
    
    # Armazena métricas para uso posterior
    task_instance.xcom_push(key='dbt_metrics', value=run_results)
    
    return run_results

# Definição das tarefas
# Sensor para aguardar a conclusão do DAG de ETL
wait_for_etl = ExternalTaskSensor(
    task_id='wait_for_etl',
    external_dag_id='flights_etl',
    external_task_id='load_flights_to_postgres',
    mode='poke',
    poke_interval=300,  # Verificar a cada 5 minutos
    timeout=3600,  # Timeout de 1 hora
    dag=dag
)

# Verificação de disponibilidade de dados
check_data = BranchPythonOperator(
    task_id='check_flights_data',
    python_callable=check_flights_data_availability,
    provide_context=True,
    dag=dag
)

# Notificação de dados indisponíveis
no_data = BashOperator(
    task_id='no_data_available',
    bash_command='echo "Não há dados para a data de execução. O processamento será interrompido."',
    dag=dag
)

# Grupo de tarefas dbt
with TaskGroup(group_id='dbt_tasks', dag=dag) as dbt_tasks:
    
    # Execução do dbt run
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=f'cd {DBT_PROJECT_DIR} && DBT_PROFILES_DIR={DBT_PROFILES_DIR} dbt run --target {DBT_TARGET} --models tag:daily',
        env={
            'DBT_PROFILES_DIR': DBT_PROFILES_DIR,
            'DBT_TARGET': DBT_TARGET,
            'EXECUTION_DATE': '{{ ds }}'
        },
        dag=dag
    )
    
    # Execução dos testes dbt
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command=f'cd {DBT_PROJECT_DIR} && DBT_PROFILES_DIR={DBT_PROFILES_DIR} dbt test --target {DBT_TARGET} --models tag:daily',
        env={
            'DBT_PROFILES_DIR': DBT_PROFILES_DIR,
            'DBT_TARGET': DBT_TARGET
        },
        dag=dag
    )
    
    # Verificação dos resultados dos testes
    check_tests = BranchPythonOperator(
        task_id='check_test_results',
        python_callable=run_dbt_tests,
        provide_context=True,
        dag=dag
    )
    
    # Geração de documentação
    generate_docs = BashOperator(
        task_id='generate_docs',
        bash_command=f'cd {DBT_PROJECT_DIR} && DBT_PROFILES_DIR={DBT_PROFILES_DIR} dbt docs generate --target {DBT_TARGET}',
        env={
            'DBT_PROFILES_DIR': DBT_PROFILES_DIR,
            'DBT_TARGET': DBT_TARGET
        },
        dag=dag
    )
    
    # Processamento dos resultados
    process_results = PythonOperator(
        task_id='process_results',
        python_callable=log_run_results,
        provide_context=True,
        dag=dag
    )
    
    # Notificação de falha nos testes
    test_failure = BashOperator(
        task_id='send_test_failure_notification',
        bash_command='echo "Falha nos testes dbt. Verifique os logs para mais detalhes."',
        dag=dag
    )
    
    # Processamento de documentação
    process_docs = PythonOperator(
        task_id='process_docs',
        python_callable=generate_dbt_docs,
        provide_context=True,
        dag=dag
    )
    
    # Definição de dependências dentro do grupo
    dbt_run >> dbt_test >> check_tests
    check_tests >> generate_docs >> process_docs >> process_results
    check_tests >> test_failure

# Definição de dependências do DAG
wait_for_etl >> check_data
check_data >> [no_data, dbt_tasks]
