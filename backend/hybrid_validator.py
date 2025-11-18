import numpy as np
import re
from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi

class HybridValidator:
    def __init__(self, embedding_model):
        self.model = embedding_model
        # Umbrales para clasificación de respuestas (basados en Short Answer Grading - SAG)
        # Estos umbrales se aplican sobre S_raw (score bruto en [0,1])
        self.thresholds = {
            'excelente': 0.85,   # ≥0.85 → Excelente (90-100%)
            'bueno': 0.70,       # 0.70-0.84 → Bueno (70-89%)
            'aceptable': 0.50,   # 0.50-0.69 → Aceptable (50-69%)
            'rechazo': 0.50      # <0.50 → Necesita mejorar (0-49%)
        }
        # Pesos optimizados para OCR + parafraseo (basado en literatura SAG)
        # Priorizan semántica sobre léxico por errores OCR en PDFs
        self.weights = {
            'bm25': 0.05,        # 5% - Coincidencias léxicas (reducido por OCR)
            'cosine': 0.80,      # 80% - Similitud semántica (eje principal)
            'coverage': 0.15     # 15% - Cobertura de keywords clave
        }
        # Rango de normalización para cosine similarity (valores empíricos)
        # Basado en all-MiniLM-L6-v2 + análisis de respuestas reales
        self.cosine_min = 0.30   # Por debajo: casi siempre incorrecto
        self.cosine_max = 0.80   # Por encima: muy similar al texto
        
        # Min-max scaling para porcentaje 0-100%
        self.expected_min = 0.30  # Respuesta muy mala → 0%
        self.expected_max = 0.90  # Respuesta excelente → 100%
        
        self.stopwords = {'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'a', 'al', 'en', 'por', 'para', 'con', 'y', 'o', 'pero', 'si', 'no', 'que', 'como', 'cuando', 'donde', 'cual', 'quien', 'su', 'sus', 'mi', 'mis', 'tu', 'tus', 'se', 'le', 'lo', 'me', 'te', 'nos', 'os'}
    
    def normalize_cosine(self, cosine_sim: float) -> float:
        """
        Normaliza similitud del coseno al rango 0-1 usando límites empíricos
        
        Basado en investigación de Sentence-BERT:
        - cosine < 0.30: sin relación (0%)
        - cosine = 0.80: muy similar (100%)
        
        Referencia: Reimers & Gurevych (2019), "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
        """
        normalized = (cosine_sim - self.cosine_min) / (self.cosine_max - self.cosine_min)
        return max(0.0, min(1.0, normalized))  # Clamp a [0, 1]
    
    def length_bonus(self, answer: str) -> float:
        """
        Bonus pequeño por respuestas de longitud razonable
        Evita respuestas telegrama o testamentos
        
        Args:
            answer: Texto de la respuesta del alumno
            
        Returns:
            float: Bonus en [0, 0.05] (máximo 5 puntos extra)
        """
        tokens = len(answer.split())
        if 8 <= tokens <= 80:  # Rango razonable para Active Recall
            return 0.05
        return 0.0
    
    def to_percentage(self, score_raw: float) -> float:
        """
        Convierte score bruto [0,1] a porcentaje 0-100% con min-max scaling
        
        Mapea el rango esperado de scores reales [0.30-0.90] a [0-100%]
        para distribuir mejor los resultados en toda la escala.
        
        Args:
            score_raw: Score bruto en [0,1]
            
        Returns:
            float: Porcentaje en [0.0, 100.0]
        """
        scaled = (score_raw - self.expected_min) / (self.expected_max - self.expected_min)
        scaled = max(0.0, min(1.0, scaled))  # Clamp a [0,1]
        return round(scaled * 100, 1)
    
    def apply_pedagogical_boost(self, score_raw: float, cosine: float, 
                                user_answer: str, ref_text: str) -> float:
        """
        Booster pedagógico para respuestas concisas pero correctas
        
        Problema: embeddings penalizan asimetría de longitud.
        Si el usuario sintetiza bien (pocas palabras, idea correcta),
        el cosine baja artificialmente.
        
        Solución: si cosine >= 0.40 (dirección correcta) Y la respuesta
        es mucho más corta que el chunk (síntesis), aplicar boost moderado.
        
        Referencia: Gemini 3 Pro analysis (Nov 2025)
        
        Args:
            score_raw: Score antes del boost [0,1]
            cosine: Similitud de embeddings [0,1]
            user_answer: Texto de la respuesta del usuario
            ref_text: Texto del chunk de referencia
            
        Returns:
            float: Score después del boost (máx 0.99)
        """
        BASE_THRESHOLD = 0.40  # Mínimo cosine para aplicar boost
        
        # Solo aplicar si hay similitud razonable
        if cosine < BASE_THRESHOLD:
            return score_raw
        
        # Calcular ratio de longitud (palabras)
        len_user = max(len(user_answer.split()), 1)
        len_ref = max(len(ref_text.split()), 1)
        len_ratio = len_user / len_ref
        
        # Si respuesta es < 50% de la longitud del chunk → síntesis
        if len_ratio < 0.5:
            # Boost progresivo según qué tan corta sea
            boost_factor = 1.5 if len_ratio < 0.3 else 1.3
            boosted = score_raw * boost_factor
            return min(boosted, 0.99)  # Nunca 100% automático
        
        return score_raw
    
    def normalize_embedding(self, embedding: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(embedding)
        if norm < 1e-10:  # Threshold para evitar division por cero o numeros muy pequeños
            return embedding
        return embedding / norm
    
    def extract_keywords(self, text: str):
        # Normalizar texto antes de extraer keywords (quitar espacios OCR)
        # Ejemplo: "H enriet te" → "Henriette"
        text = re.sub(r'\b(\w{1,2})\s+(\w{1,2})\b', r'\1\2', text)
        for _ in range(3):
            text = re.sub(r'\b(\w{1,2})\s+(\w{1,2})\b', r'\1\2', text)
        text = re.sub(r'\b(\w{2,4})\s+(\w{3,6})\b', r'\1\2', text)
        
        text = text.lower()
        words = re.findall(r'\b\w{3,}\b', text)
        keywords = [w for w in words if w not in self.stopwords]
        return keywords
    
    def expand_keywords(self, keywords):
        expanded = set(keywords)
        for word in keywords:
            expanded.add(word)
            if len(word) >= 6:
                expanded.add(word[:6])
            elif len(word) >= 5:
                expanded.add(word[:5])
            if word[0].isupper():
                expanded.add(word.lower())
        return expanded
    
    def bm25_score(self, query_keywords, chunk_text: str, corpus):
        tokenized_corpus = [self.extract_keywords(text) for text in corpus]
        
        # Protección: si el corpus está vacío o todos los documentos vacíos
        if not tokenized_corpus or all(len(doc) == 0 for doc in tokenized_corpus):
            return 0.0
        
        bm25 = BM25Okapi(tokenized_corpus)
        expanded_query = list(self.expand_keywords(query_keywords))
        
        # Protección: si la query está vacía
        if not expanded_query:
            return 0.0
        
        scores = bm25.get_scores(expanded_query)
        chunk_keywords = self.extract_keywords(chunk_text)
        try:
            chunk_index = tokenized_corpus.index(chunk_keywords)
            return scores[chunk_index]
        except ValueError:
            return np.mean(scores) if len(scores) > 0 else 0.0
    
    def cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        emb1_norm = self.normalize_embedding(emb1)
        emb2_norm = self.normalize_embedding(emb2)
        similarity = np.dot(emb1_norm, emb2_norm)
        return max(0.0, min(1.0, similarity))
    
    def calculate_coverage(self, answer_keywords, chunk_keywords):
        answer_expanded = self.expand_keywords(answer_keywords)
        chunk_expanded = self.expand_keywords(chunk_keywords)
        intersection = answer_expanded & chunk_expanded
        if len(answer_expanded) == 0:
            return 0.0
        coverage = len(intersection) / len(answer_expanded)
        return coverage
    
    def hybrid_score(self, question: str, answer: str, chunk, all_chunks):
        question_keywords = self.extract_keywords(question)
        answer_keywords = self.extract_keywords(answer)
        combined_keywords = list(set(question_keywords + answer_keywords))
        
        answer_embedding = self.normalize_embedding(
            self.model.encode(answer, convert_to_tensor=False)
        )
        chunk_embedding = self.normalize_embedding(
            np.array(chunk['embedding'])
        )
        
        corpus = [c['text_full'] for c in all_chunks]
        bm25_score_raw = self.bm25_score(combined_keywords, chunk['text_full'], corpus)
        bm25_normalized = min(1.0, bm25_score_raw / 10.0)
        
        cosine_score_raw = self.cosine_similarity(answer_embedding, chunk_embedding)
        # NUEVO: Normalizar cosine al rango 0-1 basado en valores empíricos
        cosine_normalized = self.normalize_cosine(cosine_score_raw)
        
        chunk_keywords = self.extract_keywords(chunk['text_full'])
        coverage_score = self.calculate_coverage(answer_keywords, chunk_keywords)
        
        # Score base: combinar métricas normalizadas con pesos calibrados
        # 80% semántica + 15% cobertura + 5% léxico (reducido por OCR)
        score_base = (
            self.weights['bm25'] * bm25_normalized +
            self.weights['cosine'] * cosine_normalized +
            self.weights['coverage'] * coverage_score
        )
        
        # Aplicar bonus por longitud razonable (+5% máximo)
        bonus = self.length_bonus(answer)
        score_raw = max(0.0, min(1.0, score_base + bonus))  # Clamp a [0,1]
        
        # NUEVO: Aplicar boost pedagógico para respuestas concisas pero correctas
        score_raw = self.apply_pedagogical_boost(
            score_raw=score_raw,
            cosine=cosine_normalized,
            user_answer=answer,
            ref_text=chunk['text_full']
        )
        
        # Convertir a porcentaje 0-100% con min-max scaling
        score_pct = self.to_percentage(score_raw)
        
        details = {
            'bm25': round(bm25_normalized, 4),
            'cosine': round(cosine_score_raw, 4),  # Raw para logs
            'cosine_normalized': round(cosine_normalized, 4),  # Normalizado
            'coverage': round(coverage_score, 4),
            'score_base': round(score_base, 4),
            'length_bonus': round(bonus, 4),
            'score_raw': round(score_raw, 4),  # Score bruto [0,1]
            'score_pct': score_pct,  # Porcentaje [0-100]
            'final': round(score_raw, 4),  # Mantener compatibilidad
            'weights': self.weights,
            'keywords_found': list(
                self.expand_keywords(answer_keywords) & 
                self.expand_keywords(chunk_keywords)
            )[:5]
        }
        
        return score_raw, details
    
    def detect_ambiguity(self, ranked_chunks):
        if len(ranked_chunks) < 2:
            return {'is_ambiguous': False, 'reason': 'Menos de 2 chunks'}
        
        top1_score = ranked_chunks[0][1]
        top2_score = ranked_chunks[1][1]
        score_diff = top1_score - top2_score
        is_ambiguous = score_diff < 0.08
        
        return {
            'is_ambiguous': is_ambiguous,
            'score_diff': round(score_diff, 4),
            'top1_score': round(top1_score, 4),
            'top2_score': round(top2_score, 4),
            'threshold': 0.08
        }
    
    def validate_answer(self, question: str, user_answer: str, chunks):
        if not chunks or len(chunks) == 0:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'feedback': 'No hay chunks disponibles para validacion',
                'category': 'error'
            }
        
        if len(user_answer.strip()) < 10:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'feedback': 'La respuesta es demasiado corta (minimo 10 caracteres)',
                'category': 'error'
            }
        
        scored_chunks = []
        for chunk in chunks:
            score, details = self.hybrid_score(question, user_answer, chunk, chunks)
            scored_chunks.append((chunk, score, details))
        
        ranked_chunks = sorted(scored_chunks, key=lambda x: x[1], reverse=True)
        top_k = ranked_chunks[:3]
        
        ambiguity = self.detect_ambiguity([(c, s) for c, s, _ in ranked_chunks])
        
        best_chunk, best_score_raw, best_details = top_k[0]
        best_score_pct = best_details['score_pct']  # Usar porcentaje para UI
        
        # Clasificación basada en score_raw (0-1)
        if best_score_raw >= self.thresholds['excelente']:
            category = 'excelente'
            is_valid = True
            feedback = 'Excelente! Tu respuesta captura perfectamente el contenido.'
        elif best_score_raw >= self.thresholds['bueno']:
            category = 'bueno'
            is_valid = True
            feedback = 'Muy bien. Tu respuesta es correcta y bien fundamentada.'
        elif best_score_raw >= self.thresholds['aceptable']:
            category = 'aceptable'
            is_valid = True
            feedback = 'Aceptable. Tu respuesta esta en la direccion correcta.'
        else:
            category = 'necesita_mejorar'
            is_valid = False
            feedback = 'Tu respuesta necesita más trabajo. Revisa el material.'
        
        result = {
            'is_valid': is_valid,
            'confidence': best_score_pct,  # Porcentaje 0-100
            'score_raw': round(best_score_raw, 4),  # Score bruto [0,1]
            'feedback': feedback,
            'category': category,
            'best_chunk': {
                'text': best_chunk['text_full'][:200] + '...' if len(best_chunk['text_full']) > 200 else best_chunk['text_full'],
                'page': best_chunk.get('page_number', 'N/A'),
                'chunk_id': best_chunk.get('chunk_id', 'N/A')
            },
            'top_3_scores': [
                {
                    'score': d['score_pct'],  # Porcentaje
                    'score_raw': d['score_raw'],  # Bruto
                    'chunk_id': c.get('chunk_id', 'N/A'),
                    'details': d
                }
                for c, s, d in top_k
            ],
            'ambiguity': ambiguity,
            'thresholds': {k: v * 100 for k, v in self.thresholds.items()},
            'scoring_method': 'HybridValidator (BM25 + Cosine + Coverage)',
            'weights_used': self.weights
        }
        
        return result
