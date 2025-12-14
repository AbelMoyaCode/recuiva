**ANEXO E: DOCUMENTO DE ARQUITETURA DE SOFTWARE (DAS)**

Este anexo detalla la estructura lógica, física y de datos del sistema **Recuiva**, utilizando 

diagramas estandarizados UML para representar la solución técnica implementada. La arquitectura se ha diseñado priorizando la escalabilidad modular y el procesamiento eficiente de vectores para las tareas de Inteligencia Artificial.

**D.1. Arquitectura General del Sistema**

El sistema utiliza una arquitectura de microservicios contenerizados sobre infraestructura en la nube, optimizada para el procesamiento de IA y recuperación de información (RAG). Se distingue claramente la separación entre el cliente (Frontend), la lógica de negocio (Backend API) y los servicios de persistencia y cálculo externo.

**Figura 1** 

*Arquitectura de Componentes del Sistema Recuiva*

![](Aspose.Words.a0d5507f-707f-4401-b9e1-c94278e5b42f.001.png)

*Nota.* La figura muestra la integración entre el cliente web accesando vía HTTPS, el backend contenerizado gestionado por Dokploy, y los servicios externos de IA (Groq) y Base de Datos (Supabase). Elaborado por el autor.

**D.2. Modelo de Base de Datos (DER)**

El esquema relacional implementado en PostgreSQL (Supabase) integra tablas convencionales para la gestión de usuarios y contenidos, con almacenamiento vectorial especializado mediante la extensión pgvector para soportar las búsquedas semánticas.

**Figura 2** 

*Diagrama Entidad-Relación (DER) de Recuiva*

![](Aspose.Words.a0d5507f-707f-4401-b9e1-c94278e5b42f.002.png)

*Nota.* Representa la estructura de datos para la gestión de usuarios, materiales, fragmentos vectoriales (embeddings) y la lógica de repetición espaciada. Elaborado por el autor.





**D.3. Diagramas de Comportamiento (Secuencia)**

Se detalla el flujo lógico principal del sistema: la **Validación Semántica Híbrida**. Este proceso combina búsqueda vectorial y algoritmos de Procesamiento de Lenguaje Natural (PLN) para evaluar las respuestas abiertas de los estudiantes en tiempo real.

**Figura 3** 

*Diagrama de Secuencia del Proceso de Validación Híbrida*

![](Aspose.Words.a0d5507f-707f-4401-b9e1-c94278e5b42f.003.png)

*Nota.* Ilustra la interacción secuencial entre los componentes para procesar una respuesta, recuperar el contexto semántico relevante y aplicar el algoritmo de validación triple (BM25 + Coseno + Cobertura). Elaborado por el autor.

**D.4. Diagramas de Estado (Algoritmo SM-2)**

El siguiente diagrama describe el ciclo de vida de una pregunta dentro del sistema de Repetición Espaciada, mostrando cómo transitan los estados (Nuevo, Aprendizaje, Repaso) en función de la calificación obtenida por el estudiante en cada sesión.






**Figura 4** 

*Diagrama de Estados del Algoritmo SuperMemo-2 (SM-2)*

![](Aspose.Words.a0d5507f-707f-4401-b9e1-c94278e5b42f.004.png)

*Nota.* Modela el flujo de estados de una pregunta gobernado por el rendimiento del usuario, determinando automáticamente los intervalos óptimos de repaso. Elaborado por el autor.

**D.5. Diagrama de Casos de Uso (Funcional)**

Este diagrama modela las interacciones principales entre el actor (Estudiante) y los módulos funcionales del sistema, abarcando desde la gestión de identidad hasta el ciclo de estudio con IA.

**Figura 5** *Diagrama de Casos de Uso del Sistema Recuiva*

![](Aspose.Words.a0d5507f-707f-4401-b9e1-c94278e5b42f.005.png)

*Nota.* Detalla las cinco funcionalidades críticas del sistema: autenticación, gestión de material, generación de contenido, práctica activa y visualización de progreso. Elaborado por el autor.


