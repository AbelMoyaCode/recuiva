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

# Importar módulos locales
try:
    from embeddings_module import generate_embeddings, calculate_similarity, load_model
    from chunking import chunk_text, extract_text_from_pdf, get_text_stats
except ImportError:
    print("⚠️ Módulos locales no encontrados. Asegúrate de tener embeddings_module.py y chunking.py")

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

# Configurar CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
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
    question_id: int
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
    best_match_chunk: Optional[str] = None

class MaterialResponse(BaseModel):
    id: int
    filename: str
    title: str
    uploaded_at: str
    total_chunks: int
    total_characters: int
    estimated_pages: int

# ==================== CONFIGURACIÓN ====================

# Rutas del sistema de archivos
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
MATERIALS_DIR = DATA_DIR / "materials"

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
    
    # Precargar modelo de embeddings
    try:
        load_model()
        print("✅ Modelo de embeddings cargado exitosamente")
    except Exception as e:
        print(f"⚠️ Error cargando modelo: {e}")
    
    # Cargar materiales existentes
    load_existing_materials()
    print(f"📚 Materiales cargados: {len(materials_db)}")

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
        if file.filename.endswith('.pdf'):
            print("📄 Extrayendo texto de PDF...")
            text = extract_text_from_pdf(content)
        else:
            text = content.decode('utf-8')
        
        # Obtener estadísticas del texto
        stats = get_text_stats(text)
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
        material_id = len(materials_db) + 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        material_data = {
            "id": material_id,
            "filename": file.filename,
            "title": file.filename.replace('.pdf', '').replace('.txt', '').replace('_', ' ').title(),
            "uploaded_at": timestamp,
            "total_chunks": len(chunks),
            "total_characters": len(text),
            "estimated_pages": stats["estimated_pages"]
        }
        
        materials_db.append(material_data)
        
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
    Valida semánticamente la respuesta del usuario
    Compara con los embeddings del material usando similaridad coseno
    
    Args:
        answer: Respuesta del usuario con ID de pregunta
        
    Returns:
        ValidationResult: Resultado de la validación con score y feedback
    """
    try:
        print(f"🔍 Validando respuesta para pregunta {answer.question_id}")
        
        # Buscar la pregunta
        question = next((q for q in questions_db if q["id"] == answer.question_id), None)
        if not question:
            raise HTTPException(status_code=404, detail="Pregunta no encontrada")
        
        # Cargar embeddings del material relacionado
        material_id = question.get("material_id", 1)  # Por defecto usar el primer material
        
        # Buscar archivo de embeddings
        embeddings_files = list(EMBEDDINGS_DIR.glob(f"material_{material_id}_*.json"))
        
        if not embeddings_files:
            # Si no hay material específico, usar el primero disponible
            embeddings_files = list(EMBEDDINGS_DIR.glob("material_*.json"))
            if not embeddings_files:
                raise HTTPException(
                    status_code=404, 
                    detail="No hay materiales procesados. Sube un material primero."
                )
        
        # Cargar embeddings
        print(f"📂 Cargando embeddings de: {embeddings_files[0]}")
        with open(embeddings_files[0], 'r', encoding='utf-8') as f:
            material_embeddings = json.load(f)
        
        # Generar embedding de la respuesta del usuario
        print("🧠 Generando embedding de la respuesta...")
        user_embedding = generate_embeddings(answer.user_answer)
        
        # Calcular similaridad con cada chunk y obtener el máximo
        max_similarity = 0
        best_chunk = None
        
        print(f"🔬 Calculando similaridad con {len(material_embeddings)} chunks...")
        for chunk_data in material_embeddings:
            chunk_embedding = chunk_data["embedding"]
            similarity = calculate_similarity(user_embedding, chunk_embedding)
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_chunk = chunk_data.get("text_full", chunk_data["text"])
        
        print(f"✅ Similaridad máxima: {max_similarity:.4f}")
        
        # Determinar si es correcto
        is_correct = max_similarity >= THRESHOLD_GOOD
        
        # Generar feedback basado en thresholds
        if max_similarity >= THRESHOLD_EXCELLENT:
            feedback = "¡Excelente! Tu respuesta demuestra una comprensión profunda del tema. 🌟"
        elif max_similarity >= THRESHOLD_GOOD:
            feedback = "Bien, tu respuesta es correcta pero podrías profundizar más en algunos aspectos. 👍"
        elif max_similarity >= THRESHOLD_ACCEPTABLE:
            feedback = "Tu respuesta tiene algunos conceptos correctos, pero necesitas revisar el material. 📚"
        else:
            feedback = "Tu respuesta no refleja el contenido del material. Te recomendamos repasarlo con atención. 🔄"
        
        result = ValidationResult(
            score=round(max_similarity * 100, 2),
            is_correct=is_correct,
            feedback=feedback,
            similarity=round(max_similarity, 4),
            best_match_chunk=best_chunk[:300] + "..." if best_chunk and len(best_chunk) > 300 else best_chunk
        )
        
        print(f"📊 Resultado: {result.score}% - {'✅ Correcto' if is_correct else '❌ Incorrecto'}")
        
        return result
    
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
                with open(file, 'r') as f:
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
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    print("\n" + "="*50)
    print("🚀 Iniciando Recuiva Backend API")
    print("="*50)
    print(f"📍 Host: {HOST}")
    print(f"🔌 Port: {PORT}")
    print(f"🐛 Debug: {DEBUG}")
    print(f"📚 Documentación: http://{HOST}:{PORT}/docs")
    print("="*50 + "\n")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
