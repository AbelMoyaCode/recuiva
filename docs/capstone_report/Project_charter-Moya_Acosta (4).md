**CARTA DEL PROYECTO – Taller Integrador 1**

INFORMACIÓN GENERAL DEL PROYECTO

|NOMBRE DEL PROYECTO|GERENTE DE PROYECTO|PATROCINADOR DEL PROYECTO|||
| :- | :-: | :-: | :- | :- |
|Desarrollo de una aplicación web de estudio basada en Active Recall con **validación semántica híbrida** e integración de uso mínimo de IA generativa: **Recuiva**|` `Walter Cueva Chavez|` `Walter Cueva Chavez|||
|MIEMBROS|ROL|TELËFONO/CORREO|||
|` `Abel Moya Acosta|Project Manager|+51943201120|amoyaa2@upao.edu.pe||
|Abel Moya Acosta|Scrum Master|+51943201120|amoyaa2@upao.edu.pe||

VISIÓN GENERAL DEL PROYECTO

|<p>PROBLEMA </p><p>O PROBLEMA </p>|“"No existe un sistema web que valide automáticamente la validación semántica de respuestas de Active Recall, contrastándolas con material fuente mediante **embeddings** + **búsqueda vectorial** + **validación semántica híbrida** (BM25 + Cosine Similarity + Coverage), que permita recuperar pasajes relevantes y puntuar la coherencia de la respuesta del usuario con métricas objetivas, sin depender de corrección manual.".”|
| :- | - |
|<p>PROPÓSITO </p><p>DEL PROYECTO</p>|Desarrollar un MVP de aplicación web que permita crear bancos de preguntas y sesiones de práctica de Active Recall (sin metáfora de “flashcards”), con **sugerencias de preguntas por IA de uso mínimo y siempre editables por el usuario**.<br>**Enfoque del MVP:** **coherencia semántica**, **recuperación** y **validación** de respuestas a partir del material fuente (PDFs).|
|<p>NEGOCIO </p><p>CASO</p>|<p>` `El proyecto aporta **valor académico** porque:</p><p>- **Mejora el desempeño** de los estudiantes en el estudio y exámenes al aumentar la retención de aprendizaje.</p><p>- **Ahorra tiempo** de estudio gracias a sesiones breves y enfocadas.</p><p>- **Diferenciador tecnológico (IA)**: Validación semántica híbrida única (no existe en Anki/Quizlet que usan múltiple opción o corrección manual)</p><p>- **IA como apoyo, NO como generador**: El sistema recupera fragmentos del PDF, contrasta y valida; **no responde por el usuario** (anti-pasividad cognitiva).</p>|
|OBJETIVOS / MÉTRICAS|<p>**OBJETIVOS:**</p><p>**OB:** Desarrollar un MVP de aplicación web que permita la práctica de Active Recall mediante **validación semántica automática** utilizando **embeddings** y **base de datos vectorial** para contrastar respuestas del usuario con fragmentos específicos de documentos PDF.</p><p>**O1: Sistema de embeddings y recuperación→** Implementar un sistema de embeddings funcional para análisis semántico automatizado de respuestas del usuario, contrastando con fragmentos específicos del documento fuente utilizando Sentence-Transformers y base de datos vectorial (Supabase pgvector).</p><p>**O2: Validación semántica híbrida→** Desarrollar un pipeline de validación semántica (HybridValidator) que reconozca sinónimos, variaciones contextuales y respuestas parcialmente correctas mediante análisis vectorial avanzado (30% BM25 + 50% Cosine </p><p>Similarity + 20% Coverage), logrando alta precisión de coherencia.</p><p>**O3: Generación asistida de preguntas por IA→** Integrar un módulo de generación de preguntas desde texto mediante Groq API (Llama 3.1 8B) con capacidad de edición manual, garantizando que las sugerencias sean editables por el usuario antes de </p><p>guardarlas (IA como apoyo, no como generador final).</p><p>**O4 – Sistema de repetición espaciada (Spaced Repetition) →** Implementar un algoritmo de repetición espaciada basado en SM-2 (SuperMemo 2) que calcule automáticamente los intervalos de repaso según el desempeño del usuario, permitiendo sesiones de repaso personalizadas con preguntas priorizadas por dificultad y tiempo transcurrido.</p><p>**MÉTRICAS DE VALIDACIÓN SEMÁNTICA Y RECUPERACIÓN:**</p><p>• **Cobertura de embeddings:** ≥ 95% de fragmentos (chunks) del material PDF generan embeddings válidos de 384 dimensiones usando Sentence-Transformers all-MiniLM-L6-v2, sin errores de procesamiento.</p><p>• **Precisión de recuperación top-3:** ≥ 85% de consultas recuperan el fragmento semánticamente más relevante dentro de los 3 primeros resultados mediante búsqueda vectorial (cosine similarity  en Supabase pgvector), validado contra dataset de prueba con 50 pares pregunta-fragmento.</p><p>• **Tiempo de validación:** ≤ 500ms desde el envío de la respuesta hasta el retorno del score HybridValidator (30% BM25 + 50% Cosine Similarity + 20% Coverage) y fragmentos recuperados.</p><p>• **Precisión del clasificador HybridValidator:** ≥ 75% de concordancia entre clasificación automática (correcta/parcial/incorrecta) y evaluación manual en 100 casos de prueba anotados (ground truth).</p><p>• **Reconocimiento de variaciones semánticas:** ≥ 80% de respuestas de prueba que utilizan sinónimos o paráfrasis del contenido original obtienen score ≥ 70/100 en la validación semántica (dataset de prueba con 20 variaciones).</p><p><h3>**Base académica para justificar el uso de embeddings y recuperación semántica en Active Recall:**</h3></p><p>- **Karpicke, J. D., & Roediger, H. L. III. (2008).** *The critical importance of retrieval for learning*. (Base teórica del Active Recall).</p><p>- **Reimers, N., & Gurevych, I. (2019).** *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. (Justifica el uso del modelo all-MiniLM-L6-v2 para comparar similitud semántica).</p><p>- **Lewis, P., et al. (2020).** *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. (Base teórica del sistema RAG).</p><p>- **Rayo Mosquera, J. S., et al. (2025).** *A Hybrid Approach to Information Retrieval and Answer Generation for Regulatory Texts*. (El cual justifica científicamente la técnica híbrida: integración de BM25 + Sentence Transformers para mejorar la precisión).</p><p></p>|
|ENTREGABLES ESPERADOS|<p>- Sistema de embeddings funcional para contrastar respuestas del usuario con fragmentos del documento fuente.</p><p>- Base de datos vectorial implementada (Supabase pgvector) para almacenamiento eficiente y recuperación por similitud semántica.</p><p>- Fragmentación inteligente de documentos PDF en chunks procesables de 200-300 palabras (chunking semántico con context anchors) para optimizar recuperación.</p><p>- Múltiples herramientas de Active Recall integradas: **sugerencias de preguntas por IA (editables)**, **validación semántica híbrida**, **repetición espaciada**.</p><p>- Módulo de validación semántica (HybridValidator reconoce sinónimos, variaciones y respuestas parciales).</p><p>- **Dashboard** con métricas de **validación, recuperación** y evolución de respuestas.</p><p>- Entrenador cognitivo" con IA mínima: el sistema **no genera preguntas ni respuestas, solo valida y contrasta con material fuente** (recupera, contrasta y valida).</p>|




