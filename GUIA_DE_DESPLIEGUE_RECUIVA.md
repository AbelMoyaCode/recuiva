# MANUAL DE DESPLIEGUE - RECUIVA

**Proyecto:** Recuiva - Plataforma de Estudio con IA  
**Responsable:** Abel Moya Acosta  
**Fecha:** 06/12/2025  
**Versión:** 1.0  

---

## 1. INTRODUCCIÓN

Este documento describe el procedimiento paso a paso para el despliegue de la aplicación web **Recuiva** en un entorno de producción utilizando **DigitalOcean** como proveedor de infraestructura, **Dokploy** como gestor de despliegue (PaaS auto-hospedado) y **DuckDNS** para la gestión de dominios dinámicos.

### Arquitectura de Despliegue
*   **Infraestructura:** VPS (Droplet) Ubuntu 22.04 LTS en Digital Ocean.
*   **Orquestación:** Docker Compose gestionado por Dokploy.
*   **Base de Datos:** Supabase Cloud (PostgreSQL + pgvector).
*   **Proxy Inverso:** Traefik (incluido en Dokploy) para gestión de SSL/HTTPS.
*   **Dominios:** `recuiva.duckdns.org` (Frontend) y `api-recuiva.duckdns.org` (Backend).

---

## 2. REQUISITOS PREVIOS

Antes de iniciar, se debe contar con:
1.  **Cuenta en GitHub** con acceso al repositorio **AbelMoyaCode/recuiva**.
2.  **Servidor VPS (DigitalOcean)** activo con Dokploy instalado y accesible vía IP.
3.  **Dominios DuckDNS** creados y apuntando a la IP del servidor.
4.  **Credenciales de Supabase** (URL y Keys) para las variables de entorno.

`[ESPACIO PARA CAPTURA DE PANTALLA: PANEL DE DIGITALOCEAN CON EL DROPLET ACTIVO]`

---

## 3. PASO 1: PREPARACIÓN DEL REPOSITORIO (GITHUB)

El código fuente debe estar actualizado en la rama `main` del repositorio. Se debe verificar que existan los archivos de configuración Docker:
*   `Dockerfile` (Backend)
*   `Dockerfile.frontend` (Frontend)
*   `docker-compose.yml` (Orquestación)

`[ESPACIO PARA CAPTURA DE PANTALLA: VISTA DEL REPOSITORIO EN GITHUB]`

---

## 4. PASO 2: CONFIGURACIÓN EN DOKPLOY

### 2.1. Conexión del Servicio Backend
1.  Ingresar al panel de **Dokploy**.
2.  Crear un nuevo **Proyecto** llamado `Recuiva`.
3.  Seleccionar **"Compose"** (Docker Compose) como método de despliegue.
4.  Conectar con el repositorio de GitHub y seleccionar la rama `main`.

`[ESPACIO PARA CAPTURA DE PANTALLA: DOKPLOY - SELECCIÓN DE REPOSITORIO]`

### 2.2. Configuración de Variables de Entorno
En la pestaña **"Environment"**, se deben ingresar las credenciales críticas. Copiar y pegar las siguientes claves:

```bash
# Servidor & Cors
HOST=0.0.0.0
PORT=8001
ALLOWED_ORIGINS=https://recuiva.duckdns.org,https://api-recuiva.duckdns.org

# Inteligencia Artificial & Embeddings
MODEL_NAME=all-MiniLM-L6-v2
GROQ_API_KEY=********

# Base de Datos (Supabase)
SUPABASE_URL=********
SUPABASE_KEY=********
DB_CONNECTION_STRING=postgresql://postgres:pass@db.supabase.co:5432/postgres
```

`[ESPACIO PARA CAPTURA DE PANTALLA: DOKPLOY - CONFIGURACIÓN DE VARIABLES DE ENTORNO]`

---

## 5. PASO 3: CONFIGURACIÓN DE DOMINIOS Y SSL

Para que la aplicación sea accesible públicamente con HTTPS:

1.  En la pestaña **"Domains"** de Dokploy.
2.  Agregar el dominio del Frontend: `recuiva.duckdns.org`.
    *   Puerto: `80`
    *   HTTPS: Activado (Let's Encrypt).
3.  Agregar el dominio del Backend: `api-recuiva.duckdns.org`.
    *   Puerto: `8001`
    *   HTTPS: Activado.

`[ESPACIO PARA CAPTURA DE PANTALLA: DOKPLOY - CONFIGURACIÓN DE DOMINIOS]`

---

## 6. PASO 4: EJECUCIÓN DEL DESPLIEGUE

1.  Ir a la pestaña **"Deployments"**.
2.  Hacer clic en el botón **"Deploy"**.
3.  Observar los **Logs** de construcción. El sistema descargará las imágenes, instalará dependencias de Python y React, y construirá los contenedores.

**Estado Esperado:** `Status: Running` o `Build Successful`.

`[ESPACIO PARA CAPTURA DE PANTALLA: LOGS DE DESPLIEGUE EXITOSO]`

---

## 7. VERIFICACIÓN FINAL

### 7.1. Verificación del Backend (API)
Navegar a `https://api-recuiva.duckdns.org/docs` (Swagger) o `/api/health`.
*   **Resultado esperado:** JSON con estado "healthy".

`[ESPACIO PARA CAPTURA DE PANTALLA: RESPUESTA DE LA API / SWAGGER]`

### 7.2. Verificación del Frontend (App Web)
Navegar a `https://recuiva.duckdns.org`.
*   **Resultado esperado:** Carga de la Landing Page o pantalla de Login sin errores de consola.

`[ESPACIO PARA CAPTURA DE PANTALLA: APLICACIÓN CORRIENDO EN EL NAVEGADOR]`

---

## 8. SOLUCIÓN DE PROBLEMAS COMUNES

| Problema | Causa Probable | Solución |
| :--- | :--- | :--- |
| **Error 502 Bad Gateway** | El contenedor no ha iniciado o el puerto es incorrecto. | Verificar logs en Dokploy y asegurar que `PORT=8001`. |
| **Error CORS en consola** | Dominio no autorizado en el backend. | Verificar `ALLOWED_ORIGINS` en variables de entorno. |
| **Fallo en Build** | Falta de memoria en el servidor. | Aumentar RAM o swap en DigitalOcean. |

---

**Firma de Conformidad del Despliegue:**

_____________________________
**Abel Moya Acosta**
Developer / DevOps
