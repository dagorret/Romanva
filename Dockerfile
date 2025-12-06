FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       curl \
       build-essential \
       default-libmysqlclient-dev \
       pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Instalar dependencias Python
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . /code/

# Crear directorios necesarios
RUN mkdir -p /code/data /code/staticfiles

EXPOSE 8008

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8008/ || exit 1
