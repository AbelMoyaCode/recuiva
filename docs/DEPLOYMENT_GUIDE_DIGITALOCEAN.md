# 🚀 Guía de Despliegue - Recuiva en DigitalOcean

**Proyecto:** Recuiva - Sistema de Active Recall con IA  
**Servidor:** DigitalOcean Droplet + Dokploy  
**Fecha:** 7 de octubre de 2025

---

## 📋 Requisitos previos

- ✅ Droplet creado en DigitalOcean (Ubuntu 22.04)
- ✅ IP pública del Droplet
- ✅ Contraseña root configurada
- ✅ Repositorio en GitHub: https://github.com/AbelMoyaCode/recuiva
- ✅ Créditos del GitHub Student Pack activos

---

## 🎯 Paso 1: Conectar al servidor

### Opción A: Usar el script automático
```powershell
.\connect-server.ps1
```

### Opción B: Conectar manualmente
```powershell
ssh root@TU_IP_PUBLICA
```

Ingresa la contraseña que configuraste.

---

## 🔧 Paso 2: Configurar el servidor

Una vez conectado por SSH, ejecuta estos comandos:

### Método automático (Recomendado)
```bash
# Descargar el script de instalación
curl -o setup.sh https://raw.githubusercontent.com/AbelMoyaCode/recuiva/main/setup-server.sh

# Dar permisos de ejecución
chmod +x setup.sh

# Ejecutar
./setup.sh
```

### Método manual
```bash
# 1. Actualizar sistema
apt update && apt upgrade -y

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Instalar Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 4. Verificar instalaciones
docker --version
docker-compose --version

# 5. Instalar Dokploy
curl -sSL https://dokploy.com/install.sh | sh
```

**⏱️ Tiempo estimado:** 10-15 minutos

---

## 🌐 Paso 3: Configurar Dokploy

### 1. Acceder al panel
Abre en tu navegador:
```
http://TU_IP_PUBLICA:3000
```

### 2. Crear cuenta admin
- **Usuario:** abel
- **Email:** amoyaa2@upao.edu.pe
- **Contraseña:** (elige una segura)

### 3. Conectar GitHub
- Ve a **Settings** → **Git Providers**
- Click en **Add GitHub Provider**
- Autoriza el acceso
- Selecciona el repositorio: `AbelMoyaCode/recuiva`

---

## 🚀 Paso 4: Crear aplicación en Dokploy

### 1. Nueva aplicación
- Click en **Applications** → **Create Application**
- **Name:** recuiva-production
- **Repository:** AbelMoyaCode/recuiva
- **Branch:** main

### 2. Configurar build
- **Build Method:** Docker Compose
- **Docker Compose Path:** docker-compose.yml
- **Environment Variables:** (opcional, agregar si necesitas)

### 3. Desplegar
- Click en **Deploy Now**
- Espera 10-15 minutos (primera vez)
- Monitorea los logs en tiempo real

---

## ✅ Paso 5: Verificar despliegue

### 1. Verificar servicios
```bash
docker ps
```

Deberías ver 2 contenedores corriendo:
- `recuiva-backend`
- `recuiva-frontend`

### 2. Verificar logs
```bash
# Backend
docker logs recuiva-backend -f

# Frontend
docker logs recuiva-frontend -f
```

### 3. Probar la aplicación
Abre en tu navegador:
```
http://TU_IP_PUBLICA
```

Deberías ver tu aplicación Recuiva funcionando.

---

## 🔍 Troubleshooting

### Problema: No puedo conectar por SSH
**Solución:**
```powershell
# Verifica que OpenSSH esté instalado
ssh -V

# Si no está, instálalo:
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
```

### Problema: Error al instalar Docker
**Solución:**
```bash
# Limpia instalaciones anteriores
apt remove docker docker-engine docker.io containerd runc
apt autoremove

# Vuelve a intentar
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Problema: Dokploy no carga
**Solución:**
```bash
# Verifica el estado del servicio
systemctl status dokploy

# Reinicia si es necesario
systemctl restart dokploy
```

### Problema: El despliegue falla
**Solución:**
```bash
# Verifica los logs de Docker
docker logs recuiva-backend
docker logs recuiva-frontend

# Verifica el docker-compose
cd /ruta/al/proyecto
docker-compose config
```

---

## 📊 Configuración adicional (Opcional)

### 1. Configurar dominio personalizado
En Dokploy:
- **Settings** → **Domains**
- Agregar dominio: `recuiva.tudominio.com`
- Configurar DNS apuntando a la IP del Droplet

### 2. Habilitar HTTPS/SSL
En Dokploy:
- **Settings** → **SSL**
- Habilitar **Let's Encrypt**
- Dokploy configura automáticamente el certificado

### 3. Configurar variables de entorno
```bash
# Backend
PORT=8000
MODEL_NAME=all-MiniLM-L6-v2
EMBEDDINGS_DIR=/app/data/embeddings
```

---

## 🎯 Checklist de despliegue

- [ ] Droplet creado en DigitalOcean
- [ ] Conexión SSH exitosa
- [ ] Docker instalado
- [ ] Docker Compose instalado
- [ ] Dokploy instalado y accesible
- [ ] GitHub conectado en Dokploy
- [ ] Aplicación creada en Dokploy
- [ ] Primer despliegue exitoso
- [ ] Aplicación accesible desde el navegador
- [ ] Backend API funcionando (http://IP:8000/docs)
- [ ] Frontend funcionando (http://IP)

---

## 📝 Comandos útiles

```bash
# Ver contenedores corriendo
docker ps

# Ver logs en tiempo real
docker logs -f recuiva-backend

# Reiniciar contenedor
docker restart recuiva-backend

# Detener todos los contenedores
docker-compose down

# Iniciar todos los contenedores
docker-compose up -d

# Ver uso de recursos
docker stats

# Limpiar imágenes antiguas
docker system prune -a
```

---

## 🔐 Seguridad

### 1. Configurar firewall
```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 3000/tcp
ufw enable
```

### 2. Cambiar puerto SSH (Opcional)
```bash
nano /etc/ssh/sshd_config
# Cambiar Port 22 a Port 2222
systemctl restart sshd
```

### 3. Deshabilitar login root (Recomendado)
```bash
# Crear usuario nuevo
adduser abel
usermod -aG sudo abel

# Deshabilitar root login
nano /etc/ssh/sshd_config
# PermitRootLogin no
systemctl restart sshd
```

---

## 📈 Monitoreo

### CPU y memoria
```bash
htop
```

### Espacio en disco
```bash
df -h
```

### Logs del sistema
```bash
journalctl -xe
```

---

## 🆘 Soporte

- **Documentación Dokploy:** https://dokploy.com/docs
- **Documentación Docker:** https://docs.docker.com
- **DigitalOcean Community:** https://www.digitalocean.com/community

---

**✅ ¡Listo! Tu aplicación Recuiva estará desplegada y funcionando en internet.**

**🌐 URLs importantes:**
- Aplicación: `http://TU_IP`
- Backend API: `http://TU_IP:8000`
- Swagger Docs: `http://TU_IP:8000/docs`
- Dokploy Panel: `http://TU_IP:3000`

---

**Desarrollado por:** Abel Jesús Moya Acosta  
**Universidad:** UPAO  
**Proyecto:** Recuiva - Sistema de Active Recall con IA
