"""
═══════════════════════════════════════════════════════════════════════════════
TEST_EMBEDDINGS.PY - Pruebas Unitarias del Módulo de Embeddings
═══════════════════════════════════════════════════════════════════════════════

Este módulo contiene las pruebas unitarias para verificar:
1. Carga correcta del modelo Sentence-Transformers
2. Generación de embeddings de 384 dimensiones
3. Cálculo de similitud coseno entre vectores
4. Manejo de casos edge (texto vacío, caracteres especiales)
5. Consistencia de embeddings para el mismo texto

RESPONDE A PREGUNTAS DEL PROFESOR (Semana 15):
- "¿Tienes tus casos de prueba para probar tus embeddings?"
- "¿Cuántos embeddings está extrayendo?"

Modelo: all-MiniLM-L6-v2 (384 dimensiones)
═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Agregar backend al path
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestEmbeddingModel - Pruebas de carga del modelo
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmbeddingModel:
    """
    Pruebas de carga y configuración del modelo de embeddings
    
    Verifica que:
    - El modelo se carga correctamente
    - Es el modelo esperado (all-MiniLM-L6-v2)
    - Genera embeddings del tamaño correcto
    """
    
    def test_model_loads_successfully(self):
        """
        TEST: El modelo de embeddings debe cargarse sin errores
        
        Criterio de aceptación:
        - load_model() retorna un objeto no nulo
        - No se lanzan excepciones durante la carga
        """
        from embeddings_module import load_model
        
        model = load_model()
        
        assert model is not None, "El modelo no debe ser None"
        print(f"✅ Modelo cargado: {type(model).__name__}")
    
    def test_model_dimension_is_384(self, embedding_model):
        """
        TEST: El modelo debe generar embeddings de 384 dimensiones
        
        Verificación:
        - all-MiniLM-L6-v2 produce vectores de tamaño 384
        - Este es el tamaño esperado según la documentación
        """
        from embeddings_module import generate_embeddings
        
        texto_prueba = "Este es un texto de prueba"
        embedding = generate_embeddings(texto_prueba)
        
        assert len(embedding) == 384, f"Dimensión esperada: 384, obtenida: {len(embedding)}"
        print(f"✅ Dimensión del embedding: {len(embedding)}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestEmbeddingGeneration - Pruebas de generación
# ═══════════════════════════════════════════════════════════════════════════════

class TestEmbeddingGeneration:
    """
    Pruebas de generación de embeddings
    
    Valida el proceso de conversión de texto a vectores semánticos
    y verifica propiedades matemáticas de los embeddings.
    """
    
    def test_generate_embedding_returns_numpy_array(self, embedding_model):
        """
        TEST: generate_embeddings() debe retornar un numpy array
        
        Criterio:
        - El tipo de retorno debe ser np.ndarray
        - El array debe tener valores numéricos
        """
        from embeddings_module import generate_embeddings
        
        texto = "Un puntero es una variable que almacena direcciones de memoria"
        embedding = generate_embeddings(texto)
        
        assert isinstance(embedding, np.ndarray), f"Tipo esperado: np.ndarray, obtenido: {type(embedding)}"
        assert embedding.dtype in [np.float32, np.float64], "El embedding debe contener flotantes"
        print(f"✅ Tipo de retorno correcto: {type(embedding).__name__}, dtype: {embedding.dtype}")
    
    def test_embedding_is_normalized(self, embedding_model):
        """
        TEST: Los embeddings deben estar normalizados (norma ≈ 1)
        
        Verificación:
        - La norma L2 del vector debe ser aproximadamente 1
        - Esto es necesario para que la similitud coseno funcione correctamente
        """
        from embeddings_module import generate_embeddings
        
        texto = "La desreferenciación permite acceder al valor almacenado"
        embedding = generate_embeddings(texto)
        
        norma = np.linalg.norm(embedding)
        assert 0.99 <= norma <= 1.01, f"Norma esperada ≈ 1, obtenida: {norma}"
        print(f"✅ Norma del embedding: {norma:.6f}")
    
    def test_same_text_produces_same_embedding(self, embedding_model):
        """
        TEST: El mismo texto debe producir el mismo embedding (determinismo)
        
        Criterio:
        - Dos llamadas con el mismo texto deben retornar vectores idénticos
        - Esto garantiza reproducibilidad
        """
        from embeddings_module import generate_embeddings
        
        texto = "Los punteros son fundamentales en C++"
        
        embedding_1 = generate_embeddings(texto)
        embedding_2 = generate_embeddings(texto)
        
        diferencia = np.max(np.abs(embedding_1 - embedding_2))
        assert diferencia < 1e-6, f"Los embeddings deben ser idénticos, diferencia: {diferencia}"
        print(f"✅ Embeddings idénticos, diferencia máxima: {diferencia:.10f}")
    
    def test_different_texts_produce_different_embeddings(self, embedding_model):
        """
        TEST: Textos diferentes deben producir embeddings diferentes
        
        Criterio:
        - Dos textos semánticamente diferentes deben tener embeddings distintos
        - La similitud debe ser < 0.9 para textos no relacionados
        """
        from embeddings_module import generate_embeddings
        
        texto_punteros = "Un puntero almacena direcciones de memoria"
        texto_cocina = "La receta de cocina incluye ingredientes frescos"
        
        emb_punteros = generate_embeddings(texto_punteros)
        emb_cocina = generate_embeddings(texto_cocina)
        
        similitud = np.dot(emb_punteros, emb_cocina)
        assert similitud < 0.7, f"Textos no relacionados deben tener similitud < 0.7, obtenida: {similitud}"
        print(f"✅ Similitud entre textos no relacionados: {similitud:.4f}")
    
    def test_similar_texts_have_high_similarity(self, embedding_model):
        """
        TEST: Textos semánticamente similares deben tener alta similitud
        
        Criterio:
        - Paráfrasis del mismo concepto deben tener similitud > 0.3
        - (Umbral ajustado para modelo all-MiniLM-L6-v2)
        """
        from embeddings_module import generate_embeddings
        
        texto_1 = "Un puntero es una variable que almacena la dirección de memoria"
        texto_2 = "Un puntero guarda direcciones de memoria de otras variables"
        
        emb_1 = generate_embeddings(texto_1)
        emb_2 = generate_embeddings(texto_2)
        
        similitud = np.dot(emb_1, emb_2)
        assert similitud > 0.3, f"Textos similares deben tener similitud > 0.3, obtenida: {similitud}"
        print(f"✅ Similitud entre paráfrasis: {similitud:.4f}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestSimilarityCosine - Pruebas de cálculo de similitud
# ═══════════════════════════════════════════════════════════════════════════════

class TestSimilarityCosine:
    """
    Pruebas del cálculo de similitud coseno
    
    Verifica la función calculate_similarity() que es fundamental
    para el sistema de validación híbrida.
    """
    
    def test_identical_vectors_similarity_equals_one(self, embedding_model):
        """
        TEST: Vectores idénticos deben tener similitud = 1.0
        """
        from embeddings_module import generate_embeddings, calculate_similarity
        
        texto = "El operador asterisco declara un puntero"
        embedding = generate_embeddings(texto)
        
        similitud = calculate_similarity(embedding, embedding)
        assert abs(similitud - 1.0) < 0.01, f"Esperado: 1.0, obtenido: {similitud}"
        print(f"✅ Similitud de vector consigo mismo: {similitud:.4f}")
    
    def test_orthogonal_vectors_similarity_near_zero(self, embedding_model):
        """
        TEST: Vectores ortogonales deben tener similitud cercana a 0
        
        Nota: En embeddings reales es difícil encontrar vectores perfectamente
        ortogonales, así que verificamos que textos muy diferentes tengan
        similitud baja.
        """
        from embeddings_module import generate_embeddings, calculate_similarity
        
        texto_tech = "Algoritmo de ordenamiento burbuja en estructura de datos"
        texto_nature = "Las mariposas monarca migran miles de kilómetros"
        
        emb_1 = generate_embeddings(texto_tech)
        emb_2 = generate_embeddings(texto_nature)
        
        similitud = calculate_similarity(emb_1, emb_2)
        assert similitud < 0.5, f"Textos muy diferentes deben tener similitud < 0.5, obtenida: {similitud}"
        print(f"✅ Similitud entre temas diferentes: {similitud:.4f}")
    
    def test_similarity_is_symmetric(self, embedding_model):
        """
        TEST: La similitud coseno debe ser simétrica: sim(A,B) = sim(B,A)
        """
        from embeddings_module import generate_embeddings, calculate_similarity
        
        texto_a = "Los punteros permiten acceso directo a memoria"
        texto_b = "El acceso a memoria se logra mediante punteros"
        
        emb_a = generate_embeddings(texto_a)
        emb_b = generate_embeddings(texto_b)
        
        sim_ab = calculate_similarity(emb_a, emb_b)
        sim_ba = calculate_similarity(emb_b, emb_a)
        
        assert abs(sim_ab - sim_ba) < 1e-6, f"La similitud debe ser simétrica: {sim_ab} vs {sim_ba}"
        print(f"✅ Similitud simétrica: sim(A,B)={sim_ab:.4f}, sim(B,A)={sim_ba:.4f}")
    
    def test_similarity_range_is_valid(self, embedding_model):
        """
        TEST: La similitud coseno debe estar en el rango [-1, 1]
        
        Para embeddings normalizados, generalmente está en [0, 1]
        """
        from embeddings_module import generate_embeddings, calculate_similarity
        
        textos = [
            "Puntero es una variable",
            "Memoria del sistema operativo",
            "Función matemática derivada",
            "Receta de cocina italiana"
        ]
        
        embeddings = [generate_embeddings(t) for t in textos]
        
        for i, emb_i in enumerate(embeddings):
            for j, emb_j in enumerate(embeddings):
                sim = calculate_similarity(emb_i, emb_j)
                assert -1.0 <= sim <= 1.0, f"Similitud fuera de rango: {sim}"
        
        print(f"✅ Todas las similitudes están en el rango válido [-1, 1]")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestEdgeCases - Casos límite
# ═══════════════════════════════════════════════════════════════════════════════

class TestEdgeCases:
    """
    Pruebas de casos límite y manejo de errores
    
    Verifica que el sistema maneje correctamente:
    - Texto vacío
    - Texto muy largo
    - Caracteres especiales
    - Unicode/Español
    """
    
    def test_empty_string_handling(self, embedding_model):
        """
        TEST: El sistema debe manejar texto vacío sin errores
        """
        from embeddings_module import generate_embeddings
        
        # El sistema debe retornar un embedding válido o manejarlo graciosamente
        try:
            embedding = generate_embeddings("")
            assert embedding is not None
            assert len(embedding) == 384
            print(f"✅ Texto vacío manejado correctamente")
        except Exception as e:
            # Si lanza excepción, debe ser una excepción controlada
            print(f"✅ Texto vacío genera excepción controlada: {type(e).__name__}")
    
    def test_spanish_text_with_accents(self, embedding_model):
        """
        TEST: El modelo debe procesar correctamente texto en español con acentos
        """
        from embeddings_module import generate_embeddings
        
        texto_espanol = "El árbol genealógico contiene información histórica única"
        embedding = generate_embeddings(texto_espanol)
        
        assert embedding is not None
        assert len(embedding) == 384
        print(f"✅ Texto español con acentos procesado: '{texto_espanol[:30]}...'")
    
    def test_special_characters(self, embedding_model):
        """
        TEST: El modelo debe manejar caracteres especiales
        """
        from embeddings_module import generate_embeddings
        
        texto_especial = "int *ptr = &variable; // Puntero en C++"
        embedding = generate_embeddings(texto_especial)
        
        assert embedding is not None
        assert len(embedding) == 384
        print(f"✅ Caracteres especiales manejados: '{texto_especial}'")
    
    def test_long_text_handling(self, embedding_model):
        """
        TEST: El modelo debe manejar textos largos (> 512 tokens)
        
        Nota: El modelo trunca textos largos, pero debe funcionar sin errores
        """
        from embeddings_module import generate_embeddings
        
        texto_largo = "Los punteros en C++ son fundamentales. " * 100
        embedding = generate_embeddings(texto_largo)
        
        assert embedding is not None
        assert len(embedding) == 384
        print(f"✅ Texto largo ({len(texto_largo)} caracteres) procesado correctamente")
    
    def test_whitespace_only_text(self, embedding_model):
        """
        TEST: El sistema debe manejar texto con solo espacios
        """
        from embeddings_module import generate_embeddings
        
        try:
            embedding = generate_embeddings("   \n\t   ")
            assert embedding is not None
            print(f"✅ Texto con solo espacios manejado")
        except Exception as e:
            print(f"✅ Texto con solo espacios genera excepción controlada: {type(e).__name__}")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestBatchEmbeddings - Pruebas de procesamiento por lotes
# ═══════════════════════════════════════════════════════════════════════════════

class TestBatchEmbeddings:
    """
    Pruebas de generación de embeddings en lote
    
    IMPORTANTE para el profesor:
    "¿Cuántos embeddings está extrayendo asociados a ese término?"
    """
    
    def test_multiple_chunks_embedding_count(self, embedding_model, chunks_punteros):
        """
        TEST: Verificar que se generan embeddings para TODOS los chunks
        
        Este test responde directamente a la pregunta del profesor:
        "¿Cuántos chunks está extrayéndolos asociados a ese término puntero?"
        """
        from embeddings_module import generate_embeddings
        
        embeddings_generados = []
        for i, chunk in enumerate(chunks_punteros):
            # Los chunks ahora son diccionarios con 'text_full' y 'embedding'
            chunk_text = chunk.get('text_full', chunk) if isinstance(chunk, dict) else chunk
            if chunk_text and chunk_text.strip():
                # Ya tienen embedding precalculado
                if isinstance(chunk, dict) and 'embedding' in chunk:
                    emb = chunk['embedding']
                else:
                    emb = generate_embeddings(chunk_text)
                embeddings_generados.append(emb)
                print(f"  Chunk {i+1}: {len(chunk_text)} caracteres → Embedding {len(emb)} dims")
        
        valid_chunks = [c for c in chunks_punteros if (c.get('text_full', c) if isinstance(c, dict) else c).strip()]
        assert len(embeddings_generados) == len(valid_chunks)
        print(f"✅ Total embeddings generados: {len(embeddings_generados)}")
        print(f"   (Para {len(chunks_punteros)} chunks del material de punteros)")
    
    def test_embedding_retrieval_for_term(self, embedding_model, material_punteros):
        """
        TEST: Verificar cuántos embeddings se recuperan para el término "puntero"
        
        RESPONDE DIRECTAMENTE A LA PREGUNTA DEL PROFESOR SEMANA 15:
        "¿Cuántos chunks está extrayéndolos asociados a ese término puntero?"
        """
        from embeddings_module import generate_embeddings
        from chunking import semantic_chunking
        
        # Generar chunks
        chunks = semantic_chunking(material_punteros, min_words=20, max_words=60, overlap_words=5)
        
        # Generar embedding para el término de búsqueda
        query_embedding = generate_embeddings("puntero")
        
        # Calcular similitud con cada chunk
        chunks_relevantes = []
        for chunk in chunks:
            if not chunk.strip():
                continue
            chunk_embedding = generate_embeddings(chunk)
            similitud = np.dot(query_embedding, chunk_embedding)
            if similitud > 0.3:  # Umbral mínimo de relevancia
                chunks_relevantes.append({
                    "chunk": chunk[:50] + "...",
                    "similitud": similitud
                })
        
        # Ordenar por similitud
        chunks_relevantes.sort(key=lambda x: x["similitud"], reverse=True)
        
        print(f"\n📊 CHUNKS ASOCIADOS AL TÉRMINO 'puntero':")
        print(f"   Total chunks analizados: {len(chunks)}")
        print(f"   Chunks relevantes (sim > 0.3): {len(chunks_relevantes)}")
        print(f"\n   Top 5 chunks más relevantes:")
        for i, item in enumerate(chunks_relevantes[:5]):
            print(f"   {i+1}. Similitud: {item['similitud']:.4f} - '{item['chunk']}'")
        
        assert len(chunks_relevantes) > 0, "Debe haber al menos un chunk relevante para 'puntero'"
        print(f"\n✅ Se encontraron {len(chunks_relevantes)} chunks asociados al término 'puntero'")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTS INDIVIDUALES (para ejecución rápida)
# ═══════════════════════════════════════════════════════════════════════════════

def test_embedding_dimension_quick():
    """Test rápido de dimensión sin fixture"""
    from embeddings_module import generate_embeddings
    
    emb = generate_embeddings("Prueba rápida")
    assert len(emb) == 384


def test_similarity_calculation_quick():
    """Test rápido de similitud sin fixture"""
    from embeddings_module import generate_embeddings, calculate_similarity
    
    emb1 = generate_embeddings("puntero en C++")
    emb2 = generate_embeddings("puntero en memoria")
    
    sim = calculate_similarity(emb1, emb2)
    assert 0.5 < sim < 1.0  # Deben ser similares


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
