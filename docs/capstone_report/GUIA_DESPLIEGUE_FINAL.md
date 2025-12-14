# GUÍA DE DESPLIEGUE - RECUIVA 
**Proyecto:** Recuiva - Plataforma de Estudio con IA  
**Responsable:** Abel Moya Acosta  
**Fecha:** 14/12/2025  
**Versión:** 1.0 (Producción)  

## 1. INTRODUCCIÓN
Este documento describe el procedimiento paso a paso para el despliegue de la aplicación web Recuiva en un entorno de producción utilizando DigitalOcean como proveedor de infraestructura, Dokploy como gestor de despliegue (PaaS auto-hospedado) y DuckDNS para la gestión de dominios dinámicos.

**Arquitectura de Despliegue**
*   **Infraestructura:** VPS (Droplet) Ubuntu 22.04 LTS en DigitalOcean.
*   **Orquestación:** Docker Compose gestionado por Dokploy.
*   **Base de Datos:** Supabase Cloud (PostgreSQL + pgvector).
*   **Proxy Inverso:** Traefik (incluido en Dokploy) para gestión de SSL/HTTPS.
*   **Dominios:** `recuiva.duckdns.org` (Frontend) y `api-recuiva.duckdns.org` (Backend).

## 2. REQUISITOS PREVIOS
Antes de iniciar, se debe contar con:
1.  Cuenta en GitHub con acceso al repositorio `AbelMoyaCode/recuiva`.
2.  Servidor VPS (DigitalOcean) activo con Dokploy instalado y accesible vía IP.
3.  Dominios DuckDNS creados y apuntando a la IP del servidor.
4.  Credenciales de Supabase (URL y Keys) para las variables de entorno.

**Figura 1**
*Panel de DigitalOcean con el Droplet activo*

*(Imagen del panel de DigitalOcean)*

*Nota.* Se verifica que el Droplet tenga asignada una IP pública.

## 3. PASO 1: INFRAESTRUCTURA (DIGITAL OCEAN)
**3.1. Especificaciones del Servidor**
*   **OS:** Ubuntu 22.04 LTS (x64).
*   **Plan:** Basic -> Regular -> $12/mo (2GB RAM / 60GB SSD).

**Figura 2**
*Configuración inicial del Droplet (2GB RAM / 60GB SSD)*

*(Imagen de configuración Droplet)*

*Nota.* Corrección: El disco SSD asignado es de 60GB para almacenamiento suficiente de datos Docker.

**3.2. Seguridad (Firewall)**
Configuramos `recuiva-firewall` permitiendo puertos esenciales.

**Figura 3**
*Reglas de entrada del Cloud Firewall*

*(Imagen del Firewall)*

*Nota.* Puertos abiertos: 22, 80, 443, 3000.

**3.3. Monitoreo**

**Figura 4**
*Métricas de rendimiento inicial*

*(Imagen de métricas)*

*Nota.* Confirmación de recursos disponibles antes de la instalación.

## 4. PASO 2: PREPARACIÓN DEL REPOSITORIO (GITHUB)
El código fuente debe estar actualizado en la rama `main` del repositorio.

**4.1. Estructura de Archivos Crítica**
Es vital verificar que existan los archivos de configuración Docker en la raíz:
```text
recuiva/
├── docker-compose.yml       <-- Orquestador principal
├── Dockerfile               <-- Backend (Python)
├── Dockerfile.frontend      <-- Frontend (Nginx/HTML)
├── backend/                 <-- Código fuente API
└── public/                  <-- Código fuente Web
```

**Figura 5**
*Vista del repositorio en GitHub confirmando estructura*

*(Imagen del repositorio)*

*Nota.* Sin estos archivos exactos, el "build" de Dokploy fallará.

## 5. PASO 3: INSTALACIÓN DOKPLOY (SSH)
**5.1. Instalación en el Servidor**
En la terminal SSH:
```bash
# Conexión al VPS
ssh root@147.182.226.170

# Instalación automática
curl -sSL https://dokploy.com/install.sh | sh
```

**Figura 6**
*Logs de instalación exitosa en terminal*

*(Imagen de terminal)*

*Nota.* Confirmación de que Docker Swarm y el panel de control se han inicializado correctamente.

**5.2. Acceso y Configuración**

**Figura 7**
*Pantalla de Login/Registro de Dokploy*

*(Imagen de Login)*

*Nota.* Creación del usuario administrador.

**Figura 8**
*Conexión con GitHub (Git Providers)*

*(Imagen de integración Git)*

*Nota.* Integración exitosa con check verde.

## 6. PASO 4: CONFIGURACIÓN EN DOKPLOY
**6.1. Conexión del Servicio Backend**
1.  Ingresar al panel de Dokploy.
2.  Crear nuevo Proyecto "Recuiva".
3.  Seleccionar "Compose".
4.  Conectar `AbelMoyaCode/recuiva` (Rama `main`).

