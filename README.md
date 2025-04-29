# 🎯 Liderança em Dados (Modern Data Stack)

## 🔍 Sobre este Projeto

Este repositório documenta uma jornada de desenvolvimento para liderança em Modern Data Stack, combinando aspectos técnicos e estratégicos necessários para liderar equipes de dados em uma empresa de grande porte do setor financeiro.

## 📋 Índice de Conceitos

1. **🏗️ [Arquitetura de Dados](./docs/README.md)** - Visão de plataforma, ADRs e frameworks de decisão
2. **🔄 [Projetos Práticos](./projects/README.md)** - Implementações com Airflow, dbt, Spark e monitoramento
3. **📊 [Estudos de Caso](./case-studies/README.md)** - Cenários reais de tomada de decisão
4. **👥 [Laboratório de Liderança](./leadership-lab/README.md)** - Desenvolvimento de habilidades de gestão
5. **🚀 [Projetos End-to-End](./end-to-end/README.md)** - Integrações completas com documentação

## 🌟 Objetivo

Desenvolver as competências necessárias para:
- Liderar equipes multidisciplinares de dados
- Projetar e implementar arquiteturas modernas e escaláveis
- Gerenciar projetos end-to-end com valor mensurável
- Comunicar efetivamente com stakeholders
- Equilibrar aspectos técnicos e de gestão

## 🔍 Estrutura

Cada pasta numerada contém um README com explicações detalhadas e arquivos adicionais com casos de uso específicos:

- **/docs** - Documentação estratégica e decisões arquiteturais
- **/projects** - Implementações práticas de tecnologias específicas
- **/case-studies** - Análises de cenários reais
- **/leadership-lab** - Templates e recursos de liderança
- **/end-to-end** - Projetos integrados completos

## 🛠️ Stack Tecnológica

| Categoria | Componente | Tecnologias |
|-----------|------------|-------------|
| **Ingestão** | Batch | Fivetran, Airbyte, Apache NiFi, AWS DMS, Logstash |
| | Streaming | Kafka Connect, Debezium (CDC) |
| | API | REST APIs, GraphQL, gRPC |
| **Processamento** | Batch | Apache Spark, dbt |
| | Streaming | Kafka Streams, Spark Structured Streaming, Kinesis |
| | ETL/ELT | Apache Spark, dbt, Airflow |
| **Orquestração** | | Apache Airflow |
| **Armazenamento** | Data Warehouses | Google BigQuery, Amazon Redshift, Databricks SQL |
| | Data Lakes | Delta Lake, Apache Iceberg, AWS S3 |
| | Bancos Operacionais | PostgreSQL, MySQL, MongoDB, Cassandra/ScyllaDB, Redis |
| **Governança de Dados** | Catálogo de Dados | Amundsen (mais popular em open-source) ou Collibra (mais popular comercial) |
| | Qualidade de Dados | dbt Tests |
| | Linhagem de Dados | dbt Lineage |
| | Gestão de Metadados | Apache Atlas |
| **Monitoramento** | Métricas e Alertas | Prometheus, Grafana |
| | Logs e Traces | ELK Stack, OpenTelemetry |
| **Visualização** | BI e Analytics | Tableau, Looker, Power BI |
| **Segurança e Compliance** | Gestão de Acessos | HashiCorp Vault (infraestrutura) ou Okta (identidade, mais popular) |
| **DevOps/DataOps** | CI/CD | GitHub Actions |
| | Infraestrutura como Código | Terraform |
| | Containerização e Orquestração | Docker, Kubernetes |

## 📚 Recursos Principais

- [Roadmap de Desenvolvimento](ROADMAP.md) - Plano detalhado de 90 dias
- [Documentação da Plataforma](./docs/platform-vision.md) - Visão técnica e estratégica
- [Frameworks de Decisão](./docs/decision-frameworks.md) - Guias para tomada de decisão

## Desafios e Cenários

Este repositório aborda cenários reais como:
- Gestão de incidentes em pipelines críticos
- Resolução de conflitos de prioridade entre áreas de negócio
- Modernização de plataforma (ex: migração Redshift para Snowflake)
- Otimização de orçamento com aumento de demandas
- Desenvolvimento de cultura orientada a dados

## Como Contribuir

Sugestões e contribuições são bem-vindas através de issues e pull requests!
