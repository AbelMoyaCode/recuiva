"""
═══════════════════════════════════════════════════════════════════════════════
CONFIGURACIÓN GLOBAL DE PYTEST - RECUIVA
═══════════════════════════════════════════════════════════════════════════════

Este archivo define:
- Fixtures compartidas entre todos los tests
- Configuración del entorno de pruebas
- Hooks de pytest para logging y reporting

Autor: Abel Jesús Moya Acosta
Fecha: 5 de diciembre de 2025
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import sys
import os
import warnings
from pathlib import Path
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE PATH
# ═══════════════════════════════════════════════════════════════════════════════
# Agregar el directorio backend al path para imports
BACKEND_DIR = Path(__file__).parent.parent
ROOT_DIR = BACKEND_DIR.parent
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(ROOT_DIR))

# Suprimir warnings molestos durante tests
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message=".*torch.*")

# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES COMPARTIDAS - MATERIALES DE PRUEBA
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def material_punteros():
    """
    Material de prueba sobre punteros en C/C++
    
    Este es el material que usó el profesor en la Semana 15 para probar
    el sistema de validación. Contiene definiciones claras de punteros
    que permiten verificar la extracción de chunks y validación semántica.
    """
    return """
    Un puntero es una variable que almacena la dirección de memoria de otra variable.
    Los punteros son fundamentales en la programación de bajo nivel como C y C++.
    Una variable de tipo puntero puede tomar como valor únicamente direcciones de memoria.
    
    Los punteros permiten acceso directo a la memoria del sistema operativo.
    La declaración de un puntero se realiza usando el operador asterisco (*).
    Para obtener la dirección de una variable se usa el operador ampersand (&).
    
    La desreferenciación de punteros permite acceder al valor almacenado en la dirección.
    Los punteros nulos apuntan a la dirección de memoria 0 y no son válidos para operaciones.
    
    Un conjunto de valores de un tipo de dato puntero es un conjunto de direcciones de memoria.
    Es decir, una variable de tipo puntero puede tomar como valor únicamente una dirección de memoria.
    La variable dinámica puede ser un conglomerado donde uno o más campos son punteros.
    """

@pytest.fixture(scope="session")
def material_collar_reina():
    """
    Material de prueba: fragmento del cuento "El Collar de la Reina"
    
    Usado para probar preguntas inferenciales y detección de contradicciones.
    Contiene personajes y relaciones que requieren razonamiento para responder.
    """
    return """
    Henriette era una joven que vivía en el edificio de la condesa. Cada año, la condesa
    le enviaba dinero por correo como ayuda económica. Esta costumbre se mantenía desde
    hacía varios años como muestra de generosidad.
    
    La condesa poseía un valioso collar de diamantes que guardaba en un gabinete.
    Henriette conocía la existencia del collar porque su ventana de cocina daba al
    mismo patio interior y podía ver cuando la condesa lo guardaba.
    
    Un día, el collar desapareció misteriosamente. Las sospechas recayeron sobre
    varias personas del edificio, pero nunca se encontró evidencia directa.
    """

@pytest.fixture(scope="session")
def chunks_punteros(material_punteros, embedding_model):
    """
    Genera chunks del material de punteros con embeddings
    
    El HybridValidator espera chunks como diccionarios con:
    - 'text_full': el texto del chunk
    - 'embedding': el vector de embedding del chunk
    """
    try:
        from chunking import semantic_chunking
        from embeddings_module import generate_embeddings
        
        # Generar chunks de texto
        text_chunks = semantic_chunking(material_punteros, min_words=30, max_words=80, overlap_words=5)
        
        # Convertir a formato con embeddings
        chunks_with_embeddings = []
        for i, text in enumerate(text_chunks):
            if text.strip():
                emb = generate_embeddings(text)
                chunks_with_embeddings.append({
                    'id': f'chunk_{i}',
                    'text_full': text,
                    'embedding': emb.tolist() if hasattr(emb, 'tolist') else list(emb)
                })
        
        return chunks_with_embeddings
    except ImportError as e:
        pytest.skip(f"No se pudo importar módulo: {e}")

@pytest.fixture(scope="session")
def preguntas_prueba():
    """
    Preguntas de prueba con respuestas esperadas
    
    Incluye preguntas literales e inferenciales para validar
    diferentes aspectos del sistema.
    """
    return [
        {
            "id": "q1",
            "pregunta": "¿Qué es un puntero?",
            "tipo": "literal",
            "respuesta_correcta": "Una variable que almacena la dirección de memoria de otra variable",
            "respuesta_parcial": "Es una variable de memoria",
            "respuesta_incorrecta": "Es una función matemática que calcula derivadas"
        },
        {
            "id": "q2",
            "pregunta": "¿Por qué son importantes los punteros en C++?",
            "tipo": "inferencial",
            "respuesta_correcta": "Porque permiten acceso directo a la memoria y son fundamentales para programación de bajo nivel",
            "respuesta_parcial": "Para manejar memoria",
            "respuesta_incorrecta": "Porque son más rápidos que los enteros"
        },
        {
            "id": "q3",
            "pregunta": "¿Qué operador se usa para declarar un puntero?",
            "tipo": "literal",
            "respuesta_correcta": "El operador asterisco (*)",
            "respuesta_parcial": "Asterisco",
            "respuesta_incorrecta": "El operador más (+)"
        },
        {
            "id": "q4",
            "pregunta": "¿Qué tipo de ayuda recibía Henriette de la condesa?",
            "tipo": "literal",
            "respuesta_correcta": "Recibía dinero por correo cada año como ayuda económica",
            "respuesta_parcial": "Ayuda económica",
            "respuesta_incorrecta": "La condesa nunca le mandó dinero"  # Contradicción
        }
    ]

@pytest.fixture(scope="session")
def dataset_ground_truth():
    """
    Dataset de evaluación (ground truth) - DO-003 del Project Charter
    
    20 pares pregunta-respuesta + fragmento correcto para validar
    métricas de precisión del sistema.
    """
    return [
        {
            "pregunta": "¿Qué es un puntero?",
            "respuesta_referencia": "variable que almacena dirección de memoria",
            "fragmento_esperado": "Un puntero es una variable que almacena la dirección de memoria",
            "clasificacion": "correcta"
        },
        {
            "pregunta": "¿Cómo se declara un puntero en C?",
            "respuesta_referencia": "usando el operador asterisco",
            "fragmento_esperado": "declaración de un puntero se realiza usando el operador asterisco",
            "clasificacion": "correcta"
        },
        {
            "pregunta": "¿Qué valores puede tomar una variable puntero?",
            "respuesta_referencia": "direcciones de memoria",
            "fragmento_esperado": "puede tomar como valor únicamente direcciones de memoria",
            "clasificacion": "correcta"
        },
        {
            "pregunta": "¿Qué es la desreferenciación?",
            "respuesta_referencia": "acceder al valor almacenado en la dirección",
            "fragmento_esperado": "desreferenciación de punteros permite acceder al valor",
            "clasificacion": "correcta"
        },
        {
            "pregunta": "¿Qué es un puntero nulo?",
            "respuesta_referencia": "apunta a la dirección 0, no es válido para operaciones",
            "fragmento_esperado": "punteros nulos apuntan a la dirección de memoria 0",
            "clasificacion": "correcta"
        }
    ]

# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES DE MODELO Y VALIDADOR
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def embedding_model():
    """
    Carga el modelo de embeddings (all-MiniLM-L6-v2)
    
    Scope "session" para cargar solo una vez durante toda la sesión de tests.
    """
    try:
        from embeddings_module import load_model
        print("\n🔄 Cargando modelo de embeddings para pruebas...")
        model = load_model()
        print("✅ Modelo cargado exitosamente")
        return model
    except Exception as e:
        pytest.skip(f"No se pudo cargar el modelo: {e}")

@pytest.fixture(scope="session")
def hybrid_validator(embedding_model):
    """
    Instancia del HybridValidator para pruebas
    """
    try:
        from hybrid_validator import HybridValidator
        validator = HybridValidator(embedding_model)
        return validator
    except Exception as e:
        pytest.skip(f"No se pudo crear el validador: {e}")

# ═══════════════════════════════════════════════════════════════════════════════
# HOOKS DE PYTEST
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_configure(config):
    """Configuración inicial al arrancar pytest"""
    print("\n" + "═" * 70)
    print("🧪 RECUIVA - SUITE DE PRUEBAS UNITARIAS")
    print("═" * 70)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Directorio: {BACKEND_DIR}")
    print("═" * 70)

def pytest_unconfigure(config):
    """Configuración al finalizar pytest"""
    print("\n" + "═" * 70)
    print("✅ SUITE DE PRUEBAS COMPLETADA")
    print("═" * 70)

def pytest_collection_modifyitems(config, items):
    """Modifica el orden de ejecución de tests"""
    # Ejecutar tests de embeddings primero (dependencia para otros)
    items.sort(key=lambda x: (
        0 if 'embeddings' in x.nodeid else
        1 if 'chunking' in x.nodeid else
        2 if 'hybrid' in x.nodeid else
        3 if 'sm2' in x.nodeid else
        4
    ))

# ═══════════════════════════════════════════════════════════════════════════════
# MARCADORES PERSONALIZADOS
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_configure(config):
    """Registrar marcadores personalizados"""
    config.addinivalue_line(
        "markers", "slow: marca pruebas lentas que requieren más tiempo"
    )
    config.addinivalue_line(
        "markers", "integration: marca pruebas de integración"
    )
    config.addinivalue_line(
        "markers", "requires_api: marca pruebas que requieren API externa (Groq)"
    )
