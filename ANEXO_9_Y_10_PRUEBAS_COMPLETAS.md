UNIVERSIDAD PRIVADA ANTENOR ORREGO
FACULTAD DE INGENIERÍA
PROGRAMA DE ESTUDIO DE INGENIERÍA DE SISTEMAS E INTELIGENCIA ARTIFICIAL

_______________________________________________________________________________

“SISTEMA WEB DE REPETICIÓN ESPACIADA Y VALIDACIÓN SEMÁNTICA (RECUIVA)”

_______________________________________________________________________________

ALUMNO:
ABEL MOYA

DOCENTE:
WALTER CUEVA CHAVEZ

TRUJILLO – PERÚ
2025

<br>
<br>
<br>

# ANEXO 9: PLAN DE PRUEBAS DE CAJA NEGRA - RECUIVA

**Tipo de prueba a realizar:**
Pruebas de Funcionalidad y Validación de Entradas (Alfanuméricos)

**Descripción:**
Se debe anotar lo que se probará (funcionalidad), se deben describir lo siguiente: Todo lo que está fuera de los módulos. Interfaces, Respuesta a las entradas, Integridad de archivos, Evaluar diferentes escenarios, Respuestas de la aplicación, Secuencia de mensajes.

---
<br>

## ESCENARIO 0: INICIO DE SESIÓN (LOGIN)

**Datos de Entrada:**
Credenciales de acceso de un usuario registrado.

**Entorno:**
Módulo de Autenticación (`AuthPage`). Interfaz de Login con campos de correo y contraseña, y opción de "Olvidé mi contraseña".

**Parámetros:**
●	Input Correo Electrónico (Validación de formato)
●	Input Contraseña (Min. 6 caracteres)

**Respuesta de otros módulos:**
●	**Supabase Auth:** Verifica el hash de la contraseña y retorna un JWT (Session Token).
●	**Context API:** Actualiza el estado global de `SessionUser`.
●	**Router:** Redirige a rutas protegidas si la autenticación es exitosa.

**Condiciones iniciales:**
1.	Se intenta ingresar con campos vacíos.
2.	Se ingresa un correo con caracteres inválidos (ej: "juan$#").
3.	Se ingresa un correo válido pero contraseña incorrecta.
4.	Se ingresan credenciales correctas de un usuario activo.

**Datos de Salida:**

**Resultados entregados:**
●	Para la condición 1, validación HTML5/Zod impide el envío y marca los campos en rojo.
●	Para la condición 2, el sistema detecta **formatos no alfanuméricos válidos** en el correo y bloquea el envío ("Formato de correo inválido").
●	Para la condición 3, tras verificar con Supabase, muestra: "Email o contraseña incorrectos".
●	Para la condición 4, se recibe el token de sesión, se guarda en LocalStorage y se redirige al usuario a la vista `/dashboard`.

**Estado final de las variables:**
Objeto `user_session` instanciado en el navegador con los datos del usuario.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 1**. *Login fallido por credenciales inválidas.*
<br>
<br>
**Figura 2**. *Acceso exitoso al Dashboard.*
<br>
<br>

**Requisitos de configuración para hacer la prueba:**
Usuario debe estar previamente registrado (Escenario 1).

**Método de Prueba:**
Prueba de caminos alternativos (Happy path vs Error path).

**Módulos:**
Frontend: `SignInForm`. Backend: `Supabase.auth.signInWithPassword`.

**Hardware y Software:**
Navegador Chrome/Edge. Conexión HTTPS requerida.

**Dependencias o relación con otros casos de prueba:**
-	Prerrequisito absoluto para TODO el sistema.

---
<br>

## ESCENARIO 1: REGISTRO DE NUEVO ESTUDIANTE (VALIDACIÓN ALFANUMÉRICA)

**Datos de Entrada:**
Registro de nuevo usuario en la plataforma.

**Entorno:**
Módulo de registro (Sign Up). Campos para nombres, correo institucional, contraseña.

**Parámetros:**
●	Input Nombres Completos (Solo letras y espacios, no números ni símbolos).
●	Input Correo Electrónico.
●	Input Contraseña.

**Respuesta de otros módulos:**
●	**Zod Validator:** Ejecuta regex para filtrar caracteres no permitidos en el nombre.
●	**Supabase Auth:** Creación de credenciales.

**Condiciones iniciales:**
1.	Se ingresa un nombre con números o símbolos (ej: "Juan123", "Abel_Moya").
2.	Se ingresa un correo sin formato válido (ej: "usuario.com").
3.	Se ingresa una contraseña corta.
4.	Se ingresan todos los datos válidos (Nombre solo letras).

**Datos de Salida:**

**Resultados entregados:**
●	Para la condición 1 (**Validación Alfanumérica**), el sistema muestra error: "El nombre solo debe contener letras y espacios" (Rechazo de caracteres numéricos/especiales).
●	Para la condición 2, muestra: "Ingrese un correo electrónico válido".
●	Para la condición 3, muestra: "La contraseña debe tener al menos 6 caracteres".
●	Para la condición 4, el sistema crea el usuario exitosamente y redirige.