ALCANCE DEL PROYECTO

|<p>DENTRO </p><p>ALCANCE</p>|<p>• **Sistema de embeddings** para análisis semántico automatizado de respuestas del usuario comparado con contenido del documento fuente (Sentence-Transformers all-MiniLM-L6-v2, 384 dimensiones).</p><p>• **Base de datos vectorial Supabase pgvector (extensión PostgreSQL) para**</p><p>almacenamiento eficiente y recuperación por similitud semántica de</p><p>fragmentos documentales mediante búsqueda vectorial (match\_embeddings).</p><p>• **Fragmentación inteligente de documentos PDF** en chunks procesables palabras con solapamiento (overlap) de 50 palabras paraoptimizar recuperación y mantener contexto semántico entre chunks.</p><p>• **Pipeline completo de procesamiento de texto mediante módulos propios:**</p><p>- Chunking semántico con PyPDF2 y text\_normalizer.py</p><p>- Vectorización con Sentence-Transformers (all-MiniLM-L6-v2)</p><p>- Validación semántica con hybrid\_validator.py (BM25 + Cosine + Coverage)</p><p></p><p>• **Validación semántica híbrida (HybridValidator)** con tres métricas complementarias: 30% BM25 (keywords) + 50% Cosine Similarity (similitud vectorial) + 20% Coverage (cobertura de conceptos). Reconoce sinónimos y variaciones contextuales automáticamente.</p><p>• **Generación asistida de preguntas por IA** mediante Groq API (Llama 3.1 8B, gratuito) desde texto editable, con capacidad de edición manual antes de guardar (IA como apoyo, no generador automático).</p><p>• **Sistema de repetición espaciada** basado en algoritmo SM-2 que calcula intervalos de repaso según desempeño del usuario.</p><p>• **Múltiples herramientas de Active Recall integradas**: sugerencias de preguntas IA (editables), validación semántica automática, repetición espaciada.</p><p>• **Contrastación automática de respuestas** del usuario versus fragmentos específicos del documento fuente con scoring multi-métrica (HybridValidator).</p><p>• **Dashboard de métricas en tiempo real** mostrando coherencia semántica, tasa de recuperación, precisión de clasificación y evolución longitudinal del usuario.</p><p>• **• "Entrenador cognitivo"** con uso mínimo de IA: El sistema recupera fragmentos, contrasta, valida y retroalimenta. Genera sugerencias de preguntas mediante IA (editables por el usuario), pero no genera respuestas automáticamente**.**</p><p></p>|
| :- | - |
|<p>AFUERA </p><p>DE ALCANCE</p>|<p></p><p>• Integraciones con LMS o plataformas educativas institucionales.</p><p>• Aplicaciones móviles nativas completas (solo web responsive).</p><p>• Comunidad para compartir bancos de preguntas entre usuarios.</p><p>• Sistema de gamificación avanzado (badges, rankings).</p><p>• Soporte multiidioma (solo español en MVP).</p><p>• Fine-tuning específico del modelo de embeddings.</p>|







