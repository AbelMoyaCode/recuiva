# 🎓 Recuiva - Sistema Inteligente de Active Recall con IA

![Estado: Producción](https://img.shields.io/badge/Estado-Producción-success)
![Versión](https://img.shields.io/badge/Versión-2.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green)
![pgvector](https://img.shields.io/badge/pgvector-0.8.0-orange)

**Plataforma de aprendizaje basada en Active Recall con validación semántica automática mediante Inteligencia Artificial**

Sistema completo que permite a estudiantes mejorar su retención de conocimiento mediante técnicas de recuperación activa, validadas con análisis semántico avanzado usando **HybridValidator** (BM25 + Cosine Similarity + Coverage) y **chunking semántico adaptativo**.

---

## 🌐 Aplicación en Producción

| Servicio | URL | Descripción |
|----------|-----|-------------|
| 🌍 **Frontend** | [https://recuiva.duckdns.org](https://recuiva.duckdns.org) | Aplicación web completa |
| 🔧 **API Backend** | [https://api-recuiva.duckdns.org](https://api-recuiva.duckdns.org) | API REST FastAPI |
| 📖 **Documentación API** | [https://api-recuiva.duckdns.org/docs](https://api-recuiva.duckdns.org/docs) | Swagger UI interactivo |
| 💚 **Health Check** | [https://api-recuiva.duckdns.org/api/health](https://api-recuiva.duckdns.org/api/health) | Estado del servidor |
| 🔗 **IP Directa** | [http://147.182.226.170](http://147.182.226.170) | Acceso sin DNS (universidades) |

### 📚 **Documentación Oficial**

| Documento | Descripción |
|-----------|-------------|
| 🛠️ **[Manual de Despliegue](MANUAL_DESPLIEGUE_EXPANDIDO.md)** | Guía técnica paso a paso (V10.0) para desplegar en DigitalOcean. |
| 🧑‍🎓 **[Manual de Usuario](MANUAL_USUARIO_EXPANDIDO.md)** | Guía para estudiantes sobre cómo usar la plataforma. |
| 🗺️ **[Guía de Mapeo](GUIA_MAPEO_CAPTURAS.md)** | Referencia para ubicar las capturas de pantalla en el manual. |


### ⚠️ **Acceso desde Redes Restrictivas**

Si estás en una **red universitaria o empresarial** que bloquea DNS dinámicos (DuckDNS), usa la **IP directa**:

```
Frontend: http://147.182.226.170
Backend:  http://147.182.226.170:8001
```

**El sistema detectará automáticamente el hostname y configurará las URLs correctas.**

---

## ✨ Características Principales

### 🧠 **Validación Semántica Híbrida (HybridValidator)**

**NOVEDAD v2.0:** Sistema de validación multi-métrica que elimina umbrales duros

- **BM25 (30%):** Detecta keywords importantes (términos clave específicos)
- **Cosine Similarity (50%):** Similitud semántica vectorial (embeddings 384-dim)
- **Coverage (20%):** Proporción de conceptos clave cubiertos
- **Score suave 0-100%:** No hay umbral duro del 50% (45% similitud → ~70% score)
- **Modelo:** Sentence Transformers `all-MiniLM-L6-v2`

**Ejemplo real:**
```
❌ ANTES (AdvancedValidator):
   Similitud: 45.7% → Score: 0% (rechazado por umbral 50%)

✅ AHORA (HybridValidator):
   Similitud: 45.7% → Score: ~70-75% (escalado suave)
   BM25: 28% + Cosine: 45.7% + Coverage: 22% = 70.3%
```

### 📚 **Chunking Semántico Adaptativo**

**NOVEDAD v2.0:** Fragmentación inteligente por párrafos/frases coherentes

- **Tamaño:** 120-280 palabras (antes: 150-400)
- **Overlap:** 20 palabras (context anchors)
- **Método:** Semántico (no por caracteres)
- **Resultado:** ~40-60 chunks coherentes (antes: 18 chunks grandes)

**Ventajas:**
```
❌ ANTES (chunking por caracteres):
   - 18 chunks (~1.3 páginas cada uno)
   - Cortado arbitrario en medio de oraciones
   - Múltiples temas mezclados
   
✅ AHORA (chunking semántico):
   - 40-60 chunks (~200 palabras cada uno)
   - Respeta límites de párrafos/frases
   - Una idea completa por chunk
   - Mejor precisión en búsqueda
```

### 🤖 **Generación de Preguntas con IA**

- **Modelo:** Groq API - Llama 3.1 8B Instant
- **Costo:** 100% GRATIS (sin límites de tokens)
- **Velocidad:** ~500 tokens/segundo
- **Cantidad:** 2 preguntas por chunk (80-120 preguntas totales)
- **Niveles:** Literal, Inferencial, Crítico

### 🎯 **Sistema de Preguntas**

- Crea preguntas basadas en tus materiales académicos
- Responde sin ver el material (Active Recall puro)
- Retroalimentación instantánea con score multi-métrica
- Historial completo de respuestas y progreso
- **Feedback detallado:** Top 3 chunks relevantes + scoring breakdown

### 📊 **Análisis y Estadísticas**

- Dashboard con métricas de estudio en tiempo real
- Gráficos de evolución de scores por sesión
- Identificación automática de temas débiles
- Sistema de repetición espaciada (próximamente)
- Exportación de datos a JSON

### 🔐 **Autenticación y Seguridad**

- **Supabase Auth** (email/contraseña + OAuth)
- Sesiones persistentes con JWT
- HTTPS obligatorio (Let's Encrypt)
- Row Level Security (RLS) en base de datos
- Todos los datos privados por usuario

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                         INTERNET                            │
│              (DuckDNS + Let's Encrypt SSL)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
            ┌────────────▼────────────┐
            │  Traefik (Reverse Proxy)│
            │    Puerto 80/443        │
            └────────────┬────────────┘
                         │
         ┌───────────────┴──────────────┐
         │                              │
    ┌────▼─────┐                  ┌────▼─────┐
    │ Frontend │                  │ Backend  │
    │  Nginx   │                  │ FastAPI  │
    │  :80     │◄─────CORS────────┤  :8001   │
    └──────────┘                  └────┬─────┘
         │                              │
    HTML/CSS/JS              ┌──────────▼──────────┐
    Tailwind CSS             │ Sentence Transformers│
    Supabase JS              │   all-MiniLM-L6-v2  │
                             │   PyTorch (CPU)     │
                             └─────────┬───────────┘
                                       │
                              ┌────────▼─────────┐
                              │  Supabase Cloud  │
                              │  PostgreSQL +    │
                              │  pgvector v0.8.0 │
                              │  40-60 chunks    │
                              └──────────────────┘
```

### **Flujo de Validación Semántica**

```
1. Usuario escribe respuesta
   ↓
2. Frontend envía POST /api/validate-answer
   ↓
3. Backend genera embedding (384 dims)
   ↓
4. Consulta Supabase: SELECT similarity(embedding, ?)
   ↓
5. pgvector calcula coseno con IVFFlat index (<50ms)
   ↓
6. HybridValidator aplica scoring:
   - BM25: keywords importantes (30%)
   - Cosine: similitud semántica (50%)
   - Coverage: conceptos cubiertos (20%)
   ↓
7. Frontend muestra:
   - Score final (0-100%)
   - Clasificación (EXCELENTE/BUENO/ACEPTABLE/INSUFICIENTE)
   - Top 3 chunks relevantes
   - Scoring breakdown detallado
```

---

## 🛠️ Stack Tecnológico

### **Frontend**

- **HTML5** + **Tailwind CSS v3.3**
- **JavaScript Vanilla** (sin frameworks, máxima compatibilidad)
- **Supabase JS Client** v2.38 (autenticación)
- **Nginx** como servidor web estático
- **Responsive Design** (320px → 4K)

### **Backend**

- **FastAPI** 0.104 (Python 3.10)
- **Sentence Transformers** 2.2.2 (modelo all-MiniLM-L6-v2)
- **PyTorch** 2.1.0 (versión CPU, optimizado)
- **scikit-learn** 1.3.2 (cálculo de similitud coseno)
- **PyPDF2** 3.0.1 (extracción de texto de PDFs)
- **Supabase Python Client** (conexión a PostgreSQL)
- **Groq API** (generación de preguntas con Llama 3.1 8B)

### **Base de Datos**

- **Supabase Cloud** (PostgreSQL 15.1)
- **pgvector** v0.8.0 (vectores de 384 dimensiones)
- **IVFFlat indices** (búsqueda rápida <50ms)
- **40-60 embeddings** por material (~120-180 KB)

### **Infraestructura**

- **Docker** 24.0 + **Docker Compose** v2
- **Dokploy** (CI/CD automático desde GitHub)
- **Traefik** v3.5 (Reverse Proxy + SSL automático)
- **DigitalOcean Droplet** (Ubuntu 22.04 LTS, 2GB RAM)
- **DuckDNS** (DNS dinámico gratuito)
- **Let's Encrypt** (certificados SSL válidos hasta 19/01/2026)

---

## 🚀 Inicio Rápido

### **Opción 1: Usar la Aplicación en Producción (Recomendado)**

**No necesitas instalar nada**, solo abre:

```
https://recuiva.duckdns.org
```

O si estás en una **red con firewall restrictivo**:

```
http://147.182.226.170
```

---

### **Opción 2: Desarrollo Local**

#### **Requisitos Previos**

- Python 3.10+
- Git
- 2GB RAM mínimo
- Navegador moderno (Chrome, Edge, Firefox)

#### **Paso 1: Clonar el Repositorio**

```bash
git clone https://github.com/AbelMoyaCode/recuiva.git
cd recuiva
```

#### **Paso 2: Instalar Dependencias**

```bash
cd backend
pip install -r requirements.txt
```

#### **Paso 3: Configurar Variables de Entorno**

Crea `backend/.env`:

```bash
# Supabase Configuration
SUPABASE_URL=https://xqicgzqgluslzleddmfv.supabase.co
SUPABASE_KEY=tu_service_role_key_aqui

# Groq API (GRATIS - sin límites)
GROQ_API_KEY=tu_groq_api_key

# API Configuration
HOST=0.0.0.0
PORT=8001
DEBUG=False

# Model Configuration
MODEL_NAME=all-MiniLM-L6-v2
DEFAULT_CHUNK_SIZE=500
DEFAULT_CHUNK_OVERLAP=100

# Thresholds
SIMILARITY_THRESHOLD_EXCELLENT=0.9
SIMILARITY_THRESHOLD_GOOD=0.7
SIMILARITY_THRESHOLD_ACCEPTABLE=0.55
```

**Obtener claves:**
- **Supabase:** https://supabase.com (gratis hasta 500MB)
- **Groq API:** https://console.groq.com/keys (GRATIS 100%)

#### **Paso 4: Iniciar Servidores**

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd ..
python -m http.server 5500 --directory public
```

#### **Paso 5: Acceder a la Aplicación**

```
http://localhost:5500
```

**Página principal de práctica:**
```
http://localhost:5500/app/sesion-practica.html?material_id=1
```

> **Nota**: El parámetro `material_id=1` corresponde al material cargado en el sistema.

---

### **Opción 3: Docker Compose (Producción Local)**

```bash
# Desde la raíz del proyecto
docker compose up -d --build

# Verificar estado
docker compose ps

# Ver logs
docker compose logs -f

# Acceder a la aplicación
# Frontend: http://localhost
# Backend:  http://localhost:8001
```

---

## 📦 Estructura del Proyecto

```
recuiva/
├── backend/                      # Backend FastAPI
│   ├── main.py                  # API principal (1685 líneas)
│   ├── hybrid_validator.py      # ✨ Validador híbrido (BM25+Cosine+Coverage)
│   ├── chunking.py              # ✨ Chunking semántico (120-280 palabras)
│   ├── embeddings_module.py     # Generación de embeddings
│   ├── question_generator_ai.py # Generación de preguntas (Groq)
│   ├── supabase_client.py       # Cliente Supabase
│   ├── requirements.txt         # Dependencias Python
│   └── .env.example             # Plantilla de variables de entorno
│
├── public/                       # Frontend (archivos estáticos)
│   ├── index.html               # Landing page principal
│   └── app/                     # Aplicación web
│       ├── sesion-practica.html # ⭐ Práctica con validación IA
│       ├── materiales.html      # Gestión de materiales PDF
│       ├── repasos.html         # Sistema de repasos espaciados
│       ├── dashboard.html       # Dashboard de progreso
│       ├── evolucion.html       # Gráficos de evolución
│       ├── mi-perfil.html       # Perfil de usuario
│       ├── subir-material.html  # Upload de materiales
│       ├── analytics.html       # Análisis detallado
│       ├── auth/                # Sistema de autenticación
│       │   ├── iniciar-sesion.html
│       │   └── crear-cuenta.html
│       ├── institucional/       # Páginas informativas
│       │   ├── active-recall.html
│       │   ├── validacion-semantica.html
│       │   └── diferencias.html
│       └── assets/              # Recursos estáticos
│           ├── js/
│           │   ├── api.js       # Cliente API (auto-detecta hostname)
│           │   ├── validate-answer-real.js
│           │   ├── upload-material.js
│           │   └── supabase-operations.js
│           └── img/
│
├── data/                         # Datos y materiales
│   ├── materials/               # PDFs subidos
│   ├── embeddings/              # Vectores (legacy, migrado a Supabase)
│   └── materials_index.json
│
├── docs/                         # Documentación completa
│   ├── ALGORITMO_VALIDACION_SEMANTICA.md
│   ├── GUIA_IMPLEMENTACION_SUPABASE.md
│   ├── DIAGNOSTICO_CHUNKS_PROBLEMA.md
│   └── README_COMPLETO.md
│
├── scripts/                      # Scripts de utilidad
│   ├── regenerar_indicadores.py
│   └── verificar_tr_consistencia.py
│
├── docker-compose.yml            # Orquestación de contenedores
├── Dockerfile                    # Imagen Docker principal
├── nginx.conf                    # Configuración del servidor web
├── requirements.txt              # Dependencias Python unificadas
├── config.yaml                   # Configuración general
└── README.md                     # 📖 Este archivo
```

---

## 📖 Uso de la API

### **Endpoints Principales**

#### **1. Health Check**

```bash
GET /api/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-19T15:30:45.123456",
  "model_loaded": true,
  "model_name": "all-MiniLM-L6-v2",
  "embedding_dimensions": 384
}
```

#### **2. Subir Material (PDF)**

```bash
POST /api/materials/upload
Content-Type: multipart/form-data

file: <archivo.pdf>
```

**Respuesta:**
```json
{
  "success": true,
  "material_id": "abc123xyz",
  "filename": "El_Collar_de_la_Reina.pdf",
  "total_chunks": 47,
  "estimated_pages": 24,
  "total_characters": 38450,
  "processing_time_seconds": 12.5
}
```

#### **3. Validar Respuesta (HybridValidator)**

```bash
POST /api/validate-answer
Content-Type: application/json

{
  "question_id": "q1",
  "question_text": "¿Por qué sospechan de Henriette?",
  "user_answer": "Porque vivía en el mismo edificio, conocía a la condesa...",
  "material_id": "abc123xyz"
}
```

**Respuesta:**
```json
{
  "success": true,
  "score": 75.3,
  "classification": "BUENO",
  "confidence": 0.753,
  "feedback": "Buena comprensión del concepto. Has identificado los puntos clave.",
  "category": "bueno",
  "best_chunk": {
    "text": "En el edificio vivía una amiga de convento...",
    "similarity": 0.847,
    "position": 18,
    "total_chunks": 47
  },
  "top_3_scores": [
    {"chunk_id": 18, "score": 0.847, "text": "..."},
    {"chunk_id": 19, "score": 0.782, "text": "..."},
    {"chunk_id": 20, "score": 0.715, "text": "..."}
  ],
  "scoring_breakdown": {
    "bm25_score": 28.5,
    "cosine_score": 45.7,
    "coverage_score": 22.1,
    "final_score": 75.3,
    "weights": {
      "bm25": 0.30,
      "cosine": 0.50,
      "coverage": 0.20
    }
  }
}
```

---

## 🔧 Comandos Útiles

### **Ver logs de contenedores:**
```bash
# Backend
docker logs recuiva-backend-1 -f

# Frontend
docker logs recuiva-frontend-1 -f
```

### **Reiniciar servicios:**
```bash
docker restart recuiva-backend-1
docker restart recuiva-frontend-1
```

### **Rebuild completo:**
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

### **Ver estado de Traefik:**
```bash
curl http://localhost:8080/api/http/routers | jq
```

---

## 🐛 Solución de Problemas

### **1. Backend devuelve 404**
```bash
# Verificar que los labels de Traefik estén correctos
docker inspect recuiva-backend-1 | grep traefik
```

### **2. CORS Error en el Frontend**
```bash
# Verificar que ALLOWED_ORIGINS incluya tu dominio
docker exec recuiva-backend-1 env | grep ALLOWED_ORIGINS
```

### **3. Puerto 8001 ocupado**
```bash
# Ver qué está usando el puerto
sudo lsof -i :8001

# Detener contenedores conflictivos
docker compose down
```

### **4. Modelo no se carga**
```bash
# Verificar logs del backend
docker logs recuiva-backend-1 | grep "Modelo"

# Debe decir: "✅ Modelo all-MiniLM-L6-v2 cargado exitosamente"
```

### **5. Score 0% con similitud 45%**

**Causa:** Usando AdvancedValidator en lugar de HybridValidator

**Solución:**
```bash
# Verificar que main.py use HybridValidator
grep "HybridValidator" backend/main.py

# Debe aparecer: "hybrid_validator = HybridValidator(embedding_model)"
```

---

## 📊 Métricas y Rendimiento

### **Backend (FastAPI)**
- **Tiempo de respuesta promedio:** <200ms
- **Validación semántica:** <500ms (incluye cálculo de embeddings)
- **Upload PDF (10 MB):** <3 segundos
- **Generación de embeddings:** ~100 chunks/segundo

### **Base de Datos (Supabase + pgvector)**
- **Búsqueda de similitud:** <50ms (con índices IVFFlat)
- **Almacenamiento de embeddings:** 384 dims × 4 bytes = 1.5 KB por chunk
- **40-60 chunks por material:** ~60-90 KB total

### **Infraestructura (DigitalOcean)**
- **RAM usada:** ~800 MB / 2 GB (40%)
- **CPU:** <20% en uso normal
- **Ancho de banda:** Ilimitado (DuckDNS)
- **Uptime:** 99.9% (monitorizado por Dokploy)

---

## 🚧 Roadmap y Mejoras Futuras

### **Versión 2.1 (Próxima)**
- [ ] Sistema de repetición espaciada (Spaced Repetition)
- [ ] Exportación de estadísticas a Excel/CSV
- [ ] Modo oscuro (Dark Mode)
- [ ] PWA (Progressive Web App) para uso offline
- [ ] Notificaciones push de recordatorios

### **Versión 2.2**
- [ ] Integración con Google Calendar (planificación de repasos)
- [ ] Generación automática de preguntas con GPT-4
- [ ] Comparación de respuestas con IA generativa
- [ ] Análisis de evolución con gráficos avanzados (Chart.js)

### **Versión 3.0**
- [ ] Modo colaborativo (compartir materiales entre usuarios)
- [ ] Gamificación (puntos, niveles, logros)
- [ ] API pública para integraciones
- [ ] Soporte para videos (YouTube) como material de estudio
- [ ] Reconocimiento de voz para respuestas orales

---

## 👥 Contribución

¡Las contribuciones son bienvenidas! 

### **Cómo contribuir:**

1. **Fork** el repositorio
2. Crea una **rama** para tu feature:
   ```bash
   git checkout -b feature/nombre-descriptivo
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m "feat: descripción clara del cambio"
   ```
4. **Push** a tu fork:
   ```bash
   git push origin feature/nombre-descriptivo
   ```
5. Abre un **Pull Request** en GitHub

### **Convenciones de commits:**
- `feat:` Nueva funcionalidad
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. 

Puedes usar, modificar y distribuir este código libremente, siempre que incluyas el aviso de copyright original.

---

## 👤 Autor

**Abel Jesús Moya Acosta**

- 🎓 Estudiante de Ingeniería de Computación y Sistemas
- 🏫 Universidad Privada Antenor Orrego (UPAO)
- 📧 Email: abelmoya2@upao.edu.pe
- 💼 GitHub: [@AbelMoyaCode](https://github.com/AbelMoyaCode)

---

## 🙏 Agradecimientos

- **[Sentence Transformers](https://www.sbert.net/)** - Por el excelente modelo de embeddings
- **[FastAPI](https://fastapi.tiangolo.com/)** - Por el framework web más rápido de Python
- **[Supabase](https://supabase.com/)** - Por la infraestructura de base de datos y auth
- **[pgvector](https://github.com/pgvector/pgvector)** - Por la extensión de vectores en PostgreSQL
- **[Groq](https://groq.com/)** - Por el acceso GRATUITO a Llama 3.1 8B
- **[Dokploy](https://dokploy.com/)** - Por simplificar el despliegue con Docker
- **[Traefik](https://traefik.io/)** - Por el reverse proxy automático
- **[DuckDNS](https://www.duckdns.org/)** - Por el DNS dinámico gratuito
- **[DigitalOcean](https://www.digitalocean.com/)** - Por la infraestructura cloud confiable
- **[Tailwind CSS](https://tailwindcss.com/)** - Por el framework de CSS utility-first

---

## 📞 Soporte y Contacto

### **Si tienes problemas:**

1. 📖 Revisa la sección [Solución de Problemas](#-solución-de-problemas)
2. 📚 Consulta la [documentación completa](docs/README_COMPLETO.md)
3. 🐛 Abre un [Issue en GitHub](https://github.com/AbelMoyaCode/recuiva/issues)
4. 📧 Contacta al autor: abelmoya2@upao.edu.pe

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Clonar repo
git clone https://github.com/AbelMoyaCode/recuiva.git && cd recuiva

# 2. Instalar dependencias
cd backend && pip install -r requirements.txt && cd ..

# 3. Iniciar servicios (Docker)
docker compose up -d

# 4. Abrir navegador
# http://localhost
```

**O simplemente usar la aplicación en producción:**
```
https://recuiva.duckdns.org
```

---

## 🌟 ¿Te gusta el proyecto?

Si este proyecto te ha sido útil:

- ⭐ **Dale una estrella en GitHub**
- 🐛 **Reporta bugs** para mejorar la aplicación
- 💡 **Sugiere nuevas funcionalidades**
- 🤝 **Contribuye** con código o documentación
- 📢 **Comparte** con otros estudiantes

---

## 📝 Changelog

### **v2.0.0 (19 Noviembre 2025)** 🎉

**BREAKING CHANGES:**
- ✨ **HybridValidator:** Reemplaza AdvancedValidator con sistema multi-métrica (BM25 + Cosine + Coverage)
- ✨ **Chunking Semántico:** 120-280 palabras con overlap de 20 palabras
- 🔧 **Fix Score 0%:** Eliminado umbral duro del 50%, ahora escalado suave 0-100%
- 🔧 **Mejor Precisión:** 40-60 chunks coherentes (antes: 18 chunks grandes)

**Mejoras:**
- 🚀 Generación de preguntas con Groq API (Llama 3.1 8B) - GRATIS
- 📊 Scoring breakdown detallado en respuestas
- 🎯 Top 3 chunks relevantes en validación
- 📈 Mejor detección de reformulación (keywords + semántica)

**Fixes:**
- 🐛 Corregido: 45% similitud daba 0% score
- 🐛 Corregido: Chunks cortados en medio de oraciones
- 🐛 Corregido: Importaciones duplicadas en main.py

---

**Desarrollado con ❤️ por Abel Moya - Noviembre 2025**

**¡Aprende más eficientemente con Recuiva!** 🚀
