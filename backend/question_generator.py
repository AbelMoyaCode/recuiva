"""
Generador automático de preguntas basadas en chunks del material
SIN usar LLM - usa análisis de texto y templates inteligentes

Autor: Abel Jesús Moya Acosta
Fecha: 10 de noviembre de 2025
"""

import re
import random
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class GeneratedQuestion:
    question: str
    reference_chunk: str
    chunk_index: int
    question_type: str
    concepts: List[str]

# ✅ NO SE USAN TEMPLATES ESTÁTICOS
# El sistema ahora genera preguntas DINÁMICAMENTE analizando el chunk

def detect_content_type(text: str) -> str:
    """Detecta el tipo de contenido del chunk con análisis PROFUNDO del texto"""
    text_lower = text.lower()
    
    # Contar diferentes indicadores
    narrative_score = 0
    academic_score = 0
    factual_score = 0
    
    # Indicadores de narrativa (novelas, cuentos)
    narrative_verbs = ['dijo', 'preguntó', 'respondió', 'pensó', 'miraba', 'caminaba', 
                      'observaba', 'susurró', 'gritó', 'murmuró', 'recordaba', 'sentía',
                      'exclamó', 'contestó', 'miró', 'vio', 'escuchó']
    narrative_score += sum(1 for verb in narrative_verbs if verb in text_lower)
    
    # Indicadores académicos (ensayos, papers, libros técnicos)
    academic_terms = ['concepto', 'definición', 'teoría', 'análisis', 'método', 
                     'investigación', 'estudio', 'resultado', 'conclusión', 'hipótesis',
                     'según', 'mediante', 'respecto']
    academic_score += sum(1 for term in academic_terms if term in text_lower)
    
    # Indicadores factuales (fechas, números, datos)
    if re.search(r'\b\d{4}\b|\b\d+%|\b\d+\s*(?:metros|kilómetros|años|personas)', text):
        factual_score += 2
    
    # Detectar diálogos (comillas)
    if '"' in text or '«' in text or '—' in text or "'" in text:
        narrative_score += 3
    
    # Decisión basada en scores
    if narrative_score > academic_score and narrative_score > factual_score and narrative_score >= 2:
        return 'narrative'
    
    if factual_score >= 2:
        return 'factual'
    
    # Detectar nombres propios (personajes)
    proper_names = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+\b', text)
    if len(proper_names) >= 2:
        return 'character'
    
    # Detectar fórmulas matemáticas
    if re.search(r'[=].*[\d+\-*/√∫∑]|[∫∑√]\d', text):
        return 'formula'
    
    # Por defecto: concepto general
    return 'concept'

def extract_key_concepts(text: str, max_concepts: int = 5) -> List[str]:
    """Extrae fragmentos LITERALES del texto para preguntas específicas"""
    concepts = []
    
    # 1. Extraer FRAGMENTOS LITERALES significativos (3-8 palabras)
    # Buscar frases entre comas, puntos o que empiecen con mayúscula
    literal_fragments = re.findall(r'[A-ZÁÉÍÓÚÑ][^.,;!?]{10,80}(?:[.,;!?]|$)', text)
    
    # Tomar los 2 primeros fragmentos significativos
    for fragment in literal_fragments[:2]:
        fragment = fragment.strip().rstrip('.,;!?')
        if len(fragment.split()) >= 3:  # Mínimo 3 palabras
            concepts.append(fragment)
    
    # 2. Nombres propios EXACTOS (personajes, lugares)
    proper_names = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b', text)
    for name in proper_names:
        if len(name.split()) >= 1 and name not in concepts:
            concepts.append(name)
            if len(concepts) >= max_concepts:
                break
    
    # 3. Términos clave con contexto (sustantivos importantes)
    # Buscar palabras de 5+ letras que aparezcan cerca del inicio
    words = text.split()[:50]  # Primeras 50 palabras
    key_terms = []
    for i, word in enumerate(words):
        clean_word = re.sub(r'[^\w\sáéíóúñÁÉÍÓÚÑ]', '', word)
        if (len(clean_word) >= 5 and 
            clean_word.lower() not in ['sobre', 'cuando', 'donde', 'porque', 'aunque', 
                                       'mientras', 'después', 'antes', 'siempre', 'nunca']):
            # Tomar palabra con 2-3 palabras de contexto
            start = max(0, i-1)
            end = min(len(words), i+3)
            context_phrase = ' '.join(words[start:end])
            key_terms.append(context_phrase)
            if len(key_terms) >= 2:
                break
    
    concepts.extend(key_terms)
    
    # 4. Si aún no hay conceptos, tomar fragmento inicial del chunk
    if not concepts:
        first_sentence = text.split('.')[0].strip()
        if len(first_sentence) > 20:
            concepts.append(first_sentence[:80])
    
    # Limpiar y deduplicar
    concepts = [c.strip() for c in concepts if len(c.strip()) > 5]
    seen = set()
    unique_concepts = []
    for c in concepts:
        if c.lower() not in seen:
            seen.add(c.lower())
            unique_concepts.append(c)
    
    return unique_concepts[:max_concepts]

