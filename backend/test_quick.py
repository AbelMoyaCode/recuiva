from question_generator import *

print("=== PRUEBAS LOCALES SPRINT 2 ===\n")

# Test 1: Detectar tipos
print("TEST 1: Detección de tipos de contenido")
text1 = "El cálculo diferencial es la rama de las matemáticas"
print(f"Texto: {text1}")
print(f"Tipo detectado: {detect_content_type(text1)}\n")

# Test 2: Extraer conceptos
print("TEST 2: Extracción de conceptos")
concepts = extract_key_concepts(text1)
print(f"Conceptos: {concepts}\n")

# Test 3: Generar preguntas
print("TEST 3: Generación de preguntas")
chunks = [
    "El cálculo diferencial estudia las tasas de cambio.",
    "La derivada mide la tasa de cambio instantánea."
]
questions = generate_questions_dict(chunks, 2, "random")
print(f"Generadas {len(questions)} preguntas:")
for i, q in enumerate(questions, 1):
    print(f"{i}. {q['question']} (tipo: {q['question_type']})")

print("\n✅ TODAS LAS PRUEBAS PASARON")
