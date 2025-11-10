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

QUESTION_TEMPLATES = {
    'narrative': [
        # ✅ PREGUNTAS LITERALES que requieren citar el texto exacto
        '¿Qué dice exactamente el texto sobre {context}?',
        'Según el fragmento, ¿qué ocurre con {context}?',
        'Cita textualmente qué se menciona acerca de {context}',
        '¿Cómo describe el texto la situación de {context}?',
        'Reproduce lo que el texto dice sobre {context}'
    ],
    'character': [
        # ✅ PREGUNTAS ESPECÍFICAS sobre acciones/diálogos literales
        'Según el texto, ¿qué dice o hace {concept}?',
        '¿Qué acciones específicas realiza {concept} en este fragmento?',
        'Cita textualmente las palabras o acciones de {concept}',
        '¿Cómo se describe a {concept} en esta parte del texto?',
        'Reproduce el diálogo o las acciones de {concept}'
    ],
    'concept': [
        # ✅ PREGUNTAS que piden DEFINICIÓN LITERAL del texto
        '¿Cómo define el texto el concepto de {concept}?',
        'Según el material, ¿qué es {concept}?',
        'Cita la definición textual de {concept} que aparece en el fragmento',
        '¿Qué características de {concept} menciona específicamente el texto?',
        'Reproduce la explicación literal de {concept} del material'
    ],
    'formula': [
        # ✅ PREGUNTAS TÉCNICAS sobre ecuaciones específicas
        '¿Qué fórmula o ecuación aparece en este fragmento?',
        'Transcribe la expresión matemática que se presenta',
        '¿Para qué sirve la fórmula mencionada en el texto?',
        'Según el material, ¿cómo se aplica esta ecuación?'
    ],
    'factual': [
        # ✅ PREGUNTAS FACTUALES para contenido informativo
        '¿Qué información específica presenta este fragmento?',
        'Menciona los datos concretos que aparecen en el texto',
        '¿Qué hechos o detalles específicos se describen?',
        'Resume la información factual contenida en este fragmento'
    ]
}

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
    Genera preguntas ULTRA-ESPECÍFICAS extrayendo CITAS LITERALES del chunk
    
    ESTRATEGIA RAG:
    1. Toma fragmento TEXTUAL del chunk (50-100 caracteres)
    2. Genera pregunta que REQUIERA citar ese fragmento exacto
    3. La respuesta correcta DEBE contener palabras del chunk
    
    Esto garantiza:
    - Alta similitud semántica (pregunta y respuesta comparten chunk)
    - Preguntas contextualizadas al material REAL
    - Validación RAG precisa (embedding de respuesta cerca del chunk)
    """
    if not chunks:
        return []
    
    num_questions = min(num_questions, len(chunks))
    questions = []
    
    if strategy == 'random':
        selected_indices = random.sample(range(len(chunks)), num_questions)
    elif strategy == 'diverse':
        step = max(1, len(chunks) // num_questions)
        selected_indices = [i * step for i in range(num_questions)]
    else:  # sequential
        selected_indices = list(range(num_questions))
    
    for idx in selected_indices:
        chunk = chunks[idx]
        
        # ✅ ESTRATEGIA 1: Extraer CITA LITERAL del chunk (primera oración completa)
        first_sentence = chunk.split('.')[0].strip()
        if len(first_sentence) < 20:  # Si es muy corta, tomar más
            sentences = chunk.split('.')
            first_sentence = ('.'.join(sentences[:2])).strip()
        
        # Limitar longitud de la cita (50-150 caracteres)
        citation = first_sentence[:150] if len(first_sentence) > 150 else first_sentence
        
        # ✅ ESTRATEGIA 2: Identificar concepto/personaje/término clave
        content_type = detect_content_type(chunk)
        key_concepts = extract_key_concepts(chunk, max_concepts=3)
        main_concept = key_concepts[0] if key_concepts else "este fragmento"
        
        # ✅ ESTRATEGIA 3: Generar pregunta ESPECÍFICA que requiera el chunk
        question_templates = {
            'narrative': [
                f'Según el texto que dice "{citation[:80]}...", ¿qué sucede después?',
                f'El fragmento menciona "{citation[:80]}...". Explica qué ocurre en esta parte',
                f'¿Qué dice el texto sobre {main_concept}? (Cita el fragmento completo)',
            ],
            'character': [
                f'Según el texto: "{citation[:80]}...", ¿qué hace {main_concept}?',
                f'El material dice "{citation[:80]}...". ¿Cuál es el papel de {main_concept}?',
                f'Cita textualmente qué menciona el texto sobre {main_concept}',
            ],
            'concept': [
                f'El texto define: "{citation[:80]}...". Completa la definición',
                f'¿Cómo explica el material {main_concept}? (Cita el fragmento)',
                f'Según el texto que menciona "{citation[:80]}...", explica {main_concept}',
            ],
            'formula': [
                f'¿Qué fórmula o ecuación se presenta en el fragmento que dice "{citation[:60]}..."?',
                f'Transcribe y explica la expresión matemática del texto',
            ],
            'factual': [
                f'El texto menciona: "{citation[:80]}...". ¿Qué datos específicos presenta?',
                f'Según el fragmento "{citation[:80]}...", ¿qué información factual contiene?',
            ]
        }
        
        # Seleccionar template según tipo de contenido
        templates = question_templates.get(content_type, question_templates['concept'])
        question = random.choice(templates)
        
        questions.append({
            'question': question,
            'reference_chunk': chunk,  # ✅ Chunk completo para validación RAG
            'chunk_index': idx,
            'question_type': content_type,
            'concepts': key_concepts,
            'citation': citation  # ✅ Cita literal incluida en la pregunta
        })
    
    return questions
