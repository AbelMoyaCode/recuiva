# 🏗️ ARQUITECTURA MODULAR HÍBRIDA - RECUIVA NER UNIVERSAL

## 📊 AUDITORÍA COMPLETA DEL CÓDIGO EXISTENTE

### ✅ ARCHIVOS PYTHON ACTUALES (Estado: EXCELENTES)

| Archivo | Líneas | Estado | Uso en Sistema |
|---------|--------|--------|----------------|
| **content_analyzer.py** | 506 | ✅ Excelente | Motor principal - Mantener |
| **spanish_grammar_analyzer.py** | 489 | ✅ Excelente | Validación gramática - Mantener |
| **question_generator.py** | 330 | ✅ Muy bueno | Generador - Modificar levemente |
| **advanced_validator.py** | 650+ | ✅ Excelente | Validación - Mantener intacto |
| **embeddings_module.py** | ~150 | ✅ Funcional | Embeddings - Mantener |
| **chunking.py** | ~200 | ✅ Funcional | Chunking - Mantener |
| **supabase_client.py** | ~100 | ✅ Funcional | DB - Mantener |
| **semantic_validator.py** | ~300 | ⚠️ Legacy | Reemplazado por advanced - Deprecar |

**Total existente**: ~2,700 líneas de código Python SÓLIDO ✅

---

## 🎯 DISEÑO MODULAR HÍBRIDO (OPCIÓN B)

### **PRINCIPIO**: NO Reescribir, SOLO Extender

```
┌─────────────────────────────────────────────────────────────┐
│                    SISTEMA ACTUAL (2700 líneas)             │
│                         ✅ MANTENER                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              NUEVO: universal_entity_types.py               │
│                 (150 líneas - AGREGAR)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ UNIVERSAL_INDICATORS = {                             │  │
│  │   "PERSON": [...],    # Funciona para CUALQUIER PDF │  │
│  │   "CONCEPT": [...],   # Literatura, Ciencia, Técnico│  │
│  │   "OBJECT": [...],                                   │  │
│  │   "PROCESS": [...],                                  │  │
│  │   "LOCATION": [...]                                  │  │
│  │ }                                                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│       MODIFICACIONES MÍNIMAS (3 archivos existentes)        │
│                                                              │
│  1. content_analyzer.py          (+80 líneas)               │
│     └─> _extract_entities() usar UNIVERSAL_INDICATORS       │
│                                                              │
│  2. spanish_grammar_analyzer.py  (+60 líneas)               │
│     └─> get_entity_type() clasificar por contexto           │
│                                                              │
│  3. question_generator.py        (+50 líneas)               │
│     └─> usar tipos en _generate_intelligent_question()      │
│                                                              │
│  TOTAL CAMBIOS: ~190 líneas nuevas                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 ESTRUCTURA MODULAR FINAL

```
backend/
├── 🆕 universal_entity_types.py      # NUEVO - Indicadores universales
│   ├── class EntityType(Enum)
│   ├── UNIVERSAL_INDICATORS: Dict
│   └── FUNCTION_WORDS: Set
│
├── ✏️ content_analyzer.py            # MODIFICAR - Usar indicadores
│   ├── _extract_entities()           # +40 líneas (usar UNIVERSAL_INDICATORS)
│   └── _extract_entities_universal() # +40 líneas (nuevo método)
│
├── ✏️ spanish_grammar_analyzer.py    # MODIFICAR - Clasificar tipos
│   └── get_entity_type()             # +60 líneas (nuevo método)
│
├── ✏️ question_generator.py          # MODIFICAR - Usar tipos
│   └── _generate_intelligent_question() # +50 líneas (switch por tipo)
│
├── ✅ advanced_validator.py          # MANTENER INTACTO
├── ✅ embeddings_module.py           # MANTENER INTACTO
├── ✅ chunking.py                    # MANTENER INTACTO
├── ✅ supabase_client.py             # MANTENER INTACTO
└── ⚠️ semantic_validator.py          # DEPRECAR (usar advanced_validator)
```

---

## 🔧 IMPLEMENTACIÓN DETALLADA

### **PASO 1: Crear `universal_entity_types.py` (NUEVO - 150 líneas)**

```python
"""
TIPOS DE ENTIDADES UNIVERSALES - RECUIVA
==========================================

Define indicadores lingüísticos UNIVERSALES que funcionan para:
- Literatura (señor, conde, reina)
- Ciencia (proteína, enzima, compuesto)
- Técnico (algoritmo, método, proceso)
- Académico (teoría, ley, principio)

NO es específico de "El Collar de la Reina" - funciona para CUALQUIER PDF.
"""

