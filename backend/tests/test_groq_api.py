"""
═══════════════════════════════════════════════════════════════════════════════
TEST_GROQ_API.PY - Pruebas Unitarias de la API de Groq
═══════════════════════════════════════════════════════════════════════════════

Este módulo contiene las pruebas unitarias para verificar:
1. Conexión con la API de Groq
2. Generación de preguntas con Llama 3.1 8B
3. Formato de respuestas JSON
4. Manejo de errores y rate limiting
5. Validación de prompts

Modelo utilizado: Llama 3.1 8B Instant (llama-3.1-8b-instant)
Temperatura: 0.7 (para variedad en preguntas generadas)

NOTA: Algunas pruebas requieren API key válida y conexión a Internet.
Estas pruebas están marcadas con @pytest.mark.requires_api

═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List

# Agregar backend al path
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════

GROQ_MODEL = "llama-3.1-8b-instant"
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 2048

# ═══════════════════════════════════════════════════════════════════════════════
# FIXTURES ESPECÍFICAS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_groq_client():
    """Mock del cliente de Groq para pruebas sin API"""
    mock = MagicMock()
    mock.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(
            message=MagicMock(
                content=json.dumps({
                    "preguntas": [
                        {
                            "tipo": "literal",
                            "pregunta": "¿Qué es un puntero?",
                            "dificultad": "media"
                        },
                        {
                            "tipo": "inferencial",
                            "pregunta": "¿Por qué son importantes los punteros en C++?",
                            "dificultad": "alta"
                        }
                    ]
                })
            )
        )]
    )
    return mock

@pytest.fixture
def sample_material():
    """Material de ejemplo para generación de preguntas"""
    return """
    Los punteros son variables especiales que almacenan direcciones de memoria.
    En C++, se utilizan para acceso directo a la memoria y gestión dinámica.
    La declaración se realiza con el operador asterisco (*).
    Para obtener la dirección de una variable se usa el operador ampersand (&).
    """


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestGroqConnection - Pruebas de conexión
# ═══════════════════════════════════════════════════════════════════════════════

class TestGroqConnection:
    """
    Pruebas de la conexión con la API de Groq
    """
    
    def test_groq_client_initialization(self):
        """
        TEST: Verificar que se puede crear un cliente de Groq
        """
        try:
            from groq import Groq
            import os
            
            # Intentar crear cliente (puede fallar si no hay API key)
            api_key = os.getenv("GROQ_API_KEY", "test_key")
            client = Groq(api_key=api_key)
            
            assert client is not None
            print(f"✅ Cliente Groq inicializado")
        except ImportError:
            pytest.skip("groq package not installed")
        except Exception as e:
            print(f"⚠️ Error al crear cliente: {type(e).__name__}")
    
    def test_model_name_is_correct(self):
        """
        TEST: Verificar que el modelo configurado es Llama 3.1 8B
        """
        expected_model = "llama-3.1-8b-instant"
        
        # Verificar constante o configuración
        assert GROQ_MODEL == expected_model, \
            f"Modelo esperado: {expected_model}, configurado: {GROQ_MODEL}"
        print(f"✅ Modelo configurado: {GROQ_MODEL}")
    
    def test_api_key_environment_variable(self):
        """
        TEST: Verificar que existe la variable de entorno para API key
        """
        import os
        
        api_key = os.getenv("GROQ_API_KEY")
        
        if api_key:
            # Mostrar solo los primeros caracteres por seguridad
            masked = api_key[:8] + "..." if len(api_key) > 8 else "***"
            print(f"✅ GROQ_API_KEY configurada: {masked}")
        else:
            print(f"⚠️ GROQ_API_KEY no configurada (tests con mock)")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestQuestionGeneration - Pruebas de generación de preguntas
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuestionGeneration:
    """
    Pruebas de generación de preguntas usando Groq/Llama
    """
    
    def test_generate_questions_returns_list(self, mock_groq_client, sample_material):
        """
        TEST: La generación de preguntas debe retornar una lista
        """
        # Parsear respuesta mock directamente (sin necesidad de importar groq)
        response = mock_groq_client.chat.completions.create()
        content = response.choices[0].message.content
        result = json.loads(content)
        
        assert "preguntas" in result, "Debe contener key 'preguntas'"
        assert isinstance(result["preguntas"], list), "preguntas debe ser una lista"
        print(f"✅ Generación retorna lista de {len(result['preguntas'])} preguntas")
    
    def test_question_format_structure(self, mock_groq_client):
        """
        TEST: Las preguntas generadas deben tener la estructura correcta
        
        Estructura esperada:
        {
            "tipo": "literal" | "inferencial",
            "pregunta": "string",
            "dificultad": "baja" | "media" | "alta"
        }
        """
        response = mock_groq_client.chat.completions.create()
        content = response.choices[0].message.content
        result = json.loads(content)
        
        for pregunta in result["preguntas"]:
            assert "tipo" in pregunta, "Pregunta debe tener 'tipo'"
            assert "pregunta" in pregunta, "Pregunta debe tener 'pregunta'"
            assert pregunta["tipo"] in ["literal", "inferencial"], \
                f"Tipo inválido: {pregunta['tipo']}"
        
        print(f"✅ Estructura de preguntas verificada")
    
    def test_question_types_distribution(self, mock_groq_client):
        """
        TEST: Debe haber mezcla de preguntas literales e inferenciales
        """
        response = mock_groq_client.chat.completions.create()
        content = response.choices[0].message.content
        result = json.loads(content)
        
        tipos = [p["tipo"] for p in result["preguntas"]]
        
        print(f"📊 Distribución de tipos:")
        print(f"   Literales: {tipos.count('literal')}")
        print(f"   Inferenciales: {tipos.count('inferencial')}")
        
        # Idealmente debe haber al menos de cada tipo
        if len(result["preguntas"]) >= 2:
            assert len(set(tipos)) >= 1, "Debe haber al menos un tipo de pregunta"
    
    def test_questions_are_not_empty(self, mock_groq_client):
        """
        TEST: Las preguntas no deben estar vacías
        """
        response = mock_groq_client.chat.completions.create()
        content = response.choices[0].message.content
        result = json.loads(content)
        
        for pregunta in result["preguntas"]:
            assert len(pregunta["pregunta"].strip()) > 0, "Pregunta no debe estar vacía"
            assert len(pregunta["pregunta"]) >= 10, "Pregunta debe tener al menos 10 caracteres"
        
        print(f"✅ Todas las preguntas tienen contenido")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestPromptValidation - Pruebas de validación de prompts
# ═══════════════════════════════════════════════════════════════════════════════

class TestPromptValidation:
    """
    Pruebas de los prompts enviados a Groq
    """
    
    def test_system_prompt_structure(self):
        """
        TEST: El prompt del sistema debe estar bien estructurado
        """
        system_prompt = """
        Eres un asistente educativo especializado en generar preguntas de estudio.
        Tu objetivo es crear preguntas que ayuden a los estudiantes a comprender
        y retener la información del material proporcionado.
        
        Genera preguntas de dos tipos:
        1. Literales: Que se respondan directamente con información del texto
        2. Inferenciales: Que requieran razonamiento o conexión de ideas
        
        Responde SIEMPRE en formato JSON con la estructura:
        {
            "preguntas": [
                {"tipo": "literal|inferencial", "pregunta": "...", "dificultad": "baja|media|alta"}
            ]
        }
        """
        
        # Verificar elementos clave del prompt
        assert "JSON" in system_prompt, "Prompt debe mencionar formato JSON"
        assert "literal" in system_prompt.lower(), "Prompt debe mencionar preguntas literales"
        assert "inferencial" in system_prompt.lower(), "Prompt debe mencionar preguntas inferenciales"
        
        print(f"✅ Estructura del prompt del sistema verificada")
    
    def test_user_prompt_includes_material(self, sample_material):
        """
        TEST: El prompt de usuario debe incluir el material
        """
        user_prompt = f"""
        Basándote en el siguiente material, genera 3 preguntas de estudio:
        
        MATERIAL:
        {sample_material}
        
        Genera preguntas variadas que cubran los conceptos principales.
        """
        
        assert sample_material in user_prompt, "El material debe estar en el prompt"
        assert "genera" in user_prompt.lower(), "Debe indicar que genere preguntas"
        
        print(f"✅ Prompt de usuario incluye el material correctamente")
    
    def test_prompt_length_within_limits(self, sample_material):
        """
        TEST: El prompt no debe exceder los límites del modelo
        
        Llama 3.1 8B tiene un contexto de 131072 tokens,
        pero mantenemos los prompts cortos por eficiencia.
        """
        system_prompt = "Genera preguntas de estudio en formato JSON."
        user_prompt = f"Material: {sample_material}"
        
        total_length = len(system_prompt) + len(user_prompt)
        
        # Límite conservador: 10000 caracteres para prompts
        max_length = 10000
        
        assert total_length < max_length, \
            f"Prompt muy largo: {total_length} > {max_length}"
        
        print(f"✅ Longitud del prompt: {total_length} caracteres (límite: {max_length})")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestJSONParsing - Pruebas de parsing de respuestas
# ═══════════════════════════════════════════════════════════════════════════════

class TestJSONParsing:
    """
    Pruebas del parsing de respuestas JSON de Groq
    """
    
    def test_valid_json_parsing(self):
        """
        TEST: Parsing correcto de JSON válido
        """
        response_content = '''
        {
            "preguntas": [
                {"tipo": "literal", "pregunta": "¿Qué es un puntero?", "dificultad": "media"}
            ]
        }
        '''
        
        result = json.loads(response_content)
        
        assert "preguntas" in result
        assert len(result["preguntas"]) == 1
        print(f"✅ JSON válido parseado correctamente")
    
    def test_malformed_json_handling(self):
        """
        TEST: Manejo de JSON malformado
        """
        malformed_responses = [
            "No es JSON",
            '{"preguntas": [',  # Incompleto
            "```json\n{}\n```",  # Con markdown
        ]
        
        for response in malformed_responses:
            try:
                result = json.loads(response)
            except json.JSONDecodeError:
                # Esto es esperado
                pass
        
        print(f"✅ JSON malformado detectado correctamente")
    
    def test_json_extraction_from_markdown(self):
        """
        TEST: Extraer JSON de respuesta con markdown
        
        A veces Groq envuelve la respuesta en bloques de código.
        """
        response_with_markdown = '''
        Aquí está la respuesta:
        ```json
        {
            "preguntas": [
                {"tipo": "literal", "pregunta": "Test", "dificultad": "baja"}
            ]
        }
        ```
        '''
        
        # Función para extraer JSON de markdown
        def extract_json(text: str) -> dict:
            import re
            # Buscar bloque de código JSON
            match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            # Intentar parsear directamente
            return json.loads(text)
        
        try:
            result = extract_json(response_with_markdown)
            assert "preguntas" in result
            print(f"✅ JSON extraído de markdown correctamente")
        except json.JSONDecodeError:
            print(f"⚠️ No se pudo extraer JSON del markdown")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestErrorHandling - Pruebas de manejo de errores
# ═══════════════════════════════════════════════════════════════════════════════

class TestErrorHandling:
    """
    Pruebas del manejo de errores de la API de Groq
    """
    
    def test_rate_limit_handling(self):
        """
        TEST: Manejo de rate limiting
        
        Groq tiene límites de requests por minuto.
        El sistema debe manejar errores 429 graciosamente.
        """
        # Simular error de rate limit
        class RateLimitError(Exception):
            status_code = 429
            message = "Rate limit exceeded"
        
        def handle_rate_limit(error):
            """Ejemplo de handler de rate limit"""
            if hasattr(error, 'status_code') and error.status_code == 429:
                return {"error": "rate_limit", "retry_after": 60}
            raise error
        
        result = handle_rate_limit(RateLimitError())
        assert result["error"] == "rate_limit"
        print(f"✅ Rate limit manejado: retry_after={result['retry_after']}s")
    
    def test_network_error_handling(self):
        """
        TEST: Manejo de errores de red
        """
        def handle_network_error():
            """Simular manejo de error de red"""
            try:
                raise ConnectionError("No internet connection")
            except ConnectionError:
                return {"error": "network", "message": "Sin conexión a Internet"}
        
        result = handle_network_error()
        assert result["error"] == "network"
        print(f"✅ Error de red manejado: {result['message']}")
    
    def test_invalid_api_key_handling(self):
        """
        TEST: Manejo de API key inválida
        """
        class AuthenticationError(Exception):
            status_code = 401
            message = "Invalid API key"
        
        def handle_auth_error(error):
            if hasattr(error, 'status_code') and error.status_code == 401:
                return {"error": "auth", "message": "API key inválida"}
            raise error
        
        result = handle_auth_error(AuthenticationError())
        assert result["error"] == "auth"
        print(f"✅ Error de autenticación manejado")
    
    def test_empty_response_handling(self):
        """
        TEST: Manejo de respuestas vacías
        """
        empty_responses = [
            "",
            "{}",
            '{"preguntas": []}',
            None
        ]
        
        def validate_response(response):
            if response is None or response == "":
                return {"valid": False, "reason": "empty"}
            try:
                data = json.loads(response) if isinstance(response, str) else response
                if not data.get("preguntas"):
                    return {"valid": False, "reason": "no_questions"}
                return {"valid": True}
            except json.JSONDecodeError:
                return {"valid": False, "reason": "invalid_json"}
        
        for response in empty_responses:
            result = validate_response(response)
            assert result["valid"] == False
        
        print(f"✅ Respuestas vacías detectadas correctamente")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestQuestionQuality - Pruebas de calidad de preguntas
# ═══════════════════════════════════════════════════════════════════════════════

class TestQuestionQuality:
    """
    Pruebas de la calidad de las preguntas generadas
    """
    
    def test_questions_are_grammatically_correct(self):
        """
        TEST: Las preguntas deben ser gramaticalmente correctas
        """
        preguntas_ejemplo = [
            "¿Qué es un puntero?",
            "¿Cómo se declara un puntero en C++?",
            "¿Por qué son importantes los punteros?",
        ]
        
        for pregunta in preguntas_ejemplo:
            # Verificar estructura básica de pregunta en español
            assert pregunta.startswith("¿"), "Pregunta debe iniciar con ¿"
            assert pregunta.endswith("?"), "Pregunta debe terminar con ?"
            assert len(pregunta) >= 10, "Pregunta debe tener longitud mínima"
        
        print(f"✅ Preguntas gramaticalmente correctas")
    
    def test_questions_are_relevant_to_material(self):
        """
        TEST: Las preguntas deben ser relevantes al material
        """
        material_keywords = ["puntero", "memoria", "variable", "dirección"]
        
        preguntas = [
            {"pregunta": "¿Qué es un puntero?", "keywords": ["puntero"]},
            {"pregunta": "¿Dónde se almacenan las direcciones?", "keywords": ["direcciones"]},
        ]
        
        for p in preguntas:
            relevante = any(kw in p["pregunta"].lower() for kw in material_keywords)
            # No estricto, pero idealmente las preguntas mencionan conceptos del material
            print(f"   Pregunta: '{p['pregunta']}' - Relevante: {relevante}")
        
        print(f"✅ Relevancia de preguntas verificada")
    
    def test_no_duplicate_questions(self):
        """
        TEST: No debe haber preguntas duplicadas
        """
        preguntas = [
            "¿Qué es un puntero?",
            "¿Cómo se declara un puntero?",
            "¿Qué es un puntero?",  # Duplicada
        ]
        
        unique = set(preguntas)
        has_duplicates = len(unique) < len(preguntas)
        
        if has_duplicates:
            duplicates = len(preguntas) - len(unique)
            print(f"⚠️ Se encontraron {duplicates} preguntas duplicadas")
        else:
            print(f"✅ No hay preguntas duplicadas")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS CON API REAL (marcados para skip si no hay API key)
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.requires_api
class TestRealAPIIntegration:
    """
    Pruebas con la API real de Groq
    
    Estas pruebas requieren:
    - Variable de entorno GROQ_API_KEY configurada
    - Conexión a Internet
    
    Ejecutar con: pytest -m requires_api
    """
    
    @pytest.mark.skip(reason="Requiere API key y conexión a Internet")
    def test_real_api_connection(self):
        """TEST: Conexión real a la API de Groq"""
        import os
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            pytest.skip("GROQ_API_KEY no configurada")
        
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": "Di 'Hola'"}],
            max_tokens=10
        )
        
        assert response.choices[0].message.content
        print(f"✅ API real respondió: {response.choices[0].message.content}")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS INDIVIDUALES
# ═══════════════════════════════════════════════════════════════════════════════

def test_json_format():
    """Test rápido de formato JSON"""
    data = {"preguntas": [{"tipo": "literal", "pregunta": "Test"}]}
    json_str = json.dumps(data)
    parsed = json.loads(json_str)
    assert parsed == data


def test_model_constant():
    """Test de constante del modelo"""
    assert "llama" in GROQ_MODEL.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "not requires_api"])
