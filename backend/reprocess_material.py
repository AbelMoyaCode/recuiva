"""
SCRIPT DE RE-PROCESAMIENTO DE MATERIALES
=========================================

Re-procesa materiales existentes con CHUNKING SEMANTICO mejorado.

USO:
    python reprocess_material.py --material-id <UUID>

PROCESO:
1. Descarga PDF desde Supabase
2. Extrae texto
3. Aplica chunking semantico (150-400 palabras + context anchors)
4. Genera embeddings
5. Actualiza Supabase con nuevos chunks

Autor: Abel Jesus Moya Acosta
Fecha: 17 de noviembre de 2025
"""

import sys
import os
import argparse
from pathlib import Path

# Agregar backend al path
BACKEND_DIR = Path(__file__).parent
sys.path.insert(0, str(BACKEND_DIR))

from chunking import chunk_text_semantic, extract_text_from_pdf
from embeddings_module import load_model, generate_embeddings
from supabase_client import get_supabase_client
import numpy as np


def reprocess_material(material_id: str, use_semantic_chunking: bool = True):
    """Re-procesa un material con chunking semantico"""
    print("="*80)
    print("RE-PROCESAMIENTO DE MATERIAL CON CHUNKING SEMANTICO")
    print("="*80)
    
    try:
        supabase = get_supabase_client()
        print("Conectado a Supabase")
        
        # Obtener material
        material_info = supabase.table('materials').select('*').eq('id', material_id).single().execute()
        
        if not material_info.data:
            print(f"Material {material_id} no encontrado")
            return False
        
        material = material_info.data
        print(f"Material: {material['title']}")
        print(f"Chunks actuales: {material.get('total_chunks', 0)}")
        
        # Descargar PDF
        pdf_path = material.get('pdf_path')
        if not pdf_path:
            print("No se encontro ruta del PDF")
            return False
        
        pdf_response = supabase.storage.from_('materials').download(pdf_path)
        if not pdf_response:
            print("Error descargando PDF")
            return False
        
        # Extraer texto
        text, total_pages = extract_text_from_pdf(pdf_response)
        print(f"Texto extraido: {len(text)} caracteres, {total_pages} paginas")
        
        # Chunking
        if use_semantic_chunking:
            chunks = chunk_text_semantic(text, min_chunk_size=150, max_chunk_size=400, overlap_words=15)
            print(f"Chunking semantico: {len(chunks)} chunks")
        else:
            from chunking import chunk_text
            chunks = chunk_text(text, chunk_size=1000, overlap=200)
        
        # Generar embeddings
        model = load_model()
        embeddings_data = []
        
        for i, chunk_text in enumerate(chunks):
            if (i + 1) % 10 == 0:
                print(f"Procesando chunk {i+1}/{len(chunks)}...")
            
            embedding = generate_embeddings(chunk_text)
            estimated_page = int((i / len(chunks)) * total_pages) + 1
            
            embeddings_data.append({
                'material_id': material_id,
                'chunk_index': i,
                'chunk_text': chunk_text,
                'embedding': embedding.tolist(),
                'page_number': estimated_page
            })
        
        print(f"{len(embeddings_data)} embeddings generados")
        
        # Eliminar chunks antiguos
        supabase.table('material_embeddings').delete().eq('material_id', material_id).execute()
        
        # Insertar nuevos
        batch_size = 50
        for i in range(0, len(embeddings_data), batch_size):
            batch = embeddings_data[i:i+batch_size]
            supabase.table('material_embeddings').insert(batch).execute()
            print(f"Guardado lote {i//batch_size + 1}")
        
        # Actualizar metadata
        supabase.table('materials').update({
            'total_chunks': len(chunks),
            'estimated_pages': total_pages,
            'chunking_method': 'semantic' if use_semantic_chunking else 'legacy'
        }).eq('id', material_id).execute()
        
        print("="*80)
        print("RE-PROCESAMIENTO COMPLETADO")
        print(f"Chunks antiguos: {material.get('total_chunks', 0)}")
        print(f"Chunks nuevos: {len(chunks)}")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(description='Re-procesa material con chunking semantico')
    parser.add_argument('--material-id', type=str, required=True, help='UUID del material')
    parser.add_argument('--legacy', action='store_true', help='Usar chunking legacy')
    
    args = parser.parse_args()
    
    success = reprocess_material(material_id=args.material_id, use_semantic_chunking=not args.legacy)
    
    if success:
        print("Re-procesamiento exitoso")
        sys.exit(0)
    else:
        print("Re-procesamiento fallo")
        sys.exit(1)


if __name__ == "__main__":
    main()