CALENDARIO (Dev: SCRUM y GEST: Kanban)

|**EVENTO SCRUM**|**INICIO**|**FIN**|**Hitos/Entregables**|**Historias de Usuario/Tareas Clave**|
| :-: | :-: | :-: | :-: | :-: |
|**📋 SPRINT 0: INCEPTION & SETUP**|**Sep 15, 2025**|**Sep 21, 2025**|• Product Backlog inicial creado<br>• Arquitectura técnica definida<br>• Repos y entorno configurado<br>• Definition of Done (DoD) establecido|<p>**EN-002**: Estructura de repos<br>**SP-003**: Modelo de embeddings (all-MiniLM-L6-v2)<br>**SP-002**: BD vectorial (Supabase pgvector)</p><p>**HU-001**: Registro/Login básico</p>|
|**🔄 SPRINT PLANNING 1**|**Sep 22, 2025**|**Sep 22, 2025**|<p>• Sprint Backlog definido (14 tareas)</p><p>• Estimaciones confirmadas (64 SP)<br>• Criterios de aceptación validados</p>|Selección de HU-001 a SP-001 (Sprint 1)|
|**⚡ SPRINT 1: MVP BÁSICO**|**Sep 15, 2025**|**Oct 15, 2025**|• Sistema de embeddings funcionando<br>• Chunking de PDFs operativo<br>• Validación semántica básica<br>• Active Recall flow completo<br>• Dashboard v1|**HU-002**: Crear set desde PDF<br>**HU-009**: Cargar PDF y chunking<br>**HU-011**: Validar respuesta vs fragmentos<br>**HU-003**: Practicar (intento→revelo→califico)<br>**HU-012**: Mostrar explicación (fragmento)<br>**HU-004**: Ver resultado de sesión<br>**DO-001**: Documentar API básica<br>**DO-003**: Dataset ground truth (20-30 casos)<br>**SP-001**: Hosting (Dokploy/DuckDNS)|
|**📊 DAILY STANDUP (SPRINT 1)**|**Sep 23, 2025**|**Oct 14, 2025**|Reuniones diarias 15 min:<br>• ¿Qué hice ayer?<br>• ¿Qué haré hoy?<br>• ¿Impedimentos?|Seguimiento continuo de tareas en Notion Kanban|
|**🔍 SPRINT REVIEW 1**|**Oct 15, 2025**|**Oct 15, 2025**|• Demo del MVP básico funcionando<br>• Feedback del Product Owner (Walter Cueva)<br>• Validación de flujo Active Recall|Presentación de HU-003, HU-011, HU-012, HU-004 funcionando|
|**🧠 SPRINT RETROSPECTIVE 1**|**Oct 15, 2025**|**Oct 15, 2025**|• ¿Qué salió bien?<br>• ¿Qué mejorar?<br>• Acciones de mejora para Sprint 2|Ajustes en chunking, optimización de embeddings|
|**🔄 SPRINT PLANNING 2**|**Oct 16, 2025**|**Oct 16, 2025**|• Sprint Backlog definido (8 tareas)<br>• Estimaciones confirmadas (57 SP)<br>• Priorización de HybridValidator|Selección de HU-010 a EN-003 (Sprint 2)|
|**⚡ SPRINT 2: VALIDACIÓN HÍBRIDA + IA**|**Oct 16, 2025**|**Nov 12, 2025**|• HybridValidator implementado (30% BM25 + 50% Cosine + 20% Coverage)<br>• Groq API integrado (Llama 3.1 8B)<br>• Repetición espaciada (SM-2)<br>• Dashboard de métricas completo|**HU-010**: Indexar embeddings en BD vectorial<br>**PN-003**: Seguridad básica (JWT/sesión)<br>**RN-001**: Implementar HybridValidator [CRÍTICO]<br>**HU-014**: Implementar repetición espaciada (SM-2)<br>**HU-013**: Generar preguntas con Groq API<br>**HU-015**: Vista de repasos programados<br>**HU-005**: Landing con CTA<br>**EN-003**: Dashboard de métricas|
|**📊 DAILY STANDUP (SPRINT 2)**|**Oct 17, 2025**|**Nov 11, 2025**|Reuniones diarias 15 min|Seguimiento de RN-001 (alta complejidad 13 SP)|
|**🔍 SPRINT REVIEW 2**|**Nov 12, 2025**|**Nov 12, 2025**|• Demo de validación semántica híbrida funcionando<br>• Demo de generación de preguntas con IA<br>• Demo de repetición espaciada<br>• Feedback del Product Owner|Presentación de RN-001, HU-013, HU-014 en vivo|
|**🧠 SPRINT RETROSPECTIVE 2**|**Nov 12, 2025**|**Nov 12, 2025**|• Lecciones aprendidas de HybridValidator<br>• Mejoras en integración Groq API<br>• Optimización de algoritmo SM-2|Ajustes para Sprint 3 de validación|
|**🔄 SPRINT PLANNING 3**|**Nov 13, 2025**|**Nov 13, 2025**|• Sprint Backlog definido (6 tareas)<br>• Estimaciones confirmadas (19 SP)<br>• Enfoque en KPIs y documentación|Selección de DO-004 a PN-004 (Sprint 3)|
|**⚡ SPRINT 3: PRUEBAS, VALIDACIÓN Y DOCUMENTACIÓN**|**Nov 13, 2025**|**Dec 3, 2025**|<p>• Scripts de KPIs creados<br>• Ground truth validado con 50 casos<br>• Métricas de validación semántica ≥80%</p><p>• Recall@k ≥85%<br>• README de métricas completo<br>• Informe Capstone académico</p>|**DO-004**: README de métricas<br>**PN-001**: KPI Validación semántica [CRÍTICO]<br>**PN-002**: KPI Recuperación (Recall@k) [CRÍTICO]<br>**DO-002**: KPI Repetición espaciada<br>**DO-005**: README actualizado con piloto<br>**PN-004**: Informe de validación final [CRÍTICO]|
|**📊 DAILY STANDUP (SPRINT 3)**|**Nov 14, 2025**|**Dec 2, 2025**|Reuniones diarias 15 min|Seguimiento de creación de scripts y documentación|
|**🔍 SPRINT REVIEW 3**|**Dec 3, 2025**|**Dec 3, 2025**|• Presentación de métricas finales<br>• Demo de KPIs calculados<br>• Presentación de informe académico<br>• Validación de tesis de suceso|Demostración de ≥80% validación semántica, ≥85% Recall@k|
|**🧠 SPRINT RETROSPECTIVE 3 (FINAL)**|**Dec 3, 2025**|**Dec 3, 2025**|• Retrospectiva de proyecto completo<br>• Lecciones aprendidas generales<br>• Recomendaciones para futuras iteraciones|Documentación de mejoras para versión 2.0|
|**🎯 RELEASE FINAL**|**Dec 3, 2025**|**Dec 3, 2025**|• Deployment en producción (api-recuiva.duckdns.org)<br>• URL pública accesible<br>• Documentación técnica completa|MVP Final de Recuiva v1.0 desplegado|
|**📄 CIERRE DEL PROYECTO**|**Dec 4, 2025**|**Dec 7, 2025**|<p>• Informe técnico de embeddings y métricas semánticas<br>• Entrega de Project Charter actualizado</p><p>• Presentación académica final<br>• Actas de reuniones y retrospectivas y de validación</p><p>• Presentación del proyecto completo</p><p></p>|Entrega al producto owner Walter Cueva Chávez|

