# PLAN DE PRUEBAS DE CAJA NEGRA - RECUIVA

**Proyecto:** Recuiva - Plataforma de Estudio Active Recall con Validación Semántica  
**Responsable:** Abel Moya Acosta  
**Fecha:** 06/12/2025  
**Versión:** 1.0  

---

## INTRODUCCIÓN

Este documento detalla el plan de pruebas de caja negra para el proyecto **Recuiva**. El objetivo es validar las funcionalidades críticas ("Core") del sistema desde la perspectiva del usuario final, asegurando que las entradas, procesos y salidas cumplan con los requisitos funcionales establecidos. 

Se evalúan los flujos principales ("Ruta Feliz") priorizando la validación semántica, la gestión de sesiones de estudio y la generación de material mediante IA.

**Estructura de la Prueba:**
Para cada escenario se detallan:
1.  **Datos de Entrada:** Información provista por el usuario.
2.  **Entorno:** Configuración de hardware/software.
3.  **Parámetros:** Variables de configuración del sistema.
4.  **Condiciones Iniciales:** Estado previo requerido.
5.  **Salida Esperada:** Resultado correcto del sistema.
6.  **Evidencia:** Espacio reservado para capturas de pantalla que validen el éxito de la prueba.

---

## ESCENARIO 1: GESTIÓN DE USUARIO (REGISTRO E INICIO DE SESIÓN)
**Identificador:** CP-001  
**Módulo:** Autenticación

### Descripción
Verificar que un nuevo usuario pueda registrarse exitosamente en la plataforma y posteriormente iniciar sesión para acceder al dashboard principal.

### Datos de Entrada
*   **Correo Electrónico:** `usuario_prueba@email.com`
*   **Contraseña:** `Password123!` (al menos 6 caracteres)
*   **Nombre de Usuario:** `EstudianteDemo`

### Entorno
*   **Navegador:** Google Chrome (Versión más reciente) / Edge
*   **Sistema Operativo:** Windows 10/11
*   **Conexión:** Internet estable (Acceso a Supabase Auth)

### Parámetros
*   **Servicio de Autenticación:** Supabase Auth (Email/Password provider).
*   **Validación de Formulario:** Frontend (React Hook Form / Zod).

### Condiciones Iniciales
*   La aplicación web debe estar desplegada y accesible.
*   El usuario NO debe existir previamente en la base de datos (o debe haber sido eliminado).

### Salida Esperada
1.  Al registrarse, el sistema redirige al usuario al Dashboard o muestra confirmación de cuenta creada.
2.  Al iniciar sesión con las credenciales correctas, el sistema otorga acceso al panel principal (`/dashboard`) y muestra el nombre del usuario.
3.  El token de sesión (JWT) se almacena correctamente (cookies/local storage).

### Evidencia de la Validación
> *Inserte aquí captura de pantalla del formulario de registro lleno y posterior redirección al Dashboard.*

`[ESPACIO PARA CAPTURA DE PANTALLA 1: FORMULARIO DE REGISTRO]`
`[ESPACIO PARA CAPTURA DE PANTALLA 2: DASHBOARD CON SESIÓN INICIADA]`

---

## ESCENARIO 2: CARGA Y PROCESAMIENTO DE MATERIAL (PDF A CHUNKS)
**Identificador:** CP-002  
**Módulo:** Gestión de Material (RAG)

### Descripción
Validar que el usuario pueda subir un archivo PDF, y que el sistema procese, fragmente ("chunkee") y almacene los vectores (embeddings) correctamente en la base de datos..

### Datos de Entrada
*   **Archivo:** `Documento_Prueba_Tesis.pdf` (PDF académico estándar, < 10MB, texto seleccionable).
*   **Título del Set:** "Introducción a la Tesis".

### Entorno
*   **Interfaz Web:** Módulo "Crear Nuevo Set".
*   **Backend:** Python (FastAPI/Flask) + PyPDF2 + SentenceTransformers.

### Parámetros
*   **Tamaño de Chunk:** ~200-300 palabras (configuración del splitter).
*   **Overlap:** ~50 palabras.
*   **Modelo de Embeddings:** `all-MiniLM-L6-v2`.

