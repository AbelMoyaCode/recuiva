# Recuiva - Plataforma de Active Recall

Sistema de aprendizaje adaptativo basado en Active Recall que optimiza la retención de conocimiento mediante validación semántica.

## 📁 Estructura del Proyecto

```
recuiva/
├── public/                      # Páginas públicas y de inicio
│   ├── index.html              # Página de inicio principal
│   └── landing-page.html       # Landing page
│
├── src/                        # Código fuente principal
│   ├── pages/                  # Páginas de la aplicación
│   │   ├── auth/              # Autenticación
│   │   │   ├── crear-cuenta.html
│   │   │   └── iniciar-sesion.html
│   │   ├── institucional/     # Páginas institucionales
│   │   │   ├── active-recall.html
│   │   │   ├── diferencias.html
│   │   │   └── validacion-semantica.html
│   │   ├── analytics.html     # Dashboard analítico
│   │   ├── dashboard.html     # Panel principal
│   │   ├── evolucion.html     # Evolución del estudiante
│   │   ├── materiales.html    # Gestión de materiales
│   │   ├── mi-perfil.html     # Perfil de usuario
│   │   ├── repasos.html       # Sistema de repasos
│   │   ├── sesion-practica.html  # Sesiones de práctica
│   │   └── subir-material.html   # Subir contenido
│   │
│   ├── components/            # Componentes reutilizables
│   │   └── _header-template.html
│   │
│   └── styles/                # Estilos CSS (futuro)
│
├── backend/                   # Scripts Python y API
│   ├── embeddings_gui.py     # GUI para embeddings
│   ├── embeddings_local.py   # Procesamiento local
│   ├── launcher.py           # Lanzador de servicios
│   ├── debug_score.py        # Debug de scoring
│   ├── test_debug.py         # Tests de debug
│   ├── sample_active_recall.txt
│   └── README.md             # Documentación del backend
│
├── assets/                    # Recursos estáticos
│   ├── img/                  # Imágenes e iconos
│   │   ├── Icon-Recuiva.ico
│   │   ├── Icon-Recuiva.png
│   │   └── icon-recuiva.svg
│   └── js/                   # JavaScript
│       └── mockApi.js        # API simulada
│
├── data/                     # Datos y datasets
│   └── mock-dataset.json    # Dataset de prueba
│
└── docs/                     # Documentación
    ├── api-migration.md      # Guía de migración de API
    └── frontend-best-practices.md

```

## 🚀 Características Principales

- ✅ **Validación semántica** con embeddings
- ✅ **Algoritmo de intervalos espaciados**
- ✅ **Análisis de comprensión no literal**
- ✅ **Dashboard analítico de progreso**
- ✅ **Gestión de materiales educativos**

## 🛠️ Tecnologías

### Frontend
- HTML5, CSS3 (Tailwind CSS)
- JavaScript vanilla
- Arquitectura de componentes

### Backend
- Python 3.10+
- sentence-transformers (embeddings)
- PyPDF2 (procesamiento de PDFs)
- NumPy (cálculos matemáticos)

## 📦 Instalación

### Backend (Python)
```bash
cd backend
pip install sentence-transformers PyPDF2 numpy
```

### Frontend
```bash
# Abrir en navegador o servidor local
cd public
python -m http.server 8000
```

## 🎯 Uso

### Interfaz Gráfica de Embeddings
```bash
cd backend
python launcher.py
# Seleccionar opción 2 para GUI
```

### Desarrollo Web
1. Abre `public/index.html` en tu navegador
2. Navega a la aplicación desde el menú principal
3. Registra una cuenta o inicia sesión

## 📊 Roadmap

- [ ] Migrar de mock API a backend real
- [ ] Implementar base de datos (Supabase)
- [ ] Despliegue en producción (DigitalOcean + Dokploy)
- [ ] Sistema de embeddings en tiempo real
- [ ] Análisis avanzado con LangChain

## 👥 Autor

**Abel Jesús Moya Acosta**
- Proyecto: Taller Integrador I - UPAO
- Email: amoya2@upao.edu.pe

## 📄 Licencia

Proyecto académico - Universidad Privada Antenor Orrego (UPAO)

---

**Última actualización:** Octubre 2025
