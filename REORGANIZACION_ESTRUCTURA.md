# 🗂️ Plan de Reorganización de Estructura - Recuiva

**Fecha:** 3 de noviembre de 2025  
**Autor:** Abel Jesús Moya Acosta  
**Objetivo:** Organizar el proyecto según estándares profesionales

---

## 📋 **RESUMEN EJECUTIVO**

### **Problemas actuales:**
- ❌ Archivos duplicados en `public/` y raíz (`assets/`)
- ❌ HTML duplicado: `src/pages/sesion-practica.html` y `public/app/sesion-practica.html`
- ❌ No hay separación clara entre frontend y backend
- ❌ JavaScript sin organizar por módulos
- ❌ No hay CSS personalizado (solo Tailwind inline)

### **Solución propuesta:**
- ✅ Crear carpeta `frontend/` separada
- ✅ Organizar JS en `core/`, `features/`, `mocks/`
- ✅ Eliminar duplicados
- ✅ Estructura escalable y convencional

---

## 🗃️ **ESTRUCTURA ACTUAL (PROBLEMÁTICA)**

```
recuiva/
├── public/                    # Frontend mezclado
│   ├── index.html
│   ├── dashboard.html         # ¿Duplicado?
│   ├── landing-page.html      # ¿Duplicado de index?
│   ├── app/
│   │   ├── dashboard.html     # ¿Duplicado?
│   │   ├── sesion-practica.html
│   │   └── ...
│   ├── assets/
│   │   └── js/
│   │       ├── api.js
│   │       └── ...
│   └── components/
│
├── src/                       # ❌ ¿Por qué existe?
│   └── pages/
│       └── sesion-practica.html  # ❌ DUPLICADO
│
├── assets/                    # ❌ DUPLICADOS
│   └── js/
│       ├── api.js            # ❌ Duplicado de public/assets/js/api.js
│       ├── mockApi.js        # ❌ Duplicado
│       └── ...
│
├── backend/                   # Backend mezclado con frontend
│   ├── main.py
│   └── ...
│
└── ...
```

---

## ✅ **ESTRUCTURA PROPUESTA (PROFESIONAL)**

