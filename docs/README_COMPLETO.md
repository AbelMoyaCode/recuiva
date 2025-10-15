# 🚀 RECUIVA - Sistema de Active Recall con IA

![Recuiva Logo](public/assets/img/Icon-Recuiva.png)

## 📋 Descripción

**Recuiva** es un sistema inteligente de estudio basado en **Active Recall** que utiliza **IA y validación semántica** para evaluar la comprensión del estudiante. No se trata de memorización literal, sino de entender conceptos y poder explicarlos con tus propias palabras.

### ✨ Características principales:

- 🧠 **Validación semántica inteligente** con Sentence Transformers
- 📚 **Procesamiento automático de PDFs** con chunking optimizado
- 🎯 **Scoring contextual** que entiende variaciones y parafraseo
- 📊 **Análisis multi-chunk** para respuestas más precisas
- ✏️ **Gestión completa de preguntas** (crear, editar, eliminar)
- 🏷️ **Organización por materiales y carpetas**
- 💾 **Persistencia local** de preguntas y progreso
- 🎨 **Interfaz moderna y responsive**

---

## 🚀 Inicio Rápido

### Opción 1: Ejecutar con script automático (RECOMENDADO)

**Windows:**
```bash
# Doble clic en:
EJECUTAR_RECUIVA.bat

# O desde PowerShell:
.\EJECUTAR_RECUIVA.ps1
```

**El script automático:**
1. ✅ Verifica dependencias
2. ✅ Limpia procesos anteriores
3. ✅ Inicia backend (puerto 8000)
4. ✅ Inicia frontend (puerto 5500)
5. ✅ Abre el navegador automáticamente

### Opción 2: Manual

**Terminal 1 - Backend:**
```bash
cd C:\Users\Abel\Desktop\recuiva
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd C:\Users\Abel\Desktop\recuiva\public
python -m http.server 5500
```

**Abrir navegador:**
```
http://localhost:5500/index.html
```

---

## 📦 Requisitos

### Python 3.10+

**Módulos necesarios:**
```bash
pip install -r backend/requirements.txt
```

**Principales dependencias:**
- `fastapi` - Framework web
- `uvicorn` - Servidor ASGI
- `sentence-transformers` - Embeddings semánticos
- `PyPDF2` - Procesamiento de PDFs
- `numpy` - Cálculos matemáticos
- `pydantic` - Validación de datos

---

## 📁 Estructura del Proyecto

```
recuiva/
├── 📄 EJECUTAR_RECUIVA.ps1      # Script principal de ejecución
├── 📄 EJECUTAR_RECUIVA.bat      # Iniciador Windows
├── 📂 backend/                   # API FastAPI
│   ├── main.py                  # Endpoints principales
│   ├── embeddings_module.py     # Generación de embeddings
│   ├── chunking.py              # Procesamiento de PDFs
│   └── requirements.txt         # Dependencias Python
├── 📂 public/                    # Frontend estático
│   ├── index.html               # Página principal
│   └── app/
│       ├── sesion-practica.html # Sesión de Active Recall
│       ├── subir-material.html  # Subir PDFs
│       └── materiales.html      # Gestión de materiales
├── 📂 data/                      # Datos del sistema
│   ├── materials/               # PDFs subidos
│   ├── embeddings/              # Embeddings generados
│   └── questions_storage.json   # Preguntas guardadas
└── 📂 docs/                      # Documentación

```

---

## 🎯 Uso del Sistema

### 1️⃣ Subir Material

1. Ve a **"Materiales"** → **"Subir Material"**
2. Arrastra un PDF o haz clic para seleccionar
3. El sistema procesará automáticamente:
   - ✅ Extracción de texto
   - ✅ Chunking inteligente (500-1000 caracteres)
   - ✅ Generación de embeddings
   - ✅ Almacenamiento optimizado

### 2️⃣ Crear Sesión de Práctica

1. Ve a **"Práctica"**
2. Selecciona un material activo
3. Escribe una **pregunta** sobre el contenido
4. Responde **SIN mirar el material** (Active Recall)
5. Haz clic en **"VALIDAR RESPUESTA"**

### 3️⃣ Interpretar el Score

