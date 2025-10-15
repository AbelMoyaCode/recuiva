#!/usr/bin/env python3
"""
Backend simplificado solo para validación semántica
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import numpy as np
from sentence_transformers import SentenceTransformer
import json
from pathlib import Path

# Crear aplicación FastAPI
app = FastAPI(title="Recuiva Validation API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo globalmente
print("🤖 Cargando modelo Sentence Transformers...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Modelo cargado exitosamente")

# Datos de muestra para validación
SAMPLE_CHUNKS = [
    "Active Recall es una técnica de estudio que consiste en intentar recordar información sin mirar el material. Es más efectivo que la relectura pasiva porque fuerza al cerebro a recuperar activamente la información.",
    "La validación semántica utiliza modelos de lenguaje como Sentence Transformers para comparar significados. Sentence Transformers convierte texto en vectores que representan el significado semántico.",
    "Los embeddings son representaciones vectoriales de texto que capturan el significado semántico. La similitud coseno entre embeddings indica qué tan similar es el significado de dos textos.",
    "El aprendizaje efectivo requiere práctica activa y recuperación de información. Las técnicas pasivas como releer son menos efectivas que las técnicas activas como hacerse preguntas.",
    "La comprensión profunda se logra cuando el estudiante puede explicar conceptos con sus propias palabras y aplicarlos en nuevos contextos."
]

# Generar embeddings para los chunks de muestra
print("📚 Generando embeddings para material de muestra...")
sample_embeddings = model.encode(SAMPLE_CHUNKS)
print(f"✅ {len(SAMPLE_CHUNKS)} embeddings generados")

class ValidationRequest(BaseModel):
    carpeta_id: str
    pregunta: str
    respuesta_usuario: str

class ValidationResult(BaseModel):
    score: float
    feedback: str
    relevant_chunks: List[dict] = []
    best_match_chunk: Optional[dict] = None

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
        "chunks_available": len(SAMPLE_CHUNKS)
    }

@app.post("/api/validate-semantic", response_model=ValidationResult)
async def validate_semantic(request: ValidationRequest):
    """
    Validación semántica simplificada
    """
    try:
        print(f"🔍 Validando respuesta: {request.respuesta_usuario[:100]}...")
        
        # Generar embedding para la respuesta del usuario
        user_embedding = model.encode([request.respuesta_usuario])
        
        # Calcular similaridades
        similarities = []
        for i, chunk in enumerate(SAMPLE_CHUNKS):
            chunk_embedding = sample_embeddings[i:i+1]
            
            # Calcular similitud coseno
            cosine_sim = np.dot(user_embedding[0], chunk_embedding[0]) / (
                np.linalg.norm(user_embedding[0]) * np.linalg.norm(chunk_embedding[0])
            )
            
            similarities.append({
                "chunk_id": i,
                "text": chunk,
                "similarity": float(cosine_sim)
            })
        
        # Encontrar la mejor coincidencia
        best_match = max(similarities, key=lambda x: x["similarity"])
        score_percentage = int(best_match["similarity"] * 100)
        
        # Generar feedback
        if score_percentage >= 80:
            feedback = f"¡Excelente! Tu respuesta demuestra comprensión profunda. Score: {score_percentage}%"
        elif score_percentage >= 60:
            feedback = f"Bien. Tu respuesta está correcta pero podrías profundizar más. Score: {score_percentage}%"
        elif score_percentage >= 40:
            feedback = f"Regular. Tu respuesta tiene relación pero necesita más precisión. Score: {score_percentage}%"
        else:
            feedback = f"Necesita mejorar. Revisa el material y vuelve a intentar. Score: {score_percentage}%"
        
        # Top 3 chunks más relevantes
        relevant_chunks = sorted(similarities, key=lambda x: x["similarity"], reverse=True)[:3]
        
        result = ValidationResult(
            score=score_percentage,
            feedback=feedback,
            relevant_chunks=relevant_chunks,
            best_match_chunk=best_match
        )
        
        print(f"✅ Validación completada - Score: {score_percentage}%")
        return result
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando servidor de validación...")
    uvicorn.run(app, host="127.0.0.1", port=8002)