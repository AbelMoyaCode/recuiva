#!/usr/bin/env python3
"""
Recuiva Backend API - Sistema de Active Recall con Validación Semántica
FastAPI backend con embeddings y base de datos vectorial

Autor: Abel Jesús Moya Acosta
Fecha: 7 de octubre de 2025
Proyecto: Taller Integrador I - UPAO
Versión: 1.1.0 - URLs dinámicas para producción
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv
import argparse
import sys
from pathlib import Path
import numpy as np

# Agregar el directorio backend al path para imports locales
BACKEND_DIR = Path(__file__).parent
sys.path.insert(0, str(BACKEND_DIR))

# Importar módulos locales
try:
    from embeddings_module import generate_embeddings, calculate_similarity, load_model
    from chunking import chunk_text, extract_text_from_pdf, get_text_stats
    from semantic_validator import SemanticValidator
    from supabase_client import get_supabase_client, test_connection
    MODULES_LOADED = True
    SUPABASE_ENABLED = True
except ImportError as e:
    print(f"⚠️ Módulos locales no encontrados: {e}")
    print("⚠️ Asegúrate de tener embeddings_module.py, chunking.py y semantic_validator.py")
    MODULES_LOADED = False
    SUPABASE_ENABLED = False

# Cargar variables de entorno
load_dotenv()

# Crear aplicación FastAPI
app = FastAPI(
    title="Recuiva API",
    description="Sistema de Active Recall con Validación Semántica mediante IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS - Permitir todos los orígenes en desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes
    allow_credentials=False,  # Debe ser False cuando allow_origins es ["*"]
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los headers
    expose_headers=["*"]  # Exponer todos los headers en la respuesta
)

# ==================== MODELOS PYDANTIC ====================

class Question(BaseModel):
    id: int
    text: str
    topic: str
    difficulty: str
    material_id: Optional[int] = None

class Answer(BaseModel):
    question_id: Optional[int] = None  # Para preguntas guardadas
    question_text: Optional[str] = None  # Para preguntas dinámicas
    material_id: Optional[str] = None  # UUID del material en Supabase
    user_answer: str

class Material(BaseModel):
    title: str
    topic: Optional[str] = None
    content: str

class ValidationResult(BaseModel):
    score: float
    is_correct: bool
    feedback: str
    similarity: float
    best_match_chunk: Optional[dict] = None  # Ahora es dict con info completa
    relevant_chunks: Optional[List[dict]] = []  # Lista de chunks relevantes

class MaterialResponse(BaseModel):
    id: int
    filename: str
    title: str
    uploaded_at: str
    total_chunks: int
    total_characters: int
    estimated_pages: int
    real_pages: Optional[int] = None  # Páginas reales del PDF (si aplica)

class ValidateAnswerRequest(BaseModel):
    question_text: str
    user_answer: str
    material_id: str  # UUID del material

# ==================== CONFIGURACIÓN ====================

# Rutas del sistema de archivos
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
MATERIALS_DIR = DATA_DIR / "materials"
MATERIALS_INDEX_FILE = DATA_DIR / "materials_index.json"

# Crear directorios si no existen
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
MATERIALS_DIR.mkdir(parents=True, exist_ok=True)

# Thresholds de validación
THRESHOLD_EXCELLENT = float(os.getenv("SIMILARITY_THRESHOLD_EXCELLENT", "0.9"))
THRESHOLD_GOOD = float(os.getenv("SIMILARITY_THRESHOLD_GOOD", "0.7"))
THRESHOLD_ACCEPTABLE = float(os.getenv("SIMILARITY_THRESHOLD_ACCEPTABLE", "0.5"))

# Configuración de chunking - OPTIMIZADO PARA PDFs DE 25-100+ PÁGINAS
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "1000"))  # ✅ Aumentado para mejor contexto
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "200"))  # ✅ Mayor overlap
MIN_DOCUMENT_SIZE = int(os.getenv("MIN_DOCUMENT_SIZE", "200000"))

# Base de datos en memoria (para desarrollo)
# En producción, usar PostgreSQL o MongoDB
materials_db = []
questions_db = []

# Inicializar validador semántico
semantic_validator = SemanticValidator(
    threshold_excellent=THRESHOLD_EXCELLENT,
    threshold_good=THRESHOLD_GOOD,
    threshold_acceptable=THRESHOLD_ACCEPTABLE
)

# ==================== FUNCIONES AUXILIARES ====================

async def get_current_user(authorization: Optional[str]):
    """Obtener usuario actual desde el token de Supabase"""
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado - Token faltante")
    
    try:
        # El token viene en formato "Bearer <token>"
        token = authorization.replace("Bearer ", "")
        supabase = get_supabase_client()
        
        # Verificar el token con Supabase
        user_response = supabase.auth.get_user(token)
        
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return user_response.user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Error de autenticación: {str(e)}")

# ==================== ENDPOINTS ====================

@app.on_event("startup")
async def startup_event():
    """Inicializar el modelo al arrancar el servidor"""
    print("🚀 Iniciando Recuiva Backend API...")
    print(f"📁 Directorio de datos: {DATA_DIR}")
    print(f"📊 Directorio de embeddings: {EMBEDDINGS_DIR}")
    print(f"📂 Directorio de materiales: {MATERIALS_DIR}")
    
    # Debug: Mostrar variables de entorno de Supabase
    print("\n🔍 Variables de entorno:")
    print(f"   SUPABASE_URL: {'✅ configurada' if os.getenv('SUPABASE_URL') else '❌ NO configurada'}")
    print(f"   SUPABASE_KEY: {'✅ configurada' if os.getenv('SUPABASE_KEY') else '❌ NO configurada'}")
    
    # Probar conexión a Supabase
    if SUPABASE_ENABLED:
        print("\n🔌 Conectando a Supabase...")
        if test_connection():
            print("✅ Base de datos Supabase conectada")
        else:
            print("⚠️ No se pudo conectar a Supabase - usando almacenamiento local")
    else:
        print("\n⚠️ Módulos de Supabase no cargados - modo sin base de datos")
    
    # Cargar índice de materiales
    load_materials_index()
    
    # Precargar modelo de embeddings solo si los módulos están disponibles
    if MODULES_LOADED:
        try:
            load_model()
            print("✅ Modelo de embeddings cargado exitosamente")
        except Exception as e:
            print(f"⚠️ Error cargando modelo: {e}")
    else:
        print("⚠️ Módulos de embeddings no disponibles - modo limitado")
    
    # Ya no necesitamos load_existing_materials() porque usamos índice persistente
    # load_existing_materials()
    print(f"📚 Materiales en índice: {len(materials_db)}")
    print("\n✅ Backend listo y escuchando en http://localhost:8000")
    print("📖 Documentación disponible en http://localhost:8000/docs\n")

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Recuiva API - Sistema de Active Recall con IA",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "documentation": "/docs",
            "upload": "/api/materials/upload",
            "validate": "/api/validate-answer",
            "questions": "/api/questions",
            "materials": "/api/materials",
            "stats": "/api/stats"
        },
        "stats": {
            "total_materials": len(materials_db),
            "total_questions": len(questions_db)
        }
    }

@app.post("/api/materials/upload")
async def upload_material(
    file: UploadFile = File(...),
    user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    """
    Endpoint para subir materiales (PDF o TXT)
    Procesa, chunkinea, vectoriza y guarda en Supabase
    
    Args:
        file: Archivo PDF o TXT (mínimo 80 páginas recomendado)
        user_id: ID del usuario autenticado (desde header X-User-ID)
        
    Returns:
        Información del material procesado
    """
    try:
        # IMPORTANTE: Requiere autenticación real
        # El user_id DEBE venir del header X-User-ID enviado por el frontend
        # después de que el usuario se autentique con Supabase Auth
        if SUPABASE_ENABLED and not user_id:
            print("⚠️ ADVERTENCIA: No se recibió user_id en el header X-User-ID")
            print("   Asegúrate de que el usuario esté autenticado en el frontend")
            raise HTTPException(
                status_code=401,
                detail="No autenticado. Debes iniciar sesión primero."
            )
        
        # Validar tipo de archivo
        if not file.filename.endswith(('.pdf', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="Solo se permiten archivos PDF o TXT"
            )
        
        print(f"📥 Recibiendo archivo: {file.filename}")
        
        # Leer contenido
        content = await file.read()
        
        # Extraer texto según el tipo de archivo
        pdf_page_count = None
        if file.filename.endswith('.pdf'):
            print("📄 Extrayendo texto de PDF...")
            text, pdf_page_count = extract_text_from_pdf(content)
            print(f"📄 PDF con {pdf_page_count} páginas reales")
        else:
            text = content.decode('utf-8')
            pdf_page_count = None
        
        # Obtener estadísticas del texto (pasando el conteo real de páginas del PDF)
        stats = get_text_stats(text, real_pages=pdf_page_count)
        
        print(f"📊 Estadísticas del documento:")
        print(f"   📄 Páginas: {stats['real_pages']}")
        print(f"   📝 Caracteres: {stats['characters']:,}")
        print(f"   📚 Palabras: {stats['words']:,}")
        print(f"   ✂️ Chunk size: {DEFAULT_CHUNK_SIZE} | Overlap: {DEFAULT_CHUNK_OVERLAP}")
        
        # Validar tamaño mínimo (aprox 80 páginas = ~200,000 caracteres)
        if len(text) < MIN_DOCUMENT_SIZE:
            print(f"⚠️ Advertencia: Documento pequeño ({len(text)} caracteres)")
            # Permitir pero advertir
        
        # Chunking del texto
        print("✂️ Dividiendo en chunks...")
        chunks = chunk_text(text, chunk_size=DEFAULT_CHUNK_SIZE, overlap=DEFAULT_CHUNK_OVERLAP)
        print(f"✅ Generados {len(chunks)} chunks")
        
        # Generar embeddings para cada chunk
        print("🧠 Generando embeddings...")
        embeddings_data = []
        
        for i, chunk in enumerate(chunks):
            if i % 10 == 0:
                print(f"   Procesando chunk {i+1}/{len(chunks)}...")
            
            embedding = generate_embeddings(chunk)
            embeddings_data.append({
                "chunk_id": i,
                "text": chunk[:200] + "..." if len(chunk) > 200 else chunk,  # Guardar preview
                "text_full": chunk,  # Texto completo
                "embedding": embedding.tolist()
            })
        
        print(f"✅ Embeddings generados: {len(embeddings_data)}")
        
        # ===== GUARDAR EN SUPABASE (SI ESTÁ HABILITADO) =====
        if SUPABASE_ENABLED and user_id:
            print(f"\n💾 Guardando en Supabase para usuario: {user_id}")
            try:
                supabase = get_supabase_client()
                
                # Preparar datos para Supabase
                title = file.filename.replace('.pdf', '').replace('.txt', '').replace('_', ' ').title()
                file_type = 'pdf' if file.filename.endswith('.pdf') else 'txt'
                
                # Insertar en tabla materials
                material_insert = {
                    "user_id": user_id,
                    "title": title,
                    "file_name": file.filename,
                    "file_type": file_type,
                    "total_chunks": len(chunks),
                    "total_characters": len(text),
                    "estimated_pages": stats["real_pages"],  # Usar páginas reales del PDF
                    "processing_status": "completed"
                    # file_path y storage_path los dejamos NULL por ahora
                }
                
                result = supabase.table('materials').insert(material_insert).execute()
                
                if result.data and len(result.data) > 0:
                    material_uuid = result.data[0]['id']
                    print(f"✅ Material guardado en Supabase con UUID: {material_uuid}")
                    
                    # ===== GUARDAR EMBEDDINGS EN SUPABASE CON PGVECTOR =====
                    print(f"💾 Guardando {len(embeddings_data)} embeddings en Supabase...")
                    
                    # Preparar datos para inserción batch
                    embeddings_to_insert = []
                    for i, emb_data in enumerate(embeddings_data):
                        embeddings_to_insert.append({
                            "material_id": material_uuid,
                            "chunk_index": i,
                            "chunk_text": emb_data["text_full"],
                            "embedding": emb_data["embedding"]  # pgvector acepta arrays directamente
                        })
                        
                        # Insertar en batches de 100 para evitar timeouts
                        if len(embeddings_to_insert) == 100 or i == len(embeddings_data) - 1:
                            batch_result = supabase.table('material_embeddings').insert(embeddings_to_insert).execute()
                            if batch_result.data:
                                print(f"   ✅ Batch {(i // 100) + 1}: {len(embeddings_to_insert)} embeddings guardados")
                            embeddings_to_insert = []
                    
                    print(f"✅ Todos los embeddings guardados en Supabase (pgvector)")
                    
                    # Retornar respuesta con UUID de Supabase
                    return {
                        "success": True,
                        "material_id": material_uuid,
                        "message": f"Material procesado y guardado en Supabase: {len(chunks)} chunks generados",
                        "data": {
                            "id": material_uuid,
                            "user_id": user_id,
                            "title": title,
                            "filename": file.filename,
                            "file_type": file_type,
                            "total_chunks": len(chunks),
                            "total_characters": len(text),
                            "estimated_pages": stats["estimated_pages"],
                            "real_pages": stats.get("real_pages", None),
                            "created_at": result.data[0].get('created_at')
                        }
                    }
                else:
                    raise Exception("No se recibió respuesta de Supabase")
                    
            except Exception as db_error:
                print(f"❌ Error guardando en Supabase: {db_error}")
                print("⚠️ Continuando con almacenamiento local...")
                # Si falla Supabase, continuar con método local
        
        # ===== FALLBACK: GUARDAR LOCAL (SI SUPABASE NO ESTÁ DISPONIBLE) =====
        print(f"\n💾 Guardando localmente (Supabase no disponible)")
        material_id = get_next_material_id()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Guardar archivo original
        original_filename = file.filename
        safe_filename = f"{original_filename.rsplit('.', 1)[0]}_{material_id}_{timestamp}.{original_filename.rsplit('.', 1)[1]}"
        material_file_path = MATERIALS_DIR / safe_filename
        
        print(f"💾 Guardando archivo original: {material_file_path}")
        with open(material_file_path, 'wb') as f:
            f.write(content)
        
        material_data = {
            "id": material_id,
            "filename": file.filename,
            "saved_filename": safe_filename,
            "file_path": str(material_file_path),
            "file_exists": True,
            "title": file.filename.replace('.pdf', '').replace('.txt', '').replace('_', ' ').title(),
            "uploaded_at": timestamp,
            "total_chunks": len(chunks),
            "total_characters": len(text),
            "estimated_pages": stats["estimated_pages"],
            "real_pages": stats.get("real_pages", None)  # Páginas reales del PDF
        }
        
        materials_db.append(material_data)
        save_materials_index()  # Guardar índice persistente
        
        # Guardar embeddings en archivo JSON
        embeddings_file = EMBEDDINGS_DIR / f"material_{material_id}_{timestamp}.json"
        print(f"💾 Guardando embeddings en: {embeddings_file}")
        
        with open(embeddings_file, 'w', encoding='utf-8') as f:
            json.dump(embeddings_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Material {material_id} procesado exitosamente")
        
        return {
            "success": True,
            "material_id": material_id,
            "message": f"Material procesado exitosamente: {len(chunks)} chunks generados",
            "data": material_data
        }
    
    except Exception as e:
        print(f"❌ Error procesando material: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error procesando material: {str(e)}")

@app.post("/api/validate-answer", response_model=ValidationResult)
async def validate_answer(answer: Answer):
    """
    Valida semánticamente la respuesta del usuario con SCORING INTELIGENTE
    - Análisis multi-chunk (top 5)
    - Palabras clave contextuales
    - Bonus por elaboración
    - Boost de inteligencia para variaciones
    
    Args:
        answer: Respuesta del usuario con ID de pregunta O texto de pregunta directa
        
    Returns:
        ValidationResult: Resultado de la validación con score y feedback
    """
    try:
        print(f"\n{'='*70}")
        print(f"🔍 VALIDACIÓN SEMÁNTICA INTELIGENTE")
        print(f"{'='*70}")
        
        # ===== DETERMINAR PREGUNTA Y MATERIAL =====
        question_text = None
        material_id = answer.material_id  # UUID de Supabase
        
        if answer.question_id:
            # Pregunta guardada
            question = next((q for q in questions_db if q["id"] == answer.question_id), None)
            if not question:
                raise HTTPException(status_code=404, detail="Pregunta no encontrada")
            question_text = question.get("text", "")
            material_id = question.get("material_id", material_id)
            print(f"📝 Pregunta guardada ID: {answer.question_id}")
        elif answer.question_text:
            # Pregunta dinámica
            question_text = answer.question_text
            print(f"📝 Pregunta dinámica: {question_text[:50]}...")
        else:
            raise HTTPException(status_code=400, detail="Debe proporcionar question_id o question_text")
        
        print(f"✍️  Respuesta: {answer.user_answer[:100]}...")
        print(f"📏 Longitud: {len(answer.user_answer)} caracteres")
        
        # ===== VALIDACIÓN CON SEMANTIC_VALIDATOR =====
        # Usar el módulo SemanticValidator (algoritmo documentado)
        
        # Validar longitud mínima
        try:
            # ===== CARGAR EMBEDDINGS DESDE SUPABASE CON PGVECTOR =====
            if SUPABASE_ENABLED:
                print(f"📂 Cargando embeddings desde Supabase para material: {material_id}")
                supabase = get_supabase_client()
                
                # 1. Obtener información del material (para saber las páginas reales)
                material_info = supabase.table('materials')\
                    .select('estimated_pages, total_chunks')\
                    .eq('id', material_id)\
                    .single()\
                    .execute()
                
                if not material_info.data:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Material {material_id} no encontrado"
                    )
                
                real_pages = material_info.data.get('estimated_pages', 1)
                total_chunks_db = material_info.data.get('total_chunks', 0)
                
                print(f"📄 Material tiene {real_pages} páginas y {total_chunks_db} chunks")
                
                # 2. Obtener embeddings desde Supabase
                embeddings_result = supabase.table('material_embeddings')\
                    .select('chunk_index, chunk_text, embedding')\
                    .eq('material_id', material_id)\
                    .order('chunk_index')\
                    .execute()
                
                if not embeddings_result.data or len(embeddings_result.data) == 0:
                    raise HTTPException(
                        status_code=404,
                        detail=f"No se encontraron embeddings para el material {material_id}"
                    )
                
                # Convertir a formato esperado por SemanticValidator
                material_embeddings = []
                for emb in embeddings_result.data:
                    chunk_text = emb['chunk_text']
                    # IMPORTANTE: Convertir el embedding de string a numpy array
                    embedding_vector = emb['embedding']
                    if isinstance(embedding_vector, str):
                        # Si es string, convertir a lista
                        embedding_vector = json.loads(embedding_vector)
                    if isinstance(embedding_vector, list):
                        # Convertir lista a numpy array
                        embedding_vector = np.array(embedding_vector, dtype=np.float32)
                    
                    material_embeddings.append({
                        "chunk_id": emb['chunk_index'],
                        "text": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                        "text_full": chunk_text,
                        "embedding": embedding_vector
                    })
                
                print(f"📚 {len(material_embeddings)} chunks cargados desde Supabase")
                
            else:
                # Fallback: cargar desde archivos JSON locales
                embeddings_files = list(EMBEDDINGS_DIR.glob(f"material_{material_id}_*.json"))
                
                if not embeddings_files:
                    embeddings_files = list(EMBEDDINGS_DIR.glob("material_*.json"))
                    if not embeddings_files:
                        raise HTTPException(
                            status_code=404, 
                            detail="No hay materiales procesados. Sube un material primero."
                        )
                
                print(f"📂 Cargando: {embeddings_files[0].name}")
                with open(embeddings_files[0], 'r', encoding='utf-8') as f:
                    material_embeddings = json.load(f)
                
                print(f"📚 {len(material_embeddings)} chunks disponibles")
            
            # ✅ FIX: Generar embedding SOLO de la respuesta del usuario (no combinar con pregunta)
            # Esto mejora la precisión semántica al buscar chunks que responden directamente
            user_embedding = generate_embeddings(answer.user_answer)
            print(f"🧠 Embedding generado (dim: {len(user_embedding)})")
            
            # Validar con SemanticValidator
            classification, top_chunks, best_match = semantic_validator.validate_answer(
                user_embedding=user_embedding,
                material_chunks=material_embeddings,
                user_answer=answer.user_answer,
                question_text=question_text
            )
            
            # Imprimir desglose del scoring
            print(f"\n📊 DESGLOSE DEL SCORE:")
            details = classification['scoring_details']
            print(f"   Base (similitud):     {details['base_similarity']}%")
            print(f"   + Contexto amplio:    {details['context_bonus']}%")
            print(f"   + Palabras clave:     {details['keyword_bonus']}%")
            print(f"   + Elaboración:        {details['length_bonus']}%")
            print(f"   + Boost inteligencia: {details['intelligence_boost']}%")
            print(f"   {'─'*40}")
            print(f"   SCORE FINAL:          {classification['score_porcentaje']}%")
            print(f"\n✅ Validación completada: {classification['score_porcentaje']}% {'✓' if classification['es_correcto'] else '✗'}")
            print(f"{'='*70}\n")
            
            # Calcular posición del chunk
            total_chunks = len(material_embeddings)
            best_chunk_position = best_match["chunk_id"]
            
            # Calcular página estimada correctamente:
            # Si tenemos 397 chunks en 25 páginas, cada página tiene ~15.88 chunks
            # Página estimada = (chunk_index / total_chunks) * total_pages
            estimated_page = int((best_chunk_position / max(total_chunks, 1)) * real_pages) + 1
            
            print(f"📍 Chunk más relevante: {best_chunk_position + 1}/{total_chunks} → Página ~{estimated_page}/{real_pages}")
            
            # Construir resultado
            result = ValidationResult(
                score=classification['score_porcentaje'],
                is_correct=classification['es_correcto'],
                similarity=float(best_match['similarity']),
                feedback=classification['feedback'],
                relevant_chunks=[
                    {
                        "text": chunk["text_short"],
                        "text_full": chunk["text"],
                        "similarity": chunk["similarity"],
                        "position": chunk["chunk_id"],
                        "total_chunks": total_chunks
                    }
                    for chunk in top_chunks
                ],
                best_match_chunk={
                    "text": best_match["text"],
                    "text_short": best_match["text_short"],
                    "similarity": best_match["similarity"],
                    "chunk_id": best_chunk_position,
                    "total_chunks": total_chunks,
                    "estimated_page": estimated_page,
                    "total_pages": real_pages
                }
            )
            
            return result
            
        except ValueError as ve:
            # Error de validación (respuesta muy corta)
            print(f"❌ Error de validación: {str(ve)}")
            return ValidationResult(
                score=0.0,
                is_correct=False,
                similarity=0.0,
                feedback=f"❌ {str(ve)}",
                relevant_chunks=[],
                best_match_chunk=None
            )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ===================================================================
# ENDPOINT: OBTENER MATERIALES
# ===================================================================
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error validando respuesta: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error validando respuesta: {str(e)}")

@app.get("/api/materials")
async def get_materials():
    """Obtiene la lista de todos los materiales subidos desde Supabase"""
    try:
        if SUPABASE_ENABLED:
            supabase = get_supabase_client()
            
            # Obtener todos los materiales de Supabase
            result = supabase.table('materials')\
                .select('*')\
                .order('created_at', desc=True)\
                .execute()
            
            materials = result.data if result.data else []
            
            print(f"📚 Materiales obtenidos de Supabase: {len(materials)}")
            
            return {
                "success": True,
                "total": len(materials),
                "materials": materials
            }
        else:
            # Fallback a materials_db local
            return {
                "success": True,
                "total": len(materials_db),
                "materials": materials_db
            }
    except Exception as e:
        print(f"❌ Error obteniendo materiales: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/materials/{material_id}")
async def get_material(material_id: str):
    """Obtiene los detalles de un material específico desde Supabase"""
    try:
        if SUPABASE_ENABLED:
            supabase = get_supabase_client()
            result = supabase.table('materials')\
                .select('*')\
                .eq('id', material_id)\
                .single()\
                .execute()
            
            if result.data:
                return {
                    "success": True,
                    "material": result.data
                }
            else:
                raise HTTPException(status_code=404, detail="Material no encontrado")
        else:
            # Fallback local
            material = next((m for m in materials_db if m["id"] == material_id), None)
            if not material:
                raise HTTPException(status_code=404, detail="Material no encontrado")
            return {
                "success": True,
                "material": material
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error obteniendo material: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/materials/{material_id}")
async def delete_material(material_id: str):
    """
    Elimina un material y todos sus registros asociados de Supabase
    - Elimina embeddings (CASCADE desde material_embeddings)
    - Elimina preguntas y respuestas (CASCADE)
    - Elimina registro del material
    """
    try:
        if SUPABASE_ENABLED:
            supabase = get_supabase_client()
            
            # Verificar que existe
            material = supabase.table('materials')\
                .select('id, title, file_name')\
                .eq('id', material_id)\
                .single()\
                .execute()
            
            if not material.data:
                raise HTTPException(status_code=404, detail=f"Material {material_id} no encontrado")
            
            print(f"🗑️ Eliminando material: {material.data.get('title') or material.data.get('file_name')}")
            
            # Eliminar material (CASCADE eliminará embeddings automáticamente)
            delete_result = supabase.table('materials')\
                .delete()\
                .eq('id', material_id)\
                .execute()
            
            print(f"✅ Material eliminado exitosamente de Supabase")
            
            return {
                "success": True,
                "message": "Material eliminado correctamente",
                "material_id": material_id
            }
        else:
            # Fallback: eliminar de materials_db local
            global materials_db
            material = next((m for m in materials_db if m["id"] == material_id), None)
            if not material:
                raise HTTPException(status_code=404, detail=f"Material {material_id} no encontrado")
            
            materials_db = [m for m in materials_db if m["id"] != material_id]
            
            return {
                "success": True,
                "message": "Material eliminado",
                "material_id": material_id
            }
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error eliminando material: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
        # 2. Eliminar archivo original si existe
        if material.get("file_path"):
            try:
                file_path = Path(material["file_path"])
                if file_path.exists():
                    file_path.unlink()
                    deleted_files.append(str(file_path.name))
                    print(f"🗑️ Archivo original eliminado: {file_path.name}")
            except Exception as e:
                errors.append(f"Error eliminando archivo original: {str(e)}")
        
        # También buscar por saved_filename
        if material.get("saved_filename"):
            try:
                saved_file = MATERIALS_DIR / material["saved_filename"]
                if saved_file.exists():
                    saved_file.unlink()
                    deleted_files.append(str(saved_file.name))
                    print(f"🗑️ Archivo guardado eliminado: {saved_file.name}")
            except Exception as e:
                errors.append(f"Error eliminando archivo guardado: {str(e)}")
        
        # 3. Eliminar de la base de datos en memoria
        materials_db = [m for m in materials_db if m["id"] != material_id]
        save_materials_index()  # Guardar cambios en el índice
        
        print(f"✅ Material {material_id} eliminado exitosamente")
        print(f"   - Archivos eliminados: {len(deleted_files)}")
        print(f"   - Errores: {len(errors)}")
        
        return {
            "success": True,
            "message": f"Material '{material.get('filename', material_id)}' eliminado exitosamente",
            "material": material,
            "deleted_files": deleted_files,
            "files_deleted_count": len(deleted_files),
            "errors": errors if errors else None
        }
        
    except Exception as e:
        print(f"❌ Error eliminando material {material_id}: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error al eliminar material: {str(e)}"
        )

@app.post("/api/questions")
async def create_question(question: Question):
    """Crea una nueva pregunta"""
    question_data = question.dict()
    question_data["created_at"] = datetime.now().isoformat()
    questions_db.append(question_data)
    
    print(f"➕ Nueva pregunta creada: {question.text[:50]}...")
    
    return {
        "success": True,
        "question": question_data
    }

@app.get("/api/questions")
async def get_questions(topic: Optional[str] = None, difficulty: Optional[str] = None):
    """Obtiene preguntas filtradas por tema y/o dificultad"""
    filtered_questions = questions_db
    
    if topic:
        filtered_questions = [q for q in filtered_questions if q.get("topic") == topic]
    
    if difficulty:
        filtered_questions = [q for q in filtered_questions if q.get("difficulty") == difficulty]
    
    return {
        "success": True,
        "total": len(filtered_questions),
        "questions": filtered_questions
    }

@app.get("/api/stats")
async def get_stats():
    """Obtiene estadísticas generales del sistema"""
    # Contar embeddings totales
    total_embeddings = 0
    total_size = 0
    
    for file in EMBEDDINGS_DIR.glob("*.json"):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                total_embeddings += len(data)
            total_size += file.stat().st_size
        except:
            pass
    
    return {
        "success": True,
        "stats": {
            "total_materials": len(materials_db),
            "total_questions": len(questions_db),
            "total_embeddings": total_embeddings,
            "storage_used_mb": round(total_size / (1024 * 1024), 2),
            "embeddings_files": len(list(EMBEDDINGS_DIR.glob("*.json")))
        }
    }

@app.get("/api/health")
async def health_check():
    """Endpoint de health check para monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": True  # Verificar si el modelo está cargado
    }

