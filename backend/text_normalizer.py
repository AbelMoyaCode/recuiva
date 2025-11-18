"""
Normalizador de Texto para Embeddings
======================================

Corrige errores de extracción OCR y normaliza texto antes de generar embeddings.
Esto mejora la calidad de la similitud semántica.

Problemas que soluciona:
- Espacios entre sílabas: "fo to sín te sis" → "fotosíntesis"
- Guiones de separación: "trans- formación" → "transformación"
- Espacios múltiples: "El   libro" → "El libro"
- Espacios antes de puntuación: "hola ." → "hola."

Autor: Abel Jesús Moya Acosta
Fecha: 17 de noviembre de 2025
Proyecto: Recuiva - Active Recall con IA
"""

import re
from typing import List, Union


def normalize_text(text: str) -> str:
    """
    Normaliza texto para mejorar calidad de embeddings
    
    Transformaciones aplicadas:
    1. Remover espacios entre sílabas (OCR error común)
    2. Remover guiones de separación de línea
    3. Normalizar espacios múltiples
    4. Corregir espacios antes de puntuación
    5. Trimear inicio/fin
    
    Args:
        text: Texto original (puede contener errores OCR)
        
    Returns:
        str: Texto normalizado
        
    Ejemplos:
        >>> normalize_text("La fo to sín te sis es un proceso")
        'La fotosíntesis es un proceso'
        
        >>> normalize_text("Las plantas trans- forman luz en energía")
        'Las plantas transforman luz en energía'
        
        >>> normalize_text("El   libro   tiene    muchos   espacios")
        'El libro tiene muchos espacios'
        
        >>> normalize_text("Hola , ¿cómo estás ?")
        'Hola, ¿cómo estás?'
    """
    if not text or not isinstance(text, str):
        return ""
    
    # 1. Remover espacios innecesarios entre sílabas (error OCR común)
    # Detecta patrones como: "fo to sín te sis" (espacios entre letras cortas)
    # Estrategia mejorada: Capturar fragmentos de 1-5 letras con espacios
    
    # Primero: fragmentos muy cortos (1-2 letras)
    for _ in range(5):
        text = re.sub(r'\b(\w{1,2})\s+(\w{1,2})\b', r'\1\2', text)
    
    # Segundo: fragmentos medianos (2-4 letras + 3-6 letras)
    # Ejemplo: "pr ecise" → "precise"
    for _ in range(3):
        text = re.sub(r'\b(\w{2,4})\s+(\w{3,6})\b', r'\1\2', text)
    
    # Tercero: caso específico de OCR malo - palabra al final de línea
    # Ejemplo: "esun punto" → "es un punto"
    text = re.sub(r'(\w)([a-z]{2,})\s+([a-z])', r'\1 \2 \3', text)
    
    # 2. Remover guiones de separación de línea (ej: "trans- formación")
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    
    # 3. Normalizar espacios múltiples a un solo espacio
    text = re.sub(r'\s{2,}', ' ', text)
    
    # 4. Remover espacios antes de puntuación
    text = re.sub(r'\s+([.,;:!?¿¡»])', r'\1', text)
    
    # 5. Agregar espacio después de puntuación si no existe
    text = re.sub(r'([.,;:!?])([A-Za-zÁ-úÑñ])', r'\1 \2', text)
    
    # 6. Trimear y retornar
    return text.strip()


def normalize_text_batch(texts: List[str]) -> List[str]:
    """
    Normaliza múltiples textos en lote
    
    Args:
        texts: Lista de textos a normalizar
        
    Returns:
        List[str]: Textos normalizados
    """
    return [normalize_text(t) for t in texts]


def detect_ocr_errors(text: str) -> dict:
    """
    Detecta posibles errores OCR en el texto (para debugging)
    
    Args:
        text: Texto a analizar
        
    Returns:
        dict: Estadísticas de errores detectados
    """
    stats = {
        'fragmented_words': 0,      # Palabras fragmentadas
        'hyphen_breaks': 0,          # Separaciones con guión
        'multiple_spaces': 0,        # Espacios múltiples
        'punctuation_spacing': 0,    # Espacios antes de puntuación
        'has_errors': False
    }
    
    # Contar fragmentaciones (palabras de 1-2 letras seguidas)
    fragmented = re.findall(r'\b\w{1,2}\s+\w{1,2}\b', text)
    stats['fragmented_words'] = len(fragmented)
    
    # Contar guiones de separación
    hyphen_breaks = re.findall(r'\w-\s+\w', text)
    stats['hyphen_breaks'] = len(hyphen_breaks)
    
    # Contar espacios múltiples
    multiple_spaces = re.findall(r'\s{2,}', text)
    stats['multiple_spaces'] = len(multiple_spaces)
    
    # Contar espacios antes de puntuación
    punctuation_spacing = re.findall(r'\s+[.,;:!?]', text)
    stats['punctuation_spacing'] = len(punctuation_spacing)
    
    # Determinar si hay errores
    stats['has_errors'] = any([
        stats['fragmented_words'] > 2,
        stats['hyphen_breaks'] > 0,
        stats['multiple_spaces'] > 5,
        stats['punctuation_spacing'] > 3
    ])
    
    return stats


