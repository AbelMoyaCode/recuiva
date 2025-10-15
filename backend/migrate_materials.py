#!/usr/bin/env python3
"""
Script para migrar materiales existentes al nuevo sistema de índice
"""
import json
from pathlib import Path
from datetime import datetime

# Rutas
BACKEND_DIR = Path(__file__).parent
BASE_DIR = BACKEND_DIR.parent
DATA_DIR = BASE_DIR / "data"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"
MATERIALS_DIR = DATA_DIR / "materials"
MATERIALS_INDEX_FILE = DATA_DIR / "materials_index.json"

def migrate_materials():
    """Migra materiales existentes desde embeddings al índice"""
    materials_db = []
    
    print("🔄 Migrando materiales existentes al índice...")
    print(f"📁 Buscando en: {EMBEDDINGS_DIR}")
    
    for file in sorted(EMBEDDINGS_DIR.glob("material_*.json")):
        try:
            # Extraer información del nombre del archivo
            # Formato: material_{id}_{timestamp}.json
            parts = file.stem.split('_')
            if len(parts) >= 3:
                material_id = int(parts[1])
                timestamp = parts[2]
                
                # Cargar datos del embedding
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Verificar si ya existe en el índice
                if any(m["id"] == material_id for m in materials_db):
                    print(f"  ⏭️  Material {material_id} ya existe, saltando...")
                    continue
                
                # Buscar archivo PDF original
                pdf_patterns = [
                    f"*_{material_id}_*.pdf",
                    f"*_{material_id}_*.txt"
                ]
                
                saved_filename = None
                file_path = None
                file_exists = False
                original_filename = f"material_{material_id}"
                
                for pattern in pdf_patterns:
                    pdf_files = list(MATERIALS_DIR.glob(pattern))
                    if pdf_files:
                        saved_filename = pdf_files[0].name
                        file_path = str(pdf_files[0])
                        file_exists = True
                        # Intentar extraer nombre original del archivo
                        original_filename = saved_filename.split(f"_{material_id}_")[0] + pdf_files[0].suffix
                        break
                
                # Crear entrada en el índice
                material_data = {
                    "id": material_id,
                    "filename": original_filename,
                    "saved_filename": saved_filename,
                    "file_path": file_path,
                    "file_exists": file_exists,
                    "title": original_filename.replace('.pdf', '').replace('.txt', '').replace('_', ' ').title(),
                    "uploaded_at": timestamp,
                    "total_chunks": len(data),
                    "total_characters": sum(len(chunk.get("text_full", "")) for chunk in data),
                    "estimated_pages": len(data) // 3  # Estimación aproximada
                }
                
                materials_db.append(material_data)
                print(f"  ✅ Material {material_id}: {original_filename} ({len(data)} chunks)")
                
        except Exception as e:
            print(f"  ❌ Error procesando {file.name}: {e}")
    
    # Guardar índice
    if materials_db:
        with open(MATERIALS_INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(materials_db, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Migración completada: {len(materials_db)} materiales guardados en índice")
        print(f"📝 Índice guardado en: {MATERIALS_INDEX_FILE}")
    else:
        print("\n⚠️  No se encontraron materiales para migrar")
    
    return materials_db

if __name__ == "__main__":
    print("="*60)
    print("🔄 MIGRACIÓN DE MATERIALES AL SISTEMA DE ÍNDICE")
    print("="*60 + "\n")
    
    materials = migrate_materials()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DE MATERIALES MIGRADOS:")
    print("="*60)
    for m in materials:
        print(f"\nID: {m['id']}")
        print(f"  📄 Archivo: {m['filename']}")
        print(f"  📦 Chunks: {m['total_chunks']}")
        print(f"  📁 Guardado como: {m.get('saved_filename', 'N/A')}")
        print(f"  ✓ Archivo existe: {'Sí' if m['file_exists'] else 'No'}")
    print("\n" + "="*60)
