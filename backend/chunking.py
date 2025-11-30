"""
Módulo para chunking y extracción de texto
Divide textos largos en fragmentos manejables para embeddings

Autor: Abel Jesús Moya Acosta
Fecha: 7 de octubre de 2025

✅ ACTUALIZADO: Sistema con pdftotext + ocrmypdf + Tesseract OCR
   - PRIMERO: pdftotext (extrae texto embebido, INSTANTÁNEO)
   - SEGUNDO: ocrmypdf --force-ocr (si pdftotext falla/corrupto)
   - TERCERO: Tesseract OCR directo como fallback
   - CUARTO: PyMuPDF/PyPDF2 como último recurso
   - Normalización agresiva post-extracción
"""

import re
from typing import List, Tuple
from io import BytesIO
import os
import subprocess
import tempfile
import shutil

# ═══════════════════════════════════════════════════════════════════════
# PDFTOTEXT - PRIMERA OPCIÓN (INSTANTÁNEO, extrae texto embebido)
# ═══════════════════════════════════════════════════════════════════════
PDFTOTEXT_AVAILABLE = False

try:
    # pdftotext -v escribe la versión en stderr, no stdout
    result = subprocess.run(['pdftotext', '-v'], capture_output=True, text=True)
    # Combinar stdout y stderr para buscar la versión
    output = (result.stdout + result.stderr).lower()
    if 'pdftotext' in output or 'poppler' in output or result.returncode == 0:
        PDFTOTEXT_AVAILABLE = True
        version_info = (result.stdout + result.stderr).strip().split('\n')[0]
        print(f"✅ pdftotext disponible: {version_info} (INSTANTÁNEO - primera opción)")
except Exception as e:
    print(f"⚠️ pdftotext no disponible: {e}")

# ═══════════════════════════════════════════════════════════════════════
# OCRMYPDF - SEGUNDA OPCIÓN PARA PDFs CORRUPTOS
# ═══════════════════════════════════════════════════════════════════════
OCRMYPDF_AVAILABLE = False

try:
    result = subprocess.run(['ocrmypdf', '--version'], capture_output=True, text=True)
    if result.returncode == 0:
        OCRMYPDF_AVAILABLE = True
        print(f"✅ ocrmypdf disponible: {result.stdout.strip()}")
except:
    print("⚠️ ocrmypdf no disponible")

# ═══════════════════════════════════════════════════════════════════════
# TESSERACT OCR - FALLBACK
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


