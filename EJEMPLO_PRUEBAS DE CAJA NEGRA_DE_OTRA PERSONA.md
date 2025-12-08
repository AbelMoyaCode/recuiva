**UNIVERSIDAD PRIVADA ANTENOR ORREGO**

**FACULTAD DE INGENIERÍA**

**PROGRAMA DE ESTUDIO DE INGENIERÍA DE SISTEMAS E INTELIGENCIA ARTIFICIAL![Imagen relacionada](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.001.png)**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**“AUTOMATIZACIÓN DE PROCESOS PARA LA MUNICIPALIDAD DEL PORVENIR”**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

#### **ALUMNA:** 
#### MARIA ROSA CASTILLO OTINIANO

**DOCENTE:**

`	`WALTER CUEVA CHAVEZ

#### **TRUJILLO – PERÚ**
#### <a name="_heading=h.9eoraxrihoxb"></a>**2025**



**Tipo de prueba a realizar: Pruebas de Funcionalidad**


# **ESCENARIO 1: REGISTRO DE USUARIO**

**Datos de Entrada:**

Registro de nuevo usuario.
# **Entorno:**

Para el registro de un nuevo usuario, se tiene un módulo de registro, en este módulo, se contempló los labels que almacenarán el ingreso para los nombres completos, correo, teléfono, y contraseña del usuario.
# **Parámetros:**

- Label Nombres Completos
- Label Correo
- Label Teléfono
- Label Contraseña
` `PAGE 186
![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.002.png)
# **Respuesta de otros módulos:**

Se llama al módulo de registro del usuario
# **Condiciones iniciales:**
1. Se puso nulo en el label de nombres.
1. Se puso nulo en el label de email.
1. Se puso nulo en el label de contraseña.
1. Se puso una contraseña con 2 caracteres alfanuméricos, sin carácter especial.
1. Se puso una contraseña con 5 caracteres alfanuméricos, sin carácter especial y sin letras mayúsculas.
1. Se puso una contraseña con 5 caracteres alfanuméricos, un carácter especial, sin letra mayúscula.
1. Se puso una contraseña con 5 caracteres alfanuméricos, un carácter especial, con al menos una letra mayúscula.
1. Se puso texto numérico como correo electrónico (ej: 123456).
1. Se puso un correo con 5 caracteres alfanuméricos, un @ y un dominio (ej: user1@gmail.com).
# **Datos de Salida:**

**Resultados entregados:**

- Para la condición 1 (nombres vacíos), la aplicación no permite el ingreso del dato y muestra el mensaje: "El nombre debe tener al menos 3 caracteres y no debe contener números".
- Para la condición 2 (email vacío), la aplicación muestra el mensaje: "Ingrese un correo electrónico y contraseña".
- Para la condición 3 (contraseña vacía), la aplicación muestra el mensaje: "Ingrese un correo electrónico y contraseña".
- Para la condición 4 (contraseña de 2 caracteres, sin carácter especial), la aplicación muestra el mensaje: "La contraseña debe tener al menos 8 caracteres, un número y símbolo especial".
- Para la condición 5 (contraseña de 5 caracteres, sin carácter especial, sin mayúscula), la aplicación muestra el mensaje: "La contraseña debe tener al menos 8 caracteres, un número y símbolo especial".
- Para la condición 6 (contraseña con carácter especial y sin mayúscula), la** aplicación muestra un mensaje de error, ya que no cumple con los 8 caracteres requeridos, aunque contenga un carácter especial.
- Para la condición 7 (contraseña con carácter especial y mayúscula, pero menos de 8 caracteres), la aplicación también muestra el mensaje de error: "La contraseña debe tener al menos 8 caracteres, un número y símbolo especial".
- Para la condición 8 (correo con solo números), la aplicación muestra el mensaje: "El correo no es válido".
- Para la condición 9 (correo con formato válido), la aplicación permite el ingreso del dato y continúa con el flujo de registro normalmente.
# **Estado final de las variables:**

Se adjunta screens de las pruebas:

`	`![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.003.png)

*Ilustración 1: El nombre debe tener al menos 3 caracteres y no debe contener números*


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.004.png)

*Ilustración 2: Ingrese un correo electrónico y contraseña*


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.005.png)

*Ilustración 3: La contraseña debe tener al menos 8 caracteres, un número y símbolo especial.*


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.006.png)

# **Requisitos de configuración para hacer la prueba:**


**Método de Prueba:**
# Se usó el criterio de **partición de equivalencia** para realizar esta prueba funcional, insertando diferentes tipos de caracteres (alfanuméricos, especiales, inválidos y válidos) en los campos del formulario de registro. Se evaluaron las respuestas que entrega la aplicación web ante cada entrada, verificando si se muestra el mensaje de error correspondiente o si permite el registro.
# **Módulos:**
- El módulo de validación local, ubicado en el componente RegistrateComponent, donde se definen funciones como validateNames, validateEmail y validatePassword.
- El componente de vista RegistrateComponent, donde se encuentra el formulario HTML que permite ingresar los datos del usuario.
# **Hardware y Software:**

- Sistema operativo: **Windows 11**
- Navegador web: **Google Chrome**
- Herramientas de desarrollo: **Angular 18** y **PrimeNG**
- Conexión a Internet estable.
- Resolución de pantalla utilizada: 1920x1080 px

**Procedimientos o Herramientas necesarios**

Para la ejecución de esta prueba, se requirió ir al módulo de registro de nuevo usuario en la aplicación, donde se insertó caracteres alfanuméricos y/o caracteres especiales, dependiendo de la situación, se vio la respuesta de la aplicación, viendo si la aplicación responde en determinados casos o si hay contingencia de errores.
# **Dependencias o relación con otros casos de prueba:**
- # Se debe situar en la sección de registro de nuevo usuario
- # Se debe presionar el botón de registro cumplido el llenado respectivo de los inputs
- # Dependiendo de la correcta llena de datos, se registrará un nuevo usuario

# **ESCENARIO 2: LOGIN**

**Datos de Entrada:**

Inicio de sesión de un usuario en la aplicación Municipalidad del Porvenir
# **Entorno:**

Para el inicio de sesión de un usuario, se tiene un módulo de inicio de sesión, en este módulo, se contempló los inputs que recibirán como parámetro el email, y contraseña del usuario.
# **Parámetros:**

- Input Email
- Input Contraseña


# **Respuesta de otros módulos:**
- # Se llama al módulo de autenticación de usuario, que verifica los datos ingresados mediante el servicio authService.login(email, password).
- # En caso de éxito, el módulo de sesión SessionService guarda los datos, y redirige al módulo principal de bienvenida (/welcome).
- # En caso de error (401), se muestra el mensaje "Usuario o contraseña incorrectos".
  #
