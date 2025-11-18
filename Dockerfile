FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt .

# Instalar todas las dependencias (PyTorch CPU incluido en requirements.txt)
# La línea --index-url en requirements.txt fuerza instalación CPU-only
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del backend
COPY backend/ .

# Crear archivo .env vacío (las variables se inyectan vía docker-compose.yml)
# Esto permite que load_dotenv() funcione sin errores
RUN echo "# Variables de entorno cargadas desde docker-compose.yml" > .env

# Crear directorios y establecer permisos
RUN mkdir -p /app/data && \
    chown -R nobody:nogroup /app/data && \
    chmod -R 777 /app/data

EXPOSE 8001

ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/.cache
ENV MODEL_NAME=all-MiniLM-L6-v2

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