def extract_with_pdftotext(pdf_content: bytes) -> tuple[str, int]:
    """
    Extrae texto de un PDF usando pdftotext (poppler-utils)
    
    VENTAJAS:
    - INSTANTÁNEO (no hace OCR)
    - Extrae texto embebido real del PDF
    - Mantiene layout y espaciado correcto
    
    Args:
        pdf_content: Contenido del PDF en bytes
        
    Returns:
        tuple: (texto extraído, número de páginas)
    """
    if not PDFTOTEXT_AVAILABLE:
        return "", 0
    
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, 'input.pdf')
        output_path = os.path.join(temp_dir, 'output.txt')
        
        # Guardar PDF
        with open(input_path, 'wb') as f:
            f.write(pdf_content)
        
        # Ejecutar pdftotext con layout para mantener formato
        result = subprocess.run([
            'pdftotext',
            '-layout',      # Mantiene layout original
            '-enc', 'UTF-8', # Codificación UTF-8
            input_path,
            output_path
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            print(f"   ⚠️ pdftotext error: {result.stderr}")
            return "", 0
        
        # Leer texto extraído
        with open(output_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # Contar páginas con PyMuPDF o estimación
        num_pages = 1
        if PYMUPDF_AVAILABLE:
            try:
                import fitz
                pdf_doc = fitz.open(stream=pdf_content, filetype="pdf")
                num_pages = len(pdf_doc)
                pdf_doc.close()
            except:
                # Estimar páginas por caracteres (aprox 2000 chars/página)
                num_pages = max(1, len(text) // 2000)
        
        return text.strip(), num_pages
        
    except subprocess.TimeoutExpired:
        print("   ⚠️ pdftotext timeout")
        return "", 0
    except Exception as e:
        print(f"   ⚠️ pdftotext error: {e}")
        return "", 0
    finally:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


def preprocess_pdf_with_ocrmypdf(pdf_content: bytes) -> bytes:
    """
    Pre-procesa un PDF con ocrmypdf para reparar texto corrupto
    
    ocrmypdf --force-ocr:
    1. Renderiza cada página como imagen de alta calidad
    2. Aplica Tesseract OCR de forma optimizada
    3. Genera un PDF nuevo con texto limpio embebido
    
    Args:
        pdf_content: Contenido del PDF original en bytes
        
    Returns:
        bytes: PDF procesado con texto OCR limpio
    """
    if not OCRMYPDF_AVAILABLE:
        print("   ⚠️ ocrmypdf no disponible, retornando PDF original")
        return pdf_content
    
    import gc
    temp_dir = None
    
    try:
        # Crear archivos temporales
        temp_dir = tempfile.mkdtemp()
        input_path = os.path.join(temp_dir, 'input.pdf')
        output_path = os.path.join(temp_dir, 'output.pdf')
        
        # Guardar PDF original
        with open(input_path, 'wb') as f:
            f.write(pdf_content)
        
        print("   🔧 Procesando PDF con ocrmypdf --force-ocr...")
        
        # Ejecutar ocrmypdf con force-ocr
        result = subprocess.run([
            'ocrmypdf',
            '--force-ocr',           # Forzar OCR incluso si ya tiene texto
            '--language', 'spa+eng', # Español + Inglés
            '--deskew',              # Corregir inclinación
            '--clean',               # Limpiar imagen
            '--optimize', '1',       # Optimización ligera
            '--output-type', 'pdf',
            '--jobs', '2',           # Usar 2 cores (VPS pequeño)
            input_path,
            output_path
        ], capture_output=True, text=True, timeout=300)  # 5 min timeout
        
        if result.returncode == 0:
            print("   ✅ ocrmypdf completado exitosamente")
            with open(output_path, 'rb') as f:
                processed_pdf = f.read()
            return processed_pdf
        else:
            print(f"   ⚠️ ocrmypdf falló: {result.stderr[:200]}")
            return pdf_content
            
    except subprocess.TimeoutExpired:
        print("   ⚠️ ocrmypdf timeout (>5 min), usando PDF original")
        return pdf_content
    except Exception as e:
        print(f"   ❌ Error en ocrmypdf: {e}")
        return pdf_content
    finally:
        # Limpiar archivos temporales
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        gc.collect()


def extract_with_tesseract(pdf_content: bytes) -> Tuple[str, int, int]:
    """
    Extrae texto usando Tesseract OCR REAL
    
    ✅ OPTIMIZADO PARA MEMORIA BAJA (2GB VPS):
    - Procesa UNA página a la vez (no todas a memoria)
    - DPI reducido a 150 (suficiente para texto, menos RAM)
    - Libera memoria después de cada página
    - Para PDFs muy grandes, usa fallback automático
    
    MEJOR para PDFs con texto corrupto o escaneados.
    """
    import gc
    
    print("🔍 Usando Tesseract OCR (mejor calidad)...")
    
    # Primero, obtener el número total de páginas sin cargar imágenes
    try:
        # Usar PyMuPDF para contar páginas (muy eficiente en memoria)
        if PYMUPDF_AVAILABLE:
            import fitz
            pdf_doc = fitz.open(stream=pdf_content, filetype="pdf")
            total_pages = len(pdf_doc)
            pdf_doc.close()
        else:
            # Fallback: convertir solo primera página para contar
            first_page = convert_from_bytes(pdf_content, dpi=72, first_page=1, last_page=1)
            total_pages = len(convert_from_bytes(pdf_content, dpi=72))
            del first_page
            gc.collect()
    except Exception as e:
        print(f"   ⚠️ Error contando páginas: {e}")
        total_pages = 0
    
    # Si el PDF es muy grande (>100 páginas), usar DPI más bajo o fallback
    # ✅ MEJORADO: DPI más alto para mejor calidad de OCR
    if total_pages > 100:
        print(f"   ⚠️ PDF muy grande ({total_pages} págs), usando DPI 150 para ahorrar memoria")
        dpi = 150
    elif total_pages > 50:
        print(f"   📄 PDF mediano ({total_pages} págs), usando DPI 200")
        dpi = 200
    else:
        print(f"   📄 PDF pequeño ({total_pages} págs), usando DPI 300 (alta calidad)")
        dpi = 300
    
    text = ""
    error_count = 0
    processed_pages = 0
    
    # Procesar página por página para ahorrar memoria
    try:
        for page_num in range(1, total_pages + 1):
            try:
                # Convertir SOLO esta página a imagen
                images = convert_from_bytes(
                    pdf_content, 
                    dpi=dpi, 
                    first_page=page_num, 
                    last_page=page_num,
                    grayscale=True,  # Menos memoria
                    thread_count=1   # Menos memoria
                )
                
                if images:
                    # Aplicar OCR con idioma español
                    page_text = pytesseract.image_to_string(images[0], lang='spa+eng')
                    
                    # Contar posibles errores
                    error_count += len(re.findall(r'[a-z]{3,}[A-Z][a-z]{2,}', page_text))
                    error_count += len(re.findall(r'\b\w{1,2}\s+\w{1,2}\s+\w{1,2}\b', page_text))
                    
                    text += page_text + "\n\n"
                    processed_pages += 1
                    
                    # Liberar memoria inmediatamente
                    del images
                    del page_text
                
                # Log de progreso cada 10 páginas
                if page_num % 10 == 0:
                    print(f"   OCR página {page_num}/{total_pages}...")
                    gc.collect()  # Forzar limpieza de memoria
                    
            except Exception as page_error:
                print(f"   ⚠️ Error en página {page_num}: {page_error}")
                continue
                
    except Exception as e:
        print(f"   ❌ Error general en Tesseract: {e}")
        if processed_pages == 0:
            raise e
    
    # Limpieza final
    gc.collect()
    
    print(f"   ✅ Tesseract completado: {len(text)} caracteres de {processed_pages} páginas")
    return text.strip(), processed_pages if processed_pages > 0 else total_pages, error_count


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


def detect_corrupted_text(text: str) -> Tuple[bool, str]:
    """
    Detecta si el texto extraído está corrupto (encoding incorrecto, fuentes propietarias, etc.)
    
    Args:
        text: Texto extraído del PDF
        
    Returns:
        Tuple[bool, str]: (está_corrupto, razón)
    """
    if not text or len(text) < 100:
        return True, "Texto muy corto o vacío"
    
    # 1. Detectar caracteres de control o no imprimibles
    control_chars = len(re.findall(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', text))
    if control_chars > len(text) * 0.01:  # Más de 1% caracteres de control
        return True, f"Demasiados caracteres de control ({control_chars})"
    
    # 2. Detectar secuencias de símbolos que indican encoding incorrecto
    # Ej: "→", "←", "↔", "⇒", etc. que aparecen en medio de palabras
    arrow_in_words = len(re.findall(r'\w[→←↔⇒⇐↑↓]\w', text))
    if arrow_in_words > 5:
        return True, f"Símbolos de flecha en palabras ({arrow_in_words})"
    
    # 3. Detectar ratio bajo de vocales (texto normal tiene ~40% vocales en español)
    vowels = len(re.findall(r'[aeiouáéíóúAEIOUÁÉÍÓÚ]', text))
    letters = len(re.findall(r'[a-záéíóúñA-ZÁÉÍÓÚÑ]', text))
    if letters > 0:
        vowel_ratio = vowels / letters
        if vowel_ratio < 0.25:  # Menos de 25% vocales = probablemente corrupto
            return True, f"Ratio de vocales muy bajo ({vowel_ratio:.1%})"
    
    # 4. Detectar palabras con mezcla inusual de mayúsculas/minúsculas
    # Ej: "grofeso", "entradJ", "aToda"
    weird_case = len(re.findall(r'\b[a-z]+[A-Z][a-z]*\b', text))
    if weird_case > len(text.split()) * 0.05:  # Más de 5% de palabras
        return True, f"Mezcla inusual de mayúsculas ({weird_case} palabras)"
    
    # 5. Detectar secuencias de caracteres raros consecutivos
    # Ej: ")El", "J→", etc.
    weird_sequences = len(re.findall(r'[)}\]>][A-Za-z]|[A-Za-z][(\[{<]', text))
    if weird_sequences > 20:
        return True, f"Secuencias de caracteres raros ({weird_sequences})"
    
    # 6. Detectar palabras que no parecen español/inglés
    # Palabras de >4 letras sin vocales
    no_vowel_words = len(re.findall(r'\b[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]{5,}\b', text))
    if no_vowel_words > 10:
        return True, f"Palabras sin vocales ({no_vowel_words})"
    
    # 7. ✅ NUEVO: Detectar espacios insertados incorrectamente dentro de palabras
    # Patrón: letra espacio 1-2 letras espacio letra (ej: "d e l a" o "rein a")
    fragmented_words = len(re.findall(r'\b[a-záéíóú]\s[a-záéíóú]{1,2}\s[a-záéíóú]', text.lower()))
    if fragmented_words > 20:
        return True, f"Palabras fragmentadas por espacios ({fragmented_words})"
    
    # 8. ✅ NUEVO: Detectar palabras pegadas sin espacios
    # Patrón: secuencias muy largas de letras minúsculas (>25 caracteres sin espacio)
    glued_words = len(re.findall(r'[a-záéíóú]{25,}', text.lower()))
    if glued_words > 10:
        return True, f"Palabras pegadas sin espacios ({glued_words})"
    
    # 9. ✅ NUEVO: Detectar patrón específico de espaciado incorrecto
    # "del a" en lugar de "de la", "enwww" en lugar de "en www"
    bad_spacing_patterns = len(re.findall(r'\b(de|en|la|el|un|los|las|por|con)\s[a-z]\s', text.lower()))
    bad_spacing_patterns += len(re.findall(r'[a-z](www|http|com|org|net)', text.lower()))
    if bad_spacing_patterns > 15:
        return True, f"Espaciado incorrecto detectado ({bad_spacing_patterns})"
    
    return False, "Texto parece normal"


def repair_corrupted_spacing(text: str) -> str:
    """
    Repara texto con espaciado corrupto de PDFs con fuentes propietarias
    
    ✅ ESTRATEGIA GENÉRICA (funciona para cualquier PDF):
    1. Unir fragmentos de palabras (espacios incorrectos dentro de palabras)
    2. Separar palabras pegadas usando patrones del español
    3. Limpieza final
    """
    if not text or len(text) < 50:
        return text
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 1: UNIR FRAGMENTOS DE PALABRAS
    # Patrón: palabra + espacio + 1-2 letras sueltas
    # Ejemplo: "rein a" → "reina", "histori a" → "historia"
    # ═══════════════════════════════════════════════════════════════════════
    
    for _ in range(10):  # Múltiples pasadas para casos anidados
        old_text = text
        # Unir: "palabr a" → "palabra" (palabra + espacio + 1-2 letras)
        text = re.sub(r'(\b\w{2,})\s+([a-záéíóúñ]{1,2})\b(?!\s+[a-záéíóúñ]{1,2}\b)', r'\1\2', text)
        # Unir: "a doptar" → "adoptar" (1-2 letras + espacio + palabra)
        text = re.sub(r'\b([a-záéíóúñ]{1,2})\s+([a-záéíóúñ]{3,}\b)', r'\1\2', text)
        if text == old_text:
            break
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 2: SEPARAR PALABRAS PEGADAS
    # Usar artículos, preposiciones y conjunciones del español
    # ═══════════════════════════════════════════════════════════════════════
    
    # Casos especiales: preposición + artículo pegados (dela, delos, enla, etc.)
    text = re.sub(r'\b(de)(l?[ao]s?)\b', r'\1 \2', text, flags=re.IGNORECASE)  # dela → de la
    text = re.sub(r'\b(en)(l?[ao]s?)\b', r'\1 \2', text, flags=re.IGNORECASE)  # enla → en la
    text = re.sub(r'\b(con)(l?[ao]s?)\b', r'\1 \2', text, flags=re.IGNORECASE)  # conla → con la
    text = re.sub(r'\b(por)(l?[ao]s?)\b', r'\1 \2', text, flags=re.IGNORECASE)  # porla → por la
    text = re.sub(r'\b(para)(l?[ao]s?)\b', r'\1 \2', text, flags=re.IGNORECASE)  # parala → para la
    text = re.sub(r'\b(sin)(l?[ao]s?)\b', r'\1 \2', text, flags=re.IGNORECASE)  # sinla → sin la
    
    # Artículos pegados a la siguiente palabra (3+ letras)
    text = re.sub(r'\b(el|la|los|las|un|una|unos|unas)([a-záéíóúñ]{3,})', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Preposiciones pegadas (3+ letras después)
    text = re.sub(r'\b(de|del|al|en|con|por|para|sin|sobre|entre|hasta|desde|hacia)([a-záéíóúñ]{3,})', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Conjunciones pegadas
    text = re.sub(r'\b(y|e|o|u|que|como|si|ni|pero|sino|aunque)([a-záéíóúñ]{3,})', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Pronombres pegados
    text = re.sub(r'\b(se|me|te|nos|os|lo|le|les|su|sus)([a-záéíóúñ]{3,})', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Verbos comunes pegados
    text = re.sub(r'\b(es|era|fue|son|han|ha|hay|tiene|tenía)([a-záéíóúñ]{3,})', r'\1 \2', text, flags=re.IGNORECASE)
    
    # Adverbios pegados
    text = re.sub(r'\b(no|ya|muy|tan|más|menos|bien|mal|solo)([a-záéíóúñ]{3,})', r'\1 \2', text, flags=re.IGNORECASE)
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 3: LIMPIEZA FINAL
    # ═══════════════════════════════════════════════════════════════════════
    
    # Múltiples espacios → uno solo
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Espacios antes de puntuación
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    
    # Espacio después de puntuación si falta
    text = re.sub(r'([.,;:!?])([a-záéíóúñA-ZÁÉÍÓÚÑ¿¡])', r'\1 \2', text)
    
    return text


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
    
    ✅ ESTRATEGIA OPTIMIZADA - PDFTOTEXT PRIMERO (INSTANTÁNEO):
    
    Orden de prioridad:
    1. PDFTOTEXT (instantáneo, extrae texto embebido real)
    2. OCRMYPDF --force-ocr (si pdftotext falla o texto corrupto)
    3. Tesseract directo como fallback
    4. PyMuPDF/PyPDF2 como último recurso
    
    Args:
        pdf_content: Contenido del PDF en bytes
        
    Returns:
        tuple: (texto extraído, número total de páginas)
    """
    import gc
    
    results = []
    total_pages = 0
    
    print(f"📖 Extrayendo texto del PDF...")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 0: PDFTOTEXT (INSTANTÁNEO - Primera opción)
    # ═══════════════════════════════════════════════════════════════════════
    if PDFTOTEXT_AVAILABLE:
        print("   ⚡ Intentando pdftotext (instantáneo)...")
        text_pdftotext, pages_pdftotext = extract_with_pdftotext(pdf_content)
        
        if len(text_pdftotext.strip()) > 100:
            is_corrupted, reason = detect_corrupted_text(text_pdftotext)
            
            if not is_corrupted:
                print(f"   ✅ pdftotext exitoso: {len(text_pdftotext)} chars, texto limpio")
                text = aggressive_text_cleanup(text_pdftotext)
                gc.collect()
                return text, pages_pdftotext
            else:
                print(f"   ⚠️ pdftotext produjo texto con problemas: {reason}")
                print("   🔄 Cambiando a OCR...")
        else:
            print(f"   ⚠️ pdftotext produjo muy poco texto ({len(text_pdftotext)} chars)")
            print("   🔄 Cambiando a OCR...")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 1: OCRMYPDF (si pdftotext falló)
    # ═══════════════════════════════════════════════════════════════════════
    processed_pdf = pdf_content
    if OCRMYPDF_AVAILABLE:
        print("   🔧 Pre-procesando PDF con ocrmypdf...")
        processed_pdf = preprocess_pdf_with_ocrmypdf(pdf_content)
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 2: Contar páginas y extraer con PyMuPDF (del PDF procesado)
    # ═══════════════════════════════════════════════════════════════════════
    if PYMUPDF_AVAILABLE:
        try:
            import fitz
            pdf_doc = fitz.open(stream=processed_pdf, filetype="pdf")
            total_pages = len(pdf_doc)
            pdf_doc.close()
            print(f"   📄 PDF tiene {total_pages} páginas")
            
            # Si usamos ocrmypdf, PyMuPDF debería extraer el texto OCR limpio
            if OCRMYPDF_AVAILABLE and processed_pdf != pdf_content:
                text_mupdf, pages_mupdf, errors_mupdf = extract_with_pymupdf(processed_pdf)
                is_corrupted, reason = detect_corrupted_text(text_mupdf)
                
                if not is_corrupted and len(text_mupdf.strip()) > 100:
                    print(f"   ✅ ocrmypdf + PyMuPDF: {len(text_mupdf)} chars, texto limpio")
                    text = aggressive_text_cleanup(text_mupdf)
                    gc.collect()
                    return text, pages_mupdf
                else:
                    print(f"   ⚠️ ocrmypdf produjo texto con problemas: {reason}")
                    
        except Exception as e:
            print(f"   ⚠️ No se pudo procesar con PyMuPDF: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 3: TESSERACT OCR DIRECTO (fallback si ocrmypdf falló)
    # ═══════════════════════════════════════════════════════════════════════
    if TESSERACT_AVAILABLE:
        try:
            print(f"   🔍 Usando Tesseract OCR directo...")
            text_tess, pages_tess, errors_tess = extract_with_tesseract(pdf_content)
            
            # Verificar que Tesseract produjo texto válido
            if len(text_tess.strip()) > 100:
                is_corrupted, reason = detect_corrupted_text(text_tess)
                if not is_corrupted:
                    results.append(('Tesseract', text_tess, pages_tess, errors_tess))
                    total_pages = pages_tess
                    print(f"   ✅ Tesseract: {len(text_tess)} chars, texto limpio")
                    
                    # Usar Tesseract directamente
                    text = aggressive_text_cleanup(text_tess)
                    gc.collect()
                    print(f"✅ Texto extraído con OCR: {len(text)} caracteres de {pages_tess} páginas")
                    return text, pages_tess
                else:
                    print(f"   ⚠️ Tesseract produjo texto con problemas: {reason}")
                    results.append(('Tesseract', text_tess, pages_tess, errors_tess))
            else:
                print(f"   ⚠️ Tesseract produjo muy poco texto ({len(text_tess)} chars)")
                
        except Exception as e:
            print(f"   ❌ Tesseract falló: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 3: PyMuPDF como FALLBACK (solo si Tesseract falló)
    # ═══════════════════════════════════════════════════════════════════════
    if PYMUPDF_AVAILABLE and not results:
        try:
            print(f"   📖 Fallback a PyMuPDF...")
            text_mupdf, pages_mupdf, errors_mupdf = extract_with_pymupdf(pdf_content)
            results.append(('PyMuPDF', text_mupdf, pages_mupdf, errors_mupdf))
            total_pages = pages_mupdf
            print(f"   PyMuPDF: {len(text_mupdf)} chars, {errors_mupdf} errores")
        except Exception as e:
            print(f"   ❌ PyMuPDF falló: {e}")
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 4: PyPDF2 como último recurso
    # ═══════════════════════════════════════════════════════════════════════
    if not results and PYPDF2_AVAILABLE:
        try:
            print(f"   📄 Último recurso: PyPDF2...")
            text_pypdf2, pages_pypdf2, errors_pypdf2 = extract_with_pypdf2(pdf_content)
            results.append(('PyPDF2', text_pypdf2, pages_pypdf2, errors_pypdf2))
            total_pages = pages_pypdf2
            print(f"   PyPDF2: {len(text_pypdf2)} chars")
        except Exception as e:
            print(f"   ❌ PyPDF2 falló: {e}")
    
    if not results:
        raise Exception("No se pudo extraer texto del PDF con ningún método")
    
    # ═══════════════════════════════════════════════════════════════════════
    # ELEGIR EL MEJOR RESULTADO (el de menos errores)
    # ═══════════════════════════════════════════════════════════════════════
    best = min(results, key=lambda x: x[3])  # x[3] = error_count
    print(f"   ✅ Usando {best[0]}")
    
    text = best[1]
    total_pages = best[2]
    
    # Limpiar texto extraído
    text = aggressive_text_cleanup(text)
    
    # Limpiar memoria
    gc.collect()
    
    print(f"✅ Texto extraído: {len(text)} caracteres de {total_pages} páginas")
    return text, total_pages


def aggressive_text_cleanup(text: str) -> str:
    """
    Limpieza AGRESIVA de texto extraído de PDF
    
    ✅ MEJORADO: Repara texto con espaciado incorrecto de PyMuPDF
    
    Problema detectado: PDFs con fuentes propietarias producen:
    - "de scargadoenwww" → "descargado en www"
    - "el ejandri a" → "alejandría"
    - "lacon desade" → "la condesa de"
    """
    if not text:
        return text
    
    # ═══════════════════════════════════════════════════════════════════════
    # PASO 0: Reparación de espaciado corrupto (NUEVO)
    # ═══════════════════════════════════════════════════════════════════════
    text = repair_corrupted_spacing(text)
    
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