def generate_questions_dict(chunks: List[str], num_questions: int = 5, strategy: str = 'random') -> List[Dict]:
    """
    Generador INTELIGENTE de preguntas basadas en análisis profundo del chunk
    
    ESTRATEGIA MEJORADA:
    1. Analiza el chunk completo (no solo primera oración)
    2. Identifica: definiciones, acciones, personajes, datos, conceptos
    3. Genera pregunta COMPLETA (sin "...") y NATURAL
    4. Cada llamada retorna pregunta de chunk DIFERENTE (aleatorio)
    
    TIPOS DE PREGUNTAS GENERADAS:
    - Definiciones: "¿Qué es X según el texto?"
    - Narrativa: "¿Qué ocurre cuando X hace Y?"
    - Personajes: "¿Cuál es el papel de X en esta situación?"
    - Conceptos: "Explica el concepto de X mencionado en el material"
    - Datos: "¿Qué información específica se presenta sobre X?"
    """
    if not chunks:
        return []
    
    num_questions = min(num_questions, len(chunks))
    questions = []
    
    # ✅ SIEMPRE aleatorio para que cada clic genere pregunta diferente
    selected_indices = random.sample(range(len(chunks)), num_questions)
    
    for idx in selected_indices:
        chunk = chunks[idx]
        
        # ✅ ANÁLISIS PROFUNDO del chunk
        content_type = detect_content_type(chunk)
        key_elements = extract_key_concepts(chunk, max_concepts=5)
        
        # ✅ GENERAR PREGUNTA INTELIGENTE según análisis
        question = _generate_smart_question(chunk, content_type, key_elements)
        
        questions.append({
            'question': question,
            'reference_chunk': chunk,
            'chunk_index': idx,
            'question_type': content_type,
            'concepts': key_elements
        })
    
    return questions

def _generate_smart_question(chunk: str, content_type: str, key_elements: List[str]) -> str:
    """
    Genera pregunta INTELIGENTE Y COMPLETA basada en análisis del chunk
    
    NO usa "..." ni fragmentos cortados
    Genera pregunta NATURAL que requiera entender el chunk
    """
    
    # Elemento principal del chunk
    main_element = key_elements[0] if key_elements else "el contenido de este fragmento"
    
    # ✅ ESTRATEGIA 1: Buscar DEFINICIONES en el chunk
    definition_match = re.search(
        r'(?:es|son|se define como|se entiende por|consiste en|significa)\s+([^.!?]{20,100})',
        chunk,
        re.IGNORECASE
    )
    if definition_match and content_type in ['concept', 'factual']:
        defined_term = main_element
        return f"¿Qué es {defined_term} según el material?"
    
    # ✅ ESTRATEGIA 2: Detectar ACCIONES/EVENTOS en narrativa
    if content_type == 'narrative':
        # Buscar verbos de acción
        action_verbs = ['examinó', 'descubrió', 'observó', 'encontró', 'decidió', 
                       'pensó', 'concluyó', 'investigó', 'reveló', 'demostró']
        
        for verb in action_verbs:
            if verb in chunk.lower():
                # Extraer sujeto (nombre propio antes del verbo)
                subject_match = re.search(
                    r'([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)\s+' + verb,
                    chunk
                )
                if subject_match:
                    subject = subject_match.group(1)
                    return f"¿Qué {verb} {subject} en esta parte del texto?"
                else:
                    return f"¿Qué se {verb} en este fragmento del material?"
        
        # Si no hay verbo específico, pregunta general sobre eventos
        if len(key_elements) >= 2:
            return f"¿Qué ocurre con {key_elements[0]} en relación a {key_elements[1]}?"
        else:
            return f"¿Qué sucede en la parte que habla sobre {main_element}?"
    
    # ✅ ESTRATEGIA 3: Preguntas sobre PERSONAJES
    if content_type == 'character':
        character_name = main_element
        
        # Buscar acciones del personaje
        character_actions = re.findall(
            rf'{re.escape(character_name)}\s+([\w]+)',
            chunk,
            re.IGNORECASE
        )
        
        if character_actions:
            return f"¿Cuál es el papel de {character_name} en esta situación?"
        else:
            return f"¿Qué información se presenta sobre {character_name}?"
    
    # ✅ ESTRATEGIA 4: Preguntas sobre DATOS/HECHOS
    if content_type == 'factual':
        # Buscar números, fechas, porcentajes
        has_numbers = re.search(r'\d+', chunk)
        if has_numbers:
            return f"¿Qué datos numéricos específicos se mencionan sobre {main_element}?"
        else:
            return f"¿Qué información factual se presenta acerca de {main_element}?"
    
    # ✅ ESTRATEGIA 5: Preguntas sobre FÓRMULAS
    if content_type == 'formula':
        return "¿Qué fórmula o expresión matemática se presenta y para qué sirve?"
    
    # ✅ ESTRATEGIA 6: Preguntas sobre CONCEPTOS (default)
    # Detectar si es explicación o descripción
    if any(word in chunk.lower() for word in ['porque', 'debido a', 'causa', 'razón', 'motivo']):
        return f"¿Por qué ocurre o se menciona {main_element} en el texto?"
    
    if any(word in chunk.lower() for word in ['cómo', 'manera', 'forma', 'método', 'proceso']):
        return f"¿Cómo se describe o explica {main_element} en el material?"
    
    # Pregunta general bien formulada
    if len(key_elements) >= 2:
        return f"Explica la relación entre {key_elements[0]} y {key_elements[1]} según el texto"
    else:
        return f"¿Qué se menciona específicamente sobre {main_element} en el material?"
