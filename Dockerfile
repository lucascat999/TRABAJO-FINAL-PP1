# Imagen oficial de Python 3.11 slim
FROM python:3.11-slim

# Instalar dependencias del sistema que necesite Django + PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero (aprovecha caché de Docker)
COPY requirements.txt /app/

# Instalar paquetes Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código fuente
COPY . /app/

# Script de entrada (migrate + runserver)
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Puerto que expone Django
EXPOSE 8000

# Comando por defecto
CMD ["/app/entrypoint.sh"]