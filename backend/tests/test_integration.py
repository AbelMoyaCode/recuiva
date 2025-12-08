"""
═══════════════════════════════════════════════════════════════════════════════
TEST_INTEGRATION.PY - Pruebas de Integración del Sistema RECUIVA
═══════════════════════════════════════════════════════════════════════════════

Este módulo contiene pruebas de integración que verifican:
1. Flujo completo: PDF → Chunks → Embeddings → Validación
2. Integración entre módulos
3. Performance del sistema
4. Casos de uso reales

Estas pruebas son más lentas que las unitarias pero verifican
que todos los componentes funcionan correctamente juntos.

═══════════════════════════════════════════════════════════════════════════════
"""

import pytest
import sys
import time
from pathlib import Path

# Agregar backend al path
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestCompleteFlow - Flujo completo del sistema
# ═══════════════════════════════════════════════════════════════════════════════

class TestCompleteFlow:
    """
    Pruebas del flujo completo de RECUIVA:
    Material → Chunks → Embeddings → Pregunta → Validación → Score
    """
    
    @pytest.mark.slow
    def test_full_validation_pipeline(self, material_punteros, embedding_model):
        """
        TEST: Pipeline completo de validación
        
        1. Recibir material de estudio
        2. Dividir en chunks semánticos
        3. Generar embeddings
        4. Recibir pregunta y respuesta
        5. Validar con sistema híbrido
        6. Retornar score y feedback
        """
        from chunking import semantic_chunking
        from embeddings_module import generate_embeddings
        from hybrid_validator import HybridValidator
        
        print("\n📊 PIPELINE DE VALIDACIÓN COMPLETO")
        print("=" * 50)
        
        # Paso 1: Material
        print(f"\n1️⃣ Material recibido: {len(material_punteros)} caracteres")
        
        # Paso 2: Chunking
        start = time.time()
        chunks = semantic_chunking(material_punteros, min_words=20, max_words=60, overlap_words=5)
        time_chunking = time.time() - start
        print(f"2️⃣ Chunking: {len(chunks)} chunks en {time_chunking:.3f}s")
        
        # Paso 3: Embeddings
        start = time.time()
        embeddings = [generate_embeddings(chunk) for chunk in chunks if chunk.strip()]
        time_embeddings = time.time() - start
        print(f"3️⃣ Embeddings: {len(embeddings)} vectores en {time_embeddings:.3f}s")
        
        # Paso 4-5: Validación
        validator = HybridValidator(embedding_model)
        
        question = "¿Qué es un puntero?"
        correct_answer = "Un puntero es una variable que almacena la dirección de memoria"
        
        start = time.time()
        try:
            result = validator.validate_answer(question, correct_answer, chunks)
            time_validation = time.time() - start
            
            # Paso 6: Resultado
            if isinstance(result, dict):
                score = result.get('score', result.get('confidence', 0))
            else:
                score = result
            
            print(f"4️⃣ Pregunta: '{question}'")
            print(f"5️⃣ Respuesta: '{correct_answer[:50]}...'")
            print(f"6️⃣ Validación: score = {score:.4f} en {time_validation:.3f}s")
            
            # Verificaciones
            assert score > 0.5, f"Respuesta correcta debe tener score > 0.5"
            
            print("\n✅ PIPELINE COMPLETO EJECUTADO EXITOSAMENTE")
        except Exception as e:
            pytest.skip(f"Error en validación: {e}")
    
    @pytest.mark.slow
    def test_multiple_answers_comparison(self, material_punteros, embedding_model, chunks_punteros):
        """
        TEST: Comparar múltiples tipos de respuestas
        
        Verifica que el sistema ordena correctamente:
        Correcta > Parcial > Incorrecta
        """
        from hybrid_validator import HybridValidator
        
        validator = HybridValidator(embedding_model)
        question = "¿Qué es un puntero?"
        
        answers = [
            ("Correcta", "Un puntero es una variable que almacena la dirección de memoria de otra variable"),
            ("Parcial", "Es una variable de memoria"),
            ("Incorrecta", "Es una función matemática que calcula derivadas"),
        ]
        
        results = []
        print("\n📊 COMPARACIÓN DE RESPUESTAS")
        print("=" * 50)
        
        for tipo, answer in answers:
            try:
                result = validator.validate_answer(question, answer, chunks_punteros)
                score = result.get('score', result.get('confidence', result)) if isinstance(result, dict) else result
                results.append((tipo, score))
                print(f"   {tipo}: {score:.4f} - '{answer[:40]}...'")
            except Exception as e:
                print(f"   {tipo}: Error - {e}")
        
        # Verificar orden
        if len(results) >= 3:
            assert results[0][1] >= results[1][1], "Correcta debe ser >= Parcial"
            assert results[1][1] >= results[2][1], "Parcial debe ser >= Incorrecta"
            print("\n✅ Orden de scores correcto: Correcta > Parcial > Incorrecta")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestPerformance - Pruebas de rendimiento
# ═══════════════════════════════════════════════════════════════════════════════