```
recuiva/
│
├── backend/                          # 🐍 Backend FastAPI
│   ├── main.py                      # Servidor principal
│   ├── semantic_validator.py        # ✅ Validador semántico (nuevo)
│   ├── embeddings_module.py         # Generación de embeddings
│   ├── chunking.py                  # Procesamiento de PDFs
│   ├── requirements.txt
│   ├── .env
│   └── __pycache__/
│
├── frontend/                         # 🎨 Frontend completo
│   │
│   ├── public/                      # Páginas HTML
│   │   ├── index.html              # 🏠 Landing principal
│   │   │
│   │   ├── app/                    # 📱 Aplicación autenticada
│   │   │   ├── dashboard.html      # Dashboard principal
│   │   │   ├── sesion-practica.html # ⭐ CORE - Active Recall
│   │   │   ├── materiales.html     # Gestión de materiales
│   │   │   ├── subir-material.html # Upload de PDFs
│   │   │   ├── repasos.html        # Repetición espaciada
│   │   │   ├── evolucion.html      # Analytics del usuario
│   │   │   ├── mi-perfil.html      # Perfil del usuario
│   │   │   └── analytics.html      # Analytics generales
│   │   │
│   │   ├── auth/                   # 🔐 Autenticación
│   │   │   ├── login.html          # Login
│   │   │   └── register.html       # Registro (crear)
│   │   │
│   │   └── info/                   # ℹ️ Páginas informativas
│   │       ├── active-recall.html
│   │       ├── validacion-semantica.html
│   │       └── diferencias.html
│   │
│   ├── assets/                      # 🎨 Recursos estáticos
│   │   │
│   │   ├── js/                     # JavaScript organizado
│   │   │   │
│   │   │   ├── core/               # Módulos core (reutilizables)
│   │   │   │   ├── api.js          # ✅ Cliente HTTP (con JSDoc)
│   │   │   │   ├── auth.js         # Gestión de autenticación
│   │   │   │   ├── storage.js      # Helper para localStorage
│   │   │   │   └── config.js       # Configuración global
│   │   │   │
│   │   │   ├── features/           # Funcionalidades específicas
│   │   │   │   ├── upload-material.js
│   │   │   │   ├── validate-answer.js
│   │   │   │   ├── spaced-repetition.js
│   │   │   │   ├── repetition-data.js
│   │   │   │   └── analytics.js
│   │   │   │
│   │   │   ├── mocks/              # Datos mock para desarrollo
│   │   │   │   └── mockApi.js
│   │   │   │
│   │   │   └── utils/              # Utilidades
│   │   │       ├── formatters.js   # Formateo de datos
│   │   │       └── validators.js   # Validaciones frontend
│   │   │
│   │   ├── css/                    # CSS personalizado
│   │   │   ├── main.css            # Estilos globales
│   │   │   ├── components.css      # Estilos de componentes
│   │   │   ├── utilities.css       # Clases utilitarias
│   │   │   └── variables.css       # Variables CSS
│   │   │
│   │   └── img/                    # Imágenes
│   │       ├── Icon-Recuiva.ico
│   │       ├── logo.svg
│   │       └── ...
│   │
│   └── components/                  # Componentes HTML reutilizables
│       ├── header.html             # Header común
│       ├── footer.html             # Footer común
│       ├── profile.html            # Componente de perfil
│       └── backup-manager.html     # Manager de backups
│
├── data/                            # 📊 Datos persistentes
│   ├── materials/                  # PDFs originales
│   ├── embeddings/                 # Vectores JSON
│   ├── materials_index.json        # Índice de materiales
│   └── questions_storage.json      # Preguntas guardadas
│
├── docs/                            # 📚 Documentación
│   ├── ALGORITMO_VALIDACION_SEMANTICA.md  # ✅ Algoritmo documentado
│   ├── ANALISIS_SISTEMA_USUARIOS.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── DEPLOYMENT_GUIDE_DIGITALOCEAN.md
│   └── README_COMPLETO.md
│
├── scripts/                         # 🛠️ Scripts de utilidad
│   ├── setup-server.sh             # Setup de servidor
│   ├── diagnostico-scores.js       # Diagnóstico de scores
│   └── completar_tareas.ps1
│
├── docker-compose.yml               # 🐳 Orquestación de contenedores
├── Dockerfile                       # Dockerfile del backend
├── Dockerfile.frontend              # Dockerfile del frontend
├── nginx.conf                       # Configuración de Nginx
├── README.md                        # Documentación principal
├── TESTING_GUIDE.md                 # ✅ Guía de pruebas
└── REORGANIZACION_ESTRUCTURA.md     # Este documento
```

---

## 📦 **INVENTARIO COMPLETO DE ARCHIVOS**

### **HTML (20 archivos)**

#### **Páginas principales (3)**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/index.html` | `frontend/public/index.html` | Mover |
| `public/landing-page.html` | ❌ Eliminar (duplicado) | Eliminar |
| `public/dashboard.html` | ❌ Eliminar (duplicado) | Eliminar |

#### **Aplicación (9)**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/app/dashboard.html` | `frontend/public/app/dashboard.html` | Mover |
| `public/app/sesion-practica.html` | `frontend/public/app/sesion-practica.html` | Mover |
| `public/app/materiales.html` | `frontend/public/app/materiales.html` | Mover |
| `public/app/subir-material.html` | `frontend/public/app/subir-material.html` | Mover |
| `public/app/repasos.html` | `frontend/public/app/repasos.html` | Mover |
| `public/app/evolucion.html` | `frontend/public/app/evolucion.html` | Mover |
| `public/app/mi-perfil.html` | `frontend/public/app/mi-perfil.html` | Mover |
| `public/app/analytics.html` | `frontend/public/app/analytics.html` | Mover |
| `public/app/dashboard_BASE.html` | ❌ Eliminar (backup antiguo) | Eliminar |

#### **Autenticación (1)**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/app/auth/iniciar-sesion.html` | `frontend/public/auth/login.html` | Mover y renombrar |

#### **Informativas (3)**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/app/institucional/active-recall.html` | `frontend/public/info/active-recall.html` | Mover |
| `public/app/institucional/validacion-semantica.html` | `frontend/public/info/validacion-semantica.html` | Mover |
| `public/app/institucional/diferencias.html` | `frontend/public/info/diferencias.html` | Mover |

#### **Componentes (3)**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/components/_header-template.html` | `frontend/components/header.html` | Mover y renombrar |
| `public/components/local-profile.html` | `frontend/components/profile.html` | Mover y renombrar |
| `public/components/backup-manager.html` | `frontend/components/backup-manager.html` | Mover |