# ==================== FUNCIONES AUXILIARES ====================

def load_materials_index():
    """Carga el índice de materiales desde el archivo JSON"""
    global materials_db
    if MATERIALS_INDEX_FILE.exists():
        try:
            with open(MATERIALS_INDEX_FILE, 'r', encoding='utf-8') as f:
                materials_db = json.load(f)
            print(f"📚 Índice de materiales cargado: {len(materials_db)} materiales")
        except Exception as e:
            print(f"⚠️ Error cargando índice de materiales: {e}")
            materials_db = []
    else:
        print("📝 No existe índice, migrando materiales existentes...")
        materials_db = []
        # Migrar automáticamente desde embeddings
        migrate_existing_materials()
        save_materials_index()

def migrate_existing_materials():
    """Migra materiales existentes desde embeddings al índice"""
    global materials_db
    
    for file in sorted(EMBEDDINGS_DIR.glob("material_*.json")):
        try:
            parts = file.stem.split('_')
            if len(parts) >= 3:
                material_id = int(parts[1])
                timestamp = parts[2]
                
                # Verificar si ya existe
                if any(m["id"] == material_id for m in materials_db):
                    continue
                
                # Cargar datos del embedding
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Buscar archivo original
                pdf_files = list(MATERIALS_DIR.glob(f"*_{material_id}_*"))
                saved_filename = pdf_files[0].name if pdf_files else None
                file_path = str(pdf_files[0]) if pdf_files else None
                file_exists = bool(pdf_files)
                original_filename = saved_filename.split(f"_{material_id}_")[0] + pdf_files[0].suffix if pdf_files else f"material_{material_id}"
                
                materials_db.append({
                    "id": material_id,
                    "filename": original_filename,
                    "saved_filename": saved_filename,
                    "file_path": file_path,
                    "file_exists": file_exists,
                    "title": original_filename.replace('.pdf', '').replace('.txt', '').replace('_', ' ').title(),
                    "uploaded_at": timestamp,
                    "total_chunks": len(data),
                    "total_characters": sum(len(chunk.get("text_full", "")) for chunk in data),
                    "estimated_pages": len(data) // 3
                })
                print(f"  ✅ Migrado material {material_id}: {original_filename}")
        except Exception as e:
            print(f"  ⚠️ Error migrando {file.name}: {e}")