**Figura 9**
*Dashboard de proyectos en Dokploy*

*(Imagen del Dashboard)*

*Nota.* Proyecto contenedor creado.

**Figura 10**
*Selección de repositorio y método Compose*

*(Imagen de selección)*

*Nota.* Configuración del "Source" apuntando a AbelMoyaCode/recuiva y rama main.

**6.2. Configuración de Variables de Entorno (Backend)**
En la pestaña "Environment", ingresar las claves críticas:
```env
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

**Figura 11**
*Inyección de variables de entorno*

*(Imagen de variables)*

*Nota.* Las variables se inyectan en tiempo de ejecución a los contenedores Docker.

**6.3. Configuración Específica del Frontend**
Para que la interfaz web se comunique correctamente con la API en producción, se definen las variables de entorno públicas que se inyectan durante la construcción (Build Time).

**Figura 12**
*Declaración de variables de entorno para el Frontend (VITE_)*

```env
# Conexión API Backend (Dominio Seguro)
VITE_API_URL=https://api-recuiva.duckdns.org/api

# Cliente Supabase (Auth y Storage)
VITE_SUPABASE_URL=https://tu-proyecto.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbG...
```

*Nota.* El uso del prefijo `VITE_` es obligatorio para exponer estas variables al navegador del cliente de forma segura.

## 7. PASO 5: CONFIGURACIÓN DE DOMINIOS Y SSL
**7.1. Registro DNS**

**Figura 13**
*Panel de gestión DuckDNS*

*(Imagen DuckDNS)*

*Nota.* recuiva y api-recuiva apuntando a la IP.

**7.2. Frontend (recuiva.duckdns.org)**
*   Puerto: 80
*   HTTPS: Activado (Let's Encrypt).

**Figura 14**
*Configuración de dominio Frontend*

*(Imagen config frontend)*

*Nota.* El proxy redirige el tráfico HTTPS al puerto 80 interno del contenedor web.

**7.3. Backend (api-recuiva.duckdns.org)**
*   Puerto: 8001
*   HTTPS: Activado.

**Figura 15**
*Configuración de dominio Backend*

*(Imagen config backend)*

*Nota.* El proxy redirige las peticiones de API al puerto 8001 de FastAPI.

**Figura 16**
*Explorador de archivos Traefik*

*(Imagen Traefik)*

*Nota.* Configuración dinámica de Traefik.

## 8. PASO 6: EJECUCIÓN DEL DESPLIEGUE
**8.1. Build & Deploy**
Ir a la pestaña "Deployments" y hacer clic en "Deploy".

**Figura 17**
*Logs de construcción de imágenes*

*(Imagen logs build)*

*Nota.* Evidencia de la construcción de imágenes y despliegue en el clúster Swarm.

**Figura 18**
*Historial de despliegues*

*(Imagen historial)*

*Nota.* Despliegue completado satisfactoriamente.

**8.2. Verificación Swarm**

**Figura 19**
*Estado del clúster Swarm*

*(Imagen cluster)*

*Nota.* Clúster operativo y contenedores (frontend-1, backend-1) en estado Running.

## 9. VERIFICACIÓN FINAL
**9.1. Verificación del Backend (API)**
Navegar a `https://api-recuiva.duckdns.org/api/health`.

**Figura 20**
*Respuesta JSON del endpoint de salud*

*(Imagen health check)*

*Nota.* Verificación de disponibilidad del servicio API (/api/health).

**9.2. Prueba Módulo IA**

**Figura 21**
*Prueba de conexión de inferencia de IA de API Groq*

*(Imagen prueba Groq)*

*Nota.* Validación funcional de conexión del módulo de embeddings y generación de respuestas.

**9.3. Verificación del Frontend (App Web)**
Navegar a `https://recuiva.duckdns.org`.

**Figura 22**
*Aplicación corriendo en el navegador*

*(Imagen App Web)*

*Nota.* Interfaz de usuario final accesible mediante dominio seguro HTTPS.

**9.4. Logs de Producción**

**Figura 23**
*Logs del servicio backend*

*(Imagen logs prod)*

*Nota.* Registro de actividad del servidor en tiempo real.

## 10. SOLUCIÓN DE PROBLEMAS COMUNES
*   **Error 502 Bad Gateway:** Verificar que el contenedor esté corriendo y `PORT=8001`.
*   **Error CORS:** Verificar `ALLOWED_ORIGINS` en las variables de entorno.
*   **Fallo en Build:** Aumentar RAM (Swap) si falla por memoria.

___
**Firma de Acta de Conformidad del Despliegue:**


______________________________________
**Walter Cueva Chavez**
Developer / DevOps
