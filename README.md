# 🎓 Recuiva - Sistema de Active Recall con IA# 🎓 Recuiva - Sistema de Active Recall con IA



![Estado: Producción](https://img.shields.io/badge/Estado-Producción-success)

![Versión](https://img.shields.io/badge/Versión-2.0.0-blue)

![Python](https://img.shields.io/badge/Python-3.10-blue)![Estado: Producción](https://img.shields.io/badge/Estado-Producción-success)Sistema de aprendizaje basado en Active Recall con validación semántica mediante IA.

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

![Docker](https://img.shields.io/badge/Docker-Compose-blue)![Versión](https://img.shields.io/badge/Versión-1.0.0-blue)

![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green)

![Python](https://img.shields.io/badge/Python-3.10-blue)## 🏗️ Estructura del Proyecto

**Plataforma de aprendizaje basada en Active Recall con validación semántica mediante Inteligencia Artificial**

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

Sistema completo que permite a estudiantes mejorar su retención de conocimiento mediante técnicas de recuperación activa, validadas con análisis semántico de última generación usando Sentence Transformers.

![Docker](https://img.shields.io/badge/Docker-Compose-blue)```

---

recuiva/

## 🌐 Aplicación en Producción

Sistema de estudio basado en **Active Recall** con validación semántica de respuestas usando **Inteligencia Artificial** (Sentence Transformers).├── backend/              # Backend FastAPI

### **URLs Principales**

│   ├── main.py          # API principal

| Servicio | URL | Descripción |

|----------|-----|-------------|---│   ├── embeddings_module.py

| 🌍 **Frontend** | [https://recuiva.duckdns.org](https://recuiva.duckdns.org) | Aplicación web completa |

| 🔧 **API Backend** | [https://api-recuiva.duckdns.org](https://api-recuiva.duckdns.org) | API REST FastAPI |│   ├── chunking.py

| 📖 **Documentación API** | [https://api-recuiva.duckdns.org/docs](https://api-recuiva.duckdns.org/docs) | Swagger UI interactivo |

| 💚 **Health Check** | [https://api-recuiva.duckdns.org/api/health](https://api-recuiva.duckdns.org/api/health) | Estado del servidor |## 🌐 Aplicación en Producción│   └── requirements.txt

| 🔗 **IP Directa** | [http://147.182.226.170](http://147.182.226.170) | Acceso sin DNS (universidades) |

├── public/              # Frontend (archivos servidos)

### ⚠️ **IMPORTANTE: Acceso desde Redes Restrictivas**

- **🌍 Frontend:** [https://recuiva.duckdns.org](https://recuiva.duckdns.org)│   ├── index.html      # Landing page principal

Si estás en una **red universitaria o empresarial** que bloquea DNS dinámicos (DuckDNS), usa la **IP directa**:

- **🔧 API Backend:** [https://api-recuiva.duckdns.org](https://api-recuiva.duckdns.org)│   ├── dashboard.html  # Dashboard de usuario

```

Frontend: http://147.182.226.170- **📖 Documentación API:** [https://api-recuiva.duckdns.org/docs](https://api-recuiva.duckdns.org/docs)│   ├── landing-page.html

Backend:  http://147.182.226.170:8001

```- **💚 Health Check:** [https://api-recuiva.duckdns.org/api/health](https://api-recuiva.duckdns.org/api/health)│   └── app/            # Aplicación web



**El sistema detectará automáticamente el hostname y configurará las URLs correctas.**│       ├── sesion-practica.html    # ⭐ Página principal de práctica



------│       ├── materiales.html         # Gestión de materiales PDF



## ✨ Características Principales│       ├── repasos.html           # Sistema de repasos espaciados



### 🧠 **Validación Semántica con IA**## ✨ Características Principales│       ├── dashboard.html         # Dashboard de progreso

- Usa **Sentence Transformers** (modelo `all-MiniLM-L6-v2`, 384 dimensiones)

- Calcula **similitud del coseno** entre respuesta del usuario y material académico│       ├── evolucion.html

- Clasifica automáticamente:

  - **EXCELENTE** (≥85%): Comprensión profunda### 🧠 Validación Semántica con IA│       ├── mi-perfil.html

  - **BUENO** (70-84%): Comprensión sólida

  - **ACEPTABLE** (55-69%): Comprensión básica- Usa **Sentence Transformers** (modelo `all-MiniLM-L6-v2`)│       ├── subir-material.html

  - **INSUFICIENTE** (<55%): Requiere repaso

- Identifica y muestra los **3 fragmentos más relevantes** del material- Calcula similitud coseno entre tu respuesta y el material│       ├── analytics.html



### 📚 **Gestión de Materiales**- Clasifica automáticamente: **EXCELENTE** (>90%), **BUENO** (70-90%), **ACEPTABLE** (50-70%)│       ├── auth/                  # Sistema de autenticación

- Sube **PDFs** o archivos **TXT** (hasta 50 MB)

- Fragmentación inteligente en chunks de **500 caracteres** (optimizado para precisión)- Identifica el fragmento más relevante del material│       ├── institucional/         # Páginas informativas

- Generación automática de **embeddings vectoriales** (384 dimensiones)

- Almacenamiento en **Supabase PostgreSQL** con extensión **pgvector**│       │   ├── active-recall.html

- Organización por carpetas (Semestre, Curso, Tema)

### 📚 Gestión de Materiales│       │   ├── validacion-semantica.html

### 🎯 **Sistema de Preguntas Inteligente**

- Crea preguntas basadas en tus materiales académicos- Sube **PDFs** o archivos **TXT**│       │   └── diferencias.html

- Responde sin ver el material (Active Recall puro)

- Retroalimentación instantánea con score de similitud semántica- Fragmentación automática en chunks de 500 caracteres│       └── assets/               # Recursos estáticos

- Historial completo de respuestas y progreso

- **Bonificaciones inteligentes**: contexto, keywords, longitud- Generación de embeddings para búsqueda semántica├── data/               # Datos y materiales



### 📊 **Análisis y Estadísticas**- Organización por carpetas (Semestre, Curso, Tema)│   ├── materials/      # Materiales de estudio (PDFs)

- Dashboard con métricas de estudio en tiempo real

- Gráficos de evolución de scores por sesión│   ├── embeddings/     # Vectores de embeddings

- Identificación automática de temas débiles

- Sistema de repetición espaciada (próximamente)### 🎯 Sistema de Preguntas│   └── materials_index.json

- Exportación de datos a JSON

- Crea preguntas basadas en tus materiales├── docs/               # Documentación del proyecto

### 🔐 **Autenticación y Seguridad**

- Sistema de autenticación con **Supabase Auth**- Responde sin ver el material (Active Recall)│   ├── ANALISIS_SISTEMA_USUARIOS.md    # Análisis del sistema de usuarios

- Login con email/contraseña + OAuth (Google, GitHub)

- Sesiones persistentes con tokens JWT- Retroalimentación instantánea con score de similitud│   ├── DEPLOYMENT_GUIDE.md             # Guía de deployment

- Todos los datos privados por usuario

- HTTPS obligatorio con certificados Let's Encrypt- Historial de respuestas y progreso│   ├── DEPLOYMENT_GUIDE_DIGITALOCEAN.md # Deployment en DigitalOcean



---│   ├── INICIO_RAPIDO.md                # Guía de inicio rápido



## 🏗️ Arquitectura del Sistema### 📊 Análisis y Estadísticas│   └── README_COMPLETO.md              # Documentación completa



```- Dashboard con métricas de estudio├── scripts/            # Scripts de utilidad

┌─────────────────────────────────────────────────────────────┐

│                         INTERNET                            │- Gráficos de evolución de scores│   ├── completar_tareas.ps1

│              (DuckDNS + Let's Encrypt SSL)                  │

└────────────────────────┬────────────────────────────────────┘- Identificación de temas débiles│   ├── setup-server.sh

                         │

            ┌────────────▼────────────┐- Repetición espaciada automática│   ├── fix-dokploy-port.sh

            │  Traefik v3.5           │

            │  (Reverse Proxy)        ││   └── simple_backend.py

            │  Puerto 80 → 443        │

            └────────────┬────────────┘---├── assets/             # Assets globales

                         │

         ┌───────────────┴──────────────┐│   ├── img/

         │                              │

    ┌────▼─────┐                  ┌────▼─────┐## 🏗️ Arquitectura del Sistema│   └── js/

    │ Frontend │                  │ Backend  │

    │  Nginx   │                  │ FastAPI  │├── config.yaml         # Configuración de la aplicación

    │  :80     │◄─────CORS────────┤  :8001   │

    └──────────┘                  └────┬─────┘```├── requirements.txt    # Dependencias Python unificadas

         │                              │

    HTML/CSS/JS              ┌──────────▼──────────┐┌─────────────────────────────────────────────────────────────┐├── docker-compose.yml  # Orquestación de contenedores

    Tailwind CSS             │ Sentence Transformers│

    Supabase JS              │   all-MiniLM-L6-v2  ││                         INTERNET                            │├── Dockerfile          # Imagen Docker principal

                             │   PyTorch (CPU)     │

                             └─────────┬───────────┘│                  (DuckDNS + Let's Encrypt)                  │├── nginx.conf          # Configuración del servidor web

                                       │

                              ┌────────▼─────────┐└────────────────────────┬────────────────────────────────────┘├── INICIAR_RECUIVA.bat # Script de inicio Windows

                              │  Supabase Cloud  │

                              │  PostgreSQL +    │                         │└── INICIAR_RECUIVA.ps1 # Script de inicio PowerShell

                              │  pgvector v0.8.0 │

                              │  153 embeddings  │            ┌────────────▼────────────┐```

                              └──────────────────┘

```            │  Traefik (Reverse Proxy)│



### **Flujo de Validación Semántica**            │    Puerto 80/443        │## 🚀 Inicio Rápido



```            └────────────┬────────────┘

1. Usuario escribe respuesta

   ↓                         │### 0. Instalar Dependencias

2. Frontend envía POST /api/validate-answer

   ↓         ┌───────────────┴──────────────┐

3. Backend genera embedding (384 dims)

   ↓         │                              │```bash

4. Consulta Supabase: SELECT similarity(embedding, ?)

   ↓    ┌────▼─────┐                  ┌────▼─────┐pip install -r requirements.txt

5. pgvector calcula coseno con IVFFlat index

   ↓    │ Frontend │                  │ Backend  │```

6. Backend aplica scoring inteligente:

   - Similitud base (coseno)    │  Nginx   │                  │ FastAPI  │

   - Bonus contexto (+0-5%)

   - Bonus keywords (+0-8%)    │  :80     │◄─────CORS────────┤  :8001   │### 1. Iniciar Servidores

   - Bonus longitud (+0-5%)

   - Boost inteligencia (+0-10%)    └──────────┘                  └────┬─────┘

   ↓

7. Frontend muestra:         │                              │**Windows (Batch):**

   - Score final (0-100%)

   - Clasificación (EXCELENTE/BUENO/ACEPTABLE/INSUFICIENTE)    HTML/CSS/JS              ┌──────────▼──────────┐```cmd

   - Top 3 fragmentos relevantes

   - Feedback personalizado    Tailwind CSS             │ Sentence Transformers│INICIAR_RECUIVA.bat

```

                             │   all-MiniLM-L6-v2  │```

---

                             └─────────────────────┘

## 🛠️ Stack Tecnológico

```**Windows (PowerShell):**

### **Frontend**

- **HTML5** + **Tailwind CSS v3.3**```powershell

- **JavaScript Vanilla** (sin frameworks, máxima compatibilidad)

- **Supabase JS Client** v2.38 (autenticación)---.\INICIAR_RECUIVA.ps1

- **Nginx** como servidor web estático

- **Responsive Design** (320px → 4K)```



### **Backend**## 🛠️ Stack Tecnológico

- **FastAPI** 0.104 (Python 3.10)

- **Sentence Transformers** 2.2.2 (modelo all-MiniLM-L6-v2)**Manual:**

- **PyTorch** 2.1.0 (versión CPU, optimizado)

- **scikit-learn** 1.3.2 (cálculo de similitud coseno)### **Frontend**```powershell

- **PyPDF2** 3.0.1 (extracción de texto de PDFs)

- **Supabase Python Client** (conexión a PostgreSQL)- HTML5 + Tailwind CSS# Backend (puerto 8000)



### **Infraestructura**- JavaScript Vanilla (sin frameworks)cd backend

- **Docker** 24.0 + **Docker Compose** v2

- **Dokploy** (CI/CD automático desde GitHub)- Nginx (servidor web estático)python -m uvicorn main:app --reload --port 8000

- **Traefik** v3.5 (Reverse Proxy + SSL automático)

- **DigitalOcean Droplet** (Ubuntu 22.04 LTS, 2GB RAM)

- **DuckDNS** (DNS dinámico gratuito)

- **Let's Encrypt** (certificados SSL válidos hasta 19/01/2026)### **Backend**# Frontend (puerto 5500) - en otra terminal



### **Base de Datos**- FastAPI (Python 3.10)cd ..

- **Supabase Cloud** (PostgreSQL 15.1)

- **pgvector** v0.8.0 (vectores de 384 dimensiones)- Sentence Transformers (`sentence-transformers==2.2.2`)python -m http.server 5500 --directory public

- **IVFFlat indices** (búsqueda rápida de similitud)

- **153 embeddings** almacenados (~229 KB)- PyTorch (versión CPU)```



---- PyPDF2 (extracción de texto de PDFs)



## 📦 Estructura del Proyecto### 2. Acceder a la Aplicación



```### **Infraestructura**

recuiva/

├── backend/                      # Backend FastAPI- Docker + Docker Compose**Página principal de práctica:**

│   ├── main.py                  # API principal (1014 líneas)

│   ├── semantic_validator.py   # Validador semántico (449 líneas)- Dokploy (CI/CD)```

│   ├── chunking.py              # Fragmentación de documentos

│   ├── embeddings_module.py    # Generación de embeddings- Traefik v3.5 (Reverse Proxy + SSL)http://localhost:5500/app/sesion-practica.html?material_id=1

│   ├── supabase_client.py      # Cliente Supabase

│   ├── requirements.txt         # Dependencias Python- DigitalOcean (Ubuntu 22.04 LTS)```

│   ├── Dockerfile               # Imagen Docker backend

│   └── start_backend.py         # Script de inicio- DuckDNS (DNS dinámico)

│

├── public/                       # Frontend (archivos estáticos)**Dashboard:**

│   ├── index.html               # Landing page principal

│   ├── test-universidad.html   # ⚠️ TEMP: Test red universitaria---```

│   ├── test-ip-access.html     # ⚠️ TEMP: Test acceso por IP

│   ├── app/                     # Aplicación webhttp://localhost:5500/

│   │   ├── home.html           # Dashboard principal

│   │   ├── sesion-practica.html # ⭐ Práctica con validación IA## 🚀 Instalación Local```

│   │   ├── materiales.html     # Gestión de materiales PDF

│   │   ├── repasos.html        # Sistema de repasos

│   │   ├── auth/               # Sistema de autenticación

│   │   │   ├── login.html### **Requisitos Previos**> **Nota**: El parámetro `material_id=1` corresponde al material cargado en el sistema. Si tienes múltiples materiales, cambia el número según corresponda.

│   │   │   └── crear-cuenta.html

│   │   └── institucional/      # Páginas informativas- Docker y Docker Compose instalados

│   │       ├── active-recall.html

│   │       └── validacion-semantica.html- Git## 📦 Requisitos

│   └── assets/                  # Recursos estáticos

│       ├── js/- 2GB RAM mínimo

│       │   ├── api.js          # Cliente API (auto-detecta hostname)

│       │   ├── validate-answer-real.js- Python 3.10+

│       │   └── upload-material.js

│       └── img/### **Paso 1: Clonar el Repositorio**- Librerías: FastAPI, Uvicorn, Sentence-Transformers

│

├── data/                         # Datos y materiales```bash- Navegador moderno (Chrome, Edge, Firefox)

│   ├── materials/               # PDFs subidos

│   ├── embeddings/              # Vectores (legacy, migrado a Supabase)git clone https://github.com/AbelMoyaCode/recuiva.git

│   └── materials_index.json

│cd recuiva**Instalar dependencias:**

├── docs/                         # Documentación completa

│   ├── SISTEMA_TR_TIEMPO_REAL.md``````bash

│   ├── ESTRUCTURA_FIRESTORE.md  # (legacy, ahora Supabase)

│   ├── DIAGNOSTICO_CHUNKS_PROBLEMA.md  # 🔧 Debugging de algoritmocd backend

│   └── README_COMPLETO.md

│### **Paso 2: Configurar Variables de Entorno**pip install -r requirements.txt

├── scripts/                      # Scripts de utilidad

│   ├── regenerar_indicadores.py```bash```

│   └── verificar_tr_consistencia.py

│cd backend

├── config/                       # Archivos de configuración

│   ├── user_config.jsoncp .env.example .env## 🎯 Características Principales

│   ├── infractivision_config.json

│   └── time_presets.json# Editar .env si es necesario

│

├── docker-compose.yml            # Orquestación de contenedores```- ✅ **Active Recall**: Práctica basada en recordar activamente

├── Dockerfile.frontend           # Imagen Docker frontend

├── nginx.conf                    # Configuración Nginx- 🤖 **Validación Semántica**: IA verifica comprensión conceptual

├── requirements.txt              # Dependencias unificadas

├── config.yaml                   # Configuración general### **Paso 3: Levantar con Docker Compose**- 📊 **Sistema de Puntuación**: Feedback detallado (0-100%)

└── README.md                     # 📖 Este archivo

``````bash- 💾 **Guardado Automático**: Progreso guardado en localStorage



> ⚠️ **NOTA:** Los archivos `test-universidad.html` y `test-ip-access.html` son **TEMPORALES** para diagnóstico de red. Eliminar después de verificar que el sistema funciona en la universidad.# Desde la raíz del proyecto- 📈 **Análisis de Evolución**: Métricas de aprendizaje



---docker compose up -d --build



## 🚀 Instalación y Uso```## 🔧 Configuración



### **Opción 1: Usar la Aplicación en Producción (Recomendado)**



**No necesitas instalar nada**, solo abre:### **Paso 4: Verificar que Funcione**Ver `config.yaml` para configuración del sistema.



``````bash

https://recuiva.duckdns.org

```# Backend## 📝 Uso



O si estás en una **red con firewall restrictivo**:curl http://localhost:8001/api/health



```# Respuesta esperada: {"status":"healthy","model_loaded":true}1. Inicia los servidores con `start-servers.ps1`

http://147.182.226.170

```2. Abre `http://localhost:5500/app/sesion-practica.html?material_id=1`



---# Frontend3. Escribe pregunta y respuesta (mínimo 1+1 caracteres)



### **Opción 2: Desarrollo Local**# Abrir en navegador: http://localhost:804. Click en "Validar con IA"



#### **Requisitos Previos**```5. Recibe feedback semántico instantáneo

- Python 3.10+

- Git

- 2GB RAM mínimo

- Navegador moderno (Chrome, Edge, Firefox)---**Control de funcionamiento:**



#### **Paso 1: Clonar el Repositorio**- Abre la consola del navegador (F12)

```bash

git clone https://github.com/AbelMoyaCode/recuiva.git## 📦 Despliegue en Producción- Verás logs de: "📁 Material ID: 1", "🌐 Conectando con servidor..."

cd recuiva

```- Si el backend responde, verás: "✅ Respuesta recibida del servidor"



#### **Paso 2: Configurar Backend**### **Con Dokploy (Recomendado)**- Si hay errores, aparecerán mensajes detallados en rojo

```bash

cd backend

pip install -r requirements.txt

```1. **Instalar Dokploy en el servidor:**## 🐛 Solución de Problemas



#### **Paso 3: Configurar Variables de Entorno**   ```bash



Crea `backend/.env`:   curl -sSL https://dokploy.com/install.sh | sh**Error: No se puede conectar al backend**

```bash

# Supabase Configuration   ```- Verifica que el backend esté corriendo en puerto 8000

SUPABASE_URL=https://xqicgzqgluslzleddmfv.supabase.co

SUPABASE_KEY=tu_service_role_key_aqui- Ejecuta: `curl http://localhost:8000/` (debe responder `{"status":"OK"}`)



# API Configuration2. **Crear proyecto en Dokploy UI:**

HOST=0.0.0.0

PORT=8001   - Nombre: `recuiva`**Página en blanco o errores de consola**

DEBUG=False

   - Tipo: `Docker Compose`- Asegúrate de abrir la URL correcta: `/app/sesion-practica.html`

# Model Configuration

MODEL_NAME=all-MiniLM-L6-v2   - Repositorio: `https://github.com/AbelMoyaCode/recuiva.git`- Verifica que ambos servidores estén corriendo

DEFAULT_CHUNK_SIZE=500

DEFAULT_CHUNK_OVERLAP=100   - Branch: `main`



# Thresholds**Modelo de IA no carga**

SIMILARITY_THRESHOLD_EXCELLENT=0.9

SIMILARITY_THRESHOLD_GOOD=0.73. **Configurar dominios:**- Primera vez tarda ~30 segundos descargando modelo

SIMILARITY_THRESHOLD_ACCEPTABLE=0.55

```   - Frontend: `recuiva.duckdns.org`- Revisa logs del backend



#### **Paso 4: Iniciar Backend**   - Backend: `api-recuiva.duckdns.org`

```bash

# Desde backend/## 📚 Documentación

python -m uvicorn main:app --reload --port 8001

```4. **Desplegar:**



#### **Paso 5: Iniciar Frontend** (en otra terminal)   - Click en "Deploy Server"- **Documentación antigua**: `docs/archive/`

```bash

# Desde raíz del proyecto   - Esperar a que termine el build (~2 minutos)- **API**: Ver `backend/README.md`

python -m http.server 5500 --directory public

```- **Deployment**: `docs/DEPLOYMENT_GUIDE.md`



#### **Paso 6: Abrir Navegador**### **Configuración de Traefik (Labels en docker-compose.yml)**

```

http://localhost:5500## 🌐 Deployment

```

```yaml

---

labels:Sistema listo para deployment con Docker:

### **Opción 3: Docker (Producción Local)**

  - traefik.enable=true```bash

```bash

# Desde raíz del proyecto  - traefik.docker.network=dokploy-networkdocker-compose up -d

docker compose up -d --build

  - traefik.http.routers.recuiva-backend-websecure.rule=Host(`api-recuiva.duckdns.org`)```

# Verificar estado

docker compose ps  - traefik.http.routers.recuiva-backend-websecure.entrypoints=websecure



# Ver logs  - traefik.http.routers.recuiva-backend-websecure.tls.certresolver=letsencrypt---

docker compose logs -f

  - traefik.http.services.recuiva-backend.loadbalancer.server.port=8001

# Acceder a la aplicación

# Frontend: http://localhost```**Última actualización**: Octubre 2025

# Backend:  http://localhost:8001

```**Versión**: 2.0 (Limpieza y reorganización completa)



------



## 📖 Uso de la API## 📖 Uso de la API



### **1. Health Check**### **Endpoints Principales**

```bash

GET /api/health#### **1. Health Check**

``````bash

GET /api/health

**Respuesta:**```

```json```json

{{

  "status": "healthy",  "status": "healthy",

  "timestamp": "2025-11-06T15:30:45.123456",  "timestamp": "2025-10-21T03:04:15.261906",

  "model_loaded": true,  "model_loaded": true

  "model_name": "all-MiniLM-L6-v2",}

  "embedding_dimensions": 384```

}

```#### **2. Subir Material**

```bash

---POST /api/materials/upload

Content-Type: multipart/form-data

### **2. Subir Material (PDF)**

```bashfile: <archivo.pdf>

POST /api/materials/upload```

Content-Type: multipart/form-data```json

{

file: <archivo.pdf>  "material_id": "abc123",

```  "filename": "capitulo1.pdf",

  "chunks": 153,

**Respuesta:**  "pages": 24,

```json  "status": "processed"

{}

  "success": true,```

  "material_id": "abc123xyz",

  "filename": "Odontologia_Capitulo1.pdf",#### **3. Validar Respuesta**

  "total_chunks": 153,```bash

  "estimated_pages": 24,POST /api/validate-answer

  "total_characters": 38450,Content-Type: application/json

  "processing_time_seconds": 12.5

}{

```  "question_id": "q1",

  "user_answer": "Porque vivía en el mismo edificio..."

---}

```

### **3. Validar Respuesta (IA Semántica)**```json

```bash{

POST /api/validate-answer  "score": 90.5,

Content-Type: application/json  "classification": "EXCELENTE",

  "feedback": "Has demostrado comprensión profunda del concepto",

{  "matched_fragment": "Chunk 53 de 153",

  "question_id": "q1",  "fragment_text": "...porque vivía en el mismo edificio...",

  "question_text": "¿Qué es la necrosis pulpar?",  "similarity_details": {

  "user_answer": "Es la muerte del tejido nervioso del diente causada por infección o trauma",    "method": "Sentence Transformers (all-MiniLM-L6-v2)"

  "material_id": "abc123xyz"  }

}}

``````



**Respuesta:**---

```json

{## 🔧 Comandos Útiles

  "success": true,

  "score": 92.5,### **Ver logs de contenedores:**

  "classification": "EXCELENTE",```bash

  "similarity": 0.87,# Backend

  "feedback": "¡Excelente comprensión! Has demostrado dominio profundo del concepto de necrosis pulpar.",docker logs recuiva-recuiva-7mk1x0-backend-1 -f

  "relevant_chunks": [

    {# Frontend

      "text": "La necrosis pulpar es la muerte del tejido pulpar (nervioso) del diente...",docker logs recuiva-recuiva-7mk1x0-frontend-1 -f

      "text_full": "...[texto completo del chunk]...",```

      "similarity": 0.87,

      "position": 53,### **Reiniciar servicios:**

      "total_chunks": 153```bash

    }docker restart recuiva-recuiva-7mk1x0-backend-1

  ],docker restart recuiva-recuiva-7mk1x0-frontend-1

  "scoring_breakdown": {```

    "base_similarity": 87.0,

    "context_bonus": 3.0,### **Ver estado de Traefik:**

    "keyword_bonus": 1.5,```bash

    "final_score": 92.5curl http://localhost:8080/api/http/routers | jq

  }```

}

```### **Rebuild completo:**

```bash

---docker compose down

docker compose build --no-cache

## ⚠️ Problemas Comunes y Solucionesdocker compose up -d

```

### **1. Error: "Backend no disponible" en Frontend**

---

**Causa:** CORS o backend no iniciado

## 🧪 Testing

**Solución:**

```bash### **Probar el Backend Localmente:**

# Verificar que backend esté corriendo```bash

curl http://localhost:8001/api/healthcd backend

python -m pytest tests/

# Verificar CORS en main.py```

grep "allow_origins" backend/main.py

```### **Probar un endpoint manualmente:**

```bash

---curl -X POST http://localhost:8001/api/validate-answer \

  -H "Content-Type: application/json" \

### **2. Error: "Modelo no se carga" (Model Loading Failed)**  -d '{

    "question_id": "test",

**Causa:** Primera descarga del modelo (requiere Internet)    "user_answer": "Respuesta de prueba"

  }'

**Solución:**```

```bash

# Esperar 30-60 segundos en primera ejecución---

# Ver logs del backend

docker compose logs backend -f## 📊 Estructura de Directorios



# Debe aparecer:```

# ✅ Modelo all-MiniLM-L6-v2 cargado exitosamenterecuiva/

```├── assets/                 # Recursos estáticos (JS, imágenes)

│   ├── js/

---│   │   ├── api.js         # Cliente de la API

│   │   ├── upload-material.js

### **3. Error: "Supabase connection failed"**│   │   └── validate-answer.js

│   └── img/

**Causa:** Variables de entorno incorrectas├── backend/                # Código del backend FastAPI

│   ├── main.py            # App principal

**Solución:**│   ├── embeddings_module.py

```bash│   ├── chunking.py

# Verificar variables│   └── requirements.txt

docker compose exec backend env | grep SUPABASE├── public/                 # Frontend HTML

│   ├── index.html

# Debe mostrar:│   ├── dashboard.html

# SUPABASE_URL=https://xqicgzqgluslzleddmfv.supabase.co│   └── app/

# SUPABASE_KEY=eyJhbGciOi...│       ├── subir-material.html

```│       └── sesion-practica.html

├── data/                   # Datos persistentes

---│   ├── materials/

│   └── embeddings/

### **4. Error 404 al acceder por IP (http://147.182.226.170)**├── docs/                   # Documentación adicional

├── docker-compose.yml      # Orquestación de contenedores

**Causa:** Traefik no configurado para IP├── Dockerfile              # Imagen del backend

├── Dockerfile.frontend     # Imagen del frontend

**Solución:**└── README.md               # Este archivo

Ya está **solucionado** en versión 2.0.0. Verificar:```

```bash

# Ver labels de Traefik---

docker inspect recuiva-frontend-1 | grep traefik.http.routers

## 🔒 Seguridad

# Debe incluir:

# traefik.http.routers.recuiva-frontend-ip.rule=PathPrefix(`/`)- ✅ **HTTPS obligatorio** (certificados SSL automáticos)

```- ✅ **CORS configurado** solo para dominios permitidos

- ✅ **Healthchecks** para monitoreo

---- ✅ **Rate limiting** en endpoints sensibles

- ✅ **Validación de entrada** en todos los endpoints

### **5. Chunks irrelevantes en validación semántica**

---

**Causa:** Bug corregido en versión 2.0.0

## 🐛 Problemas Comunes y Soluciones

**Solución implementada:**

- ✅ Normalización de scores corregida (eliminado `(x+1)/2`)### **1. Backend devuelve 404**

- ✅ Bonificaciones reducidas a la mitad```bash

- ✅ Embeddings solo de respuesta (no combinados con pregunta)# Verificar que los labels de Traefik estén correctos

- ✅ Chunk size optimizado a 500 caracteresdocker inspect recuiva-recuiva-7mk1x0-backend-1 | grep traefik

```

Ver `docs/DIAGNOSTICO_CHUNKS_PROBLEMA.md` para detalles técnicos.

### **2. CORS Error en el Frontend**

---```bash

# Verificar que ALLOWED_ORIGINS incluya tu dominio

## 🔐 Seguridad y Mejores Prácticasdocker exec recuiva-recuiva-7mk1x0-backend-1 env | grep ALLOWED_ORIGINS

```

### **Implementado:**

- ✅ **HTTPS obligatorio** (certificados SSL Let's Encrypt)### **3. Puerto 8001 ocupado**

- ✅ **CORS configurado** (`allow_origins=["*"]` solo en desarrollo)```bash

- ✅ **Autenticación JWT** con Supabase Auth# Ver qué está usando el puerto

- ✅ **Validación de entrada** en todos los endpointssudo lsof -i :8001

- ✅ **Healthchecks** cada 30 segundos# Detener contenedores conflictivos

- ✅ **Variables de entorno** para secretosdocker compose down

- ✅ **Logs estructurados** con timestamps```



### **Recomendaciones:**### **4. Modelo no se carga**

- 🔒 **NO** commitear `.env` a GitHub```bash

- 🔒 Rotar `SUPABASE_KEY` cada 3 meses# Verificar logs del backend

- 🔒 Usar `service_role_key` solo en backenddocker logs recuiva-recuiva-7mk1x0-backend-1 | grep "Modelo"

- 🔒 Usar `anon_key` en frontend# Debe decir: "✅ Modelo all-MiniLM-L6-v2 cargado exitosamente"

- 🔒 Habilitar MFA en cuenta de Dokploy```

- 🔒 Backups diarios de Supabase (configurar en dashboard)

---

---

## 🚧 Roadmap (Mejoras Futuras)

## 📊 Métricas y Rendimiento

- [ ] Instalar Tailwind CSS localmente (eliminar CDN)

### **Backend (FastAPI)**- [ ] Autenticación de usuarios (JWT)

- **Tiempo de respuesta promedio:** <200ms- [ ] Base de datos PostgreSQL

- **Validación semántica:** <500ms (incluye cálculo de embeddings)- [ ] CI/CD con GitHub Actions

- **Upload PDF (10 MB):** <3 segundos- [ ] Tests automatizados (pytest + coverage)

- **Generación de embeddings:** ~100 chunks/segundo- [ ] Monitoreo con Prometheus + Grafana

- [ ] Backups automáticos

### **Base de Datos (Supabase + pgvector)**- [ ] PWA (Progressive Web App)

- **Búsqueda de similitud:** <50ms (con índices IVFFlat)- [ ] Modo offline

- **Almacenamiento de embeddings:** 384 dims × 4 bytes = 1.5 KB por chunk

- **153 embeddings actuales:** ~229 KB total---



### **Infraestructura (DigitalOcean)**## 👥 Contribución

- **RAM usada:** ~800 MB / 2 GB (40%)

- **CPU:** <20% en uso normal¡Las contribuciones son bienvenidas! Por favor:

- **Ancho de banda:** Ilimitado (DuckDNS)

- **Uptime:** 99.9% (monitorizado por Dokploy)1. Fork el repositorio

2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`

---3. Commit: `git commit -am 'Añade nueva funcionalidad'`

4. Push: `git push origin feature/nueva-funcionalidad`

## 🚧 Roadmap y Mejoras Futuras5. Abre un Pull Request



### **Versión 2.1 (Próxima)**---

- [ ] Sistema de repetición espaciada (Spaced Repetition)

- [ ] Exportación de estadísticas a Excel/CSV## 📄 Licencia

- [ ] Modo oscuro (Dark Mode)

- [ ] PWA (Progressive Web App) para uso offlineEste proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

- [ ] Notificaciones push de recordatorios

---

### **Versión 2.2**

- [ ] Integración con Google Calendar (planificación de repasos)## 👤 Autor

- [ ] Generación automática de preguntas con GPT-4

- [ ] Comparación de respuestas con IA generativa**Abel Jesús Moya Acosta**

- [ ] Análisis de evolución con gráficos avanzados (Chart.js)- GitHub: [@AbelMoyaCode](https://github.com/AbelMoyaCode)

- Email: abelmoya2@upao.edu.pe

### **Versión 3.0**

- [ ] Modo colaborativo (compartir materiales entre usuarios)---

- [ ] Gamificación (puntos, niveles, logros)

- [ ] API pública para integraciones## 🙏 Agradecimientos

- [ ] Soporte para videos (YouTube) como material de estudio

- [ ] Reconocimiento de voz para respuestas orales- [Sentence Transformers](https://www.sbert.net/) por el modelo de embeddings

- [FastAPI](https://fastapi.tiangolo.com/) por el excelente framework

---- [Dokploy](https://dokploy.com/) por simplificar el despliegue

- [DuckDNS](https://www.duckdns.org/) por DNS gratuito

## 👥 Contribución

---

¡Las contribuciones son bienvenidas! 

## 📞 Soporte

### **Cómo contribuir:**

Si tienes problemas o preguntas:

1. **Fork** el repositorio

2. Crea una **rama** para tu feature:1. Revisa la sección [Problemas Comunes](#-problemas-comunes-y-soluciones)

   ```bash2. Consulta la [documentación completa](docs/README_COMPLETO.md)

   git checkout -b feature/nombre-descriptivo3. Abre un [Issue en GitHub](https://github.com/AbelMoyaCode/recuiva/issues)

   ```4. Contacta al autor

3. **Commit** tus cambios:

   ```bash---

   git commit -m "feat: descripción clara del cambio"

   ```**¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!**

4. **Push** a tu fork:

   ```bash---

   git push origin feature/nombre-descriptivo

   ```**Última actualización:** 21 de octubre de 2025  

5. Abre un **Pull Request** en GitHub**Versión:** 1.0.0 (Producción)


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
- **[Dokploy](https://dokploy.com/)** - Por simplificar el despliegue con Docker
- **[Traefik](https://traefik.io/)** - Por el reverse proxy automático
- **[DuckDNS](https://www.duckdns.org/)** - Por el DNS dinámico gratuito
- **[DigitalOcean](https://www.digitalocean.com/)** - Por la infraestructura cloud confiable
- **[Tailwind CSS](https://tailwindcss.com/)** - Por el framework de CSS utility-first

---

## 📞 Soporte y Contacto

### **Si tienes problemas:**

1. 📖 Revisa la sección [Problemas Comunes](#-problemas-comunes-y-soluciones)
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

**Desarrollado con ❤️ por Abel Moya - Noviembre 2025**

**¡Aprende más eficientemente con Recuiva!** 🚀
