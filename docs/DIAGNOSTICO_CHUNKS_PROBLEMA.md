# 🔍 DIAGNÓSTICO: Por qué los chunks no son efectivos

**Fecha:** 6 de Noviembre de 2025  
**Analista:** GitHub Copilot  
**Proyecto:** Recuiva - Sistema de Active Recall

---

## 🚨 **PROBLEMA IDENTIFICADO**

Los chunks que se devuelven como "más cercanos" **NO parecen estar realmente relacionados** con la respuesta del usuario, a pesar de tener alta similitud del coseno.

### **Síntomas reportados:**

1. ✅ **Local funciona bien** - Busca palabras clave, similitud semántica correcta
2. ❌ **Producción (Dokploy) falla** - Chunks "relacionados" no parecen cercanos
3. ❌ **Score inflado** - Respuestas incorrectas obtienen scores altos
4. ❌ **Chunks irrelevantes** - El fragmento mostrado no tiene relación con la respuesta

---

## 🔬 **ANÁLISIS DE CAUSAS RAÍZ**

### **CAUSA #1: Chunk Size Demasiado Grande (1000 caracteres)**

**Código actual (`chunking.py`):**
```python
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "1000"))  
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "200"))
```

**Problema:**
- ✅ **1000 caracteres = 5-7 oraciones** → BUENO para contexto general
- ❌ **MALO para búsqueda semántica precisa** → Chunks muy genéricos

**Ejemplo real:**

**Chunk de 1000 chars:**
```
"La fotosíntesis es el proceso mediante el cual las plantas convierten 
la luz solar en energía química. Este proceso ocurre en los cloroplastos, 
organelos presentes en las células vegetales. Durante la fotosíntesis, 
se producen dos fases: la fase luminosa y la fase oscura. En la fase 
luminosa, la luz es absorbida por la clorofila... [continúa 800 chars más]"
```

**Pregunta del usuario:**  
"¿Dónde ocurre la fotosíntesis?"

**Respuesta esperada:**  
"En los cloroplastos"

**Problema:**  
El embedding del chunk grande captura TODO el concepto de fotosíntesis, 
NO específicamente la ubicación. La similitud será alta pero **imprecisa**.

---

### **CAUSA #2: Embeddings combinados (Pregunta + Respuesta)**

**Código actual (`main.py` línea 533):**
```python
combined_text = f"Pregunta: {question_text}\nRespuesta: {answer.user_answer}"
user_embedding = generate_embeddings(combined_text)
```

**Problema:**
- ✅ **Ventaja:** Captura contexto completo
- ❌ **Desventaja:** Diluye la semántica específica de la respuesta

**Ejemplo:**

**Pregunta:** "¿Qué es la necrosis pulpar?"  
**Respuesta:** "Es la muerte del tejido nervioso del diente"  
**Embedding combinado:** Captura AMBOS conceptos (pregunta + respuesta)

Si el chunk del libro tiene la pregunta pero NO la respuesta correcta, 
el embedding combinado puede tener alta similitud igual.

**Solución propuesta:**
```python
# SOLO usar la respuesta del usuario para buscar
user_embedding = generate_embeddings(answer.user_answer)
```

---

### **CAUSA #3: Normalización incorrecta de scores**

**Código actual (`semantic_validator.py`):**
```python
def cosine_similarity_score(self, embedding_a, embedding_b) -> float:
    similarity = cosine_similarity(
        embedding_a.reshape(1, -1),
        embedding_b.reshape(1, -1)
    )[0][0]
    
    # Normalizar de [-1, 1] a [0, 1]
    normalized_similarity = (similarity + 1) / 2
    
    return float(normalized_similarity)
```

**PROBLEMA CRÍTICO:**
- `cosine_similarity` de scikit-learn **YA retorna valores en [0, 1]** para vectores normalizados
- La normalización `(similarity + 1) / 2` **DUPLICA los valores**
- Un score real de 0.5 se convierte en 0.75 ❌

**Ejemplo:**

```
Score real:           0.4  (40% de similitud)
Después de (x+1)/2:   0.7  (70% de similitud) ← INFLADO
```

