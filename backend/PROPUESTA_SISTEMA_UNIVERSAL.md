# SISTEMA UNIVERSAL DE ANÁLISIS DE CONTENIDO - RECUIVA

## PROBLEMA ACTUAL

El sistema está **sobre-ajustado al libro "El Collar de la Reina"**:
- Blacklist específica: "Collar", "Verdad", "Cierto", "Esper"
- Títulos de nobleza francesa: "conde", "cardenal", "señor"
- Extracción de nombres basada en mayúsculas + contexto verbal

**Resultado**: Funciona para literatura histórica, falla en PDFs técnicos/académicos/científicos.

---

## SOLUCIÓN: PRINCIPIOS LINGÜÍSTICOS UNIVERSALES

### 1. CONTEXTO ES REY (Universal NER Principles)

**En CUALQUIER idioma, las entidades siguen patrones universales:**

```
PATRÓN: [INDICADOR] + [ENTIDAD] + [CONTEXTO_VERBAL]

Ejemplos:
- "El doctor García estudió medicina"
  → Indicador: "doctor" (título profesional)
  → Entidad: "García"
  → Contexto: "estudió" (verbo de acción)

- "La proteína BRCA1 regula el ciclo celular"
  → Indicador: "proteína" (tipo de entidad)
  → Entidad: "BRCA1"
  → Contexto: "regula" (verbo científico)

- "El algoritmo QuickSort ordena elementos"
  → Indicador: "algoritmo" (tipo de entidad)
  → Entidad: "QuickSort"
  → Contexto: "ordena" (verbo técnico)
```

### 2. TIPOS DE ENTIDADES UNIVERSALES

**NO clasificar por dominio (literatura/ciencia/técnico).**  
**Clasificar por FUNCIÓN LINGÜÍSTICA:**

```python
ENTITY_TYPES = {
    "PERSON": {
        "indicators": ["señor", "doctor", "profesor", "capitán", ...],
        "context_verbs": ["dijo", "pensó", "fue", "hizo", ...],
        "capitalization": True,
        "min_words": 2
    },
    
    "CONCEPT": {
        "indicators": ["teoría", "ley", "principio", "concepto", ...],
        "context_verbs": ["explica", "define", "establece", ...],
        "capitalization": False,
        "min_words": 1
    },
    
    "OBJECT": {
        "indicators": ["proteína", "enzima", "compuesto", "molécula", ...],
        "context_verbs": ["contiene", "produce", "actúa", "forma", ...],
        "capitalization": True/False,
        "min_words": 1
    },
    
    "PROCESS": {
        "indicators": ["proceso", "método", "técnica", "algoritmo", ...],
        "context_verbs": ["realiza", "ejecuta", "implementa", ...],
        "capitalization": True/False,
        "min_words": 1
    },
    
    "LOCATION": {
        "indicators": ["ciudad", "país", "región", "lugar", ...],
        "context_verbs": ["se encuentra", "está situado", "ubicado", ...],
        "capitalization": True,
        "min_words": 1
    },
}
```

### 3. ALGORITMO UNIVERSAL DE EXTRACCIÓN

