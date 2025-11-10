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
    'definition': [
        '¿Qué es {concept}?',
        'Define {concept}',
        'Explica el concepto de {concept}'
    ],
    'process': [
        '¿Cómo funciona {concept}?',
        'Describe el proceso de {concept}'
    ],
    'formula': [
        '¿Para qué se utiliza esta fórmula?',
        'Explica los componentes de esta ecuación'
    ]
}

def detect_content_type(text: str) -> str:
    text_lower = text.lower()
    if re.search(r'[=+\-*/∫∑√]', text):
        return 'formula'
    if any(m in text_lower for m in ['es el', 'se define', 'definición']):
        return 'definition'
    if any(m in text_lower for m in ['pasos', 'proceso', 'procedimiento']):
        return 'process'
    return 'definition'

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
    if not chunks:
        return []
    num_questions = min(num_questions, len(chunks))
    questions = []
    if strategy == 'random':
        selected_indices = random.sample(range(len(chunks)), num_questions)
    elif strategy == 'diverse':
        step = len(chunks) // num_questions
        selected_indices = [i * step for i in range(num_questions)]
    else:
        selected_indices = list(range(num_questions))
    for idx in selected_indices:
        chunk = chunks[idx]
        content_type = detect_content_type(chunk)
        concepts = extract_key_concepts(chunk)
        if content_type == 'formula':
            question = random.choice(QUESTION_TEMPLATES['formula'])
        else:
            concept = concepts[0] if concepts else 'el tema principal'
            template = random.choice(QUESTION_TEMPLATES[content_type])
            question = template.format(concept=concept)
        questions.append({
            'question': question,
            'reference_chunk': chunk,
            'chunk_index': idx,
            'question_type': content_type,
            'concepts': concepts
        })
    return questions