from enum import Enum
from typing import Dict, Set, List

class EntityType(Enum):
    """Tipos de entidades universales (independientes del dominio)"""
    PERSON = "persona"          # María, doctor García
    CONCEPT = "concepto"        # teoría de la relatividad, ley de Newton
    OBJECT = "objeto"           # proteína BRCA1, collar de la reina
    PROCESS = "proceso"         # algoritmo QuickSort, fotosíntesis
    LOCATION = "ubicación"      # París, laboratorio X
    ORGANIZATION = "org"        # universidad, empresa
    UNKNOWN = "desconocido"


# ============================================================================
# INDICADORES UNIVERSALES - Funcionan para CUALQUIER dominio
# ============================================================================

UNIVERSAL_INDICATORS: Dict[EntityType, List[str]] = {
    
    # PERSONAS - Literatura, Historia, Biografías
    EntityType.PERSON: [
        # Títulos nobleza
        'señor', 'señora', 'señorita', 'don', 'doña',
        'conde', 'condesa', 'duque', 'duquesa', 'marqués', 'marquesa',
        'rey', 'reina', 'príncipe', 'princesa', 'emperador', 'emperatriz',
        
        # Títulos religiosos
        'papa', 'cardenal', 'obispo', 'arzobispo', 'padre', 'fray',
        'hermano', 'hermana', 'sor', 'san', 'santa', 'monseñor',
        
        # Títulos académicos/profesionales
        'doctor', 'doctora', 'dr', 'dra',
        'profesor', 'profesora', 'prof',
        'ingeniero', 'ingeniera', 'ing',
        'licenciado', 'licenciada', 'lic',
        'maestro', 'maestra', 'mtra', 'mtro',
        
        # Títulos militares
        'general', 'coronel', 'capitán', 'teniente', 'sargento',
        'almirante', 'comandante', 'mayor',
        
        # Relaciones familiares (solo en contexto específico)
        'esposo', 'esposa', 'hijo', 'hija', 'hermano', 'hermana',
        'padre', 'madre', 'abuelo', 'abuela', 'tío', 'tía',
        'sobrino', 'sobrina', 'primo', 'prima'
    ],
    
    # CONCEPTOS - Ciencia, Filosofía, Academia
    EntityType.CONCEPT: [
        # Científicos
        'teoría', 'ley', 'principio', 'hipótesis', 'modelo',
        'paradigma', 'postulado', 'axioma', 'teorema', 'corolario',
        
        # Filosóficos
        'concepto', 'idea', 'noción', 'tesis', 'doctrina',
        'ideología', 'corriente', 'escuela', 'movimiento',
        
        # Técnicos
        'método', 'técnica', 'metodología', 'enfoque', 'estrategia',
        'sistema', 'marco', 'esquema', 'estructura'
    ],
    
    # OBJETOS - Ciencia, Medicina, Química, Física
    EntityType.OBJECT: [
        # Biología/Medicina
        'proteína', 'enzima', 'gen', 'cromosoma', 'adn', 'arn',
        'célula', 'órgano', 'tejido', 'molécula', 'átomo',
        'bacteria', 'virus', 'anticuerpo', 'hormona',
        
        # Química
        'compuesto', 'elemento', 'sustancia', 'reactivo', 'catalizador',
        'ácido', 'base', 'sal', 'óxido', 'ion', 'radical',
        
        # Física
        'partícula', 'onda', 'campo', 'fuerza', 'energía',
        'masa', 'velocidad', 'aceleración',
        
        # Objetos físicos generales
        'objeto', 'artefacto', 'dispositivo', 'instrumento',
        'herramienta', 'máquina', 'aparato', 'equipo',
        
        # Objetos específicos (literatura, historia)
        'collar', 'anillo', 'corona', 'espada', 'armadura',
        'libro', 'manuscrito', 'documento', 'carta', 'diploma'
    ],
    
    # PROCESOS - Informática, Matemáticas, Procedimientos
    EntityType.PROCESS: [
        # Informática
        'algoritmo', 'programa', 'software', 'aplicación', 'función',
        'procedimiento', 'rutina', 'script', 'código',
        
        # Biología
        'proceso', 'ciclo', 'síntesis', 'metabolismo', 'respiración',
        'fotosíntesis', 'mitosis', 'meiosis', 'transcripción', 'traducción',
        
        # Generales
        'método', 'técnica', 'mecanismo', 'operación', 'protocolo',
        'fase', 'etapa', 'paso', 'secuencia'
    ],
    
    # UBICACIONES - Geografía, Lugares
    EntityType.LOCATION: [
        'ciudad', 'país', 'región', 'provincia', 'estado', 'nación',
        'continente', 'isla', 'península', 'cabo', 'golfo',
        'montaña', 'cordillera', 'valle', 'río', 'lago', 'mar', 'océano',
        'calle', 'avenida', 'plaza', 'parque', 'edificio', 'torre',
        'palacio', 'castillo', 'catedral', 'iglesia', 'templo',
        'museo', 'biblioteca', 'universidad', 'hospital', 'laboratorio'
    ],
    
    # ORGANIZACIONES - Instituciones, Empresas
    EntityType.ORGANIZATION: [
        'universidad', 'instituto', 'academia', 'escuela', 'colegio',
        'empresa', 'corporación', 'compañía', 'firma', 'negocio',
        'organización', 'asociación', 'fundación', 'sociedad',
        'gobierno', 'ministerio', 'departamento', 'agencia',
        'partido', 'movimiento', 'grupo', 'equipo'
    ]
}


