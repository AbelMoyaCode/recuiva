import numpy as np
import re
from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi

class HybridValidator:
    def __init__(self, embedding_model):
        self.model = embedding_model
        # Umbrales para clasificación de respuestas
        self.thresholds = {
            'excelente': 0.80,   # ≥80% → Excelente
            'bueno': 0.60,       # 60-79% → Bueno  
            'aceptable': 0.45,   # 45-59% → Aceptable
            'rechazo': 0.35      # <45% → Necesita mejorar
        }
        # Pesos para combinación híbrida (priorizan similitud semántica)
        self.weights = {
            'bm25': 0.10,        # 10% - Coincidencias léxicas exactas
            'cosine': 0.75,      # 75% - Similitud semántica (eje principal)
            'coverage': 0.15     # 15% - Cobertura de keywords clave
        }
        # Rango de normalización para cosine similarity
        # Valores típicos de all-MiniLM-L6-v2: 0.25 (sin relación) a 0.80 (muy similar)
        self.cosine_min = 0.25
        self.cosine_max = 0.80
        
        self.stopwords = {'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'a', 'al', 'en', 'por', 'para', 'con', 'y', 'o', 'pero', 'si', 'no', 'que', 'como', 'cuando', 'donde', 'cual', 'quien', 'su', 'sus', 'mi', 'mis', 'tu', 'tus', 'se', 'le', 'lo', 'me', 'te', 'nos', 'os'}
    
    def normalize_cosine(self, cosine_sim: float) -> float:
        """
        Normaliza similitud del coseno al rango 0-1 usando límites empíricos
        
        Basado en investigación de Sentence-BERT:
        - cosine < 0.25: sin relación (0%)
        - cosine = 0.80: muy similar (100%)
        
        Referencia: Reimers & Gurevych (2019), "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
        """
        normalized = (cosine_sim - self.cosine_min) / (self.cosine_max - self.cosine_min)
        return max(0.0, min(1.0, normalized))  # Clamp a [0, 1]
    
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
        
        # Combinar con pesos calibrados (75% semántica, 10% léxica, 15% cobertura)
        final_score = (
            self.weights['bm25'] * bm25_normalized +
            self.weights['cosine'] * cosine_normalized +
            self.weights['coverage'] * coverage_score
        )
        
        details = {
            'bm25': round(bm25_normalized, 4),
            'cosine': round(cosine_score_raw, 4),  # Raw para logs
            'cosine_normalized': round(cosine_normalized, 4),  # Normalizado
            'coverage': round(coverage_score, 4),
            'final': round(final_score, 4),
            'weights': self.weights,
            'keywords_found': list(
                self.expand_keywords(answer_keywords) & 
                self.expand_keywords(chunk_keywords)
            )[:5]
        }
        
        return final_score, details
    
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
        
        best_chunk, best_score, best_details = top_k[0]
        
        if best_score >= self.thresholds['excelente']:
            category = 'excelente'
            is_valid = True
            feedback = 'Excelente! Tu respuesta captura perfectamente el contenido.'
        elif best_score >= self.thresholds['bueno']:
            category = 'bueno'
            is_valid = True
            feedback = 'Muy bien. Tu respuesta es correcta y bien fundamentada.'
        elif best_score >= self.thresholds['aceptable']:
            category = 'aceptable'
            is_valid = True
            feedback = 'Aceptable. Tu respuesta esta en la direccion correcta.'
        elif best_score >= self.thresholds['rechazo']:
            category = 'parcial'
            is_valid = False
            feedback = 'Tu respuesta esta relacionada pero le falta precision.'
        else:
            category = 'incorrecto'
            is_valid = False
            feedback = 'Tu respuesta no coincide con el contenido del material.'
        
        result = {
            'is_valid': is_valid,
            'confidence': round(best_score * 100, 2),
            'feedback': feedback,
            'category': category,
            'best_chunk': {
                'text': best_chunk['text_full'][:200] + '...' if len(best_chunk['text_full']) > 200 else best_chunk['text_full'],
                'page': best_chunk.get('page_number', 'N/A'),
                'chunk_id': best_chunk.get('chunk_id', 'N/A')
            },
            'top_3_scores': [
                {
                    'score': round(s * 100, 2),
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