#### **Duplicados a eliminar**
| Archivo | Razón |
|---------|-------|
| `src/pages/sesion-practica.html` | Duplicado de `public/app/sesion-practica.html` |

---

### **JavaScript (11 archivos únicos)**

#### **Core (API y utilidades)**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/assets/js/api.js` | `frontend/assets/js/core/api.js` | Mover |
| `assets/js/api.js` | ❌ Eliminar (duplicado) | Eliminar |

#### **Features (funcionalidades específicas)**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/assets/js/upload-material.js` | `frontend/assets/js/features/upload-material.js` | Mover |
| `public/assets/js/validate-answer.js` | `frontend/assets/js/features/validate-answer.js` | Mover |
| `public/assets/js/validate-answer-real.js` | `frontend/assets/js/features/validate-answer-real.js` | Mover |
| `public/app/spaced-repetition.js` | `frontend/assets/js/features/spaced-repetition.js` | Mover |
| `public/app/repetition-data.js` | `frontend/assets/js/features/repetition-data.js` | Mover |

#### **Mocks**
| Archivo actual | Nueva ubicación | Acción |
|---------------|-----------------|--------|
| `public/assets/js/mockApi.js` | `frontend/assets/js/mocks/mockApi.js` | Mover |
| `assets/js/mockApi.js` | ❌ Eliminar (duplicado) | Eliminar |

#### **Duplicados a eliminar**
| Archivo | Razón |
|---------|-------|
| `assets/js/upload-material.js` | Duplicado de `public/assets/js/upload-material.js` |
| `assets/js/validate-answer.js` | Duplicado de `public/assets/js/validate-answer.js` |

---

### **CSS (crear nuevos archivos)**

Actualmente NO hay CSS personalizado, solo Tailwind CDN. Propongo crear:

| Nuevo archivo | Propósito |
|--------------|-----------|
| `frontend/assets/css/main.css` | Estilos globales base |
| `frontend/assets/css/variables.css` | Variables CSS (colores, espaciado) |
| `frontend/assets/css/components.css` | Estilos de componentes reutilizables |
| `frontend/assets/css/utilities.css` | Clases utilitarias personalizadas |

---

## 🔄 **COMANDOS DE MIGRACIÓN (PowerShell)**

```powershell
# ===== 1. MOVER HTML PRINCIPALES =====

# Index (único landing)
Move-Item "public\index.html" "frontend\public\index.html"

# Aplicación
Move-Item "public\app\dashboard.html" "frontend\public\app\dashboard.html"
Move-Item "public\app\sesion-practica.html" "frontend\public\app\sesion-practica.html"
Move-Item "public\app\materiales.html" "frontend\public\app\materiales.html"
Move-Item "public\app\subir-material.html" "frontend\public\app\subir-material.html"
Move-Item "public\app\repasos.html" "frontend\public\app\repasos.html"
Move-Item "public\app\evolucion.html" "frontend\public\app\evolucion.html"
Move-Item "public\app\mi-perfil.html" "frontend\public\app\mi-perfil.html"
Move-Item "public\app\analytics.html" "frontend\public\app\analytics.html"

# Autenticación
Move-Item "public\app\auth\iniciar-sesion.html" "frontend\public\auth\login.html"

# Informativas
Move-Item "public\app\institucional\active-recall.html" "frontend\public\info\active-recall.html"
Move-Item "public\app\institucional\validacion-semantica.html" "frontend\public\info\validacion-semantica.html"
Move-Item "public\app\institucional\diferencias.html" "frontend\public\info\diferencias.html"

# Componentes
Move-Item "public\components\_header-template.html" "frontend\components\header.html"
Move-Item "public\components\local-profile.html" "frontend\components\profile.html"
Move-Item "public\components\backup-manager.html" "frontend\components\backup-manager.html"

# ===== 2. MOVER JAVASCRIPT =====

# Core
Move-Item "public\assets\js\api.js" "frontend\assets\js\core\api.js"

# Features
Move-Item "public\assets\js\upload-material.js" "frontend\assets\js\features\upload-material.js"
Move-Item "public\assets\js\validate-answer.js" "frontend\assets\js\features\validate-answer.js"
Move-Item "public\assets\js\validate-answer-real.js" "frontend\assets\js\features\validate-answer-real.js"
Move-Item "public\app\spaced-repetition.js" "frontend\assets\js\features\spaced-repetition.js"
Move-Item "public\app\repetition-data.js" "frontend\assets\js\features\repetition-data.js"

# Mocks
Move-Item "public\assets\js\mockApi.js" "frontend\assets\js\mocks\mockApi.js"

# ===== 3. MOVER IMÁGENES =====

# Copiar todas las imágenes
Copy-Item "public\assets\img\*" "frontend\assets\img\" -Recurse

# ===== 4. ELIMINAR DUPLICADOS =====

# Eliminar carpeta duplicada de assets en raíz
Remove-Item "assets" -Recurse -Force

# Eliminar carpeta src temporal
Remove-Item "src" -Recurse -Force

# Eliminar duplicados en public
Remove-Item "public\landing-page.html" -Force
Remove-Item "public\dashboard.html" -Force
Remove-Item "public\app\dashboard_BASE.html" -Force

# ===== 5. LIMPIAR CARPETAS VACÍAS =====

# Eliminar carpeta public antigua (ya movimos todo)
Remove-Item "public" -Recurse -Force
```

---

## ⚠️ **ADVERTENCIAS Y CONSIDERACIONES**

### **1. Actualizar rutas en HTML**

Después de mover archivos, **DEBES actualizar las rutas** en:

#### **Ejemplo: `frontend/public/app/dashboard.html`**

**Antes:**
```html
<script src="../assets/js/api.js"></script>
<link rel="icon" href="../assets/img/Icon-Recuiva.ico"/>
```

**Después:**
```html
<script src="../../assets/js/core/api.js"></script>
<link rel="icon" href="../../assets/img/Icon-Recuiva.ico"/>
```

### **2. Actualizar Nginx**

**Archivo:** `nginx.conf`

**Antes:**
```nginx
root /usr/share/nginx/html/public;
```

**Después:**
```nginx
root /usr/share/nginx/html/frontend/public;
```

### **3. Actualizar Dockerfile.frontend**

**Antes:**
```dockerfile
COPY public /usr/share/nginx/html/public
```

**Después:**
```dockerfile
COPY frontend/public /usr/share/nginx/html/frontend/public
COPY frontend/assets /usr/share/nginx/html/frontend/assets
COPY frontend/components /usr/share/nginx/html/frontend/components
```

---

## ✅ **CHECKLIST DE MIGRACIÓN**

- [ ] Crear estructura de carpetas `frontend/`
- [ ] Mover archivos HTML a nuevas ubicaciones
- [ ] Mover archivos JS a `core/`, `features/`, `mocks/`
- [ ] Mover imágenes a `frontend/assets/img/`
- [ ] Crear archivos CSS base
- [ ] Eliminar duplicados (`assets/`, `src/`)
- [ ] Actualizar rutas en todos los HTML
- [ ] Actualizar `nginx.conf`
- [ ] Actualizar `Dockerfile.frontend`
- [ ] Actualizar `docker-compose.yml` si es necesario
- [ ] Probar localmente
- [ ] Hacer commit
- [ ] Deploy a producción

---

## 🚀 **BENEFICIOS DE LA NUEVA ESTRUCTURA**

### **1. Separación de Responsabilidades**
- ✅ Frontend y backend claramente separados
- ✅ Fácil de entender para nuevos desarrolladores

### **2. Escalabilidad**
- ✅ Fácil agregar nuevas features en `features/`
- ✅ Fácil agregar nuevos módulos core en `core/`

### **3. Mantenibilidad**
- ✅ Sin duplicados (código DRY)
- ✅ Organización por tipo de archivo

### **4. Profesionalismo**
- ✅ Estructura estándar de la industria
- ✅ Fácil de presentar en portfolio

---

## 📝 **PRÓXIMOS PASOS**

### **Fase 1: Reorganización (1-2 horas)**
1. Ejecutar comandos de migración
2. Actualizar rutas en HTML
3. Probar localmente

### **Fase 2: CSS Personalizado (1 hora)**
1. Crear archivos CSS base
2. Extraer estilos inline a CSS
3. Definir variables CSS

### **Fase 3: Modularización JS (2 horas)**
1. Crear `auth.js`, `storage.js`, `config.js`
2. Refactorizar código duplicado
3. Agregar más JSDoc

### **Fase 4: Deploy (30 min)**
1. Actualizar Docker
2. Push a Dokploy
3. Verificar en producción

---

**¿Ejecutamos la migración ahora?** 🚀