# **Condiciones iniciales:**
1. Se puso nulo en los inputs de email y contraseña
1. Se puso caracteres numéricos en los inputs de email y contraseña
1. Se puso 5 caracteres alfanuméricos, sin carácter especial y sin letras mayúsculas
1. Se puso 5 caracteres alfanuméricos, un carácter especial, sin letra mayúscula
1. Se puso 5 caracteres alfanuméricos, un carácter especial, con letra mayúscula
1. Se puso un email y contraseña correcto cumpliendo con las normas del login

# **Datos de Salida:**

**Resultados entregados:**

- Para el caso 1 si email y la contraseña están vacíos, se muestra el mensaje “Ingrese un usuario y contraseña”. 
- Para el caso 2 si el email es solo números se muestra el mensaje “Error al intentar login, mensaje: Usuario o contraseña incorrectos”, ya que el email es inválido. 
- Para el caso 4 y 5 si uno de los datos ingresados es inválido muestra un error ya que el backend lo válida. 
- Para el caso 6 como el usuario y credenciales son correctos te redirige a la vista del welcome.

# **Estado final de las variables:**
Se adjunta screens de las pruebas:


# ![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.007.png)
*Ilustración 4: Correo Inválido*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.008.png)

*Ilustración 5: Ingrese un usuario y contraseña.*




# **Requisitos de configuración para hacer la prueba:**
**Método de Prueba:**
# Se utilizó la técnica de **partición de equivalencia** para agrupar valores válidos e inválidos de entrada. Se probaron múltiples combinaciones de email y contraseña directamente desde el formulario de login
# **Módulos:**
- LoginComponent**:** Controlador que captura datos del formulario y ejecuta la autenticación.
- SessionService**:** Guarda la sesión en caso de éxito.
- Formulario** HTML**:** Captura los datos desde el usuario.
# **Hardware y Software:**
- Navegador: **Google Chrome** 
- Sistema operativo: **Windows 11**
- Framework: **Angular v18**
- Librerías UI: **PrimeNG**, **PrimeFlex**
- Backend: **Nodejs + MongoDB**
- Conexión a Internet estable
- Resolución de pantalla: 1920x1080 px

# **Procedimientos o herramientas necesarios:**
Para la ejecución de esta prueba, se requirió ir al módulo de inicio de sesión del usuario en la aplicación, donde se insertó caracteres alfanuméricos y/o caracteres especiales también ingresando valores nulos, dependiendo de la situación, se vio la respuesta de la aplicación, viendo si la aplicación responde en determinados casos o si hay contingencia de errores.
# **Dependencias o relación con otros casos de prueba:**
- Se debe situar en la vista inicial, la de inicio de sesión del usuario
- Se debe presionar el botón de iniciar sesión cumplido el llenado respectivo de los inputs.
- Dependiendo de la correcta llena de datos, iniciará sesión el usuario o no.

# **ESCENARIO 3: MÓDULO DIVORCIOS**

**Datos de Entrada:**

`	`**Entorno:**

En el módulo de divorcios, para crear un registro, el usuario debe de ingresar la información necesaria de él y de su esposa.
# **Parámetros:**
- Roles del sistema:
  - Usuario Administrador
  - Usuario Normal
- Información registrada por el usuario:\
  ● Datos del solicitante (DNI, nombres, correo, celular, dirección)\
  ● Datos del cónyuge (DNI, nombres, correo, celular)\
  ● Información del matrimonio (fecha, municipalidad, distrito)\
  ● Recibo de pago (imagen de Yape)

# **Respuesta de otros módulos:**
Se utiliza la lógica del backend implementada en **Node.js**, donde:

- Se usa Multer para recibir la imagen del recibo de Yape.
- Se extrae texto del recibo usando **Tesseract.js** (OCR) para obtener: número de operación, nombre, monto y hora.
- La información extraída se guarda automáticamente en la base de datos.
- Se configura un cron job (node-cron) que:
  - Envía un **correo electrónico** al usuario los primeros 4 días a las 9 de am después de aprobar la solicitud.
  - Envía un **mensaje de WhatsApp (Twilio)** el 5° día

# **Condiciones iniciales:**
1. Usuario normal intenta registrar una solicitud sin completar uno o más campos requeridos.
1. Usuario normal completa todos los campos, pero no sube el recibo Yape, por lo tanto, el administrador no aprueba la solicitud.
1. Usuario normal completa todo, pero sube una imagen no legible (OCR falla).
1. Usuario normal registra correctamente toda la solicitud (datos + recibo Yape).
1. Usuario administrador accede al CRUD y aprueba una solicitud en estado “En proceso”.
1. Cron job ejecuta envío de correos en los días 1, 2, 3 y 4 tras la aprobación.
1. Cron job ejecuta envío de mensaje por WhatsApp en el día 5 tras la aprobación.
1. El usuario puede editar la información de su registro, después de haberlo creado.
1. Usuario intenta ingresar una solicitud duplicada (mismo DNI y matrimonio) → Falla esperada.
# **Datos de Salida:**

**Resultados entregados:**

Para el primer caso, cuando un usuario normal intenta registrar una solicitud sin completar uno o más campos requeridos, la aplicación impide el registro y muestra mensajes de validación indicando los campos obligatorios que faltan.

En el segundo caso, al completar todos los campos del formulario, pero no adjuntar el recibo de Yape, el administrador no llega a aprobar la solicitud por falta de pago.

En el tercer caso, cuando el usuario carga una imagen legible del recibo, el sistema intenta extraer los datos usando OCR (Tesseract.js), pero al no reconocer los campos necesarios, el sistema no extrae ningún dato y queda como vacío. 

Para el cuarto caso, al completar correctamente todos los datos requeridos y subir una imagen legible del recibo Yape, el sistema registra exitosamente la solicitud, la guarda en la base de datos con estado "En proceso" y extrae correctamente el número de operación, monto, nombre y hora desde la imagen del recibo.

En el quinto caso, el usuario administrador accede al sistema, revisa la solicitud y al aprobar, esta cambia su estado de “En proceso” a “Aprobado”, activando automáticamente la programación de envío de notificaciones por cron.

En el sexto caso, a partir de la aprobación, el cron job configurado envía automáticamente correos electrónicos al solicitante en los días 1, 2, 3 y 4 a la 9 am. Los envíos se realizaron correctamente utilizando el servicio de SendGrid y se verificaron en los registros del sistema.

En el séptimo caso, el quinto día posterior a la aprobación, el cron job envía un mensaje de WhatsApp al número de celular del solicitante y conyuge utilizando la API de Twilio. La entrega del mensaje fue exitosa y se reflejó en los logs.

Para el octavo caso, el usuario administrador elimina una solicitud en estado "En proceso", y el sistema permite la eliminación correctamente, mostrando un mensaje de confirmación.

Finalmente, en el noveno caso, cuando un usuario intenta registrar una solicitud duplicada (es decir, misma combinación de DNI del solicitante y fecha de matrimonio), el sistema detecta la duplicidad y bloquea la operación, mostrando un mensaje informativo indicando que la solicitud ya fue registrada previamente.
# **Estado final de las variables:**

