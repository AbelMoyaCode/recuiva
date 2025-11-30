# 📘 MANUAL DE USUARIO - RECUIVA

**Sistema de Estudio Activo con Validación Semántica**

---

## 📋 Información General

| Campo | Descripción |
|-------|-------------|
| **Nombre del Sistema** | Recuiva |
| **Versión** | 1.0 |
| **URL de Acceso** | https://recuiva.duckdns.org |
| **Navegadores Compatibles** | Chrome, Firefox, Edge (versiones actuales) |
| **Dispositivos** | PC, Tablet, Smartphone |

---

## 1. ACCESO AL SISTEMA

### 1.1 Página de Inicio

Al ingresar a **https://recuiva.duckdns.org**, el usuario visualiza la página principal con información sobre el sistema y las opciones de acceso.

**Opciones disponibles:**
- **Iniciar Sesión**: Para usuarios con cuenta existente.
- **Crear Cuenta**: Para nuevos usuarios.

> 📸 **Figura MU-1**: Captura de la página de inicio mostrando los botones "Iniciar Sesión" y "Crear Cuenta".

---

### 1.2 Crear una Cuenta

1. Hacer clic en **"Crear Cuenta"**.
2. Completar el formulario con:
   - Nombre completo
   - Correo electrónico institucional
   - Contraseña (mínimo 6 caracteres)
3. Hacer clic en **"Registrarse"**.
4. Verificar el correo electrónico si se solicita confirmación.

> 📸 **Figura MU-2**: Captura del formulario de registro con los campos requeridos.

---

### 1.3 Iniciar Sesión

1. Hacer clic en **"Iniciar Sesión"**.
2. Ingresar correo electrónico y contraseña.
3. Hacer clic en **"Entrar"**.
4. El sistema redirige al **Dashboard** principal.

> 📸 **Figura MU-3**: Captura del formulario de inicio de sesión.

---

## 2. DASHBOARD PRINCIPAL

El Dashboard es la pantalla central del sistema donde el usuario puede ver su progreso y acceder a todas las funcionalidades.

**Elementos del Dashboard:**

| Sección | Descripción |
|---------|-------------|
| **Resumen de Progreso** | Muestra materiales estudiados, repasos pendientes y estadísticas generales. |
| **Menú de Navegación** | Acceso rápido a todas las secciones del sistema. |
| **Repasos del Día** | Lista de materiales programados para repaso según el algoritmo SM-2. |

> 📸 **Figura MU-4**: Captura del Dashboard mostrando el resumen de progreso y menú de navegación.

---

## 3. SUBIR MATERIAL DE ESTUDIO

Esta funcionalidad permite cargar documentos PDF para generar preguntas de estudio automáticamente.

### Pasos para subir un material:

1. Ir a **"Subir Material"** desde el menú.
2. Hacer clic en **"Seleccionar archivo"** o arrastrar el PDF al área indicada.
3. Verificar que el archivo sea PDF y no supere 10 MB.
4. Ingresar un **título descriptivo** para el material.
5. Hacer clic en **"Subir Material"**.
6. Esperar mientras el sistema procesa el documento (extracción de texto, chunking y generación de embeddings).
7. Al finalizar, aparece mensaje de confirmación.

**Formatos aceptados:** PDF  
**Tamaño máximo:** 10 MB  
**Páginas recomendadas:** Hasta 50 páginas

> 📸 **Figura MU-5**: Captura de la pantalla de subida de material con el área de arrastre y el campo de título.

> 📸 **Figura MU-6**: Captura del mensaje de éxito tras subir un material correctamente.

---

## 4. MIS MATERIALES

En esta sección el usuario visualiza todos los materiales que ha subido al sistema.

**Funcionalidades disponibles:**

| Acción | Descripción |
|--------|-------------|
| **Ver detalles** | Muestra información del material (fecha, páginas, chunks generados). |
| **Iniciar Práctica** | Comienza una sesión de estudio con ese material. |
| **Eliminar** | Borra el material y sus datos asociados. |

> 📸 **Figura MU-7**: Captura de la lista de materiales mostrando las opciones disponibles para cada uno.

---

## 5. SESIÓN DE PRÁCTICA (Active Recall)

Esta es la funcionalidad principal del sistema. Permite estudiar activamente mediante preguntas y validación semántica de respuestas.

### Flujo de una sesión de práctica:

1. Seleccionar un material desde **"Mis Materiales"** o **"Repasos"**.
2. Hacer clic en **"Iniciar Práctica"**.
3. El sistema muestra una **pregunta** generada automáticamente.
4. Escribir la respuesta en el campo de texto.
5. Hacer clic en **"Validar Respuesta"**.
6. El sistema evalúa la respuesta usando validación semántica híbrida.
7. Se muestra el resultado:
   - ✅ **Correcta**: La respuesta es completa y precisa.
   - 🟡 **Parcial**: La respuesta es incompleta pero tiene conceptos correctos.
   - ❌ **Incorrecta**: La respuesta no corresponde al contenido esperado.
