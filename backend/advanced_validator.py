"""
VALIDADOR SEMÁNTICO AVANZADO - RECUIVA
========================================

Sistema de validación multi-nivel que imita razonamiento humano:
- LITERAL: Coincidencia exacta de palabras clave
- INFERENCIAL: Detección de conceptos relacionados
- CRÍTICO: Evaluación de razonamiento profundo

MEJORAS vs semantic_validator.py:
✅ Filtrado inteligente de chunks por palabras clave
✅ Ranking de chunks por relevancia semántica
✅ Validación contra TOP 3 chunks (no solo el mejor)
✅ Justificación transparente de scores
✅ Detección de nivel de lectura (literal/inferencial/crítico)
✅ Compensación justa para reformulaciones inteligentes

Autor: Abel Jesús Moya Acosta
Fecha: 10 de noviembre de 2025
Proyecto: Recuiva - Active Recall con IA
"""

import numpy as np
from typing import List, Dict, Tuple, Optional, Set
from sklearn.metrics.pairwise import cosine_similarity
import re
from dataclasses import dataclass
from enum import Enum


class ReadingLevel(Enum):
    """Niveles de lectura según comprensión lectora"""
    LITERAL = "literal"          # Repite textualmente del material
    INFERENCIAL = "inferencial"  # Reformula con propias palabras
    CRITICO = "critico"          # Analiza, sintetiza, evalúa


@dataclass
class ValidationResult:
    """Resultado completo de validación con justificación"""
    score_final: int             # 0-100
    nivel: str                   # EXCELENTE, BUENO, ACEPTABLE, INSUFICIENTE
    reading_level: ReadingLevel  # literal, inferencial, critico
    es_correcto: bool            # True si >= 55%
    feedback: str                # Mensaje al estudiante
    color: str                   # Color UI (#hex)
    
    # Transparencia del scoring
    justificacion: str           # Por qué este score
    scoring_breakdown: Dict      # Desglose detallado
    best_chunk: Dict             # Chunk más relevante
    alternative_chunks: List[Dict]  # Chunks alternativos considerados
    
    # Debugging
    keywords_found: List[str]    # Palabras clave compartidas
    chunks_analyzed: int         # Total chunks analizados
    chunks_filtered: int         # Chunks relevantes tras filtrado


