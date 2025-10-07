FROM python:3.10-slim

# Metadatos
LABEL maintainer="Abel Moya <amoya2@upao.edu.pe>"
LABEL description="Recuiva Backend - API REST con FastAPI y Embeddings Semánticos"

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del backend
COPY backend/ .

# Crear directorios necesarios
RUN mkdir -p /app/data/embeddings /app/data/materials

EXPOSE 80

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/.cache
ENV HOST=0.0.0.0
ENV PORT=80

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
