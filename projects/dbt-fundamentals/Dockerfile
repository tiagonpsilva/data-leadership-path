FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git \
        ssh-client \
        software-properties-common \
        make \
        build-essential \
        ca-certificates \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /usr/app

# Copiar requirements
COPY requirements.txt .

# Instalar Python deps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Criar diretório para profiles
RUN mkdir -p /usr/app/profiles

# Copiar arquivo de profiles
COPY profiles/profiles.yml /usr/app/profiles/profiles.yml

# Configurar PATH para comandos dbt
ENV PATH="/usr/local/bin:${PATH}"

# Verificar instalação do dbt
RUN dbt --version

# O contêiner permanecerá em execução para comandos interativos
CMD ["bash"]