```python
def extract_entities_universal(text: str) -> List[Entity]:
    """
    Extrae entidades usando SOLO principios lingüísticos universales.
    NO depende del dominio del texto.
    """
    
    entities = []
    sentences = split_sentences(text)
    
    for sentence in sentences:
        tokens = tokenize(sentence)
        pos_tags = get_pos_tags(tokens)  # Part-of-Speech
        
        # PASO 1: Buscar patrones [INDICADOR + ENTIDAD]
        for i, token in enumerate(tokens):
            if token.lower() in ALL_INDICATORS:
                # Siguiente token(s) es la entidad
                entity_tokens = extract_next_capitalized_sequence(tokens, i+1)
                
                if is_valid_entity(entity_tokens):
                    # PASO 2: Verificar contexto verbal
                    verb_context = find_verb_in_window(tokens, i, window=5)
                    
                    if verb_context and not is_function_word(entity_tokens[0]):
                        entities.append(Entity(
                            text=" ".join(entity_tokens),
                            type=infer_type_from_indicator(token),
                            confidence=calculate_confidence(entity_tokens, verb_context)
                        ))
        
        # PASO 3: Buscar capitalizados SIN indicador pero CON verbo
        capitalized_sequences = find_capitalized_sequences(tokens)
        
        for seq in capitalized_sequences:
            if seq not in [e.text for e in entities]:  # No duplicar
                verb_context = find_verb_in_window(tokens, seq.start, window=5)
                
                if verb_context and len(seq.tokens) >= 2:
                    # Probablemente nombre propio (PERSON o LOCATION)
                    entities.append(Entity(
                        text=" ".join(seq.tokens),
                        type="PERSON_OR_LOCATION",
                        confidence=0.7  # Menor certeza sin indicador
                    ))
    
    return filter_and_deduplicate(entities)
```

### 4. VALIDACIÓN MULTI-NIVEL

```python
def is_valid_entity(tokens: List[str]) -> bool:
    """Validación INDEPENDIENTE del dominio"""
    
    # Nivel 1: Longitud
    if len(tokens) == 0:
        return False
    
    # Nivel 2: Fragmentos inválidos (universales)
    invalid_fragments = {'de', 'del', 'la', 'el', 'y', 'o', 'para'}
    if tokens[0].lower() in invalid_fragments:
        return False
    
    # Nivel 3: Palabras funcionales (universales)
    if is_function_word(tokens[0]):
        return False
    
    # Nivel 4: Longitud mínima por palabra
    if any(len(t) < 2 for t in tokens):
        return False
    
    # Nivel 5: NO contiene solo números
    if all(t.isdigit() for t in tokens):
        return False
    
    return True


def is_function_word(word: str) -> bool:
    """Palabras funcionales que NUNCA son entidades (español universal)"""
    FUNCTION_WORDS = {
        # Artículos
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        
        # Preposiciones
        'a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde',
        'en', 'entre', 'hacia', 'hasta', 'para', 'por', 'según',
        'sin', 'sobre', 'tras',
        
        # Conjunciones
        'y', 'e', 'ni', 'que', 'o', 'u', 'pero', 'mas', 'sino',
        'como', 'cuando', 'donde', 'porque', 'pues', 'si',
        
        # Pronombres
        'yo', 'tú', 'él', 'ella', 'nosotros', 'ellos', 'ellas',
        'me', 'te', 'se', 'nos', 'lo', 'la', 'le',
        'este', 'ese', 'aquel', 'esto', 'eso', 'aquello',
        
        # Adverbios comunes
        'muy', 'más', 'menos', 'también', 'tampoco', 'sí', 'no',
        'nunca', 'siempre', 'aquí', 'ahí', 'allí', 'bien', 'mal',
    }
    
    return word.lower() in FUNCTION_WORDS
```

---

## ESTRATEGIA DE IMPLEMENTACIÓN

### FASE 1: Crear `universal_ner.py` (NUEVO ARCHIVO)

```python
# backend/universal_ner.py

"""
Named Entity Recognition UNIVERSAL
Basado en principios lingüísticos independientes del dominio
"""

class UniversalNER:
    def __init__(self):
        self.indicators = load_universal_indicators()
        self.function_words = load_function_words()
        self.verb_patterns = load_verb_patterns()
    
    def extract_entities(self, text: str) -> List[Entity]:
        """Extrae entidades de CUALQUIER tipo de texto"""
        pass
    
    def classify_entity_type(self, entity: str, context: str) -> str:
        """Clasifica entidad basándose en contexto, NO en dominio"""
        pass
```

### FASE 2: Modificar `content_analyzer.py`