RECURSOS

|EQUIPO DEL PROYECTO|<p></p><p>Abel Moya Acosta (PM, Scrum Master, desarrollo inicial).</p><p></p>|
| :- | :- |
|RECURSOS DE SOPORTE|Walter Cueva Chávez (Patrocinador / Asesor académico).|
|NECESIDADES ESPECIALES|<p>- Internet estable.</p><p>- Acceso (permiso) a estudiantes para pruebas piloto.</p><p></p>|

COSTOS

|**TIPO DE COSTO**|**NOMBRES DE PROVEEDORES / TRABAJADORES**|**PRECIO UNITARIO**|**CANTIDAD**|**IMPORTE**||
| :- | :- | :-: | :-: | :-: | :- |
|**Servicio**|Hosting web (Dokploy / Duckdns (subdominio) / Digital Ocean — free tier)|S/.0|1|S/.0||
|**Servicio**|Base de datos vectorial (Supabase – pgvector — free)|S/.0|1|S/.0||
|**Servicio**|Embeddings (Sentence-Transformers all-MiniLM-L6-v2 -free)|S/.0|1|S/.0||
|**Servicio**|Procesamiento PDF (PyPDF2 — free)|S/.0|1|S/.0||
|**Trabajo**|Desarrollo del MVP con validación semántica (**aporte del estudiante**)|S/.0|1|S/.0||
|**Suministros**||||||