**Estado final de las variables:**
`auth.users` contiene el nuevo UUID. `public_user_profiles` contiene el registro vinculado.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 3**. *Validación de campos alfanuméricos en el registro.*
<br>
<br>
**Figura 4**. *Registro exitoso y redirección al Dashboard.*
<br>
<br>

**Requisitos de configuración para hacer la prueba:**

**Método de Prueba:**
Partición de equivalencia y **Prueba de Validación de Entradas**. Se verifica explícitamente el rechazo de datos no alfanuméricos donde no corresponde.

**Módulos:**
Frontend: `SignUpForm` (React Hook Form + Zod).

**Hardware y Software:**
Sistema operativo: Windows 11. Navegador web: Google Chrome / Edge.

**Procedimientos o Herramientas necesarios:**
Intentar registrar usuarios con nombres como "User 01" o "Nombre!" para confirmar el bloqueo.

**Dependencias o relación con otros casos de prueba:**
-	Prerrequisito para acceso.

---
<br>

## ESCENARIO 2: GESTIÓN DE MATERIALES (CARGA DE PDF Y RAG)

**Datos de Entrada:**
Subida de documentos académicos en formato PDF.

**Entorno:**
Módulo "Mi Biblioteca". Zona de "Drag & Drop".

**Parámetros:**
●	Archivo seleccionado (.pdf)

**Respuesta de otros módulos:**
●	**StorageService:** Valida tipo MIME.
●	**EmbeddingService:** Genera chunks y vectores. Valida integridad del texto extraído.

**Condiciones iniciales:**
1.	Se intenta subir un archivo no permitido (ej: .docx).
2.	Se sube un PDF válido estándar.

**Datos de Salida:**

**Resultados entregados:**
●	Para la condición 1, rechazo inmediato: "Formato no soportado".
●	Para la condición 2, éxito en la carga y visualización de la barra de progreso.

**Estado final de las variables:**
Tabla `material_embeddings` poblada con vectores.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 5**. *Rechazo de archivo por formato inválido.*
<br>
<br>
**Figura 6**. *Carga y vectorización exitosa.*
<br>
<br>

**Método de Prueba:**
Prueba de límites y formato.

---
<br>

## ESCENARIO 3: GENERACIÓN DE PREGUNTAS CON IA Y RESULTADOS DE CHUNKS

**Datos de Entrada:**
Solicitud de generación de flashcards.

**Entorno:**
Vista de detalle del material.

**Parámetros:**
●	Material ID.
●	Contexto (Chunks recuperados).

**Respuesta de otros módulos:**
●	**RAG Engine:** Recupera los chunks más relevantes (Top-K) basados en similitud coseno.
●	**Groq API:** Genera preguntas.

**Condiciones iniciales:**
1.	Material sin texto procesable.
2.	Material válido con texto rico.

**Datos de Salida:**

**Resultados entregados:**
●	Para la condición 1, alerta de "Texto no procesable".
●	Para la condición 2, recuperación exitosa de **Chunks (Similitud > 0.7)** y generación de 5 preguntas coherentes.

**Estado final de las variables:**
`questions` table recibe registros.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 7**. *Modal de generación de preguntas.*
<br>
<br>
**Figura 8**. *Preguntas generadas listas para guardar.*
<br>
<br>

**Método de Prueba:**
Pruebas de Integración y **Verificación de Recuperación (Chunks)**.

---
<br>

## ESCENARIO 4: SESIÓN DE ESTUDIO (VALIDACIÓN SEMÁNTICA)

**Datos de Entrada:**
Respuesta del estudiante.

**Entorno:**
Interfaz de "Modo Estudio".

**Parámetros:**
●	Input Respuesta del Usuario.

**Respuesta de otros módulos:**
●	**ValidationService:** Compara respuesta usuario vs respuesta ideal.

**Condiciones iniciales:**
1.	Respuesta vacía.
2.	Respuesta parafraseada correcta.

**Datos de Salida:**

**Resultados entregados:**
●	Para la condición 1, solicita más detalle.
●	Para la condición 2, el algoritmo de similitud semántica (Cosine Similarity) retorna **Score > 0.8**, marcando la respuesta como "Correcta".

**Estado final de las variables:**
Actualización de feedback visual.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 9**. *Respuesta incorrecta y retroalimentación.*
<br>
<br>
**Figura 10**. *Validación positiva de respuesta parafraseada.*
<br>
<br>

**Método de Prueba:**
Pruebas Funcionales y de Algoritmo Semántico.

---
<br>

## ESCENARIO 5: ALGORITMO DE REPETICIÓN ESPACIADA (SM-2)

**Datos de Entrada:**
Calificación de autoevaluación (Easy, Good, Hard, Again).

**Entorno:**
Botonera de calificación post-respuesta.

**Parámetros:**
●	Calidad de respuesta (0-5).