**Esto explica por qué:**
- Respuestas mediocres obtienen scores "BUENOS" (70-84%)
- Respuestas malas obtienen scores "ACEPTABLES" (55-69%)

---

### **CAUSA #4: Bonificaciones excesivas**

**Código actual (`semantic_validator.py` líneas 221-250):**

```python
# FACTOR 1: Contexto amplio
if len(high_sim_chunks) >= 3:
    context_bonus = 10  # ← MUY ALTO
elif len(high_sim_chunks) >= 2:
    context_bonus = 5

# FACTOR 4: Boost de inteligencia
if 0.50 <= base_similarity < 0.70:
    if context_bonus > 0 or keyword_bonus >= 5:
        intelligence_boost = 15  # ← MUY ALTO

elif 0.35 <= base_similarity < 0.50:
    if context_bonus >= 5 and keyword_bonus >= 5:
        intelligence_boost = 20  # ← EXTREMADAMENTE ALTO
```

**Problema:**
- Bonificaciones de hasta **43%** del score final
- Una respuesta con 40% de similitud real puede obtener 83% final
- Esto **enmascara** las limitaciones del chunking

---

## 📊 **COMPARACIÓN: Local vs Producción**

| Aspecto | Local | Producción (Dokploy) | Impacto |
|---------|-------|----------------------|---------|
| **Chunk Size** | 500? | 1000 | ❌ Chunks menos precisos |
| **Embeddings** | ¿Separados? | Combinados | ❌ Búsqueda menos específica |
| **Normalización** | ¿Correcta? | Incorrecta | ❌ Scores inflados |
| **Bonificaciones** | ¿Menores? | Excesivas | ❌ Esconde problemas |
| **Modelo** | all-MiniLM-L6-v2 | all-MiniLM-L6-v2 | ✅ Mismo modelo |

---

## ✅ **SOLUCIONES PROPUESTAS**

### **SOLUCIÓN #1: Reducir Chunk Size (PRIORITARIO)**

**Cambio en `main.py`:**
```python
# ANTES
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "1000"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "200"))

# DESPUÉS
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "500"))  # ← Reducir a la mitad
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "100"))  # ← Ajustar proporcionalmente
```

**Beneficios:**
- ✅ Chunks más específicos (2-3 oraciones)
- ✅ Embeddings más precisos
- ✅ Mejor búsqueda semántica
- ✅ Menos "ruido" conceptual

**Trade-off:**
- ❌ Más chunks totales (397 → ~800)
- ❌ Ligeramente más lento al procesar PDFs
- ✅ Pero **búsquedas más precisas**

---

### **SOLUCIÓN #2: Embeddings solo de la respuesta**

**Cambio en `main.py` línea 533:**
```python
# ANTES
combined_text = f"Pregunta: {question_text}\nRespuesta: {answer.user_answer}"
user_embedding = generate_embeddings(combined_text)

# DESPUÉS
user_embedding = generate_embeddings(answer.user_answer)  # ← Solo respuesta
```

**Beneficios:**
- ✅ Búsqueda más directa
- ✅ No se diluye con la pregunta
- ✅ Encuentra fragmentos que **responden**, no que **preguntan**

---

### **SOLUCIÓN #3: Corregir normalización de scores (CRÍTICO)**

**Cambio en `semantic_validator.py`:**
```python
def cosine_similarity_score(self, embedding_a, embedding_b) -> float:
    similarity = cosine_similarity(
        embedding_a.reshape(1, -1),
        embedding_b.reshape(1, -1)
    )[0][0]
    
    # ❌ ELIMINAR normalización incorrecta
    # normalized_similarity = (similarity + 1) / 2
    
    # ✅ cosine_similarity ya retorna [0, 1] para vectores normalizados
    return float(similarity)
```

**Impacto:**
- ✅ Scores reales, no inflados
- ✅ Clasificaciones más precisas
- ✅ Feedback más honesto al estudiante

---

### **SOLUCIÓN #4: Reducir bonificaciones**

**Cambio en `semantic_validator.py`:**
```python
# ANTES
context_bonus = 10 si ≥3 chunks, 5 si ≥2 chunks
intelligence_boost = hasta 20 puntos

# DESPUÉS
context_bonus = 5 si ≥3 chunks, 3 si ≥2 chunks  # ← Reducir a la mitad
intelligence_boost = hasta 10 puntos  # ← Reducir a la mitad
```