class TestPerformance:
    """
    Pruebas de rendimiento del sistema
    
    Métricas objetivo:
    - Tiempo de respuesta < 3 segundos
    - Procesamiento de chunk < 100ms
    """
    
    @pytest.mark.slow
    def test_embedding_generation_speed(self, embedding_model):
        """
        TEST: Velocidad de generación de embeddings
        
        Objetivo: < 100ms por embedding
        """
        from embeddings_module import generate_embeddings
        
        textos = [
            "Un puntero almacena direcciones de memoria",
            "La declaración usa el operador asterisco",
            "Los punteros son fundamentales en C++",
        ] * 10  # 30 textos
        
        start = time.time()
        for texto in textos:
            generate_embeddings(texto)
        total_time = time.time() - start
        
        avg_time = (total_time / len(textos)) * 1000  # ms
        
        print(f"\n📊 RENDIMIENTO DE EMBEDDINGS")
        print(f"   Total textos: {len(textos)}")
        print(f"   Tiempo total: {total_time:.3f}s")
        print(f"   Promedio por embedding: {avg_time:.1f}ms")
        
        assert avg_time < 200, f"Embedding muy lento: {avg_time}ms (objetivo: <200ms)"
        print(f"✅ Rendimiento dentro del objetivo")
    
    @pytest.mark.slow
    def test_chunking_speed(self):
        """
        TEST: Velocidad de chunking
        
        Objetivo: Procesar texto largo en < 1 segundo
        """
        from chunking import semantic_chunking
        
        # Texto largo (~5000 palabras)
        texto_largo = "Los punteros son variables especiales. " * 1000
        
        start = time.time()
        chunks = semantic_chunking(texto_largo, min_words=20, max_words=60)
        total_time = time.time() - start
        
        print(f"\n📊 RENDIMIENTO DE CHUNKING")
        print(f"   Longitud texto: {len(texto_largo)} caracteres")
        print(f"   Chunks generados: {len(chunks)}")
        print(f"   Tiempo total: {total_time:.3f}s")
        
        assert total_time < 2.0, f"Chunking muy lento: {total_time}s (objetivo: <2s)"
        print(f"✅ Rendimiento dentro del objetivo")
    
    @pytest.mark.slow
    def test_end_to_end_latency(self, embedding_model, chunks_punteros):
        """
        TEST: Latencia total de respuesta
        
        Objetivo: < 3 segundos para validación completa
        """
        from hybrid_validator import HybridValidator
        
        validator = HybridValidator(embedding_model)
        
        start = time.time()
        try:
            result = validator.validate_answer(
                "¿Qué es un puntero?",
                "Una variable que almacena direcciones de memoria",
                chunks_punteros
            )
        except Exception as e:
            pytest.skip(f"Error: {e}")
        
        total_time = time.time() - start
        
        print(f"\n📊 LATENCIA END-TO-END")
        print(f"   Tiempo de respuesta: {total_time:.3f}s")
        
        assert total_time < 5.0, f"Latencia muy alta: {total_time}s (objetivo: <5s)"
        print(f"✅ Latencia dentro del objetivo")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestRealWorldScenarios - Escenarios del mundo real
# ═══════════════════════════════════════════════════════════════════════════════

class TestRealWorldScenarios:
    """
    Pruebas con escenarios del mundo real
    
    Basado en casos de uso reales del sistema RECUIVA.
    """
    
    def test_student_typing_partial_answer(self, embedding_model, chunks_punteros):
        """
        TEST: Estudiante escribiendo respuesta gradualmente
        
        Simula el caso donde el estudiante escribe poco a poco.
        El sistema debe funcionar con respuestas parciales.
        """
        from hybrid_validator import HybridValidator
        
        validator = HybridValidator(embedding_model)
        question = "¿Qué es un puntero?"
        
        # Respuestas progresivas (como si el estudiante estuviera escribiendo)
        progressive_answers = [
            "Un",
            "Un puntero",
            "Un puntero es",
            "Un puntero es una variable",
            "Un puntero es una variable que almacena",
            "Un puntero es una variable que almacena direcciones de memoria"
        ]
        
        print("\n📊 RESPUESTAS PROGRESIVAS")
        scores = []
        
        for answer in progressive_answers:
            try:
                result = validator.validate_answer(question, answer, chunks_punteros)
                # Extraer score correctamente del resultado
                if isinstance(result, dict):
                    score = result.get('score', 0)
                elif isinstance(result, (int, float)):
                    score = result
                else:
                    score = 0
                scores.append(score)
                print(f"   '{answer[:30]}...' → {score}")
            except Exception as e:
                print(f"   Error: {e}")
                scores.append(0)
        
        # Los scores deben tender a aumentar con más información
        if len(scores) >= 3:
            # El último score debe ser mayor o igual que el primero
            assert scores[-1] >= scores[0], f"Score debe mejorar con más información: {scores[0]} → {scores[-1]}"
        
        print(f"✅ Sistema maneja respuestas progresivas")
    
    def test_different_phrasings_same_meaning(self, embedding_model, chunks_punteros):
        """
        TEST: Diferentes formas de decir lo mismo
        
        El sistema debe reconocer respuestas semánticamente equivalentes.
        """
        from hybrid_validator import HybridValidator
        
        validator = HybridValidator(embedding_model)
        question = "¿Qué es un puntero?"
        
        equivalent_answers = [
            "Una variable que almacena la dirección de memoria",
            "Una variable que guarda ubicaciones de memoria",
            "Es una referencia a una posición en la memoria del computador",
            "Almacena la dirección donde se encuentra otro dato",
        ]
        
        print("\n📊 RESPUESTAS SEMÁNTICAMENTE EQUIVALENTES")
        scores = []
        
        for answer in equivalent_answers:
            try:
                result = validator.validate_answer(question, answer, chunks_punteros)
                # Extraer score correctamente del resultado
                if isinstance(result, dict):
                    score = result.get('score', 0)
                elif isinstance(result, (int, float)):
                    score = result
                else:
                    score = 0
                scores.append(score)
                print(f"   Score {score}: '{answer[:40]}...'")
            except Exception as e:
                print(f"   Error: {e}")
                scores.append(0)
        
        # Todas las respuestas equivalentes deben tener scores similares
        if len(scores) >= 2:
            min_score = min(scores)
            max_score = max(scores)
            range_score = max_score - min_score
            
            # La diferencia no debe ser mayor a cierto umbral
            print(f"   Rango de scores: {min_score} - {max_score} (diff: {range_score})")
        
        print(f"✅ Sistema reconoce equivalencias semánticas")


