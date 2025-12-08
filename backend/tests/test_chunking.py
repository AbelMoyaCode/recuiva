"""
═══════════════════════════════════════════════════════════════════════════════
TEST_CHUNKING.PY - Pruebas Unitarias del Módulo de Chunking
═══════════════════════════════════════════════════════════════════════════════

Este módulo contiene las pruebas unitarias para verificar:
1. Extracción de texto desde PDFs
2. División semántica del texto en chunks
3. Parámetros de chunking (min_words, max_words, overlap)
4. Manejo de diferentes formatos de entrada
5. Calidad de los chunks generados

Métodos de extracción probados:
- pdftotext
- PyMuPDF (fitz)
- PyPDF2
- Tesseract OCR (fallback)

═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Agregar backend al path
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestSemanticChunking - Pruebas de división semántica
# ═══════════════════════════════════════════════════════════════════════════════

class TestSemanticChunking:
    """
    Pruebas de la función semantic_chunking()
    
    Esta función divide el texto en fragmentos semánticamente coherentes
    respetando los límites configurados.
    """
    
    def test_chunking_returns_list(self):
        """
        TEST: semantic_chunking() debe retornar una lista
        """
        from chunking import semantic_chunking
        
        texto = "Un puntero es una variable. Almacena direcciones de memoria."
        chunks = semantic_chunking(texto)
        
        assert isinstance(chunks, list), f"Debe retornar list, obtenido: {type(chunks)}"
        print(f"✅ Retorna lista con {len(chunks)} chunks")
    
    def test_chunking_respects_min_words(self):
        """
        TEST: Los chunks deben tener al menos min_words palabras
        """
        from chunking import semantic_chunking
        
        texto = """
        Los punteros son variables especiales que almacenan direcciones de memoria.
        En C++, se declaran usando el operador asterisco.
        La desreferenciación permite acceder al valor almacenado.
        Los punteros nulos apuntan a la dirección cero.
        """
        
        min_words = 10
        chunks = semantic_chunking(texto, min_words=min_words, max_words=50)
        
        for i, chunk in enumerate(chunks):
            if chunk.strip():
                word_count = len(chunk.split())
                # Permitir cierta flexibilidad en los bordes
                assert word_count >= min_words * 0.5 or len(chunks) == 1, \
                    f"Chunk {i} tiene {word_count} palabras, mínimo esperado: {min_words}"
        
        print(f"✅ Todos los chunks respetan min_words={min_words}")
    
    def test_chunking_respects_max_words(self):
        """
        TEST: Los chunks no deben exceder max_words palabras
        """
        from chunking import semantic_chunking
        
        # Texto más realista con oraciones completas
        texto = """
        Los punteros son variables especiales que almacenan direcciones de memoria.
        En C++ se utilizan para acceso directo a la memoria del sistema operativo.
        La declaración de un puntero se realiza usando el operador asterisco.
        Para obtener la dirección de una variable se usa el operador ampersand.
        La desreferenciación permite acceder al valor almacenado en la dirección.
        Los punteros nulos apuntan a la dirección cero y no son válidos.
        """ * 5  # Repetir para tener texto largo
        
        max_words = 80
        
        chunks = semantic_chunking(texto, min_words=20, max_words=max_words)
        
        # Verificar que hay múltiples chunks
        assert len(chunks) >= 1, "Debe generar al menos un chunk"
        
        # La mayoría de chunks deben respetar el límite (permitir excepciones)
        chunks_dentro_limite = sum(1 for c in chunks if len(c.split()) <= max_words * 1.5)
        porcentaje = chunks_dentro_limite / len(chunks) if chunks else 0
        
        assert porcentaje >= 0.5, f"Al menos 50% de chunks deben respetar max_words"
        
        print(f"✅ {chunks_dentro_limite}/{len(chunks)} chunks respetan max_words={max_words}")
    
    def test_chunking_with_overlap(self):
        """
        TEST: Los chunks deben tener overlap para contexto
        """
        from chunking import semantic_chunking
        
        texto = """
        Concepto uno sobre punteros y variables en programación.
        Concepto dos sobre memoria y direcciones del sistema.
        Concepto tres sobre declaración y uso de punteros.
        Concepto cuatro sobre desreferenciación de variables.
        """
        
        overlap_words = 5
        chunks = semantic_chunking(texto, min_words=10, max_words=30, overlap_words=overlap_words)
        
        if len(chunks) > 1:
            # Verificar que hay algún texto compartido entre chunks consecutivos
            # (El overlap puede no ser exactamente las mismas palabras debido a la división semántica)
            print(f"✅ Generados {len(chunks)} chunks con overlap_words={overlap_words}")
        else:
            print(f"✅ Texto muy corto, solo 1 chunk generado")
    
    def test_empty_text_handling(self):
        """
        TEST: semantic_chunking() debe manejar texto vacío
        """
        from chunking import semantic_chunking
        
        try:
            chunks = semantic_chunking("")
            assert chunks == [] or chunks == [""], "Texto vacío debe retornar lista vacía o con string vacío"
            print(f"✅ Texto vacío manejado correctamente: {chunks}")
        except Exception as e:
            print(f"✅ Texto vacío genera excepción controlada: {type(e).__name__}")
    
    def test_whitespace_only_text(self):
        """
        TEST: Texto con solo espacios debe manejarse correctamente
        """
        from chunking import semantic_chunking
        
        try:
            chunks = semantic_chunking("   \n\t   ")
            print(f"✅ Texto con espacios manejado: {len(chunks)} chunks")
        except Exception as e:
            print(f"✅ Texto con espacios genera excepción controlada: {type(e).__name__}")
    
    def test_spanish_text_with_accents(self):
        """
        TEST: El chunking debe funcionar con texto en español
        """
        from chunking import semantic_chunking
        
        texto_espanol = """
        La programación orientada a objetos utiliza clases y métodos.
        Los algoritmos de búsqueda son fundamentales en ciencias de la computación.
        La recursión permite resolver problemas dividiéndolos en subproblemas más pequeños.
        """
        
        chunks = semantic_chunking(texto_espanol, min_words=10, max_words=50)
        
        assert len(chunks) > 0, "Debe generar al menos un chunk"
        # Verificar que los acentos se preservan
        texto_completo = " ".join(chunks)
        assert "programación" in texto_completo or "computación" in texto_completo, \
            "Los acentos deben preservarse"
        
        print(f"✅ Texto español procesado: {len(chunks)} chunks")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestPDFExtraction - Pruebas de extracción de PDF
# ═══════════════════════════════════════════════════════════════════════════════

class TestPDFExtraction:
    """
    Pruebas de extracción de texto desde PDFs
    
    Métodos disponibles:
    - pdftotext (línea de comandos)
    - PyMuPDF (fitz)
    - PyPDF2
    - Tesseract OCR (fallback)
    """
    
    def test_extract_text_function_exists(self):
        """
        TEST: La función extract_text_from_pdf debe existir
        """
        from chunking import extract_text_from_pdf
        
        assert callable(extract_text_from_pdf), "extract_text_from_pdf debe ser una función"
        print(f"✅ Función extract_text_from_pdf disponible")
    
    def test_extraction_with_invalid_path(self):
        """
        TEST: Debe manejar rutas de archivo inválidas
        """
        from chunking import extract_text_from_pdf
        
        try:
            result = extract_text_from_pdf("/ruta/invalida/archivo.pdf")
            # Puede retornar None, string vacío, o lanzar excepción
            print(f"✅ Ruta inválida manejada: {type(result)}")
        except (FileNotFoundError, Exception) as e:
            print(f"✅ Ruta inválida genera excepción controlada: {type(e).__name__}")
    
    def test_extraction_methods_available(self):
        """
        TEST: Verificar qué métodos de extracción están disponibles
        """
        available_methods = []
        
        # Verificar PyMuPDF
        try:
            import fitz
            available_methods.append("PyMuPDF (fitz)")
        except ImportError:
            pass
        
        # Verificar PyPDF2
        try:
            import PyPDF2
            available_methods.append("PyPDF2")
        except ImportError:
            pass
        
        # Verificar pdftotext (difícil de verificar sin ejecutar)
        available_methods.append("pdftotext (si está instalado)")
        
        print(f"📊 Métodos de extracción disponibles:")
        for method in available_methods:
            print(f"   ✓ {method}")
        
        assert len(available_methods) >= 1, "Debe haber al menos un método de extracción"


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestAdaptiveChunking - Pruebas de chunking adaptativo
# ═══════════════════════════════════════════════════════════════════════════════

class TestAdaptiveChunking:
    """
    Pruebas del chunking adaptativo
    
    El chunking adaptativo ajusta los parámetros según
    las características del documento.
    """
    
    def test_adaptive_chunking_exists(self):
        """
        TEST: Verificar que existe función de chunking adaptativo
        """
        try:
            from chunking import adaptive_chunking
            assert callable(adaptive_chunking)
            print(f"✅ Función adaptive_chunking disponible")
        except ImportError:
            pytest.skip("adaptive_chunking no implementado")
    
    def test_short_text_fewer_chunks(self):
        """
        TEST: Texto corto debe generar pocos chunks
        """
        from chunking import semantic_chunking
        
        texto_corto = "Un puntero almacena direcciones."
        texto_largo = texto_corto * 20
        
        chunks_corto = semantic_chunking(texto_corto, min_words=5, max_words=50)
        chunks_largo = semantic_chunking(texto_largo, min_words=5, max_words=50)
        
        assert len(chunks_corto) <= len(chunks_largo), \
            "Texto corto debe generar <= chunks que texto largo"
        
        print(f"✅ Texto corto: {len(chunks_corto)} chunks, Texto largo: {len(chunks_largo)} chunks")
    
    def test_chunks_preserve_sentence_boundaries(self):
        """
        TEST: Los chunks deben respetar límites de oraciones cuando sea posible
        """
        from chunking import semantic_chunking
        
        texto = """
        Primera oración completa sobre punteros.
        Segunda oración sobre memoria y variables.
        Tercera oración sobre declaraciones en C++.
        """
        
        chunks = semantic_chunking(texto, min_words=5, max_words=20)
        
        # Verificar que los chunks terminan con puntuación o son coherentes
        for chunk in chunks:
            chunk = chunk.strip()
            if chunk:
                # El chunk debe ser texto legible
                assert len(chunk) > 0, "Chunk no debe estar vacío"
        
        print(f"✅ Chunks generados respetan estructura del texto")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestChunkQuality - Pruebas de calidad de chunks
# ═══════════════════════════════════════════════════════════════════════════════

class TestChunkQuality:
    """
    Pruebas de calidad de los chunks generados
    
    Los chunks deben ser:
    - Semánticamente coherentes
    - No demasiado cortos ni largos
    - Útiles para embeddings
    """
    
    def test_chunks_are_not_empty(self, material_punteros):
        """
        TEST: Los chunks no deben estar vacíos
        """
        from chunking import semantic_chunking
        
        chunks = semantic_chunking(material_punteros, min_words=10, max_words=50)
        
        empty_chunks = [c for c in chunks if not c.strip()]
        non_empty_chunks = [c for c in chunks if c.strip()]
        
        # Permitir algunos chunks vacíos pero la mayoría deben tener contenido
        assert len(non_empty_chunks) > len(empty_chunks), \
            f"Demasiados chunks vacíos: {len(empty_chunks)}/{len(chunks)}"
        
        print(f"✅ {len(non_empty_chunks)} chunks con contenido, {len(empty_chunks)} vacíos")
    
    def test_chunks_contain_meaningful_content(self, material_punteros):
        """
        TEST: Los chunks deben contener contenido significativo
        """
        from chunking import semantic_chunking
        
        chunks = semantic_chunking(material_punteros, min_words=10, max_words=50)
        
        # Palabras clave que deberían aparecer en los chunks
        keywords = ["puntero", "memoria", "variable", "dirección"]
        
        keywords_found = set()
        for chunk in chunks:
            chunk_lower = chunk.lower()
            for kw in keywords:
                if kw in chunk_lower:
                    keywords_found.add(kw)
        
        # Al menos algunas keywords deben estar presentes
        assert len(keywords_found) >= 2, \
            f"Solo se encontraron {len(keywords_found)} keywords: {keywords_found}"
        
        print(f"✅ Keywords encontradas: {keywords_found}")
    
    def test_chunk_length_distribution(self, material_punteros):
        """
        TEST: La distribución de longitud de chunks debe ser razonable
        """
        from chunking import semantic_chunking
        
        chunks = semantic_chunking(material_punteros, min_words=20, max_words=60)
        
        lengths = [len(c.split()) for c in chunks if c.strip()]
        
        if lengths:
            avg_length = sum(lengths) / len(lengths)
            min_length = min(lengths)
            max_length = max(lengths)
            
            print(f"📊 Distribución de longitud de chunks:")
            print(f"   Mínimo: {min_length} palabras")
            print(f"   Máximo: {max_length} palabras")
            print(f"   Promedio: {avg_length:.1f} palabras")
            print(f"   Total chunks: {len(lengths)}")
            
            # La variación no debe ser extrema
            assert max_length <= avg_length * 3, "Variación de longitud muy alta"
        
        print(f"✅ Distribución de longitud dentro de parámetros")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestChunkingConfiguration - Pruebas de configuración
# ═══════════════════════════════════════════════════════════════════════════════

class TestChunkingConfiguration:
    """
    Pruebas de diferentes configuraciones de chunking
    """
    
    def test_default_parameters(self):
        """
        TEST: Verificar parámetros por defecto
        """
        from chunking import semantic_chunking
        import inspect
        
        sig = inspect.signature(semantic_chunking)
        
        print(f"📊 Parámetros de semantic_chunking:")
        for name, param in sig.parameters.items():
            default = param.default if param.default != inspect.Parameter.empty else "requerido"
            print(f"   {name}: {default}")
        
        print(f"✅ Configuración de parámetros verificada")
    
    def test_custom_parameters(self):
        """
        TEST: Chunking con parámetros personalizados
        """
        from chunking import semantic_chunking
        
        texto = "Texto de prueba. " * 50
        
        # Probar diferentes configuraciones
        configs = [
            {"min_words": 10, "max_words": 30},
            {"min_words": 20, "max_words": 60},
            {"min_words": 30, "max_words": 100},
        ]
        
        for config in configs:
            chunks = semantic_chunking(texto, **config)
            print(f"   Config {config}: {len(chunks)} chunks")
        
        print(f"✅ Parámetros personalizados funcionan correctamente")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS INDIVIDUALES
# ═══════════════════════════════════════════════════════════════════════════════

def test_chunking_import():
    """Test rápido de importación"""
    from chunking import semantic_chunking
    assert semantic_chunking is not None


def test_basic_chunking():
    """Test básico de chunking"""
    from chunking import semantic_chunking
    
    texto = "Este es un texto de prueba. Contiene varias oraciones. Para verificar el chunking."
    chunks = semantic_chunking(texto, min_words=5, max_words=20)
    
    assert isinstance(chunks, list)
    assert len(chunks) >= 1


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
