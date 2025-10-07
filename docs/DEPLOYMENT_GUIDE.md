# Guía de Deployment - Recuiva en DigitalOcean + Dokploy

## 📋 Prerrequisitos

- ✅ GitHub Student Pack aprobado
- ✅ Cuenta de DigitalOcean vinculada
- ✅ Repositorio GitHub: AbelMoyaICSI/Recuiva
- ✅ SSH configurado en tu máquina local

---

## 🚀 Paso 1: Crear Droplet en DigitalOcean

### 1.1 Acceder a DigitalOcean
```bash
# Ir a: https://cloud.digitalocean.com
# Login con cuenta vinculada a GitHub Student Pack
```

### 1.2 Crear Droplet
1. Click en **"Create" → "Droplets"**
2. **Región:** Frankfurt, Amsterdam o Nueva York (más cercana)
3. **Imagen:** Ubuntu 22.04 LTS x64
4. **Plan:**
   - **Basic:** $6/mes
   - **Regular CPU**
   - **1 GB RAM / 1 vCPU / 25 GB SSD**
5. **Autenticación:** SSH Key (recomendado) o Password
6. **Hostname:** `recuiva-production`
7. Click **"Create Droplet"**

### 1.3 Esperar creación (1-2 minutos)
- Copiar IP pública del Droplet

---

## 🔐 Paso 2: Conectar por SSH

### 2.1 Conectar al servidor
```bash
# Reemplazar YOUR_DROPLET_IP con la IP del Droplet
ssh root@YOUR_DROPLET_IP
```

### 2.2 Actualizar sistema
```bash
apt update && apt upgrade -y
```

---

## 🐳 Paso 3: Instalar Docker

### 3.1 Instalar Docker Engine
```bash
# Instalar dependencias
apt install -y apt-transport-https ca-certificates curl software-properties-common

# Agregar GPG key de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Agregar repositorio Docker
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io

# Verificar instalación
docker --version
```

### 3.2 Instalar Docker Compose
```bash
# Descargar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Dar permisos de ejecución
chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker-compose --version
```

### 3.3 Habilitar Docker al inicio
```bash
systemctl enable docker
systemctl start docker
```

---

## 🎯 Paso 4: Instalar Dokploy

### 4.1 Ejecutar instalador de Dokploy
```bash
curl -sSL https://dokploy.com/install.sh | sh
```

### 4.2 Esperar instalación (5-10 minutos)
- Dokploy se instalará automáticamente
- Al finalizar, verás la URL de acceso

### 4.3 Acceder a Dokploy UI
```bash
# Abrir en navegador:
http://YOUR_DROPLET_IP:3000
```

### 4.4 Configurar Dokploy
1. Crear cuenta de administrador
2. Usuario: `abel` o `admin`
3. Email: `amoya2@upao.edu.pe`
4. Contraseña segura (guardar en 1Password/Bitwarden)

---

## 📦 Paso 5: Conectar GitHub

### 5.1 En Dokploy UI
1. **Settings** → **Git Providers**
2. Click **"Add GitHub Provider"**
3. **Authorize GitHub App**
4. Seleccionar repositorio: `AbelMoyaICSI/Recuiva`

### 5.2 Crear aplicación
1. **Applications** → **Create Application**
2. **Name:** `recuiva-production`
3. **Repository:** Seleccionar `Recuiva`
4. **Branch:** `main`
5. **Build Method:** Docker Compose

---

## 🏗️ Paso 6: Configurar Deployment

### 6.1 Variables de entorno (opcional)
```env
PYTHONUNBUFFERED=1
TRANSFORMERS_CACHE=/app/.cache
NODE_ENV=production
```

### 6.2 Build Configuration
- **Dockerfile path:** `./Dockerfile`
- **Docker Compose path:** `./docker-compose.yml`
- **Port:** 80 (frontend), 8000 (backend)

### 6.3 Deployment Settings
- **Auto Deploy:** ✅ Enabled
- **Deploy on push:** ✅ Enabled (rama `main`)

---

## 🚀 Paso 7: Primer Deployment

### 7.1 Deploy manual
1. En Dokploy: Click **"Deploy Now"**
2. Ver logs en tiempo real
3. Esperar build (5-10 minutos primera vez)

### 7.2 Verificar deployment
```bash
# En el servidor, verificar contenedores
docker ps

# Deberías ver:
# - recuiva-frontend (nginx)
# - recuiva-backend (python)
```

