# Usar imagem oficial do Python
FROM python:3.9-slim

# Evitar que o Python gere arquivos .pyc e garantir output em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir diretório de trabalho
WORKDIR /code

# Instalar dependências do sistema necessárias para psycopg2 e outras
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . /code/

# Comando para rodar a aplicação
CMD ["python", "main.py"]