def save_materials_index():
    """Guarda el índice de materiales en el archivo JSON"""
    try:
        with open(MATERIALS_INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(materials_db, f, ensure_ascii=False, indent=2)
        print(f"💾 Índice de materiales guardado: {len(materials_db)} materiales")
    except Exception as e:
        print(f"❌ Error guardando índice de materiales: {e}")

def get_next_material_id():
    """Obtiene el siguiente ID disponible para materiales"""
    if not materials_db:
        return 1
    return max(m["id"] for m in materials_db) + 1

def load_existing_materials():
    """Carga materiales existentes del directorio de embeddings"""
    global materials_db
    
    for file in EMBEDDINGS_DIR.glob("material_*.json"):
        try:
            # Extraer información del nombre del archivo
            # Formato: material_{id}_{timestamp}.json
            parts = file.stem.split('_')
            if len(parts) >= 3:
                material_id = int(parts[1])
                timestamp = parts[2]
                
                # Cargar datos del embedding para obtener información
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Agregar a la base de datos si no existe
                if not any(m["id"] == material_id for m in materials_db):
                    materials_db.append({
                        "id": material_id,
                        "filename": f"material_{material_id}",
                        "title": f"Material {material_id}",
                        "uploaded_at": timestamp,
                        "total_chunks": len(data),
                        "total_characters": sum(len(chunk.get("text_full", "")) for chunk in data),
                        "estimated_pages": 0
                    })
        except Exception as e:
            print(f"⚠️ Error cargando material {file}: {e}")

# ==================== SPRINT 2: ENDPOINTS DE TÓPICOS Y GENERACIÓN AUTOMÁTICA ====================

# Importar el generador de preguntas
try:
    from question_generator import generate_questions_dict
    QUESTION_GENERATOR_ENABLED = True
except ImportError:
    print("⚠️ question_generator.py no encontrado. Funcionalidad de generación automática deshabilitada.")
    QUESTION_GENERATOR_ENABLED = False

class TopicCreate(BaseModel):
    name: str
    description: Optional[str] = None
    folder_id: Optional[str] = None  # SPRINT 2: Relación con carpeta

class TopicResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    folder_id: Optional[str]  # SPRINT 2: Relación con carpeta
    created_at: str

class GenerateQuestionsRequest(BaseModel):
    num_questions: int = 5
    strategy: str = "random"  # random, diverse, sequential

@app.post("/api/topics", response_model=TopicResponse)
async def create_topic(topic: TopicCreate, authorization: Optional[str] = Header(None)):
    """Crear un nuevo tópico/tema"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase no está disponible")
    
    try:
        supabase = get_supabase_client()
        user = await get_current_user(authorization)
        
        topic_data = {
            'user_id': user['id'],
            'name': topic.name,
            'description': topic.description
        }
        
        # SPRINT 2: Incluir folder_id si está presente
        if topic.folder_id:
            topic_data['folder_id'] = topic.folder_id
        
        result = supabase.table('topics').insert(topic_data).execute()
        
        return result.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando tópico: {str(e)}")

@app.get("/api/topics", response_model=List[TopicResponse])
async def get_topics(authorization: Optional[str] = Header(None)):
    """Obtener todos los tópicos del usuario"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase no está disponible")
    
    try:
        supabase = get_supabase_client()
        user = await get_current_user(authorization)
        
        result = supabase.table('topics').select('*').eq('user_id', user['id']).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo tópicos: {str(e)}")