||
| :- |

|||||||
| :- | :- | :-: | :-: | :- | :- |

|Internet y electricidad (recursos personales)|
| :- |

|||S/.100|1|S/.100||
| :- | :- | :-: | :-: | :- | :- |
|**Misceláneos**||||||

||
| :- |

|||||||
| :- | :- | :-: | :-: | :- | :- |

|Diseño UI (Figma — free tier)|
| :- |

|||S/.0|1|$0||
| :- | :- | :-: | :-: | :- | :- |
|COSTOS TOTALES||||S/.100||



BENEFICIOS Y CLIENTES

|PROPIETARIO DEL PROCESO|` `Equipo de Taller Integrador I.||||
| :- | - | :- | :- | :- |
|PRINCIPALES PARTES INTERESADAS|` `Estudiantes usuarios.||||
|CLIENTE FINAL|` `Estudiantes universitarios.||||
|BENEFICIOS ESPERADOS|<p>- **Ahorro de tiempo en estudio** mediante sesiones breves y enfocadas.</p><p>&emsp;- **Mayor motivación** gracias al **panel de resultados** (tablero de métricas que muestra progreso: coherencia semántica, tasa de recuperación, precisión y evolución longitudinal del usuario).</p><p>&emsp;- **Validación práctica del aprendizaje activo**, garantizando que las respuestas se contrasten con el material fuente y no solo con memoria superficial.</p>||||
|**TIPO DE PRESTACIÓN**|**BASE DE ESTIMACIÓN**|**MONTO ESTIMADO DEL BENEFICIO**|||
|**Ahorro de costes específicos**|No se requiere compra de software propietario ni licencias; se usa Sentence-Transformers (gratis), Supabase (free tier), Groq API (gratis), Dokploy (gratis), DuckDNS (gratis) y Digital Ocean en versión gratuita.|S/.0 (uso de free tier)|||
|**Ingresos mejorados**|No aplica a nivel académico; el beneficio se traduce en **valor académico** para estudiantes y universidad.|-|||
|**Mayor productividad (suave)**|Estudiantes dedican **menos tiempo a releer** con sesiones cortas de Active Recall. Se estima que pueden **reducir 20–30% del tiempo de estudio** (valor estimado cualitativo).|Valor intangible|||
|**Cumplimiento mejorado**|Mayor adherencia al plan de estudio al usar la app **≥80% de validación semántica** en respuestas validadas automáticamente (meta de validación técnica).|Valor intangible|||
|**Mejor toma de decisiones**|El **panel de resultados** en métricas permite al estudiante identificar sus áreas débiles y decidir en qué temas concentrar su estudio.|Valor intangible|||
|**Menos mantenimiento**|<p>La aplicación web está desplegada en infraestructura tecnológica gratuita (stack gratuito: </p><p>Sentence-Transformers + Supabase free tier + Groq API + Dokploy + Traefik + DuckDNS), lo que requiere **bajo mantenimiento** (sin dependencias de APIs de pago).</p>|$0|||
|**Otros costos evitados**|Se evitan gastos en materiales físicos (tarjetas de papel, impresiones) y se centraliza todo en digital.|Ahorro referencial: **S/ 30.00 – S/ 60.00** por semestre|||
||||BENEFICIO TOTAL|S/.30-60|