**Respuesta de otros módulos:**
●	**SM2Algorithm:** Calcula nueva fecha de repaso.

**Condiciones iniciales:**
1.	Usuario marca "Again".
2.	Usuario marca "Easy".

**Datos de Salida:**

**Resultados entregados:**
●	"Again": Intervalo < 1 día.
●	"Easy": Intervalo > 4 días.

**Estado final de las variables:**
`next_review_date` actualizada.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 11**. *Botones de calificación SM-2.*
<br>
<br>
**Figura 12**. *Programación de próxima revisión en BD.*
<br>
<br>

---
<br>

## ESCENARIO 6: VISUALIZACIÓN DE ESTADÍSTICAS

**Datos de Entrada:**
Acceso al Dashboard.

**Entorno:**
Módulo `/analytics`.

**Parámetros:**
●	Historial de repasos.

**Respuesta de otros módulos:**
●	**AnalyticsService:** Agregación de datos.

**Condiciones iniciales:**
1.	Usuario con actividad reciente.

**Datos de Salida:**

**Resultados entregados:**
●	Gráficos de barras mostrados correctamente con los datos del usuario.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 13**. *Dashboard con estadísticas del usuario.*
<br>
<br>

---
<br>

## ESCENARIO 7: GESTIÓN DE PERFIL (VALIDACIÓN ALFANUMÉRICA)

**Datos de Entrada:**
Actualización de Nombres/Apellidos.

**Entorno:**
Página "Mi Perfil".

**Parámetros:**
●	Input Nombres (Solo alfanuméricos válidos).

**Respuesta de otros módulos:**
●	**Validation:** Expresión regular impide caracteres especiales.

**Condiciones iniciales:**
1.	Se intenta guardar un nombre "Admin@123".
2.	Se guarda un nombre válido "Abel Moya".

**Datos de Salida:**

**Resultados entregados:**
●	Para la condición 1, error de validación: "El nombre contiene caracteres inválidos".
●	Para la condición 2, actualización exitosa y feedback visual (Toast).

**Estado final de las variables:**
Perfil actualizado.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 14**. *Validación de caracteres en edición de perfil.*
<br>
<br>

---
<br>

## ESCENARIO 8: GESTIÓN DE MIS MATERIALES (CRUD)

**Datos de Entrada:**
Eliminación de material.

**Entorno:**
Biblioteca.

**Respuesta de otros módulos:**
●	**Cascade Delete:** Eliminación de embeddings y preguntas vinculadas.

**Condiciones iniciales:**
1.	Eliminar material con preguntas asociadas.

**Datos de Salida:**

**Resultados entregados:**
●	Confirmación de borrado en cascada exitosa.

**Se adjunta screens de las pruebas:**
<br>
<br>
**Figura 15**. *Confirmación de eliminación de material.*
<br>
<br>

_______________________________________________________________________________
<br>
<br>
<br>

# Anexo 10: Documentos de Heurísticas de Nielsen

**Metodología**

**1.1 Comparación entre Usabilidad y Experiencia del usuario**
Cuando hablamos de Usabilidad, refiriéndonos al contexto de Recuiva, apuntamos al grado en que la plataforma educativa puede ser usada por los estudiantes para generar material y repasar conceptos con efectividad y eficiencia.

**1.2 Métodos de evaluación de usabilidad**

**1.2.1 Evaluación Heurística**
La evaluación heurística realizada a Recuiva consiste en un análisis técnico basado en los 10 principios de Jakob Nielsen.

**3. Ejecución (Hallazgos Principales)**

**Hallazgo 1: Feedback durante la Vectorización (H1 - Visibilidad)**
*   **Problema:** Spinner indeterminado en PDFs grandes.
*   **Severidad:** (3) Mayor.

**Hallazgo 2: Edición de Preguntas Generadas (H3 - Control del Usuario)**
*   **Problema:** No se pueden editar preguntas antes de guardar.
*   **Severidad:** (2) Menor.

**Hallazgo 3: Terminología Técnica (H2 - Conexión)**
*   **Problema:** Uso de palabras como "Embeddings" en errores.
*   **Severidad:** (2) Menor.

**Hallazgo 4: Modo Estudio Recargado (H8 - Minimalismo)**
*   **Problema:** Distracciones visuales en modo repaso.
*   **Severidad:** (2) Menor.

**5. Gráficos y Anexos**

**Figura 16**. *Loader de generación de IA (Mejora propuesta).*

**Figura 17**. *Validación de archivos en el Uploader.*

**Figura 18**. *Comparativa Modo Normal vs Modo Estudio (Zen).*

<br>
<br>
<br>

# HOJA DE APROBACIÓN

<br>

| Rol | Nombre | Firma / Conformidad | Fecha |
| :--- | :--- | :--- | :--- |
| **Desarrollador** | Abel Moya Acosta | ____________________ | 06/12/2025 |
| **Docente / Revisor** | Walter Cueva Chavez | ____________________ | |