Se adjunta screens de las pruebas:
# ![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.009.png)
*Ilustración 6: Se intenta registrar un nuevo usuario, pero es necesario completar todos los campos para que se habilite el botón de Guardar.*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.010.png)

*Ilustración 7: Sube una imagen que no es de YAPE y el OCR no captura los datos.*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.011.png)

*Ilustración 8: Al no capturar los datos no se extrae nada y quedan nulos.*
#
# ![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.012.png)
*Ilustración 9: Usuario administrador accede al CRUD y aprueba una solicitud en estado “En proceso”.*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.013.png)

*Ilustración 10: Cron job ejecuta envío de correos en los días 1, 2, 3 y 4 tras la aprobación.*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.014.jpeg)

*Ilustración 11: Cron job ejecuta envío de mensaje WhatsApp en el día 5 tras la aprobación*
#
# ![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.015.png)
*Ilustración 12: El sistema permite editar correctamente la información.*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.016.png)

*Ilustración 13: Usuario intenta ingresar una solicitud duplicada (mismo DNI y matrimonio) → Falla esperada.*
# **Requisitos de configuración para hacer la prueba:**
# **Método de Prueba:**
# Se aplicó partición de equivalencia y análisis de valores límites para evaluar entradas válidas e inválidas. También se evaluó la lógica temporal del cron jobs (node-cron) mediante pruebas simuladas de fechas.

**Módulos:**

- Frontend** Angular: Formulario de solicitud con validaciones de campos requeridos y carga del recibo Yape.
- Backend** Node.js/Express:
- Controladores de solicitudes
- OCR con tesseract.js
- Envío de correo con @sendgrid/mail y nodemailer
- Envío de WhatsApp con twilio
- Tareas programadas con node-cron
- Base** de Datos: MongoDB gestionado con mongoose.
# **Hardware y Software:**
- Navegador: Google Chrome
- Sistema operativo: Windows 11
- Backend: Node.js 18+, Express
- OCR: tesseract.js
- Cron: node-cron
- Mensajería: twilio, @sendgrid/mail
- Base de datos: MongoDB Atlas
- Herramientas adicionales: Postman, DevTools
# **Procedimientos o herramientas necesarios:**
- Acceder al sistema como usuario normal y registrar una solicitud con los campos requeridos.
- Adjuntar imagen Yape y enviar formulario.
- Revisar la base de datos y verificar si se extrajo la información correctamente.
- Iniciar sesión como administrador, acceder al módulo de solicitudes y aprobarla.
- Simular paso del tiempo o esperar ejecución del cron job.
- Verificar el envío de correos (SendGrid) y mensajes (Twilio).
- Validar acciones restringidas por rol.
# **Dependencias o relación con otros casos de prueba:**
- Relacionado con módulos de autenticación **y** roles del sistema.
- Depende del correcto funcionamiento de los servicios externos: OCR, correo y Twilio.
- Se integra con el módulo de usuarios registrados y logs de auditoría.


# **ESCENARIO 4: MODULO LICENCIAS** 

**Datos de Entrada:**

# **Parámetros:**
**Campos del formulario de solicitud:**\
● Razón social\
● RUC\
● Representante\
● DNI del representante\
● Dirección\
● Giro de negocio\
● Teléfono\
● Correo\
● Observaciones\
● Recibo de pago (imagen)
=======================================
# **Automatizaciones backend:**
● Generación de PDF de compromiso con datos del permiso\
● Envío de PDF por correo con nodemailer con todos los detalles\
● Envío de recordatorios por correo y WhatsApp si no se registra pago en 3 días
===============================================================================
# **Respuesta de otros módulos:**
# Se llama al módulo de **Visualización y Gestión de Licencias**, el cual permite al usuario consultar el estado actual de su solicitud, descargar el PDF generado con el compromiso de pago y visualizar el código QR para realizar el pago correspondiente. Asimismo, en este módulo se refleja si el pago fue validado, rechazado o sigue pendiente, permitiendo una trazabilidad clara del proceso.
# **Condiciones iniciales:**
1. Usuario envía formulario sin completar campos obligatorios.
1. Usuario completa todos los campos, pero no adjunta recibo, por lo tanto, el administrador no lo aprueba.
1. Usuario completa todo, pero el sistema falla al calcular el costo.
1. El Usuario registra correctamente toda la solicitud (formulario + recibo).
1. Cron job genera el PDF y lo envía por correo el mismo día.
1. Al tercer día sin pago, se reenvía correo y mensaje por WhatsApp.
1. Usuario ve estado actualizado del permiso desde el frontend.
1. El usuario puede editar correctamente su registro después de haberlo creado.
1. El sistema no permite editar una solicitud ya aprobada.
# **Datos de Salida:**

**Resultados entregados:**

Dependiendo del escenario, para el primer escenario, cuando se ingresó al detalle del dato, en este caso “Peso”, se observó que no hay datos ni gráfica, pero no manda ningún mensaje de error o alerta diciendo que no hay datos.

Para el segundo escenario, se observó que al ingresar al módulo del detalle de “Comidas Consumidas” no se muestran datos y la aplicación no manda un mensaje o alerta notificando que no aceptamos los permisos.

Para el tercer escenario, se observó, al ingresar al módulo “Calorías Quemadas”, se pudo ver la correcta información llena de datos, con la generación del gráfico y la interpretación necesaria.
# **Estado final de las variables:**

Se adjunta screens de las pruebas:


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.017.png)

*Ilustración 14: El sistema no permite registrar si no se completan los campos obligatorios.*


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.018.png)

*Ilustración 15: El sistema envía el correo indicando el pago y fecha límite.*


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.019.png)

*Ilustración 16: El sistema envía un PDF indicando el costo el base al aforo de las personas.*


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.020.png)

*Ilustración 17: El usuario puede editar la información del registro sin problema*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.021.png)

*Ilustración 18: El usuario no puede editar un registro que ya ha sido aprobado.*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.022.png)

*Ilustración 19: El usuario ve aprobado su registro desde el frontend.*
# **Requisitos de configuración para hacer la prueba:**

**Método de Prueba:**

Se utilizó la técnica de partición de equivalencia y análisis de condiciones temporales, simulando distintos escenarios de solicitud de licencias, incluyendo los estados iniciales, envío correcto del formulario, adjuntos válidos y observación del comportamiento del sistema en días posteriores a la aprobación.

La prueba también incluyó la verificación de automatizaciones tales como generación de PDF, envío de correo por Gmail y recordatorios mediante WhatsApp usando Twilio. Se analizaron los casos en los que se realiza o no el pago dentro del plazo estimado de 3 días, y el sistema actúa en consecuencia.
# **Módulos:**
Para esta prueba se utilizó el módulo de Licencias, desarrollado en el backend con Node.js. Las funcionalidades probadas incluyen:

- Validaciones del formulario en frontend Angular.
- Carga de recibo mediante multer.
- Generación del documento PDF de compromiso con pdfkit.
- Envío automático de correos electrónicos mediante nodemailer usando cuenta Gmail.
- Envío de notificaciones al WhatsApp del solicitante mediante la API de Twilio.
- Cálculo automático del costo del permiso.
- Ejecución automática de tareas programadas con node-cron.

Se usó la base de datos MongoDB para validar el almacenamiento y actualización de los datos de la solicitud (permisos).
# **Hardware y Software:**
Para la realización de la prueba se utilizaron los siguientes entornos y herramientas:

- **Navegador:** Google Chrome
- **Sistema Operativo:** Windows 10 y Ubuntu 22.04
- **Backend:** Node.js 18 con Express.js
- **Frontend:** Angular versión 18
- **Base de datos:** MongoDB
- **Correo electrónico:** Cuenta Gmail conectada vía SMTP con nodemailer
- **Mensajería:** API de Twilio para mensajes WhatsApp
- **Generación de documentos:** Librería pdfkit para PDF con código QR integrado
- **Tareas programadas:** node-cron ejecutando recordatorios diarios
- **Dependencias adicionales:** dotenv, mongoose, multer, axios
# **Procedimientos o herramientas necesarios:**

Para la ejecución de esta prueba, fue necesario completar el formulario (todos los campos), y después enviar el administrador es quien aprueba el registro e valida que el pdf con los detalles llegué al correo del solicitante.
# **Dependencias o relación con otros casos de prueba:**
- Requiere que el **usuario esté autenticado**, por lo tanto, depende del módulo de Login.
- Depende de que el correo del solicitante sea válido para recibir el PDF.
- Depende de la correcta ejecución del cron para los recordatorios (relación con el módulo de tareas programadas).
- Se relaciona con el **módulo de administración**, ya que el estado del permiso se actualiza por un administrador.


# **ESCENARIO 5: MÓDULO PERMISOS**

**Datos de Entrada:**
# **Parámetros:**
**Campos del formulario de solicitud:**\
● Tipo de Evento\
● Fecha\
● Lugar\
● Horario\
● Aforo
=======================================
# **Automatizaciones backend:**
● Generación de PDF de compromiso con datos del permiso\
● Envío de PDF por correo con nodemailer\
● Envío de recordatorios por correo y WhatsApp si no se registra pago en 4 días\
● Inclusión de QR de pago en el correo PDF**\
● Cálculo del costo total según el aforo
===============================================================================
# **Entorno:**
# Para que el usuario pueda solicitar un permiso de alquiler de un local debe de llenar todos los campos del formulario y además realizar el pago correspondiente dependiendo del aforo.
# **Respuesta de otros módulos:**
# Se llama al módulo de **Visualización y Gestión de Permisos**, el cual permite al usuario consultar el estado actual de su solicitud, descargar el PDF generado con el compromiso de pago y visualizar el código QR para realizar el pago correspondiente. Asimismo, en este módulo se refleja si el pago fue validado, rechazado o sigue pendiente, permitiendo una trazabilidad clara del proceso.
# **Condiciones iniciales:**
1. No se permite el registro de eventos con la misma fecha y hora exacta.\
   Por ejemplo, si ya existe un evento el 25/05/2025 a las 4:00 PM, no se puede registrar otro evento a esa misma hora, pero sí a las 5:00 PM.
1. El costo del permiso se calcula automáticamente según el valor del aforo ingresado.
1. Solo el administrador** tiene acceso para cambiar el estado de una solicitud a “Aprobado”.
1. Se genera un PDF con los detalles del evento 
1. Si en los primeros 4 días no se adjunta un comprobante de pago, se envía un correo recordatorio diario**.**
1. Si después de 5 días aún no se realiza el pago, se envía un mensaje de advertencia por WhatsApp**.**

# **Datos de Salida:**

**Resultados entregados:**

0. En el caso de la condición 1, el sistema valida que no se registre una solicitud en la misma fecha y misma hora, solo permite si la diferencia de hora es mayor a 1 hora. 
0. En el caso de la condición 2 el sistema válido que si el aforo es mayor a 100 personas le aumenta 50 soles al precio base que es 50, si es mayor a 200 personas le aumenta 50 soles más. 
0. En el caso de la condición 3, el sistema valida los roles, solo el administrador tiene habilitado el botón de aprobar la solicitud. 
0. En el caso de la condición 4, el sistema envía el PDF con los detalles del permiso y además con un código QR para que pueda realizar el pago el usuario.
0. En el caso de la condición 5 el sistema envía el pdf al correo del solicitante, esto durante los primeros 4 días.
0. En el caso de la condición 6 el sistema envía un mensaje al WhatsApp indicando que tiene pendiente un pago por cancelar correspondiente al permiso que ha solicitado.
# **Estado final de las variables:**

Se adjunta screens de las pruebas:

`		`![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.023.png)

*Ilustración 20: El sistema no permite el registro de eventos con la misma fecha y hora exacta*

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.024.png)

*Ilustración 21: El sistema envia el pdf con los detalles sobre el permiso y el monto a cancelar.*


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.025.png)

*Ilustración 22: Solo el administrador tiene permiso de aprobar la solicitud del permiso.*

# **Requisitos de configuración para hacer la prueba:**

**Método de Prueba:**

Se empleó la técnica de** análisis de decisiones combinada con pruebas de frontera, evaluando:

- El correcto funcionamiento de las validaciones (campos requeridos y colisión de horarios).
- La correcta generación del PDF 
- El flujo automatizado de recordatorios por correo y mensajería.
- El rol del administrador como única entidad habilitada para aprobar solicitudes.

Se simularon escenarios donde se intenta registrar permisos con datos válidos e inválidos, así como verificaciones temporales simulando el paso de los días para activar las tareas programadas y además simulando cruces de permisos.
# **Módulos:**
# Para esta prueba se usaron las rutas y controladores del módulo de permisos en Node.js, desarrollados con Express. El cálculo del costo se realiza directamente en los servicios del backend según el aforo ingresado. Para la generación del PDF se usan las librerías pdfkit respectivamente. Además, se emplean los servicios de nodemailer para el envío de correos electrónicos y twilio para el envío de mensajes por WhatsApp. Las tareas programadas fueron configuradas mediante node-cron, y todos los datos son almacenados y validados en MongoDB con Mongoose.
# **Hardware y Software:**
- **Sistema operativo:** Windows 11
- **Navegador:** Google Chrome 
- **Frontend:** Angular v18
- **Backend:** Node.js v18
- **Base de datos:** MongoDB
- **Correo:** Cuenta Gmail autenticada vía SMTP (nodemailer)
- **Mensajería:** WhatsApp vía Twilio API
- **Automatización:** node-cron
- **Librerías clave:** pdfkit, multer, qrcode, twilio, nodemailer, mongoose, dotenv
# **Procedimientos o herramientas necesarios:**

