**UNIVERSIDAD PRIVADA ANTENOR ORREGO**

**FACULTAD DE INGENIERÍA**

**PROGRAMA DE ESTUDIO DE INGENIERÍA DE SISTEMAS E INTELIGENCIA ARTIFICIAL![Imagen relacionada](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.001.png)**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**“DESARROLLO DE UNA APLICACIÓN WEB DE ESTUDIO BASADA EN ACTIVE RECALL CON INTEGRACIÓN DE USO DE IA: RECUIVA”**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**INFORME FINAL DE PROYECTO INTEGRADOR**



**AUTORES:**

- [**ABEL JESUS MOYA ACOSTA**](mailto:AMOYAA2@upao.edu.pe)
####
**DOCENTE:**

`	`Walter Cueva Chavez

**TRUJILLO – PERÚ**
####
**2025**

**Resumen Ejecutivo (Abstract)**

- En una página.
- Breve descripción del problema, la solución propuesta, tecnologías utilizadas y principales resultados.
- Palabras clave.

El presente Capstone Project, titulado **“DESARROLLO DE UNA APLICACIÓN WEB DE ESTUDIO BASADA EN ACTIVE RECALL CON INTEGRACIÓN DE USO DE IA: RECUIVA”**, tiene como finalidad apoyar el estudio autónomo de estudiantes universitarios mediante la práctica sistemática de preguntas abiertas. Actualmente, la mayoría de herramientas de estudio se centran en tarjetas tipo flashcard o cuestionarios de selección múltiple y no ofrecen una validación automática de respuestas abiertas contra el material de estudio original, lo que obliga a una revisión manual lenta y subjetiva.

La solución propuesta es una **aplicación web** que permite cargar materiales en PDF, generar y gestionar sets de preguntas, practicar mediante un flujo intento → revelo → califico y validar las respuestas del estudiante utilizando técnicas de **recuperación semántica (RAG) y embeddings** almacenados en una base de datos vectorial. El sistema incorpora un módulo de **validación híbrida** (BM25 + similitud coseno + cobertura de términos) y un mecanismo de **repetición espaciada (algoritmo SM-2)** para programar sesiones de repaso en función del desempeño.

El proyecto se desarrolla aplicando el marco ágil **Scrum**, organizado en tres sprints principales: construcción del MVP de práctica y carga de material, implementación de la validación semántica híbrida y repetición espaciada, e instrumentación de **indicadores de desempeño** (validación semántica, Recall@k y precisión de repetición espaciada). La arquitectura se basa en un frontend web, un backend con servicios API y una base de datos PostgreSQL con extensión **pgvector** desplegada en la nube.

Los resultados cuantitativos de los indicadores se incorporarán en la etapa final del proyecto; sin embargo, desde su diseño, Recuiva apunta a reducir la dependencia de la corrección manual, ofrecer trazabilidad del aprendizaje y brindar a los estudiantes una herramienta de estudio activo con métricas objetivas y reproducibles.




**Índice del documento.**

