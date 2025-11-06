# 🧹 Limpieza de Docker en DigitalOcean

## **Paso 1: Conectarte al servidor por SSH**

Abre una terminal (PowerShell o CMD) y ejecuta:

```bash
ssh root@147.182.226.170
```

Contraseña: (tu contraseña de root de DigitalOcean)

---

## **Paso 2: Ver espacio en disco**

```bash
df -h
```

**Buscar línea con `/dev/vda1` o similar:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        60G   58G   2G  97%  /
```

Si `Use%` está cerca del 100%, continúa limpiando.

---

## **Paso 3: Limpiar imágenes y contenedores de Docker**

### **3.1. Ver contenedores detenidos:**
```bash
docker ps -a --filter "status=exited"
```

### **3.2. Eliminar contenedores detenidos:**
```bash
docker container prune -f
```

### **3.3. Ver imágenes sin usar:**
```bash
docker images
```

### **3.4. Eliminar imágenes sin usar:**
```bash
docker image prune -a -f
```

**⚠️ ADVERTENCIA:** Esto eliminará TODAS las imágenes que no estén en uso.

### **3.5. Limpiar volúmenes:**
```bash
docker volume prune -f
```

### **3.6. Limpiar caché de build:**
```bash
docker builder prune -a -f
```

---

## **Paso 4: Verificar espacio liberado**

```bash
df -h
```

**Deberías tener al menos 10-15 GB libres** después de limpiar.

---

## **Paso 5: Reintentar deploy**

1. Ve a Dokploy: https://147.182.226.170:3000
2. Projects → recuiva → production → recuiva
3. Click en **"Deploy"** → **"Reload"**

---

## **Si sigue fallando por espacio:**

### **Opción A: Upgrade del Droplet (RECOMENDADO)**

1. Ve a DigitalOcean Dashboard
2. Click en tu droplet **"recuiva"**
3. **Resize** → Selecciona plan con más disco (ej: 80 GB o 120 GB)
4. Apply changes

### **Opción B: Reducir dependencias (AVANZADO)**

Usar versiones CPU-only de PyTorch (más ligeras):

```python
# En requirements.txt, REEMPLAZAR:
torch==2.8.0
torchvision==0.23.0

# POR:
torch==2.1.0+cpu
torchvision==0.16.0+cpu
```

**Ventaja:** Reduce tamaño de ~3 GB a ~200 MB  
**Desventaja:** Ya lo estás usando (instalas en Dockerfile con CPU)

---

## **Comandos útiles para monitoreo:**

```bash
# Ver espacio por directorio
du -sh /var/lib/docker/*

# Ver logs de Dokploy
journalctl -u dokploy -f

# Ver contenedores activos
docker ps

# Ver uso de disco detallado
df -i
```