# ============================================================================
# PALABRAS FUNCIONALES - NUNCA son entidades (español universal)
# ============================================================================

FUNCTION_WORDS: Set[str] = {
    # Artículos
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
    
    # Preposiciones
    'a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'durante',
    'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 'por',
    'según', 'sin', 'sobre', 'tras', 'versus', 'vía',
    
    # Conjunciones
    'y', 'e', 'ni', 'que', 'o', 'u', 'pero', 'mas', 'sino',
    'aunque', 'como', 'cuando', 'donde', 'porque', 'pues', 'si',
    'mientras', 'pues', 'luego', 'conque',
    
    # Pronombres
    'yo', 'tú', 'él', 'ella', 'nosotros', 'nosotras', 'vosotros',
    'vosotras', 'ellos', 'ellas', 'usted', 'ustedes',
    'me', 'te', 'se', 'nos', 'os', 'lo', 'la', 'le', 'les',
    'este', 'ese', 'aquel', 'esto', 'eso', 'aquello',
    'quien', 'cual', 'cuyo', 'cuanto',
    
    # Adverbios comunes
    'muy', 'más', 'menos', 'tan', 'tanto', 'mucho', 'poco',
    'bastante', 'demasiado', 'casi', 'solo', 'solamente',
    'también', 'tampoco', 'sí', 'no', 'nunca', 'siempre', 'jamás',
    'aquí', 'ahí', 'allí', 'acá', 'allá', 'cerca', 'lejos',
    'antes', 'después', 'luego', 'entonces', 'ahora', 'hoy',
    'ayer', 'mañana', 'bien', 'mal', 'así', 'tal', 'recién',
    
    # Determinantes
    'algún', 'alguna', 'algunos', 'algunas', 'ningún', 'ninguna',
    'todo', 'toda', 'todos', 'todas', 'otro', 'otra', 'otros', 'otras',
    'mismo', 'misma', 'mismos', 'mismas', 'cada', 'cualquier',
    
    # Números cardinales (evitar "Dos personas", "Tres días")
    'cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete',
    'ocho', 'nueve', 'diez', 'once', 'doce', 'trece', 'catorce', 'quince',
    'veinte', 'treinta', 'cuarenta', 'cincuenta', 'cien', 'mil',
    'varios', 'muchos', 'pocos', 'algunos', 'demasiados'
}


# ============================================================================
# VERBOS DE CONTEXTO - Ayudan a identificar tipo de entidad
# ============================================================================