@app.post("/api/materials/{material_id}/assign-topic")
async def assign_topic_to_material(material_id: str, topic_id: str, authorization: Optional[str] = Header(None)):
    """Asignar un tópico a un material"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase no está disponible")
    
    try:
        supabase = get_supabase_client()
        user = await get_current_user(authorization)
        
        result = supabase.table('materials').update({
            'topic_id': topic_id
        }).eq('id', material_id).eq('user_id', user['id']).execute()
        
        return {"success": True, "material_id": material_id, "topic_id": topic_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error asignando tópico: {str(e)}")

@app.post("/api/materials/{material_id}/generate-questions")
async def generate_questions_for_material(
    material_id: str, 
    request: GenerateQuestionsRequest,
    authorization: Optional[str] = Header(None)
):
    """Generar preguntas automáticamente desde un material"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase no está disponible")
    
    if not QUESTION_GENERATOR_ENABLED:
        raise HTTPException(status_code=503, detail="Generador de preguntas no disponible")
    
    try:
        supabase = get_supabase_client()
        # ✅ NO requerir autenticación por ahora (el material_id ya identifica al usuario)
        # user = await get_current_user(authorization)
        
        # Obtener chunks del material
        print(f"🔍 Buscando chunks para material: {material_id}")
        chunks_result = supabase.table('material_embeddings').select('chunk_text').eq('material_id', material_id).order('chunk_index').execute()
        
        if not chunks_result.data:
            raise HTTPException(status_code=404, detail="Material no encontrado o sin chunks")
        
        print(f"📚 Chunks encontrados: {len(chunks_result.data)}")
        chunks = [item['chunk_text'] for item in chunks_result.data]
        
        # Generar preguntas usando el módulo question_generator
        print(f"🎯 Generando {request.num_questions} preguntas con estrategia {request.strategy}")
        questions = generate_questions_dict(chunks, request.num_questions, request.strategy)
        
        print(f"✅ Preguntas generadas: {len(questions)}")
        
        # ✅ NO GUARDAR AUTOMÁTICAMENTE - El usuario decide si guarda con "Guardar Pregunta"
        # Solo retornar las preguntas generadas para mostrarlas en el textarea
        
        return {
            "success": True,
            "material_id": material_id,
            "questions_generated": len(questions),
            "questions": questions
        }
    except Exception as e:
        print(f"❌ Error generando preguntas: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generando preguntas: {str(e)}")