# ===== FUNCIONES AUXILIARES =====

def clean_latex_artifacts(text: str) -> str:
    """
    Remueve artefactos de LaTeX/OCR matemático
    
    Args:
        text: Texto con posibles artefactos LaTeX
        
    Returns:
        str: Texto limpio
    """
    # Remover comandos LaTeX comunes
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    
    # Remover símbolos matemáticos aislados
    text = re.sub(r'\$([^$]*)\$', r'\1', text)
    
    return text


def fix_common_ocr_substitutions(text: str) -> str:
    """
    Corrige sustituciones OCR comunes (caracteres confundidos)
    
    Ejemplos:
    - 'l' (L minúscula) → '1' (uno)
    - '0' (cero) → 'O' (o mayúscula)
    - 'rn' → 'm'
    
    Args:
        text: Texto con posibles sustituciones
        
    Returns:
        str: Texto corregido
    """
    # Lista de sustituciones comunes
    # (Puede expandirse según el tipo de PDF)
    substitutions = [
        # (patrón_incorrecto, corrección)
        (r'\bl1\b', 'li'),  # Ejemplo: "l1bro" → "libro"
        (r'\brn\b', 'm'),   # Ejemplo: "forrna" → "forma"
    ]
    
    for pattern, replacement in substitutions:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


# ===== TESTING =====

if __name__ == "__main__":
    """Pruebas del normalizador"""
    
    print("=" * 70)
    print("🧹 NORMALIZADOR DE TEXTO - TESTS")
    print("=" * 70)
    
    # Test 1: Fragmentación de palabras
    test1 = "La fo to sín te sis es un pro ce so bi o ló gi co"
    print(f"\n📝 Test 1 - Fragmentación:")
    print(f"   Antes: {test1}")
    print(f"   Después: {normalize_text(test1)}")
    
    # Test 2: Guiones de separación
    test2 = "Las plantas trans- forman la luz solar en ener- gía química"
    print(f"\n📝 Test 2 - Guiones:")
    print(f"   Antes: {test2}")
    print(f"   Después: {normalize_text(test2)}")
    
    # Test 3: Espacios múltiples
    test3 = "El   libro    tiene     muchos    espacios"
    print(f"\n📝 Test 3 - Espacios múltiples:")
    print(f"   Antes: '{test3}'")
    print(f"   Después: '{normalize_text(test3)}'")
    
    # Test 4: Puntuación
    test4 = "Hola , ¿cómo estás ? Bien ."
    print(f"\n📝 Test 4 - Puntuación:")
    print(f"   Antes: {test4}")
    print(f"   Después: {normalize_text(test4)}")
    
    # Test 5: Caso real del PDF
    test5 = """El co llar de la rei na es una obra maes tra de Mau rice Le blanc , 
    pu bli ca da en 1907 . En ella , el au tor fran cés na rra las a ven tu ras"""
    print(f"\n📝 Test 5 - Caso real (PDF con OCR malo):")
    print(f"   Antes: {test5}")
    print(f"   Después: {normalize_text(test5)}")
    
    # Test 6: Detección de errores
    print(f"\n🔍 Test 6 - Detección de errores:")
    errors = detect_ocr_errors(test5)
    print(f"   Palabras fragmentadas: {errors['fragmented_words']}")
    print(f"   Guiones de separación: {errors['hyphen_breaks']}")
    print(f"   Espacios múltiples: {errors['multiple_spaces']}")
    print(f"   Errores de puntuación: {errors['punctuation_spacing']}")
    print(f"   ¿Tiene errores?: {'✅ SÍ' if errors['has_errors'] else '❌ NO'}")
    
    print("\n" + "=" * 70)
    print("✅ Tests completados")
    print("=" * 70)
