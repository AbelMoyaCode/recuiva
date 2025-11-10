"""
GENERADOR INTELIGENTE DE PREGUNTAS - RECUIVA
=============================================

Sistema de generación de preguntas basado en análisis lingüístico profundo.
SIN usar LLMs externos - usa ContentAnalyzer para análisis inteligente.

CARACTERÍSTICAS:
- Filtra chunks de metadata automáticamente
- Detecta tipo de contenido (narrativo, académico, técnico, etc.)
- Genera preguntas contextualizadas al tipo detectado
- Justifica cada decisión con razonamiento explícito
- Compatible con UTF-8, emojis, múltiples idiomas

Autor: Abel Jesús Moya Acosta
Fecha: 10 de noviembre de 2025
Proyecto: Recuiva - Active Recall con IA
"""

import re
import random
from typing import List, Dict, Optional
from dataclasses import dataclass
from content_analyzer import ContentAnalyzer, ChunkAnalysis

@dataclass
class GeneratedQuestion:
    """Pregunta generada con justificación completa"""
    question: str
    reference_chunk: str
    chunk_index: int
    question_type: str
    concepts: List[str]
    reasoning: Dict[str, any]  # Justificación del análisis
    confidence: float  # Confianza en la pregunta generada


# Inicializar analizador global
_analyzer = ContentAnalyzer()


def generate_questions_dict(chunks: List[str], num_questions: int = 5, strategy: str = 'random') -> List[Dict]:
    """
    Generador INTELIGENTE de preguntas usando análisis lingüístico profundo
    
    MEJORAS:
    - ✅ Filtra automáticamente chunks de metadata
    - ✅ Analiza tipo de contenido (narrativo, académico, técnico...)
    - ✅ Genera preguntas CONTEXTUALIZADAS al tipo
    - ✅ Justifica cada decisión
    - ✅ Siempre aleatorio para variedad
    
    Args:
        chunks: Lista de chunks del material
        num_questions: Número de preguntas a generar
        strategy: Ignorado (siempre aleatorio)
        
    Returns:
        Lista de diccionarios con preguntas y metadatos
    """
    if not chunks:
        return []
    
    # Filtrar chunks válidos (excluir metadata)
    valid_chunks = []
    for idx, chunk in enumerate(chunks):
        analysis = _analyzer.analyze(chunk)
        if analysis.content_type != 'metadata':
            valid_chunks.append((idx, chunk, analysis))
    
    if not valid_chunks:
        print("⚠️ Todos los chunks son metadata, no se pueden generar preguntas")
        return []
    
    # Seleccionar chunks aleatorios
    num_questions = min(num_questions, len(valid_chunks))
    selected = random.sample(valid_chunks, num_questions)
    
    questions = []
    for idx, chunk, analysis in selected:
        question_data = _generate_intelligent_question(chunk, idx, analysis)
        questions.append(question_data)
    
    return questions


def _generate_intelligent_question(
    chunk: str,
    chunk_index: int,
    analysis: ChunkAnalysis
) -> Dict:
    """
    Genera pregunta inteligente basada en el análisis del chunk
    
    ESTRATEGIA:
    1. Usa el tipo detectado (narrative, academic, technical...)
    2. Extrae entidades clave del análisis
    3. Aplica template contextualizado
    4. Retorna con justificación completa
    """
    content_type = analysis.content_type
    entities = analysis.key_entities
    patterns = analysis.patterns_detected
    features = analysis.linguistic_features
    
    # Entidad principal
    main_entity = entities[0] if entities else "este concepto"
    
    # Generar pregunta según tipo
    if content_type == 'narrative':
        question = _generate_narrative_question(chunk, entities, analysis.main_verbs, patterns)
    
    elif content_type == 'academic':
        question = _generate_academic_question(chunk, entities, patterns)
    
    elif content_type == 'technical':
        question = _generate_technical_question(chunk, entities, patterns)
    
    elif content_type == 'procedural':
        question = _generate_procedural_question(chunk, entities, patterns)
    
    else:  # descriptive
        question = _generate_descriptive_question(chunk, entities, patterns)
    
    # Preparar razonamiento
    reasoning = {
        'content_type': content_type,
        'confidence': analysis.confidence,
        'patterns_detected': patterns,
        'entities_found': len(entities),
        'main_verbs_count': len(analysis.main_verbs),
        'justification': analysis.justification,
        'linguistic_features': {
            'word_count': features['word_count'],
            'sentence_count': features['sentence_count'],
            'has_dialogue': 'dialogue' in patterns
        }
    }
    
    return {
        'question': question,
        'reference_chunk': chunk,
        'chunk_index': chunk_index,
        'question_type': content_type,
        'concepts': entities,
        'reasoning': reasoning,
        'confidence': analysis.confidence
    }


