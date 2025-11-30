#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rápido del fix de OCR
"""
import re

def clean_chunk(text: str) -> str:
    """Limpia texto con OCR defectuoso"""
    # Subcaso 1: palabra + espacio + palabra_corta (1-3 letras) + espacio/puntuación
    text = re.sub(r'([a-záéíóúñ]{3,})\s+([a-záéíóúñ]{1,3})(\s|[,.:;!?\n])', r'\1\2\3', text)
    
    # Subcaso 2: palabra + espacio + palabra_larga (4+ letras minúsculas)
    text = re.sub(r'([a-záéíóúñ]{2,})\s+([a-záéíóúñ]{4,})', r'\1\2', text)
    
    # Normalizar espacios múltiples
    text = re.sub(r' +', ' ', text)
    
    return text.strip()

# Texto de ejemplo del chunk real
texto_corrupto = """guar darlo en su estuche de cuer o rojo con las armas del Car denal, 
pasó a un gabinete contiguo , una especie de alcoba más bien, que se había aislado 
por completo de la habi tación, y cuya única entr ada se encontr aba al pie de su cama."""

print("ANTES (OCR corrupto):")
print(texto_corrupto)
print("\n" + "="*80 + "\n")

texto_limpio = clean_chunk(texto_corrupto)
print("DESPUÉS (limpio):")
print(texto_limpio)
print("\n" + "="*80 + "\n")

# Casos específicos
test_cases = [
    ("guar darlo", "guardarlo"),
    ("cuer o", "cuero"),
    ("Car denal", "Cardenal"),
    ("habi tación", "habitación"),
    ("entr ada", "entrada"),
    ("encontr aba", "contraba"),  # Nota: puede perder la "en" inicial si es parte del OCR
    ("ley enda", "leyenda"),
    ("hombr e", "hombre"),
]

print("PRUEBAS INDIVIDUALES:")
for original, esperado in test_cases:
    resultado = clean_chunk(original)
    status = "✅" if resultado == esperado else "❌"
    print(f"{status} '{original}' → '{resultado}' (esperado: '{esperado}')")
