#!/usr/bin/env python3
"""
Recuiva Backend API - Sistema de Active Recall con Validación Semántica
FastAPI backend con embeddings y base de datos vectorial

Autor: Abel Jesús Moya Acosta
Fecha: 7 de octubre de 2025
Proyecto: Taller Integrador I - UPAO
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
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

# Agregar el directorio backend al path para imports locales
BACKEND_DIR = Path(__file__).parent
sys.path.insert(0, str(BACKEND_DIR))

# Importar módulos locales
try:
    from embeddings_module import generate_embeddings, calculate_similarity, load_model
    from chunking import chunk_text, extract_text_from_pdf, get_text_stats
    MODULES_LOADED = True
except ImportError as e:
    print(f"⚠️ Módulos locales no encontrados: {e}")
    print("⚠️ Asegúrate de tener embeddings_module.py y chunking.py")
    MODULES_LOADED = False

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

# Configurar CORS desde variables de entorno
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    material_id: Optional[int] = None  # Para especificar material directamente
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

# Configuración de chunking
DEFAULT_CHUNK_SIZE = int(os.getenv("DEFAULT_CHUNK_SIZE", "500"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("DEFAULT_CHUNK_OVERLAP", "50"))
MIN_DOCUMENT_SIZE = int(os.getenv("MIN_DOCUMENT_SIZE", "200000"))

# Base de datos en memoria (para desarrollo)
# En producción, usar PostgreSQL o MongoDB
materials_db = []
questions_db = []

# ==================== ENDPOINTS ====================

@app.on_event("startup")
async def startup_event():
    """Inicializar el modelo al arrancar el servidor"""
    print("🚀 Iniciando Recuiva Backend API...")
    print(f"📁 Directorio de datos: {DATA_DIR}")
    print(f"📊 Directorio de embeddings: {EMBEDDINGS_DIR}")
    print(f"📂 Directorio de materiales: {MATERIALS_DIR}")
    
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
async def upload_material(file: UploadFile = File(...)):
    """
    Endpoint para subir materiales (PDF o TXT)
    Procesa, chunkinea y vectoriza el contenido
    
    Args:
        file: Archivo PDF o TXT (mínimo 80 páginas recomendado)
        
    Returns:
        Información del material procesado
    """
    try:
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
        
        # Obtener estadísticas del texto
        stats = get_text_stats(text)
        
        # Usar conteo real de páginas del PDF si está disponible
        if pdf_page_count is not None:
            stats["estimated_pages"] = pdf_page_count
            stats["real_pages"] = pdf_page_count
        
        print(f"📊 Estadísticas: {stats}")
        
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
        
        # Guardar material y embeddings
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
        material_id = answer.material_id or 1
        
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
        
        # ===== VALIDACIONES PREVIAS =====
        MIN_RESPONSE_LENGTH = 15
        if len(answer.user_answer.strip()) < MIN_RESPONSE_LENGTH:
            print(f"❌ Respuesta muy corta")
            return ValidationResult(
                score=0.0,
                is_correct=False,
                similarity=0.0,
                feedback=f"❌ Respuesta muy corta. Active Recall requiere que expliques el concepto con tus propias palabras (mínimo {MIN_RESPONSE_LENGTH} caracteres).",
                relevant_chunks=[],
                best_match_chunk=None
            )
        
        # ===== CARGAR MATERIAL =====
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
        
        # ===== GENERAR EMBEDDINGS =====
        # Combinar pregunta + respuesta para mejor contexto
        combined_text = f"Pregunta: {question_text}\nRespuesta: {answer.user_answer}"
        user_embedding = generate_embeddings(combined_text)
        print(f"� Embedding generado (dim: {len(user_embedding)})")
        
        # ===== CALCULAR SIMILARIDADES (TODOS LOS CHUNKS) =====
        similarities = []
        for idx, chunk_data in enumerate(material_embeddings):
            chunk_embedding = chunk_data["embedding"]
            chunk_text = chunk_data.get("text_full", chunk_data.get("text", ""))
            similarity = calculate_similarity(user_embedding, chunk_embedding)
            
            similarities.append({
                "chunk_id": chunk_data.get("chunk_id", idx),
                "text": chunk_text,
                "text_short": chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text,
                "similarity": float(similarity)
            })
        
        # Ordenar por similaridad
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        # ===== ANÁLISIS MULTI-CHUNK (TOP 5) =====
        TOP_CHUNKS = min(5, len(similarities))
        top_chunks = similarities[:TOP_CHUNKS]
        
        print(f"\n� TOP {TOP_CHUNKS} CHUNKS MÁS RELEVANTES:")
        for i, chunk in enumerate(top_chunks, 1):
            print(f"   {i}. Chunk {chunk['chunk_id']}: {chunk['similarity']:.4f} ({int(chunk['similarity']*100)}%)")
        
        best_match = similarities[0]
        base_similarity = best_match["similarity"]
        
        # ===== SCORING INTELIGENTE =====
        import re
        
        # FACTOR 1: Similitud base
        similarity_score = base_similarity * 100
        
        # FACTOR 2: Contexto amplio (múltiples chunks relevantes)
        context_bonus = 0
        high_sim_chunks = [c for c in top_chunks if c['similarity'] > 0.5]
        if len(high_sim_chunks) >= 3:
            context_bonus = 10
            print(f"   ✅ Bonus contexto: +{context_bonus}% ({len(high_sim_chunks)} chunks)")
        elif len(high_sim_chunks) >= 2:
            context_bonus = 5
            print(f"   ✅ Bonus contexto: +{context_bonus}% ({len(high_sim_chunks)} chunks)")
        
        # FACTOR 3: Palabras clave compartidas
        answer_keywords = set(re.findall(r'\b\w{4,}\b', answer.user_answer.lower()))
        chunk_keywords = set(re.findall(r'\b\w{4,}\b', best_match["text"].lower()))
        shared_keywords = answer_keywords.intersection(chunk_keywords)
        
        keyword_bonus = 0
        if len(shared_keywords) >= 5:
            keyword_bonus = 8
            print(f"   ✅ Bonus keywords: +{keyword_bonus}% ({len(shared_keywords)} términos)")
        elif len(shared_keywords) >= 3:
            keyword_bonus = 5
            print(f"   ✅ Bonus keywords: +{keyword_bonus}% ({len(shared_keywords)} términos)")
        
        # FACTOR 4: Elaboración de respuesta
        length_bonus = 0
        if len(answer.user_answer) > 200:
            length_bonus = 5
            print(f"   ✅ Bonus elaboración: +{length_bonus}% ({len(answer.user_answer)} chars)")
        elif len(answer.user_answer) > 100:
            length_bonus = 3
            print(f"   ✅ Bonus elaboración: +{length_bonus}% ({len(answer.user_answer)} chars)")
        
        # FACTOR 5: Boost de inteligencia (concepto correcto, formulación diferente)
        intelligence_boost = 0
        if 0.50 <= base_similarity < 0.70:
            if context_bonus > 0 or keyword_bonus >= 5:
                intelligence_boost = 15
                print(f"   🧠 BOOST INTELIGENCIA: +{intelligence_boost}% (concepto OK, forma diferente)")
        elif 0.35 <= base_similarity < 0.50:
            if context_bonus >= 5 and keyword_bonus >= 5:
                intelligence_boost = 20
                print(f"   🧠 BOOST INTELIGENCIA: +{intelligence_boost}% (contexto+keywords buenos)")
        
        # SCORE FINAL
        raw_score = similarity_score + context_bonus + keyword_bonus + length_bonus + intelligence_boost
        score_percentage = min(int(raw_score), 100)
        
        print(f"\n📊 DESGLOSE DEL SCORE:")
        print(f"   Base (similitud):     {int(similarity_score)}%")
        print(f"   + Contexto amplio:    {context_bonus}%")
        print(f"   + Palabras clave:     {keyword_bonus}%")
        print(f"   + Elaboración:        {length_bonus}%")
        print(f"   + Boost inteligencia: {intelligence_boost}%")
        print(f"   {'─'*40}")
        print(f"   SCORE FINAL:          {score_percentage}%")
        
        # ===== GENERAR FEEDBACK =====
        is_correct = score_percentage >= 55
        
        if score_percentage >= 85:
            feedback = f"""🎉 ¡EXCELENTE! Tu respuesta demuestra comprensión profunda del concepto.