# Para la ejecución de estas pruebas, se requirió ir al módulo de Permisos y allí, el usuario completa los datos requeridos (tipo de evento, fecha, lugar, horario, aforo y adjunto del recibo de pago), luego pulsa en el botón para registrar la solicitud. Posteriormente, un administrador inicia sesión, accede al panel de solicitudes y aprueba una de ellas, lo cual desencadena el envío del PDF al correo. Finalmente, se simula el paso del tiempo para verificar el envío automático de recordatorios al correo y al WhatsApp del usuario si no se registra el pago.
# **Dependencias o relación con otros casos de prueba:**
- Requiere inicio de sesión: relacionado con el módulo de autenticación.
- Requiere rol administrador para aprobar solicitudes
- Se apoya en módulo de cron para la automatización.
- Conecta con servicios externos como Gmail (correo) y Twilio (WhatsApp).
# **ESCENARIO 6: MÓDULO RENTAS** 

**Datos de Entrada:**

Vista Editar Perfil del paciente
# **Entorno:**

Para que el paciente pueda actualizar sus datos como su nombre, apellido y/o foto de perfil, requiere que en los labels respectivos se pueda poner los datos que el paciente necesite, estos datos se pasan a la base de datos local y a firebase mediante los servicios solicitados por la aplicación.
# **Parámetros:**

0. Label del nombre del usuario
0. Label del apellido del usuario
0. Ullmage View con la foto de perfil del usuario
# **Respuesta de otros módulos:**

Se llama al módulo de editar perfil del usuario
# **Condiciones iniciales:**

1. Se puso nulo en los labels de nombre y apellido
1. Se puso caracteres numéricos labels de nombre y apellidos
1. Se puso con 2 caracteres alfanuméricos en el label de nombre y apellido, ningún carácter especial
1. No se seleccionó alguna imagen para la foto de perfil
1. Se seleccionó la opción de ir a galería, en la foto de perfil
1. Se seleccionó la cámara, para agregar una nueva foto de perfil
# **Datos de Salida: Resultados entregados:**
0. Para las opciones 1 y 2, la aplicación no permite el ingreso del dato y muestra un mensaje de error.
0. Para la opción 3, la aplicación permite el ingreso del nuevo dato, lo actualiza y muestra la información actualizada.
0. Para la opción 4, la aplicación muestra una imagen predeterminada.
0. Para las opciones 5 y 6, la aplicación nos manda a la galería para seleccionar la imagen que queramos, la guarda, pero no manda mensaje de confirmación.
# **Estado final de las variables:**

Se adjunta screens de las pruebas:














llustración: Ventana para editar perfil del paciente

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.026.jpeg)

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.027.jpeg)

Fuente: inHealth
# **Requisitos de configuración para hacer la prueba:**

**Método de Prueba:**

Se usó la partición de equivalencia para la realización de esta primera prueba, donde se insertó diferentes tipos de caracteres en diferentes situaciones, se contempló las diferentes respuestas de la aplicación móvil.




# **Módulos:**

Para esta prueba se usaron los View Controllers de editar perfil y el servicio de Firebase para poder guardar y/o actualizar los datos que sean necesarios.
# **Hardware y Software:**

Para la realización de la prueba, se usó un celular iPhone con conexión a internet.

iOS mínimo requerido por la aplicación: iOS 12.

iPhone mínimo requerido por la aplicación: desde el iPhone 5s en adelante.
# **Procedimientos o herramientas necesarios:**

Para la ejecución de esta prueba, se requirió ir al módulo perfil del paciente, donde pulsando el botón superior derecho, mostramos una nueva interfaz donde se puede observar nuestros datos como el nombre, apellido y foto de perfil. Tenemos la opción de cambiar esos datos y la foto, después de modificarlas, se hace clic en el botón superior derecho “Guardar Datos” para que se actualice y se muestran en el perfil.
# **Dependencias o relación con otros casos de prueba:**

El paciente se debe situar en la pestaña de editar perfil haciendo clic en el botón superior derecho de su perfil

Se deben cambiar los datos que quiera y hacer clic en el botón “Guardar Datos” para actualizarlos

Dependiendo del cambio de datos que el paciente realice, se refleja en el perfil con sus nuevos datos.

# **Escenario 7:**

**Datos de Entrada:**

Creación de una nueva cita médica
# **Entorno:**

Para poder generar una nueva cita médica, se debe ir al módulo de creación de cita médica, accediendo desde el módulo de citas médicas, donde se selecciona una fecha y se prosigue la guía que la aplicación le da al paciente para poder seguir con la creación de la cita, seleccionando al médico, la hora y añadiendo notas, para finalizar con un mensaje de creación de la cita y viendo el detalle de la misma.
# **Parámetros:**
- Selección de la fecha
- Selección del médico
- Selección de la hora
- Label de la nota que acompaña la cita
# **Respuesta de otros módulos:**

Se llama al módulo Citas médicas, donde se abre el calendario respectivo, para acceder al módulo de generación de citas, se selecciona en la parte superior derecha el signo (+), que genera un llamado al módulo de creación de la cita.
# **Condiciones iniciales:**

1. Se seleccionó una fecha anterior a la actual
1. No se seleccionó un médico
1. Se seleccionó una fecha actual y un médico, no se agregó una nota
1. Se agregó una nota y una hora
# **Datos de Salida:**

**Resultados entregados:**

Para el primer caso, se siguió el flujo de creación de citas, pero no se guardó la cita en la fecha anterior seleccionada y no se mandó ninguna alerta o modal que refiera a ese error.

Dentro del segundo caso, simplemente al querer llegar a la vista donde se guarda un texto con las notas y la selección de la hora, la aplicación sufre un crash y se cierra inesperadamente.

Para el tercer caso, se crea la cita y se puede visualizar, en el detalle de la cita, se ve en la sección de agregar nota, un texto predeterminado, para contener el error de no escribir una nota.

Para el último caso, se crea la nota correctamente y se ve un mensaje de creación de la nota.
# **Estado final de las variables:**
Se adjunta screens de las pruebas:

Ilustración: Ventana de Citas Médicas para la aplicación inHealth


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.028.jpeg)![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.029.jpeg)

Fuente: inHealth
# **Requisitos de configuración para hacer la prueba:**

**Método de Prueba:**

Se usó la técnica de decisiones, donde se partió de la situación donde vemos si seleccionamos o no un médico, si seleccionamos o no una fecha correcta o futura, donde agregamos una nota o no, dependiendo de la situación se ve que la aplicación responde, pero muestra fallo de crash y se cierra inesperadamente la aplicación cuando no se selecciona un médico, a la vez no se ve los modales respectivos de errores, pero si se ve el modal de creación de la aplicación.
# **Módulos:**

Para esta prueba se usó el módulo del controlador de creación de una cita médica, a la vez se requiere del servicio de firebase para la creación de la cita médica.
# **Hardware y Software:**
Para la realización de la prueba, se usó un celular iPhone con conexión a internet.

iOS mínimo requerido por la aplicación: iOS 12.

