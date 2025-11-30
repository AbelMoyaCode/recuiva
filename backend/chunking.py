"""
Módulo para chunking y extracción de texto
Divide textos largos en fragmentos manejables para embeddings

Autor: Abel Jesús Moya Acosta
Fecha: 7 de octubre de 2025

✅ ACTUALIZADO: Sistema con Tesseract OCR REAL
   - PRIMERO intenta Tesseract OCR (lee imágenes, mejor calidad)
   - Si Tesseract falla, usa PyMuPDF o PyPDF2 como fallback
   - Normalización agresiva post-extracción
"""

import re
from typing import List, Tuple
from io import BytesIO
import os

# ═══════════════════════════════════════════════════════════════════════
# TESSERACT OCR - MEJOR CALIDAD (lee la imagen visual del PDF)
# ═══════════════════════════════════════════════════════════════════════
TESSERACT_AVAILABLE = False

# Rutas posibles de Tesseract según SO
TESSERACT_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",  # Windows
    "/usr/bin/tesseract",                              # Linux (Docker/Ubuntu)
    "/usr/local/bin/tesseract",                        # macOS Homebrew
]

try:
    import pytesseract
    from pdf2image import convert_from_bytes
    
    # Buscar Tesseract en las rutas conocidas
    tesseract_found = False
    for path in TESSERACT_PATHS:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            tesseract_found = True
            break
    
    # Si no se encontró en rutas conocidas, intentar usar el del PATH del sistema
    if not tesseract_found:
        # En Linux/Docker, tesseract suele estar en PATH
        import shutil
        tesseract_in_path = shutil.which("tesseract")
        if tesseract_in_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_in_path
            tesseract_found = True
    
    if tesseract_found:
        # Verificar que funciona
        version = pytesseract.get_tesseract_version()
        TESSERACT_AVAILABLE = True
        print(f"✅ Tesseract OCR v{version} disponible (MEJOR CALIDAD)")
    else:
        print(f"⚠️ Tesseract no encontrado en rutas conocidas ni en PATH")
        
except ImportError as e:
    print(f"⚠️ pytesseract o pdf2image no disponible: {e}")
except Exception as e:
    print(f"⚠️ Error inicializando Tesseract: {e}")

# ═══════════════════════════════════════════════════════════════════════
# FALLBACKS: PyMuPDF y PyPDF2
# ═══════════════════════════════════════════════════════════════════════
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
    print("✅ PyMuPDF disponible (fallback)")
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("⚠️ PyMuPDF no disponible")

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
    print("✅ PyPDF2 disponible (fallback)")
except ImportError:
    PYPDF2_AVAILABLE = False
    print("⚠️ PyPDF2 no disponible")

# ✅ Normalizador para limpiar chunks de errores OCR
try:
    from text_normalizer import normalize_text
    NORMALIZER_AVAILABLE = True
    print("✅ text_normalizer cargado - chunks serán normalizados")
except ImportError:
    NORMALIZER_AVAILABLE = False
    print("⚠️ text_normalizer no disponible")


def extract_with_tesseract(pdf_content: bytes) -> Tuple[str, int, int]:
    """
    Extrae texto usando Tesseract OCR REAL
    
    Convierte cada página del PDF a imagen y aplica OCR.
    MEJOR para PDFs con texto corrupto o escaneados.
    """
    print("🔍 Usando Tesseract OCR (mejor calidad)...")
    
    # Convertir PDF a imágenes (una por página)
    images = convert_from_bytes(pdf_content, dpi=300)
    total_pages = len(images)
    
    text = ""
    error_count = 0
    
    for i, image in enumerate(images):
        if i % 5 == 0:
            print(f"   OCR página {i+1}/{total_pages}...")
        
        # Aplicar OCR con idioma español
        page_text = pytesseract.image_to_string(image, lang='spa+eng')
        
        # Contar posibles errores
        error_count += len(re.findall(r'[a-z]{3,}[A-Z][a-z]{2,}', page_text))
        error_count += len(re.findall(r'\b\w{1,2}\s+\w{1,2}\s+\w{1,2}\b', page_text))
        
        text += page_text + "\n\n"
    
    print(f"   ✅ Tesseract completado: {len(text)} caracteres")
    return text.strip(), total_pages, error_count


