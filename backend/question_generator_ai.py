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
GROQ_MODEL = "llama-3.1-8b-instant"  # Llama 3.1 8B - Ultra rápido y sin límites de tokens


def classify_question_type(question: str) -> str:
    """
    Clasifica una pregunta como 'literal', 'inferential' u 'other'
    usando reglas simples basadas en palabras clave.
    
    - LITERAL: pide info explícita del texto (¿quién?, ¿qué hizo?, ¿dónde?, ¿cuándo?, ¿cuántos?…)
    - INFERENCIAL: pide deducir, interpretar, explicar causas, intenciones, consecuencias
    
    Args:
        question: Texto de la pregunta
        
    Returns:
        'literal', 'inferential' u 'other'
    """
    q = question.lower().strip()
    
    # Patrones para preguntas INFERENCIALES (razonamiento, deducción)
    inferential_patterns = [
        # Por qué (causa/razón)
        "por qué", "por que",
        # Inferir/deducir
        "qué sugiere", "que sugiere",
        "qué podemos inferir", "que podemos inferir",
        "qué se puede inferir", "que se puede inferir",
        "qué puede inferirse", "que puede inferirse",
        "puede inferirse", "puede deducirse",
        "se puede inferir", "se puede deducir",
        # Cómo se + verbo (relaciones, comportamientos, explicaciones)
        "cómo se relaciona", "como se relaciona",
        "cómo se explica", "como se explica",
        "cómo se comportó", "como se comporto",
        "cómo se conecta", "como se conecta",
        "cómo se vincula", "como se vincula",
        "cómo se manifiesta", "como se manifiesta",
        "cómo se refleja", "como se refleja",
        "cómo se evidencia", "como se evidencia",
        "cómo se caracteriza", "como se caracteriza",  # 👈 NUEVO
        "cómo se desarrolla", "como se desarrolla",  # 👈 NUEVO
        "cómo se transforma", "como se transforma",  # 👈 NUEVO
        "cómo se presenta", "como se presenta",  # 👈 NUEVO
        "cómo se describe", "como se describe",  # 👈 NUEVO
        "cómo reaccionó", "como reacciono",
        "cómo actuó", "como actuo",
        "cómo logró", "como logro",
        "cómo influyó", "como influyo",
        # Intenciones/consecuencias
        "qué intención", "que intencion", "que intención",
        "qué consecuencias", "que consecuencias",
        "qué implicaciones", "que implicaciones",
        # Opinión/interpretación
        "qué crees", "que crees",
        "qué piensas", "que piensas",
        "qué opinas", "que opinas",
        "cómo interpretas", "como interpretas",
        # Significado/relación
        "qué significa", "que significa",
        "qué relación", "que relacion", "que relación",
        "cómo influye", "como influye",
        "qué motiva", "que motiva",
        # Causa/efecto
        "cuál es la causa", "cual es la causa",
        "cuál es el motivo", "cual es el motivo",
        "qué efecto", "que efecto",
        "cómo afecta", "como afecta",
        # Hipotéticos
        "qué podría", "que podria", "que podría",
        "qué hubiera", "que hubiera",
        "qué habría", "que habria", "que habría",
        # Análisis
        "de qué manera", "de que manera",
        "en qué sentido", "en que sentido",
        "qué nos dice esto sobre", "que nos dice esto sobre",
        "qué revela", "que revela",
        "cómo demuestra", "como demuestra",
        "qué demuestra", "que demuestra",
        "qué indica", "que indica",
        "qué evidencia", "que evidencia",
        "qué refleja", "que refleja",
        "qué nos permite", "que nos permite",
        "sobre su comprensión", "sobre su entendimiento",
        # Frases con "la idea de" (análisis conceptual)
        "con la idea de", "la idea de",
        # Preguntas de análisis profundo
        "qué papel juega", "que papel juega",
        "qué rol cumple", "que rol cumple",
        "qué función tiene", "que funcion tiene",
        "qué importancia", "que importancia",
        # Preguntas evaluativas y comparativas
        "qué ventaja", "que ventaja",
        "qué desventaja", "que desventaja",
        "qué beneficio", "que beneficio",
        "qué diferencia", "que diferencia",
        "qué similitud", "que similitud",
        "qué aspecto", "que aspecto",
        "qué característica", "que caracteristica", "que característica",
        "qué elemento", "que elemento",
        "qué factor", "que factor",
        "qué rasgo", "que rasgo",
        "qué cualidad", "que cualidad",
        "qué tipo de", "que tipo de",
        # Más patrones de "cómo se..."
        "cómo se percibe", "como se percibe",
        "cómo se representa", "como se representa",
        "cómo se expresa", "como se expresa",
        "cómo se construye", "como se construye",
        "cómo se articula", "como se articula",
        "cómo se plantea", "como se plantea",
        "cómo se vincula", "como se vincula",
        "cómo se conecta", "como se conecta",
        "cómo se estructura", "como se estructura",
        "cómo se organiza", "como se organiza",
        "cómo se define", "como se define",
        "cómo se ejemplifica", "como se ejemplifica",
        "cómo se aplica", "como se aplica",
        "cómo se usa", "como se usa",
        "cómo se utiliza", "como se utiliza",
        # Preguntas de valoración
        "es importante", "son importantes",
        "es significativo", "son significativos",
        "es relevante", "son relevantes"
    ]
    
    # Patrones para preguntas LITERALES (información explícita)
    literal_patterns = [
        "quién ", "quien ",  # espacio para evitar falsos positivos
        "quiénes", "quienes",
        "qué hizo", "que hizo",
        "qué pasó", "que paso", "qué pasó",
        "qué ocurrió", "que ocurrio", "que ocurrió",
        "qué sucedió", "que sucedio", "que sucedió",
        "dónde ", "donde ",
        "cuándo", "cuando",
        "cuántos", "cuantos",
        "cuántas", "cuantas",
        "en qué año", "en que año", "en que ano",
        "en qué lugar", "en que lugar",
        "en qué ciudad", "en que ciudad",
        "en qué país", "en que pais", "en que país",
        "qué recibió", "que recibio", "que recibió",
        "qué encontró", "que encontro", "que encontró",
        "qué dijo", "que dijo",
        "qué respondió", "que respondio", "que respondió",
        "cuál es el nombre", "cual es el nombre",
        "cómo se llama", "como se llama",
        "a quién", "a quien",
        "de quién", "de quien",
        "qué objeto", "que objeto",
        "qué color", "que color",
        "qué tipo de", "que tipo de",
        "cuál fue", "cual fue",
        "qué edad", "que edad",
        "cuánto tiempo", "cuanto tiempo",
        "cuánto dinero", "cuanto dinero",
        "qué cantidad", "que cantidad"
    ]
    
    # Verificar patrones inferenciales primero (más específicos)
    if any(pat in q for pat in inferential_patterns):
        return "inferential"
    
    # Luego verificar patrones literales
    if any(pat in q for pat in literal_patterns):
        return "literal"
    
    return "other"


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
    print(f"  GENERANDO PREGUNTAS CON GROQ AI ({GROQ_MODEL})")
    print(f"{'='*70}")
    
    # 0. Validar que GROQ_API_KEY esté configurada
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY no está configurada en .env")
        return {
            "success": False,
            "error": "GROQ_API_KEY no está configurada. Configúrala en el archivo .env del servidor.",
            "questions": [],
            "total_questions": 0,
            "chunks_processed": 0
        }
    
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
    
    # 2. Generar preguntas POR LOTES (batch processing) - 10x más rápido
    all_questions = []
    chunks_processed = 0
    chunks_failed = 0
    
    # Configuración de lotes
    BATCH_SIZE = 10  # Procesar 10 chunks a la vez
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    
    print(f"\n🤖 Generando preguntas con Groq AI (⚡ ultra rápido)...")
    print(f"   Chunks a procesar: {len(chunks)}")
    print(f"   Tamaño de lote: {BATCH_SIZE} chunks")
    print(f"   Total de lotes: {total_batches}")
    print(f"   Preguntas por chunk: {num_questions_per_chunk}")
    print(f"   Total esperado: {len(chunks) * num_questions_per_chunk} preguntas\n")
    
    # Procesar chunks en lotes
    for batch_num in range(total_batches):
        start_idx = batch_num * BATCH_SIZE
        end_idx = min(start_idx + BATCH_SIZE, len(chunks))
        batch_chunks = chunks[start_idx:end_idx]
        
        print(f"   📦 Lote {batch_num + 1}/{total_batches} ({len(batch_chunks)} chunks)...", end=" ")
        
        try:
            # Generar preguntas para todo el lote en una sola llamada
            batch_questions = await generate_questions_batch(
                chunks_batch=batch_chunks,
                num_questions_per_chunk=num_questions_per_chunk
            )
            
            # Agregar preguntas generadas
            all_questions.extend(batch_questions)
            chunks_processed += len(batch_chunks)
            print(f"✅ {len(batch_questions)} preguntas")
            
        except Exception as e:
            chunks_failed += len(batch_chunks)
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