### 7.3 Acceder a la aplicación
```bash
# Abrir en navegador:
http://YOUR_DROPLET_IP
```

---

## 🌐 Paso 8: Configurar Dominio (Opcional)

### 8.1 Opción A - Usar DuckDNS (Gratis)
```bash
# Ir a: https://www.duckdns.org
# Login con GitHub
# Crear subdominio: recuiva.duckdns.org
# Copiar token
```

### 8.2 Configurar DuckDNS en Droplet
```bash
# Crear script de actualización
mkdir -p /root/duckdns
cd /root/duckdns

# Crear script (reemplazar TOKEN y SUBDOMAIN)
echo "echo url=\"https://www.duckdns.org/update?domains=SUBDOMAIN&token=TOKEN&ip=\" | curl -k -o /root/duckdns/duck.log -K -" > duck.sh

chmod 700 duck.sh

# Agregar a crontab (actualizar cada 5 min)
crontab -e
# Agregar línea:
*/5 * * * * /root/duckdns/duck.sh >/dev/null 2>&1
```

### 8.3 Opción B - Usar dominio propio
1. Comprar dominio en Namecheap (gratis con Student Pack)
2. Configurar DNS A record: `@` → `YOUR_DROPLET_IP`
3. Esperar propagación DNS (5-30 minutos)

---

## 🔒 Paso 9: Configurar SSL (HTTPS)

### 9.1 Instalar Certbot
```bash
apt install -y certbot python3-certbot-nginx
```

### 9.2 Obtener certificado SSL
```bash
# Reemplazar tu-dominio.com con tu dominio real
certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

### 9.3 Auto-renovación
```bash
# Certbot ya configura auto-renovación
# Verificar:
certbot renew --dry-run
```

---

## 🔥 Paso 10: Configurar Firewall

### 10.1 Habilitar UFW
```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3000/tcp  # Dokploy UI
ufw enable
```

### 10.2 Verificar status
```bash
ufw status
```

---

## 📊 Monitoreo y Logs

### Ver logs de contenedores
```bash
# Frontend
docker logs recuiva-frontend -f

# Backend
docker logs recuiva-backend -f

# Todos
docker-compose logs -f
```

### Reiniciar servicios
```bash
cd /ruta/al/proyecto
docker-compose restart
```

### Actualizar código
```bash
# Desde Dokploy UI: Click "Deploy Now"
# O manualmente:
git pull origin main
docker-compose down
docker-compose up -d --build
```

---

## 🎯 Checklist Post-Deployment

- [ ] Aplicación accesible en http://YOUR_DROPLET_IP
- [ ] Frontend carga correctamente
- [ ] Backend responde (si está activo)
- [ ] Logs sin errores críticos
- [ ] Auto-deploy configurado
- [ ] Firewall activo
- [ ] SSL configurado (si usas dominio)
- [ ] Monitoreo configurado en Dokploy
- [ ] Backup configurado (opcional)
- [ ] Documentación actualizada

---

## 🆘 Troubleshooting

### Problema: Contenedor no inicia
```bash
# Ver logs detallados
docker logs recuiva-backend

# Verificar configuración
docker-compose config

# Reconstruir imagen
docker-compose build --no-cache
docker-compose up -d
```

### Problema: Puerto 80 en uso
```bash
# Ver qué usa el puerto
lsof -i :80

# Detener servicio conflictivo
systemctl stop apache2  # Si hay Apache
```

### Problema: Sin espacio en disco
```bash
# Limpiar imágenes y contenedores antiguos
docker system prune -a --volumes

# Ver uso de disco
df -h
```

---

## 📚 Recursos Adicionales

- **Dokploy Docs:** https://docs.dokploy.com
- **DigitalOcean Docs:** https://docs.digitalocean.com
- **Docker Compose Docs:** https://docs.docker.com/compose
- **Certbot Docs:** https://certbot.eff.org

---

## ✅ Siguiente Fase

Una vez completado este deployment:

1. **Sprint Review:** Mostrar aplicación desplegada al profesor
2. **Integrar API:** Convertir mockApi.js en API real
3. **Conectar Supabase:** Base de datos PostgreSQL
4. **CI/CD:** Automatizar tests antes de deploy
5. **Monitoreo:** Configurar alertas de uptime

---

**¡Deployment exitoso!** 🚀

Tu aplicación ahora está en producción en DigitalOcean con Dokploy, tal como lo requiere el profesor.
