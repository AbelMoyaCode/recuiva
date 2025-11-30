# ═══════════════════════════════════════════════════════════════════════
# STAGE 1: Builder - Instalar dependencias
# ═══════════════════════════════════════════════════════════════════════
FROM python:3.10-slim AS builder

WORKDIR /app

# Copiar requirements primero para cache de Docker
COPY backend/requirements.txt .

# Instalar dependencias de Python en un virtualenv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar dependencias con optimizaciones de espacio
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    # Limpiar cache de pip
    rm -rf /root/.cache/pip && \
    # Eliminar archivos innecesarios de PyTorch
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -name "*.pyc" -delete 2>/dev/null || true

# ═══════════════════════════════════════════════════════════════════════
# STAGE 2: Runtime - Imagen final ligera
# ═══════════════════════════════════════════════════════════════════════
FROM python:3.10-slim

WORKDIR /app

# Instalar solo dependencias de runtime (sin build-essential)
# ✅ Agregamos ocrmypdf para pre-procesar PDFs corruptos
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-spa \
    tesseract-ocr-eng \
    poppler-utils \
    ghostscript \
    ocrmypdf \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Verificar instalación de Tesseract y ocrmypdf
RUN tesseract --version && tesseract --list-langs && ocrmypdf --version

# Copiar virtualenv desde builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar código del backend
COPY backend/ .

# Crear archivo .env vacío y directorios
RUN echo "# Variables de entorno cargadas desde docker-compose.yml" > .env && \
    mkdir -p /app/data && \
    chown -R nobody:nogroup /app/data && \
    chmod -R 777 /app/data

EXPOSE 8001

ENV PYTHONUNBUFFERED=1
ENV TRANSFORMERS_CACHE=/app/.cache
ENV MODEL_NAME=all-MiniLM-L6-v2

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