8. Se muestra retroalimentación con el fragmento correcto del material.
9. Hacer clic en **"Siguiente Pregunta"** para continuar.

> 📸 **Figura MU-8**: Captura de la pantalla de práctica mostrando una pregunta y el campo de respuesta.

> 📸 **Figura MU-9**: Captura del resultado de validación mostrando el score, clasificación y fragmento relevante.

---

## 6. REPASOS PROGRAMADOS

El sistema implementa el algoritmo **SM-2 (SuperMemo 2)** para programar repasos en intervalos óptimos.

### Cómo funcionan los repasos:

- Después de cada práctica, el sistema calcula cuándo debes repasar ese material.
- Los materiales aparecen en **"Repasos"** cuando llega su fecha programada.
- Materiales con respuestas incorrectas se repasan antes.
- Materiales dominados tienen intervalos más largos.

**Intervalos típicos:** 1 día → 3 días → 7 días → 14 días → 30 días → 60 días

> 📸 **Figura MU-10**: Captura de la sección de repasos mostrando materiales pendientes y sus fechas.

---

## 7. MI PERFIL

En esta sección el usuario puede ver y editar su información personal.

**Información visible:**
- Nombre de usuario
- Correo electrónico
- Fecha de registro
- Estadísticas generales (materiales subidos, sesiones completadas)

**Acciones disponibles:**
- Cambiar contraseña
- Cerrar sesión

> 📸 **Figura MU-11**: Captura de la pantalla "Mi Perfil" con la información del usuario.

---

## 8. CERRAR SESIÓN

Para salir del sistema de forma segura:

1. Hacer clic en el ícono de usuario o en **"Mi Perfil"**.
2. Hacer clic en **"Cerrar Sesión"**.
3. El sistema redirige a la página de inicio.

---

## 9. RECOMENDACIONES DE USO

### Para mejores resultados:

| Recomendación | Descripción |
|---------------|-------------|
| **Subir PDFs legibles** | Evitar documentos escaneados con mala calidad (afecta la extracción de texto). |
| **Títulos descriptivos** | Usar nombres claros como "Capítulo 3 - Bases de Datos" en lugar de "archivo1". |
| **Practicar diariamente** | El Active Recall es más efectivo con práctica constante. |
| **Completar repasos** | No ignorar los repasos programados, son clave para retención a largo plazo. |
| **Respuestas completas** | Escribir respuestas con tus propias palabras, no solo palabras clave. |

---

## 10. SOLUCIÓN DE PROBLEMAS COMUNES

### El PDF no se procesa correctamente

**Posibles causas:**
- El PDF es una imagen escaneada sin OCR.
- El archivo está corrupto o protegido.
- Excede el tamaño máximo de 10 MB.

**Solución:** Usar PDFs con texto seleccionable. Si es escaneado, aplicar OCR antes de subir.

---

### La validación marca respuestas correctas como incorrectas

**Posibles causas:**
- La respuesta usa términos muy diferentes al material original.
- El fragmento recuperado no es el más relevante.

**Solución:** Intentar usar vocabulario similar al del material. Revisar el fragmento mostrado en la retroalimentación.

---

### No puedo iniciar sesión

**Posibles causas:**
- Contraseña incorrecta.
- Cuenta no verificada.

**Solución:** Usar "Olvidé mi contraseña" o verificar el correo de confirmación.

---

## 11. CONTACTO Y SOPORTE

Para reportar problemas o sugerencias:

| Canal | Información |
|-------|-------------|
| **Desarrollador** | Abel Jesús Moya Acosta |
| **Correo** | amoyaa2@upao.edu.pe |
| **Repositorio** | github.com/AbelMoyaCode/recuiva |

---

## 📎 RESUMEN DE FIGURAS DEL MANUAL

| Figura | Descripción | Página/Sección a capturar |
|--------|-------------|---------------------------|
| MU-1 | Página de inicio | `index.html` - Vista completa |
| MU-2 | Formulario de registro | `auth/crear-cuenta.html` |
| MU-3 | Formulario de login | `auth/iniciar-sesion.html` |
| MU-4 | Dashboard principal | `app/dashboard.html` |
| MU-5 | Pantalla subir material | `app/subir-material.html` |
| MU-6 | Mensaje de éxito al subir | `app/subir-material.html` (estado éxito) |
| MU-7 | Lista de materiales | `app/materiales.html` |
| MU-8 | Pregunta en sesión práctica | `app/sesion-practica.html` |
| MU-9 | Resultado de validación | `app/sesion-practica.html` (post-validación) |
| MU-10 | Repasos programados | `app/repasos.html` |
| MU-11 | Perfil de usuario | `app/mi-perfil.html` |

---

**Fin del Manual de Usuario**

*Documento elaborado por: Abel Jesús Moya Acosta*  
*Versión: 1.0*  
*Fecha: Noviembre 2025*
