"""
VALIDADOR SEM├üNTICO AVANZADO - RECUIVA
========================================

Sistema de validaci├│n multi-nivel que imita razonamiento humano:
- LITERAL: Coincidencia exacta de palabras clave
- INFERENCIAL: Detecci├│n de conceptos relacionados
- CR├ìTICO: Evaluaci├│n de razonamiento profundo

MEJORAS vs semantic_validator.py:
Ô£à Filtrado inteligente de chunks por palabras clave
Ô£à Ranking de chunks por relevancia sem├íntica
Ô£à Validaci├│n contra TOP 3 chunks (no solo el mejor)
Ô£à Justificaci├│n transparente de scores
Ô£à Detecci├│n de nivel de lectura (literal/inferencial/cr├¡tico)
Ô£à Compensaci├│n justa para reformulaciones inteligentes

Autor: Abel Jes├║s Moya Acosta
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
    """Niveles de lectura seg├║n comprensi├│n lectora"""
    LITERAL = "literal"          # Repite textualmente del material
    INFERENCIAL = "inferencial"  # Reformula con propias palabras
    CRITICO = "critico"          # Analiza, sintetiza, eval├║a


@dataclass
class ValidationResult:
    """Resultado completo de validaci├│n con justificaci├│n"""
    score_final: int             # 0-100
    nivel: str                   # EXCELENTE, BUENO, ACEPTABLE, INSUFICIENTE
    reading_level: ReadingLevel  # literal, inferencial, critico
    es_correcto: bool            # True si >= 55%
    feedback: str                # Mensaje al estudiante
    color: str                   # Color UI (#hex)
    
    # Transparencia del scoring
    justificacion: str           # Por qu├® este score
    scoring_breakdown: Dict      # Desglose detallado
    best_chunk: Dict             # Chunk m├ís relevante
    alternative_chunks: List[Dict]  # Chunks alternativos considerados
    
    # Debugging
    keywords_found: List[str]    # Palabras clave compartidas
    chunks_analyzed: int         # Total chunks analizados
    chunks_filtered: int         # Chunks relevantes tras filtrado


class AdvancedValidator:
    """
    Validador sem├íntico con razonamiento multi-nivel
    """
    
    # Palabras de conexi├│n/relleno (ignorar en an├ílisis de keywords)
    STOPWORDS = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'de', 'del', 'al', 'por', 'para', 'con', 'sin', 'sobre',
        'en', 'entre', 'hacia', 'desde', 'hasta',
        'que', 'qu├®', 'cual', 'cu├íl', 'donde', 'd├│nde',
        'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
        'aquel', 'aquella', 'aquellos', 'aquellas',
        'es', 'son', 'est├í', 'est├ín', 'fue', 'fueron',
        'como', 'muy', 'm├ís', 'menos', 'tan', 'tanto'
    }
    
    def __init__(
        self,
        threshold_excellent: float = 0.85,
        threshold_good: float = 0.70,
        threshold_acceptable: float = 0.55,
        min_response_length: int = 15,
        keyword_weight: float = 0.15,      # 15% peso para keywords
        context_weight: float = 0.10,      # 10% peso para contexto
        reasoning_weight: float = 0.15     # 15% peso para razonamiento
    ):
        """
        Inicializa validador avanzado
        
        Args:
            threshold_excellent: Umbral EXCELENTE (default: 85%)
            threshold_good: Umbral BUENO (default: 70%)
            threshold_acceptable: Umbral ACEPTABLE (default: 55%)
            min_response_length: M├¡nimo caracteres de respuesta
            keyword_weight: Peso de bonificaci├│n por keywords (0-1)
            context_weight: Peso de bonificaci├│n por contexto (0-1)
            reasoning_weight: Peso de bonificaci├│n por razonamiento (0-1)
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
        Extrae palabras clave significativas + stems + nombres propios
        
        🔥 MEJORA (17 nov 2025): Detecta variaciones morfológicas:
        - "sospecha" / "sospechan" / "sospechaba" → stem "sospe"
        - "Henriette" → nombre propio completo
        
        Args:
            text: Texto a procesar
            min_length: Longitud mínima de palabra
            
        Returns:
            Set[str]: Keywords + stems (5-6 chars) + nombres propios
        """
        # Extraer palabras alfanuméricas (conservar mayúsculas para nombres propios)
        words_original = re.findall(r'\b\w+\b', text)
        words_lower = [w.lower() for w in words_original]
        
        # Filtrar stopwords y palabras cortas
        keywords = {
            w for w in words_lower 
            if len(w) >= min_length and w not in self.STOPWORDS
        }
        
        # STEMS para variaciones: "sospecha"/"sospechan"/"sospechaba" → "sospe"
        stems = {
            w[:6] if len(w) > 6 else w[:5] 
            for w in keywords 
            if len(w) >= 6
        }
        
        # Nombres propios (capitalizados): Henriette, Condesa, Maurice
        proper_nouns = {
            w.lower() for w in words_original 
            if len(w) >= 4 and w[0].isupper() and w.lower() not in self.STOPWORDS
        }
        
        return keywords.union(stems).union(proper_nouns)
    
    def filter_chunks_by_keywords(
        self,
        question_text: str,
        user_answer: str,
        chunks: List[Dict]
    ) -> List[Dict]:
        """
        Filtra chunks relevantes basándose en palabras clave (PRE-FILTRADO AGRESIVO)
        
        ✅ MEJORA (17 nov 2025): Threshold aumentado a 40% para reducir noise
        
        ESTRATEGIA:
        1. Extrae keywords de pregunta + respuesta
        2. Calcula overlap de keywords con cada chunk
        3. Rankea chunks por relevancia léxica
        4. Retorna solo chunks con ≥40% overlap O top 15
        
        Args:
            question_text: Texto de la pregunta
            user_answer: Respuesta del usuario
            chunks: Todos los chunks del material
            
        Returns:
            Lista de chunks filtrados y rankeados (reducido de 150+ a ~10-20)
        """
        # Keywords de pregunta y respuesta
        query_keywords = self.extract_keywords(question_text + " " + user_answer)
        
        if not query_keywords:
            # Si no hay keywords, retornar top 20 chunks (fallback)
            return chunks[:20]
        
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
        
        # 🔥 ESTRATEGIA HÍBRIDA: Filtro suave (25%) + Top 30 por keywords
        # Permite que búsqueda semántica posterior refine
        threshold_overlap = 0.25  # Reducido 40% → 25% (más permisivo)
        
        # Opción A: Filtrar por threshold O top 30 por keyword overlap
        filtered_by_threshold = [
            c for c in ranked_chunks
            if c['keyword_overlap'] >= threshold_overlap
        ]
        
        # Opción B: Si muy pocos, tomar top 30 aunque no lleguen al 25%
        TOP_N_KEYWORDS = 30
        if len(filtered_by_threshold) < 10:
            filtered = ranked_chunks[:TOP_N_KEYWORDS]
            print(f"⚠️ Pocos chunks con ≥{threshold_overlap*100:.0f}%, usando top {TOP_N_KEYWORDS}")
        else:
            filtered = filtered_by_threshold
        
        print(f"\n📊 Keywords extraídos: {query_keywords}")
        print(f"✂️ Filtrado por keywords: {len(filtered)}/{len(chunks)} chunks (threshold: ≥{threshold_overlap*100:.0f}% o top {TOP_N_KEYWORDS})")
        
        # Mostrar top 5 chunks con mayor overlap
        print(f"\n🔝 Top 5 chunks por keyword overlap:")
        for i, chunk in enumerate(ranked_chunks[:5], 1):
            overlap_pct = chunk['keyword_overlap'] * 100
            shared_kw = list(chunk['shared_keywords'])[:3]  # Primeras 3 keywords
            chunk_preview = chunk.get('text_full', chunk.get('text', ''))[:60]
            print(f"   {i}. Chunk #{chunk.get('chunk_id', '?')} → {overlap_pct:.1f}% overlap → KW: {shared_kw} → '{chunk_preview}...'")
        
        # Si quedan muy pocos (<10), expandir a top 15
        if len(filtered) < 10:
            filtered = ranked_chunks[:15]
            print(f"⚠️ Pocos matches con 40%+ overlap, expandido a top 15 chunks")
        
        
        # Si aún quedan muy pocos (<5), usar top 20 como fallback
        if len(filtered) < 5:
            return ranked_chunks[:20]
        
        return filtered
    
    def detect_ambiguity(self, top_chunks: List[Dict], threshold: float = 0.08) -> Dict:
        """
        Detecta si hay múltiples chunks con score similar (ambigüedad semántica)
        
        ✅ NUEVO (17 nov 2025): Advierte cuando hay múltiples fragmentos igualmente relevantes
        
        Args:
            top_chunks: Lista de chunks rankeados por similitud
            threshold: Diferencia máxima para considerar chunks "similares" (default: 8%)
            
        Returns:
            dict: {
                'is_ambiguous': bool,          # True si hay ≥2 chunks con similitud parecida
                'similar_chunks_count': int,   # Cantidad de chunks similares
                'confidence': float,            # 0-1, baja si hay ambigüedad
                'warning': str | None           # Mensaje de advertencia
            }
            
        Ejemplo:
            >>> # Chunks: [0.85, 0.83, 0.55] → Ambiguo (0.85-0.83 = 0.02 < 0.08)
            >>> detect_ambiguity(chunks)
            {'is_ambiguous': True, 'similar_chunks_count': 2, 'confidence': 0.7}
        """
        if len(top_chunks) < 2:
            return {
                'is_ambiguous': False,
                'similar_chunks_count': 1,
                'confidence': 1.0,
                'warning': None
            }
        
        best_sim = top_chunks[0]['similarity']
        similar_count = 1
        
        # Contar chunks con similitud cercana al mejor
        for chunk in top_chunks[1:]:
            if abs(chunk['similarity'] - best_sim) < threshold:
                similar_count += 1
        
        is_ambiguous = similar_count >= 2
        
        # Calcular confianza (menor si hay ambigüedad)
        confidence = 1.0 if not is_ambiguous else 0.75
        
        # Generar warning si es ambiguo
        warning = None
        if is_ambiguous:
            warning = (
                f"⚠️ Se encontraron {similar_count} fragmentos con similitud parecida. "
                f"Tu respuesta podría relacionarse con múltiples secciones del material. "
                f"Considera revisar varios fragmentos para validar tu comprensión."
            )
        
        return {
            'is_ambiguous': is_ambiguous,
            'similar_chunks_count': similar_count,
            'confidence': confidence,
            'warning': warning
        }
    
    def validate_answer_advanced(
        self,
        user_embedding: np.ndarray,
        material_chunks: List[Dict],
        user_answer: str,
        question_text: str
    ) -> ValidationResult:
        """
        Validaci├│n avanzada con razonamiento multi-nivel
        
        PROCESO:
        1. Filtrado l├®xico por keywords (reduce noise)
        2. Ranking sem├íntico (coseno similitud)
        3. Validaci├│n contra TOP 3 chunks
        4. Scoring multi-nivel (literal, inferencial, cr├¡tico)
        5. Justificaci├│n transparente
        
        Args:
            user_embedding: Embedding de respuesta (384 dims)
            material_chunks: Todos los chunks con embeddings
            user_answer: Texto de la respuesta
            question_text: Texto de la pregunta
            
        Returns:
            ValidationResult con scoring completo y justificaci├│n
        """
        # === PASO 1: VALIDACI├ôN B├üSICA ===
        if len(user_answer.strip()) < self.min_response_length:
            return self._create_error_result(
                f"Respuesta muy corta (m├¡nimo {self.min_response_length} caracteres)"
            )
        
        # === PASO 2: FILTRADO INTELIGENTE DE CHUNKS ===
        filtered_chunks = self.filter_chunks_by_keywords(
            question_text=question_text,
            user_answer=user_answer,
            chunks=material_chunks
        )
        
        print(f"🔍 PRE-FILTRADO: {len(material_chunks)} chunks → {len(filtered_chunks)} relevantes (40% keywords)")
        
        if not filtered_chunks:
            filtered_chunks = material_chunks[:10]  # Fallback
        
        # === PASO 3: C├üLCULO DE SIMILITUDES SEM├üNTICAS ===
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
        
        # Mostrar TOP 3 chunks con mayor similitud semántica (después del filtrado)
        print(f"\n🎯 Top 3 chunks con mayor SIMILITUD SEMÁNTICA (Cosine Similarity):")
        for i, chunk in enumerate(similarities[:3], 1):
            sim_pct = chunk['similarity'] * 100
            chunk_preview = chunk['text_short'][:70]
            kw_overlap = chunk.get('keyword_overlap', 0) * 100
            print(f"   {i}. Chunk #{chunk['chunk_id']} → Similitud: {sim_pct:.1f}% | KW overlap: {kw_overlap:.0f}% → '{chunk_preview}...'")
        
        # === PASO 4: VALIDACIÓN DE RELEVANCIA SEMÁNTICA ===
        top_3_chunks = similarities[:3]
        best_chunk = top_3_chunks[0]
        
        # ✅ Threshold de rechazo: 50% según ALGORITMO_VALIDACION_SEMANTICA.md
        # "ACEPTABLE: ≥50%" - Cohen (1988): correlaciones >0.5 = moderadas a fuertes
        if best_chunk['similarity'] < 0.50:
            return ValidationResult(
                score_final=0,
                nivel='INSUFICIENTE',
                reading_level=ReadingLevel.LITERAL,
                es_correcto=False,
                feedback=f"❌ Tu respuesta NO tiene relación coherente con el material.\n\n"
                        f"📊 Similitud del fragmento más cercano: **{best_chunk['similarity']*100:.1f}%**\n"
                        f"📏 Mínimo requerido: **50%** (según Cohen, 1988)\n\n"
                        f"💡 **Recomendación**: Revisa el material y responde con información más relacionada al contenido.",
                color='#ef4444',
                justificacion=f"Rechazado automáticamente: similitud semántica insuficiente ({best_chunk['similarity']*100:.1f}% < 50%). "
                             f"Según Cohen (1988), correlaciones <0.5 son débiles. La respuesta no guarda coherencia con el material.",
                scoring_breakdown={
                    'base_similarity': round(best_chunk['similarity'] * 100, 2),
                    'keyword_bonus': 0,
                    'context_bonus': 0,
                    'reasoning_bonus': 0,
                    'final_score': 0,
                    'rejection_reason': 'similitud_insuficiente'
                },
                best_chunk={
                    'chunk_id': best_chunk['chunk_id'],
                    'text_preview': best_chunk['text_short'][:150],
                    'similarity': round(best_chunk['similarity'] * 100, 1),
                    'keyword_overlap': round(best_chunk.get('keyword_overlap', 0) * 100, 1)
                },
                alternative_chunks=[],
                keywords_found=[],
                chunks_analyzed=len(material_chunks),
                chunks_filtered=len(filtered_chunks)
            )
        
        # Base: Similitud semántica (60-70% del score)
        base_sim = best_chunk['similarity']
        base_score = base_sim * 100
        
        # NIVEL 1: LITERAL (Coincidencia de keywords)
        answer_keywords = self.extract_keywords(user_answer)
        chunk_keywords = self.extract_keywords(best_chunk['text'])
        shared_keywords = answer_keywords.intersection(chunk_keywords)
        
        keyword_ratio = len(shared_keywords) / len(answer_keywords) if answer_keywords else 0
        keyword_bonus = keyword_ratio * 20  # Máx 20 puntos (antes * 100)
        
        # NIVEL 2: INFERENCIAL (Múltiples chunks relevantes)
        # 🔥 Threshold 0.40: más permisivo
        high_sim_chunks = [c for c in top_3_chunks if c['similarity'] > 0.40]
        context_bonus = len(high_sim_chunks) * 5  # Máx 15 puntos (5 por chunk)
        
        # NIVEL 3: CRÍTICO (Razonamiento profundo)
        # Detectar reformulación inteligente:
        # - Similitud media (55-75%)
        # - Alto overlap de keywords (>60%)
        # - Respuesta elaborada (>100 chars)
        reasoning_bonus = 0
        
        # ✅ BONUS para reformulaciones inteligentes (zona 40-70%)
        # Recompensa cuando keywords + longitud compensan similitud moderada
        if 0.40 <= base_sim < 0.70:
            if keyword_ratio > 0.50 and len(user_answer) > 80:
                reasoning_bonus = 15  # Máx 15 puntos
        
        # ✅ PENALIZACIÓN SOLO para similitud MUY baja (<40%)
        similarity_penalty = 0
        if base_sim < 0.40:
            similarity_penalty = (0.40 - base_sim) * 50  # Penalización hasta -20 puntos
            print(f"⚠️ Penalización por similitud baja ({base_sim*100:.1f}%): -{similarity_penalty:.1f} puntos")
        
        # Score final con penalización
        final_score = min(int(base_score + keyword_bonus + context_bonus + reasoning_bonus - similarity_penalty), 100)
        final_score = max(final_score, 0)  # No permitir scores negativos
        
        # === PASO 5: CLASIFICACI├ôN Y NIVEL DE LECTURA ===
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
        
        # ✅ NUEVO: Detectar ambigüedad semántica
        ambiguity_info = self.detect_ambiguity(top_3_chunks)
        
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
        
        # ✅ MEJORADO: Feedback con warning de ambigüedad
        feedback = self._generate_feedback(
            nivel=nivel,
            score=final_score,
            reading_level=reading_level,
            shared_keywords=shared_keywords,
            ambiguity_warning=ambiguity_info.get('warning')  # ✅ NUEVO
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
                'final_score': final_score,
                # ✅ NUEVO: Info de ambigüedad
                'is_ambiguous': ambiguity_info['is_ambiguous'],
                'confidence': ambiguity_info['confidence'],
                'similar_chunks_count': ambiguity_info['similar_chunks_count']
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
        Genera justificaci├│n transparente del scoring
        
        Returns:
            Explicaci├│n detallada en espa├▒ol
        """
        parts = []
        
        # Base sem├íntica
        parts.append(f"**Similitud sem├íntica base**: {base_score:.1f}% (coseno de embeddings)")
        
        # Keywords
        if keyword_bonus > 0:
            keywords_str = ", ".join(list(shared_keywords)[:5])
            if len(shared_keywords) > 5:
                keywords_str += f" (+{len(shared_keywords) - 5} m├ís)"
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
                f"(reformulaci├│n inteligente detectada)"
            )
        
        # Nivel de lectura
        nivel_desc = {
            ReadingLevel.LITERAL: "Lectura **literal** (repite del material)",
            ReadingLevel.INFERENCIAL: "Lectura **inferencial** (reformula con propias palabras)",
            ReadingLevel.CRITICO: "Lectura **cr├¡tica** (analiza y sintetiza)"
        }
        parts.append(f"\n**Nivel de comprensi├│n**: {nivel_desc[reading_level]}")
        
        return "\n".join(parts)
    
    def _generate_feedback(
        self,
        nivel: str,
        score: int,
        reading_level: ReadingLevel,
        shared_keywords: Set[str],
        ambiguity_warning: Optional[str] = None  # ✅ NUEVO parámetro
    ) -> str:
        """Genera feedback personalizado según nivel y comprensión"""
        
        # Base del feedback según nivel
        if nivel == 'EXCELENTE':
            feedback = f"""🎖️ **¡EXCELENTE!** Comprensión profunda del concepto.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

✅ Tu explicación captura la esencia del material. {"Has reformulado inteligentemente el concepto." if reading_level == ReadingLevel.INFERENCIAL else "Dominas el tema completamente."}

🎯 **Sigue así** con Active Recall. Estás en el camino correcto."""
        
        elif nivel == 'BUENO':
            feedback = f"""✅ **¡MUY BIEN!** Buen entendimiento del tema.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

👍 Has captado los conceptos principales. {f"Encontraste {len(shared_keywords)} palabras clave correctas." if shared_keywords else ""}

💡 **Tip**: Podrías profundizar un poco más, pero vas muy bien."""
        
        elif nivel == 'ACEPTABLE':
            feedback = f"""⚠️ **RESPUESTA PARCIAL**. Tienes la idea, pero falta desarrollo.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

📌 Tu respuesta toca puntos correctos, pero necesita más precisión o detalle.

📚 **Sugerencia**: Revisa el fragmento y explica con más profundidad. Recuerda: **ENTENDER > Memorizar**."""
        
        else:  # INSUFICIENTE
            feedback = f"""❌ **NECESITA MEJORAR**. La respuesta no refleja bien el material.

📊 **Score**: {score}% | 🧠 **Nivel**: {reading_level.value.capitalize()}

🔄 **Intenta de nuevo**:
1. Relee el fragmento relevante
2. Cierra el material
3. Explica **CON TUS PROPIAS PALABRAS**
4. Enfócate en **ENTENDER**, no memorizar

🎯 **Tip**: Imagina que se lo explicas a un amigo."""
        
        # ✅ NUEVO: Agregar warning de ambigüedad al final si existe
        if ambiguity_warning:
            feedback += f"\n\n{ambiguity_warning}"
        
        return feedback
    
    def _create_error_result(self, error_message: str) -> ValidationResult:
        """Crea resultado de error para respuestas inv├ílidas"""
        return ValidationResult(
            score_final=0,
            nivel='INSUFICIENTE',
            reading_level=ReadingLevel.LITERAL,
            es_correcto=False,
            feedback=f"ÔØî {error_message}",
            color='#ef4444',
            justificacion=error_message,
            scoring_breakdown={},
            best_chunk={},
            alternative_chunks=[],
            keywords_found=[],
            chunks_analyzed=0,
            chunks_filtered=0
        )


