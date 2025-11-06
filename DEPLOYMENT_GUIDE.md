# 🚀 Guía de Despliegue - Recuiva en Dokploy

## 📋 Pre-requisitos

- ✅ Servidor DigitalOcean con Ubuntu 22.04
- ✅ Dokploy instalado
- ✅ Dominios DuckDNS configurados:
  - `recuiva.duckdns.org` → Frontend
  - `api-recuiva.duckdns.org` → Backend

## 🔧 Archivos de Configuración

### 1. Estructura del Proyecto

```
recuiva/
├── Dockerfile              # Backend (FastAPI + PyTorch)
├── Dockerfile.frontend     # Frontend (Nginx)
├── docker-compose.yml      # Orquestación completa
├── nginx.conf              # Configuración de Nginx
├── .dockerignore           # Archivos excluidos del build
├── config.yaml             # Configuración general
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
└── public/
    ├── index.html
    ├── app/
    └── assets/
```

### 2. Variables de Entorno en Dokploy

Configurar en `Environment Settings`:

```bash
# Servidor
HOST=0.0.0.0
PORT=8001
DEBUG=False

# CORS (CRÍTICO: usar DuckDNS, NO traefik.me)
ALLOWED_ORIGINS=http://localhost:3000,https://recuiva.duckdns.org,https://api-recuiva.duckdns.org

# Modelo de embeddings
MODEL_NAME=all-MiniLM-L6-v2

# Thresholds de validación
SIMILARITY_THRESHOLD_EXCELLENT=0.9
SIMILARITY_THRESHOLD_GOOD=0.7
SIMILARITY_THRESHOLD_ACCEPTABLE=0.5

# Chunking
DEFAULT_CHUNK_SIZE=500
DEFAULT_CHUNK_OVERLAP=50
MIN_DOCUMENT_SIZE=200000

# Logging
LOG_LEVEL=INFO

# Límites
MAX_FILE_SIZE_MB=50
MAX_CHUNKS_PER_MATERIAL=1000
```

### 3. Configuración de Dominios en Dokploy

