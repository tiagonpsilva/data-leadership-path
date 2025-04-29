# dbt Fundamentals

Este projeto tem como objetivo fornecer uma introdução prática ao dbt (data build tool), com foco nos conceitos essenciais para um Head de Dados.

## Objetivos de Aprendizado

- Compreender o paradigma de Analytics Engineering e como o dbt se encaixa nele
- Desenvolver habilidades no design e implementação de modelos de dados usando dbt
- Implementar testes de dados e documentação como parte do workflow
- Aplicar padrões de modelagem como Kimball e Data Vault
- Configurar pipelines CI/CD para modelos dbt

## Estrutura do Projeto

```
dbt-fundamentals/
├── docker-compose.yml       # Ambiente local com PostgreSQL e dbt
├── models/                  # Modelos dbt organizados por camadas
│   ├── staging/             # Camada de staging
│   ├── intermediate/        # Camada intermediária
│   │   ├── intermediate_models.sql
│   │   └── intermediate_schema.yml
│   └── marts/               # Camada de marts (consumo)
│       ├── finance/         # Marts organizados por domínio
│       └── marketing/
├── seeds/                   # Arquivos CSV para testes e desenvolvimento
├── macros/                  # Funções reutilizáveis em SQL
├── tests/                   # Testes personalizados
│   └── test_data_quality.sql
├── analyses/                # Análises ad-hoc
├── snapshots/               # Implementação de SCD (slowly changing dimensions)
└── dbt_project.yml          # Arquivo de configuração do projeto
```

## Requisitos

- Docker e Docker Compose
- Conhecimentos básicos de SQL
- Familiaridade com conceitos de data warehouse

## Conceitos Abordados

### Fundamentos
- Estrutura e filosofia do dbt
- Modelos e materialização (view, table, incremental, ephemeral)
- Testes (unique, not_null, relationships, accepted_values)
- Documentação e lineage automática

### Modelagem de Dados
- Implementação do padrão Kimball (fatos e dimensões)
- Técnicas de modelagem dimensional
- Padrões de nomenclatura e organização

### Recursos Avançados
- Macros para extensão de funcionalidade
- Snapshots para SCD Tipo 2
- Seeds para dados de referência
- Hooks para execução de código personalizado

### Integração e CI/CD
- Uso de variáveis e ambientes
- Testes automatizados em pipeline CI/CD
- Integração com sistemas de controle de versão

## Como Usar

### Configuração do Ambiente

1. Clone este repositório
2. Navegue até o diretório `dbt-fundamentals`
3. Execute o comando para iniciar o ambiente:

```bash
docker-compose up -d
```

4. Conecte-se ao contêiner dbt para executar comandos:

```bash
docker-compose exec dbt bash
```

5. Execute o comando de inicialização do projeto:

```bash
dbt run
```

## Recursos Adicionais

- [Documentação oficial do dbt](https://docs.getdbt.com/)
- [Curso dbt Fundamentals](https://courses.getdbt.com/collections)
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Awesome dbt (recursos comunitários)](https://github.com/Hiflylabs/awesome-dbt)

## Próximos Passos

Após dominar os conceitos fundamentais deste projeto, recomenda-se avançar para:

1. Integração do dbt com Airflow para orquestração de cargas
2. Implementação de um modelo de governança de dados usando dbt e metadados
3. Uso do dbt para qualidade de dados e validação em pipelines de ML
