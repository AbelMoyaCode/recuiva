# 🚀 Guía de Inicio Local - Recuiva

## 📋 Análisis del Proyecto Actual

### ✅ **Archivos correctos (ya usando Supabase)**
- ✅ `public/app/auth/crear-cuenta.html` - Usa Supabase
- ✅ `public/app/auth/iniciar-sesion.html` - Usa Supabase  
- ✅ `public/assets/js/supabase-config.js` - Configuración Supabase

### ⚠️ **Archivos que AÚN usan mockApi.js (necesitan actualización)**
- ❌ `public/index.html` - Landing page
- ❌ `public/landing-page.html` - Landing page backup
- ❌ `public/app/dashboard.html` - Dashboard principal
- ❌ `public/app/materiales.html` - Gestión de materiales

### 📦 **Archivos JavaScript en el proyecto**
1. `public/assets/js/supabase-config.js` - ✅ **USAR ESTE** (Supabase)
2. `public/assets/js/mockApi.js` - ⚠️ **MANTENER** (dashboard aún lo usa)
3. `public/assets/js/api.js` - Para llamadas al backend
4. `public/assets/js/validate-answer.js` - Validación de respuestas
5. `public/assets/js/upload-material.js` - Subir materiales

---

## 🔧 Pasos para Iniciar Localmente

### **1️⃣ Preparar el entorno**

#### A. Verificar Python
```powershell
python --version  # Debe ser Python 3.8+
```

#### B. Activar entorno virtual
```powershell
cd C:\Users\Abel\Desktop\recuiva
.\venv\Scripts\Activate.ps1
```

#### C. Instalar dependencias del backend
```powershell
pip install -r requirements.txt
```

---

### **2️⃣ Iniciar el Backend (FastAPI)**

```powershell
# Desde la carpeta raíz del proyecto
cd C:\Users\Abel\Desktop\recuiva

# Activar venv
.\venv\Scripts\Activate.ps1

# Iniciar servidor
python backend/main.py
```

**El backend estará disponible en:**
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

---

### **3️⃣ Iniciar el Frontend (servidor estático)**

**Opción A: Python HTTP Server (RECOMENDADO)**
```powershell
# En otra terminal PowerShell
cd C:\Users\Abel\Desktop\recuiva\public
python -m http.server 3000
```

**Opción B: Live Server (VS Code)**
1. Instala extensión "Live Server" en VS Code
2. Click derecho en `public/index.html`
3. "Open with Live Server"

**El frontend estará disponible en:**
- Landing: `http://localhost:3000/`
- Dashboard: `http://localhost:3000/app/dashboard.html`
- Crear cuenta: `http://localhost:3000/app/auth/crear-cuenta.html`

---

## ✅ Probar el Sistema

### **Paso 1: Crear una cuenta**
1. Ve a `http://localhost:3000/app/auth/crear-cuenta.html`
2. Ingresa:
   - Nombre: `Juan Pérez`
   - Email: `juanperez44@gmail.com`
   - Contraseña: `12345678`
3. Clic en "Crear cuenta"
4. Verifica en **Supabase Dashboard > Authentication > Users**

### **Paso 2: Iniciar sesión**
1. Ve a `http://localhost:3000/app/auth/iniciar-sesion.html`
2. Ingresa las credenciales del Paso 1
3. Deberías ser redirigido a `/app/dashboard.html`

### **Paso 3: Verificar redirección automática**
1. Ve a `http://localhost:3000/` (landing page)
2. Si ya estás logueado → Redirige a dashboard
3. Si NO estás logueado → Muestra landing page

---

## 🐛 Problemas Comunes

### **Error: "Cannot read properties of undefined (reading 'split')"**
**Causa:** Página intentando usar `mockAPI` cuando no está cargado.  
**Solución:** Ya corregido en crear-cuenta.html e iniciar-sesion.html. Dashboard aún usa mockAPI (es normal).

### **Error: "ModuleNotFoundError: No module named 'sentence_transformers'"**
**Causa:** Falta instalar dependencias del backend.  
**Solución:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

### **Error: "Supabase client not defined"**
**Causa:** No se cargó `supabase-config.js`.  
**Solución:** Verificar que el HTML tenga:
```html
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="../../assets/js/supabase-config.js"></script>
```

### **Puerto 3000 o 8000 ya en uso**
**Solución:**
```powershell
# Ver qué proceso usa el puerto
netstat -ano | findstr :3000

# Matar el proceso (reemplaza PID)
taskkill /PID <número> /F

# O usa otro puerto
python -m http.server 3001
```

---

## 📊 Estado Actual del Proyecto

| Componente | Estado | Notas |
|-----------|--------|-------|
| **Supabase Auth** | ✅ Funcionando | Crear cuenta e iniciar sesión |
| **Landing Page** | ⚠️ Usa mockAPI | Necesita migrar a Supabase |
| **Dashboard** | ⚠️ Usa mockAPI | Necesita migrar a Supabase |
| **Backend FastAPI** | ✅ Funcionando | Puerto 8000 |
| **Validación Semántica** | ✅ Funcionando | Con embeddings |
| **Materiales** | ⚠️ Usa mockAPI | Necesita migrar a Supabase |

---

## 🎯 Próximos Pasos

### **Fase 1: Migrar Dashboard a Supabase** (PRIORITARIO)
1. Actualizar `dashboard.html` para usar `supabase-config.js`
2. Quitar `mockApi.js` del dashboard
3. Conectar con tabla `materials` en Supabase

### **Fase 2: Migrar Landing Page**
1. Actualizar `index.html` para usar Supabase
2. Quitar `mockApi.js` del landing

### **Fase 3: Backend Multi-Usuario**
1. Actualizar `backend/main.py` para recibir `user_id`
2. Modificar endpoints para filtrar por usuario
3. Guardar embeddings en carpetas por usuario

### **Fase 4: Deploy a Producción**
1. Configurar variables de entorno en Dokploy
2. Subir código actualizado
3. Verificar en `recuiva.duckdns.org`

---

## 📝 Comandos Rápidos

```powershell
# Iniciar todo el sistema (2 terminales)

# Terminal 1 - Backend
cd C:\Users\Abel\Desktop\recuiva
.\venv\Scripts\Activate.ps1
python backend/main.py

# Terminal 2 - Frontend
cd C:\Users\Abel\Desktop\recuiva\public
python -m http.server 3000
```

---

## ✅ Checklist de Verificación

- [ ] Backend FastAPI corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 3000
- [ ] Puedo acceder a la landing page
- [ ] Puedo crear una cuenta nueva
- [ ] Puedo iniciar sesión
- [ ] El usuario aparece en Supabase Dashboard
- [ ] La redirección automática funciona
- [ ] Puedo acceder al dashboard después de login

---

**¡Listo!** Ahora tienes todo configurado para trabajar localmente. 🚀
