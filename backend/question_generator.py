"""
GENERADOR INTELIGENTE DE PREGUNTAS - RECUIVA
=============================================

Sistema de generación de preguntas basado en análisis lingüístico profundo.
SIN usar LLMs externos - usa ContentAnalyzer para análisis inteligente.

CARACTERÍSTICAS:
- Filtra chunks de metadata automáticamente
- Detecta tipo de contenido (narrativo, académico, técnico, etc.)
- NUEVO: Genera preguntas basadas en TIPO DE ENTIDAD (universal)
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
from spanish_grammar_analyzer import get_entity_type
from universal_entity_types import EntityType

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
    
    MEJORAS:
    ✅ Valida entidades (no "Como", "Pero", etc.)
    ✅ Clasifica entidades por tipo UNIVERSAL (persona, concepto, objeto, proceso)
    ✅ Genera preguntas ESPECÍFICAS al tipo de entidad
    ✅ Funciona para literatura, ciencia, técnico, académico
    """
    content_type = analysis.content_type
    entities = analysis.key_entities
    patterns = analysis.patterns_detected
    features = analysis.linguistic_features
    
    # VALIDACIÓN: Filtrar entidades inválidas
    valid_entities = []
    INVALID_WORDS = {
        'como', 'pero', 'cuando', 'donde', 'porque', 'aunque', 'cierto',
        'verdad', 'inmediatamente', 'entonces', 'mientras', 'después', 'antes',
        'esper', 'cabal', 'loro', 'eux', 'mot', 'te'
    }
    
    for entity in entities:
        words = entity.lower().split()
        if not any(w in INVALID_WORDS for w in words):
            if len(entity) >= 4 and len(entity.split()) >= 1:
                valid_entities.append(entity)
    
    entities = valid_entities
    
    # NUEVO: CLASIFICAR ENTIDADES POR TIPO UNIVERSAL
    entity_types_map = {}
    for entity in entities[:3]:  # Solo primeras 3 para eficiencia
        entity_type = get_entity_type(entity, chunk)
        entity_types_map[entity] = entity_type
    
    # NUEVO: GENERAR PREGUNTA BASADA EN TIPO DE ENTIDAD (prioridad)
    for entity, entity_type in entity_types_map.items():
        
        if entity_type == EntityType.PERSON:
            question = f"¿Quién fue {entity} y qué papel desempeñó en los acontecimientos descritos?"
            question_type = 'entity_person'
            break
        
        elif entity_type == EntityType.CONCEPT:
            question = f"Define y explica el concepto de {entity} según el material presentado"
            question_type = 'entity_concept'
            break
        
        elif entity_type == EntityType.OBJECT:
            question = f"Describe las características y función de {entity} mencionadas en el texto"
            question_type = 'entity_object'
            break
        
        elif entity_type == EntityType.PROCESS:
            question = f"Explica paso a paso cómo funciona el proceso de {entity}"
            question_type = 'entity_process'
            break
        
        elif entity_type == EntityType.LOCATION:
            question = f"¿Qué importancia tiene {entity} en el contexto descrito?"
            question_type = 'entity_location'
            break
        
        elif entity_type == EntityType.ORGANIZATION:
            question = f"¿Cuál es el rol de {entity} según lo mencionado en el material?"
            question_type = 'entity_organization'
            break
    
    else:
        # FALLBACK: Si no hay entidades tipadas, usar método por content_type
        if content_type == 'narrative':
            question = _generate_narrative_question(chunk, entities, analysis.main_verbs, patterns)
            question_type = content_type
        elif content_type == 'academic':
            question = _generate_academic_question(chunk, entities, patterns)
            question_type = content_type
        elif content_type == 'technical':
            question = _generate_technical_question(chunk, entities, patterns)
            question_type = content_type
        elif content_type == 'procedural':
            question = _generate_procedural_question(chunk, entities, patterns)
            question_type = content_type
        else:
            question = _generate_descriptive_question(chunk, entities, patterns)
            question_type = content_type
    
    # Preparar razonamiento
    reasoning = {
        'content_type': content_type,
        'confidence': analysis.confidence,
        'patterns_detected': patterns,
        'entities_found': len(entities),
        'entities_valid': entities,
        'entity_types': {k: v.value for k, v in entity_types_map.items()},  # NUEVO
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
        'question_type': question_type,  # Actualizado con tipo específico
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
    """
    Genera pregunta para contenido NARRATIVO (historias, novelas)
    
    MEJORAS:
    ✅ Preguntas completas y naturales (sin límites artificiales)
    ✅ Usa nombres completos validados gramaticalmente
    ✅ Preguntas específicas basadas en el chunk real
    ✅ Si no hay entidades válidas, extrae del texto directamente
    """
    
    # Extraer primera oración completa del chunk para contexto
    sentences = chunk.split('.')
    first_sentence = sentences[0].strip() if sentences else chunk[:200]
    
    # Si hay diálogo Y entidades válidas
    if 'dialogue' in patterns and entities:
        character = entities[0]
        return f"Según el fragmento, ¿qué dice, hace o piensa {character} en esta parte de la narración?"
    
    # Si hay verbos narrativos Y entidades
    if verbs and entities:
        verb_type, verb = verbs[0]
        subject = entities[0]
        return f"En el texto, ¿qué {verb} {subject} y por qué es relevante este acontecimiento?"
    
    # Si hay múltiples entidades válidas
    if len(entities) >= 2:
        return f"Explica la relación entre {entities[0]} y {entities[1]} según lo descrito en el fragmento"
    
    # Si hay UNA entidad válida
    elif len(entities) == 1:
        # Buscar acción específica en el chunk
        action_verbs = ['hizo', 'dijo', 'pensó', 'sintió', 'vio', 'llegó', 'salió', 'entró']
        found_action = None
        for action in action_verbs:
            if action in chunk.lower():
                found_action = action
                break
        
        if found_action:
            return f"¿Qué {found_action} {entities[0]} en este fragmento del material?"
        else:
            return f"Resume los eventos más importantes que involucran a {entities[0]} en este fragmento"
    
    # Si NO hay entidades válidas, genera pregunta basada en el contenido real
    else:
        # Extraer sustantivos del chunk (palabras capitalizadas o sustantivos comunes)
        words = chunk.split()
        important_words = [w for w in words if len(w) > 5 and w[0].isupper()]
        
        if important_words and len(important_words) > 0:
            # Usar las primeras palabras importantes encontradas
            context_hint = important_words[0] if len(important_words) == 1 else f"{important_words[0]} y {important_words[1]}"
            return f"¿Qué se describe sobre {context_hint} en este fragmento del material?"
        elif 'dialogue' in patterns:
            return "¿Qué conversación o diálogo se presenta en este fragmento y qué información aporta?"
        elif verbs:
            return "Resume los acontecimientos principales narrados en este fragmento"
        else:
            # Último recurso: usar parte del texto real
            snippet = first_sentence[:80] + "..." if len(first_sentence) > 80 else first_sentence
            return f"Explica con tus palabras el siguiente fragmento: '{snippet}'"


def _generate_academic_question(
    chunk: str,
    entities: List[str],
    patterns: List[str]
) -> str:
    """
    Genera pregunta para contenido ACADÉMICO (ensayos, papers, libros técnicos)
    
    MEJORAS:
    ✅ Preguntas elaboradas sin restricciones de longitud
    ✅ Múltiples entidades en preguntas complejas
    ✅ Extrae conceptos clave del texto real
    """
    
    # Extraer conceptos técnicos del chunk (palabras importantes)
    words = chunk.split()
    technical_terms = [w.strip(',.;:') for w in words if len(w) > 6 and not w.lower() in {'ejemplo', 'embargo', 'través', 'mediante'}]
    
    # Si hay definición
    if 'definition' in patterns:
        if entities:
            return f"¿Cómo se define {entities[0]} según el material? Explica sus características principales"
        elif technical_terms:
            concept = technical_terms[0]
            return f"Define el concepto de {concept} mencionado en el texto y explica su importancia"
        else:
            return "¿Qué concepto se define en este fragmento y cuáles son sus características principales?"
    
    # Si hay comparación
    if 'comparison' in patterns:
        if len(entities) >= 2:
            return f"Compara {entities[0]} con {entities[1]} según el material, indicando diferencias y similitudes"
        elif len(technical_terms) >= 2:
            return f"Compara {technical_terms[0]} con {technical_terms[1]} según lo explicado en el fragmento"
        else:
            return "¿Qué elementos se comparan en el texto y cuáles son sus diferencias principales?"
    
    # Si hay causalidad
    if 'causality' in patterns:
        if entities:
            return f"¿Por qué ocurre {entities[0]} según el material? Explica las causas y consecuencias"
        else:
            return "Explica la relación causa-efecto descrita en el texto"
    
    # Si hay ejemplos
    if 'example' in patterns and entities:
        return f"¿Qué ejemplos se presentan sobre {entities[0]} y cómo ilustran el concepto?"
    
    # Pregunta académica basada en el contenido real
    if len(entities) >= 2:
        entities_str = ", ".join(entities[:3])
        return f"Explica la relación entre {entities_str} según el fragmento"
    elif entities:
        return f"Desarrolla el concepto de {entities[0]} mencionado en el material"
    elif technical_terms:
        # Usar términos técnicos extraídos del chunk
        if len(technical_terms) >= 2:
            return f"¿Qué relación existe entre {technical_terms[0]} y {technical_terms[1]} según el texto?"
        else:
            return f"Explica qué se menciona sobre {technical_terms[0]} en el fragmento"
    else:
        # Extraer primera oración para dar contexto
        first_sentence = chunk.split('.')[0].strip()
        if len(first_sentence) > 15:
            snippet = first_sentence[:100] + "..." if len(first_sentence) > 100 else first_sentence
            return f"Explica con tus palabras: '{snippet}'"
        else:
            return "¿Qué idea principal se desarrolla en este fragmento del material?"


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