📊 Score de comprensión: {score_percentage}%

✅ Tu explicación coincide muy bien con el material. El sistema identificó {len(high_sim_chunks)} fragmentos relacionados en el libro.

💡 Captaste correctamente la esencia del concepto. ¡Sigue así con Active Recall!"""

        elif score_percentage >= 70:
            feedback = f"""✅ ¡MUY BIEN! Tu respuesta muestra buen entendimiento del tema.

📊 Score de comprensión: {score_percentage}%

👍 Has captado los conceptos principales. Tu formulación puede ser diferente al libro, pero el contenido es correcto.

💭 Sugerencia: Podrías profundizar un poco más, pero vas por buen camino."""

        elif score_percentage >= 55:
            feedback = f"""⚠️ RESPUESTA PARCIAL. Tienes la idea general, pero falta desarrollo.

📊 Score de comprensión: {score_percentage}%

🔍 Tu respuesta toca algunos puntos correctos, pero necesita más detalle o precisión.

📖 Revisa el material y explica el concepto con más profundidad. Recuerda: Active Recall = ENTENDER, no memorizar."""

        else:
            feedback = f"""❌ NECESITA MEJORAR. La respuesta no refleja bien el contenido del material.

📊 Score de comprensión: {score_percentage}%

🔄 Intenta de nuevo:
1. Relee el fragmento relevante
2. Cierra el libro y explica CON TUS PROPIAS PALABRAS
3. Enfócate en ENTENDER el concepto

