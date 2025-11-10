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
        '¿Qué sucede en este fragmento?',
        'Resume lo que ocurre en esta parte',
        'Describe los eventos narrados aquí'
    ],
    'character': [
        '¿Qué hace {concept} en esta parte?',
        'Describe el papel de {concept}',
        '¿Cómo actúa {concept} en este fragmento?'
    ],
    'concept': [
        'Explica el concepto de {concept} según el texto',
        '¿Qué es {concept} en este contexto?',
        'Define {concept} basándote en esta sección'
    ]
}

def detect_content_type(text: str) -> str:
    """Detecta el tipo de contenido del chunk"""
    text_lower = text.lower()
    
    # ✅ SOLO fórmulas REALES (ecuaciones matemáticas)
    if re.search(r'[=].*[\d+\-*/√∫∑]|[∫∑√]\d', text):
        return 'formula'
    
    # ✅ Detectar si es narrativa (común en novelas/historias)
    if any(w in text_lower for w in ['dijo', 'preguntó', 'respondió', 'pensó', 'miraba', 'caminaba']):
        return 'narrative'
    
    # ✅ Detectar nombres propios (personajes)
    if re.search(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b', text):
        return 'character'
    
    # Por defecto: concepto general
    return 'concept'

def extract_key_concepts(text: str, max_concepts: int = 3) -> List[str]:
    concepts = []
    patterns = [
        r'(?:es el|es la|es un|es una)\s+([^.,;]+)',
        r'concepto de\s+([^.,;]+)'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        concepts.extend([m.strip() for m in matches])
    capitalized = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\b', text)
    concepts.extend(capitalized)
    concepts = list(set([c.strip() for c in concepts if len(c.strip()) > 3]))
    if not concepts:
        words = re.findall(r'\b\w{5,}\b', text.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        concepts = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        concepts = [word for word, _ in concepts[:max_concepts]]
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
        
        # ✅ Generar pregunta COHERENTE según el tipo
        if content_type == 'narrative':
            # Para narrativa: pregunta general sobre el fragmento
            question = random.choice(QUESTION_TEMPLATES['narrative'])
        elif content_type == 'character' and concepts:
            # Para personajes: pregunta sobre el personaje principal
            template = random.choice(QUESTION_TEMPLATES['character'])
            question = template.format(concept=concepts[0])
        else:
            # Para conceptos: pregunta sobre concepto específico
            concept = concepts[0] if concepts else 'el tema de este fragmento'
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
