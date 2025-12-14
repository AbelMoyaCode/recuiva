# **MANUAL DE USUARIO – RECUIVA**
Sistema de Estudio Activo con Validación Semántica

|**Versión del documento**|1\.0|
| :- | :- |
|**Fecha**|Noviembre 2025|
|**Autor**|Abel Jesús Moya Acosta|
|**Curso**|Taller Integrador I – UPAO|
## **TABLA DE CONTENIDOS**
[1. Información General del Sistema](#bookmark=id.dn88vllrhc4g) 

[2. Acceso al Sistema](#bookmark=id.m51shz7twoe5) 

[3. Dashboard Principal](#bookmark=id.sjomjtck6gf) 

[4. Subir Material de Estudio](#bookmark=id.vin90uczojdp) 

[5. Mis Materiales](#bookmark=id.nqf5r81267h9) 

[6. Sesión de Práctica (Active Recall)](#bookmark=id.5u4sdg3fuks5) 

[7. Repasos Programados (Algoritmo SM-2)](#bookmark=id.i9pwutgv2zmx) 

[8. Mi Perfil](#bookmark=id.jrc3nsg0mmqs) 

[9. Cerrar Sesión](#bookmark=id.1bkx60ln4wmn) 

[10. Solución de Problemas Comunes](#bookmark=id.2yhca564qk5p) 

[11. Contacto y Soporte](#bookmark=id.vt8yaoltsv3x) 

[Anexo: Índice de Figuras](#bookmark=id.5b5b1pm6ape) 










## **1. Información General del Sistema**
Recuiva es una plataforma educativa de vanguardia que utiliza Inteligencia Artificial para transformar documentos estáticos (PDFs) en sesiones de interrogatorio dinámico. A diferencia de los lectores tradicionales, Recuiva emplea **Active Recall** (Recuerdo Activo) y **Repetición Espaciada** para optimizar la retención de información a largo plazo.

**Recuiva** es más que un simple repositorio de documentos; es un entrenador personal de estudio impulsado por Inteligencia Artificial. La plataforma está diseñada para combatir la "curva del olvido" mediante dos técnicas científicamente probadas:

1. **Active Recall (Recuerdo Activo):** En lugar de releer pasivamente, el sistema te desafía con preguntas para que fuerces a tu cerebro a recuperar la información.
1. **Repetición Espaciada (Spaced Repetition):** El sistema programa los repasos en los momentos óptimos (justo antes de que olvides) para consolidar la memoria a largo plazo.

El sistema procesa tus documentos (PDFs) o te permite trabajar con libros físicos, generando un plan de estudio personalizado y validando tus respuestas semánticamente para asegurar que realmente entiendes los conceptos.
### **Ficha Técnica**

|**Campo**|**Descripción**|
| :- | :- |
|**Nombre del Sistema**|Recuiva|
|**Versión Actual**|v1.0 (MVP completado)|
|**URL de Acceso**|<https://recuiva.duckdns.org>|
|**Tecnologías Base**|React, Supabase, Groq API (LLM), pgvector|
|**Navegadores**|Google Chrome, Mozilla Firefox, Edge, Opera|
## **2. Acceso al Sistema**
### **2.1 Página de Inicio**
Al ingresar a la plataforma, el usuario es recibido por la página de aterrizaje con la propuesta de valor.

Al ingresar a https://recuiva.duckdns.org, encontrarás la página de bienvenida. Aquí podrás visualizar la propuesta de valor de Recuiva, entender cómo funciona el método de estudio y ver testimonios o ejemplos de uso.

- **Acción:** Utiliza los botones "Iniciar Sesión" o "Crear Cuenta" ubicados en la esquina superior derecha o en el centro de la pantalla para comenzar.

**Figura MU-1**\
*Página de inicio con botones de acceso* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.001.png)

*Nota. Captura de pantalla del sistema Recuiva (2025).*
### **2.2 Registro de Usuario**
Para utilizar las funciones de IA, es obligatorio disponer de una cuenta personal.

**Pasos para registrarse:**

1. Clic en **"Crear Cuenta"**.
1. Completar: Nombre, Correo Institucional, Contraseña.
1. Clic en **"Registrarse"**.


**Figura MU-2**\
*Formulario de registro* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.002.png)

*Nota. Elaboración propia (2025).*
### **2.3 Inicio de Sesión**
Si ya posee cuenta, ingrese sus credenciales.

**Pasos:**

1. Haga clic en **"Iniciar Sesión"**.
1. Ingrese su correo electrónico y contraseña registrados.
1. Haga clic en el botón **"Ingresar"**.
   1. *Nota:* Si olvidó su contraseña, utilice la opción "¿Olvidaste tu contraseña?" para restablecerla vía correo.

**Figura MU-3**\
*Formulario de inicio de sesión* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.003.png)

*Nota. Elaboración propia (2025).*
## **3. HOME Principal**

El Home es su "centro principal". Al iniciar sesión, verá una interfaz limpia diseñada para enfocar su atención en el estudio.

**Componentes Principales:**

1. **Organización de Carpetas:** El área central donde creará y gestionará sus asignaturas o temas (ej. "Anatomía", "Historia", "Tesis").


**Figura MU-4**\
*Home principal* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.004.png)

*Nota. Captura del sistema (2025).*
## **4. Subir Material de Estudio**
Recuiva procesa documentos PDF para entender su contenido (Chunking + Embeddings).

**Pasos:** Clic en  organización del home y darle en el botón “Entrar” a la ruta donde se quiere subir o "Subir Material" > Arrastrar PDF > Escribir Título > Confirmar.

**Pasos:**

1. Haga clic sobre la carpeta deseada para entrar en ella.
1. Presione el botón **"Subir Material"** o **"Nuevo Tema"**.
1. Se abrirá una ventana preguntando **"¿Cómo vas a estudiar este tema?"**. Seleccione una opción:
   1. **Opción A: Tengo PDF o imágenes (Digital)**
      1. Seleccione esta opción si tiene diapositivas o lecturas en PDF.
      1. Arrastre el archivo al área indicada.
      1. El sistema procesará el documento (esto puede tomar unos segundos mientras la IA lee y "entiende" el texto).
   1. **Opción B: Solo tengo libro físico (Modo Espejo)**
      1. Seleccione esta opción si estudia con un libro en papel.
      1. El sistema no leerá el libro, pero le permitirá crear preguntas manuales ("Flashcards") y usará el algoritmo para programar cuándo debe volver a responderlas.
   1. **Opción C: Empezar sin material**
      1. Ideal para autoevaluarse sobre conocimientos previos sin basarse en un documento específico.
1. Confirme la acción. Si subió un PDF, recibirá una notificación de **"Material Procesado Exitosamente"** cuando esté listo para practicar.

**Figura MU-5**\
*Pantalla de subida de material* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.005.png)

*Nota. Elaboración propia.*

**Figura MU-6**\
*Mensaje de éxito* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.006.png)

*Nota. Elaboración propia.*
## **5. Mis Materiales**
En esta sección puede administrar todo el contenido que ha subido a la plataforma.

**Funcionalidades:**

- **Vista de Lista:** Vea todos sus documentos con detalles como fecha de subida y estado de procesamiento.
- **Estado del Material:**
  - *Procesando:* La IA está analizando el texto. Espere unos momentos.
  - *Listo:* Ya puede iniciar sesiones de práctica.
  - *Error:* El PDF no era legible (ej. era una imagen escaneada sin texto seleccionable).
- **Acciones:** Use los botones junto a cada material para **Iniciar Práctica**, **Ver Detalles** (preguntas generadas) o **Eliminar** el material si ya no lo necesita.








**Figura MU-7**\
*Lista de materiales* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.007.png)

*Nota. Elaboración propia.*

**Figura MU-8**\
*Eliminación de materiales* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.008.png)

*Nota. Elaboración propia.*






## **6. Sesión de Práctica (Active Recall)**
Esta es la función principal de Recuiva. Aquí es donde ocurre el aprendizaje real.

**Flujo de la Sesión:**

1. **La Pregunta:** El sistema le presentará una pregunta abierta sobre su material. *No verá opciones múltiples*, ya que el objetivo es forzar el recuerdo.
1. **Su Respuesta:**
   1. Piense su respuesta.
   1. Escríbala en el campo de texto (opcional, pero recomendado para mejorar la retención) o díctela si la función de voz está activa.
   1. Haga clic en **"Enviar Respuesta"**.
1. **Validación con IA:**
   1. El sistema comparará su respuesta con el contenido original usando tres capas de análisis (Similitud de Coseno, BM25 y Evaluación LLM).
   1. Recibirá un feedback inmediato: **Correcto**, **Parcialmente Correcto** (con sugerencias de qué le faltó mencionar) o **Incorrecto**.
1. **Autoevaluación (Feedback para el Algoritmo):**
   1. Después de ver la respuesta correcta, deberá calificar qué tan difícil fue recordar la información:
      1. *Fácil:* Lo recordé al instante.
      1. *Medio:* Tuve que pensarlo un poco.
      1. *Difícil:* Me costó mucho o no lo recordé.
   1. *Importante:* Sea honesto en esta calificación, ya que esto determina cuándo volverá a ver esta pregunta.

**Figura MU-9**\
*Vista de pregunta y campo de respuesta* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.009.png)

*Nota. Interfaz de interrogatorio activo.*

**Figura MU-9**\
*Resultado de validación* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.010.png)

*Nota. Feedback inmediato.*
## **7. Repasos Programados (SM-2)**
Algoritmo de repetición espaciada para programar repasos futuros basados en su desempeño.

No necesita preocuparse por agendar sus estudios. Recuiva lo hace por usted.

- **¿Cómo funciona?** Basado en sus calificaciones (Fácil/Medio/Difícil) de las sesiones anteriores, el sistema calcula la "fecha de olvido" probable.
- **La Cola de Repaso:** En el Dashboard o en la sección "Repasos", verá una lista de sesiones pendientes para el día de hoy.
- **Recomendación:** Trate de completar su cola de repasos diariamente para mantener su "Racha" y maximizar la retención.

**Figura MU-10**\
*Lista de repasos programados* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.011.png)

*Nota. Cola de tareas del algoritmo.*

## **8. Mi Perfil**
Gestión de avatar, datos personales y cambio de contraseña.

En esta sección puede personalizar su experiencia en la plataforma.

- **Avatar:** Seleccione un personaje que lo represente.
- **Datos Personales:** Actualice su nombre o información académica.
- **Seguridad:** Cambie su contraseña periódicamente para proteger su cuenta.
- **Preferencias de Estudio:** Ajuste la cantidad de preguntas por sesión o la rigurosidad de la corrección de la IA.

**Figura MU-11**\
*Pantalla Mi Perfil* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.012.png)