def extract_with_pymupdf(pdf_content: bytes) -> Tuple[str, int, int]:
    """Extrae texto con PyMuPDF"""
    pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
    text = ""
    total_pages = len(pdf_document)
    error_count = 0
    
    for page in pdf_document:
        page_text = page.get_text("text")
        # Contar errores de OCR (palabras pegadas o fragmentadas)
        error_count += len(re.findall(r'[a-z]{3,}[A-Z][a-z]{2,}', page_text))  # palabrasPegadas
        error_count += len(re.findall(r'\b\w{1,2}\s+\w{1,2}\s+\w{1,2}\b', page_text))  # f ra g men tos
        text += page_text + "\n\n"
    
    pdf_document.close()
    return text.strip(), total_pages, error_count


def extract_with_pypdf2(pdf_content: bytes) -> Tuple[str, int, int]:
    """Extrae texto con PyPDF2"""
    pdf_file = BytesIO(pdf_content)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    total_pages = len(pdf_reader.pages)
    error_count = 0
    
    for page in pdf_reader.pages:
        page_text = page.extract_text() or ""
        error_count += len(re.findall(r'[a-z]{3,}[A-Z][a-z]{2,}', page_text))
        error_count += len(re.findall(r'\b\w{1,2}\s+\w{1,2}\s+\w{1,2}\b', page_text))
        text += page_text + "\n"
    
    return text.strip(), total_pages, error_count