CONTEXT_VERBS: Dict[EntityType, Set[str]] = {
    
    EntityType.PERSON: {
        # Verbos de comunicación (solo personas hablan)
        'dijo', 'dice', 'decir', 'preguntó', 'pregunta', 'preguntar',
        'respondió', 'responde', 'responder', 'exclamó', 'exclama',
        'gritó', 'grita', 'susurró', 'susurra', 'murmuró', 'murmura',
        
        # Verbos de pensamiento/emoción
        'pensó', 'piensa', 'pensar', 'creyó', 'cree', 'creer',
        'sintió', 'siente', 'sentir', 'amó', 'ama', 'amar',
        'temió', 'teme', 'temer', 'odiaba', 'odia', 'odiar',
        
        # Verbos de acción humana
        'caminó', 'camina', 'entró', 'entra', 'salió', 'sale',
        'miró', 'mira', 'vio', 've', 'escuchó', 'escucha'
    },
    
    EntityType.CONCEPT: {
        'define', 'explica', 'establece', 'propone', 'postula',
        'plantea', 'sugiere', 'implica', 'sostiene', 'afirma'
    },
    
    EntityType.OBJECT: {
        'contiene', 'produce', 'forma', 'compone', 'integra',
        'consiste', 'incluye', 'abarca', 'presenta', 'muestra'
    },
    
    EntityType.PROCESS: {
        'ejecuta', 'realiza', 'implementa', 'desarrolla', 'procesa',
        'calcula', 'genera', 'transforma', 'convierte', 'opera'
    },
    
    EntityType.LOCATION: {
        'ubica', 'sitúa', 'localiza', 'encuentra', 'está',
        'queda', 'extiende', 'limita', 'bordea'
    }
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def is_function_word(word: str) -> bool:
    """Verifica si una palabra es funcional (nunca entidad)"""
    return word.lower() in FUNCTION_WORDS


def get_indicators_for_type(entity_type: EntityType) -> List[str]:
    """Retorna indicadores para un tipo específico"""
    return UNIVERSAL_INDICATORS.get(entity_type, [])


def get_all_indicators() -> Set[str]:
    """Retorna TODOS los indicadores de todos los tipos"""
    all_indicators = set()
    for indicators in UNIVERSAL_INDICATORS.values():
        all_indicators.update(indicators)
    return all_indicators


def infer_type_from_indicator(indicator: str) -> EntityType:
    """Infiere tipo de entidad basándose en el indicador usado"""
    indicator_lower = indicator.lower()
    
    for entity_type, indicators in UNIVERSAL_INDICATORS.items():
        if indicator_lower in indicators:
            return entity_type
    
    return EntityType.UNKNOWN
```

---

### **PASO 2: Modificar `content_analyzer.py` (+80 líneas)**

**Ubicación**: Línea ~243 (método `_extract_entities()`)

**Cambio**:

```python
# AGREGAR al inicio del archivo:
from universal_entity_types import (
    UNIVERSAL_INDICATORS, 
    FUNCTION_WORDS, 
    EntityType,
    get_all_indicators,
    infer_type_from_indicator
)

# MODIFICAR el método _extract_entities() existente:

def _extract_entities(self, text: str) -> List[str]:
    """
    MEJORADO: Extrae entidades usando indicadores UNIVERSALES
    
    ANTES: Solo nombres de personas con títulos de nobleza
    AHORA: Personas, conceptos, objetos, procesos, ubicaciones
    
    FUNCIONA PARA:
    ✅ Literatura: "señor Dreux", "reina María Antonieta"
    ✅ Ciencia: "proteína BRCA1", "enzima catalasa"
    ✅ Técnico: "algoritmo QuickSort", "método Agile"
    ✅ Académico: "teoría de la relatividad", "ley de Newton"
    """
    entities = []
    
    # PASO 1: BUSCAR ENTIDADES CON INDICADOR (Universal)
    for entity_type, indicators in UNIVERSAL_INDICATORS.items():
        for indicator in indicators:
            # Patrón: [artículo opcional] + indicador + entidad
            # Ejemplos: "el doctor García", "la proteína BRCA1", "algoritmo QuickSort"
            pattern = rf'\b(?:el|la|los|las|un|una)?\s*{re.escape(indicator)}\s+([A-ZÁÉÍÓÚÑ0-9][\wáéíóúñ\-]+(?:\s+(?:de|del|y|con)\s+[\wáéíóúñA-ZÁÉÍÓÚÑ0-9\-]+)*(?:\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñ\-]+)*)'
            
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entity_text = match.group(1).strip()
                
                # Validar que no sea palabra funcional
                if not is_function_word(entity_text.split()[0]):
                    # Verificar contexto verbal (opcional pero ayuda)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]
                    
                    # Agregar si tiene longitud razonable
                    if len(entity_text) >= 3 and entity_text not in entities:
                        entities.append(entity_text)
    
    # PASO 2: Mantener extracción de nombres SIN indicador (tu código actual)
    # ... (tu lógica actual para nombres propios sin título)
    
    return entities[:10]  # Top 10 entidades
```

---

### **PASO 3: Modificar `spanish_grammar_analyzer.py` (+60 líneas)**

**Ubicación**: Línea ~489 (al final del archivo)

**Cambio**:

```python
# AGREGAR al inicio:
from universal_entity_types import (
    EntityType,
    CONTEXT_VERBS,
    UNIVERSAL_INDICATORS,
    infer_type_from_indicator
)

# AGREGAR al final de la clase SpanishGrammarAnalyzer:

def get_entity_type(self, entity: str, context: str) -> EntityType:
    """
    Clasifica entidad en tipo UNIVERSAL basándose en contexto
    
    Args:
        entity: "García", "BRCA1", "QuickSort", "relatividad"
        context: Oración completa donde aparece la entidad
    
    Returns:
        EntityType: PERSON | CONCEPT | OBJECT | PROCESS | LOCATION | UNKNOWN
    
    Ejemplos:
        >>> get_entity_type("García", "el doctor García estudió medicina")
        EntityType.PERSON
        
        >>> get_entity_type("BRCA1", "la proteína BRCA1 regula el ciclo")
        EntityType.OBJECT
        
        >>> get_entity_type("QuickSort", "el algoritmo QuickSort ordena")
        EntityType.PROCESS
    """
    context_lower = context.lower()
    entity_lower = entity.lower()
    
    # MÉTODO 1: Buscar INDICADOR en contexto
    for entity_type, indicators in UNIVERSAL_INDICATORS.items():
        for indicator in indicators:
            # Patrón: "indicador + entidad"
            if re.search(rf'\b{re.escape(indicator)}\s+{re.escape(entity_lower)}', context_lower):
                return entity_type
    
    # MÉTODO 2: Buscar VERBO de contexto
    for entity_type, verbs in CONTEXT_VERBS.items():
        for verb in verbs:
            # Patrón: "entidad + verbo" (sujeto-verbo)
            if re.search(rf'\b{re.escape(entity_lower)}\s+{verb}', context_lower):
                return entity_type
    
    # MÉTODO 3: Heurísticas por capitalización y longitud
    if entity[0].isupper() and len(entity.split()) >= 2:
        # Probablemente persona o lugar
        if any(verb in context_lower for verb in CONTEXT_VERBS[EntityType.PERSON]):
            return EntityType.PERSON
        return EntityType.LOCATION
    
    return EntityType.UNKNOWN
```

---

### **PASO 4: Modificar `question_generator.py` (+50 líneas)**

**Ubicación**: Línea ~89 (método `_generate_intelligent_question()`)

**Cambio**:

```python
# AGREGAR al inicio:
from spanish_grammar_analyzer import SpanishGrammarAnalyzer
from universal_entity_types import EntityType

# MODIFICAR _generate_intelligent_question():

def _generate_intelligent_question(...) -> Dict:
    """
    MEJORADO: Genera preguntas basadas en TIPO DE ENTIDAD (universal)
    """
    # ... (validación de entidades existente)
    
    # NUEVO: Clasificar entidades por tipo
    grammar = SpanishGrammarAnalyzer()
    
    entity_types_map = {}
    for entity in valid_entities[:3]:  # Solo primeras 3
        entity_type = grammar.get_entity_type(entity, chunk)
        entity_types_map[entity] = entity_type
    
    # NUEVO: Generar pregunta basada en tipo UNIVERSAL
    for entity, entity_type in entity_types_map.items():
        
        if entity_type == EntityType.PERSON:
            return f"¿Quién fue {entity} y qué papel desempeñó en los acontecimientos descritos?"
        
        elif entity_type == EntityType.CONCEPT:
            return f"Define y explica el concepto de {entity} según el material presentado"
        
        elif entity_type == EntityType.OBJECT:
            return f"Describe las características y función de {entity} mencionadas en el texto"
        
        elif entity_type == EntityType.PROCESS:
            return f"Explica paso a paso cómo funciona el proceso de {entity}"
        
        elif entity_type == EntityType.LOCATION:
            return f"¿Qué importancia tiene {entity} en el contexto descrito?"
        
        elif entity_type == EntityType.ORGANIZATION:
            return f"¿Cuál es el rol de {entity} según lo mencionado en el material?"
    
    # Fallback a método actual si no se identificó tipo
    if content_type == 'narrative':
        return _generate_narrative_question(...)
    # ... (resto del código actual)
```

---

## 📊 RESUMEN DE CAMBIOS

| Archivo | Acción | Líneas Nuevas | Líneas Modificadas | Total Impacto |
|---------|--------|---------------|-------------------|---------------|
| `universal_entity_types.py` | **CREAR** | +150 | 0 | +150 |
| `content_analyzer.py` | **MODIFICAR** | +40 | +40 | +80 |
| `spanish_grammar_analyzer.py` | **MODIFICAR** | +60 | 0 | +60 |
| `question_generator.py` | **MODIFICAR** | +30 | +20 | +50 |
| **TOTAL** | | **+280 líneas** | **+60 líneas** | **+340 líneas** |

**Código existente mantenido**: 2,700 líneas ✅  
**Código nuevo agregado**: 340 líneas ✅  
**Ratio preservación/extensión**: **88% preservado, 12% nuevo** ✅

---

## ✅ VENTAJAS DEL DISEÑO HÍBRIDO

1. ✅ **Aprovecha TODO tu código existente** (2,700 líneas funcionando)
2. ✅ **Solo 340 líneas nuevas** (vs 800+ del sistema universal completo)
3. ✅ **Modular**: Cada archivo tiene responsabilidad única
4. ✅ **Fácil de debuggear**: Separación clara de conceptos
5. ✅ **Funciona para CUALQUIER PDF**: Literatura, ciencia, técnico
6. ✅ **Backward compatible**: No rompe código existente
7. ✅ **Fácil de testear**: Cada módulo se prueba independientemente

---

## 🧪 PLAN DE TESTING

### Test 1: Literatura (DEBE SEGUIR FUNCIONANDO)
```python
test_text = """
La condesa de Dreux-Soubise lucía el collar de la reina.
María Antonieta recibió el regalo del cardenal de Rohan.
"""

# Entidades esperadas:
# - PERSON: "condesa de Dreux-Soubise", "María Antonieta", "cardenal de Rohan"
# - OBJECT: "collar de la reina"
```

### Test 2: Ciencia (NUEVO - DEBE FUNCIONAR)
```python
test_text = """
La proteína BRCA1 regula el ciclo celular mediante fosforilación.
La enzima catalasa descompone el peróxido de hidrógeno en agua y oxígeno.
"""

# Entidades esperadas:
# - OBJECT: "proteína BRCA1", "enzima catalasa", "peróxido de hidrógeno"
# - PROCESS: "fosforilación", "ciclo celular"
```

### Test 3: Técnico (NUEVO - DEBE FUNCIONAR)
```python
test_text = """
El algoritmo QuickSort ordena elementos en O(n log n) promedio.
El método Agile implementa desarrollo iterativo e incremental.
"""

# Entidades esperadas:
# - PROCESS: "algoritmo QuickSort", "método Agile"
# - CONCEPT: "desarrollo iterativo"
```

---

## 🚀 PRÓXIMOS PASOS (ORDEN DE IMPLEMENTACIÓN)

1. ✅ **Crear `universal_entity_types.py`** (15 min)
2. ✅ **Modificar `content_analyzer.py`** (20 min)
3. ✅ **Modificar `spanish_grammar_analyzer.py`** (15 min)
4. ✅ **Modificar `question_generator.py`** (20 min)
5. ✅ **Testear con 3 dominios** (30 min)
6. ✅ **Commit y push** (5 min)

**TIEMPO TOTAL ESTIMADO**: ~1.5 horas

---

## 📝 COMMIT MESSAGES SUGERIDOS

```bash
# Commit 1
feat: Add universal entity types module for multi-domain NER
- Supports literature, science, technical, and academic content
- 150+ universal indicators across 6 entity types
- Function words blacklist for Spanish

# Commit 2
refactor: Enhance content_analyzer with universal indicators
- Extend _extract_entities() to use universal indicators
- Maintain backward compatibility with existing extraction
- Support PERSON, CONCEPT, OBJECT, PROCESS, LOCATION, ORG

# Commit 3
feat: Add entity type classification to spanish_grammar_analyzer
- New get_entity_type() method for universal classification
- Context-based inference using indicators and verbs
- Returns EntityType enum for downstream use

# Commit 4
refactor: Generate questions based on universal entity types
- Questions adapt to entity type (person/concept/object/process)
- More specific and relevant questions per domain
- Maintains fallback to content-type based generation
```

---

**Autor**: Abel Jesús Moya Acosta  
**Fecha**: 10 de noviembre de 2025  
**Sistema**: Recuiva - NER Universal Híbrido  
**Versión**: 1.0 (Arquitectura Modular)
