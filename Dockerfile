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

# Configurar cache de pip para persistir entre builds
ENV PIP_CACHE_DIR=/opt/pip-cache
RUN mkdir -p $PIP_CACHE_DIR

# Instalar torch PRIMERO (capa separada para mejor caching)
RUN --mount=type=cache,target=/opt/pip-cache \
    pip install torch==2.1.0 torchvision==0.23.0 --extra-index-url https://download.pytorch.org/whl/cpu

# Copiar requirements y instalar otras dependencias
COPY backend/requirements.txt .
RUN --mount=type=cache,target=/opt/pip-cache \
    pip install -r requirements.txt

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
ENV MODEL_NAME=all-MiniLM-L6-v2

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:80/ || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
