# 🏗️ Arquitetura de Dados

## 📝 Definição

Esta seção contém a documentação estratégica da plataforma de dados, incluindo decisões arquiteturais, visão técnica e frameworks de decisão.

## 🔄 Como Funciona

```mermaid
%%{init: { "themeVariables": { "fontFamily": "Arial", "fontSize": "10px" } }}%%
graph TD
    A[Visão de Plataforma] --> B[ADRs]
    A --> C[Haikus Arquiteturais]
    B --> D[Decisões Técnicas]
    C --> D
    D --> E[Implementação]
    D --> F[Prototipagem Local (DuckDB)]
```

## 📊 Tipos Principais

### 📑 ADRs (Architecture Decision Records)
Documentação das decisões arquiteturais significativas tomadas no projeto, incluindo contexto, consequências e status.

### 📜 Haikus Arquiteturais
Representações concisas e poéticas de conceitos arquiteturais complexos, facilitando a comunicação e memorização.

### 🎯 Frameworks de Decisão
Guias estruturados para tomada de decisão em diferentes contextos da plataforma de dados.

> **Nota:** Para experimentação, prototipagem e workloads locais, recomenda-se o uso do DuckDB como engine SQL embutido, facilitando testes rápidos, POCs e integração com notebooks Python/R.

## 🔗 Casos de Uso

- [ADRs](./adr/README.md) - Registro de decisões arquiteturais
- [Haikus](./architecture-haikus/README.md) - Haikus arquiteturais
- [Visão de Plataforma](./platform-vision.md) - Documento de visão técnica 