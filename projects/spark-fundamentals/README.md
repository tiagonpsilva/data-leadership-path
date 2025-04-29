# Spark Fundamentals

Este projeto tem como objetivo fornecer uma introdução prática ao Apache Spark, com foco nos conceitos essenciais para um Head de Dados liderar equipes e projetos que utilizam processamento distribuído.

## Objetivos de Aprendizado

- Compreender a arquitetura e os principais componentes do Apache Spark
- Implementar operações fundamentais usando Spark SQL, DataFrame e RDD APIs
- Aplicar padrões de otimização para jobs Spark
- Desenvolver habilidades de troubleshooting e debugging de aplicações Spark
- Compreender técnicas de monitoramento e gerenciamento de recursos

## Arquitetura do Ambiente

```
┌─────────────────────────────────────────────────────────────┐
│                       Docker Compose                        │
│                                                             │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐             │
│  │  Spark    │   │  Spark    │   │  Spark    │             │
│  │  Master   │   │  Worker 1 │   │  Worker 2 │             │
│  └───────────┘   └───────────┘   └───────────┘             │
│        │               │               │                    │
│        └───────────────┼───────────────┘                    │
│                        │                                    │
│  ┌───────────┐   ┌───────────┐   ┌───────────┐             │
│  │  Jupyter  │   │   MinIO   │   │ PostgreSQL│             │
│  │ Notebook  │   │  (S3-like)│   │           │             │
│  └───────────┘   └───────────┘   └───────────┘             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Estrutura do Projeto

```
spark-fundamentals/
├── docker-compose.yml              # Configuração do ambiente Spark
├── notebooks/                      # Jupyter notebooks com exemplos
│   ├── 01_spark_basics.ipynb       # Fundamentos do Spark
│   ├── 02_dataframe_operations.ipynb # Operações com DataFrames
│   ├── 03_spark_sql.ipynb          # Spark SQL
│   ├── 04_spark_streaming.ipynb    # Introdução ao Spark Streaming
│   └── 05_spark_ml.ipynb           # Machine Learning com Spark
├── jobs/                           # Jobs Spark standalone
│   ├── batch_processing.py         # Exemplo de processamento em batch
│   ├── streaming_example.py        # Exemplo de streaming
│   └── ml_pipeline.py              # Pipeline de ML
├── data/                           # Dados de exemplo
│   ├── raw/                        # Dados brutos para processamento
│   └── reference/                  # Dados de referência
└── docs/                           # Documentação adicional
    ├── spark_architecture.md       # Arquitetura do Spark
    ├── performance_tuning.md       # Guia de otimização
    └── troubleshooting.md          # Guia de solução de problemas
```

## Conceitos Abordados

### Fundamentos do Spark
- Arquitetura do Spark (Driver, Executor, SparkContext)
- Diferenças entre RDDs, DataFrames e Datasets
- Lazy evaluation e plano de execução
- Persistência e particionamento

### Operações com DataFrames
- Leitura e escrita de dados (CSV, JSON, Parquet, JDBC)
- Operações de transformação (select, filter, groupBy)
- Funções de janela (window functions)
- Manipulação de dados temporais e complexos

### Spark SQL
- Criação e uso de tabelas temporárias
- Consultas SQL avançadas
- Integração com fontes de dados externas
- Performance de queries SQL vs. DataFrame API

### Spark Streaming
- Conceitos básicos de streaming
- Processamento de streaming estruturado
- Operações de janela deslizante e agregações
- Integração com sistemas como Kafka

### Spark MLlib
- Pipeline de machine learning
- Algoritmos comuns (classificação, regressão, clustering)
- Feature engineering em escala
- Avaliação e deployment de modelos

## Recursos de Performance e Otimização
- Estratégias de particionamento
- Broadcast joins vs. shuffle joins
- Gerenciamento de memória
- Monitoramento e debugging
- Tunning de aplicações Spark

## Como Usar

### Requisitos
- Docker e Docker Compose
- Conhecimentos básicos de Python
- Familiaridade com SQL

### Instalação
1. Clone este repositório
2. Navegue até o diretório `spark-fundamentals`
3. Execute o ambiente com Docker Compose:

```bash
docker-compose up -d
```

4. Acesse o Jupyter Notebook em `http://localhost:8888`
5. Acesse a UI do Spark em `http://localhost:8080`
6. Acesse o MinIO em `http://localhost:9001`

### Execução de Jobs Spark
Para executar jobs Spark diretamente:

```bash
# Acessar o contêiner do Spark
docker exec -it spark-master bash

# Executar um job Spark
spark-submit --master spark://spark-master:7077 /jobs/batch_processing.py
```

## Aplicações Práticas

O projeto inclui exemplos práticos que demonstram cenários comuns de uso do Spark:

1. **Processamento de logs de servidores web**: Análise de padrões de tráfego, detecção de anomalias e geração de dashboards de monitoramento.

2. **Análise de dados de vendas**: Processamento de grandes volumes de transações para identificar tendências, sazonalidades e oportunidades de cross-selling.

3. **Processamento de dados de sensores IoT**: Ingestão e análise de streams de dados de dispositivos conectados, com detecção de eventos em tempo real.

4. **Recomendação de produtos**: Implementação de algoritmos de recomendação utilizando filtragem colaborativa e técnicas de embeddings.

## Melhores Práticas

O projeto apresenta e segue as seguintes melhores práticas para desenvolvimento com Spark:

- Estrutura modular e reutilizável para jobs
- Padrões para processamento de erros e dados inválidos
- Técnicas de logging e monitoramento eficaz
- Estratégias de teste para aplicações Spark
- Integração com sistemas de versionamento e CI/CD

## Recursos Adicionais

- [Documentação oficial do Apache Spark](https://spark.apache.org/docs/latest/)
- [Spark: The Definitive Guide](https://www.oreilly.com/library/view/spark-the-definitive/9781491912201/)
- [Learning Spark, 2nd Edition](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/)
- [Spark GitHub Repository](https://github.com/apache/spark)
- [Databricks Blog](https://databricks.com/blog)

## Próximos Passos

Após dominar os conceitos fundamentais deste projeto, recomenda-se explorar:

1. Spark Structured Streaming em produção
2. Integração com Delta Lake para transações ACID
3. Arquiteturas modernas como Lakehouse
4. Spark em ambientes Kubernetes
5. Integração do Spark com ferramentas de ML Ops