@app.get("/api/materials/by-topic/{topic_id}")
async def get_materials_by_topic(topic_id: str, authorization: Optional[str] = Header(None)):
    """Obtener todos los materiales de un tópico"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase no está disponible")
    
    try:
        supabase = get_supabase_client()
        user = await get_current_user(authorization)
        
        result = supabase.table('materials').select('*').eq('topic_id', topic_id).eq('user_id', user['id']).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo materiales: {str(e)}")

@app.post("/api/questions/validate-by-topic")
async def validate_answer_by_topic(answer: Answer, authorization: Optional[str] = Header(None)):
    """Validar respuesta contra múltiples materiales de un tópico"""
    if not SUPABASE_ENABLED:
        raise HTTPException(status_code=503, detail="Supabase no está disponible")
    
    try:
        supabase = get_supabase_client()
        user = await get_current_user(authorization)
        
        # Obtener el material y su tópico
        material = supabase.table('materials').select('topic_id').eq('id', answer.material_id).single().execute()
        
        if not material.data or not material.data.get('topic_id'):
            # Si no tiene tópico, validar solo contra el material
            return await validate_answer(answer)
        
        topic_id = material.data['topic_id']
        
        # Obtener todos los materiales del mismo tópico
        materials = supabase.table('materials').select('id').eq('topic_id', topic_id).eq('user_id', user['id']).execute()
        material_ids = [m['id'] for m in materials.data]
        
        # Obtener chunks de todos los materiales del tópico
        all_chunks = []
        for mat_id in material_ids:
            chunks_result = supabase.table('material_embeddings').select('*').eq('material_id', mat_id).execute()
            all_chunks.extend(chunks_result.data)
        
        if not all_chunks:
            raise HTTPException(status_code=404, detail="No se encontraron chunks en el tópico")
        
        # Generar embedding de la respuesta
        answer_embedding = generate_embeddings([answer.user_answer])[0]
        
        # Calcular similitud con todos los chunks
        similarities = []
        for chunk in all_chunks:
            chunk_embedding = np.array(chunk['embedding'])
            similarity = calculate_similarity(answer_embedding, chunk_embedding)
            similarities.append({
                'chunk': chunk,
                'similarity': float(similarity)
            })
        
        # Ordenar por similitud
        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_chunks = similarities[:5]
        
        # Validación semántica con el mejor chunk
        validator = SemanticValidator()
        best_similarity = top_chunks[0]['similarity']
        
        # Determinar texto de pregunta
        question_text = answer.question_text if answer.question_text else ""
        if answer.question_id and questions_db:
            question = next((q for q in questions_db if q["id"] == answer.question_id), None)
            if question:
                question_text = question.get("text", "")
        
        validation = validator.validate_answer(
            question=question_text,
            user_answer=answer.user_answer,
            reference_chunk=top_chunks[0]['chunk']['chunk_text'],
            similarity_score=best_similarity
        )
        
        return {
            "score": validation['score'],
            "classification": validation['classification'],
            "similarity": best_similarity,
            "is_correct": validation['is_correct'],
            "feedback": validation['feedback'],
            "best_match_chunk": top_chunks[0]['chunk']['chunk_text'],
            "relevant_chunks": [
                {
                    "text": c['chunk']['chunk_text'],
                    "similarity": c['similarity']
                } for c in top_chunks
            ],
            "topic_validation": True,
            "materials_checked": len(material_ids)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validando respuesta por tópico: {str(e)}")

# ==================== FIN SPRINT 2 ====================

# ==================== MAIN ====================

if __name__ == "__main__":
    # Parsear argumentos de línea de comando
    parser = argparse.ArgumentParser(description="Recuiva Backend API")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")),
                      help="Puerto para ejecutar el servidor")
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "0.0.0.0"),
                      help="Host para ejecutar el servidor")
    parser.add_argument("--debug", action='store_true', default=False,
                      help="Modo debug con auto-reload")
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("🚀 Iniciando Recuiva Backend API")
    print("="*50)
    print(f"📍 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"🐛 Debug: {args.debug}")
    print(f"📚 Documentación: http://{args.host}:{args.port}/docs")
    print("="*50 + "\n")
    
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.debug,
        log_level="info"
    )