iPhone mínimo requerido por la aplicación: desde el iPhone 5s en adelante.
# **Procedimientos o herramientas necesarios:**

Para la ejecución de esta prueba, se requirió que ya se cuente con un médico asociado, para poder crear la cita agendando con el médico seleccionado, además se requiere seguir el flujo de creación de citas explicado en la aplicación.
# **Dependencias o relación con otros casos de prueba:**


médica.

Se debe de tener asociado a su cuenta, un médico para poder crear la cita

Se debe seguir con la secuencia de creación de la cita, explicada anteriormente.

Dependiendo de la creación de la cita, se podrá ver la cita en el día seleccionado y ver el detalle de la misma.




# **Escenario 8:**

**Datos de Entrada:**

Tener habilitado el Game Center en el móvil
# **Entorno:**

Para poder acceder a los módulos de gamificación (Logros y Tabla de puntuaciones), dentro de la aplicación, se necesita previamente haber accedido y configurado el Game Center en el iPhone.
# **Parámetros:**
- Acceder al módulo de logros en el apartado desafíos.
- Acceder al módulo tabla de puntuación en el apartado desafíos.
# **Respuesta de otros módulos:**

Se llama al módulo GameKit Service, donde se contempla los métodos de acceso al Game Center del usuario, para poder inicializar las demás clases en los controladores de los desafíos.
# **Condiciones iniciales:**

1. Se habilitó el acceso de Game Center a la aplicación y se seleccionó el módulo de logros
1. Se inhabilitó el acceso de Game Center a la aplicación y se seleccionó el módulo tabla de puntuación
1. Se habilitó el acceso de Game Center a la aplicación y se seleccionó el módulo tabla de puntuación.
1. Se inhabilitó el acceso de Game Center a la aplicación y se seleccionó el módulo Logros
# **Datos de Salida:**

**Resultados entregados:**

Luego de establecidos los casos - condiciones iniciales, se declara que, en los casos 1 y 3 logran pasar satisfactoriamente al módulo especificado, mostrando al principio, cuando se inicia la aplicación un banner alerta dando un mensaje de bienvenida, que se inició el Game Center en la aplicación, por el contrario para los casos 2 y 4 al restringir el acceso al Game Center en la aplicación y querer acceder a un módulo establecidos en esos casos, nos aparece un modal de alerta diciendo que el usuario no sé auténtico con Game Center, por lo que no puede ver los módulos respectivos.
# **Estado final de las variables:**

Se adjunta screens de las pruebas:

Ilustración: Ventana de Desafíos para la aplicación inHealth

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.030.jpeg)

Fuente: inHealth
# **Requisitos de configuración para hacer la prueba:**

**Método de Prueba:**

Se usó la técnica de decisiones, donde se partió de dos opciones, una sabiendo que la aplicación tiene acceso al Game Center, pues este está habilitado por el usuario y el otro escenario donde no se tiene acceso, dado en los primeros escenarios, se logra ver el acceso al Game Center mediante los logros o la tabla de puntuación, pero al no tener acceso se muestra un modal diciendo que el usuario no está logueado en Game Center por lo que no puede acceder al módulo específico.
# **Módulos:**

Para esta prueba se usó la clase servicio de Game Center, para poder ver si el usuario se autenticó con el servicio, además de los controladores necesarios para las vistas de Desafíos dentro de la aplicación.
# **Hardware y Software:**
Para la realización de la prueba, se usó un celular iPhone con conexión a internet.

iOS mínimo requerido por la aplicación: iOS 12.

iPhone mínimo requerido por la aplicación: desde el iPhone 5s en adelante.
# **Procedimientos o herramientas necesarios:**

Para la ejecución de esta prueba, se requirió que el usuario habilite el Game Center dentro de su iPhone para poder así acceder a los módulos y seguir con las pruebas especificadas anteriormente.
# **Dependencias o relación con otros casos de prueba:**

Se debe de iniciar sesión y habilitar el Game Center previamente.

Se debe dirigir al apartado de desafíos y así seleccionar logros o tabla de puntuación según parezca.

Dependiendo de la opción, seguirá el flujo, ya sea en la vista de logros o en la vista de tabla de puntuación.
# **Listado técnico:**

**Archivos Involucrados:**

Se usaron los servicios establecidos en el proyecto tales como servicios de autenticación de firebase, servicios de generación de la base de datos en firebase, servicio de permisos de healthkit, servicios de GameKit, servicios de selección de datos de healthkit, las clases modelos, los controladores de las vistas involucradas, la clase útil para las validaciones y/o métodos que ayudaron al formateo de diferentes elementos en la aplicación, los controladores de las tablas creadas, el storyboard y el launch board.
# **Sistemas y Bibliotecas:**

Entre las librerías externas podemos listas las siguientes:

- Firebase (Auth, Database, Storage, Analytic, Messaging)
- JTAppleCalendar











# **Errores:**
- Keyboard
- Charts
- RealSwift
- Floating Panel
- HealthKit
- GameKit
- Push Notifications
































# **Notas:**
- Al momento de que el paciente se registra en la aplicación ingresando su nombre, apellido, correo y contraseña; en caso que en el label del nombre y apellido se ingrese valores numéricos u otros valores no aceptados. No hay mensajes de error que le indiquen al paciente que los datos ingresados son incorrectos.
- Los labels de nombre y apellido no están validados para que acepten sólo valores de texto.
- Al momento que el paciente quiere agregar a su médico, ya sea en el mismo módulo de doctores o por medio del escaneo de su código QR, no hay un mensaje de confirmación que le diga al paciente que lo registró correctamente, por lo que se tiene que ir hasta el módulo de médicos para poder verificarlo.
- Cuando el paciente entra a su perfil puede observar todos sus datos médicos donde cada uno tiene un detalle, información general y un gráfico estadístico. En caso que uno de esos datos no tenga su gráfico o le falta algún parámetro, no hay algún mensaje de error o alerta que avisen al desarrollador que existe ese problema.
- Al momento que el paciente ingresa al módulo de citas e intenta agendar una con un médico en específico, la aplicación sufre crasheos momentáneos y se cierra abruptamente.
- Al momento del registro y/o inicio de sesión, se podría agregar un botón que permita ver que la contraseña ingresada oculta sea la correcta.
- En el módulo de citas, al momento de observar la lista de mis citas registradas se consideraría visualizar un calendario mensual general, con el que no se tenga que hacer swipe por cada semana individualmente.
- En el módulo de desafíos, se consideraría agregar planes de dietas y ejercicios que ayude a los pacientes a mejorar su estilo de vida.



**Anexo 10: Documentos de Heurísticas de Nielsen**

1. **Metodología**

1. **Comparación entre Usabilidad y Experiencia del usuario**

Cuando hablamos de Usabilidad, podemos referenciar al grado en que un producto puede ser usado para conseguir metas específicas con efectividad y eficiencia, es por eso que, como un objetivo, la Usabilidad es conseguir que la aplicación o herramienta web sea fácil de utilizar.

