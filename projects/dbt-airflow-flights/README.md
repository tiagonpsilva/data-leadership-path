# Integração dbt + Airflow: Análise de Dados de Voos

Este projeto demonstra a integração entre Apache Airflow e dbt para criar um pipeline end-to-end de dados de voos, consumindo uma API pública de voos e transformando os dados para análise.

## Objetivos de Aprendizado

- Implementar a integração entre Airflow (orquestração) e dbt (transformação)
- Desenvolver pipelines de dados completos, desde a extração até a análise
- Aplicar práticas de monitoramento e gerenciamento de qualidade dos dados
- Implementar padrões de design para operadores personalizados no Airflow
- Criar um fluxo de dados reproduzível e documentado

## Arquitetura da Solução

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   API de    │    │   Airflow   │    │  PostgreSQL │    │     dbt     │
│    Voos     │───►│  Extração   │───►│  Raw Data   │───►│Transformação│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                          │                                      │
                          │                                      │
                          ▼                                      ▼
                    ┌─────────────┐                      ┌─────────────┐
                    │  Airflow    │                      │  Data Marts │
                    │Monitoramento│                      │  (Análise)  │
                    └─────────────┘                      └─────────────┘
```

## Estrutura do Projeto

```
dbt-airflow-flights/
├── airflow/                      # Configuração do Airflow
│   ├── dags/                     # DAGs do pipeline
│   │   ├── flights_etl_dag.py    # DAG principal para ETL
│   │   └── dbt_dag.py            # DAG para orquestração do dbt
│   ├── plugins/                  # Plugins e operadores customizados
│   │   └── operators/            # Operadores para API de voos
│   └── include/                  # Scripts auxiliares
│       └── api/                  # Wrappers de API
├── dbt/                          # Projeto dbt
│   ├── models/                   # Modelos organizados por camadas
│   │   ├── staging/              # Modelos de staging
│   │   ├── intermediate/         # Modelos intermediários 
│   │   └── marts/                # Modelos para análise
│   ├── tests/                    # Testes de dados
│   ├── macros/                   # Macros SQL reutilizáveis
│   └── dbt_project.yml           # Configuração do dbt
├── docker/                       # Arquivos Docker
│   ├── airflow.Dockerfile        # Dockerfile para Airflow 
│   └── dbt.Dockerfile            # Dockerfile para dbt
└── docker-compose.yml            # Composição dos serviços
```

## API de Voos Utilizada

Este projeto utiliza a [Aviation Stack API](https://aviationstack.com/) que oferece dados em tempo real de voos, incluindo:
- Status de voos
- Dados de aeroportos e companhias aéreas
- Rotas e rastreamento de aeronaves

Alternativas gratuitas incluem:
- [Open Sky Network API](https://opensky-network.org/apidoc/)
- [Aviation Edge API](https://aviation-edge.com/) (versão gratuita limitada)

## Conceitos e Tecnologias

### Airflow
- Implementação de DAGs com dependências
- Sensores para verificação de disponibilidade da API
- Operadores personalizados para interagir com APIs de voos
- Uso de XComs para transferência de dados entre tarefas
- Monitoramento e alertas de falhas

### dbt
- Modelagem incremental para processamento eficiente
- Testes de qualidade de dados
- Documentação automática dos modelos
- Macros para padronização de transformações
- Geração de documentação para análise de linhagem de dados

### Integração
- Uso do dbt através do BashOperator no Airflow
- Passagem de parâmetros de execução do Airflow para o dbt
- Validação de pré-requisitos antes da execução do dbt
- Monitoramento consolidado dos dois sistemas

## Análises Geradas

O projeto gera as seguintes análises a partir dos dados coletados:

1. **Análise de pontualidade por companhia aérea**
2. **Estatísticas de ocupação por rota e período**
3. **Análise de causas de atrasos por aeroporto**
4. **Dashboard operacional de voos ativos**
5. **Previsão de demanda por rota**

## Como Usar

1. Clone este repositório
2. Configure as credenciais da API de voos no arquivo `.env`
3. Execute o ambiente com Docker Compose:

```bash
docker-compose up -d
```

4. Acesse a interface do Airflow em `http://localhost:8080`
5. Acesse a documentação do dbt em `http://localhost:8081`

## Próximos Passos

Após dominar este projeto, sugere-se:

1. Adicionar testes automáticos para validar os pipelines
2. Implementar monitoramento avançado com Prometheus + Grafana
3. Desenvolver uma camada de API para expor os dados processados
4. Implementar previsões utilizando ML com os dados capturados