### Condiciones Iniciales
*   Usuario logueado en la plataforma.
*   El backend de procesamiento debe estar activo y conectado a la BD Vectorial.

### Salida Esperada
1.  Barra de progreso completa al 100%.
2.  Mensaje de éxito: "Documento procesado correctamente".
3.  El nuevo Set aparece en la lista de "Mis Materiales".
4.  (Verificación interna) Los chunks y sus embeddings existen en la tabla `document_chunks` en Supabase.

### Evidencia de la Validación
> *Inserte aquí captura del mensaje de éxito tras subir el PDF y la vista del nuevo set creado en la lista.*

`[ESPACIO PARA CAPTURA DE PANTALLA: MENSAJE DE ÉXITO DE CARGA]`
`[ESPACIO PARA CAPTURA DE PANTALLA: LISTA DE SETS MOSTRANDO EL NUEVO MATERIAL]`

---

## ESCENARIO 3: GENERACIÓN DE PREGUNTAS CON IA (GROQ API)
**Identificador:** CP-003  
**Módulo:** Generador de Preguntas

### Descripción
Verificar que el sistema pueda generar preguntas de práctica automáticamente a partir del contenido de un PDF subido, utilizando la integración con Groq API (Llama 3), y que estas sean editables.

### Datos de Entrada
*   **Set Seleccionado:** "Introducción a la Tesis" (del CP-002).
*   **Tipo de Pregunta:** "Pregunta Abierta para Active Recall".
*   **Cantidad Solicitada:** 3 preguntas sugeridas.

### Entorno
*   **API:** Groq API (Modelo `llama-3.1-8b-instant`).
*   **Contexto:** Chunks recuperados del PDF subido.

### Parámetros
*   **Prompt:** Template de sistema para generar preguntas educativas sin alucinaciones.
*   **Temperatura:** 0.3 (para mayor determinismo).

### Condiciones Iniciales
*   El material (Set) debe tener chunks procesados y disponibles.

### Salida Esperada
1.  El sistema muestra una lista de preguntas sugeridas coherentes con el texto del PDF.
2.  El usuario puede **editar** el texto de una pregunta sugerida antes de guardarla.
3.  Las preguntas seleccionadas se guardan en el banco de preguntas del Set.

### Evidencia de la Validación
> *Inserte aquí captura de las preguntas generadas por la IA y el modal de edición.*

`[ESPACIO PARA CAPTURA DE PANTALLA: SUGERENCIAS DE IA MOSTRADAS EN PANTALLA]`
`[ESPACIO PARA CAPTURA DE PANTALLA: PREGUNTA GUARDADA EN EL SET]`

---

## ESCENARIO 4: FLUJO DE ESTUDIO ACTIVE RECALL (PRÁCTICA)
**Identificador:** CP-004  
**Módulo:** Modo Práctica

### Descripción
Validar el flujo principal de estudio: El usuario ve una pregunta, intenta responderla mentalmente o por escrito (sin ver la respuesta), revela la respuesta real/fragmento fuente y se autoevalúa.

### Datos de Entrada
*   **Acción de Usuario:** Clic en botón "Comenzar Práctica".
*   **Respuesta Usuario (Input):** "La tesis es un trabajo de investigación original..." (Texto ingresado en el campo de respuesta).

### Entorno
*   **Interfaz de Estudio:** Vista limpia sin distracciones.

### Parámetros
*   **Modo:** Active Recall (Pregunta -> Esfuerzo de Recuperación -> Feedback).

### Condiciones Iniciales
*   Debe existir al menos un Set con preguntas creadas.

### Salida Esperada
1.  Se muestra la pregunta CLARAMENTE.
2.  El contenido de la fuente (respuesta correcta) está OCULTO inicialmente.
3.  Al hacer clic en "Revelar/Validar", se muestra el fragmento original del PDF que responde la pregunta.
4.  El sistema permite pasar a la siguiente pregunta.

