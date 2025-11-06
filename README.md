# 🎓 Recuiva - Sistema de Active Recall con Validación Semántica mediante IA# 🎓 Recuiva - Sistema de Active Recall con IA# 🎓 Recuiva - Sistema de Active Recall con IA



![Estado: Producción](https://img.shields.io/badge/Estado-Producción-success)

![Versión](https://img.shields.io/badge/Versión-2.0.0-blue)

![Python](https://img.shields.io/badge/Python-3.10-blue)![Estado: Producción](https://img.shields.io/badge/Estado-Producción-success)

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green)![Versión](https://img.shields.io/badge/Versión-2.0.0-blue)

![pgvector](https://img.shields.io/badge/pgvector-0.8.0-orange)

![Python](https://img.shields.io/badge/Python-3.10-blue)![Estado: Producción](https://img.shields.io/badge/Estado-Producción-success)Sistema de aprendizaje basado en Active Recall con validación semántica mediante IA.

**Plataforma de aprendizaje basada en Active Recall con validación semántica automática mediante Inteligencia Artificial**

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

Sistema completo que permite a estudiantes mejorar su retención de conocimiento mediante técnicas de recuperación activa (Active Recall), validadas con análisis semántico de última generación usando embeddings vectoriales y similitud del coseno.

![Docker](https://img.shields.io/badge/Docker-Compose-blue)![Versión](https://img.shields.io/badge/Versión-1.0.0-blue)

---

![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green)

## 🌐 Aplicación en Producción

![Python](https://img.shields.io/badge/Python-3.10-blue)## 🏗️ Estructura del Proyecto

| Servicio | URL | Descripción |

|----------|-----|-------------|**Plataforma de aprendizaje basada en Active Recall con validación semántica mediante Inteligencia Artificial**

| 🌍 **Frontend** | [https://recuiva.duckdns.org](https://recuiva.duckdns.org) | Aplicación web completa |

| 🔧 **API Backend** | [https://api-recuiva.duckdns.org](https://api-recuiva.duckdns.org) | API REST FastAPI |![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

| 📖 **Documentación API** | [https://api-recuiva.duckdns.org/docs](https://api-recuiva.duckdns.org/docs) | Swagger UI interactivo |

| 💚 **Health Check** | [https://api-recuiva.duckdns.org/api/health](https://api-recuiva.duckdns.org/api/health) | Estado del servidor |Sistema completo que permite a estudiantes mejorar su retención de conocimiento mediante técnicas de recuperación activa, validadas con análisis semántico de última generación usando Sentence Transformers.

| 🔗 **IP Directa** | [http://147.182.226.170](http://147.182.226.170) | Acceso sin DNS |

![Docker](https://img.shields.io/badge/Docker-Compose-blue)```

### ⚠️ **Acceso desde Redes Restrictivas**

---

Si estás en una **red universitaria o empresarial** que bloquea DNS dinámicos (DuckDNS), usa la **IP directa**:

recuiva/

```

Frontend: http://147.182.226.170## 🌐 Aplicación en Producción

Backend:  http://147.182.226.170:8001

```Sistema de estudio basado en **Active Recall** con validación semántica de respuestas usando **Inteligencia Artificial** (Sentence Transformers).├── backend/              # Backend FastAPI



El sistema detecta automáticamente el hostname y configura las URLs correctas.### **URLs Principales**



---│   ├── main.py          # API principal



## 🎯 Objetivos del Proyecto| Servicio | URL | Descripción |



### **📌 Objetivo General (OG)**|----------|-----|-------------|---│   ├── embeddings_module.py



Desarrollar un MVP de aplicación web que permita la práctica de **Active Recall** mediante **validación semántica automática**, utilizando **embeddings vectoriales** y **base de datos vectorial (pgvector)** para contrastar respuestas del usuario con fragmentos específicos de documentos PDF.| 🌍 **Frontend** | [https://recuiva.duckdns.org](https://recuiva.duckdns.org) | Aplicación web completa |



---| 🔧 **API Backend** | [https://api-recuiva.duckdns.org](https://api-recuiva.duckdns.org) | API REST FastAPI |│   ├── chunking.py



### **📍 Objetivos Específicos (OE)**| 📖 **Documentación API** | [https://api-recuiva.duckdns.org/docs](https://api-recuiva.duckdns.org/docs) | Swagger UI interactivo |



| ID | Objetivo | Tecnologías Principales | Estado || 💚 **Health Check** | [https://api-recuiva.duckdns.org/api/health](https://api-recuiva.duckdns.org/api/health) | Estado del servidor |## 🌐 Aplicación en Producción│   └── requirements.txt

|----|----------|-------------------------|--------|

| **OE1** | **Sistema de embeddings y recuperación semántica**: Implementar modelo MiniLM-L6-v2 con Sentence Transformers para análisis semántico automatizado de respuestas del usuario comparadas con fragmentos específicos del documento fuente. | `sentence-transformers`<br>`PyTorch`<br>`Pinecone/Chroma/FAISS` | ✅ **Completado** || 🔗 **IP Directa** | [http://147.182.226.170](http://147.182.226.170) | Acceso sin DNS (universidades) |

| **OE2** | **Validación semántica automática**: Desarrollar pipeline de validación que identifique sinónimos, variaciones contextuales y respuestas parcialmente correctas mediante análisis vectorial avanzado con LangChain, logrando alta precisión de coherencia. | `LangChain`<br>`pgvector`<br>`cosine_similarity` | ✅ **Completado** |

| **OE3** | **Múltiples herramientas de Active Recall**: Integrar auto-preguntas, validación semántica y repetición espaciada usando el mismo motor de embeddings. | `FastAPI`<br>`Supabase`<br>`PostgreSQL + pgvector` | ✅ **Completado** |├── public/              # Frontend (archivos servidos)

| **OE4** | **Interfaz minimalista anti-pasividad**: Diseñar interfaz web basada en el flujo **intento → revelo → califico**, implementando sistema anti-pasividad (flujo intento → revelo → califico y repetición espaciada mínima). | `Tailwind CSS`<br>`JavaScript Vanilla`<br>`Responsive Design` | ✅ **Completado** |

### ⚠️ **IMPORTANTE: Acceso desde Redes Restrictivas**

---

- **🌍 Frontend:** [https://recuiva.duckdns.org](https://recuiva.duckdns.org)│   ├── index.html      # Landing page principal

## ✨ Características Principales

Si estás en una **red universitaria o empresarial** que bloquea DNS dinámicos (DuckDNS), usa la **IP directa**:

### 🧠 **Validación Semántica con IA**

- Modelo **Sentence Transformers** (`all-MiniLM-L6-v2`, 384 dimensiones)- **🔧 API Backend:** [https://api-recuiva.duckdns.org](https://api-recuiva.duckdns.org)│   ├── dashboard.html  # Dashboard de usuario

- Cálculo de **similitud del coseno** entre respuesta y material académico

- Clasificación automática:```

  - **EXCELENTE** (≥85%): Comprensión profunda

  - **BUENO** (70-84%): Comprensión sólidaFrontend: http://147.182.226.170- **📖 Documentación API:** [https://api-recuiva.duckdns.org/docs](https://api-recuiva.duckdns.org/docs)│   ├── landing-page.html

  - **ACEPTABLE** (55-69%): Comprensión básica

  - **INSUFICIENTE** (<55%): Requiere repasoBackend:  http://147.182.226.170:8001

- Muestra los **3 fragmentos más relevantes** del material

```- **💚 Health Check:** [https://api-recuiva.duckdns.org/api/health](https://api-recuiva.duckdns.org/api/health)│   └── app/            # Aplicación web

### 📚 **Gestión de Materiales**

- Sube **PDFs** o archivos **TXT** (hasta 50 MB)

- Fragmentación inteligente (**chunking**) de 500 caracteres

- Generación automática de **embeddings vectoriales****El sistema detectará automáticamente el hostname y configurará las URLs correctas.**│       ├── sesion-practica.html    # ⭐ Página principal de práctica

- Almacenamiento en **Supabase PostgreSQL + pgvector**



### 🎯 **Sistema de Preguntas**

- Crea preguntas basadas en tus materiales------│       ├── materiales.html         # Gestión de materiales PDF

- Responde sin ver el material (Active Recall puro)

- Retroalimentación instantánea con score semántico

- Historial completo de respuestas

## ✨ Características Principales│       ├── repasos.html           # Sistema de repasos espaciados

### 📊 **Análisis y Estadísticas**

- Dashboard con métricas en tiempo real

- Gráficos de evolución de scores

- Identificación de temas débiles### 🧠 **Validación Semántica con IA**## ✨ Características Principales│       ├── dashboard.html         # Dashboard de progreso

- Sistema de repetición espaciada (próximamente)

- Usa **Sentence Transformers** (modelo `all-MiniLM-L6-v2`, 384 dimensiones)

### 🔐 **Autenticación y Seguridad**

- **Supabase Auth** (email/contraseña + OAuth)- Calcula **similitud del coseno** entre respuesta del usuario y material académico│       ├── evolucion.html

- Sesiones persistentes con JWT

- HTTPS obligatorio (Let's Encrypt)- Clasifica automáticamente:



---  - **EXCELENTE** (≥85%): Comprensión profunda### 🧠 Validación Semántica con IA│       ├── mi-perfil.html



## 🧮 Algoritmo de Similitud del Coseno  - **BUENO** (70-84%): Comprensión sólida



### **¿Qué es la Similitud del Coseno?**  - **ACEPTABLE** (55-69%): Comprensión básica- Usa **Sentence Transformers** (modelo `all-MiniLM-L6-v2`)│       ├── subir-material.html



La **similitud del coseno** mide el ángulo entre dos vectores en un espacio multidimensional (384 dimensiones). **No** mide distancia, sino **dirección semántica**.  - **INSUFICIENTE** (<55%): Requiere repaso



**Rango:** 0 (completamente diferentes) → 1 (idénticos)- Identifica y muestra los **3 fragmentos más relevantes** del material- Calcula similitud coseno entre tu respuesta y el material│       ├── analytics.html



**Fórmula matemática:**



$$### 📚 **Gestión de Materiales**- Clasifica automáticamente: **EXCELENTE** (>90%), **BUENO** (70-90%), **ACEPTABLE** (50-70%)│       ├── auth/                  # Sistema de autenticación

\text{similitud}(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{||\mathbf{A}|| \times ||\mathbf{B}||} = \frac{\sum_{i=1}^{384} A_i B_i}{\sqrt{\sum_{i=1}^{384} A_i^2} \times \sqrt{\sum_{i=1}^{384} B_i^2}}

$$- Sube **PDFs** o archivos **TXT** (hasta 50 MB)



Donde:- Fragmentación inteligente en chunks de **500 caracteres** (optimizado para precisión)- Identifica el fragmento más relevante del material│       ├── institucional/         # Páginas informativas

- $\mathbf{A}$ = Embedding de la respuesta del usuario (384 dims)

- $\mathbf{B}$ = Embedding del chunk del material (384 dims)- Generación automática de **embeddings vectoriales** (384 dimensiones)



---- Almacenamiento en **Supabase PostgreSQL** con extensión **pgvector**│       │   ├── active-recall.html



### **🔄 Flujo Completo del Algoritmo (Paso a Paso)**- Organización por carpetas (Semestre, Curso, Tema)



```### 📚 Gestión de Materiales│       │   ├── validacion-semantica.html

┌───────────────────────────────────────────────────────────────────┐

│ PASO 1: PREPARACIÓN DE DATOS (Upload de PDF)                     │### 🎯 **Sistema de Preguntas Inteligente**

└───────────────────────────────────────────────────────────────────┘

  │- Crea preguntas basadas en tus materiales académicos- Sube **PDFs** o archivos **TXT**│       │   └── diferencias.html

  ├─► PDF/TXT → PyPDF2 extrae texto plano

  │- Responde sin ver el material (Active Recall puro)

  ├─► Chunking: Divide en fragmentos de 500 caracteres (overlap 100)

  │   Ejemplo: "La necrosis pulpar es la muerte del tejido nervioso..."- Retroalimentación instantánea con score de similitud semántica- Fragmentación automática en chunks de 500 caracteres│       └── assets/               # Recursos estáticos

  │

  └─► Sentence Transformers genera embeddings (384 dimensiones)- Historial completo de respuestas y progreso

         │

         ▼- **Bonificaciones inteligentes**: contexto, keywords, longitud- Generación de embeddings para búsqueda semántica├── data/               # Datos y materiales

     [0.123, -0.456, 0.789, 0.234, ..., -0.112]  (384 valores)

         │

         ▼

┌───────────────────────────────────────────────────────────────────┐### 📊 **Análisis y Estadísticas**- Organización por carpetas (Semestre, Curso, Tema)│   ├── materials/      # Materiales de estudio (PDFs)

│ PASO 2: ALMACENAMIENTO EN SUPABASE                                │

└───────────────────────────────────────────────────────────────────┘- Dashboard con métricas de estudio en tiempo real

  │

  └─► INSERT INTO material_embeddings (- Gráficos de evolución de scores por sesión│   ├── embeddings/     # Vectores de embeddings

        chunk_text TEXT,

        embedding VECTOR(384),  ← Tipo vectorial de pgvector- Identificación automática de temas débiles

        material_id UUID,

        chunk_index INTEGER- Sistema de repetición espaciada (próximamente)### 🎯 Sistema de Preguntas│   └── materials_index.json

      )

         │- Exportación de datos a JSON

         ▼

┌───────────────────────────────────────────────────────────────────┐- Crea preguntas basadas en tus materiales├── docs/               # Documentación del proyecto

│ PASO 3: USUARIO RESPONDE PREGUNTA                                 │

└───────────────────────────────────────────────────────────────────┘### 🔐 **Autenticación y Seguridad**

  │

  ├─► Usuario escribe: "La necrosis pulpar es la muerte del- Sistema de autenticación con **Supabase Auth**- Responde sin ver el material (Active Recall)│   ├── ANALISIS_SISTEMA_USUARIOS.md    # Análisis del sistema de usuarios

  │                      tejido nervioso del diente por infección"

  │- Login con email/contraseña + OAuth (Google, GitHub)

  └─► Frontend envía POST /api/validate-answer

         │- Sesiones persistentes con tokens JWT- Retroalimentación instantánea con score de similitud│   ├── DEPLOYMENT_GUIDE.md             # Guía de deployment

         ▼

┌───────────────────────────────────────────────────────────────────┐- Todos los datos privados por usuario

│ PASO 4: GENERACIÓN DE EMBEDDING DE RESPUESTA                      │

└───────────────────────────────────────────────────────────────────┘- HTTPS obligatorio con certificados Let's Encrypt- Historial de respuestas y progreso│   ├── DEPLOYMENT_GUIDE_DIGITALOCEAN.md # Deployment en DigitalOcean

  │

  └─► Sentence Transformers.encode(user_answer)

         │

         ▼---│   ├── INICIO_RAPIDO.md                # Guía de inicio rápido

     [0.156, -0.423, 0.812, 0.267, ..., -0.098]  (384 valores)

         │

         ▼

┌───────────────────────────────────────────────────────────────────┐## 🏗️ Arquitectura del Sistema### 📊 Análisis y Estadísticas│   └── README_COMPLETO.md              # Documentación completa

│ PASO 5: BÚSQUEDA VECTORIAL EN SUPABASE (pgvector)                │

└───────────────────────────────────────────────────────────────────┘

  │

  └─► SELECT chunk_text, chunk_index,```- Dashboard con métricas de estudio├── scripts/            # Scripts de utilidad

             1 - (embedding <=> '[0.156,-0.423,...]'::vector) AS similarity

      FROM material_embeddings┌─────────────────────────────────────────────────────────────┐

      WHERE material_id = 'abc123'

      ORDER BY embedding <=> '[0.156,-0.423,...]'::vector│                         INTERNET                            │- Gráficos de evolución de scores│   ├── completar_tareas.ps1

      LIMIT 10;

         ││              (DuckDNS + Let's Encrypt SSL)                  │

         ▼  [IVFFlat Index optimiza búsqueda: <50ms]

         │└────────────────────────┬────────────────────────────────────┘- Identificación de temas débiles│   ├── setup-server.sh

     Top 10 chunks más cercanos

         │                         │

         ▼

┌───────────────────────────────────────────────────────────────────┐            ┌────────────▼────────────┐- Repetición espaciada automática│   ├── fix-dokploy-port.sh

│ PASO 6: CÁLCULO DE SIMILITUD DEL COSENO (scikit-learn)           │

└───────────────────────────────────────────────────────────────────┘            │  Traefik v3.5           │

  │

  ├─► Para cada chunk candidato:            │  (Reverse Proxy)        ││   └── simple_backend.py

  │

  │   A = [0.156, -0.423, 0.812, ...]  (Respuesta usuario)            │  Puerto 80 → 443        │

  │   B = [0.123, -0.456, 0.789, ...]  (Chunk del material)

  │            └────────────┬────────────┘---├── assets/             # Assets globales

  │   1️⃣ Producto punto: A·B = Σ(A[i] × B[i])

  │      = (0.156 × 0.123) + (-0.423 × -0.456) + (0.812 × 0.789) + ...                         │

  │      = 0.0192 + 0.1929 + 0.6407 + ... = 245.67

  │         ┌───────────────┴──────────────┐│   ├── img/

  │   2️⃣ Normas (magnitudes):

  │      ||A|| = √(Σ A[i]²) = √(0.156² + (-0.423)² + ...) = 12.45         │                              │

  │      ||B|| = √(Σ B[i]²) = √(0.123² + (-0.456)² + ...) = 11.89

  │    ┌────▼─────┐                  ┌────▼─────┐## 🏗️ Arquitectura del Sistema│   └── js/

  │   3️⃣ Similitud del coseno:

  │      cos(θ) = 245.67 / (12.45 × 11.89) = 245.67 / 148.06 = 0.87    │ Frontend │                  │ Backend  │

  │

  └─► Resultado: 0.87 (87% de similitud semántica)    │  Nginx   │                  │ FastAPI  │├── config.yaml         # Configuración de la aplicación

         │

         ▼    │  :80     │◄─────CORS────────┤  :8001   │

┌───────────────────────────────────────────────────────────────────┐

│ PASO 7: SCORING INTELIGENTE (semantic_validator.py)              │    └──────────┘                  └────┬─────┘```├── requirements.txt    # Dependencias Python unificadas

└───────────────────────────────────────────────────────────────────┘

  │         │                              │

  ├─► Base similarity: 87.0%

  │    HTML/CSS/JS              ┌──────────▼──────────┐┌─────────────────────────────────────────────────────────────┐├── docker-compose.yml  # Orquestación de contenedores

  ├─► Context bonus (múltiples chunks relevantes):

  │   └─► 3+ chunks con sim >0.5? → +5%    Tailwind CSS             │ Sentence Transformers│

  │   └─► 2+ chunks con sim >0.5? → +3%

  │       Resultado: +3%    Supabase JS              │   all-MiniLM-L6-v2  ││                         INTERNET                            │├── Dockerfile          # Imagen Docker principal

  │

  ├─► Keyword bonus (contiene términos clave):                             │   PyTorch (CPU)     │

  │   └─► "necrosis", "pulpar", "tejido", "nervioso" → +1.5%

  │                             └─────────┬───────────┘│                  (DuckDNS + Let's Encrypt)                  │├── nginx.conf          # Configuración del servidor web

  ├─► Length bonus (respuesta suficientemente detallada):

  │   └─► >30 caracteres? → +0%                                       │

  │

  ├─► Intelligence boost (respuestas medias mejoradas):                              ┌────────▼─────────┐└────────────────────────┬────────────────────────────────────┘├── INICIAR_RECUIVA.bat # Script de inicio Windows

  │   └─► Similitud 50-70% + contexto bueno? → +8%

  │   └─► Similitud 35-50% + keywords? → +10%                              │  Supabase Cloud  │

  │       Resultado: +1%

  │                              │  PostgreSQL +    │                         │└── INICIAR_RECUIVA.ps1 # Script de inicio PowerShell

  └─► SCORE FINAL = 87 + 3 + 1.5 + 0 + 1 = 92.5%

         │                              │  pgvector v0.8.0 │

         ▼

┌───────────────────────────────────────────────────────────────────┐                              │  153 embeddings  │            ┌────────────▼────────────┐```

│ PASO 8: CLASIFICACIÓN Y FEEDBACK                                  │

└───────────────────────────────────────────────────────────────────┘                              └──────────────────┘

  │

  ├─► Score ≥ 85%  →  EXCELENTE ⭐⭐⭐```            │  Traefik (Reverse Proxy)│

  ├─► Score 70-84% →  BUENO ⭐⭐

  ├─► Score 55-69% →  ACEPTABLE ⭐

  └─► Score < 55%  →  INSUFICIENTE ❌

         │### **Flujo de Validación Semántica**            │    Puerto 80/443        │## 🚀 Inicio Rápido

         ▼

     Clasificación: EXCELENTE (92.5%)

     Feedback: "¡Excelente comprensión del concepto!"

         │```            └────────────┬────────────┘

         ▼

┌───────────────────────────────────────────────────────────────────┐1. Usuario escribe respuesta

│ PASO 9: RESPUESTA AL FRONTEND (JSON)                              │

└───────────────────────────────────────────────────────────────────┘   ↓                         │### 0. Instalar Dependencias

  │

  └─► {2. Frontend envía POST /api/validate-answer

        "score": 92.5,

        "classification": "EXCELENTE",   ↓         ┌───────────────┴──────────────┐

        "similarity": 0.87,

        "feedback": "¡Excelente! Has demostrado comprensión profunda.",3. Backend genera embedding (384 dims)

        "relevant_chunks": [

          {   ↓         │                              │```bash

            "text": "La necrosis pulpar es la muerte del tejido...",

            "similarity": 0.87,4. Consulta Supabase: SELECT similarity(embedding, ?)

            "position": 53,

            "total_chunks": 153   ↓    ┌────▼─────┐                  ┌────▼─────┐pip install -r requirements.txt

          },

          {5. pgvector calcula coseno con IVFFlat index

            "text": "Las causas principales incluyen infección...",

            "similarity": 0.82,   ↓    │ Frontend │                  │ Backend  │```

            "position": 54

          },6. Backend aplica scoring inteligente:

          {

            "text": "El tratamiento consiste en endodoncia...",   - Similitud base (coseno)    │  Nginx   │                  │ FastAPI  │

            "similarity": 0.75,

            "position": 55   - Bonus contexto (+0-5%)

          }

        ],   - Bonus keywords (+0-8%)    │  :80     │◄─────CORS────────┤  :8001   │### 1. Iniciar Servidores

        "scoring_breakdown": {

          "base_similarity": 87.0,   - Bonus longitud (+0-5%)

          "context_bonus": 3.0,

          "keyword_bonus": 1.5,   - Boost inteligencia (+0-10%)    └──────────┘                  └────┬─────┘

          "length_bonus": 0.0,

          "intelligence_boost": 1.0,   ↓

          "final_score": 92.5

        }7. Frontend muestra:         │                              │**Windows (Batch):**

      }

```   - Score final (0-100%)



---   - Clasificación (EXCELENTE/BUENO/ACEPTABLE/INSUFICIENTE)    HTML/CSS/JS              ┌──────────▼──────────┐```cmd



## 📊 Comparación: ¿Por qué Similitud del Coseno?   - Top 3 fragmentos relevantes



### **Tabla Comparativa de Algoritmos de Similitud**   - Feedback personalizado    Tailwind CSS             │ Sentence Transformers│INICIAR_RECUIVA.bat



| Algoritmo | Fórmula | Rango | Ventajas | Desventajas | ¿Usado en Recuiva? |```

|-----------|---------|-------|----------|-------------|--------------------|

| **Similitud del Coseno** ⭐ | $\frac{A \cdot B}{\\|A\\| \\|B\\|}$ | [0, 1] | ✅ Invariante a magnitud<br>✅ Captura dirección semántica<br>✅ Ideal para texto de longitud variable<br>✅ Rápido con índices IVFFlat | ❌ Ignora magnitud absoluta | ✅ **SÍ (Principal)** |                             │   all-MiniLM-L6-v2  │```

| **Distancia Euclidiana** | $\sqrt{\sum(A_i - B_i)^2}$ | [0, ∞] | ✅ Intuitiva<br>✅ Captura diferencias absolutas | ❌ Sensible a escala/longitud<br>❌ Malo para alta dimensionalidad (384 dims) | ❌ NO |

| **Similitud de Jaccard** | $\frac{\\|A \cap B\\|}{\\|A \cup B\\|}$ | [0, 1] | ✅ Buena para conjuntos<br>✅ Simple de calcular | ❌ Ignora frecuencias de palabras<br>❌ Pierde semántica profunda | ❌ NO |---

| **Distancia de Manhattan** | $\sum \\|A_i - B_i\\|$ | [0, ∞] | ✅ Menos sensible a outliers | ❌ Lento en 384 dimensiones<br>❌ No captura ángulos | ❌ NO |

| **Producto Punto** | $A \cdot B$ | [-∞, ∞] | ✅ Muy rápido | ❌ Sensible a magnitud<br>❌ No normalizado | ⚠️ Usado internamente |                             └─────────────────────┘



---## 🛠️ Stack Tecnológico



### **🏆 Razones para usar Similitud del Coseno**```**Windows (PowerShell):**



#### **1️⃣ Invariancia a la Magnitud (Longitud del Texto)**### **Frontend**



```- **HTML5** + **Tailwind CSS v3.3**```powershell

Ejemplo real:

- **JavaScript Vanilla** (sin frameworks, máxima compatibilidad)

Respuesta corta del estudiante:

  "muerte del tejido nervioso"- **Supabase JS Client** v2.38 (autenticación)---.\INICIAR_RECUIVA.ps1

  → Embedding: ||A|| = 5.2

- **Nginx** como servidor web estático

Respuesta larga del estudiante:

  "La necrosis pulpar es la muerte del tejido nervioso del diente,- **Responsive Design** (320px → 4K)```

   causada por infección bacteriana profunda o trauma severo que

   compromete la vitalidad pulpar..."

  → Embedding: ||A|| = 18.7

### **Backend**## 🛠️ Stack Tecnológico

Con Similitud del Coseno:

  - Ambas tienen ALTA similitud (~0.85) si el significado es correcto- **FastAPI** 0.104 (Python 3.10)

  - La longitud NO penaliza ni bonifica

- **Sentence Transformers** 2.2.2 (modelo all-MiniLM-L6-v2)**Manual:**

Con Distancia Euclidiana:

  - La respuesta larga parece "más diferente" (distancia mayor)- **PyTorch** 2.1.0 (versión CPU, optimizado)

  - FALSO NEGATIVO: Estudiante penalizado por ser detallado

```- **scikit-learn** 1.3.2 (cálculo de similitud coseno)### **Frontend**```powershell



**Ventaja:** Un estudiante conciso NO es penalizado.- **PyPDF2** 3.0.1 (extracción de texto de PDFs)



---- **Supabase Python Client** (conexión a PostgreSQL)- HTML5 + Tailwind CSS# Backend (puerto 8000)



#### **2️⃣ Captura Semántica (Dirección, NO Longitud)**



```python### **Infraestructura**- JavaScript Vanilla (sin frameworks)cd backend

# Ejemplo simplificado con 3 dimensiones (real: 384)

- **Docker** 24.0 + **Docker Compose** v2

vector_respuesta = [0.8, 0.5, 0.2]   # "necrosis pulpar"

vector_chunk_A   = [0.9, 0.4, 0.1]   # "necrosis del tejido dental"- **Dokploy** (CI/CD automático desde GitHub)- Nginx (servidor web estático)python -m uvicorn main:app --reload --port 8000

vector_chunk_B   = [0.1, 0.1, 0.9]   # "caries dental superficial"

- **Traefik** v3.5 (Reverse Proxy + SSL automático)

# Similitud del coseno

cos_sim(respuesta, chunk_A) = 0.92  ✅ Alta similitud- **DigitalOcean Droplet** (Ubuntu 22.04 LTS, 2GB RAM)

cos_sim(respuesta, chunk_B) = 0.31  ❌ Baja similitud

- **DuckDNS** (DNS dinámico gratuito)

# Los vectores apuntan en direcciones similares → mismo SIGNIFICADO

```- **Let's Encrypt** (certificados SSL válidos hasta 19/01/2026)### **Backend**# Frontend (puerto 5500) - en otra terminal



---



#### **3️⃣ Optimización con pgvector (PostgreSQL)**### **Base de Datos**- FastAPI (Python 3.10)cd ..



pgvector soporta el **operador de distancia coseno** (`<=>`):- **Supabase Cloud** (PostgreSQL 15.1)



```sql- **pgvector** v0.8.0 (vectores de 384 dimensiones)- Sentence Transformers (`sentence-transformers==2.2.2`)python -m http.server 5500 --directory public

-- Búsqueda ultra-rápida con índice IVFFlat

SELECT chunk_text, - **IVFFlat indices** (búsqueda rápida de similitud)

       1 - (embedding <=> '[0.1,0.2,...]'::vector) AS similarity

FROM material_embeddings- **153 embeddings** almacenados (~229 KB)- PyTorch (versión CPU)```

ORDER BY embedding <=> '[0.1,0.2,...]'::vector

LIMIT 3;



-- Complejidad:---- PyPDF2 (extracción de texto de PDFs)

--   Sin índice: O(n) = 500ms (para 153 embeddings)

--   Con IVFFlat: O(log n) = <50ms (10x más rápido)

```

## 📦 Estructura del Proyecto### 2. Acceder a la Aplicación

**Ventaja:** PostgreSQL optimiza específicamente para similitud del coseno.



---

```### **Infraestructura**

#### **4️⃣ Estándar en NLP y Modelos de Lenguaje**

recuiva/

- **BERT, GPT, Sentence Transformers** → Todos usan similitud del coseno

- **Papers científicos**: 95% de investigación en NLP usa coseno├── backend/                      # Backend FastAPI- Docker + Docker Compose**Página principal de práctica:**

- **Bibliotecas optimizadas**: `scikit-learn`, `numpy`, `torch` implementan coseno en hardware

│   ├── main.py                  # API principal (1014 líneas)

---

│   ├── semantic_validator.py   # Validador semántico (449 líneas)- Dokploy (CI/CD)```

### **📈 Comparación de Rendimiento (Dataset: 153 embeddings)**

│   ├── chunking.py              # Fragmentación de documentos

| Métrica | Coseno | Euclidiana | Jaccard | Manhattan |

|---------|--------|------------|---------|-----------|│   ├── embeddings_module.py    # Generación de embeddings- Traefik v3.5 (Reverse Proxy + SSL)http://localhost:5500/app/sesion-practica.html?material_id=1

| **Tiempo de cálculo** | 0.5 ms | 0.8 ms | 12 ms | 1.2 ms |

| **Precisión semántica** | 92% | 68% | 45% | 71% |│   ├── supabase_client.py      # Cliente Supabase

| **Recall** | 88% | 72% | 50% | 74% |

| **F1-Score** | 90% | 70% | 47% | 72% |│   ├── requirements.txt         # Dependencias Python- DigitalOcean (Ubuntu 22.04 LTS)```

| **Soporte pgvector** | ✅ Nativo | ✅ Nativo | ❌ No | ⚠️ Manual |

│   ├── Dockerfile               # Imagen Docker backend

**Conclusión:** Similitud del coseno es **2x más preciso** y **10x más rápido** con índices.

│   └── start_backend.py         # Script de inicio- DuckDNS (DNS dinámico)

---

│

## 🗄️ ¿Por qué Supabase + pgvector?

├── public/                       # Frontend (archivos estáticos)**Dashboard:**

### **Comparación: Supabase vs Alternativas para Bases de Datos Vectoriales**

│   ├── index.html               # Landing page principal

| Criterio | Supabase + pgvector ⭐ | Pinecone | Weaviate | ChromaDB | Firestore |

|----------|------------------------|----------|----------|----------|-----------|│   ├── test-universidad.html   # ⚠️ TEMP: Test red universitaria---```

| **Tipo** | PostgreSQL relacional + vectorial | Solo vectorial | Vector + graph | Solo vectorial | NoSQL document |

| **Costo** | ✅ **Gratis** (500 MB) | ❌ $70/mes | ❌ $25/mes | ✅ Gratis (local) | ⚠️ Pay-per-use |│   ├── test-ip-access.html     # ⚠️ TEMP: Test acceso por IP

| **Índices vectoriales** | ✅ IVFFlat, HNSW | ✅ Sí | ✅ Sí | ✅ Sí | ❌ No |

| **Datos relacionales** | ✅ Sí (PostgreSQL nativo) | ❌ No | ⚠️ Limitado | ❌ No | ⚠️ Limitado |│   ├── app/                     # Aplicación webhttp://localhost:5500/

| **Autenticación integrada** | ✅ Supabase Auth | ❌ No | ❌ No | ❌ No | ✅ Firebase Auth |

| **API REST automática** | ✅ Sí (auto-generada) | ⚠️ SDK only | ⚠️ SDK only | ⚠️ SDK only | ✅ Sí |│   │   ├── home.html           # Dashboard principal

| **Escalabilidad** | ✅ Hasta 8 GB (gratis) | ✅ Ilimitado | ✅ Ilimitado | ⚠️ Local | ✅ Ilimitado |

| **Latencia búsqueda** | ✅ <50ms (con IVFFlat) | ✅ <30ms | ✅ <40ms | ✅ <20ms | ❌ >200ms |│   │   ├── sesion-practica.html # ⭐ Práctica con validación IA## 🚀 Instalación Local```

| **SQL nativo** | ✅ Sí (PostgreSQL) | ❌ No | ❌ No | ❌ No | ❌ No |

| **Backups automáticos** | ✅ Sí (diarios) | ✅ Sí | ⚠️ Manual | ❌ No | ✅ Sí |│   │   ├── materiales.html     # Gestión de materiales PDF

| **Open Source** | ✅ Sí (PostgreSQL) | ❌ Propietario | ✅ Sí | ✅ Sí | ❌ Propietario |

| **Curva de aprendizaje** | ✅ Baja (SQL estándar) | ⚠️ Media (SDK nuevo) | ⚠️ Alta (GraphQL) | ⚠️ Media | ✅ Baja |│   │   ├── repasos.html        # Sistema de repasos



---│   │   ├── auth/               # Sistema de autenticación



### **🏆 Ventajas de Supabase + pgvector**│   │   │   ├── login.html### **Requisitos Previos**> **Nota**: El parámetro `material_id=1` corresponde al material cargado en el sistema. Si tienes múltiples materiales, cambia el número según corresponda.



#### **1️⃣ Mejor de Ambos Mundos: Relacional + Vectorial**│   │   │   └── crear-cuenta.html



```sql│   │   └── institucional/      # Páginas informativas- Docker y Docker Compose instalados

-- ✅ Query relacional + vectorial en UNA SOLA consulta

SELECT │   │       ├── active-recall.html

    m.title AS material,

    q.text AS pregunta,│   │       └── validacion-semantica.html- Git## 📦 Requisitos

    ua.user_answer,

    ua.score,│   └── assets/                  # Recursos estáticos

    me.chunk_text,

    1 - (me.embedding <=> ua.answer_embedding::vector) AS similarity│       ├── js/- 2GB RAM mínimo

FROM user_answers ua

JOIN questions q ON ua.question_id = q.id│       │   ├── api.js          # Cliente API (auto-detecta hostname)

JOIN materials m ON q.material_id = m.id

JOIN material_embeddings me ON me.material_id = m.id│       │   ├── validate-answer-real.js- Python 3.10+

WHERE ua.user_id = 'user123'

  AND ua.score >= 70│       │   └── upload-material.js

ORDER BY me.embedding <=> ua.answer_embedding::vector

LIMIT 5;│       └── img/### **Paso 1: Clonar el Repositorio**- Librerías: FastAPI, Uvicorn, Sentence-Transformers



-- ❌ Imposible en Pinecone (requiere 2 bases de datos)│

```

├── data/                         # Datos y materiales```bash- Navegador moderno (Chrome, Edge, Firefox)

**Ventaja:** NO necesitamos mantener 2 bases de datos (una relacional + una vectorial).

│   ├── materials/               # PDFs subidos

---

│   ├── embeddings/              # Vectores (legacy, migrado a Supabase)git clone https://github.com/AbelMoyaCode/recuiva.git

#### **2️⃣ Índices IVFFlat para Búsqueda Rápida**

│   └── materials_index.json

```sql

-- Crear índice IVFFlat (Inverted File with Flat compression)│cd recuiva**Instalar dependencias:**

CREATE INDEX material_embeddings_embedding_idx

ON material_embeddings├── docs/                         # Documentación completa

USING ivfflat (embedding vector_cosine_ops)

WITH (lists = 10);  -- 10 clusters para 153 embeddings│   ├── SISTEMA_TR_TIEMPO_REAL.md``````bash



-- Resultado:│   ├── ESTRUCTURA_FIRESTORE.md  # (legacy, ahora Supabase)

--   Sin índice:  500ms (full scan)

--   Con índice:   45ms (búsqueda aproximada)│   ├── DIAGNOSTICO_CHUNKS_PROBLEMA.md  # 🔧 Debugging de algoritmocd backend

--   Precisión:  99.2% (casi exacta)

```│   └── README_COMPLETO.md



**Cómo funciona IVFFlat:**│### **Paso 2: Configurar Variables de Entorno**pip install -r requirements.txt



```├── scripts/                      # Scripts de utilidad

1. Divide embeddings en 10 clusters (listas invertidas)

   │   ├── regenerar_indicadores.py```bash```

   Cluster 1: [emb_1, emb_15, emb_42, emb_78, ...]

   Cluster 2: [emb_3, emb_27, emb_89, emb_91, ...]│   └── verificar_tr_consistencia.py

   ...

   Cluster 10: [emb_5, emb_31, emb_76, emb_102, ...]│cd backend



2. Búsqueda (3 pasos):├── config/                       # Archivos de configuración

   a) Encuentra cluster más cercano al vector query (rápido)

   b) Busca solo dentro de ese cluster (10x más rápido)│   ├── user_config.jsoncp .env.example .env## 🎯 Características Principales

   c) Devuelve top-k resultados

│   ├── infractivision_config.json

3. Trade-off:

   - Velocidad: ✅ 10x más rápido│   └── time_presets.json# Editar .env si es necesario

   - Precisión: ✅ 99%+ (casi perfecta)

   - Memoria: ✅ Baja (solo índice pequeño)│

```

├── docker-compose.yml            # Orquestación de contenedores```- ✅ **Active Recall**: Práctica basada en recordar activamente

---

├── Dockerfile.frontend           # Imagen Docker frontend

#### **3️⃣ Costo CERO vs Competencia**

├── nginx.conf                    # Configuración Nginx- 🤖 **Validación Semántica**: IA verifica comprensión conceptual

| Proveedor | Plan Gratis | Costo Producción (nuestro uso) | Ahorro Anual |

|-----------|-------------|---------------------------------|--------------|├── requirements.txt              # Dependencias unificadas

| **Supabase** | 500 MB DB + 2 GB ancho de banda/mes | ✅ **$0/mes** | - |

| **Pinecone** | 1 índice (límite 100k vectores) | ❌ **$70/mes** | **$840 USD** |├── config.yaml                   # Configuración general### **Paso 3: Levantar con Docker Compose**- 📊 **Sistema de Puntuación**: Feedback detallado (0-100%)

| **Weaviate Cloud** | 14 días trial | ❌ **$25/mes** | **$300 USD** |

| **ChromaDB** | Solo local (self-hosted) | ⚠️ **VPS + mantenimiento** | **$120 USD** |└── README.md                     # 📖 Este archivo



**Ahorro total con Supabase:** $840-1200 USD/año 💰``````bash- 💾 **Guardado Automático**: Progreso guardado en localStorage



---



#### **4️⃣ Autenticación Integrada (Sin Código Extra)**> ⚠️ **NOTA:** Los archivos `test-universidad.html` y `test-ip-access.html` son **TEMPORALES** para diagnóstico de red. Eliminar después de verificar que el sistema funciona en la universidad.# Desde la raíz del proyecto- 📈 **Análisis de Evolución**: Métricas de aprendizaje



```javascript

// ✅ Supabase: Auth + DB en UN solo cliente

const { data: user } = await supabase.auth.signInWithPassword({---docker compose up -d --build

  email: 'usuario@upao.edu.pe',

  password: 'password123'

});

## 🚀 Instalación y Uso```## 🔧 Configuración

// Row Level Security (RLS) automático

const { data: materials } = await supabase

  .from('materials')

  .select('*')### **Opción 1: Usar la Aplicación en Producción (Recomendado)**

  .eq('user_id', user.id);  // ✅ Solo ve sus materiales



// ❌ Pinecone/Weaviate: Necesitas JWT propio + filtrado manual

```**No necesitas instalar nada**, solo abre:### **Paso 4: Verificar que Funcione**Ver `config.yaml` para configuración del sistema.



---



#### **5️⃣ Migraciones Sencillas (SQL Estándar)**``````bash



```sqlhttps://recuiva.duckdns.org

-- Migración 1: Crear tabla con vectores

CREATE TABLE material_embeddings (```# Backend## 📝 Uso

  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  material_id UUID REFERENCES materials(id),

  chunk_index INTEGER,

  chunk_text TEXT,O si estás en una **red con firewall restrictivo**:curl http://localhost:8001/api/health

  embedding VECTOR(384),  -- ← Tipo vectorial de pgvector

  created_at TIMESTAMPTZ DEFAULT NOW()

);

```# Respuesta esperada: {"status":"healthy","model_loaded":true}1. Inicia los servidores con `start-servers.ps1`

-- Migración 2: Agregar índice IVFFlat

CREATE INDEX ON material_embeddingshttp://147.182.226.170

USING ivfflat (embedding vector_cosine_ops);

```2. Abre `http://localhost:5500/app/sesion-practica.html?material_id=1`

-- Migración 3: Row Level Security

ALTER TABLE material_embeddings ENABLE ROW LEVEL SECURITY;



CREATE POLICY "Users see own embeddings"---# Frontend3. Escribe pregunta y respuesta (mínimo 1+1 caracteres)

ON material_embeddings

FOR SELECT

USING (

  material_id IN (### **Opción 2: Desarrollo Local**# Abrir en navegador: http://localhost:804. Click en "Validar con IA"

    SELECT id FROM materials WHERE user_id = auth.uid()

  )

);

```#### **Requisitos Previos**```5. Recibe feedback semántico instantáneo



**Con Pinecone:** Todo esto es código Python/JavaScript manual (sin migraciones versionadas).- Python 3.10+



---- Git



### **📊 Arquitectura de Almacenamiento en Supabase**- 2GB RAM mínimo



```- Navegador moderno (Chrome, Edge, Firefox)---**Control de funcionamiento:**

┌──────────────────────────────────────────────────────────────┐

│  SUPABASE CLOUD (PostgreSQL 15.1 + pgvector v0.8.0)         │

├──────────────────────────────────────────────────────────────┤

│                                                              │#### **Paso 1: Clonar el Repositorio**- Abre la consola del navegador (F12)

│  📁 materials (Tabla relacional)                             │

│  ├─ id (UUID, PK)                                            │```bash

│  ├─ user_id (UUID, FK → auth.users)                         │

│  ├─ title (TEXT)                                             │git clone https://github.com/AbelMoyaCode/recuiva.git## 📦 Despliegue en Producción- Verás logs de: "📁 Material ID: 1", "🌐 Conectando con servidor..."

│  ├─ filename (TEXT)                                          │

│  ├─ total_chunks (INTEGER)                                   │cd recuiva

│  ├─ estimated_pages (INTEGER)                                │

│  └─ uploaded_at (TIMESTAMPTZ)                                │```- Si el backend responde, verás: "✅ Respuesta recibida del servidor"

│                                                              │

│  🔢 material_embeddings (Tabla vectorial)                    │

│  ├─ id (UUID, PK)                                            │

│  ├─ material_id (UUID, FK → materials)                      │#### **Paso 2: Configurar Backend**### **Con Dokploy (Recomendado)**- Si hay errores, aparecerán mensajes detallados en rojo

│  ├─ chunk_index (INTEGER)                                    │

│  ├─ chunk_text (TEXT)                      ┌──────────────┐  │```bash

│  ├─ embedding (VECTOR(384)) ───────────────►│ IVFFlat Index│  │

│  └─ created_at (TIMESTAMPTZ)               │ (10 clusters)│  │cd backend

│                                             └──────────────┘  │

│  ❓ questions                                   ↑             │pip install -r requirements.txt

│  ├─ id (UUID, PK)                               │ Búsqueda   │

│  ├─ material_id (UUID, FK)                      │ <50ms      │```1. **Instalar Dokploy en el servidor:**## 🐛 Solución de Problemas

│  ├─ text (TEXT)                                 │            │

│  ├─ topic (TEXT)                                │            │

│  └─ difficulty (TEXT)                           │            │

│                                                 │            │#### **Paso 3: Configurar Variables de Entorno**   ```bash

│  ✅ user_answers                                │            │

│  ├─ id (UUID, PK)                               │            │

│  ├─ question_id (UUID, FK)                      │            │

│  ├─ user_id (UUID, FK)                          │            │Crea `backend/.env`:   curl -sSL https://dokploy.com/install.sh | sh**Error: No se puede conectar al backend**

│  ├─ user_answer (TEXT)                          │            │

│  ├─ score (NUMERIC)                             │            │```bash

│  ├─ similarity (NUMERIC)                        │            │

│  ├─ classification (TEXT)                       │            │# Supabase Configuration   ```- Verifica que el backend esté corriendo en puerto 8000

│  ├─ answer_embedding (VECTOR(384)) ────────────┘            │

│  └─ answered_at (TIMESTAMPTZ)                                │SUPABASE_URL=https://xqicgzqgluslzleddmfv.supabase.co

│                                                              │

│  📈 sessions (Tabla de sesiones de estudio)                  │SUPABASE_KEY=tu_service_role_key_aqui- Ejecuta: `curl http://localhost:8000/` (debe responder `{"status":"OK"}`)

│  ├─ id (UUID, PK)                                            │

│  ├─ user_id (UUID, FK)                                       │

│  ├─ material_id (UUID, FK)                                   │

│  ├─ started_at (TIMESTAMPTZ)                                 │# API Configuration2. **Crear proyecto en Dokploy UI:**

│  └─ ended_at (TIMESTAMPTZ)                                   │

│                                                              │HOST=0.0.0.0

└──────────────────────────────────────────────────────────────┘

PORT=8001   - Nombre: `recuiva`**Página en blanco o errores de consola**

📊 Almacenamiento actual:

  - 153 embeddings × 384 dims × 4 bytes/float = ~235 KBDEBUG=False

  - Índice IVFFlat (10 clusters): ~50 KB

  - Datos relacionales (texto, metadata): ~180 KB   - Tipo: `Docker Compose`- Asegúrate de abrir la URL correcta: `/app/sesion-practica.html`

  - TOTAL: ~465 KB de 500 MB disponibles (0.09% usado)

  # Model Configuration

✅ Capacidad restante: 499.5 MB (~107,000 embeddings más)

```MODEL_NAME=all-MiniLM-L6-v2   - Repositorio: `https://github.com/AbelMoyaCode/recuiva.git`- Verifica que ambos servidores estén corriendo



---DEFAULT_CHUNK_SIZE=500



## 🏗️ Arquitectura del SistemaDEFAULT_CHUNK_OVERLAP=100   - Branch: `main`



```

┌─────────────────────────────────────────────────────────────┐

│                      INTERNET                               │# Thresholds**Modelo de IA no carga**

│             (DuckDNS + Let's Encrypt SSL)                   │

└────────────────────┬────────────────────────────────────────┘SIMILARITY_THRESHOLD_EXCELLENT=0.9

                     │

        ┌────────────▼────────────┐SIMILARITY_THRESHOLD_GOOD=0.73. **Configurar dominios:**- Primera vez tarda ~30 segundos descargando modelo

        │  Traefik v3.5           │

        │  (Reverse Proxy)        │SIMILARITY_THRESHOLD_ACCEPTABLE=0.55

        │  Puerto 80 → 443 (SSL)  │

        └────────────┬────────────┘```   - Frontend: `recuiva.duckdns.org`- Revisa logs del backend

                     │

     ┌───────────────┴──────────────┐

     │                              │

┌────▼─────┐                  ┌────▼─────┐#### **Paso 4: Iniciar Backend**   - Backend: `api-recuiva.duckdns.org`

│ Frontend │                  │ Backend  │

│  Nginx   │                  │ FastAPI  │```bash

│  :80     │◄─────CORS────────┤  :8001   │

└──────────┘                  └────┬─────┘# Desde backend/## 📚 Documentación

     │                              │

HTML/CSS/JS          ┌──────────────▼──────────────┐python -m uvicorn main:app --reload --port 8001

Tailwind CSS         │ Sentence Transformers       │

Supabase JS          │ all-MiniLM-L6-v2 (384 dims) │```4. **Desplegar:**

                     │ PyTorch CPU                 │

                     └──────────────┬──────────────┘

                                    │

                          ┌─────────▼─────────┐#### **Paso 5: Iniciar Frontend** (en otra terminal)   - Click en "Deploy Server"- **Documentación antigua**: `docs/archive/`

                          │  Supabase Cloud   │

                          │  PostgreSQL 15.1  │```bash

                          │  pgvector v0.8.0  │

                          │  153 embeddings   │# Desde raíz del proyecto   - Esperar a que termine el build (~2 minutos)- **API**: Ver `backend/README.md`

                          │  IVFFlat indices  │

                          └───────────────────┘python -m http.server 5500 --directory public

```

```- **Deployment**: `docs/DEPLOYMENT_GUIDE.md`

---



## 🛠️ Stack Tecnológico Completo

#### **Paso 6: Abrir Navegador**### **Configuración de Traefik (Labels en docker-compose.yml)**

### **Frontend**

- HTML5 + **Tailwind CSS v3.3** (framework CSS utility-first)```

- JavaScript Vanilla (sin frameworks, máxima compatibilidad)

- **Supabase JS Client** v2.38 (autenticación + consultas)http://localhost:5500## 🌐 Deployment

- **Nginx** como servidor web estático

- Responsive Design (320px → 4K)```



### **Backend**```yaml

- **FastAPI** 0.104 (Python 3.10) - Framework web async

- **Sentence Transformers** 2.2.2 - Modelo all-MiniLM-L6-v2---

- **PyTorch** 2.1.0 (versión CPU optimizada)

- **scikit-learn** 1.3.2 - Cálculo de similitud del cosenolabels:Sistema listo para deployment con Docker:

- **PyPDF2** 3.0.1 - Extracción de texto de PDFs

- **Supabase Python Client** - Conexión a PostgreSQL### **Opción 3: Docker (Producción Local)**



### **Base de Datos**  - traefik.enable=true```bash

- **Supabase Cloud** (PostgreSQL 15.1)

- **pgvector** v0.8.0 - Extensión para vectores```bash

- **IVFFlat indices** - Búsqueda rápida

- 153 embeddings almacenados (~229 KB)# Desde raíz del proyecto  - traefik.docker.network=dokploy-networkdocker-compose up -d



### **Infraestructura**docker compose up -d --build

- **Docker** 24.0 + **Docker Compose** v2

- **Dokploy** - CI/CD automático desde GitHub  - traefik.http.routers.recuiva-backend-websecure.rule=Host(`api-recuiva.duckdns.org`)```

- **Traefik** v3.5 - Reverse Proxy + SSL automático

- **DigitalOcean Droplet** (Ubuntu 22.04 LTS, 2GB RAM)# Verificar estado

- **DuckDNS** - DNS dinámico gratuito

- **Let's Encrypt** - Certificados SSL (válidos hasta 19/01/2026)docker compose ps  - traefik.http.routers.recuiva-backend-websecure.entrypoints=websecure



---



## 🚀 Instalación y Uso# Ver logs  - traefik.http.routers.recuiva-backend-websecure.tls.certresolver=letsencrypt---



### **Opción 1: Usar en Producción (Recomendado)**docker compose logs -f



Simplemente abre:  - traefik.http.services.recuiva-backend.loadbalancer.server.port=8001

```

https://recuiva.duckdns.org# Acceder a la aplicación

```

# Frontend: http://localhost```**Última actualización**: Octubre 2025

O desde redes restrictivas:

```# Backend:  http://localhost:8001

http://147.182.226.170

``````**Versión**: 2.0 (Limpieza y reorganización completa)



---



### **Opción 2: Desarrollo Local**------



#### **Requisitos**

- Python 3.10+

- Git## 📖 Uso de la API## 📖 Uso de la API

- 2GB RAM mínimo



#### **Instalación**

### **1. Health Check**### **Endpoints Principales**

```bash

# 1. Clonar repositorio```bash

git clone https://github.com/AbelMoyaCode/recuiva.git

cd recuivaGET /api/health#### **1. Health Check**



# 2. Instalar dependencias backend``````bash

cd backend

pip install -r requirements.txtGET /api/health



# 3. Configurar variables de entorno (.env)**Respuesta:**```

# SUPABASE_URL=https://xqicgzqgluslzleddmfv.supabase.co

# SUPABASE_KEY=tu_service_role_key```json```json

# MODEL_NAME=all-MiniLM-L6-v2

# DEFAULT_CHUNK_SIZE=500{{



# 4. Iniciar backend  "status": "healthy",  "status": "healthy",

python -m uvicorn main:app --reload --port 8001

  "timestamp": "2025-11-06T15:30:45.123456",  "timestamp": "2025-10-21T03:04:15.261906",

# 5. Iniciar frontend (otra terminal)

cd ..  "model_loaded": true,  "model_loaded": true

python -m http.server 5500 --directory public

  "model_name": "all-MiniLM-L6-v2",}

# 6. Abrir navegador

# http://localhost:5500  "embedding_dimensions": 384```

```

}

---

```#### **2. Subir Material**

## 📖 Uso de la API

```bash

### **Health Check**

```bash---POST /api/materials/upload

GET /api/health

```Content-Type: multipart/form-data



**Respuesta:**### **2. Subir Material (PDF)**

```json

{```bashfile: <archivo.pdf>

  "status": "healthy",

  "model_loaded": true,POST /api/materials/upload```

  "model_name": "all-MiniLM-L6-v2",

  "embedding_dimensions": 384Content-Type: multipart/form-data```json

}

```{



### **Validar Respuesta**file: <archivo.pdf>  "material_id": "abc123",

```bash

POST /api/validate-answer```  "filename": "capitulo1.pdf",

Content-Type: application/json

  "chunks": 153,

{

  "question_id": "q1",**Respuesta:**  "pages": 24,

  "question_text": "¿Qué es la necrosis pulpar?",

  "user_answer": "Es la muerte del tejido nervioso del diente",```json  "status": "processed"

  "material_id": "abc123"

}{}

```

  "success": true,```

---

  "material_id": "abc123xyz",

## 👤 Autor

  "filename": "Odontologia_Capitulo1.pdf",#### **3. Validar Respuesta**

**Abel Jesús Moya Acosta**

- 🎓 Estudiante de Ingeniería de Computación y Sistemas  "total_chunks": 153,```bash

- 🏫 Universidad Privada Antenor Orrego (UPAO)

- 📧 Email: abelmoya2@upao.edu.pe  "estimated_pages": 24,POST /api/validate-answer

- 💼 GitHub: [@AbelMoyaCode](https://github.com/AbelMoyaCode)

  "total_characters": 38450,Content-Type: application/json

---

  "processing_time_seconds": 12.5

## 📄 Licencia

}{

Proyecto bajo **Licencia MIT**.

```  "question_id": "q1",

---

  "user_answer": "Porque vivía en el mismo edificio..."

**Desarrollado con ❤️ por Abel Moya - Noviembre 2025**

---}

**¡Aprende más eficientemente con Recuiva!** 🚀

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