**Backend:**
- Domain: `api-recuiva.duckdns.org`
- Path: `/`
- Port: `8001`
- HTTPS: ✅ Enabled (Let's Encrypt)

**Frontend:**
- Domain: `recuiva.duckdns.org`
- Path: `/`
- Port: `80`
- HTTPS: ✅ Enabled (Let's Encrypt)

## 🐳 Comandos de Despliegue

### Deploy desde GitHub

1. **Configurar repositorio en Dokploy:**
   - Repository: `https://github.com/AbelMoyaCode/recuiva.git`
   - Branch: `main`
   - Compose Path: `./docker-compose.yml`
   - Trigger: `On Push` (deploy automático)

2. **Build manual (si es necesario):**
   ```bash
   docker compose -p recuiva-recuiva-7mk1x0 \
     -f ./docker-compose.yml \
     up -d --build --remove-orphans
   ```

### Deploy local (testing)

```bash
# Construir imágenes
docker compose build

# Levantar servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Detener servicios
docker compose down
```

## 🔍 Verificación del Despliegue

### 1. Health Check del Backend

```bash
curl https://api-recuiva.duckdns.org/api/health
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2025-11-05T..."
}
```

### 2. Frontend

Acceder a: `https://recuiva.duckdns.org`

- ✅ Debe cargar la landing page
- ✅ Login/Registro funcional
- ✅ Dashboard accesible después de login

### 3. Integración Backend-Frontend

En el dashboard, subir un material de prueba:
- ✅ El archivo debe subirse correctamente
- ✅ Debe generarse embeddings (ver logs del backend)
- ✅ Debe aparecer en la lista de materiales

## 🐛 Solución de Problemas

### Error: "failed to solve: /src not found"

**Causa:** Dockerfile.frontend intenta copiar carpetas que no existen.

**Solución:**
```dockerfile
# ❌ ANTES (INCORRECTO)
COPY assets/ /usr/share/nginx/html/assets/
COPY src/ /usr/share/nginx/html/src/

# ✅ AHORA (CORRECTO)
COPY public/ /usr/share/nginx/html/
```

### Error: CORS al subir archivos

**Causa:** ALLOWED_ORIGINS apunta a dominios incorrectos.

**Solución en Dokploy Environment:**
```bash
ALLOWED_ORIGINS=https://recuiva.duckdns.org,https://api-recuiva.duckdns.org
```

### Error: Timeout al subir archivos grandes

**Causa:** Nginx tiene timeouts por defecto de 60s.

**Solución:** Ya configurado en `nginx.conf`:
```nginx
proxy_connect_timeout 300;
proxy_send_timeout 300;
proxy_read_timeout 300;
```

### Backend no responde

**Verificar:**
```bash
# Ver logs del backend
docker logs recuiva-recuiva-7mk1x0-backend-1

# Ver estado de contenedores
docker ps -a | grep recuiva

# Reiniciar servicio
docker compose restart backend
```

## 📊 Monitoreo

### Logs en Dokploy

Ver en la interfaz web:
- `Deployments` → `View` → Ver logs en tiempo real

### Logs manuales

```bash
# Backend
docker logs -f recuiva-recuiva-7mk1x0-backend-1

# Frontend
docker logs -f recuiva-recuiva-7mk1x0-frontend-1

# Todos
docker compose logs -f
```

### Recursos del servidor

En Dokploy dashboard:
- CPU Usage
- Memory Usage
- Disk I/O
- Bandwidth

## 🔄 Actualización del Código

### Deploy automático (On Push)

1. Hacer commit y push a `main`:
   ```bash
   git add .
   git commit -m "feat: Nueva funcionalidad"
   git push origin main
   ```

2. Dokploy detectará el push y hará deploy automáticamente.

### Deploy manual

En Dokploy:
1. Ir a `Services` → `recuiva`
2. Click en `Deploy` → `Reload`

## 🔐 Seguridad

### Firewall (DigitalOcean)

**Puertos abiertos:**
- ✅ 22 (SSH)
- ✅ 80 (HTTP)
- ✅ 443 (HTTPS)
- ❌ 3000, 8000, 8001 (cerrar en producción)

**Configuración recomendada:**
```bash
# En DigitalOcean Firewall
Inbound:
  SSH    TCP  22   All IPv4, All IPv6
  HTTP   TCP  80   All IPv4, All IPv6
  HTTPS  TCP  443  All IPv4, All IPv6
```

### HTTPS/SSL

- ✅ Let's Encrypt configurado automáticamente por Traefik
- ✅ Redirect HTTP → HTTPS habilitado
- ✅ Certificados auto-renovables

## 📝 Checklist Pre-Despliegue

- [ ] Archivos de configuración actualizados
  - [ ] `Dockerfile`
  - [ ] `Dockerfile.frontend`
  - [ ] `docker-compose.yml`
  - [ ] `nginx.conf`
  - [ ] `.dockerignore`
  
- [ ] Variables de entorno configuradas en Dokploy
  - [ ] `ALLOWED_ORIGINS` con DuckDNS
  - [ ] Resto de variables del backend
  
- [ ] Dominios configurados
  - [ ] `recuiva.duckdns.org` → Frontend
  - [ ] `api-recuiva.duckdns.org` → Backend
  
- [ ] Código commiteado y pusheado a GitHub
  ```bash
  git add .
  git commit -m "fix: Corregir rutas de Dockerfile para despliegue"
  git push origin main
  ```

- [ ] Deploy ejecutado en Dokploy

- [ ] Health check del backend exitoso

- [ ] Frontend carga correctamente

- [ ] Login/Registro funcional

- [ ] Subida de materiales funcional

## 🎉 ¡Listo!

Acceder a: **https://recuiva.duckdns.org**

---

**Última actualización:** 5 de noviembre de 2025