### Evidencia de la Validación
> *Inserte captura del estado "Pregunta" (respuesta oculta) y estado "Respuesta Revelada".*

`[ESPACIO PARA CAPTURA DE PANTALLA: INTERFAZ CON PREGUNTA]`
`[ESPACIO PARA CAPTURA DE PANTALLA: RESPUESTA INGRESADA Y FRAGMENTO REVELADO]`

---

## ESCENARIO 5: VALIDACIÓN SEMÁNTICA HÍBRIDA (FEEDBACK AUTOMÁTICO)
**Identificador:** CP-005  
**Módulo:** HybridValidator

### Descripción
Comprobar que el sistema evalúa la respuesta del usuario contrastándola semánticamente con el fragmento fuente y asigna una calificación (Correcto, Parcial, Incorrecto) de forma automática.

### Datos de Entrada
*   **Pregunta:** "¿Cuál es el objetivo de la validación híbrida?"
*   **Fragmento Fuente (Ground Truth):** "...combinar BM25 para palabras clave y similitud coseno para contexto semántico..."
*   **Respuesta Usuario (Variación Semántica):** "Su meta es usar tanto la búsqueda exacta de términos como el significado vectorial para mejorar la precisión." (Sinónimos y parafraseo).

### Entorno
*   **Algoritmo:** HybridValidator (Python).

### Parámetros
*   **Pesos:** 30% BM25 + 50% Cosine + 20% Coverage.
*   **Umbral de Aprobación:** Score > 0.70 (configurable).

### Condiciones Iniciales
*   Usuario en sesión de práctica activa enviando una respuesta.

### Salida Esperada
1.  El sistema clasifica la respuesta como **"CORRECTA"** o **"ALTA PRECISIÓN"** a pesar de no usar las palabras exactas.
2.  Se muestra el Score de similitud (ej. "85% de precisión semántica").
3.  Se resalta las partes cubiertas (Coverage) si la interfaz lo permite.

### Evidencia de la Validación
> *Inserte captura del feedback automático mostrando la calificación positiva ante una respuesta parafraseada.*

`[ESPACIO PARA CAPTURA DE PANTALLA: FEEDBACK DE VALIDACIÓN SEMÁNTICA]`

---

## ESCENARIO 6: REPETICIÓN ESPACIADA (DASHBOARD DE REPASOS)
**Identificador:** CP-006  
**Módulo:** Algoritmo SM-2 / Dashboard

### Descripción
Verificar que, tras completar una sesión, el sistema programe el próximo repaso de las preguntas basándose en el desempeño (SM-2) y actualice el Dashboard.

### Datos de Entrada
*   **Calificación de Sesión:** El usuario recibió calificaciones "Correcto" en las preguntas de la sesión anterior.

### Entorno
*   **Cálculo:** Algoritmo SuperMemo-2 (actualización de `next_review_date`).

### Parámetros
*   **Intervalo Inicial:** 1 día (para aciertos).
*   **Easiness Factor:** Variable según historial.

### Condiciones Iniciales
*   Sesión de práctica CP-004/005 finalizada.

### Salida Esperada
1.  En el Dashboard, la sección "Próximos Repasos" muestra las preguntas estudiadas programadas para una fecha futura (ej. "Mañana" o fecha específica).
2.  Las métricas de "Preguntas Estudiadas" o "Tasa de Acierto" se actualizan globalmente.

### Evidencia de la Validación
> *Inserte captura del Dashboard mostrando la actualización de las métricas y la fecha del próximo repaso.*

`[ESPACIO PARA CAPTURA DE PANTALLA: DASHBOARD CON MÉTRICAS ACTUALIZADAS]`

---

## HOJA DE APROBACIÓN

| Rol | Nombre | Firma / Conformidad | Fecha |
| :--- | :--- | :--- | :--- |
| **Tesista / Desarrollador** | Abel Moya Acosta | ____________________ | 06/12/2025 |
| **Docente / Revisor** | [Nombre del Docente] | ____________________ | ___/___/___ |

---
*Nota: Las capturas de pantalla deben ser legibles y mostrar la fecha/hora del sistema si es posible para mayor validez.*
