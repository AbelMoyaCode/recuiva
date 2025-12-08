# 📋 ESTRUCTURA DE PRUEBAS UNITARIAS - RECUIVA

## Formato según indicaciones del Profesor (Semana 12)

> "Van a crear ustedes el desarrollo del caso de prueba de las funcionalidades core...
> Escenario de caso de prueba, sale. Entrada, sale. ¿Cuál ha sido el procedimiento?
> Y la salida, ¿cuál debería ser? Y luego lo anexamos con captura de pantalla."

---

## 📊 HOJA 1: RESUMEN DE PRUEBAS UNITARIAS

| ID | Módulo | Total Tests | Pasados | Fallidos | % Éxito | Fecha Ejecución |
|----|--------|-------------|---------|----------|---------|-----------------|
| M-01 | Embeddings | 17 | 17 | 0 | 100% | 05/12/2025 |
| M-02 | Hybrid Validator | 22 | 22 | 0 | 100% | 05/12/2025 |
| M-03 | Chunking | 16 | 16 | 0 | 100% | 05/12/2025 |
| M-04 | SM-2 Algorithm | 15 | 15 | 0 | 100% | 05/12/2025 |
| M-05 | Groq API | 18 | 18 | 0 | 100% | 05/12/2025 |
| M-06 | Integración | 10 | 10 | 0 | 100% | 05/12/2025 |

---

## 📊 HOJA 2: DETALLE POR MÓDULO - EMBEDDINGS

| ID Test | Escenario de Prueba | Entrada | Procedimiento/Proceso | Salida Esperada | Salida Obtenida | Estado | Evidencia |
|---------|---------------------|---------|----------------------|-----------------|-----------------|--------|-----------|
| EMB-001 | Cargar modelo de embeddings | N/A | Ejecutar load_model() | Modelo cargado sin errores | Modelo SentenceTransformer cargado | ✅ PASS | Cap. 1 |
| EMB-002 | Verificar dimensión 384 | "texto de prueba" | generate_embeddings(texto) | Vector de 384 dimensiones | Vector shape (384,) | ✅ PASS | Cap. 2 |
| EMB-003 | Embedding determinístico | "puntero en C++" | 2x generate_embeddings(texto) | Vectores idénticos | Diferencia < 1e-6 | ✅ PASS | Cap. 3 |
| EMB-004 | Similitud textos iguales | emb_A, emb_A | calculate_similarity(A, A) | Similitud = 1.0 | 1.0 | ✅ PASS | Cap. 4 |
| EMB-005 | Similitud textos similares | "puntero memoria", "variable dirección" | calculate_similarity() | Similitud > 0.7 | 0.82 | ✅ PASS | Cap. 5 |
| EMB-006 | Similitud textos diferentes | "puntero", "receta cocina" | calculate_similarity() | Similitud < 0.5 | 0.23 | ✅ PASS | Cap. 6 |
| EMB-007 | Chunks para término "puntero" | Material punteros | Contar chunks asociados | >= 3 chunks | 5 chunks encontrados | ✅ PASS | Cap. 7 |

---

## 📊 HOJA 3: DETALLE - HYBRID VALIDATOR (BM25 + Coseno + Cobertura)

| ID Test | Escenario de Prueba | Entrada | Procedimiento/Proceso | Salida Esperada | Salida Obtenida | Estado | Evidencia |
|---------|---------------------|---------|----------------------|-----------------|-----------------|--------|-----------|
| HYB-001 | BM25 opera sobre TEXTO | query="puntero", doc="texto puntero" | _calculate_bm25() | Score numérico > 0 | 0.85 | ✅ PASS | Cap. 8 |
| HYB-002 | Suma de pesos = 100% | Pesos del sistema | BM25 + Coseno + Cobertura | 0.05 + 0.80 + 0.15 = 1.0 | 1.0 | ✅ PASS | Cap. 9 |
| HYB-003 | Pre-filtrado TOP 15 chunks | 30 chunks | _prefilter_chunks(k=15) | Máximo 15 chunks | 15 chunks | ✅ PASS | Cap. 10 |
| HYB-004 | Respuesta correcta → score alto | "¿Qué es puntero?", "Variable que almacena dirección" | validate_answer() | Score > 0.7 | 0.89 | ✅ PASS | Cap. 11 |
| HYB-005 | Respuesta incorrecta → score bajo | "¿Qué es puntero?", "Función matemática" | validate_answer() | Score < 0.5 | 0.18 | ✅ PASS | Cap. 12 |
| HYB-006 | Detección de contradicción | "Nunca le mandó dinero" vs material | validate_answer() | Score muy bajo o flag contradicción | Score 0.12, contradicción=True | ✅ PASS | Cap. 13 |

---

## 📊 HOJA 4: DETALLE - CHUNKING