| Score | Significado |
|-------|-------------|
| 90-100% | ✅ Excelente comprensión |
| 80-89% | ✅ Buena comprensión |
| 70-79% | ⚠️ Comprensión aceptable |
| 60-69% | ⚠️ Necesita refuerzo |
| <60% | ❌ Repasar el material |

**El scoring considera:**
- 📊 Similitud semántica base
- 🧠 Boost por variaciones inteligentes
- 📖 Bonus por contexto amplio
- 🔑 Bonus por palabras clave
- ✍️ Bonus por elaboración detallada

### 4️⃣ Gestionar Preguntas

**Cada pregunta guardada tiene:**
- ✏️ **Editar** - Modifica el texto
- 🗑️ **Eliminar** - Borra con confirmación
- 📊 **Score** - Puntuación obtenida
- 🏷️ **Carpeta** - Organización por material
- 📅 **Fecha** - Timestamp de creación

**Botones disponibles:**
- ➕ **Nueva Pregunta** - Al final de la lista
- 💾 **Guardar** - Almacena en localStorage
- 🔄 **Cargar** - Click en pregunta para reutilizar

---

## 🔧 Configuración Avanzada

### Backend (backend/main.py)

```python
# Configuración de puertos
PORT = 8000
HOST = "0.0.0.0"

# Modelo de embeddings
MODEL_NAME = "all-MiniLM-L6-v2"

# Tamaño de chunks
CHUNK_SIZE = 800
CHUNK_OVERLAP = 200
```

### Frontend

**Cambiar puerto del servidor:**
```bash
python -m http.server 5500  # Cambiar 5500 por otro puerto
```

**URLs importantes:**
- Backend API: `http://localhost:8000`
- Documentación: `http://localhost:8000/docs`
- Frontend: `http://localhost:5500`

---

## 📊 API Endpoints

### Materiales

```bash
GET  /api/materials           # Listar materiales
POST /api/materials/upload    # Subir PDF
GET  /api/health              # Estado del servidor
```

### Validación

```bash
POST /api/validate-answer
{
  "question_text": "¿Por qué...?",
  "material_id": 2,
  "user_answer": "Porque..."
}

# Respuesta:
{
  "score": 88.0,
  "is_correct": true,
  "similarity": 0.62,
  "feedback": "✅ EXCELENTE...",
  "relevant_chunks": [...]
}
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

```bash
pip install -r backend/requirements.txt
```

### Error: "Puerto 8000 en uso"

```bash
# Detener procesos Python
taskkill /F /IM python.exe

# O cambiar puerto en el script
```

### Error: "No se encuentra el material"

1. Verifica que el PDF esté en `data/materials/`
2. Verifica que exista el embedding en `data/embeddings/`
3. Recarga el material desde la UI

### Backend se detiene solo

**No uses `--reload` en uvicorn:**
```bash
# ❌ MAL
uvicorn backend.main:app --reload

# ✅ BIEN
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## 🎓 Metodología: Active Recall

**¿Qué es Active Recall?**

Active Recall es una técnica de estudio que consiste en:
1. 📖 Leer/estudiar el material
2. 📚 Cerrar el material
3. 🧠 Intentar recordar y explicar con tus palabras
4. ✅ Verificar y corregir

**¿Por qué funciona?**

- 🧠 Fortalece conexiones neuronales
- 📈 Mejora retención a largo plazo
- 🎯 Identifica lagunas de conocimiento
- 💪 Desarrolla comprensión profunda

**Recuiva automatiza y mejora este proceso con:**
- ✅ Validación semántica inteligente
- 📊 Feedback instantáneo y detallado
- 📈 Tracking de progreso
- 🎯 Enfoque en comprensión, no memorización

---

## 👨‍💻 Autor

**Abel Jesús Moya Acosta**

- Universidad: UPAO (Universidad Privada Antenor Orrego)
- Proyecto: Taller Integrador I
- Fecha: Octubre 2025

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos para el curso de Taller Integrador I.

---

## 🆘 Soporte

Si encuentras problemas:

1. Verifica que todas las dependencias estén instaladas
2. Revisa los logs en la terminal
3. Consulta la documentación en `docs/`
4. Abre un issue en GitHub (si aplica)

---

## 🎉 ¡Disfruta estudiando con Recuiva!

**Recuerda:** El objetivo no es memorizar, sino **entender** 🧠