async def generate_questions_batch(
    chunks_batch: List[Dict],
    num_questions_per_chunk: int = 2
) -> List[Dict]:
    """
    Genera preguntas para un lote de chunks en UNA SOLA llamada a Groq
    
    OPTIMIZACIÓN: Procesa 10 chunks a la vez en lugar de uno por uno
    Esto reduce de 153 llamadas a 15 llamadas (10x más rápido)
    
    Args:
        chunks_batch: Lista de chunks (cada uno con id, chunk_index, chunk_text)
        num_questions_per_chunk: Preguntas por chunk
        
    Returns:
        List[Dict]: Preguntas con metadatos
    """
    
    # Validar GROQ_API_KEY antes de llamar
    if not GROQ_API_KEY:
        print("❌ GROQ_API_KEY no configurada en generate_questions_batch")
        return []
    
    # Construir prompt para procesar TODO el lote
    # MEJORA GPT: Mezcla de preguntas literales (50%) e inferenciales (50%)
    system_prompt = """Eres un profesor universitario experto en Active Recall y pedagogía.

TAREA: Generar preguntas variadas para MÚLTIPLES fragmentos de un texto.

REGLAS IMPORTANTES:
1. Para CADA fragmento, genera exactamente las preguntas solicitadas
2. MEZCLA de tipos de preguntas (aproximadamente 50/50):
   - LITERALES: Datos específicos del texto (qué, quién, cuándo, dónde, cuántos)
   - INFERENCIALES: Requieren razonar, analizar causas, consecuencias, intenciones
3. Las preguntas deben ser específicas al contenido de cada fragmento
4. Usar terminología del texto original
5. Fomentar tanto comprensión factual como pensamiento crítico

EJEMPLOS:
- Literal: "¿Qué objeto recibía Henriette cada año como regalo?"
- Inferencial: "¿Por qué crees que el personaje sospechaba del mayordomo?"

FORMATO JSON ESTRICTO:
{
  "chunks": [
    {
      "chunk_index": 0,
      "questions": ["Pregunta 1", "Pregunta 2"]
    },
    {
      "chunk_index": 1,
      "questions": ["Pregunta 1", "Pregunta 2"]
    }
  ]
}

Responde SOLO con JSON válido, sin texto adicional ni marcadores markdown."""

    # Construir user_prompt con todos los chunks del lote
    chunks_text = ""
    for chunk in chunks_batch:
        chunks_text += f"\n--- FRAGMENTO {chunk['chunk_index']} ---\n{chunk['chunk_text']}\n"
    
    user_prompt = f"""Genera {num_questions_per_chunk} preguntas de Active Recall para cada uno de estos {len(chunks_batch)} fragmentos:

{chunks_text}

Formato JSON con array "chunks"."""

    try:
        client = AsyncGroq(api_key=GROQ_API_KEY)
        
        completion = await client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=4000,  # Más tokens para procesar lote
            response_format={"type": "json_object"}
        )
        
        response_text = completion.choices[0].message.content
        
        # MEJORA GPT: Limpiar posibles marcadores markdown (robustez)
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        response_json = json.loads(response_text)
        
        # Mapear preguntas con metadatos
        all_questions = []
        chunks_data = response_json.get("chunks", [])
        
        for chunk_data in chunks_data:
            chunk_idx = chunk_data.get("chunk_index")
            questions = chunk_data.get("questions", [])
            
            # Encontrar el chunk original
            original_chunk = next((c for c in chunks_batch if c['chunk_index'] == chunk_idx), None)
            
            if original_chunk:
                for question_text in questions:
                    if isinstance(question_text, str) and question_text.strip():
                        # Clasificar tipo de pregunta (literal/inferential/other)
                        q_type = classify_question_type(question_text.strip())
                        
                        all_questions.append({
                            "question": question_text.strip(),
                            "question_type": q_type,  # 👈 NUEVO: tipo de pregunta
                            "chunk_id": original_chunk['id'],
                            "chunk_index": original_chunk['chunk_index'],
                            "source_preview": original_chunk['chunk_text'][:150] + "..."
                        })
            else:
                # MEJORA GPT: Loguear cuando no se encuentra el chunk
                print(f"   ⚠️ chunk_index {chunk_idx} no encontrado en el lote original")
        
        return all_questions
        
    except json.JSONDecodeError as e:
        print(f"\n❌ Error parseando JSON en lote: {e}")
        print(f"   Respuesta recibida: {response_text[:200]}...")
        return []
    
    except Exception as e:
        print(f"\n❌ Error en lote: {e}")
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