Por otro lado, nos referimos a experiencia de usuario nos enfocamos en la satisfacción conseguida en el usuario durante su interacción con la aplicación móvil o herramienta web.
1. # **Métodos de evaluación de usabilidad**

El método para la evaluación de usabilidad es un procedimiento sistemático para grabar datos relacionados con la interacción del usuario final con un producto software o sistema. Los datos recolectados son analizados y evaluados para determinar la usabilidad del producto.
1. # **Pruebas de usabilidad**

Según IDF (Interaction Design Foundation), afirma que las pruebas de usabilidad se definen como la práctica de probar lo fácil que un diseño es

usar en un grupo de usuarios representativos. Por lo general, implica observar a los usuarios cuando intentan completar las tareas y pueden realizarse para diferentes tipos de diseños, desde interfaces de usuario hasta productos físicos. Por lo general se realizan de manera constante, desde el desarrollo inicial hasta la liberación de un producto.

Podemos mencionar los diferentes métodos, tales como:

- **Ordenamiento de Tarjetas:** Cuando hablamos de Ordenamiento de Tarjetas, nos centramos en el agrupamiento y ordenamiento de tarjetas las cuales poseen conceptos generales y específicos del sistema, con el objetivo de encontrar los patrones necesarios para determinar la forma de las acciones o contenido que el usuario espera ver en la interfaz.
- **Pensamiento en voz alta:** En este tipo de prueba se le solicita al usuario que exprese en voz alta sus pensamientos, emociones, sensaciones y opiniones de cada acción que realiza.
- **Co-descubrimiento:** Participan dos usuarios en la prueba de usabilidad, los cuales deben realizar ciertas acciones diseñadas por los expertos, con el objetivo de encontrar y comentar problemas en voz alta de un sistema dado.
- **Pruebas en Papel:** Consiste en evaluar una interfaz de usuario mediante modelos mostrados en papel para que este determine si cumple o no las necesidades reales de él como usuario del sistema.
  1. # **Evaluación Heurística**

La evaluación Heurística es la ciencia del descubrimiento y el conjunto de principios que sigue un experto para realizar una investigación. Referentemente, en el ámbito de Ciencias de la Computación, las evaluaciones heurísticas consisten en un análisis técnico que busca

identificar los errores de usabilidad y mostrar oportunidades de optimización.

Estas pruebas son una forma eficiente y accesible de asegurar la usabilidad de una interfaz, permitiendo encontrar hasta un 80% de los errores más frecuentes por medio de una serie de verificaciones y consecuciones de objetivos.

Gracias a estas pruebas podemos medir:

- El éxito de las tareas
- Tiempo de las tareas
- Errores
- Satisfacción subjetiva

A continuación, se presenta la escala de frecuencia y severidad:

|Frecuencia|Severidad|
| :- | :- |
|(4) >90%|(4) Catastrófico|
|(3) 51-90%|(3) Mayor|
|(2) 11-50%|(2) Menor|
|(1) 1-10%|(1) Cosmético|
|(0) 0%|(0)	No	es	un problema|


1. # **Interpretación de las escalas de Frecuencia y Severidad**

De esta tabla, podemos sacar lo siguiente:

**Severidad**: Siendo esta, el nivel de gravedad del problema identificado. Gracias a la severidad podemos identificar problemas más peligrosos, que comprometen la usabilidad del sistema.

**Frecuencia**: Se refiere al grado de ocurrencia del problema identificado. Con esto, es posible saber qué tan habitual o repetido es el problema dentro del sistema.

**Criticidad**: Es la suma de la severidad más la frecuencia. Con esto, es posible determinar qué problemas son más críticos o cruciales, que ameritan una solución más rápida, pues involucran aún más la usabilidad del sistema, comparados con otros.


1. # **Principios Heurísticos**

A continuación, se mencionan los principios Heurísticos de Nielsen:

1. **Visibilidad del estado del sistema:** ¿El usuario sabe qué está pasando? El sistema SIEMPRE debe informar al usuario de lo que está haciendo, es decir, proveer feedback en un tiempo razonable.
1. **Conexión entre el sistema y mundo real:** El sistema y el usuario tienen que hablar en el mismo idioma, siguiendo las convenciones del entorno del usuario.
1. **Uso y control de usuario:** Tener sensación de control y no tener miedo de efectuar acciones y probar cosas nuevas, es de vital importancia para que la persona interactúe y aprenda por sí misma.
1. **Consistencia y estándares:** Es muy importante tener consistencia a lo largo de todo el sistema y no ir variando los elementos y su funcionamiento en cada pantalla.
1. **Prevención de errores:** Lo ideal es que nunca haya errores, con instrucciones claras de que se debe hacer en cada pantalla, sistemas de ayuda. Si se pueden validar los errores antes de enviar la acción, como la validación en línea de un formulario mucho mejor.
1. **Reconocer mejor que recordar:** El usuario dispone de poca memoria a corto plazo, por lo que minimiza el uso de su memoria colocando las opciones a la vista o de fácil acceso. Es mucho más fácil que reconozca algo a que lo recuerde estando muy ligado al punto 4 de Consistencia y estándares.
1. **Uso eficiente y flexibilidad:** El diseño debe servir tanto para usuarios inexpertos como expertos.
1. **Diseño práctico y minimalista:** No todas las acciones pueden estar a la vista, ya que cada unidad de información reduce la visibilidad de la información que de verdad importa. Manejar correctamente las jerarquías visuales y el espacio en blanco.
1. **Ayuda, diagnóstico y recuperación de errores:** En el caso de que haya una situación de error, el sistema debe indicar al usuario que ha pasado y cómo resolverlo.
1. **Ayuda y documentación:** Aunque el sistema es suficientemente usable y no es necesario ninguna documentación, siempre habrá usuarios que puedan necesitarla. Por ello es importante verificar que el sistema ofrezca ayuda relevante al contexto del usuario, cajas de búsqueda, etc.
1. **Habilidades:** El sistema debería anticipar las habilidades y conocimientos del usuario para ofrecer información adaptada al usuario.
1. **Interacción con el usuario placentera y respetuosa:** Las interacciones de los usuarios con el sistema deben favorecer la calidad de su vida.
1. **Privacidad:** El sistema debe ayudar a proteger la privacidad del usuario
1. # **Preparación**
En esta sección se delimitará el sector y los principios heurísticos que soportará la aplicación, además se seleccionará a los evaluadores por último se presentará la herramienta de recolección, selección y clasificación con respecto a las interfaces de la aplicación.
1. # **Sector**

La aplicación está enfocada en el sector “Salud y Estilos de Vida”, se debe a tener en cuenta la privacidad del dato de salud que se comparte con la aplicación.