def _generate_narrative_question(
    chunk: str,
    entities: List[str],
    verbs: List[tuple],
    patterns: List[str]
) -> str:
    """Genera pregunta para contenido NARRATIVO (historias, novelas)"""
    
    # Si hay diálogo
    if 'dialogue' in patterns and entities:
        character = entities[0]
        return f"Según el texto, ¿qué dice o hace {character} en esta parte?"
    
    # Si hay verbos narrativos
    if verbs:
        verb_type, verb = verbs[0]
        if entities:
            subject = entities[0]
            return f"¿Qué {verb} {subject} en el fragmento?"
        else:
            return f"¿Qué se {verb} en esta parte de la historia?"
    
    # Pregunta general narrativa
    if len(entities) >= 2:
        return f"¿Qué sucede con {entities[0]} en relación a {entities[1]}?"
    elif entities:
        return f"Resume los eventos que involucran a {entities[0]}"
    else:
        return "¿Qué acontecimientos se narran en este fragmento?"


def _generate_academic_question(
    chunk: str,
    entities: List[str],
    patterns: List[str]
) -> str:
    """Genera pregunta para contenido ACADÉMICO (ensayos, papers)"""
    
    # Si hay definición
    if 'definition' in patterns:
        if entities:
            return f"¿Cómo se define {entities[0]} según el material?"
        else:
            return "¿Qué concepto se define en este fragmento?"
    
    # Si hay comparación
    if 'comparison' in patterns and len(entities) >= 2:
        return f"Compara {entities[0]} y {entities[1]} según el texto"
    
    # Si hay causalidad
    if 'causality' in patterns:
        if entities:
            return f"¿Por qué ocurre {entities[0]} según el material?"
        else:
            return "Explica la relación causa-efecto mencionada en el texto"
    
    # Si hay ejemplos
    if 'example' in patterns and entities:
        return f"¿Qué ejemplos se presentan sobre {entities[0]}?"
    
    # Pregunta académica general
    if entities:
        return f"Explica el concepto de {entities[0]} mencionado en el material"
    else:
        return "¿Qué idea principal se desarrolla en este fragmento?"


def _generate_technical_question(
    chunk: str,
    entities: List[str],
    patterns: List[str]
) -> str:
    """Genera pregunta para contenido TÉCNICO (manuales, código)"""
    
    # Si hay fórmula matemática
    if 'mathematical_formula' in patterns:
        if entities:
            return f"¿Qué fórmula se presenta para calcular {entities[0]}?"
        else:
            return "¿Qué expresión matemática se muestra y para qué sirve?"
    
    # Si hay datos numéricos
    if 'numerical_data' in patterns:
        if entities:
            return f"¿Qué datos específicos se mencionan sobre {entities[0]}?"
        else:
            return "¿Qué información cuantitativa se presenta en el fragmento?"
    
    # Pregunta técnica general
    if entities:
        return f"¿Cómo funciona {entities[0]} según el texto?"
    else:
        return "Explica el proceso técnico descrito en el material"


def _generate_procedural_question(
    chunk: str,
    entities: List[str],
    patterns: List[str]
) -> str:
    """Genera pregunta para contenido PROCEDIMENTAL (instrucciones, pasos)"""
    
    # Si hay lista o enumeración
    if 'list' in patterns:
        if entities:
            return f"¿Cuáles son los pasos relacionados con {entities[0]}?"
        else:
            return "Enumera los pasos o elementos mencionados en el texto"
    
    # Pregunta procedimental general
    if entities:
        return f"¿Cómo se realiza el proceso de {entities[0]}?"
    else:
        return "Describe el procedimiento explicado en el fragmento"


def _generate_descriptive_question(
    chunk: str,
    entities: List[str],
    patterns: List[str]
) -> str:
    """Genera pregunta para contenido DESCRIPTIVO (descripciones, explicaciones)"""
    
    if len(entities) >= 2:
        return f"Describe la relación entre {entities[0]} y {entities[1]}"
    elif entities:
        return f"¿Qué características de {entities[0]} se mencionan en el texto?"
    else:
        return "¿Qué información se presenta en este fragmento del material?"


# ========================================
# FUNCIONES LEGACY (para compatibilidad)
# ========================================

def detect_content_type(text: str) -> str:
    """LEGACY: Usa el analizador nuevo"""
    analysis = _analyzer.analyze(text)
    return analysis.content_type


def extract_key_concepts(text: str, max_concepts: int = 5) -> List[str]:
    """LEGACY: Usa el analizador nuevo"""
    analysis = _analyzer.analyze(text)
    return analysis.key_entities[:max_concepts]