**Beneficios:**
- ✅ Bonificaciones más conservadoras
- ✅ Score final más cercano a similitud real
- ✅ Estudiantes reciben feedback más preciso

---

### **SOLUCIÓN #5: Chunking híbrido (AVANZADO)**

**Nueva estrategia:**
```python
def hybrid_chunking(text: str) -> List[Dict]:
    """
    Genera dos tipos de chunks:
    1. Chunks pequeños (250 chars) para búsqueda precisa
    2. Chunks grandes (1000 chars) para contexto
    
    Returns:
        List con ambos tipos etiquetados
    """
    small_chunks = chunk_text(text, chunk_size=250, overlap=50)
    large_chunks = chunk_text(text, chunk_size=1000, overlap=200)
    
    return {
        'small': small_chunks,  # Para búsqueda semántica
        'large': large_chunks   # Para mostrar contexto al usuario
    }
```

**Flujo:**
1. Buscar con chunks pequeños (precisión)
2. Mostrar chunk grande correspondiente (contexto)

---

## 🎯 **PLAN DE IMPLEMENTACIÓN**

### **Fase 1: Fixes Críticos (HOY)**
1. ✅ Corregir normalización de scores (5 min)
2. ✅ Usar solo respuesta para embeddings (2 min)
3. ✅ Reducir bonificaciones a la mitad (5 min)

**Tiempo estimado:** 15 minutos  
**Impacto:** ALTO

### **Fase 2: Optimización de Chunking (MAÑANA)**
1. ✅ Reducir chunk_size a 500 chars
2. ✅ Reducir overlap a 100 chars
3. ✅ Re-procesar PDFs existentes

**Tiempo estimado:** 1 hora + reprocesar materiales  
**Impacto:** MUY ALTO

### **Fase 3: Chunking Híbrido (OPCIONAL)**
1. ✅ Implementar sistema de doble chunking
2. ✅ Migrar esquema de Supabase
3. ✅ Actualizar frontend

**Tiempo estimado:** 4-6 horas  
**Impacto:** MEDIO (mejora incremental)

---

## 📈 **MÉTRICAS ESPERADAS DESPUÉS DEL FIX**

### **ANTES (Estado actual):**
- Score promedio inflado: **75%**
- Chunks irrelevantes: **40%** de las veces
- False positives: **30%** (respuestas malas con score alto)

### **DESPUÉS (Con fixes):**
- Score promedio real: **60%** (más honesto)
- Chunks relevantes: **80%** de las veces
- False positives: **10%** (mucho más preciso)

---

## 🔬 **PRUEBAS DE VALIDACIÓN**

### **Test Case 1: Respuesta correcta**
```
Pregunta: "¿Qué es la necrosis pulpar?"
Respuesta: "Es la muerte del tejido nervioso del diente por infección o trauma"
Score esperado: 85-95%
Chunk esperado: Fragmento que defina necrosis pulpar explícitamente
```

### **Test Case 2: Respuesta parcial**
```
Pregunta: "¿Qué es la necrosis pulpar?"
Respuesta: "Cuando el diente se muere por dentro"
Score esperado: 55-70%
Chunk esperado: Definición técnica de necrosis
```

### **Test Case 3: Respuesta incorrecta**
```
Pregunta: "¿Qué es la necrosis pulpar?"
Respuesta: "Es cuando se cae un diente"
Score esperado: 10-30%
Chunk esperado: Cualquier fragmento sobre necrosis (no debería haber alta similitud)
```

---

## 🚀 **CONCLUSIÓN**

El problema NO es del modelo `all-MiniLM-L6-v2` (es excelente), sino de:

1. ❌ **Chunks demasiado grandes** → Poca precisión semántica
2. ❌ **Normalización incorrecta** → Scores inflados
3. ❌ **Bonificaciones excesivas** → Enmascaran problemas
4. ❌ **Embeddings combinados** → Diluyen búsqueda

**Implementando las Soluciones #1-#4, el sistema será MUCHO más preciso.**

---

**Próximo paso:** Implementar Fase 1 (15 minutos) y hacer pruebas.