# ===== FUNCI├ôN DE INTEGRACI├ôN CON ENDPOINT EXISTENTE =====

def validate_with_advanced_system(
    user_embedding: np.ndarray,
    material_chunks: List[Dict],
    user_answer: str,
    question_text: str,
    use_advanced: bool = True
) -> Dict:
    """
    Wrapper para integraci├│n con backend/main.py
    
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
    print("­ƒºá ADVANCED VALIDATOR - Sistema Multi-Nivel")
    print("="*80)
    
    validator = AdvancedValidator()
    
    print("\nÔ£à Caracter├¡sticas:")
    print("   - Filtrado por keywords antes de validaci├│n")
    print("   - Ranking de chunks por relevancia")
    print("   - Validaci├│n contra TOP 3 chunks")
    print("   - Scoring multi-nivel (literal, inferencial, cr├¡tico)")
    print("   - Justificaci├│n transparente")
    print("   - Compensaci├│n justa para reformulaciones")
    
    print("\n­ƒôè Pesos configurados:")
    print(f"   - Keywords: {validator.weights['keyword']*100}%")
    print(f"   - Contexto: {validator.weights['context']*100}%")
    print(f"   - Razonamiento: {validator.weights['reasoning']*100}%")
    
    print("\n­ƒÄ» Umbrales:")
    for nivel, threshold in validator.thresholds.items():
        print(f"   - {nivel}: ÔëÑ{threshold*100}%")
    
    print("="*80)