*Nota. Configuración de usuario.*
## **9. Cerrar Sesión**
Clic en Avatar > Cerrar Sesión. Recomendado en equipos compartidos.
## **10. Solución de Problemas Comunes**

|**Problema**|**Solución**|
| :- | :- |
|PDF no procesa|Verificar que sea texto seleccionable (no imagen).|
|Respuesta Incorrecta (Falso Negativo)|Escribir respuestas completas y explicativas.|
|No puedo entrar|Verificar contraseña o contactar soporte.|
## **11. Contacto y Soporte**
**Desarrollador:** Abel Jesús Moya Acosta

**Correo:** amoyaa2@upao.edu.pe

**GitHub:** [AbelMoyaCode/recuiva](https://github.com/AbelMoyaCode/recuiva)

Si en caso existieran dudas sobre la técnica de estudio o sobre lo que es Active Recall y saber cómo se realizar las métricas de puntuación de validación semántica, se debe ingresar al apartado inferior del pie de página sea en **“Active Recall”** o **“Validación Semántica”** respectivamente.








**Figura MU-12**\
*Pantalla de explicación de Active Recall* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.013.png)

*Nota. Para la explicación detallada de esta técnica de estudio.*

















**Figura MU-13**\
*Pantalla de explicación de Active Recall* 

![](Aspose.Words.7e72b987-c21e-4aa3-96e5-51c884d7774b.014.png)

*Nota. Para la explicación detallada de esta técnica de estudio.*
## <a name="_heading=h.nxs1yiz4aeis"></a>**9. Cerrar Sesión**
## **Anexo: Índice de Figuras**

|**Código**|**Descripción**|**Ubicación**|
| :- | :- | :- |
|MU-1|Página de inicio|index.html|
|MU-2|Formulario de registro|auth/register|
|MU-3|Inicio de sesión|auth/login|
|MU-4|Dashboard|app/dashboard|
|MU-5|Subida de material|app/upload|
|MU-6|Mensaje de éxito|app/upload|
|MU-7|Lista de materiales|app/materials|
|MU-8|Pregunta práctica|app/practice|
|MU-9|Resultado validación|app/practice|
|MU-10|Repasos|app/reviews|
|MU-11|Perfil|app/profile|
|MU-12|Active Recall|app/active-recall|
|MU-13|Validación Semántica|app/semantic-validator|

**Firma de Acta de Conformidad del documento de Manual de Usuario:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Walter Cueva Chavez**