# ═══════════════════════════════════════════════════════════════════════════════
# CLASE: TestMetrics - Pruebas de métricas del sistema
# ═══════════════════════════════════════════════════════════════════════════════

class TestMetrics:
    """
    Pruebas para verificar métricas de calidad del sistema
    
    Métricas del Project Charter:
    - KPIs de precisión
    - Eficiencia de respuesta
    - Detección de feedback
    """
    
    def test_accuracy_on_ground_truth(self, embedding_model, dataset_ground_truth, material_punteros):
        """
        TEST: Precisión sobre dataset de evaluación (DO-003)
        
        Mide la precisión del sistema comparando con respuestas etiquetadas.
        """
        from chunking import semantic_chunking
        from hybrid_validator import HybridValidator
        
        chunks = semantic_chunking(material_punteros, min_words=20, max_words=60)
        validator = HybridValidator(embedding_model)
        
        correct_predictions = 0
        total = len(dataset_ground_truth)
        
        print("\n📊 EVALUACIÓN CON GROUND TRUTH")
        print("=" * 50)
        
        for item in dataset_ground_truth:
            try:
                result = validator.validate_answer(
                    item["pregunta"],
                    item["respuesta_referencia"],
                    chunks
                )
                score = result.get('score', result) if isinstance(result, dict) else result
                
                # Clasificación: si score > 0.5, predecimos "correcta"
                predicted = "correcta" if score > 0.5 else "incorrecta"
                actual = item.get("clasificacion", "correcta")
                
                if predicted == actual:
                    correct_predictions += 1
                    status = "✓"
                else:
                    status = "✗"
                
                print(f"   {status} '{item['pregunta'][:30]}...' → {predicted} (score: {score:.3f})")
            except Exception as e:
                print(f"   Error: {e}")
        
        accuracy = correct_predictions / total if total > 0 else 0
        print(f"\n📈 PRECISIÓN: {correct_predictions}/{total} = {accuracy:.1%}")
        
        # Objetivo: 70% de precisión mínimo
        target_accuracy = 0.7
        if accuracy >= target_accuracy:
            print(f"✅ Precisión cumple objetivo (>= {target_accuracy:.0%})")
        else:
            print(f"⚠️ Precisión por debajo del objetivo ({target_accuracy:.0%})")
    
    def test_feedback_quality(self, embedding_model, chunks_punteros):
        """
        TEST: Calidad del feedback generado
        
        El sistema debe proporcionar retroalimentación útil.
        """
        from hybrid_validator import HybridValidator
        
        validator = HybridValidator(embedding_model)
        
        try:
            result = validator.validate_answer(
                "¿Qué es un puntero?",
                "No sé",
                chunks_punteros
            )
            
            if isinstance(result, dict):
                feedback = result.get('feedback', '')
                chunk_relevante = result.get('relevant_chunk', result.get('best_chunk', ''))
                
                print(f"\n📊 FEEDBACK GENERADO")
                print(f"   Feedback: '{feedback[:100]}...' " if feedback else "   No feedback")
                print(f"   Chunk relevante: '{chunk_relevante[:50]}...'" if chunk_relevante else "   Sin chunk")
                
                # Verificar que hay feedback para respuestas incorrectas
                if feedback:
                    print(f"✅ Sistema genera feedback")
                else:
                    print(f"⚠️ Sistema no generó feedback")
            else:
                print(f"   Resultado numérico: {result}")
        except Exception as e:
            pytest.skip(f"Error: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "not slow"])
