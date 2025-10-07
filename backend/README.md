# 🧠 Recuiva Backend - API con FastAPI

Backend profesional para el sistema de Active Recall con validación semántica mediante IA.

## 🚀 Características

- ✅ **API REST** con FastAPI
- ✅ **Embeddings** con Sentence Transformers (modelo MiniLM)
- ✅ **Chunking inteligente** de textos largos (80+ páginas)
- ✅ **Validación semántica** con similaridad coseno
- ✅ **Procesamiento de PDF** y archivos TXT
- ✅ **Base de datos vectorial** en JSON
- ✅ **CORS configurado** para desarrollo frontend

## 📋 Requisitos

- Python 3.9+
- 4GB RAM mínimo (para el modelo de embeddings)
- 2GB espacio en disco

## 🔧 Instalación

### 1. Crear entorno virtual

```bash
cd backend
python -m venv venv
```

### 2. Activar entorno virtual

**Windows:**
```powershell
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```powershell
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env según tus necesidades
```

## ▶️ Ejecución

### Modo Desarrollo (Recomendado)

```bash
python main.py
```

O con uvicorn directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Modo Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

La API estará disponible en: **http://localhost:8000**

## 📡 Endpoints Principales

### 🏠 Raíz
```http
GET /
```
Información general de la API

### 📤 Subir Material
```http
POST /api/materials/upload
Content-Type: multipart/form-data

Body:
- file: archivo PDF o TXT (mínimo 80 páginas recomendado)
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "material_id": 1,
  "message": "Material procesado exitosamente: 156 chunks generados",
  "data": {
    "id": 1,
    "filename": "matematicas_discretas.pdf",
    "total_chunks": 156,
    "total_characters": 234567
  }
}
```

### ✅ Validar Respuesta
```http
POST /api/validate-answer
Content-Type: application/json

Body:
{
  "question_id": 1,
  "user_answer": "La respuesta del estudiante aquí"
}
```

**Respuesta:**
```json
{
  "score": 87.5,
  "is_correct": true,
  "feedback": "¡Excelente! Tu respuesta demuestra una comprensión profunda del tema.",
  "similarity": 0.8753
}
```

### 📚 Obtener Materiales
```http
GET /api/materials
```

### ❓ Crear Pregunta
```http
POST /api/questions
Content-Type: application/json

Body:
{
  "id": 1,
  "text": "¿Qué es un grafo dirigido?",
  "topic": "Grafos",
  "difficulty": "medium"
}
```

### 📊 Estadísticas
```http
GET /api/stats
```

## 🧪 Pruebas

### Documentación interactiva

FastAPI genera documentación automática:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Prueba con PowerShell

**Subir material:**
```powershell
$file = Get-Content -Path "C:\ruta\documento.pdf" -Raw -Encoding Byte
Invoke-RestMethod -Uri "http://localhost:8000/api/materials/upload" -Method Post -Form @{file=$file}
```

**Validar respuesta:**
```powershell
$body = @{
    question_id = 1
    user_answer = "Un grafo dirigido es una estructura..."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/validate-answer" -Method Post -Body $body -ContentType "application/json"
```

## 📊 Arquitectura

```
backend/
├── main.py                    # API principal con FastAPI
├── embeddings_module.py       # Generación de embeddings
├── chunking.py                # Procesamiento de textos
├── requirements.txt           # Dependencias
├── .env                       # Configuración (no en Git)
├── .env.example              # Ejemplo de configuración
└── README.md                 # Este archivo

data/ (generada automáticamente)
├── embeddings/               # Archivos JSON con embeddings
│   └── material_*.json
└── materials/                # Materiales subidos (opcional)
```

## 🔬 Validación Semántica

El sistema usa **similaridad coseno** para validar respuestas:

| Similaridad | Calificación | Feedback |
|-------------|--------------|----------|
| ≥ 0.9       | Excelente    | Comprensión profunda 🌟 |
| 0.7 - 0.89  | Bueno        | Correcto, puede profundizar 👍 |
| 0.5 - 0.69  | Aceptable    | Conceptos correctos, revisar 📚 |
| < 0.5       | Incorrecto   | Necesita repasar 🔄 |

## 🛠️ Configuración Avanzada

### Cambiar modelo de embeddings

En `.env`:
```bash
MODEL_NAME=paraphrase-multilingual-MiniLM-L12-v2
```

### Ajustar chunking

En `.env`:
```bash
DEFAULT_CHUNK_SIZE=1000
DEFAULT_CHUNK_OVERLAP=100
```

### Ajustar umbrales

En `.env`:
```bash
SIMILARITY_THRESHOLD_EXCELLENT=0.85
SIMILARITY_THRESHOLD_GOOD=0.65
```

## 🐳 Docker

```bash
docker build -t recuiva-backend .
docker run -p 8000:8000 recuiva-backend
```

## 📝 Notas Importantes

1. **Primera ejecución:** El modelo se descargará automáticamente (~90MB)
2. **Procesamiento:** Documentos grandes pueden tardar varios minutos
3. **Almacenamiento:** Los embeddings se guardan en JSON (~1MB por 100 chunks)
4. **Memoria:** Cada validación usa ~100-200MB de RAM temporalmente

## 🆘 Troubleshooting

### Error: "Model not found"
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### Error: "CORS policy"
Agregar tu origen en `.env`:
```bash
ALLOWED_ORIGINS=http://localhost:3000,http://tu-dominio.com
```

### Error al activar entorno virtual
Si tienes problemas de permisos en PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📚 Scripts Antiguos (Referencia)

Los scripts anteriores (`embeddings_local.py`, `embeddings_gui.py`, `launcher.py`) siguen disponibles para referencia, pero ahora el backend principal usa `main.py` con FastAPI

## Estructura del JSON de salida

```json
{
  "metadata": {
    "timestamp": "2025-09-30T...",
    "model": "all-MiniLM-L6-v2",
    "total_chunks": 6,
    "dimension": 384
  },
  "chunks": [
    {
      "id": "chunk_001",
      "content": "Active Recall es una técnica...",
      "embedding": {
        "vector": [0.123, -0.456, ...],
        "dimension": 384,
        "norm": 1.0
      }
    }
  ],
  "top_similaridades": [
    {
      "chunk_1": "chunk_001",
      "chunk_2": "chunk_003",
      "similaridad": 0.8234
    }
  ]
}
```

## Evidencia para Notion

- **HU-010**: Embeddings → Estado: Parcial
- **Evidencia**: Captura de consola + archivo JSON
- **Progreso**: Script funcional para generar embeddings locales