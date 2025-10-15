# 🚀 RECUIVA - Inicio Rápido

## ✅ Requisitos Previos

- Python 3.10 o superior
- Git (opcional, para clonar)

---

## 📦 Instalación (Primera vez)

### 1. Clonar el repositorio (si aplica)
```bash
git clone <url-del-repo>
cd recuiva
```

### 2. Crear y activar entorno virtual
```powershell
# Crear venv
python -m venv venv

# Activar venv
.\venv\Scripts\activate
```

### 3. Instalar dependencias
```powershell
pip install -r backend\requirements.txt
```

---

## 🎯 Ejecutar el Proyecto

### **Opción 1: Doble clic en archivo .bat** (MÁS FÁCIL)

1. Haz doble clic en `INICIAR_RECUIVA.bat`
2. Se abrirán automáticamente:
   - Backend (puerto 8000)
   - Frontend (puerto 5500)
   - Navegador con la aplicación

### **Opción 2: Script PowerShell**

```powershell
.\INICIAR_RECUIVA.ps1
```

### **Opción 3: Manual (2 terminales)**

**Terminal 1 - Backend:**
```powershell
cd c:\Users\Abel\Desktop\recuiva
.\venv\Scripts\activate
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Users\Abel\Desktop\recuiva\public
python -m http.server 5500
```

---

## 🌐 URLs de Acceso

- **Frontend**: http://localhost:5500/index.html
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 🛑 Detener el Proyecto

Cierra las ventanas de los servidores o presiona `Ctrl+C` en las terminales.

---

## 📁 Estructura del Proyecto

```
recuiva/
├── venv/                    # Entorno virtual (ÚNICO)
├── backend/
│   ├── main.py             # API FastAPI
│   ├── chunking.py         # Procesamiento de PDFs
│   └── requirements.txt    # Dependencias
├── public/
│   ├── index.html          # Página principal
│   └── app/                # Páginas de la aplicación
├── data/
│   ├── materials/          # PDFs subidos
│   ├── embeddings/         # Vectores generados
│   └── materials_index.json  # Índice de materiales
├── INICIAR_RECUIVA.bat     # Script de inicio (Windows)
└── INICIAR_RECUIVA.ps1     # Script de inicio (PowerShell)
```

---

## 🔧 Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'fastapi'"

**Solución:**
```powershell
.\venv\Scripts\activate
pip install -r backend\requirements.txt
```

### Error: "Puerto 8000 ya está en uso"

**Solución:**
```powershell
# Buscar proceso usando el puerto
netstat -ano | findstr :8000

# Matar el proceso (reemplaza <PID> con el número que aparece)
taskkill /PID <PID> /F
```

---

## 📚 Documentación Completa

- [README Completo](README_COMPLETO.md)
- [Documentación API](docs/api-migration.md)
- [Guía de Deployment](docs/DEPLOYMENT_GUIDE.md)

---

**Autor:** Abel Jesús Moya Acosta  
**Fecha:** Octubre 2025
