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
        '¿Qué sucede cuando {context}?',
        'Describe los eventos que ocurren en el fragmento que menciona {context}',
        '¿Qué acontecimientos se narran relacionados con {context}?',
        'Resume la situación cuando se habla de {context}',
        '¿Cómo se desarrolla la escena donde aparece {context}?'
    ],
    'character': [
        '¿Qué hace {concept} y por qué es importante?',
        'Describe las acciones de {concept} en este contexto',
        '¿Cuál es el papel de {concept} en esta situación?',
        '¿Cómo actúa {concept} y qué revela esto?',
        'Analiza el comportamiento de {concept} en este fragmento'
    ],
    'concept': [
        'Explica {concept} según lo descrito en el material',
        '¿Qué significa {concept} en este contexto específico?',
        'Define {concept} basándote en la información del texto',
        '¿Cómo se relaciona {concept} con el tema principal?',
        'Desarrolla el concepto de {concept} usando el material'
    ],
    'formula': [
        'Explica para qué se utiliza esta fórmula matemática',
        '¿Qué representa cada elemento en esta ecuación?',
        'Describe cómo se aplica esta fórmula',
        '¿En qué contexto se usa esta expresión matemática?'
    ]
}

def detect_content_type(text: str) -> str:
    """Detecta el tipo de contenido del chunk con análisis PROFUNDO del texto"""
    text_lower = text.lower()
    
    # Contar diferentes indicadores
    narrative_score = 0
    academic_score = 0
    
    # Indicadores de narrativa (novelas, cuentos)
    narrative_verbs = ['dijo', 'preguntó', 'respondió', 'pensó', 'miraba', 'caminaba', 
                      'observaba', 'susurró', 'gritó', 'murmuró', 'recordaba', 'sentía']
    narrative_score += sum(1 for verb in narrative_verbs if verb in text_lower)
    
    # Indicadores académicos (ensayos, papers, libros técnicos)
    academic_terms = ['concepto', 'definición', 'teoría', 'análisis', 'método', 
                     'investigación', 'estudio', 'resultado', 'conclusión', 'hipótesis']
    academic_score += sum(1 for term in academic_terms if term in text_lower)
    
    # Detectar diálogos (comillas)
    if '"' in text or '«' in text or '—' in text:
        narrative_score += 2
    
    # Decisión basada en scores
    if narrative_score > academic_score and narrative_score >= 2:
        return 'narrative'
    
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
    """Extrae conceptos clave y contexto del chunk de manera INTELIGENTE"""
    concepts = []
    
    # 1. Buscar definiciones explícitas
    definition_patterns = [
        r'(?:es el|es la|es un|es una|se define como|se entiende por)\s+([^.,;]+)',
        r'concepto de\s+([^.,;]+)',
        r'(?:llamado|conocido como|denominado)\s+([^.,;]+)'
    ]
    for pattern in definition_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        concepts.extend([m.strip() for m in matches])
    
    # 2. Nombres propios (personajes, lugares, organizaciones)
    proper_names = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b', text)
    concepts.extend([name for name in proper_names if len(name) > 3])
    
    # 3. Sustantivos clave (palabras capitalizadas o repetidas)
    capitalized = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{3,}\b', text)
    concepts.extend(capitalized)
    
    # 4. Términos técnicos o palabras importantes por frecuencia
    words = re.findall(r'\b[a-záéíóúñ]{5,}\b', text.lower())
    word_freq = {}
    for word in words:
        # Filtrar palabras comunes
        if word not in ['sobre', 'cuando', 'donde', 'porque', 'aunque', 'mientras', 
                       'después', 'antes', 'siempre', 'nunca', 'también', 'además']:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Tomar las 3 palabras más frecuentes
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
    concepts.extend([word for word, _ in top_words])
    
    # Limpiar y deduplicar
    concepts = list(set([c.strip() for c in concepts if len(c.strip()) > 3]))
    
    # Si no hay conceptos, extraer fragmento de contexto
    if not concepts:
        # Tomar las primeras 4-6 palabras como contexto
        first_words = ' '.join(text.split()[:6])
        concepts = [first_words[:50]]
    
    return concepts[:max_concepts]

def generate_questions_dict(chunks: List[str], num_questions: int = 5, strategy: str = 'random') -> List[Dict]:
    """Genera preguntas inteligentes basadas en el contenido real de los chunks"""
    if not chunks:
        return []
    
    num_questions = min(num_questions, len(chunks))
    questions = []
    
    if strategy == 'random':
        selected_indices = random.sample(range(len(chunks)), num_questions)
    elif strategy == 'diverse':
        step = len(chunks) // num_questions
        selected_indices = [i * step for i in range(num_questions)]
    else:  # sequential
        selected_indices = list(range(num_questions))
    
    for idx in selected_indices:
        chunk = chunks[idx]
        
        # Detectar tipo de contenido
        content_type = detect_content_type(chunk)
        
        # Extraer conceptos clave
        concepts = extract_key_concepts(chunk)
        
        # ✅ Generar pregunta INTELIGENTE basada en el contenido REAL del chunk
        if content_type == 'narrative':
            # Para narrativa: usar contexto específico del fragmento
            context = concepts[0] if concepts else 'esta parte de la historia'
            template = random.choice(QUESTION_TEMPLATES['narrative'])
            question = template.format(context=context)
        
        elif content_type == 'character' and concepts:
            # Para personajes: pregunta sobre el personaje mencionado
            character = concepts[0]  # Primer nombre propio encontrado
            template = random.choice(QUESTION_TEMPLATES['character'])
            question = template.format(concept=character)
        
        elif content_type == 'formula':
            # Para fórmulas: pregunta técnica sobre la ecuación
            question = random.choice(QUESTION_TEMPLATES['formula'])
        
        else:
            # Para conceptos: usar concepto ESPECÍFICO del chunk
            if concepts:
                concept = concepts[0]
            else:
                # Extraer fragmento del inicio del chunk como concepto
                concept = ' '.join(chunk.split()[:5])
            
            template = random.choice(QUESTION_TEMPLATES['concept'])
            question = template.format(concept=concept)
        
        questions.append({
            'question': question,
            'reference_chunk': chunk,
            'chunk_index': idx,
            'question_type': content_type,
            'concepts': concepts
        })
    
    return questions
