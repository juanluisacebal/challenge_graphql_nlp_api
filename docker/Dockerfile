FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements/ /app/requirements/

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements/prod.txt

# Copiar código fuente
COPY src/ /app/src/
COPY schemas/ /app/schemas/

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"] 