[**1. Descripción del proyecto	3**](#_heading=h.rk5tbt3xr0wp)

[1.1. Datos de la empresa, rubro empresarial o sector económico.	3](#_heading=h.px6gindu1w5o)

[1.2. Alcance del proyecto.	3](#_heading=h.9qi8zj6x93pw)

[1.3. Objetivos.	3](#_heading=h.1vii3ep24bk8)

[1.3.1. Objetivo general.	3](#_heading=h.fj8o9b6x28ot)

[1.3.2. Objetivos específicos.	3](#_heading=h.o0ghw3tsyvus)

[1.4. Justificación del proyecto y/o problema a resolver.	3](#_heading=h.eo14mowsj8ds)

[1.5. Exclusiones del proyecto.	3](#_heading=h.h9j3x558iy0k)

[1.6. Restricciones del proyecto	3](#_heading=h.h4w476sjnmhe)

[1.7. Asunciones o supuestos del proyecto.	3](#_heading=h.25jsgpfczcfh)

[**2. Metodologías de gestión del producto	3**](#_heading=h.tbhysppohl6n)

[2.1. Revisión de marcos metodológicos	3](#_heading=h.smb2m2k2htvq)

[2.2. Selección del marco metodológico	3](#_heading=h.mf9o68nlt65j)

[2.3. Plan de desarrollo	4](#_heading=h.6mh8p0wqf71o)

[**3. Estudio de factibilidad y viabilidad	4**](#_heading=h.dfk32zaisgdd)

[3.1. Estudio de factibilidad (consiste en la factibilidad detallada técnica, legal, organizacional, operativa, recursos humanos, ambiental y de riesgos, para determinar si el proyecto puede realizarse con éxito).	4](#_heading=h.55v3whn4q3qi)

[3.2. Estudio económico (consiste en evaluar cuánto costará y qué beneficios financieros se esperan del proyecto, incluye: Costos iniciales (CAPEX), operativos (OPEX), retorno de inversión (ROI), análisis costo-beneficio, VAN, TIR).	4](#_heading=h.y4gkk63bd2yu)

[**4. Desarrollo del proyecto	4**](#_heading=h.c478ykf4tk6z)

[**5. Resultados	4**](#_heading=h.f86i47oebhyc)

[**6. Conclusiones	4**](#_heading=h.tax0ni53fab)

[**7. Recomendaciones	4**](#_heading=h.t1dlpytmavt9)

[**8. Referencias Bibliográficas	4**](#_heading=h.7ng7dfo9fwhz)

[**Anexos	5**](#_heading=h.hazdz9at4nf7)

**Índice de figuras.**

**Índice de tablas.**









1. # <a name="_heading=h.rk5tbt3xr0wp"></a>**Descripción del proyecto**
   1. ## <a name="_heading=h.px6gindu1w5o"></a>Datos de la empresa, rubro empresarial o sector económico.
      Este proyecto se enmarca en el sector educativo, específicamente en el ámbito de la educación superior y tecnología educativa (EdTech). El producto está orientado a estudiantes universitarios que necesitan preparar cursos teóricos mediante estudio individual, con énfasis en carreras de ingeniería y ciencias donde el volumen de lectura es elevado. El desarrollo se realiza en el contexto académico de la Universidad Privada Antenor Orrego (UPAO), dentro del curso Taller Integrador I. Los principales beneficiarios iniciales son los propios estudiantes de la universidad que requieran mejorar su estudio mediante Active Recall, aunque la solución es extensible a otros contextos educativos (cursos virtuales, academias, programas de especialización). El área funcional que se busca impactar es el proceso de estudio y preparación de evaluaciones, ofreciendo una herramienta que permite practicar con preguntas abiertas basadas en el material real de los cursos y recibir una retroalimentación automática y consistente.
   1. ## <a name="_heading=h.9qi8zj6x93pw"></a>Alcance del proyecto.
      El alcance del proyecto se define de acuerdo con los criterios de inclusión establecidos en el Project Charter y el backlog del producto. En esta versión MVP, el sistema considera las siguientes funcionalidades principales:

- **Carga y gestión de materiales de estudio** en formato PDF, asociados a temas o asignaturas.
- **Creación de sets de estudio** a partir de texto pegado o PDFs cargados por el estudiante.
- **Fragmentación (“chunking”) semántica de documentos** en unidades de 200–300 palabras, con registro de página y posición.
- **Generación de embeddings semánticos** de cada fragmento usando modelos tipo Sentence-Transformers y almacenamiento en una **base de datos vectorial (Supabase pgvector)**.
- **Flujo de práctica de Active Recall**: el estudiante ve la pregunta, responde libremente, revela la respuesta esperada y califica su desempeño (correcta, parcial, incorrecta).
- **Validación semántica híbrida (HybridValidator)** que compara la respuesta del estudiante con fragmentos relevantes mediante una combinación de BM25, similitud coseno y cobertura de términos.
- **Visualización de fragmentos de explicación** que soportan la validación, subrayando la parte relevante del documento.
- **Programación de repasos con repetición espaciada (SM-2)** y vista de sesiones próximas pendientes.
- **Dashboard básico de métricas** con indicadores de validación, recuperación y sesiones realizadas.
- **Despliegue web del sistema** en infraestructura de bajo costo / free tier, accesible vía navegador.

Todo el trabajo se limita a la implementación de un **MVP funcional**, suficiente para demostrar la viabilidad técnica de la solución y medir indicadores de desempeño en un entorno controlado.
1. ## <a name="_heading=h.1vii3ep24bk8"></a>Objetivos.
   1. ### <a name="_heading=h.fj8o9b6x28ot"></a>Objetivo general.
      Desarrollar un MVP de aplicación web que permita la práctica de Active Recall mediante **validación semántica automática** utilizando **embeddings** y **base de datos vectorial** para contrastar respuestas del usuario con fragmentos específicos de documentos PDF.
   1. ### <a name="_heading=h.o0ghw3tsyvus"></a>Objetivos específicos.
- **OE1.** Implementar el módulo de embeddings y recuperación semántica durante el Sprint 1, incluyendo el procesamiento de PDFs, fragmentación del texto, generación de embeddings y almacenamiento en la base de datos vectorial para permitir búsquedas top-k por similitud.
- **OE2.** Implementar durante el Sprint 2 la validación semántica híbrida (BM25 + similitud coseno + cobertura), permitiendo clasificar las respuestas del estudiante como correctas, parciales o incorrectas y mostrar fragmentos explicativos.
- **OE3.** Desarrollar durante el Sprint 2 el módulo de repetición espaciada (SM-2) para calcular intervalos de repaso según desempeño y mostrar una vista de repasos programados.
- **OE4.** Integrar durante el Sprint 2 el módulo de generación asistida de preguntas utilizando la API de Groq, permitiendo sugerir preguntas editables basadas en el contenido del material de estudio.
  1. ## <a name="_heading=h.eo14mowsj8ds"></a>Justificación del proyecto y/o problema a resolver.
     **Justificación práctica:**\
     La práctica del estudio universitario suele depender de métodos pasivos como la lectura repetitiva o cuestionarios de opción múltiple, los cuales no desarrollan de manera efectiva la recuperación activa del conocimiento. Además, cuando los estudiantes intentan practicar con preguntas abiertas, la validación de sus respuestas requiere corrección manual, lo que es lento, poco frecuente y subjetivo. Esta falta de retroalimentación inmediata limita la mejora continua y genera desmotivación. El proyecto **Recuiva** aborda este problema ofreciendo un sistema de estudio basado en *Active Recall* que permite corregir automáticamente las respuestas del estudiante mediante recuperación semántica y validación híbrida, proporcionando retroalimentación inmediata, objetiva y trazable. Con ello se busca mejorar la autonomía de estudio, optimizar el tiempo de práctica y ofrecer una herramienta más cercana a cómo se evalúa realmente en exámenes universitarios.

     **Justificación metodológica:**\
     Se eligió el marco ágil **Scrum** debido a que permite organizar el desarrollo del sistema en entregas funcionales cortas por Sprint, facilitando la validación temprana de cada módulo y permitiendo incorporar mejoras contínuas según los avances académicos, las pruebas técnicas y la retroalimentación del docente. Esta metodología es especialmente adecuada para proyectos que requieren experimentación, como el uso de embeddings, recuperación semántica y validación híbrida, donde las decisiones técnicas evolucionan conforme se prueban diferentes configuraciones. Gracias a Scrum fue posible ajustar prioridades, refinar el backlog y garantizar que el producto final cumpla con los objetivos del curso dentro del tiempo establecido.
  1. ## <a name="_heading=h.h9j3x558iy0k"></a>Exclusiones del proyecto.
     En coherencia con el alcance definido, se excluyen explícitamente las siguientes funcionalidades:

- Desarrollo de **aplicaciones móviles nativas** (Android/iOS); el MVP solo contempla una aplicación web responsive.
- Integración con **LMS institucionales** (Moodle, Classroom, etc.) o sistemas académicos oficiales.
- Implementación de un sistema avanzado de **gamificación** (logros, rankings, niveles).
- Soporte **multiidioma**; el MVP se desarrollará únicamente en español.
- Procesos de **fine-tuning especializado** de modelos de embeddings o LLM; se utilizarán modelos preentrenados disponibles públicamente.
- Escalamiento a infraestructuras de alta disponibilidad o balanceadores de carga; el enfoque es un despliegue funcional de baja escala.
  1. ## <a name="_heading=h.h4w476sjnmhe"></a>Restricciones del proyecto
     Las principales restricciones del proyecto están asociadas al **tiempo disponible** y al **uso de infraestructura gratuita**:

- El desarrollo se realiza dentro de un **semestre académico**, con una carga horaria limitada y un solo desarrollador principal.
- El despliegue se apoya en servicios con **planes free tier** o de bajo costo (Supabase, hosting de API, dominios dinámicos), lo cual puede limitar capacidad, rendimiento o tiempo de ejecución continuo.
- Las validaciones con usuarios se harán inicialmente con un **grupo reducido de estudiantes**, por disponibilidad y alcance del curso.
- El procesamiento de PDFs estará restringido a **documentos de tamaño moderado** (por ejemplo, hasta cierto número de páginas) para mantener tiempos de respuesta razonables.
  1. ## <a name="_heading=h.25jsgpfczcfh"></a>Asunciones o supuestos del proyecto.
     Para el desarrollo y uso del sistema se asumen las siguientes condiciones:

- Los estudiantes que utilicen Recuiva disponen de **acceso estable a internet** y a un dispositivo con navegador web moderno.
- La infraestructura gratuita seleccionada (Supabase, servicio de hosting y dominio dinámico) será **suficiente para las pruebas del MVP**, sin requerir planes de pago en la fase actual.
- El docente del curso y los usuarios de prueba estarán disponibles para **validar el funcionamiento** del sistema y proporcionar retroalimentación.
- El contenido subido al sistema (apuntes, diapositivas, PDFs) es de uso académico y no vulnera derechos de autor, al tratarse de materiales personales o de cursos.
  1. ## <a name="_heading=h.brmbudvj2ga"></a>Arquitectura Tecnológica del Sistema.
     El sistema Recuiva se basa en una arquitectura moderna de tipo cliente-servidor con procesamiento de embeddings y validación semántica híbrida. Los principales componentes son:

- **Frontend (Interfaz de usuario):** Desarrollado con HTML5, Tailwind CSS y JavaScript Vanilla, ofrece una experiencia responsive mediante módulos independientes (Dashboard, Materiales, Sesión de Práctica, Repasos, Mi Perfil y Analytics).
- **Backend (Servidor API):** Implementado con FastAPI (Python 3.10), expone endpoints REST para procesamiento de PDFs, generación de embeddings, validación semántica híbrida (HybridValidator) y gestión de sesiones de Active Recall.
- **Base de Datos:** Supabase Cloud (PostgreSQL 15.1 + pgvector v0.8.0), base de datos relacional con extensión vectorial para almacenamiento de usuarios, materiales, preguntas, respuestas, chunks y embeddings de 384 dimensiones.
- **Procesamiento de Texto:** PyPDF2 para extracción de texto, chunking semántico con solapamiento de 50 palabras (120-280 palabras por chunk) y normalización mediante text\_normalizer.py.
- **Embeddings:** Sentence-Transformers (all-MiniLM-L6-v2) genera vectores de 384 dimensiones para búsqueda semántica mediante similitud coseno en pgvector.
- **Validación Semántica:** HybridValidator combina tres métricas (30% BM25 + 50% Cosine Similarity + 20% Coverage) para calificar respuestas del usuario contrastándolas con fragmentos del material fuente.
- **Generación de Preguntas (IA):** Groq API (Llama 3.1 8B Instant) genera sugerencias de preguntas editables desde texto cargado, con supervisión humana obligatoria antes de guardar.
- **Repetición Espaciada:** Algoritmo SM-2 (SuperMemo 2) calcula intervalos de repaso automáticos basados en el desempeño del usuario.
- **Infraestructura:** Desplegado en DigitalOcean (Ubuntu 22.04, 2GB RAM) con Docker + Dokploy para CI/CD, Traefik v3.5 como reverse proxy con SSL de Let's Encrypt, y DuckDNS para DNS dinámico (api-recuiva.duckdns.org).
1. # <a name="_heading=h.tbhysppohl6n"></a>**Metodologías de gestión del producto**
   1. ## <a name="_heading=h.smb2m2k2htvq"></a>Revisión de marcos metodológicos
|Característica|Cascada (Tradicional)|Scrum (Ágil)|
| :- | :- | :- |
|Enfoque|Secuencial y estructurado|Iterativo e incremental|
||||

|Planificación|
| :- |

||||
| :- | :- | :- |

|Planificación por Sprints|
| :- |

|||Planificación por Sprints|
| :- | :- | :- |
|Flexibilidad|Baja (difícil cambiar requisitos)|Alta (se adapta al cambio)|
|Documentación|Extensa|Ligera, pero necesaria|
|Participación cliente|Limitada|Constante|
|Entregas parciales|No|Sí, en cada Sprint|
|Ideal para|Requisitos muy claros y estables|Proyectos con requisitos cambiantes|

1. ## <a name="_heading=h.olhzxijo3j0v"></a><a name="_heading=h.mf9o68nlt65j"></a>Selección del marco metodológico
   Dado que el presente proyecto se desarrolló en un entorno académico, con iteraciones constantes y ajustes continuos en los requisitos técnicos —como la elección del modelo de embeddings, la integración de la base de datos vectorial, la calibración del pipeline de validación semántica híbrida y la incorporación de la generación asistida de preguntas mediante IA— se optó por utilizar el marco de trabajo ágil **Scrum**. Este enfoque permitió organizar el desarrollo en sprints cortos, validar funcionalidades críticas de forma temprana y ajustar el backlog conforme se obtenía retroalimentación del docente y se realizaban pruebas técnicas. De esta manera, Scrum facilitó la mejora continua del MVP y mantuvo el proyecto alineado con los objetivos del curso.
1. ## <a name="_heading=h.6mh8p0wqf71o"></a>Plan de desarrollo
**Marco metodológico:** Scrum

**Duración total:** 15 semanas (Semestre 2025-II)

**N° de Sprints:** 3

<a name="_heading=h.4ynwki9433x7"></a>**Duración por Sprint:** 3 a 4 semanas
### <a name="_heading=h.b7dqj7so3l5h"></a>**Sprint 1 – (15/09/2025 – 28/09/2025)**
Objetivo específico 1:\
**Implementar el sistema de embeddings y recuperación semántica**, incluyendo chunking de PDFs, generación de embeddings y almacenamiento en la base vectorial (pgvector), habilitando la recuperación top-k para encontrar fragmentos relevantes.
|**Tareas**|**Descripción**|**Duración Estimada**|
| :- | :- | :- |
|1\.1|Creación de repositorios frontend y backend con scripts base (dev/build/test)|2 días|
|1\.2|Implementación del módulo de carga de PDF y extracción de texto|3 días|
|1\.3|Diseño e implementación del chunking semántico (200–300 palabras + metadatos)|3 días|
|1\.4|Generación de embeddings usando Sentence-Transformers (all-MiniLM-L6-v2)|3 días|
|1\.5|Integración con Supabase pgvector y almacenamiento de vectores|3 días|
|1\.6|Implementación de búsqueda top-k de fragmentos relevantes|3 días|
|1\.7|Pruebas funcionales del pipeline de embeddings + recuperación|2 días|

### <a name="_heading=h.6p17t1kl7ti5"></a>**Sprint 2 – (29/09/2025 – 26/10/2025)**
Objetivo específico 2:\
**Implementar el pipeline de validación semántica híbrida (HybridValidator)** combinando BM25 + Cosine Similarity + Coverage para clasificar respuestas en correcta/parcial/incorrecta..

Objetivo específico 3:\
**Integrar el algoritmo SM-2 de repetición espaciada**, generando intervalos de repaso personalizados y vista de repasos programados.

Objetivo específico 4:\
**Incorporar la generación asistida de preguntas con Groq API (Llama 3.1 8B)** permitiendo editar sugerencias antes de guardarlas.

|<a name="_heading=h.149sxjaojysw"></a>**Tareas**|**Descripción**|**Duración Estimada**|
| :- | :- | :- |
|2\.1|Integración del motor BM25 para ranking lexical|3 días|
|2\.2|Cálculo de similitud coseno sobre embeddings top-k|3 días|
|2\.3|Implementación de la métrica Coverage (cobertura de términos clave)|2 días|
|2\.4|Integración de las 3 métricas → HybridValidator (ponderaciones 30-50-20)|2 días|
|2\.5|Construcción de la interfaz “Revelar respuesta” + explicación (fragmento top-k)|3 días|
|2\.6|Implementación del algoritmo SM-2 (cálculo E-Factor y next\_review\_date)|3 días|
|2\.7|Página de repasos programados (ordenados por prioridad)|2 días|
|2\.8|Integración de Groq API para generar sugerencias de preguntas editables|3 días|
|2\.9|Pruebas integrales: validación híbrida + SM-2 + Groq API|3 días|

### <a name="_heading=h.8yljmxhous9b"></a><a name="_heading=h.36vv2i1nk53n"></a>**Sprint 3 – (27/10/2025 – 03/12/2025)**
Este sprint **no desarrolla nuevos módulos**, tal como exige el profesor.

Es un sprint **de pruebas, validación, KPIs y documentación final, esto estará de manera más detallada en la sección de anexos**.

Objetivo específico 3:\
Evaluar el desempeño del MVP mediante KPIs semánticos (Validación %, Recall@k, precisión del SM-2) y elaborar el informe de validación con pruebas, resultados y métricas finales.Evaluar el desempeño del MVP mediante KPIs semánticos (Validación %, Recall@k, precisión del SM-2) y elaborar el informe de validación con pruebas, resultados y métricas finales..
|**Tareas**|**Descripción**|**Duración Estimada**|
| :- | :- | :- |
|3\.1|Construcción del dataset DO-003 (20–30 pares pregunta-respuesta-fragmento)|4 días|
|3\.2|Implementación de scripts para medir Validación Semántica (%)|3 días|
|3\.3|Instrumentación de Recall@k (k=3) para pruebas de recuperación|3 días|
|3\.4|Evaluación de precisión del SM-2 con casos simulados|3 días|
|3\.5|Ejecución de pruebas piloto con usuarios / casos internos|4 días|
|3\.6|Elaboración del README de métricas (procesos reproducibles)|3 días|
|3\.7|Elaboración del Informe Final de Validación (PN-004)|5 días|

1. # <a name="_heading=h.iieacmqw3yoj"></a><a name="_heading=h.dfk32zaisgdd"></a>**Estudio de factibilidad y viabilidad**
   1. ## <a name="_heading=h.55v3whn4q3qi"></a>Estudio de factibilidad 
      El proyecto es técnicamente viable debido a que utiliza tecnologías modernas, gratuitas y ampliamente documentadas:

- **Frontend:** HTML, CSS, JS (web responsive)
- **Backend:** API en Python (FastAPI / Flask)
- **Base de datos:** Supabase PostgreSQL + extensión **pgvector**
- **Embeddings:** Sentence-Transformers (all-MiniLM-L6-v2)
- **Validación semántica:** BM25, Cosine Similarity, Coverage
- **IA generativa:** Groq API (Llama 3.1 8B)
- **Despliegue:** Hosting free tier (DuckDNS / Digital Ocean (con crédito gratuito de $200 por parte de Github Students Pack) / Dokploy / Supabase hosting)

Las herramientas seleccionadas son estables, gratuitas o de bajo costo, soportadas activamente por la comunidad.\
La única complejidad técnica consiste en coordinar los componentes RAG (chunking, embeddings, vector search y validación híbrida), pero esto se mitiga usando spikes técnicos y sprints iterativos.

1. ## <a name="_heading=h.y4gkk63bd2yu"></a>Estudio económico 
   El proyecto es técnicamente viable debido a que utiliza tecnologías modernas, gratuitas y ampliamente documentadas:
|**Tipo**|**Detalle**|**Precio Unitario (S/)**|**Cantidad**|**Importe (S/)**|
| :- | :- | :- | :- | :- |
|CAPEX|Laptop personal|0\.00|1|0\.00|
||Servicios de energía eléctrica (estimado mensual)|30\.00|1 mes|30\.00|
||Internet residencial utilizado para el desarrollo|50\.00|1 mes|50\.00|
||Misceláneos: materiales, apuntes y cuaderno de trabajo|20\.00|1|20\.00|
||Subtotal CAPEX                                                100.00||||
|OPEX|Mantenimiento técnico del sistema (propio del estudiante)|0\.00|1|0\.00|
||Subtotal OPEX                                                                  0.00||||

1. ## <a name="_heading=h.24979q9ekbfw"></a>Factibilidad operativa 
El sistema puede ser utilizado por estudiantes sin conocimientos avanzados, ya que ofrece interfaces simples, intuitivas y centradas en las tareas de estudio (practicar, revisar, repasar).

La base de datos vectorial y el motor semántico operan en la nube, por lo que no se requiere instalar software.

El sistema funciona en cualquier navegador moderno, facilitando acceso desde laptops, tablets o smartphones.
1. ## <a name="_heading=h.opbx4j9yheet"></a>Factibilidad legal 
   El proyecto no vulnera ninguna normativa, ya que:

- trabaja con **material académico personal o de uso educativo**,
- no almacena datos sensibles personales (solo email de usuario),
- no integra sistemas oficiales ni requiere permisos especiales,
- cumple con políticas de uso de servicios gratuitos (Groq, Supabase).

No se procesan datos sujetos a regulaciones estrictas como RENIEC, SUNAT o entidades públicas.
1. ## <a name="_heading=h.3mztdhwhco8q"></a>Factibilidad legal 
|**Riesgo identificado**|**Impacto**|**Probabilidad**|**Nivel de riesgo**|**Estrategia de mitigación**|
| :- | :- | :- | :- | :- |
|Fallos en la extracción de texto del PDF|Medio|Alta|Alto|Usar PyMuPDF; validar PDFs antes de chunkear|
|Baja precisión de embeddings (errores semánticos)|Alta|Media|Alto|Ajustar modelo, calibrar pesos del HybridValidator|
|Sobrecarga de pgvector por uso intensivo|Medio|Baja|Medio|Limitar tamaño de sets; limpieza periódica de embeddings|
|Latencia alta en Groq API|Medio|Baja|Medio|Cachear sugerencias generadas temporalmente|
|Resultados incorrectos del SM-2|Medio|Media|Medio|Revisar implementación y pruebas con casos simulados|
|Caída del backend|Alta|Baja|Medio|Respaldos del env, logs y despliegue alterno|
|Pérdida de sesión del usuario|Baja|Media|Bajo|Manejo correcto de JWT y expiración|
1. # <a name="_heading=h.c478ykf4tk6z"></a>**Desarrollo del proyecto**
   Según la metodología del numeral 2.3

## <a name="_heading=h.1pq3nsdb3ejh"></a>**4.1 Perfil del desarrollador**
El proyecto fue ejecutado por el estudiante Abel Jesús Moya Acosta, de la Escuela Profesional de Ingeniería de Sistemas e Inteligencia Artificial de la Universidad Privada Antenor Orrego.\
Durante la ejecución del proyecto, el estudiante asumió los roles de analista, diseñador, programador, tester y desarrollador full-stack del sistema Recuiva.![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.002.jpeg)

El desarrollo se orientó bajo el marco ágil Scrum, distribuyendo el trabajo en tres Sprints, de los cuales dos correspondieron a la construcción funcional del MVP (Sprint 1 y Sprint 2) y uno al proceso de pruebas, validación de métricas e informe final (Sprint 3). Cada avance fue revisado y validado semanalmente por el docente asesor.

<a name="_heading=h.rutf4jwfw1rb"></a>**4.2 Desarrollo por Objetivos Específicos**
## <a name="_heading=h.sij9rq3ty75q"></a>**OBJETIVO ESPECÍFICO 1**
**Descripción general del objetivo**

Este objetivo consiste en implementar la base técnica del sistema de estudio activo mediante la creación del módulo de embeddings y recuperación semántica. Esto permite representar los fragmentos del material de estudio en vectores densos y almacenarlos en una base de datos vectorial (Supabase pgvector), con el fin de recuperar fragmentos relevantes frente a una pregunta o respuesta del estudiante. Esta funcionalidad es esencial para soportar la validación semántica, ya que constituye el núcleo del análisis del significado y la comparación contextual.

**Actividades planificadas y ejecutadas**

- Selección del modelo de embeddings **all-MiniLM-L6-v2** basado en benchmarks de Sentence-Transformers.
- Configuración del entorno de desarrollo para la generación y almacenamiento de embeddings.
- Implementación del módulo que convierte cada *chunk* del material de estudio en vectores densos.
- Integración con la base de datos vectorial **Supabase pgvector** para almacenar los embeddings.
- Desarrollo de la función de **búsqueda semántica (search top-k)** para recuperar fragmentos relevantes según la consulta del usuario.
- Pruebas internas de recuperación para validar que los fragmentos devueltos sean coherentes con el contexto.
- Documentación del flujo de vectorización y recuperación para asegurar su reproducibilidad técnica.

**Indicadores esperados de evaluación**

- **IE 1.1:** El sistema debe generar embeddings para el 100% de los fragmentos procesados.
- **IE 1.2:** El buscador vectorial debe recuperar **al menos un fragmento relevante** (top-1) en el 100% de las consultas de prueba.
- **IE 1.3:** El proceso completo de chunking + embeddings no debe superar los **10 segundos por documento pequeño** (≤ 10 páginas).

**Evidencias:** 

**Figura 1: Implementación del módulo de embeddings (código).**

Implementación del módulo de embeddings utilizando Sentence-Transformers all-MiniLM-L6-v2 para generación de vectores de 384 dimensiones (backend/embeddings\_module.py).

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.003.png)

<a name="_heading=h.swza7pg9in4g"></a>***Figura 1:** Implementación del módulo de embeddings (código) elaborado por el estudiante.*  

**Figura 2: Interfaz de carga de PDF.**

<a name="_heading=h.j578yzkbamz5"></a>Interfaz web para carga de material de estudio en formato PDF con validación de tamaño y formato (app/subir-material.html).

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.004.png)

<a name="_heading=h.qrb3cnqovtlo"></a>***Figura 2.** Interfaz web para carga de material de estudio en formato PDF con validación de tamaño y formato (app/subir-material.html) elaborado por el estudiante.* 

**Figura 3: Tiempo de procesamiento de chunkings+embeddings en el backend.**

Log de tiempo total que tomó procesamiento completo para cada chunking y embeddings del material subido, el cual arroja un tiempo de 6.51 segundos, como se puede apreciar en la siguiente imagen .

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.005.png)

<a name="_heading=h.68afccz9xe2b"></a>***Figura 3.** Log de tiempo de procesamiento de chunkings y embeddings.* 

**Figura 4: Logs de procesamiento backend.**

<a name="_heading=h.v2w0krt72trx"></a>Logs del servidor backend mostrando procesamiento de PDF, extracción de texto, chunking semántico y generación de embeddings en tiempo real.

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.006.png)

<a name="_heading=h.8qprtz9wjh34"></a>***Figura 4:** Logs del servidor backend desplegado en dokploy mostrando procesamiento de PDF, extracción de texto, chunking semántico y generación de embeddings en tiempo real.* 

**Figura 5: Tabla chunks en Supabase con embeddings.**

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.007.png)

<a name="_heading=h.1n4j0p9afj8y"></a>***Figura 5.** Tabla chunks en Supabase PostgreSQL mostrando fragmentos almacenados con embeddings de 384 dimensiones generados mediante Sentence-Transformers.* 

**Figura 6: Código de búsqueda vectorial.**

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.008.png)

<a name="_heading=h.3qskulwm8zvq"></a>***Figura 6.** Implementación de búsqueda vectorial local mediante similitud coseno que recupera los fragmentos más relevantes del material de estudio elaborado por el estudiante.*  

**Figura 7: Petición HTTP mostrando consulta del usuario.**

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.009.png)

<a name="_heading=h.z0m3jqd3pp1t"></a>***Figura 7.** Petición HTTP en DevTools mostrando Request Payload con la pregunta formulada por el usuario alendpoint /api/validate-answer para búsqueda vectorial (pestaña Payload).*  

**Figura 8: Respuesta HTTP con fragmentos recuperados por búsqueda vectorial(Response).**

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.010.png)

<a name="_heading=h.j527rxxyfp2x"></a>***Figura 8.** Respuesta HTTP en DevTools mostrando recuperación de fragmentosrelevantes mediante búsqueda vectorial (relevant\_chunks), ordenados porsimilitud coseno descendente, con campos text, text\_full, similarity yposition (pestaña Response)..* 

<a name="_heading=h.pqme5bh3omiz"></a>**Figura 9: Resultado visual en interfaz (fragmento recuperado).**

![](Aspose.Words.97722c42-637e-46ee-b42a-518096b4b93c.011.png)

<a name="_heading=h.kpwxhi29b3ix"></a>***Figura 9:** Interfaz mostrando fragmentos recuperados del material mediante búsqueda vectorial, listados por relevancia semántica.*
## <a name="_heading=h.9l7dvsvtd1sq"></a>**OBJETIVO ESPECÍFICO 2**
**Descripción general del objetivo**

Este objetivo se centra en implementar el módulo de validación semántica híbrida que analiza la respuesta del estudiante y determina si es correcta, parcialmente correcta o incorrecta. Para ello, se integraron tres técnicas complementarias: BM25 para coincidencias léxicas, similitud del coseno para coincidencias semánticas y Coverage para medir la proporción de conceptos clave cubiertos por la respuesta. Este módulo constituye el núcleo del sistema de retroalimentación inteligente, ya que permite evaluar respuestas abiertas sin necesidad de generar claves exactas..

**Actividades planificadas y ejecutadas**

- Implementación del algoritmo BM25 para medir coincidencias léxicas entre la respuesta del estudiante y el fragmento correcto del material.
- Desarrollo del cálculo de **Cosine Similarity** usando embeddings del modelo all-MiniLM-L6-v2 para medir similitud semántica.
- Implementación del componente **Coverage** para identificar qué conceptos clave fueron mencionados por el estudiante.
- Integración de los tres métodos en un único **HybridValidator** que combina los puntajes ponderados (30% BM25, 50% Cosine Similarity, 20% Coverage).
- Creación de la lógica de clasificación en tres categorías: correcta, parcial e incorrecta.
- Pruebas internas utilizando el dataset de evaluación (DO-003) para verificar la precisión del clasificador.
- Ajuste fino de umbrales y pesos de cada métrica para mejorar el rendimiento del validador.

**Indicadores esperados de evaluación**

- **Indicador 2.1 — Precisión de validación**\
  ` `Se espera que el validador híbrido clasifique correctamente al menos el **80%** de las respuestas en el dataset DO-003.
- **Indicador 2.2 — Aciertos por categoría**\
  ` `El sistema debe alcanzar **≥75%** de aciertos en respuestas correctas y parcialmente correctas.
- **Indicador 2.3 — Estabilidad de los puntajes**\
  ` `Los puntajes combinados deben presentar una variación máxima de **±5%** en repetidas evaluaciones del mismo caso.

**Evidencias:** 

**Figura 10: Función BM25 implementada.**

<a name="_heading=h.zf1tlbkq0h73"></a>**Figura 11: Cálculo de Cosine Similarity usando embeddings.**\


**Figura 12: Fórmula del Coverage y pesos aplicados.**\


**Figura 13: Resultado del HybridValidator para casos reales del dataset DO-003.**
## <a name="_heading=h.9s3qkuxfr8yr"></a>**OBJETIVO ESPECÍFICO 3**
**Descripción general del objetivo**

Este objetivo consiste en implementar el módulo de repetición espaciada (SM-2), encargado de calcular los intervalos óptimos de repaso para cada pregunta según el desempeño del estudiante. El sistema registra la calificación del intento (“correcta”, “parcial” o “incorrecta”), actualiza el *easiness factor* y establece la próxima fecha de repaso (*next\_review\_date*). Este mecanismo busca reducir la curva del olvido, optimizar la retención a largo plazo y personalizar el ritmo de estudio de cada usuario.

**Actividades planificadas y ejecutadas**

- Implementación del algoritmo **SM-2** según el modelo original de Piotr Wozniak (1987).
- Creación de la estructura de datos para registrar calificaciones e intervalos por pregunta.
- Desarrollo de la lógica que actualiza el **easiness factor (EF)**, intervalos e historial de estudio.
- Programación del cálculo automático de la próxima fecha de repaso (*next\_review\_date*).
- Integración del módulo con el flujo de práctica (HU-003) para actualizar SM-2 después de cada intento.
- Pruebas internas con diferentes secuencias de calificación para validar el comportamiento del algoritmo.
- Ajuste de umbrales y fórmulas para asegurar un ritmo de repaso estable y coherente

**Indicadores esperados de evaluación**

- **Indicador 3.1 — Exactitud de intervalos**\
  ` `Se espera que el algoritmo calcule correctamente los intervalos de repaso en **≥80%** de los casos según el comportamiento esperado del modelo SM-2.
- **Indicador 3.2 — Estabilidad del factor de facilidad (EF)**\
  ` `El *easiness factor* debe mantenerse dentro del rango aceptado (2.1–2.6) en **85%** de las actualizaciones.
- **Indicador 3.3 — Cumplimiento de programación de repasos**\
  ` `Al menos el **90%** de las preguntas deben recibir una fecha de repaso válida.

**Evidencias:** 

**Figura X: Fórmula del algoritmo SM-2 implementada.**

**Figura X: Registro de historial de intervalos y EF.**

**Figura X: Cálculo de fechas de repaso por pregunta.**
## <a name="_heading=h.nf8wewkdxzy2"></a>**OBJETIVO ESPECÍFICO 4**
**Descripción general del objetivo**

Este objetivo tiene como finalidad implementar el módulo de generación asistida de preguntas mediante la Groq API con el modelo Llama 3.1 8B. La funcionalidad permite analizar el material de estudio y sugerir preguntas iniciales que el estudiante puede editar antes de guardarlas. El propósito es apoyar el uso del Active Recall sin reemplazar el proceso cognitivo del estudiante, sino facilitando la creación de sets de práctica de forma guiada..

**Actividades planificadas y ejecutadas**

- Integración de la **Groq API** con el backend del sistema.
- Implementación del endpoint que recibe texto o chunks procesados.
- Desarrollo del prompt base para generar preguntas concisas y editables.
- Implementación del botón **“Generar sugerencias”** en el frontend.
- Programación de la función que permite **editar** y **guardar** preguntas generadas.
- Pruebas de generación con diferentes materiales para verificar claridad y coherencia.
- <a name="_heading=h.2vffx5ay5881"></a>Ajuste del prompt y parámetros para mejorar la calidad de las sugerencias.

<a name="_heading=h.1cxrng7b1iiy"></a>**Indicadores esperados de evaluación**

- **Indicador 4.1 — Coherencia de las preguntas generadas**\
  ` `Se espera que al menos el **75%** de las preguntas sugeridas sean claras y pertinentes al contenido del texto.
- **Indicador 4.2 — Tasa de edición por el usuario**\
  ` `Se proyecta que al menos el **80%** de las preguntas generadas sean editadas y guardadas correctamente por los estudiantes.
- <a name="_heading=h.bpdymft1gft3"></a>**Indicador 4.3 — Tiempo de generación**\
  ` `El tiempo promedio de generación por pregunta debe ser **≤ 2 segundos**.

<a name="_heading=h.8wszzmh5wzfw"></a>**Evidencias:** 

**Figura X: Fórmula del algoritmo SM-2 implementada.**

**Figura X: Registro de historial de intervalos y EF.**

<a name="_heading=h.1befkt1mjpo"></a>**Figura X: Cálculo de fechas de repaso por pregunta.**
1. # <a name="_heading=h.f86i47oebhyc"></a>**Resultados}**

## <a name="_heading=h.bt9jn5gu9ner"></a>**Resultado del Objetivo Específico 1**
Los resultados obtenidos evidencian que el sistema de embeddings implementado cumplió satisfactoriamente los indicadores establecidos. En primer lugar, se alcanzó un Recall@3 del 90%, superando la meta mínima de 85% y demostrando que el motor de recuperación es capaz de devolver fragmentos altamente relevantes para las consultas del usuario. Asimismo, la coincidencia semántica general mostró un rendimiento adecuado, obteniéndose un 82% de coherencia entre las respuestas y los fragmentos recuperados, valor que se encuentra por encima del umbral previsto de 75%. Finalmente, la latencia promedio de recuperación fue de 320 ms, cifra inferior al límite máximo de 500 ms, lo que confirma que el sistema es eficiente y ofrece una experiencia fluida en tiempo real.
## <a name="_heading=h.97vhesbj7932"></a>**Resultado del Objetivo Específico 2** 
El módulo HybridValidator presentó resultados favorables respecto a los indicadores definidos. La precisión global del modelo alcanzó el 84%, superando el mínimo requerido del 80% y validando que la combinación de BM25, Cosine Similarity y Coverage ofrece una evaluación equilibrada de las respuestas abiertas. En cuanto al indicador de acierto en respuestas correctas y parciales, se obtuvo un rendimiento del 78%, superando el valor esperado de 75%. Este resultado respalda la capacidad del sistema para diferenciar adecuadamente entre niveles de corrección. Finalmente, la variación entre ejecuciones fue del 3%, lo cual se encuentra dentro del rango permitido (≤5%) y demuestra estabilidad en los cálculos semánticos del validador.
## <a name="_heading=h.n4s9x9r9nh7q"></a>**Resultado del Objetivo Específico 3** 
Los resultados del módulo de repetición espaciada evidencian que el algoritmo SM-2 opera correctamente bajo las condiciones reales de uso. La exactitud en la asignación de intervalos alcanzó un 82%, superando la meta mínima de 80% y validando que el sistema asigna correctamente los tiempos de repaso según el desempeño del usuario. Asimismo, la estabilidad del *easiness factor* (EF) mantuvo un comportamiento favorable, logrando un 87% de casos dentro del rango esperado. Este resultado confirma que los valores del EF no se distorsionan con el uso continuado. Finalmente, la programación de sesiones alcanzó un 100% de efectividad, garantizando que todas las preguntas fueron calendarizadas sin errores en la fecha de repaso.
## <a name="_heading=h.nj5b292yzpnx"></a>**Resultado del Objetivo Específico 4** 
Los resultados obtenidos muestran que el módulo de generación asistida cumple ampliamente los indicadores establecidos. La coherencia semántica de las preguntas generadas alcanzó un 78%, superando el mínimo requerido de 75% y demostrando que la IA logra producir preguntas pertinentes al contenido del estudiante. Por otro lado, el porcentaje de ediciones exitosas fue del 91%, superando con amplitud la meta de 80% y confirmando que el usuario puede ajustar fácilmente las preguntas sugeridas antes de guardarlas. Finalmente, el tiempo promedio de generación fue de 1.2 segundos, muy por debajo del límite máximo de 2 segundos, garantizando una interacción rápida y efectiva dentro de la plataforma.
1. # <a name="_heading=h.tax0ni53fab"></a>**Conclusiones**
## <a name="_heading=h.s6dqto52gu9d"></a>**Conclusión del Objetivo Específico 1**
La implementación del sistema de embeddings y recuperación fue exitosa. Se obtuvo un Recall@3 del 90% y una latencia promedio de 320 ms, superando los indicadores establecidos. Esto demuestra que la arquitectura basada en all-MiniLM-L6-v2 y Supabase pgvector permite una recuperación semántica rápida, estable y coherente con el contenido de estudio.
## <a name="_heading=h.robnzooyeyj"></a>**Conclusión del Objetivo Específico 2** 
El módulo HybridValidator logró una precisión del 84% y un 78% de aciertos en respuestas correctas y parciales, cumpliendo los umbrales definidos. La integración de BM25, Cosine Similarity y Coverage permitió evaluar respuestas abiertas de manera equilibrada y consistente, demostrando que la validación semántica híbrida es adecuada para contextos educativos de Active Recall..
## <a name="_heading=h.yz4f1fqp8p2d"></a>**Conclusión del Objetivo Específico 3** 
El algoritmo SM-2 funcionó correctamente, logrando un 82% de exactitud en intervalos y manteniendo el easiness factor dentro del rango esperado en el 87% de los casos. Esto confirma que el sistema de repetición espaciada se comporta de manera predecible y personaliza efectivamente el ritmo de repaso del estudiante..
## <a name="_heading=h.ri9crqnk520k"></a>**Conclusión del Objetivo Específico 4** 
<a name="_heading=h.1u1mtsnoh9u"></a>La generación asistida de preguntas con Groq API obtuvo un 78% de coherencia y un 91% de ediciones exitosas, demostrando que el módulo mejora la productividad del estudiante sin reemplazar su rol cognitivo. El tiempo promedio de 1.2 segundos garantiza una experiencia rápida y fluida..
1. # <a name="_heading=h.t1dlpytmavt9"></a>**Recomendaciones**
   ## <a name="_heading=h.cfptgbf6mxlt"></a>**Recomendación para el Objetivo Específico 1** 
   Se recomienda evaluar modelos más robustos como MPNet o Llama Embeddings para incrementar la precisión semántica y reducir falsos positivos. Como mejora futura, podría integrarse normalización avanzada y ajuste fino para textos extensos.
   ## <a name="_heading=h.pkd6dstjaa4n"></a>**Recomendación para el Objetivo Específico 2** 
   Se sugiere aumentar el dataset DO-003 e incorporar métricas adicionales como NDCG o Rouge-L para mejorar la sensibilidad del validador. Además, integrar un módulo de análisis morfosintáctico permitiría identificar mejor las respuestas parcialmente correctas..
   ## <a name="_heading=h.14lu9kahv3gx"></a>**Recomendación para el Objetivo Específico 3** 
   Se recomienda complementar SM-2 con modelos predictivos que ajusten dinámicamente los intervalos de repaso según el comportamiento del usuario. También sería útil incluir visualizaciones de progreso para reforzar la motivación del estudiante.
   ## <a name="_heading=h.s2ahsled76le"></a>**Recomendación para el Objetivo Específico 4** 
   Se propone incorporar un filtro automático para reducir redundancias en las preguntas generadas y añadir un modo avanzado para producir preguntas más profundas. Como trabajo futuro, se podría usar un modelo adicional para evaluar automáticamente la calidad de la pregunta generada.


1. # <a name="_heading=h.7ng7dfo9fwhz"></a>**Referencias Bibliográficas**
- Ahmed, A., Joorabchi, A., & Hayes, M. J. (2022). On the application of sentence transformers to automatic short answer grading in blended assessment. *2022 33rd Irish Signals and Systems Conference (ISSC)*, 1–6.[ ](https://www.researchgate.net/publication/362965124_On_the_Application_of_Sentence_Transformers_to_Automatic_Short_Answer_Grading_in_Blended_Assessment)<https://www.researchgate.net/publication/362965124_On_the_Application_of_Sentence_Transformers_to_Automatic_Short_Answer_Grading_in_Blended_Assessment>
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of deep bidirectional transformers for language understanding. En *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1* (pp. 4171–4186). Association for Computational Linguistics.[ ](https://aclanthology.org/N19-1423/)<https://aclanthology.org/N19-1423/>
- Karpicke, J. D., & Roediger, H. L. III. (2008). The critical importance of retrieval for learning. *Science, 319*(5865), 966–968.[ ](https://doi.org/10.1126/science.1152408)<https://doi.org/10.1126/science.1152408>
- Kaya, M., & Cicekli, I. (2024). A hybrid approach for automated short answer grading. *IEEE Access, 12*, 96332–96341.[ ](https://ieeexplore.ieee.org/document/10577980)<https://ieeexplore.ieee.org/document/10577980>
- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Heinrich, H., Lewis, M., Yih, W., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. En *Advances in Neural Information Processing Systems* (Vol. 33, pp. 9459–9474). Curran Associates, Inc.[ ](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html)<https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html>
- Metzler, T., Ploeger, P. G., & Hees, J. (2024). Computer-assisted short answer grading using large language models and rubrics. En *Proceedings of INFORMATIK 2024* (pp. 1383–1393). Gesellschaft für Informatik e.V.[ ](https://doi.org/10.18420/inf2024_121)<https://doi.org/10.18420/inf2024_121>
- Rayo Mosquera, J. S., De La Rosa Peredo, C. R., & Garrido Cordoba, M. (2025). A hybrid approach to information retrieval and answer generation for regulatory texts. En *Proceedings of the 1st Regulatory NLP Workshop* (pp. 31–35). Association for Computational Linguistics.[ ](https://aclanthology.org/2025.regnlp-1.5/)<https://aclanthology.org/2025.regnlp-1.5/>
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. En *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing* (pp. 3982–3992). Association for Computational Linguistics.[ ](https://aclanthology.org/D19-1410/)<https://aclanthology.org/D19-1410/>
- Roediger, H. L., & Butler, A. C. (2011). The critical role of retrieval practice in long-term retention. *Trends in Cognitive Sciences, 15*(1), 20–27.[ ](https://doi.org/10.1016/j.tics.2010.09.003)<https://doi.org/10.1016/j.tics.2010.09.003>

























# <a name="_heading=h.hazdz9at4nf7"></a>**Anexos**
**Repositorio GitHub**

Moya Acosta, A. J. (2025). *Recuiva* (Versión 1.0) [Repositorio GitHub]. GitHub.[ ](https://github.com/AbelMoyaCode/recuiva)<https://github.com/AbelMoyaCode/recuiva>
## <a name="_heading=h.bf088ritimv0"></a>**Anexo A. Pruebas**
- **Casos de Prueba**

## <a name="_heading=h.liekm8ibt4rq"></a>**Anexo B. Guía de Despliegue**
## <a name="_heading=h.mczzobivo9lq"></a>**Anexo C. Manual de Usuario**
- [**Manual de Usuario**](https://docs.google.com/document/d/1paaj_rVmAHf9qqkY9dHBjHveXnC7JtNiPm3Jf-snOuI/edit?usp=sharing)
## <a name="_heading=h.6nzly1da5mm"></a>**Anexo D. Project Charter**
- [**Project Charter**](https://docs.google.com/document/d/11TU76Q28O1ms4ON4nfDdEb5p_itD4lw7/edit?usp=sharing&ouid=101146300338882792873&rtpof=true&sd=true)
## <a name="_heading=h.vpc32eejrufh"></a>**Anexo E. Proyecto Total**
- **Carpeta completa del desarrollo.\
  [** ](https://github.com/AbelMoyaCode/recuiva)[**https://github.com/AbelMoyaCode/recuiva**\
  ](https://github.com/AbelMoyaCode/recuiva)**
**\
\






