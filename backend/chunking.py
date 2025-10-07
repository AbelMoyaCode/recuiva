"""
Módulo para chunking y extracción de texto
Divide textos largos en fragmentos manejables para embeddings

Autor: Abel Jesús Moya Acosta
Fecha: 7 de octubre de 2025
"""

import re
from typing import List
import PyPDF2
from io import BytesIO

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extrae texto de un archivo PDF
    
    Args:
        pdf_content: Contenido del PDF en bytes
        
    Returns:
        str: Texto extraído del PDF
    """
    try:
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        total_pages = len(pdf_reader.pages)
        
        print(f"📖 Extrayendo texto de {total_pages} páginas...")
        
        for i, page in enumerate(pdf_reader.pages):
            if i % 10 == 0:
                print(f"   Procesando página {i+1}/{total_pages}...")
            text += page.extract_text() + "\n"
        
        print(f"✅ Texto extraído: {len(text)} caracteres")
        return text.strip()
        
    except Exception as e:
        raise Exception(f"Error extrayendo texto del PDF: {str(e)}")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Divide el texto en chunks con overlap para mantener contexto
    
    Args:
        text: Texto a dividir
        chunk_size: Tamaño aproximado de cada chunk (en caracteres)
        overlap: Cantidad de caracteres que se solapan entre chunks
        
    Returns:
        List[str]: Lista de chunks de texto
    """
    # Limpiar el texto
    text = clean_text(text)
    
    # Dividir por oraciones
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Si agregar esta oración excede el tamaño, guardar el chunk actual
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            
            # Comenzar nuevo chunk con overlap
            words = current_chunk.split()
            overlap_words = min(overlap, len(words))
            overlap_text = ' '.join(words[-overlap_words:]) if overlap_words > 0 else ""
            current_chunk = overlap_text + " " + sentence if overlap_text else sentence
        else:
            current_chunk += " " + sentence if current_chunk else sentence
    
    # Agregar el último chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def clean_text(text: str) -> str:
    """
    Limpia el texto removiendo caracteres innecesarios
    
    Args:
        text: Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
    # Remover múltiples espacios
    text = re.sub(r'\s+', ' ', text)
    
    # Remover caracteres especiales pero mantener puntuación básica
    text = re.sub(r'[^\w\s.,;:!?¿¡áéíóúÁÉÍÓÚñÑ()"\'-]', '', text)
    
    # Remover líneas vacías múltiples
    text = re.sub(r'\n\s*\n', '\n', text)
    
    return text.strip()

def get_text_stats(text: str) -> dict:
    """
    Obtiene estadísticas del texto
    
    Args:
        text: Texto a analizar
        
    Returns:
        dict: Diccionario con estadísticas
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    paragraphs = text.split('\n\n')
    
    return {
        "characters": len(text),
        "characters_no_spaces": len(text.replace(' ', '')),
        "words": len(words),
        "sentences": len([s for s in sentences if s.strip()]),
        "paragraphs": len([p for p in paragraphs if p.strip()]),
        "avg_word_length": round(sum(len(word) for word in words) / len(words), 2) if words else 0,
        "avg_sentence_length": round(len(words) / len([s for s in sentences if s.strip()]), 2) if sentences else 0,
        "estimated_pages": len(text) // 2500  # Aprox 2500 caracteres por página
    }

def chunk_by_paragraphs(text: str, max_chunk_size: int = 1000) -> List[str]:
    """
    Divide el texto en chunks basándose en párrafos
    
    Args:
        text: Texto a dividir
        max_chunk_size: Tamaño máximo de cada chunk
        
    Returns:
        List[str]: Lista de chunks
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            current_chunk += "\n\n" + paragraph if current_chunk else paragraph
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def smart_chunk(text: str, target_size: int = 500, min_size: int = 100) -> List[str]:
    """
    Chunking inteligente que respeta límites de oraciones y párrafos
    
    Args:
        text: Texto a dividir
        target_size: Tamaño objetivo de cada chunk
        min_size: Tamaño mínimo aceptable
        
    Returns:
        List[str]: Lista de chunks optimizados
    """
    text = clean_text(text)
    
    # Dividir por párrafos primero
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # Si el párrafo es muy grande, dividirlo por oraciones
        if len(paragraph) > target_size:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            
            for sentence in sentences:
                if len(current_chunk) + len(sentence) > target_size and len(current_chunk) >= min_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += " " + sentence if current_chunk else sentence
        else:
            # Agregar párrafo completo
            if len(current_chunk) + len(paragraph) > target_size and len(current_chunk) >= min_size:
                chunks.append(current_chunk.strip())
                current_chunk = paragraph
            else:
                current_chunk += "\n\n" + paragraph if current_chunk else paragraph
    
    # Agregar último chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks
