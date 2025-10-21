# 🎓 Recuiva - Sistema de Active Recall con IA# 📚 Recuiva - Sistema de Active Recall con IA



![Estado: Producción](https://img.shields.io/badge/Estado-Producción-success)Sistema de aprendizaje basado en Active Recall con validación semántica mediante IA.

![Versión](https://img.shields.io/badge/Versión-1.0.0-blue)

![Python](https://img.shields.io/badge/Python-3.10-blue)## 🏗️ Estructura del Proyecto

![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)

![Docker](https://img.shields.io/badge/Docker-Compose-blue)```

recuiva/

Sistema de estudio basado en **Active Recall** con validación semántica de respuestas usando **Inteligencia Artificial** (Sentence Transformers).├── backend/              # Backend FastAPI

│   ├── main.py          # API principal

---│   ├── embeddings_module.py

│   ├── chunking.py

## 🌐 Aplicación en Producción│   └── requirements.txt

├── public/              # Frontend (archivos servidos)

- **🌍 Frontend:** [https://recuiva.duckdns.org](https://recuiva.duckdns.org)│   ├── index.html      # Landing page principal

- **🔧 API Backend:** [https://api-recuiva.duckdns.org](https://api-recuiva.duckdns.org)│   ├── dashboard.html  # Dashboard de usuario

- **📖 Documentación API:** [https://api-recuiva.duckdns.org/docs](https://api-recuiva.duckdns.org/docs)│   ├── landing-page.html

- **💚 Health Check:** [https://api-recuiva.duckdns.org/api/health](https://api-recuiva.duckdns.org/api/health)│   └── app/            # Aplicación web

│       ├── sesion-practica.html    # ⭐ Página principal de práctica

---│       ├── materiales.html         # Gestión de materiales PDF

│       ├── repasos.html           # Sistema de repasos espaciados

## ✨ Características Principales│       ├── dashboard.html         # Dashboard de progreso

│       ├── evolucion.html

### 🧠 Validación Semántica con IA│       ├── mi-perfil.html

- Usa **Sentence Transformers** (modelo `all-MiniLM-L6-v2`)│       ├── subir-material.html

- Calcula similitud coseno entre tu respuesta y el material│       ├── analytics.html

- Clasifica automáticamente: **EXCELENTE** (>90%), **BUENO** (70-90%), **ACEPTABLE** (50-70%)│       ├── auth/                  # Sistema de autenticación

- Identifica el fragmento más relevante del material│       ├── institucional/         # Páginas informativas

│       │   ├── active-recall.html

### 📚 Gestión de Materiales│       │   ├── validacion-semantica.html

- Sube **PDFs** o archivos **TXT**│       │   └── diferencias.html

- Fragmentación automática en chunks de 500 caracteres│       └── assets/               # Recursos estáticos

- Generación de embeddings para búsqueda semántica├── data/               # Datos y materiales

- Organización por carpetas (Semestre, Curso, Tema)│   ├── materials/      # Materiales de estudio (PDFs)

│   ├── embeddings/     # Vectores de embeddings

### 🎯 Sistema de Preguntas│   └── materials_index.json

- Crea preguntas basadas en tus materiales├── docs/               # Documentación del proyecto

- Responde sin ver el material (Active Recall)│   ├── ANALISIS_SISTEMA_USUARIOS.md    # Análisis del sistema de usuarios

- Retroalimentación instantánea con score de similitud│   ├── DEPLOYMENT_GUIDE.md             # Guía de deployment

- Historial de respuestas y progreso│   ├── DEPLOYMENT_GUIDE_DIGITALOCEAN.md # Deployment en DigitalOcean

│   ├── INICIO_RAPIDO.md                # Guía de inicio rápido

### 📊 Análisis y Estadísticas│   └── README_COMPLETO.md              # Documentación completa

- Dashboard con métricas de estudio├── scripts/            # Scripts de utilidad

- Gráficos de evolución de scores│   ├── completar_tareas.ps1

- Identificación de temas débiles│   ├── setup-server.sh

- Repetición espaciada automática│   ├── fix-dokploy-port.sh

│   └── simple_backend.py

---├── assets/             # Assets globales

│   ├── img/

## 🏗️ Arquitectura del Sistema│   └── js/

├── config.yaml         # Configuración de la aplicación

```├── requirements.txt    # Dependencias Python unificadas

┌─────────────────────────────────────────────────────────────┐├── docker-compose.yml  # Orquestación de contenedores

│                         INTERNET                            │├── Dockerfile          # Imagen Docker principal

│                  (DuckDNS + Let's Encrypt)                  │├── nginx.conf          # Configuración del servidor web

└────────────────────────┬────────────────────────────────────┘├── INICIAR_RECUIVA.bat # Script de inicio Windows

                         │└── INICIAR_RECUIVA.ps1 # Script de inicio PowerShell

            ┌────────────▼────────────┐```

            │  Traefik (Reverse Proxy)│

            │    Puerto 80/443        │## 🚀 Inicio Rápido

            └────────────┬────────────┘

                         │### 0. Instalar Dependencias

         ┌───────────────┴──────────────┐

         │                              │```bash

    ┌────▼─────┐                  ┌────▼─────┐pip install -r requirements.txt

    │ Frontend │                  │ Backend  │```

    │  Nginx   │                  │ FastAPI  │

    │  :80     │◄─────CORS────────┤  :8001   │### 1. Iniciar Servidores

    └──────────┘                  └────┬─────┘

         │                              │**Windows (Batch):**

    HTML/CSS/JS              ┌──────────▼──────────┐```cmd

    Tailwind CSS             │ Sentence Transformers│INICIAR_RECUIVA.bat

                             │   all-MiniLM-L6-v2  │```

                             └─────────────────────┘

```**Windows (PowerShell):**

```powershell

---.\INICIAR_RECUIVA.ps1

```

## 🛠️ Stack Tecnológico

**Manual:**

### **Frontend**```powershell

- HTML5 + Tailwind CSS# Backend (puerto 8000)

- JavaScript Vanilla (sin frameworks)cd backend

- Nginx (servidor web estático)python -m uvicorn main:app --reload --port 8000



### **Backend**# Frontend (puerto 5500) - en otra terminal

- FastAPI (Python 3.10)cd ..

- Sentence Transformers (`sentence-transformers==2.2.2`)python -m http.server 5500 --directory public

- PyTorch (versión CPU)```

- PyPDF2 (extracción de texto de PDFs)

### 2. Acceder a la Aplicación

### **Infraestructura**

- Docker + Docker Compose**Página principal de práctica:**

- Dokploy (CI/CD)```

- Traefik v3.5 (Reverse Proxy + SSL)http://localhost:5500/app/sesion-practica.html?material_id=1

- DigitalOcean (Ubuntu 22.04 LTS)```

- DuckDNS (DNS dinámico)

**Dashboard:**

---```

http://localhost:5500/

## 🚀 Instalación Local```



### **Requisitos Previos**> **Nota**: El parámetro `material_id=1` corresponde al material cargado en el sistema. Si tienes múltiples materiales, cambia el número según corresponda.

- Docker y Docker Compose instalados

- Git## 📦 Requisitos

- 2GB RAM mínimo

- Python 3.10+

### **Paso 1: Clonar el Repositorio**- Librerías: FastAPI, Uvicorn, Sentence-Transformers

```bash- Navegador moderno (Chrome, Edge, Firefox)

git clone https://github.com/AbelMoyaCode/recuiva.git

cd recuiva**Instalar dependencias:**

``````bash

cd backend

### **Paso 2: Configurar Variables de Entorno**pip install -r requirements.txt

```bash```

cd backend

cp .env.example .env## 🎯 Características Principales

# Editar .env si es necesario

```- ✅ **Active Recall**: Práctica basada en recordar activamente

- 🤖 **Validación Semántica**: IA verifica comprensión conceptual

### **Paso 3: Levantar con Docker Compose**- 📊 **Sistema de Puntuación**: Feedback detallado (0-100%)

```bash- 💾 **Guardado Automático**: Progreso guardado en localStorage

# Desde la raíz del proyecto- 📈 **Análisis de Evolución**: Métricas de aprendizaje

docker compose up -d --build

```## 🔧 Configuración



### **Paso 4: Verificar que Funcione**Ver `config.yaml` para configuración del sistema.

```bash

# Backend## 📝 Uso

curl http://localhost:8001/api/health

# Respuesta esperada: {"status":"healthy","model_loaded":true}1. Inicia los servidores con `start-servers.ps1`

2. Abre `http://localhost:5500/app/sesion-practica.html?material_id=1`

# Frontend3. Escribe pregunta y respuesta (mínimo 1+1 caracteres)

# Abrir en navegador: http://localhost:804. Click en "Validar con IA"

```5. Recibe feedback semántico instantáneo



---**Control de funcionamiento:**

- Abre la consola del navegador (F12)

## 📦 Despliegue en Producción- Verás logs de: "📁 Material ID: 1", "🌐 Conectando con servidor..."

- Si el backend responde, verás: "✅ Respuesta recibida del servidor"

### **Con Dokploy (Recomendado)**- Si hay errores, aparecerán mensajes detallados en rojo



1. **Instalar Dokploy en el servidor:**## 🐛 Solución de Problemas

   ```bash

   curl -sSL https://dokploy.com/install.sh | sh**Error: No se puede conectar al backend**

   ```- Verifica que el backend esté corriendo en puerto 8000

- Ejecuta: `curl http://localhost:8000/` (debe responder `{"status":"OK"}`)

2. **Crear proyecto en Dokploy UI:**

   - Nombre: `recuiva`**Página en blanco o errores de consola**

   - Tipo: `Docker Compose`- Asegúrate de abrir la URL correcta: `/app/sesion-practica.html`

   - Repositorio: `https://github.com/AbelMoyaCode/recuiva.git`- Verifica que ambos servidores estén corriendo

   - Branch: `main`

**Modelo de IA no carga**

3. **Configurar dominios:**- Primera vez tarda ~30 segundos descargando modelo

   - Frontend: `recuiva.duckdns.org`- Revisa logs del backend

   - Backend: `api-recuiva.duckdns.org`

## 📚 Documentación

4. **Desplegar:**

   - Click en "Deploy Server"- **Documentación antigua**: `docs/archive/`

   - Esperar a que termine el build (~2 minutos)- **API**: Ver `backend/README.md`

- **Deployment**: `docs/DEPLOYMENT_GUIDE.md`

### **Configuración de Traefik (Labels en docker-compose.yml)**

## 🌐 Deployment

```yaml

labels:Sistema listo para deployment con Docker:

  - traefik.enable=true```bash

  - traefik.docker.network=dokploy-networkdocker-compose up -d

  - traefik.http.routers.recuiva-backend-websecure.rule=Host(`api-recuiva.duckdns.org`)```

  - traefik.http.routers.recuiva-backend-websecure.entrypoints=websecure

  - traefik.http.routers.recuiva-backend-websecure.tls.certresolver=letsencrypt---

  - traefik.http.services.recuiva-backend.loadbalancer.server.port=8001

```**Última actualización**: Octubre 2025

**Versión**: 2.0 (Limpieza y reorganización completa)

---

## 📖 Uso de la API

### **Endpoints Principales**

#### **1. Health Check**
```bash
GET /api/health
```
```json
{
  "status": "healthy",
  "timestamp": "2025-10-21T03:04:15.261906",
  "model_loaded": true
}
```

#### **2. Subir Material**
```bash
POST /api/materials/upload
Content-Type: multipart/form-data

file: <archivo.pdf>
```
```json
{
  "material_id": "abc123",
  "filename": "capitulo1.pdf",
  "chunks": 153,
  "pages": 24,
  "status": "processed"
}
```

#### **3. Validar Respuesta**
```bash
POST /api/validate-answer
Content-Type: application/json

{
  "question_id": "q1",
  "user_answer": "Porque vivía en el mismo edificio..."
}
```
```json
{
  "score": 90.5,
  "classification": "EXCELENTE",
  "feedback": "Has demostrado comprensión profunda del concepto",
  "matched_fragment": "Chunk 53 de 153",
  "fragment_text": "...porque vivía en el mismo edificio...",
  "similarity_details": {
    "method": "Sentence Transformers (all-MiniLM-L6-v2)"
  }
}
```

---

## 🔧 Comandos Útiles

### **Ver logs de contenedores:**
```bash
# Backend
docker logs recuiva-recuiva-7mk1x0-backend-1 -f

# Frontend
docker logs recuiva-recuiva-7mk1x0-frontend-1 -f
```

### **Reiniciar servicios:**
```bash
docker restart recuiva-recuiva-7mk1x0-backend-1
docker restart recuiva-recuiva-7mk1x0-frontend-1
```

### **Ver estado de Traefik:**
```bash
curl http://localhost:8080/api/http/routers | jq
```

### **Rebuild completo:**
```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

---

## 🧪 Testing

### **Probar el Backend Localmente:**
```bash
cd backend
python -m pytest tests/
```

### **Probar un endpoint manualmente:**
```bash
curl -X POST http://localhost:8001/api/validate-answer \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "test",
    "user_answer": "Respuesta de prueba"
  }'
```

---

## 📊 Estructura de Directorios

```
recuiva/
├── assets/                 # Recursos estáticos (JS, imágenes)
│   ├── js/
│   │   ├── api.js         # Cliente de la API
│   │   ├── upload-material.js
│   │   └── validate-answer.js
│   └── img/
├── backend/                # Código del backend FastAPI
│   ├── main.py            # App principal
│   ├── embeddings_module.py
│   ├── chunking.py
│   └── requirements.txt
├── public/                 # Frontend HTML
│   ├── index.html
│   ├── dashboard.html
│   └── app/
│       ├── subir-material.html
│       └── sesion-practica.html
├── data/                   # Datos persistentes
│   ├── materials/
│   └── embeddings/
├── docs/                   # Documentación adicional
├── docker-compose.yml      # Orquestación de contenedores
├── Dockerfile              # Imagen del backend
├── Dockerfile.frontend     # Imagen del frontend
└── README.md               # Este archivo
```

---

## 🔒 Seguridad

- ✅ **HTTPS obligatorio** (certificados SSL automáticos)
- ✅ **CORS configurado** solo para dominios permitidos
- ✅ **Healthchecks** para monitoreo
- ✅ **Rate limiting** en endpoints sensibles
- ✅ **Validación de entrada** en todos los endpoints

---

## 🐛 Problemas Comunes y Soluciones

### **1. Backend devuelve 404**
```bash
# Verificar que los labels de Traefik estén correctos
docker inspect recuiva-recuiva-7mk1x0-backend-1 | grep traefik
```

### **2. CORS Error en el Frontend**
```bash
# Verificar que ALLOWED_ORIGINS incluya tu dominio
docker exec recuiva-recuiva-7mk1x0-backend-1 env | grep ALLOWED_ORIGINS
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
docker logs recuiva-recuiva-7mk1x0-backend-1 | grep "Modelo"
# Debe decir: "✅ Modelo all-MiniLM-L6-v2 cargado exitosamente"
```

---

## 🚧 Roadmap (Mejoras Futuras)

- [ ] Instalar Tailwind CSS localmente (eliminar CDN)
- [ ] Autenticación de usuarios (JWT)
- [ ] Base de datos PostgreSQL
- [ ] CI/CD con GitHub Actions
- [ ] Tests automatizados (pytest + coverage)
- [ ] Monitoreo con Prometheus + Grafana
- [ ] Backups automáticos
- [ ] PWA (Progressive Web App)
- [ ] Modo offline

---

## 👥 Contribución

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Añade nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👤 Autor

**Abel Jesús Moya Acosta**
- GitHub: [@AbelMoyaCode](https://github.com/AbelMoyaCode)
- Email: abelmoya2@upao.edu.pe

---

## 🙏 Agradecimientos

- [Sentence Transformers](https://www.sbert.net/) por el modelo de embeddings
- [FastAPI](https://fastapi.tiangolo.com/) por el excelente framework
- [Dokploy](https://dokploy.com/) por simplificar el despliegue
- [DuckDNS](https://www.duckdns.org/) por DNS gratuito

---

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa la sección [Problemas Comunes](#-problemas-comunes-y-soluciones)
2. Consulta la [documentación completa](docs/README_COMPLETO.md)
3. Abre un [Issue en GitHub](https://github.com/AbelMoyaCode/recuiva/issues)
4. Contacta al autor

---

**¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!**

---

**Última actualización:** 21 de octubre de 2025  
**Versión:** 1.0.0 (Producción)