La aplicación está dirigida a hombres y mujeres de edades entre 45 - 60 años de edad, por lo que se requiere de colores descansables a la vista, interfaces limpias y no muy saturadas ni recargadas con elementos innecesarios, se requiere de textos medianamente grandes y del uso de la negrita, para poder identificar texto o información relevante.
1. # **Elección de principios heurísticos**

Dentro de los principios heurísticos establecidos anteriormente, se procede a la selección de los principios que se adaptan a esta evaluación de las interfaces de la aplicación móvil inHealth.

- Visibilidad del estado del sistema.
- Uso y control de usuario.
- Consistencia y estándares.
- Prevención de errores.
- Reconocer mejor que recordar.
- Uso eficiente y flexibilidad.
- Diseño práctico y minimalista.
- Interacción con el usuario placentera y respetuosa.
- Privacidad.


1. # **Herramienta de evaluación:**

Se presenta la siguiente tabla de evaluación donde se contempla lo siguiente:

- **Interfaz:** Nombre de la interfaz a evaluar.
- **Frecuencia:** El problema es común o raras veces ocurre, descripción de la frecuencia del problema encontrado.
- **Impacto:** Nivel de impacto del problema relacionado a los usuarios.
- **Persistencia:** El problema se resuelve con una serie de pasos o reiteradamente aparece.
  1. # **Herramienta de recolección, selección y clasificación**

Se presenta el siguiente Excel, donde tenemos lo siguiente:

- **Pantalla:** El nombre de la interfaz a evaluar.
- **Problema:**	Problema	encontrado,	especificado	y	explicado detalladamente.
- **Recomendación:** Recomendaciones que el evaluador enfatiza para las correcciones necesarias.
- **Prioridad:** Escala de prioridades, según Nielsen, explicadas en la tabla de Frecuencia y Severidad.
  1. # **Herramienta de contrastación entre las heurísticas seleccionadas y las interfaces de la aplicación**
- **Interfaz:** Nombre de la interfaz de la aplicación a evaluar.
- **Heurística Seleccionada:** Heurística seleccionada que será el indicador a evaluar con respecto a la interfaz.
- **Comentario:** Comentario del experto que evaluó la interfaz.
  1. # **Selección de evaluadores**

Para las evaluaciones dadas, se llamará a un grupo de expertos, los cuales se le dará la herramienta detallada anteriormente para la evaluación de las interfaces dadas.
1. # **Ejecución**

1. **Distribución de datos en tabla de evaluación:**

Se procede a tabular los datos en la tabla de evaluación, descrita anteriormente.

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.031.jpeg)
1. # **Distribución de datos en herramienta seleccionada:**

Se procede a distribuir los datos en la herramienta establecida, descrita anteriormente:

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.032.jpeg)


1. # **Distribución de datos con las heurísticas seleccionadas:**
Se procede a hacer una contrastación entre las interfaces con respecto a las heurísticas seleccionadas

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.033.jpeg)
1. # **Conclusiones**

Se han encontrado los problemas señalados anteriormente, en su mayoría problemas de validación y diseño que ya han sido identificados, localizados y priorizados.

Los problemas han sido solucionados por el equipo de trabajo, pero este documento nos sirve para visualizar pequeños problemas que se han mostrado durante el funcionamiento de la aplicación por paciente con Infarto Agudo de Miocardio.

Esta prueba heurística ha permitido encontrar problemas específicos, en detalle un problema que era error técnico en la interfaz de Citas, por lo que tomando en cuenta el impacto que tendría en el proyecto se ha solucionado.
1. # **Gráficos**

1. **Anexo 1:**

Ilustración: Ventana de Registro del Paciente (datos erróneos)

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.034.jpeg)

Fuente: inHealth
1. # **Anexo 2:**

Ilustración: Mensaje de error en Inicio de Sesión del paciente

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.035.jpeg)

Fuente: inHealth


1. # **Anexo 3:**

Ilustración: Ventana de perfil del paciente

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.036.jpeg)

Fuente: inHealth
1. # **Anexo 4:**

Ilustración: Ventana de datos médicos del paciente

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.037.jpeg)

Fuente: inHealth


1. # **Anexo 5:**
Ilustración: Ventana de detalle de cada dato médico

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.038.jpeg)

Fuente: inHealth


1. # **Anexo 6:**

Ilustración: Ventana de agregar médico por código QR

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.039.jpeg)

Fuente: inHealth
1. # **Anexo 7:**

Ilustración: Ventana de editar perfil

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.040.jpeg)

Fuente: inHealth



1. # **Anexo 8:**

Ilustración: Ventana de agendar cita médica

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.041.jpeg)

Fuente: inHealth
1. # **Anexo 9:**

Ilustración: Ventana de desafíos

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.042.jpeg)

Fuente: inHealth
1. # **Estado final de las variables:**

Se adjunta screens de las pruebas:

Ilustración: Ventana de permiso a datos para la aplicación inHealth

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.043.jpeg)

Fuente: inHealth





















1. # **Estado final de las variables:**

Se adjunta screens de las pruebas:

Ilustración: Ventana de detalle de cada dato médico


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.044.png)

Fuente: inHealth




















1. # **Estado final de las variables:**

Se adjunta screens de las pruebas:

Ilustración: Ventana de cámara y código QR para la aplicación inHealth

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.045.jpeg)

Fuente: inHealth
1. # **Estado final de las variables:**

Se adjunta screens de las pruebas:

Ilustración: Ventana para editar perfil del paciente

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.046.jpeg)![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.047.jpeg)

Fuente: inHealth
1. # **Estado final de las variables:**

Se adjunta screens de las pruebas:

Ilustración: Ventana de Citas Médicas para la aplicación inHealth


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.048.jpeg)![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.049.jpeg)

Fuente: inHealth
1. # **Estado final de las variables:**

Se adjunta screens de las pruebas:

Ilustración: Ventana de Desafíos para la aplicación inHealth

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.050.jpeg)

Fuente: inHealth

**Anexo 11: Encuesta realizada a pacientes post InHealth**

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.051.jpeg)

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.052.jpeg)

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.053.jpeg)

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.054.jpeg)

**Anexo 12: Entrevista realizada a pacientes después del uso de InHealth**

1. **Entrevista a pacientes:**

https:[//www.youtube.com/watch?v=2ePACfPq3Xo](http://www.youtube.com/watch?v=2ePACfPq3Xo)












1. **Fotos de la entrevista realizada:**


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.055.png)

**Anexo 13: Correo de validación del médico**

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.056.jpeg)














**Anexo 14: Correo de Aprobación de Test Flight**

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.057.jpeg)

2. **Evidencias de la ejecución de la propuesta (diseños de sesiones, talleres, fotos, etc.)**


![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.058.png)

Gráfico 34: Entrevista post a paciente	Gráfico 35: Entrevista post a paciente

2. **R.D. que aprueba el proyecto de investigación**

2. **Constancia de la Institución y/o organización donde se ha desarrollado la propuesta de investigación.**

![](Aspose.Words.648545d7-0646-4a59-ae90-8c19ebf28f8a.059.jpeg)