RIESGOS, LIMITACIONES Y SUPUESTOS

|RIESGOS|<p>- Complejidad de implementación de embeddings y Supabase pgvector con HybridValidator.</p><p>&emsp;- Precisión limitada en validación semántica por modelos no fine-tuneados específicamente para Active Recall.</p><p>&emsp;- Fragmentación deficiente de PDFs con formato complejo o tablas (requiere chunking semántico robusto).</p>|
| :- | - |
|RESTRICCIONES|<p>- Desarrollo individual (tiempo limitado).</p><p>&emsp;- Validaciones solo con grupo reducido de estudiantes.</p><p>&emsp;- ` `Dependencia de **Sentence-Transformers** (all-MiniLM-L6-v2) sin fine-tuning específico.</p><p>&emsp;- Procesamiento limitado a **PDFs** de máximo 10 páginas por eficiencia (chunking semántico).</p><p></p>|
|SUPOSICIONES|<p>- Los estudiantes tienen acceso a internet y dispositivos modernos.</p><p>&emsp;- La **infraestructura tecnológica gratuita** (stack gratuito: **Sentence-Transformers + Supabase free tier + Groq API + Dokploy +Digital Ocean + Traefik + DuckDNS**) es suficiente para el MVP.</p><p></p>|


|PREPARADO POR|TÍTULO|FECHA|
| :- | :- | :-: |
|` `Abel Moya Acosta| |04/09/2025 |

**REFERENCIAS/ANEXO:**

- Ahmed, A., Joorabchi, A., & Hayes, M. J. (2022). On the Application of Sentence Transformers to Automatic Short Answer Grading in Blended Assessment. *2022 33rd Irish Signals and Systems Conference (ISSC)*, 1–6. <https://www.researchgate.net/publication/362965124_On_the_Application_of_Sentence_Transformers_to_Automatic_Short_Answer_Grading_in_Blended_Assessment>
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. En *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1* (pp. 4171–4186). Association for Computational Linguistics. <https://aclanthology.org/N19-1423/>
- Karpicke, J. D., & Roediger, H. L. III. (2008). The critical importance of retrieval for learning. *Science, 319*(5865), 966–968. <https://doi.org/10.1126/science.1152408>
- Kaya, M., & Cicekli, I. (2024). A Hybrid Approach for Automated Short Answer Grading. *IEEE Access, 12*, 96332–96341. <https://ieeexplore.ieee.org/document/10577980>
- Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., Heinrich, H., Lewis, M., Yih, W., & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. En *Advances in Neural Information Processing Systems* (Vol. 33, pp. 9459–9474). Curran Associates, Inc. <https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html>
- Metzler, T., Ploeger, P. G., & Hees, J. (2024). Computer-Assisted Short Answer Grading Using Large Language Models and Rubrics. En *Proceedings of INFORMATIK 2024* (pp. 1383–1393). Gesellschaft für Informatik e.V. [https://doi.org/10.18420/inf2024_121](https://www.google.com/search?q=https://doi.org/10.18420/inf2024_121&authuser=3)
- Rayo Mosquera, J. S., De La Rosa Peredo, C. R., & Garrido Cordoba, M. (2025). A Hybrid Approach to Information Retrieval and Answer Generation for Regulatory Texts. En *Proceedings of the 1st Regulatory NLP Workshop* (pp. 31–35). Association for Computational Linguistics. <https://aclanthology.org/2025.regnlp-1.5/>
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. En *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing* (pp. 3982–3992). Association for Computational Linguistics. <https://aclanthology.org/D19-1410/>
- Roediger, H. L., & Butler, A. C. (2011). The critical role of retrieval practice in long-term retention. *Trends in Cognitive Sciences, 15*(1), 20–27. <https://doi.org/10.1016/j.tics.2010.09.003>