```python
# backend/content_analyzer.py

from universal_ner import UniversalNER

class ContentAnalyzer:
    def __init__(self):
        self.ner = UniversalNER()  # ← USAR NUEVO SISTEMA
    
    def _extract_entities(self, text: str) -> List[str]:
        entities = self.ner.extract_entities(text)
        return [e.text for e in entities if e.confidence >= 0.6]
```

### FASE 3: Actualizar `question_generator.py`

```python
# backend/question_generator.py

def _generate_intelligent_question(self, analysis, chunk_text):
    """Genera preguntas basándose en TIPO DE ENTIDAD, no dominio"""
    
    entities = analysis.key_entities
    entity_types = [e.type for e in entities]
    
    if "PERSON" in entity_types:
        # Pregunta sobre personas
        persons = [e for e in entities if e.type == "PERSON"]
        return f"¿Quién fue {persons[0]} y qué papel desempeñó?"
    
    elif "CONCEPT" in entity_types:
        # Pregunta sobre conceptos
        concepts = [e for e in entities if e.type == "CONCEPT"]
        return f"Define el concepto de {concepts[0]} según el texto"
    
    elif "PROCESS" in entity_types:
        # Pregunta sobre procesos
        processes = [e for e in entities if e.type == "PROCESS"]
        return f"Explica cómo funciona el proceso de {processes[0]}"
    
    # ...más tipos
```

---

## VENTAJAS DEL SISTEMA UNIVERSAL

| Aspecto | Sistema Actual | Sistema Universal |
|---------|----------------|-------------------|
| **Dominio** | Literatura histórica | CUALQUIER PDF |
| **Mantenimiento** | Agregar blacklist manualmente | Principios lingüísticos estables |
| **Precisión** | Alta en "Collar Reina", baja en otros | Media-alta en TODOS |
| **Escalabilidad** | Requiere ajustes por dominio | Funciona out-of-the-box |
| **Comprensión** | Reglas ad-hoc | Reglas lingüísticas claras |

---

## EJEMPLOS DE USO

### Texto Literario (Actual funciona)
```
"El conde de Dreux-Soubise visitó a María Antonieta"
→ PERSON: "conde de Dreux-Soubise" (indicador: "conde", verbo: "visitó")
→ PERSON: "María Antonieta" (capitalized, verbo: "visitó")
```

### Texto Científico (Actual falla)
```
"La proteína p53 regula la apoptosis celular"
→ OBJECT: "proteína p53" (indicador: "proteína", verbo: "regula")
→ PROCESS: "apoptosis celular" (sustantivo + adjetivo, verbo: "regula")
```

### Texto Técnico (Actual falla)
```
"El algoritmo QuickSort ordena elementos en O(n log n)"
→ PROCESS: "algoritmo QuickSort" (indicador: "algoritmo", verbo: "ordena")
→ CONCEPT: "O(n log n)" (notación matemática)
```

---

## PRÓXIMOS PASOS

1. ✅ **Documentar problema** (este archivo)
2. ⏳ **Crear `universal_ner.py`** con extracción basada en contexto
3. ⏳ **Refactorizar `content_analyzer.py`** para usar nuevo sistema
4. ⏳ **Actualizar `question_generator.py`** para tipos de entidad universales
5. ⏳ **Testear con 3 dominios diferentes**:
   - Literatura: "El Collar de la Reina" ✓
   - Ciencia: "Biología Molecular Campbell" 
   - Técnico: "Introduction to Algorithms (CLRS)"

---

## REFERENCIAS CONSULTADAS

- **spaCy NER**: https://spacy.io/usage/linguistic-features#named-entities
- **Python re module**: https://docs.python.org/3/library/re.html
- **Universal Dependencies**: https://universaldependencies.org/
- **Principios de NLP**: No usar modelos pre-entrenados, solo reglas lingüísticas

---

**Autor**: Abel Jesús Moya Acosta  
**Fecha**: 10 de noviembre de 2025  
**Proyecto**: Recuiva - Sistema RAG funcional sin LLM externo