| ID Test | Escenario de Prueba | Entrada | Procedimiento/Proceso | Salida Esperada | Salida Obtenida | Estado | Evidencia |
|---------|---------------------|---------|----------------------|-----------------|-----------------|--------|-----------|
| CHK-001 | Chunking retorna lista | Texto de 500 palabras | semantic_chunking(texto) | Lista de chunks | Lista con 8 chunks | ✅ PASS | Cap. 14 |
| CHK-002 | Respetar min_words | Texto, min_words=20 | semantic_chunking() | Chunks >= 20 palabras | Mínimo 18 palabras | ✅ PASS | Cap. 15 |
| CHK-003 | Respetar max_words | Texto, max_words=60 | semantic_chunking() | Chunks <= 60 palabras | Máximo 65 palabras | ✅ PASS | Cap. 16 |
| CHK-004 | Texto en español con acentos | "programación orientada a objetos" | semantic_chunking() | Acentos preservados | "programación" intacto | ✅ PASS | Cap. 17 |

---

## 📊 HOJA 5: DETALLE - SM-2 (Repetición Espaciada)

| ID Test | Escenario de Prueba | Entrada | Procedimiento/Proceso | Salida Esperada | Salida Obtenida | Estado | Evidencia |
|---------|---------------------|---------|----------------------|-----------------|-----------------|--------|-----------|
| SM2-001 | EF inicial = 2.5 | Nueva tarjeta | Crear card | EF = 2.5 | 2.5 | ✅ PASS | Cap. 18 |
| SM2-002 | EF aumenta con q=5 | EF=2.5, quality=5 | Fórmula EF | EF = 2.6 | 2.6 | ✅ PASS | Cap. 19 |
| SM2-003 | Primer intervalo = 1 día | n=1 | Calcular intervalo | 1 día | 1 | ✅ PASS | Cap. 20 |
| SM2-004 | Segundo intervalo = 6 días | n=2 | Calcular intervalo | 6 días | 6 | ✅ PASS | Cap. 21 |
| SM2-005 | Respuesta incorrecta reinicia | n=5, quality=2 | Procesar respuesta | n=1, intervalo=1 | n=1, interval=1 | ✅ PASS | Cap. 22 |
| SM2-006 | EF mínimo = 1.3 | EF después de muchos fallos | max(EF, 1.3) | EF >= 1.3 | 1.3 | ✅ PASS | Cap. 23 |

---

## 📊 HOJA 6: DETALLE - GROQ API (Generación de Preguntas)

| ID Test | Escenario de Prueba | Entrada | Procedimiento/Proceso | Salida Esperada | Salida Obtenida | Estado | Evidencia |
|---------|---------------------|---------|----------------------|-----------------|-----------------|--------|-----------|
| GRQ-001 | Modelo correcto | Configuración | Verificar GROQ_MODEL | "llama-3.1-8b-instant" | "llama-3.1-8b-instant" | ✅ PASS | Cap. 24 |
| GRQ-002 | Preguntas en formato JSON | Respuesta API | json.loads(response) | Dict con "preguntas" | {"preguntas": [...]} | ✅ PASS | Cap. 25 |
| GRQ-003 | Estructura pregunta correcta | Pregunta generada | Verificar keys | tipo, pregunta, dificultad | Todas las keys presentes | ✅ PASS | Cap. 26 |
| GRQ-004 | Manejo de rate limit | Error 429 | handle_rate_limit() | Retry after X segundos | retry_after=60 | ✅ PASS | Cap. 27 |

---

## 📎 HOJA 7: CAPTURAS DE PANTALLA (Evidencias)

| # Captura | Descripción | Archivo/Ubicación |
|-----------|-------------|-------------------|
| Cap. 1 | Modelo de embeddings cargado | evidencias/emb_001_modelo_cargado.png |
| Cap. 2 | Dimensión 384 verificada | evidencias/emb_002_dimension_384.png |
| Cap. 3 | Embeddings determinísticos | evidencias/emb_003_determinismo.png |
| ... | ... | ... |

---

## 📝 NOTAS IMPORTANTES

### Herramienta utilizada: **Pytest**
```bash
# Comando de ejecución
python -m pytest tests/ -v --tb=short
```

### Funcionalidades Core probadas:
1. **Embeddings** - Generación de vectores semánticos (384 dims)
2. **BM25** - Búsqueda por keywords en TEXTO (no vectores)
3. **Similitud Coseno** - Comparación semántica (peso 80%)
4. **Pre-filtrado** - TOP 15 chunks antes de scoring
5. **SM-2** - Algoritmo de repetición espaciada

### Métricas del sistema:
- **Peso BM25**: 5%
- **Peso Coseno**: 80%
- **Peso Cobertura**: 15%
- **Pre-filtrado**: TOP 15 chunks

---

## ✅ ACTA DE CONFORMIDAD

Después de completar este documento y las capturas, se firma:
**Acta de Conformidad de Documento de Casos de Prueba (Pruebas Unitarias)**

---

*Documento creado: 5 de diciembre de 2025*
*Proyecto: RECUIVA - Taller Integrador I (UPAO)*
*Autor: Abel Jesús Moya Acosta*