💡 Tip: Imagina que se lo explicas a un amigo."""
        
        print(f"\n✅ Validación completada: {score_percentage}% {'✓' if is_correct else '✗'}")
        print(f"{'='*70}\n")
        
        # Calcular la posición del chunk en el material (estimada)
        total_chunks = len(similarities)
        best_chunk_position = best_match["chunk_id"]
        estimated_page = (best_chunk_position * 500) // 2500  # Estimar página basada en caracteres
        
        # Resultado con información COMPLETA del chunk
        result = ValidationResult(
            score=score_percentage,
            is_correct=is_correct,
            similarity=float(base_similarity),
            feedback=feedback,
            relevant_chunks=[
                {
                    "text": chunk["text_short"],
                    "text_full": chunk["text"],
                    "similarity": chunk["similarity"],
                    "position": chunk["chunk_id"],
                    "total_chunks": total_chunks
                }
                for chunk in top_chunks[:3]
            ],
            best_match_chunk={
                "text": best_match["text"],
                "text_short": best_match["text_short"],
                "similarity": best_match["similarity"],
                "chunk_id": best_chunk_position,
                "total_chunks": total_chunks,
                "estimated_page": estimated_page
            }
        )
        
        print(f"📍 Chunk más relevante: {best_chunk_position + 1}/{total_chunks} (página ~{estimated_page})")
        
        return result
        
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
    """Obtiene la lista de todos los materiales subidos"""
    return {
        "success": True,
        "total": len(materials_db),
        "materials": materials_db
    }

@app.get("/api/materials/{material_id}")
async def get_material(material_id: int):
    """Obtiene los detalles de un material específico"""
    material = next((m for m in materials_db if m["id"] == material_id), None)
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    return {
        "success": True,
        "material": material
    }

@app.delete("/api/materials/{material_id}")
async def delete_material(material_id: int):
    """
    Elimina un material y todos sus archivos asociados
    - Elimina embeddings del material
    - Elimina archivos PDF originales
    - Elimina entrada de la base de datos
    """
    global materials_db
    
    # Verificar que el material existe
    material = next((m for m in materials_db if m["id"] == material_id), None)
    if not material:
        raise HTTPException(status_code=404, detail=f"Material con ID {material_id} no encontrado")
    
    deleted_files = []
    errors = []
    
    try:
        # 1. Eliminar archivos de embeddings
        embeddings_files = list(EMBEDDINGS_DIR.glob(f"material_{material_id}_*.json"))
        for emb_file in embeddings_files:
            try:
                emb_file.unlink()
                deleted_files.append(str(emb_file.name))
                print(f"🗑️ Embedding eliminado: {emb_file.name}")
            except Exception as e:
                errors.append(f"Error eliminando {emb_file.name}: {str(e)}")
        
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

# ==================== MAIN ====================

if __name__ == "__main__":
    # Parsear argumentos de línea de comando
    parser = argparse.ArgumentParser(description="Recuiva Backend API")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8000")),
                      help="Puerto para ejecutar el servidor")
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "0.0.0.0"),
                      help="Host para ejecutar el servidor")
    parser.add_argument("--debug", type=bool, default=os.getenv("DEBUG", "True").lower() == "true",
                      help="Modo debug")
    
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