def extract_text_from_pdf(pdf_content: bytes) -> tuple[str, int]:
    """
    Extrae texto de un archivo PDF usando el mejor método disponible
    
    ✅ ESTRATEGIA (en orden de preferencia):
    1. Tesseract OCR (MEJOR - lee imagen visual)
    2. PyMuPDF como fallback
    3. PyPDF2 como último recurso
    4. Aplica normalización agresiva al final
    
    Args:
        pdf_content: Contenido del PDF en bytes
        
    Returns:
        tuple: (texto extraído, número total de páginas)
    """
    results = []
    
    print(f"📖 Extrayendo texto del PDF...")
    
    # ═══════════════════════════════════════════════════════════════════════
    # OPCIÓN 1: Tesseract OCR (MEJOR CALIDAD)
    # ═══════════════════════════════════════════════════════════════════════
    if TESSERACT_AVAILABLE:
        try:
            text_tess, pages_tess, errors_tess = extract_with_tesseract(pdf_content)
            results.append(('Tesseract', text_tess, pages_tess, errors_tess))
            print(f"   Tesseract: {len(text_tess)} chars, {errors_tess} errores detectados")
        except Exception as e:
            print(f"   ❌ Tesseract falló: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # FALLBACKS: PyMuPDF y PyPDF2
    # ═══════════════════════════════════════════════════════════════════════
    if PYMUPDF_AVAILABLE:
        try:
            text_mupdf, pages_mupdf, errors_mupdf = extract_with_pymupdf(pdf_content)
            results.append(('PyMuPDF', text_mupdf, pages_mupdf, errors_mupdf))
            print(f"   PyMuPDF: {len(text_mupdf)} chars, {errors_mupdf} errores detectados")
        except Exception as e:
            print(f"   ❌ PyMuPDF falló: {e}")
    
    if PYPDF2_AVAILABLE:
        try:
            text_pypdf2, pages_pypdf2, errors_pypdf2 = extract_with_pypdf2(pdf_content)
            results.append(('PyPDF2', text_pypdf2, pages_pypdf2, errors_pypdf2))
            print(f"   PyPDF2: {len(text_pypdf2)} chars, {errors_pypdf2} errores detectados")
        except Exception as e:
            print(f"   ❌ PyPDF2 falló: {e}")
    
    if not results:
        raise Exception("No se pudo extraer texto del PDF con ningún método")
    
    # ═══════════════════════════════════════════════════════════════════════
    # ELEGIR EL MEJOR RESULTADO
    # Prioridad: Tesseract > menos errores > más texto
    # ═══════════════════════════════════════════════════════════════════════
    
    # Si Tesseract está disponible y funcionó, usarlo siempre
    tesseract_result = next((r for r in results if r[0] == 'Tesseract'), None)
    if tesseract_result and len(tesseract_result[1]) > 100:
        best = tesseract_result
        print(f"   ✅ Usando Tesseract OCR (mejor calidad)")
    else:
        # Fallback: elegir el método con menos errores
        best = min(results, key=lambda x: x[3])  # x[3] = error_count
        print(f"   ✅ Usando {best[0]} (menos errores: {best[3]})")
    best = min(results, key=lambda x: x[3])  # x[3] = error_count
    print(f"   ✅ Usando {best[0]} (menos errores: {best[3]})")
    
    text = best[1]
    total_pages = best[2]
    
    # Limpiar texto extraído
    text = aggressive_text_cleanup(text)
    
    print(f"✅ Texto extraído: {len(text)} caracteres de {total_pages} páginas")
    return text, total_pages


def aggressive_text_cleanup(text: str) -> str:
    """
    Limpieza AGRESIVA de texto extraído de PDF
    
    Corrige los errores más comunes de OCR/extracción:
    - Palabras pegadas: "serreconocido" → "ser reconocido"
    - Fragmentación: "histori a" → "historia"
    - Espacios en medio: "quienlohabí a" → "quien lo había"
    """
    if not text:
        return text
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 1: Separar palabras pegadas (camelCase accidental)
    # ═══════════════════════════════════════════════════════════════════════
    # "serreconocido" → "ser reconocido" (minúscula seguida de mayúscula)
    text = re.sub(r'([a-záéíóúñ])([A-ZÁÉÍÓÚÑ])', r'\1 \2', text)
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 2: Unir fragmentos sueltos (errores OCR típicos)
    # ═══════════════════════════════════════════════════════════════════════
    
    # Patrón: "palabra + espacio + 1-3 letras" → unir
    # Ej: "histori a" → "historia", "Henriet te" → "Henriette"
    for _ in range(5):  # Repetir varias veces para casos anidados
        text = re.sub(r'(\w{3,})\s+([a-záéíóúñ]{1,3})\b', r'\1\2', text, flags=re.IGNORECASE)
    
    # Patrón: "1-4 letras + espacio + palabra" → unir
    # Ej: "a doptar" → "adoptar"
    for _ in range(3):
        text = re.sub(r'\b([a-záéíóúñ]{1,4})\s+([a-záéíóúñ]{3,})', r'\1\2', text, flags=re.IGNORECASE)
    
    # Patrón: Mayúscula + espacio + resto
    # Ej: "V alorbe" → "Valorbe"
    text = re.sub(r'\b([A-ZÁÉÍÓÚÑ])\s+([a-záéíóúñ]{2,})', r'\1\2', text)
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 3: Separar palabras que deberían estar separadas
    # ═══════════════════════════════════════════════════════════════════════
    
    # Artículos pegados a palabras
    articles = ['el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'al', 'del']
    for art in articles:
        # "losdemás" → "los demás"
        text = re.sub(rf'\b({art})([a-záéíóúñ]{{3,}})', rf'\1 \2', text, flags=re.IGNORECASE)
    
    # Preposiciones pegadas
    preps = ['con', 'en', 'de', 'por', 'para', 'sin', 'sobre', 'entre', 'hasta', 'desde', 'como', 'que']
    for prep in preps:
        text = re.sub(rf'\b({prep})([a-záéíóúñ]{{3,}})', rf'\1 \2', text, flags=re.IGNORECASE)
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 4: Limpiar puntuación y espacios
    # ═══════════════════════════════════════════════════════════════════════
    
    # Unir palabras cortadas por guión al final de línea
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)
    
    # Múltiples espacios → uno solo
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Múltiples saltos de línea → máximo 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Espacios antes de puntuación
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    
    # Espacio después de puntuación si falta
    text = re.sub(r'([.,;:!?])([a-záéíóúñA-ZÁÉÍÓÚÑ¿¡])', r'\1 \2', text)
    
    # Remover líneas que solo tienen números (paginación)
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
    
    return text.strip()

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
