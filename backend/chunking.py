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

# ✅ NUEVO: Importar normalizador para limpiar chunks de errores OCR
try:
    from text_normalizer import normalize_text
    NORMALIZER_AVAILABLE = True
    print("✅ text_normalizer cargado - chunks serán normalizados")
except ImportError:
    NORMALIZER_AVAILABLE = False
    print("⚠️ text_normalizer no disponible, chunks pueden tener errores OCR")

def extract_text_from_pdf(pdf_content: bytes) -> tuple[str, int]:
    """
    Extrae texto de un archivo PDF
    
    Args:
        pdf_content: Contenido del PDF en bytes
        
    Returns:
        tuple: (texto extraído, número total de páginas)
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
        
        print(f"✅ Texto extraído: {len(text)} caracteres de {total_pages} páginas")
        return text.strip(), total_pages
        
    except Exception as e:
        raise Exception(f"Error extrayendo texto del PDF: {str(e)}")

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Divide el texto en chunks con overlap para mantener contexto
    
    OPTIMIZADO PARA PDFs DE 25-100+ PÁGINAS:
    - chunk_size=1000: Contexto completo (5-7 oraciones)
    - overlap=200: Mayor continuidad entre chunks
    
    Args:
        text: Texto a dividir
        chunk_size: Tamaño aproximado de cada chunk (en caracteres) [default: 1000]
        overlap: Cantidad de caracteres que se solapan entre chunks [default: 200]
        
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
    
    # ✅ NUEVO: Normalizar todos los chunks para corregir errores OCR
    if NORMALIZER_AVAILABLE:
        chunks = [normalize_text(chunk) for chunk in chunks]
        print(f"✅ Chunks normalizados: errores OCR corregidos")
    
    return chunks

def clean_text(text: str) -> str:
    """
    Limpia el texto removiendo caracteres innecesarios
    
    NOTA IMPORTANTE: 
    - Si el PDF tiene OCR defectuoso (espacios en medio de palabras), 
      este filtro NO lo arreglará automáticamente
    - Para PDFs con OCR corrupto, ejecutar manualmente el script SQL:
      database/fix_ocr_chunks_CORRECTO.sql
    
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

