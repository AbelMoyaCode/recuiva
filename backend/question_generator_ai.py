"""
Generador de Preguntas Inteligentes usando Groq API
Sistema RAG (Retrieval-Augmented Generation) para Active Recall

Este módulo genera preguntas de comprensión profunda basándose en los chunks
del material PDF usando Groq API (GRATIS 100% - Ultra rápido).

Autor: Abel Jesús Moya Acosta
Fecha: 17 de noviembre de 2025
"""

import os
import json
import asyncio
from typing import List, Dict, Optional
from dotenv import load_dotenv
from groq import AsyncGroq

# Cargar variables de entorno
load_dotenv()

# Configuración de Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"  # Llama 3.3 70B - Modelo más reciente (nov 2025)


async def generate_questions_with_ai(
    material_id: str,
    supabase_client,
    num_questions_per_chunk: int = 2,
    max_chunks: Optional[int] = None
) -> Dict:
    """
    Genera preguntas inteligentes usando Groq RAG
    
    Args:
        material_id: UUID del material en Supabase
        supabase_client: Cliente de Supabase
        num_questions_per_chunk: Número de preguntas por chunk (default: 2)
        max_chunks: Límite de chunks a procesar (None = todos)
        
    Returns:
        Dict con:
            - success: bool
            - questions: List[Dict] con preguntas generadas
            - total_questions: int
            - chunks_processed: int
            - cost_estimate: float (USD estimado)
    """
    
    print(f"\n{'='*70}")
    print(f"  GENERANDO PREGUNTAS CON GROQ AI (Llama 3.1 70B)")
    print(f"{'='*70}")
    
    # 1. Obtener chunks del material desde Supabase
    print(f"📚 Obteniendo chunks del material {material_id}...")
    
    try:
        response = supabase_client.table('material_embeddings')\
            .select('id, chunk_index, chunk_text')\
            .eq('material_id', material_id)\
            .order('chunk_index')\
            .execute()
        
        chunks = response.data
        
        if not chunks:
            return {
                "success": False,
                "error": f"No se encontraron chunks para material {material_id}",
                "questions": [],
                "total_questions": 0,
                "chunks_processed": 0
            }
        
        # Limitar chunks si se especifica
        if max_chunks:
            chunks = chunks[:max_chunks]
        
        print(f"✅ Chunks encontrados: {len(chunks)}")
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Error obteniendo chunks: {str(e)}",
            "questions": [],
            "total_questions": 0,
            "chunks_processed": 0
        }
    
    # 2. Generar preguntas para cada chunk
    all_questions = []
    chunks_processed = 0
    chunks_failed = 0
    
    print(f"\n🤖 Generando preguntas con Groq AI (⚡ ultra rápido)...")
    print(f"   Chunks a procesar: {len(chunks)}")
    print(f"   Preguntas por chunk: {num_questions_per_chunk}")
    print(f"   Total esperado: {len(chunks) * num_questions_per_chunk} preguntas\n")
    
    for i, chunk in enumerate(chunks, 1):
        try:
            print(f"   [{i}/{len(chunks)}] Procesando chunk {chunk['chunk_index']}...", end=" ")
            
            # Generar preguntas con Groq
            questions = await generate_questions_for_chunk(
                chunk_text=chunk['chunk_text'],
                chunk_index=chunk['chunk_index'],
                num_questions=num_questions_per_chunk
            )
            
            # Agregar metadatos a cada pregunta
            for question_text in questions:
                all_questions.append({
                    "question": question_text,
                    "chunk_id": chunk['id'],
                    "chunk_index": chunk['chunk_index'],
                    "material_id": material_id,
                    "source_preview": chunk['chunk_text'][:150] + "..."
                })
            
            chunks_processed += 1
            print(f"✅ {len(questions)} preguntas")
            
            # Pequeño delay para no saturar API
            await asyncio.sleep(1)
            
        except Exception as e:
            chunks_failed += 1
            print(f"❌ Error: {str(e)[:50]}...")
            continue
    
    print(f"\n{'='*70}")
    print(f"  RESUMEN DE GENERACIÓN")
    print(f"{'='*70}")
    print(f"✅ Chunks procesados: {chunks_processed}/{len(chunks)}")
    if chunks_failed > 0:
        print(f"⚠️  Chunks fallidos: {chunks_failed}")
    print(f"✅ Preguntas generadas: {len(all_questions)}")
    print(f"💰 Costo: $0.00 (GRATIS 100%)")
    print(f"{'='*70}\n")
    
    return {
        "success": True,
        "questions": all_questions,
        "total_questions": len(all_questions),
        "chunks_processed": chunks_processed,
        "chunks_failed": chunks_failed,
        "cost_estimate": 0.0
    }


