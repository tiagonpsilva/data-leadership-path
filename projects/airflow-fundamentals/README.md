# Airflow Fundamentals

Este projeto tem como objetivo fornecer uma introdução prática ao Apache Airflow, com foco nos conceitos essenciais para um Head de Dados.

## Objetivos de Aprendizado

- Configurar um ambiente Airflow local usando Docker
- Compreender os componentes fundamentais do Airflow (DAGs, Operators, Sensors)
- Implementar padrões comuns de orquestração de dados
- Desenvolver habilidades de monitoramento e troubleshooting
- Aplicar boas práticas de organização e desenvolvimento de DAGs

## Estrutura do Projeto

```
airflow-fundamentals/
├── docker-compose.yml       # Configuração para ambiente Airflow local
├── dags/                    # Diretório com exemplos de DAGs
│   ├── example_etl_dag.py   # Exemplo de pipeline ETL básico
│   ├── example_ml_dag.py    # Exemplo de pipeline para ML
│   └── example_sensor_dag.py # Exemplo com uso de sensores
├── plugins/                 # Plugins e operators customizados
│   └── custom_operators/    # Operators específicos para nossos casos de uso
├── include/                 # Scripts e arquivos auxiliares
│   ├── sql/                 # Queries SQL utilizadas nas DAGs
│   └── python/              # Scripts Python auxiliares
└── tests/                   # Testes para as DAGs e operators
    └── test_dags.py         # Testes básicos de validação de DAGs
```

## Requisitos

- Docker e Docker Compose
- Python 3.8+
- Conhecimentos básicos de SQL e Python

## Como Usar

### Configuração do Ambiente

1. Clone este repositório
2. Navegue até o diretório `airflow-fundamentals`
3. Execute o comando para iniciar o ambiente Airflow:

```bash
docker-compose up -d
```

4. Acesse a UI do Airflow em http://localhost:8080
   - Username: airflow
   - Password: airflow

### Exploração dos Exemplos

O diretório `dags/` contém exemplos progressivos que introduzem diferentes conceitos:

1. **example_etl_dag.py**: Um pipeline ETL básico que demonstra:
   - Extração de dados de uma fonte externa
   - Transformação dos dados usando PythonOperator
   - Carregamento em um destino

2. **example_ml_dag.py**: Um pipeline para Machine Learning que demonstra:
   - Preparação de dados para treinamento
   - Treinamento de modelo
   - Avaliação e registro de métricas
   - Deployment do modelo

3. **example_sensor_dag.py**: Um pipeline que demonstra o uso de sensores para:
   - Aguardar a chegada de arquivos
   - Monitorar a conclusão de outro DAG
   - Implementar padrões de dependência entre DAGs

## Conceitos Abordados

### Componentes Básicos
- DAGs (Directed Acyclic Graphs)
- Operators (BashOperator, PythonOperator, etc.)
- Sensors (FileSensor, ExternalTaskSensor)
- Hooks (conexões com sistemas externos)

### Conceitos Avançados
- XComs (troca de dados entre tasks)
- Branching (execução condicional)
- Subdag (modularização)
- Task Groups (organização visual)
- Dynamic DAGs (geração dinâmica de tarefas)

### Boas Práticas
- Idempotência de tarefas
- Tratamento de erros e retentativas
- Organização e padrões de código
- Monitoramento e observabilidade
- Testes de DAGs

## Recursos Adicionais

- [Documentação oficial do Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html)
- [Airflow: Conceitos e Introdução (Medium)](https://medium.com/data-hackers/apache-airflow-entendendo-o-conceito-de-dag-c0ce5fcb70bb)
- [Best Practices para DAG com Python (Towards Data Science)](https://towardsdatascience.com/data-engineering-how-to-write-your-first-airflow-dag-using-python-1bcb1c88b2b9)
- [Astronomer Academy (Cursos e Tutoriais)](https://academy.astronomer.io/)

## Próximos Passos

Após dominar os conceitos deste projeto, recomenda-se avançar para:

1. Implementação de um pipeline end-to-end usando dados reais
2. Integração do Airflow com outras ferramentas como dbt e Spark
3. Configuração de monitoramento avançado com Prometheus e Grafana
4. Exploração de padrões de governança e qualidade de dados com Airflow
