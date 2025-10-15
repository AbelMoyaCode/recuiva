# 📚 Recuiva - Sistema de Active Recall con IA

Sistema de aprendizaje basado en Active Recall con validación semántica mediante IA.

## 🏗️ Estructura del Proyecto

```
recuiva/
├── backend/              # Backend FastAPI
│   ├── main.py          # API principal
│   ├── embeddings_module.py
│   ├── chunking.py
│   └── requirements.txt
├── public/              # Frontend (archivos servidos)
│   ├── index.html      # Landing page principal
│   ├── dashboard.html  # Dashboard de usuario
│   ├── landing-page.html
│   └── app/            # Aplicación web
│       ├── sesion-practica.html    # ⭐ Página principal de práctica
│       ├── materiales.html         # Gestión de materiales PDF
│       ├── repasos.html           # Sistema de repasos espaciados
│       ├── dashboard.html         # Dashboard de progreso
│       ├── evolucion.html
│       ├── mi-perfil.html
│       ├── subir-material.html
│       ├── analytics.html
│       ├── auth/                  # Sistema de autenticación
│       ├── institucional/         # Páginas informativas
│       │   ├── active-recall.html
│       │   ├── validacion-semantica.html
│       │   └── diferencias.html
│       └── assets/               # Recursos estáticos
├── data/               # Datos y materiales
│   ├── materials/      # Materiales de estudio (PDFs)
│   ├── embeddings/     # Vectores de embeddings
│   └── materials_index.json
├── docs/               # Documentación del proyecto
│   ├── ANALISIS_SISTEMA_USUARIOS.md    # Análisis del sistema de usuarios
│   ├── DEPLOYMENT_GUIDE.md             # Guía de deployment
│   ├── DEPLOYMENT_GUIDE_DIGITALOCEAN.md # Deployment en DigitalOcean
│   ├── INICIO_RAPIDO.md                # Guía de inicio rápido
│   └── README_COMPLETO.md              # Documentación completa
├── scripts/            # Scripts de utilidad
│   ├── completar_tareas.ps1
│   ├── setup-server.sh
│   ├── fix-dokploy-port.sh
│   └── simple_backend.py
├── assets/             # Assets globales
│   ├── img/
│   └── js/
├── config.yaml         # Configuración de la aplicación
├── docker-compose.yml  # Orquestación de contenedores
├── Dockerfile          # Imagen Docker principal
├── nginx.conf          # Configuración del servidor web
├── INICIAR_RECUIVA.bat # Script de inicio Windows
└── INICIAR_RECUIVA.ps1 # Script de inicio PowerShell
```

## 🚀 Inicio Rápido

### 1. Iniciar Servidores

**Windows (Batch):**
```cmd
INICIAR_RECUIVA.bat
```

**Windows (PowerShell):**
```powershell
.\INICIAR_RECUIVA.ps1
```

**Manual:**
```powershell
# Backend (puerto 8000)
cd backend
python -m uvicorn main:app --reload --port 8000

# Frontend (puerto 5500) - en otra terminal
cd ..
python -m http.server 5500 --directory public
```

### 2. Acceder a la Aplicación

**Página principal de práctica:**
```
http://localhost:5500/app/sesion-practica.html?material_id=1
```

**Dashboard:**
```
http://localhost:5500/
```

> **Nota**: El parámetro `material_id=1` corresponde al material cargado en el sistema. Si tienes múltiples materiales, cambia el número según corresponda.

## 📦 Requisitos

- Python 3.10+
- Librerías: FastAPI, Uvicorn, Sentence-Transformers
- Navegador moderno (Chrome, Edge, Firefox)

**Instalar dependencias:**
```bash
cd backend
pip install -r requirements.txt
```

## 🎯 Características Principales

- ✅ **Active Recall**: Práctica basada en recordar activamente
- 🤖 **Validación Semántica**: IA verifica comprensión conceptual
- 📊 **Sistema de Puntuación**: Feedback detallado (0-100%)
- 💾 **Guardado Automático**: Progreso guardado en localStorage
- 📈 **Análisis de Evolución**: Métricas de aprendizaje

## 🔧 Configuración

Ver `config.yaml` para configuración del sistema.

## 📝 Uso

1. Inicia los servidores con `start-servers.ps1`
2. Abre `http://localhost:5500/app/sesion-practica.html?material_id=1`
3. Escribe pregunta y respuesta (mínimo 1+1 caracteres)
4. Click en "Validar con IA"
5. Recibe feedback semántico instantáneo

**Control de funcionamiento:**
- Abre la consola del navegador (F12)
- Verás logs de: "📁 Material ID: 1", "🌐 Conectando con servidor..."
- Si el backend responde, verás: "✅ Respuesta recibida del servidor"
- Si hay errores, aparecerán mensajes detallados en rojo

## 🐛 Solución de Problemas

**Error: No se puede conectar al backend**
- Verifica que el backend esté corriendo en puerto 8000
- Ejecuta: `curl http://localhost:8000/` (debe responder `{"status":"OK"}`)

**Página en blanco o errores de consola**
- Asegúrate de abrir la URL correcta: `/app/sesion-practica.html`
- Verifica que ambos servidores estén corriendo

**Modelo de IA no carga**
- Primera vez tarda ~30 segundos descargando modelo
- Revisa logs del backend

## 📚 Documentación

- **Documentación antigua**: `docs/archive/`
- **API**: Ver `backend/README.md`
- **Deployment**: `docs/DEPLOYMENT_GUIDE.md`

## 🌐 Deployment

Sistema listo para deployment con Docker:
```bash
docker-compose up -d
```

---

**Última actualización**: Octubre 2025
**Versión**: 2.0 (Limpieza y reorganización completa)