async def generate_questions_for_chunk(
    chunk_text: str,
    chunk_index: int,
    num_questions: int = 2
) -> List[str]:
    """
    Genera preguntas para un chunk específico usando Groq
    
    Args:
        chunk_text: Texto del chunk
        chunk_index: Índice del chunk (para contexto)
        num_questions: Número de preguntas a generar
        
    Returns:
        List[str]: Lista de preguntas generadas
    """
    
    # Prompt optimizado para Llama 3.1 70B
    system_prompt = """Eres un profesor universitario experto en Active Recall y pedagogía.

Tu tarea: Generar preguntas de comprensión profunda para aprendizaje activo.

REGLAS ESTRICTAS:
1. Las preguntas DEBEN requerir EXPLICAR, ANALIZAR, COMPARAR o RELACIONAR conceptos (NO memorizar datos)
2. Basarse ÚNICAMENTE en el contenido del fragmento proporcionado
3. Ser específicas y contextualizadas al contenido
4. Usar terminología académica apropiada
5. Fomentar pensamiento crítico y comprensión profunda

FORMATO DE SALIDA: JSON válido con esta estructura:
{
  "questions": ["Pregunta 1", "Pregunta 2"]
}

Responde SOLO con el JSON, sin texto adicional."""

    user_prompt = f"""Fragmento del libro (Sección {chunk_index}):

{chunk_text}

Genera {num_questions} preguntas de Active Recall en formato JSON."""

    try:
        # Llamada a Groq API (AsyncGroq)
        client = AsyncGroq(api_key=GROQ_API_KEY)
        
        completion = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        # Parsear respuesta
        generated_text = completion.choices[0].message.content
        
        # Limpiar posibles marcadores de markdown
        if generated_text.startswith("```json"):
            generated_text = generated_text[7:]
        if generated_text.endswith("```"):
            generated_text = generated_text[:-3]
        
        # Parsear JSON
        generated = json.loads(generated_text.strip())
        
        # Validar estructura
        if "questions" not in generated:
            raise ValueError("Respuesta no contiene campo 'questions'")
        
        questions = generated["questions"]
        
        # Validar que sean strings no vacías
        questions = [q.strip() for q in questions if isinstance(q, str) and q.strip()]
        
        return questions
        
    except json.JSONDecodeError as e:
        print(f"\n⚠️  Error parseando JSON: {e}")
        return []
    
    except Exception as e:
        print(f"\n⚠️  Error llamando a Groq API: {e}")
        return []


async def save_generated_questions_to_supabase(
    questions: List[Dict],
    material_id: str,
    user_id: str,
    supabase_client
) -> Dict:
    """
    Guarda preguntas generadas en Supabase
    
    Args:
        questions: Lista de diccionarios con preguntas
        material_id: UUID del material
        user_id: UUID del usuario
        supabase_client: Cliente de Supabase
        
    Returns:
        Dict con resultado de la operación
    """
    
    print(f"\n💾 Guardando {len(questions)} preguntas en Supabase...")
    
    saved_count = 0
    failed_count = 0
    
    for q in questions:
        try:
            # Insertar en tabla questions
            supabase_client.table('questions').insert({
                'material_id': material_id,
                'user_id': user_id,
                'question_text': q['question'],
                'topic': None,  # Se puede agregar categorización después
                'difficulty': 'medium',  # Por defecto
                'expected_answer': None  # No tenemos respuesta esperada
            }).execute()
            
            saved_count += 1
            
        except Exception as e:
            print(f"   ⚠️  Error guardando pregunta: {str(e)[:50]}...")
            failed_count += 1
            continue
    
    print(f"✅ Preguntas guardadas: {saved_count}/{len(questions)}")
    if failed_count > 0:
        print(f"⚠️  Preguntas fallidas: {failed_count}")
    
    return {
        "success": True,
        "saved_count": saved_count,
        "failed_count": failed_count
    }


async def test_groq_connection():
    """
    Prueba la conexión con Groq API
    
    Returns:
        Dict con resultado de la prueba
    """
    
    print("\n🔍 Probando conexión con Groq API...")
    
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY no está configurada en .env")
        return {"success": False, "error": "API key no configurada"}
    
    try:
        client = AsyncGroq(api_key=GROQ_API_KEY)
        
        completion = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "user", "content": "Responde solo con 'OK' si puedes leerme."}
            ],
            max_tokens=10
        )
        
        response = completion.choices[0].message.content
        
        print(f"✅ Conexión exitosa con Groq")
        print(f"   Modelo: {GROQ_MODEL}")
        print(f"   Respuesta: {response}")
        
        return {
            "success": True,
            "message": "Conexión exitosa",
            "response": response
        }
        
    except Exception as e:
        print(f"❌ Error conectando con Groq: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# Script de prueba
if __name__ == "__main__":
    async def main():
        """Prueba básica del módulo"""
        
        # Test: Probar conexión
        await test_groq_connection()
        
        print("\n" + "="*70)
        print("  TEST: Generación de pregunta de ejemplo")
        print("="*70)
        
        sample_chunk = """
        El collar de la reina es una obra maestra de Maurice Leblanc,
        publicada en 1907. En ella, el autor francés narra las aventuras
        de Arsène Lupin, el famoso ladrón de guante blanco, quien se
        enfrenta a un enigma histórico relacionado con el collar de
        diamantes de la reina María Antonieta.
        """
        
        questions = await generate_questions_for_chunk(
            chunk_text=sample_chunk,
            chunk_index=0,
            num_questions=2
        )
        
        print(f"\n✅ Preguntas generadas:\n")
        for i, q in enumerate(questions, 1):
            print(f"   {i}. {q}\n")
    
    # Ejecutar test
    asyncio.run(main())
