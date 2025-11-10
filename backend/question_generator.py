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
    
    MEJORA CRÍTICA:
    ✅ Valida que entidades sean nombres reales (no "Como", "Pero", etc.)
    ✅ Si no hay entidades válidas, genera pregunta genérica
    ✅ Previene preguntas absurdas como "relación entre Como y Cierto"
    """
    content_type = analysis.content_type
    entities = analysis.key_entities
    patterns = analysis.patterns_detected
    features = analysis.linguistic_features
    
    # VALIDACIÓN CRÍTICA: Filtrar entidades inválidas
    valid_entities = []
    INVALID_WORDS = {
        'como', 'pero', 'cuando', 'donde', 'porque', 'aunque', 'cierto',
        'verdad', 'inmediatamente', 'entonces', 'mientras', 'después', 'antes',
        'esper', 'cabal', 'loro', 'eux', 'mot', 'te'  # Fragmentos rotos
    }
    
    for entity in entities:
        # Validar que no sea palabra inválida
        words = entity.lower().split()
        if not any(w in INVALID_WORDS for w in words):
            # Validar longitud mínima razonable
            if len(entity) >= 4 and len(entity.split()) >= 1:
                valid_entities.append(entity)
    
    # Actualizar análisis con entidades válidas
    entities = valid_entities
    
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
        'entities_valid': entities,  # NUEVO: Lista de entidades válidas
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
        'concepts': entities,  # Solo entidades válidas
        'reasoning': reasoning,
        'confidence': analysis.confidence
    }


def _generate_narrative_question(
    chunk: str,
    entities: List[str],
    verbs: List[tuple],
    patterns: List[str]
) -> str:
    """
    Genera pregunta para contenido NARRATIVO (historias, novelas)
    
    MEJORAS:
    ✅ Preguntas completas y naturales (sin límites artificiales)
    ✅ Usa nombres completos validados gramaticalmente
    ✅ Si no hay entidades válidas, pregunta sobre el contenido general
    """
    
    # Si hay diálogo Y entidades válidas
    if 'dialogue' in patterns and entities:
        character = entities[0]
        return f"Según el fragmento, ¿qué dice, hace o piensa {character} en esta parte de la narración?"
    
    # Si hay verbos narrativos Y entidades
    if verbs and entities:
        verb_type, verb = verbs[0]
        subject = entities[0]
        return f"En el texto mencionado, ¿qué {verb} {subject} y cuál es la importancia de esta acción?"
    
    # Si hay múltiples entidades válidas
    if len(entities) >= 2:
        return f"Explica la relación entre {entities[0]} y {entities[1]} según lo descrito en el fragmento del material"
    
    # Si hay UNA entidad válida
    elif len(entities) == 1:
        return f"Resume los eventos más importantes que involucran a {entities[0]} en este fragmento"
    
    # Si NO hay entidades válidas, pregunta genérica sobre contenido
    else:
        if 'dialogue' in patterns:
            return "¿Qué conversación o diálogo se presenta en este fragmento y qué información aporta a la historia?"
        elif verbs:
            return "Resume los acontecimientos principales narrados en este fragmento del material"
        else:
            return "¿Qué eventos importantes se describen en esta parte de la narración?"


def _generate_academic_question(
    chunk: str,
    entities: List[str],
    patterns: List[str]
) -> str:
    """
    Genera pregunta para contenido ACADÉMICO (ensayos, papers)
    
    MEJORAS:
    ✅ Preguntas elaboradas sin restricciones de longitud
    ✅ Múltiples entidades en preguntas complejas
    """
    
    # Si hay definición
    if 'definition' in patterns:
        if entities:
            return f"¿Cómo se define el concepto de {entities[0]} según el material? Explica con detalle los aspectos más importantes mencionados"
        else:
            return "¿Qué concepto se define en este fragmento y cuáles son sus características principales según el texto?"
    
    # Si hay comparación
    if 'comparison' in patterns and len(entities) >= 2:
        return f"Compara y contrasta {entities[0]} con {entities[1]} según lo explicado en el material, destacando las diferencias y similitudes clave"
    
    # Si hay causalidad
    if 'causality' in patterns:
        if entities:
            return f"¿Por qué ocurre {entities[0]} según el material? Explica las causas y consecuencias mencionadas en el texto"
        else:
            return "Explica la relación causa-efecto descrita en el texto y analiza los factores involucrados"
    
    # Si hay ejemplos
    if 'example' in patterns and entities:
        return f"¿Qué ejemplos se presentan sobre {entities[0]} y cómo ilustran el concepto explicado en el material?"
    
    # Pregunta académica general con múltiples entidades
    if len(entities) >= 2:
        entities_str = ", ".join(entities[:3])
        return f"Explica la relación entre {entities_str} según el análisis presentado en el fragmento"
    elif entities:
        return f"Desarrolla y explica el concepto de {entities[0]} mencionado en el material, incluyendo sus aspectos más relevantes"
    else:
        return "¿Qué idea principal se desarrolla en este fragmento y cuáles son los argumentos o evidencias que la sustentan?"


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