def get_text_stats(text: str, real_pages: int = None) -> dict:
    """
    Obtiene estadísticas del texto
    
    Args:
        text: Texto a analizar
        real_pages: Número real de páginas del PDF (si está disponible)
        
    Returns:
        dict: Diccionario con estadísticas
    """
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    paragraphs = text.split('\n\n')
    
    # Calcular páginas estimadas basándose en caracteres (1300 chars/página es más realista)
    estimated_pages = len(text) // 1300 if not real_pages else real_pages
    
    return {
        "characters": len(text),
        "characters_no_spaces": len(text.replace(' ', '')),
        "words": len(words),
        "sentences": len([s for s in sentences if s.strip()]),
        "paragraphs": len([p for p in paragraphs if p.strip()]),
        "avg_word_length": round(sum(len(word) for word in words) / len(words), 2) if words else 0,
        "avg_sentence_length": round(len(words) / len([s for s in sentences if s.strip()]), 2) if sentences else 0,
        "estimated_pages": estimated_pages,
        "real_pages": real_pages if real_pages else estimated_pages  # Devolver el conteo real si existe
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
    
    # Agregar el último chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # ✅ NUEVO: Normalizar todos los chunks para corregir errores OCR
    if NORMALIZER_AVAILABLE:
        print(f"🧹 Normalizando {len(chunks)} chunks (corrigiendo errores OCR)...")
        chunks = [normalize_text(chunk) for chunk in chunks]
        print(f"✅ Chunks normalizados correctamente")
    
    return chunks


def adaptive_chunking(text: str, total_pages: int) -> List[str]:
    """
    🎯 CHUNKING ADAPTATIVO INTELIGENTE según tamaño del PDF
    
    Ajusta automáticamente los parámetros de chunking para mantener
    el equilibrio entre precisión y eficiencia según el tamaño del documento.
    
    ESTRATEGIA POR TAMAÑO:
    📘 PDFs pequeños (1-50 págs):    chunks detallados (80-180 palabras)
    📗 PDFs medianos (51-300 págs):  chunks moderados (150-350 palabras)
    📕 PDFs grandes (301-1000 págs): chunks amplios (250-600 palabras)
    📚 PDFs masivos (1000+ págs):    chunks extensos (400-1000 palabras)
    
    BENEFICIOS:
    ✅ Reduce ruido en PDFs grandes (menos chunks = mejor retrieval)
    ✅ Mantiene detalle en PDFs pequeños
    ✅ Optimiza tiempo de procesamiento
    ✅ Mejor balance precisión/escalabilidad
    
    Args:
        text: Texto completo a dividir
        total_pages: Número total de páginas del PDF
        
    Returns:
        List[str]: Chunks optimizados según tamaño del documento
    """
    print(f"\n🎯 CHUNKING ADAPTATIVO para PDF de {total_pages} páginas")
    
    if total_pages <= 50:
        # PDFs pequeños: máximo detalle
        print("   📘 Estrategia: DETALLADA (80-180 palabras/chunk)")
        return semantic_chunking(text, min_words=80, max_words=180, overlap_words=20)
    
    elif total_pages <= 300:
        # PDFs medianos: balance detalle/eficiencia
        print("   📗 Estrategia: MODERADA (150-350 palabras/chunk)")
        return semantic_chunking(text, min_words=150, max_words=350, overlap_words=30)
    
    elif total_pages <= 1000:
        # PDFs grandes: priorizar coherencia
        print("   📕 Estrategia: AMPLIA (250-600 palabras/chunk)")
        return semantic_chunking(text, min_words=250, max_words=600, overlap_words=50)
    
    else:
        # PDFs masivos: reducir ruido al máximo
        print("   📚 Estrategia: EXTENSIVA (400-1000 palabras/chunk)")
        return semantic_chunking(text, min_words=400, max_words=1000, overlap_words=80)

def semantic_chunking(text: str, min_words: int = 150, max_words: int = 400, overlap_words: int = 15) -> List[str]:
    """
    🧠 CHUNKING SEMÁNTICO INTELIGENTE - BASE
    
    Divide texto por PÁRRAFOS Y ORACIONES (no caracteres arbitrarios).
    Se adapta al contenido respetando límites semánticos.
    
    CARACTERÍSTICAS:
    ✅ División por párrafos (\n\n) - respeta estructura del documento
    ✅ Subdivisión por oraciones si párrafo es muy largo
    ✅ Context anchors: 15 palabras de overlap entre chunks
    ✅ Rango adaptativo: 150-400 palabras (no caracteres fijos)
    ✅ Respeta límites de ideas completas
    
    EJEMPLO DE RESULTADO:
    - Chunk antiguo (1000 chars): "...una amiga de convento que se enemis..." (cortado)
    - Chunk semántico (250 palabras): "En el edificio vivía una amiga de convento que se enemistó 
      con su familia. Prestaba servicios a la condesa y conocía sus rutinas. Siempre se hablaba 
      delante de ella. Su ventana de cocina daba exactamente al mismo patio interior..." (completo)
    
    Args:
        text: Texto completo a dividir
        min_words: Mínimo de palabras por chunk (default: 150)
        max_words: Máximo de palabras por chunk (default: 400)
        overlap_words: Palabras de overlap entre chunks (default: 15)
        
    Returns:
        List[str]: Chunks semánticos con context anchors
    """
    text = clean_text(text)
    
    # 1. DIVIDIR POR PÁRRAFOS (respeta estructura del documento)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    current_chunk = []
    word_count = 0
    
    print(f"\n🧠 INICIANDO CHUNKING SEMÁNTICO...")
    print(f"   Rango: {min_words}-{max_words} palabras por chunk")
    print(f"   Context anchors: {overlap_words} palabras de overlap")
    
    for paragraph in paragraphs:
        paragraph_words = paragraph.split()
        paragraph_word_count = len(paragraph_words)
        
        # Si el párrafo es muy largo (> max_words), dividirlo por oraciones
        if paragraph_word_count > max_words:
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            
            for sentence in sentences:
                sentence_words = sentence.split()
                sentence_word_count = len(sentence_words)
                
                # Si agregar esta oración supera max_words, guardar chunk actual
                if word_count + sentence_word_count > max_words and word_count >= min_words:
                    # Guardar chunk actual
                    chunk_text = ' '.join(current_chunk)
                    chunks.append(chunk_text)
                    
                    # Context anchor: últimas N palabras del chunk anterior
                    overlap = current_chunk[-overlap_words:] if len(current_chunk) >= overlap_words else current_chunk
                    current_chunk = overlap + sentence_words
                    word_count = len(current_chunk)
                else:
                    current_chunk.extend(sentence_words)
                    word_count += sentence_word_count
        else:
            # Párrafo completo cabe en el chunk actual
            if word_count + paragraph_word_count > max_words and word_count >= min_words:
                # Guardar chunk actual
                chunk_text = ' '.join(current_chunk)
                chunks.append(chunk_text)
                
                # Context anchor
                overlap = current_chunk[-overlap_words:] if len(current_chunk) >= overlap_words else current_chunk
                current_chunk = overlap + paragraph_words
                word_count = len(current_chunk)
            else:
                # Agregar párrafo al chunk actual
                if current_chunk:
                    current_chunk.append('\n\n')
                current_chunk.extend(paragraph_words)
                word_count += paragraph_word_count
    
    # Agregar último chunk
    if current_chunk:
        chunk_text = ' '.join(current_chunk)
        chunks.append(chunk_text)
    
    # Normalizar chunks
    if NORMALIZER_AVAILABLE:
        print(f"🧹 Normalizando {len(chunks)} chunks semánticos...")
        chunks = [normalize_text(chunk) for chunk in chunks]
    
    # Estadísticas
    chunk_lengths = [len(chunk.split()) for chunk in chunks]
    avg_words = sum(chunk_lengths) / len(chunks) if chunks else 0
    
    print(f"\n✅ CHUNKING SEMÁNTICO COMPLETADO:")
    print(f"   Total chunks: {len(chunks)}")
    print(f"   Promedio palabras/chunk: {avg_words:.1f}")
    print(f"   Rango: {min(chunk_lengths)}-{max(chunk_lengths)} palabras")
    print(f"   Context anchors: {overlap_words} palabras de overlap\n")
    
    return chunks
