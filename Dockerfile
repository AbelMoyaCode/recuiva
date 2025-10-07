FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt .

# Instalar TODAS las dependencias de una vez (sin cache mount)
RUN pip install --no-cache-dir torch==2.1.0 torchvision==0.23.0 --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY backend/ .

# Crear directorios
RUN mkdir -p /app/data/embeddings /app/data/materials

EXPOSE 80

ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/.cache
ENV MODEL_NAME=all-MiniLM-L6-v2

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
