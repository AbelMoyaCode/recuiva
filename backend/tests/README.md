# 🧪 RECUIVA - Suite de Pruebas Unitarias

## Descripción

Esta suite de pruebas valida los componentes principales del sistema RECUIVA (REpetición, CUIz, VAlidación). Responde directamente a los requerimientos del profesor (Semana 15):

> "¿Tienes tus casos de prueba? ¿La prueba unitaria? Para poderlo probar ahí tus embeddings"

## 📁 Estructura de Tests

```
backend/tests/
├── __init__.py              # Inicialización del módulo
├── conftest.py              # Configuración global y fixtures
├── test_embeddings.py       # Pruebas de generación de embeddings
├── test_hybrid_validator.py # Pruebas del validador híbrido
├── test_chunking.py         # Pruebas de chunking de texto
├── test_sm2_algorithm.py    # Pruebas del algoritmo SM-2
├── test_groq_api.py         # Pruebas de la API de Groq
├── test_integration.py      # Pruebas de integración
└── README.md                # Este archivo
```

## 🚀 Ejecución de Tests

### Ejecutar todos los tests
```powershell
cd c:\Users\HOUSE\Desktop\recuiva\backend
python -m pytest tests/ -v
```

### Ejecutar tests específicos
```powershell
# Solo embeddings
python -m pytest tests/test_embeddings.py -v

# Solo validador híbrido
python -m pytest tests/test_hybrid_validator.py -v

# Solo chunking
python -m pytest tests/test_chunking.py -v

# Solo SM-2
python -m pytest tests/test_sm2_algorithm.py -v

# Solo Groq API
python -m pytest tests/test_groq_api.py -v
```

### Ejecutar tests sin los lentos
```powershell
python -m pytest tests/ -v -m "not slow"
```

### Ejecutar con cobertura
```powershell
python -m pytest tests/ --cov=. --cov-report=html
```

## 📊 Tests por Módulo

### test_embeddings.py
Pruebas del modelo de embeddings (all-MiniLM-L6-v2):

| Test | Descripción |
|------|-------------|
| `test_model_loads_successfully` | Verifica que el modelo se carga sin errores |
| `test_model_dimension_is_384` | Verifica que los embeddings tienen 384 dimensiones |
| `test_same_text_produces_same_embedding` | Verifica determinismo |
| `test_similar_texts_have_high_similarity` | Verifica similitud semántica |
| `test_embedding_retrieval_for_term` | **PREGUNTA DEL PROFESOR**: ¿Cuántos chunks para "puntero"? |

### test_hybrid_validator.py
Pruebas del sistema de validación híbrida:

| Test | Descripción |
|------|-------------|
| `test_bm25_operates_on_text_not_embeddings` | BM25 trabaja sobre texto (no vectores) |
| `test_weights_sum_to_one` | Pesos suman 100% (5% + 80% + 15%) |
| `test_prefilter_returns_top_k_chunks` | Pre-filtrado TOP 15 chunks |
| `test_correct_answer_high_score` | Respuesta correcta → score alto |
| `test_contradiction_detected` | Detección de contradicciones |

### test_chunking.py
Pruebas del módulo de chunking:

| Test | Descripción |
|------|-------------|
| `test_chunking_returns_list` | Retorna lista de chunks |
| `test_chunking_respects_min_words` | Respeta mínimo de palabras |
| `test_chunking_respects_max_words` | Respeta máximo de palabras |
| `test_spanish_text_with_accents` | Funciona con español y acentos |

### test_sm2_algorithm.py
Pruebas del algoritmo de repetición espaciada:

| Test | Descripción |
|------|-------------|
| `test_ef_initial_value` | EF inicial = 2.5 |
| `test_ef_increases_with_perfect_answer` | EF aumenta con q=5 |
| `test_first_interval_is_one_day` | Primer intervalo = 1 día |
| `test_incorrect_answer_resets_interval` | Respuesta incorrecta reinicia |

### test_groq_api.py
Pruebas de la API de generación de preguntas:

| Test | Descripción |
|------|-------------|
| `test_model_name_is_correct` | Modelo = llama-3.1-8b-instant |
| `test_question_format_structure` | Estructura JSON correcta |
| `test_malformed_json_handling` | Manejo de errores |

## 🎯 Métricas Objetivo

| Métrica | Objetivo | Descripción |
|---------|----------|-------------|
| Precisión | ≥ 70% | Clasificación correcta de respuestas |
| Latencia | < 3s | Tiempo de respuesta |
| Cobertura | ≥ 80% | Cobertura de código |

## 📝 Fixtures Disponibles

Las fixtures están definidas en `conftest.py`:

```python
@pytest.fixture
def material_punteros():
    """Material sobre punteros en C/C++"""

@pytest.fixture
def chunks_punteros():
    """Chunks del material de punteros"""

@pytest.fixture
def preguntas_prueba():
    """Preguntas con respuestas etiquetadas"""

@pytest.fixture
def embedding_model():
    """Modelo de embeddings cargado"""

@pytest.fixture
def hybrid_validator():
    """Instancia del HybridValidator"""
```

## 🔧 Configuración

### Variables de Entorno
```powershell
$env:GROQ_API_KEY = "gsk_..."  # Para tests de Groq API
```

### Dependencias
```
pytest>=7.0.0
pytest-cov>=4.0.0
numpy>=1.21.0
sentence-transformers>=2.2.0
```

## ⚠️ Marcadores

```python
@pytest.mark.slow        # Tests lentos (> 5s)
@pytest.mark.integration # Tests de integración
@pytest.mark.requires_api # Requiere API key externa
```

Ejecutar sin tests lentos:
```powershell
python -m pytest tests/ -v -m "not slow"
```

## 📈 Reportes

### Generar reporte HTML
```powershell
python -m pytest tests/ --html=report.html --self-contained-html
```

### Generar reporte de cobertura
```powershell
python -m pytest tests/ --cov=. --cov-report=html
# Abrir htmlcov/index.html
```

## 👨‍💻 Autor

**Abel Jesús Moya Acosta**  
UPAO - Taller Integrador I  
Fecha: 5 de diciembre de 2025