class AdvancedValidator:
    """
    Validador semántico con razonamiento multi-nivel
    """
    
    # Palabras de conexión/relleno (ignorar en análisis de keywords)
    STOPWORDS = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'de', 'del', 'al', 'por', 'para', 'con', 'sin', 'sobre',
        'en', 'entre', 'hacia', 'desde', 'hasta',
        'que', 'qué', 'cual', 'cuál', 'donde', 'dónde',
        'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
        'aquel', 'aquella', 'aquellos', 'aquellas',
        'es', 'son', 'está', 'están', 'fue', 'fueron',
        'como', 'muy', 'más', 'menos', 'tan', 'tanto'
    }
    
    def __init__(
        self,
        threshold_excellent: float = 0.75,   # 75% (antes 85%)
        threshold_good: float = 0.60,        # 60% (antes 70%)
        threshold_acceptable: float = 0.45,  # 45% (antes 55%)
        min_response_length: int = 15,
        keyword_weight: float = 0.20,        # 20% peso keywords (antes 15%)
        context_weight: float = 0.15,        # 15% peso contexto (antes 10%)
        reasoning_weight: float = 0.20       # 20% peso razonamiento (antes 15%)
    ):
        """
        Inicializa validador avanzado
        
        UMBRALES AJUSTADOS PARA ACTIVE RECALL:
        - Active Recall NO requiere coincidencia literal
        - Se premia la comprensión conceptual y parafraseo
        - Umbrales más realistas para respuestas con propias palabras
        
        Args:
            threshold_excellent: Umbral EXCELENTE (default: 75%, antes 85%)
            threshold_good: Umbral BUENO (default: 60%, antes 70%)
            threshold_acceptable: Umbral ACEPTABLE (default: 45%, antes 55%)
            min_response_length: Mínimo caracteres de respuesta
            keyword_weight: Peso de bonificación por keywords (20%)
            context_weight: Peso de bonificación por contexto (15%)
            reasoning_weight: Peso de bonificación por razonamiento (20%)
        """
        self.thresholds = {
            'EXCELENTE': threshold_excellent,
            'BUENO': threshold_good,
            'ACEPTABLE': threshold_acceptable,
            'INSUFICIENTE': 0.0
        }
        self.min_response_length = min_response_length
        self.weights = {
            'keyword': keyword_weight,
            'context': context_weight,
            'reasoning': reasoning_weight
        }
    
    def extract_keywords(self, text: str, min_length: int = 4) -> Set[str]:
        """
        Extrae palabras clave significativas (sin stopwords)
        
        Args:
            text: Texto a procesar
            min_length: Longitud mínima de palabra
            
        Returns:
            Set de keywords normalizadas (lowercase)
        """
        # Extraer palabras alfanuméricas
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filtrar stopwords y palabras cortas
        keywords = {
            w for w in words 
            if len(w) >= min_length and w not in self.STOPWORDS
        }
        
        return keywords
    
    def filter_chunks_by_keywords(
        self,
        question_text: str,
        user_answer: str,
        chunks: List[Dict]
    ) -> List[Dict]:
        """
        Filtra chunks relevantes basándose en palabras clave
        
        ESTRATEGIA:
        1. Extrae keywords de pregunta + respuesta
        2. Calcula overlap de keywords con cada chunk
        3. Rankea chunks por relevancia léxica
        4. Retorna top chunks + todos con >50% overlap
        
        Args:
            question_text: Texto de la pregunta
            user_answer: Respuesta del usuario
            chunks: Todos los chunks del material
            
        Returns:
            Lista de chunks filtrados y rankeados
        """
        # Keywords de pregunta y respuesta
        query_keywords = self.extract_keywords(question_text + " " + user_answer)
        
        if not query_keywords:
            # Si no hay keywords, retornar todos los chunks
            return chunks
        
        # Rankear chunks por overlap de keywords
        ranked_chunks = []
        
        for chunk in chunks:
            chunk_text = chunk.get('text_full', chunk.get('text', ''))
            chunk_keywords = self.extract_keywords(chunk_text)
            
            # Calcular overlap (Jaccard similarity)
            if chunk_keywords:
                shared = query_keywords.intersection(chunk_keywords)
                overlap_ratio = len(shared) / len(query_keywords)
            else:
                overlap_ratio = 0.0
            
            ranked_chunks.append({
                **chunk,
                'keyword_overlap': overlap_ratio,
                'shared_keywords': shared if overlap_ratio > 0 else set()
            })
        
        # Ordenar por overlap descendente
        ranked_chunks.sort(key=lambda x: x['keyword_overlap'], reverse=True)
        
        # Filtrar: Top 10 O todos con >30% overlap
        threshold_overlap = 0.30
        filtered = [
            c for c in ranked_chunks[:10]
            if c['keyword_overlap'] >= threshold_overlap or ranked_chunks.index(c) < 5
        ]
        
        # Si tras filtrado quedan <3 chunks, retornar top 10 sin filtro
        if len(filtered) < 3:
            return ranked_chunks[:10]
        
        return filtered
    
    def validate_answer_advanced(
        self,
        user_embedding: np.ndarray,
        material_chunks: List[Dict],
        user_answer: str,
        question_text: str
    ) -> ValidationResult:
        """
        Validación avanzada con razonamiento multi-nivel
        
        PROCESO:
        1. Filtrado léxico por keywords (reduce noise)
        2. Ranking semántico (coseno similitud)
        3. Validación contra TOP 3 chunks
        4. Scoring multi-nivel (literal, inferencial, crítico)
        5. Justificación transparente
        
        Args:
            user_embedding: Embedding de respuesta (384 dims)
            material_chunks: Todos los chunks con embeddings
            user_answer: Texto de la respuesta
            question_text: Texto de la pregunta
            
        Returns:
            ValidationResult con scoring completo y justificación
        """
        # === PASO 1: VALIDACIÓN BÁSICA ===
        if len(user_answer.strip()) < self.min_response_length:
            return self._create_error_result(
                f"Respuesta muy corta (mínimo {self.min_response_length} caracteres)"
            )
        
        # === PASO 2: FILTRADO INTELIGENTE DE CHUNKS ===
        filtered_chunks = self.filter_chunks_by_keywords(
            question_text=question_text,
            user_answer=user_answer,
            chunks=material_chunks
        )
        
        if not filtered_chunks:
            filtered_chunks = material_chunks[:10]  # Fallback
        
        # === PASO 3: CÁLCULO DE SIMILITUDES SEMÁNTICAS ===
        similarities = []
        
        for chunk in filtered_chunks:
            chunk_embedding = np.array(chunk['embedding'])
            chunk_text = chunk.get('text_full', chunk.get('text', ''))
            
            # Similitud del coseno
            sim = cosine_similarity(
                user_embedding.reshape(1, -1),
                chunk_embedding.reshape(1, -1)
            )[0][0]
            
            similarities.append({
                'chunk_id': chunk.get('chunk_id', 0),
                'text': chunk_text,
                'text_short': chunk_text[:200] + '...' if len(chunk_text) > 200 else chunk_text,
                'similarity': float(sim),
                'keyword_overlap': chunk.get('keyword_overlap', 0.0),
                'shared_keywords': list(chunk.get('shared_keywords', set()))
            })
        
        # Ordenar por similitud descendente
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        
        # === PASO 4: SCORING MULTI-NIVEL ===
        top_3_chunks = similarities[:3]
        best_chunk = top_3_chunks[0]
        
        # Base: Similitud semántica (60-70% del score)
        base_sim = best_chunk['similarity']
        base_score = base_sim * 100
        
        # NIVEL 1: LITERAL (Coincidencia de keywords)
        answer_keywords = self.extract_keywords(user_answer)
        chunk_keywords = self.extract_keywords(best_chunk['text'])
        shared_keywords = answer_keywords.intersection(chunk_keywords)
        
        keyword_ratio = len(shared_keywords) / len(answer_keywords) if answer_keywords else 0
        keyword_bonus = keyword_ratio * 100 * self.weights['keyword']  # Máx 20 puntos
        
        # NIVEL 2: INFERENCIAL (Múltiples chunks relevantes)
        high_sim_chunks = [c for c in top_3_chunks if c['similarity'] > 0.50]
        context_bonus = len(high_sim_chunks) * 3.33 * self.weights['context']  # Máx 15 puntos
        
        # NIVEL 3: CRÍTICO (Razonamiento profundo y parafraseo)
        # MEJORA: Premiar parafraseo inteligente
        reasoning_bonus = 0
        
        # Caso 1: Similitud media-alta (35-75%) + keywords relevantes = PARAFRASEO BUENO
        if 0.35 <= base_sim < 0.75:
            if keyword_ratio > 0.40 and len(user_answer) > 60:
                reasoning_bonus = 20 * self.weights['reasoning']  # Máx 20 puntos
        
        # Caso 2: Similitud media-baja (30-40%) pero muchas keywords = COMPRENSIÓN REAL
        elif 0.30 <= base_sim < 0.40:
            if keyword_ratio > 0.60 and len(user_answer) > 100:
                reasoning_bonus = 15 * self.weights['reasoning']
        
        # Bonus adicional: Respuestas muy elaboradas (>100 chars)
        if len(user_answer) > 100:
            reasoning_bonus += 5 * self.weights['reasoning']
        
        # Score final (máximo 100)
        final_score = min(int(base_score + keyword_bonus + context_bonus + reasoning_bonus), 100)
        
        # === PASO 5: CLASIFICACIÓN Y NIVEL DE LECTURA ===
        if final_score >= self.thresholds['EXCELENTE'] * 100:
            nivel = 'EXCELENTE'
            color = '#10b981'
        elif final_score >= self.thresholds['BUENO'] * 100:
            nivel = 'BUENO'
            color = '#3b82f6'
        elif final_score >= self.thresholds['ACEPTABLE'] * 100:
            nivel = 'ACEPTABLE'
            color = '#f59e0b'
        else:
            nivel = 'INSUFICIENTE'
            color = '#ef4444'
        
        # Determinar nivel de lectura
        if keyword_ratio > 0.80 and base_sim > 0.85:
            reading_level = ReadingLevel.LITERAL
        elif 0.40 <= base_sim < 0.85 and keyword_ratio > 0.40:
            reading_level = ReadingLevel.INFERENCIAL
        elif reasoning_bonus > 0:
            reading_level = ReadingLevel.CRITICO
        else:
            reading_level = ReadingLevel.LITERAL
        
        # === PASO 6: JUSTIFICACIÓN TRANSPARENTE ===
        justification = self._generate_justification(
            base_score=base_score,
            keyword_bonus=keyword_bonus,
            context_bonus=context_bonus,
            reasoning_bonus=reasoning_bonus,
            shared_keywords=shared_keywords,
            reading_level=reading_level,
            high_sim_chunks=len(high_sim_chunks)
        )
        
        # Feedback al estudiante
        feedback = self._generate_feedback(
            nivel=nivel,
            score=final_score,
            reading_level=reading_level,
            shared_keywords=shared_keywords
        )
        
        # === PASO 7: RESULTADO COMPLETO ===
        return ValidationResult(
            score_final=final_score,
            nivel=nivel,
            reading_level=reading_level,
            es_correcto=final_score >= self.thresholds['ACEPTABLE'] * 100,
            feedback=feedback,
            color=color,
            justificacion=justification,
            scoring_breakdown={
                'base_similarity': round(base_score, 2),
                'keyword_bonus': round(keyword_bonus, 2),
                'context_bonus': round(context_bonus, 2),
                'reasoning_bonus': round(reasoning_bonus, 2),
                'final_score': final_score
            },
            best_chunk={
                'chunk_id': best_chunk['chunk_id'],
                'text_preview': best_chunk['text_short'],
                'similarity': round(best_chunk['similarity'] * 100, 1),
                'keyword_overlap': round(best_chunk.get('keyword_overlap', 0) * 100, 1)
            },
            alternative_chunks=[
                {
                    'chunk_id': c['chunk_id'],
                    'similarity': round(c['similarity'] * 100, 1),
                    'text_preview': c['text_short'][:100]
                }
                for c in top_3_chunks[1:3]
            ],
            keywords_found=list(shared_keywords),
            chunks_analyzed=len(material_chunks),
            chunks_filtered=len(filtered_chunks)
        )
    
    def _generate_justification(
        self,
        base_score: float,
        keyword_bonus: float,
        context_bonus: float,
        reasoning_bonus: float,
        shared_keywords: Set[str],
        reading_level: ReadingLevel,
        high_sim_chunks: int
    ) -> str:
        """
        Genera justificación transparente del scoring
        
        Returns:
            Explicación detallada en español
        """
        parts = []
        
        # Base semántica
        parts.append(f"**Similitud semántica base**: {base_score:.1f}% (coseno de embeddings)")
        
        # Keywords
        if keyword_bonus > 0:
            keywords_str = ", ".join(list(shared_keywords)[:5])
            if len(shared_keywords) > 5:
                keywords_str += f" (+{len(shared_keywords) - 5} más)"
            parts.append(
                f"**+ Bonus por keywords**: +{keyword_bonus:.1f}% "
                f"({len(shared_keywords)} palabras clave compartidas: {keywords_str})"
            )
        
        # Contexto
        if context_bonus > 0:
            parts.append(
                f"**+ Bonus por contexto**: +{context_bonus:.1f}% "
                f"({high_sim_chunks} chunks relevantes encontrados)"
            )
        
        # Razonamiento
        if reasoning_bonus > 0:
            parts.append(
                f"**+ Bonus por razonamiento**: +{reasoning_bonus:.1f}% "
                f"(reformulación inteligente detectada)"
            )
        
        # Nivel de lectura
        nivel_desc = {
            ReadingLevel.LITERAL: "Lectura **literal** (repite del material)",
            ReadingLevel.INFERENCIAL: "Lectura **inferencial** (reformula con propias palabras)",
            ReadingLevel.CRITICO: "Lectura **crítica** (analiza y sintetiza)"
        }
        parts.append(f"\n**Nivel de comprensión**: {nivel_desc[reading_level]}")
        
        return "\n".join(parts)
    
    def _generate_feedback(
        self,
        nivel: str,
        score: int,
        reading_level: ReadingLevel,
        shared_keywords: Set[str]
    ) -> str:
        """Genera feedback personalizado según nivel y comprensión"""
        
        if nivel == 'EXCELENTE':
            return f"""🎉 **¡EXCELENTE!** Comprensión profunda del concepto.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

✅ Tu explicación captura la esencia del material. {"Has reformulado inteligentemente el concepto." if reading_level == ReadingLevel.INFERENCIAL else "Dominas el tema completamente."}

💡 **Sigue así** con Active Recall. Estás en el camino correcto."""
        
        elif nivel == 'BUENO':
            return f"""✅ **¡MUY BIEN!** Buen entendimiento del tema.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

👍 Has captado los conceptos principales. {f"Encontraste {len(shared_keywords)} palabras clave correctas." if shared_keywords else ""}

💭 **Tip**: Podrías profundizar un poco más, pero vas muy bien."""
        
        elif nivel == 'ACEPTABLE':
            return f"""⚠️ **RESPUESTA PARCIAL**. Tienes la idea, pero falta desarrollo.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

🔍 Tu respuesta toca puntos correctos, pero necesita más precisión o detalle.

📖 **Sugerencia**: Revisa el fragmento y explica con más profundidad. Recuerda: **ENTENDER > Memorizar**."""
        
        else:  # INSUFICIENTE
            return f"""❌ **NECESITA MEJORAR**. La respuesta no refleja bien el material.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

🔄 **Intenta de nuevo**:
1. Relee el fragmento relevante
2. Cierra el material
3. Explica **CON TUS PROPIAS PALABRAS**
4. Enfócate en **ENTENDER**, no memorizar

💡 **Tip**: Imagina que se lo explicas a un amigo."""
    
    def _create_error_result(self, error_message: str) -> ValidationResult:
        """Crea resultado de error para respuestas inválidas"""
        return ValidationResult(
            score_final=0,
            nivel='INSUFICIENTE',
            reading_level=ReadingLevel.LITERAL,
            es_correcto=False,
            feedback=f"❌ {error_message}",
            color='#ef4444',
            justificacion=error_message,
            scoring_breakdown={},
            best_chunk={},
            alternative_chunks=[],
            keywords_found=[],
            chunks_analyzed=0,
            chunks_filtered=0
        )


