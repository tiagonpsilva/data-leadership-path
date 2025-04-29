# Projeto End-to-End: Pipeline Integrado de Dados

Este projeto demonstra uma arquitetura completa de processamento de dados que integra todas as principais tecnologias do ecossistema moderno de dados: PostgreSQL, Apache Airflow, Apache Spark, dbt e Prometheus para monitoramento.

## Objetivo

Criar uma plataforma de dados completa e escalável que demonstre como implementar:
- Ingestão e processamento de dados em batch e streaming
- Transformações e modelagem dimensional
- Governança e qualidade de dados
- Monitoramento e observabilidade
- Orquestração e operacionalização

## Arquitetura

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              PIPELINE END-TO-END                              │
│                                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │ Fontes  │    │ Ingestão│    │Armazena-│    │Transfor-│    │   Data  │     │
│  │de Dados │───►│ (Airflow│───►│  mento  │───►│  mação  │───►│  Marts  │     │
│  │         │    │   API)  │    │(Postgre)│    │  (dbt)  │    │         │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                      │                             ▲                          │
│                      │                             │                          │
│                      ▼                             │                          │
│                 ┌─────────┐                   ┌─────────┐                     │
│                 │Processa-│                   │Cataloga-│                     │
│                 │  mento  │──────────────────►│   ção   │                     │
│                 │ (Spark) │                   │         │                     │
│                 └─────────┘                   └─────────┘                     │
│                                                                              │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐     │
│  │  API    │    │ Alertas │    │Dashboards│   │Documenta│    │ Testes  │     │
│  │de Dados │◄───┤Prometheus◄───┤ Grafana │◄───┤   ção   │◄───┤Automatizados  │
│  │         │    │         │    │         │    │         │    │         │     │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Componentes do Sistema

### 1. Fontes de Dados
- API pública de dados financeiros
- Banco de dados transacional PostgreSQL
- Arquivos CSV e JSON (dados históricos)
- Simulação de dados em streaming

### 2. Ingestão e Orquestração (Apache Airflow)
- DAGs para processamento batch
- Sensores para detecção de novos dados
- Operadores personalizados para fontes específicas
- Orquestração do workflow completo

### 3. Processamento (Apache Spark)
- Processamento de dados em larga escala
- Agregações e transformações complexas
- Validação e limpeza de dados
- Processamento de dados históricos

### 4. Armazenamento (PostgreSQL)
- Camada raw para dados brutos
- Armazenamento intermediário
- Tabelas finais para análise
- Versionamento e rastreabilidade

### 5. Transformação e Modelagem (dbt)
- Modelos incrementais
- Testes de qualidade de dados
- Documentação automática
- Modelagem dimensional

### 6. Monitoramento (Prometheus/Grafana)
- Métricas de performance
- Alertas em tempo real
- Dashboards operacionais
- Monitoramento de SLAs

## Caso de Uso: Análise Financeira

O pipeline processará dados financeiros de diferentes fontes para criar:

1. **Dashboard de Performance Financeira**
   - Indicadores-chave de performance
   - Análises de tendências
   - Alertas de desvios

2. **Modelo de Predição de Fluxo de Caixa**
   - Previsão de receitas e despesas
   - Análise de cenários

3. **Relatórios Regulatórios Automatizados**
   - Conformidade com requisitos legais
   - Geração automática de relatórios

## Estrutura do Projeto

```
end-to-end-pipeline/
├── docker-compose.yml                # Configuração dos serviços
├── airflow/                          # Configuração do Airflow
│   ├── dags/                         # DAGs para orquestração
│   │   ├── ingest_financial_data.py  # Ingestão de dados financeiros
│   │   ├── spark_processing.py       # Orquestração do Spark
│   │   └── dbt_transformations.py    # Orquestração do dbt
│   └── plugins/                      # Plugins personalizados
├── spark/                            # Aplicações Spark
│   ├── jobs/                         # Jobs Spark
│   │   ├── data_cleaning.py          # Limpeza de dados
│   │   └── feature_engineering.py    # Preparação de features
│   └── config/                       # Configurações do Spark
├── dbt/                              # Projeto dbt
│   ├── models/                       # Modelos dbt
│   │   ├── staging/                  # Camada de staging
│   │   ├── intermediate/             # Camada intermediária
│   │   └── marts/                    # Data marts
│   ├── tests/                        # Testes de dados
│   └── dbt_project.yml               # Configuração do dbt
├── postgres/                         # Configuração do PostgreSQL
│   └── init/                         # Scripts de inicialização
├── monitoring/                       # Configuração de monitoramento
│   ├── prometheus/                   # Configuração do Prometheus
│   └── grafana/                      # Dashboards do Grafana
└── scripts/                          # Scripts utilitários
    ├── setup.sh                      # Script de setup inicial
    └── seed_data.py                  # Geração de dados de exemplo
```

## Ferramentas e Tecnologias

- **Apache Airflow**: Orquestração e scheduling
- **Apache Spark**: Processamento distribuído
- **PostgreSQL**: Armazenamento relacional
- **dbt (data build tool)**: Transformação e modelagem
- **Prometheus**: Monitoramento e alertas
- **Grafana**: Visualização e dashboards
- **Docker/Docker Compose**: Conteinerização

## Como Usar

### Pré-requisitos
- Docker e Docker Compose
- Git
- Pelo menos 8GB de RAM disponível

### Instalação e Execução

1. Clone este repositório
2. Execute o script de configuração inicial:
   ```
   ./scripts/setup.sh
   ```
3. Inicie todos os serviços:
   ```
   docker-compose up -d
   ```
4. Acesse os serviços:
   - Airflow UI: http://localhost:8080
   - PostgreSQL: localhost:5432
   - Spark UI: http://localhost:4040
   - Grafana: http://localhost:3000

### Executando o Pipeline

1. Ative o DAG principal no Airflow UI
2. Monitore a execução através do Airflow UI
3. Verifique os resultados no dashboard do Grafana

## Melhores Práticas Demonstradas

1. **Arquitetura em Camadas**
   - Separação clara entre ingestão, armazenamento e transformação
   - Princípio de responsabilidade única

2. **Governança de Dados**
   - Rastreamento de linhagem de dados
   - Testes automatizados de qualidade
   - Documentação integrada

3. **DevOps para Dados**
   - Infraestrutura como código
   - Conteinerização completa
   - Monitoramento e alertas integrados

4. **Segurança**
   - Credenciais gerenciadas de forma segura
   - Princípio de menor privilégio
   - Auditoria de acesso

## Desafios e Aprendizados

Este projeto aborda desafios comuns em pipelines de dados empresariais:

1. **Integração de Tecnologias Diversas**
   - Como fazer diferentes ferramentas trabalharem juntas
   - Gerenciamento de dependências e compatibilidade

2. **Balanceamento de Performance e Custo**
   - Estratégias de otimização
   - Escalabilidade sob demanda

3. **Qualidade e Confiabilidade**
   - Testes automatizados
   - Monitoramento proativo
   - Recuperação de falhas

## Próximos Passos

- Implementação de processamento em tempo real com Spark Streaming
- Adição de machine learning para previsões avançadas
- Expansão do monitoramento para métricas de negócio
- Integração com sistemas de BI
