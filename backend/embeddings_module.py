"""
Módulo para generación y manejo de embeddings
Usa Sentence Transformers para crear representaciones vectoriales semánticas

Autor: Abel Jesús Moya Acosta
Fecha: 7 de octubre de 2025
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import json
from pathlib import Path
import os

# Cargar modelo globalmente para reutilizar
MODEL_NAME = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')
model = None

def load_model():
    """Carga el modelo de embeddings si no está cargado"""
    global model
    if model is None:
        print(f"🔄 Cargando modelo {MODEL_NAME}...")
        try:
            model = SentenceTransformer(MODEL_NAME)
            print(f"✅ Modelo {MODEL_NAME} cargado exitosamente")
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            raise
    return model

def generate_embeddings(text: Union[str, List[str]]) -> np.ndarray:
    """
    Genera embeddings para texto o lista de textos
    
    Args:
        text: Texto o lista de textos a vectorizar
        
    Returns:
        np.ndarray: Array de embeddings
    """
    model = load_model()
    
    if isinstance(text, str):
        return model.encode(text, convert_to_numpy=True)
    else:
        return model.encode(text, convert_to_numpy=True, show_progress_bar=True)

def calculate_similarity(embedding1: Union[np.ndarray, List], 
                        embedding2: Union[np.ndarray, List]) -> float:
    """
    Calcula la similaridad coseno entre dos embeddings
    
    Args:
        embedding1: Primer embedding
        embedding2: Segundo embedding
        
    Returns:
        float: Similaridad coseno (0 a 1)
    """
    # Convertir a numpy arrays si son listas
    if isinstance(embedding1, list):
        embedding1 = np.array(embedding1)
    if isinstance(embedding2, list):
        embedding2 = np.array(embedding2)
    
    # Calcular similaridad coseno
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    similarity = dot_product / (norm1 * norm2)
    
    # Asegurar que esté en rango [0, 1]
    # La similaridad coseno va de -1 a 1, normalizar a 0-1
    return float(max(0.0, min(1.0, (similarity + 1) / 2)))

def find_most_similar(query_embedding: np.ndarray, 
                     embeddings_list: List[dict], 
                     top_k: int = 5) -> List[dict]:
    """
    Encuentra los embeddings más similares a la consulta
    
    Args:
        query_embedding: Embedding de la consulta
        embeddings_list: Lista de diccionarios con embeddings
        top_k: Número de resultados a retornar
        
    Returns:
        List[dict]: Lista de los top_k resultados más similares
    """
    results = []
    
    for item in embeddings_list:
        similarity = calculate_similarity(query_embedding, item['embedding'])
        results.append({
            **item,
            'similarity': similarity
        })
    
    # Ordenar por similaridad descendente
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    return results[:top_k]

def save_embeddings(embeddings_data: List[dict], filepath: Path):
    """
    Guarda embeddings en archivo JSON
    
    Args:
        embeddings_data: Lista de diccionarios con embeddings
        filepath: Ruta donde guardar el archivo
    """
    # Convertir numpy arrays a listas para JSON
    for item in embeddings_data:
        if isinstance(item.get('embedding'), np.ndarray):
            item['embedding'] = item['embedding'].tolist()
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(embeddings_data, f, ensure_ascii=False, indent=2)

def load_embeddings(filepath: Path) -> List[dict]:
    """
    Carga embeddings desde archivo JSON
    
    Args:
        filepath: Ruta del archivo a cargar
        
    Returns:
        List[dict]: Lista de embeddings
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Precargar el modelo cuando se importa el módulo (opcional)
# load_model()