# ===== FUNCIÓN DE INTEGRACIÓN CON ENDPOINT EXISTENTE =====

def validate_with_advanced_system(
    user_embedding: np.ndarray,
    material_chunks: List[Dict],
    user_answer: str,
    question_text: str,
    use_advanced: bool = True
) -> Dict:
    """
    Wrapper para integración con backend/main.py
    
    COMPATIBILIDAD:
    - Si use_advanced=True, usa AdvancedValidator (RECOMENDADO)
    - Si use_advanced=False, usa SemanticValidator antiguo
    
    Args:
        user_embedding: Embedding de respuesta
        material_chunks: Chunks con embeddings
        user_answer: Texto de respuesta
        question_text: Texto de pregunta
        use_advanced: True para sistema nuevo
        
    Returns:
        Dict compatible con formato esperado por frontend
    """
    if use_advanced:
        validator = AdvancedValidator()
        result = validator.validate_answer_advanced(
            user_embedding=user_embedding,
            material_chunks=material_chunks,
            user_answer=user_answer,
            question_text=question_text
        )
        
        # Convertir a formato legacy
        return {
            'nivel': result.nivel,
            'score_porcentaje': result.score_final,
            'score_raw': result.score_final,
            'feedback': result.feedback,
            'color': result.color,
            'es_correcto': result.es_correcto,
            # NUEVO: Transparencia
            'justificacion': result.justificacion,
            'reading_level': result.reading_level.value,
            'scoring_details': result.scoring_breakdown,
            'best_chunk_id': result.best_chunk.get('chunk_id'),
            'alternative_chunks': result.alternative_chunks,
            'keywords_found': result.keywords_found
        }
    
    else:
        # Fallback a sistema antiguo
        from semantic_validator import SemanticValidator
        old_validator = SemanticValidator()
        classification, top_chunks, best = old_validator.validate_answer(
            user_embedding=user_embedding,
            material_chunks=material_chunks,
            user_answer=user_answer,
            question_text=question_text
        )
        return classification


# ===== EJEMPLO DE USO =====

if __name__ == "__main__":
    print("="*80)
    print("🧠 ADVANCED VALIDATOR - Sistema Multi-Nivel")
    print("="*80)
    
    validator = AdvancedValidator()
    
    print("\n✅ Características:")
    print("   - Filtrado por keywords antes de validación")
    print("   - Ranking de chunks por relevancia")
    print("   - Validación contra TOP 3 chunks")
    print("   - Scoring multi-nivel (literal, inferencial, crítico)")
    print("   - Justificación transparente")
    print("   - Compensación justa para reformulaciones")
    
    print("\n📊 Pesos configurados:")
    print(f"   - Keywords: {validator.weights['keyword']*100}%")
    print(f"   - Contexto: {validator.weights['context']*100}%")
    print(f"   - Razonamiento: {validator.weights['reasoning']*100}%")
    
    print("\n🎯 Umbrales:")
    for nivel, threshold in validator.thresholds.items():
        print(f"   - {nivel}: ≥{threshold*100}%")
    
    print("="*80)
