#!/usr/bin/env python3
"""
Recuiva - Embeddings Locales (Evidencia Técnica)
Sprint 1 - HU-010: Generación de embeddings desde texto/PDF

Autor: Abel Moya
Fecha: 30/09/2025
Propósito: Demostrar capacidad técnica de procesamiento de embeddings
para validación semántica en Active Recall
"""

import json
import numpy as np
from datetime import datetime
import os
import sys

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️  sentence-transformers no instalado. Generando embeddings mock...")

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  PyPDF2 no instalado. Usando texto de muestra...")

def leer_pdf(pdf_path):
    """Leer contenido de un archivo PDF"""
    if not PDF_AVAILABLE:
        print("⚠️  PyPDF2 no disponible, usando texto de muestra...")
        return crear_texto_muestra()
    
    if not os.path.exists(pdf_path):
        print(f"⚠️  PDF no encontrado: {pdf_path}")
        print("📝 Usando texto de muestra...")
        return crear_texto_muestra()
    
    try:
        print(f"📖 Leyendo PDF: {pdf_path}")
        texto_completo = ""
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_paginas = len(pdf_reader.pages)
            print(f"📄 Total de páginas: {total_paginas}")
            
            for i, page in enumerate(pdf_reader.pages[:5]):  # Máximo 5 páginas
                print(f"   → Procesando página {i+1}/{min(5, total_paginas)}")
                texto_pagina = page.extract_text()
                if texto_pagina.strip():
                    texto_completo += f"\n\n--- PÁGINA {i+1} ---\n"
                    texto_completo += texto_pagina
        
        if not texto_completo.strip():
            print("⚠️  No se pudo extraer texto del PDF")
            return crear_texto_muestra()
        
        print(f"✅ PDF procesado: {len(texto_completo)} caracteres extraídos")
        return texto_completo
        
    except Exception as e:
        print(f"❌ Error leyendo PDF: {str(e)}")
        print("📝 Usando texto de muestra...")
        return crear_texto_muestra()

def crear_texto_muestra():
    """Texto de muestra sobre Active Recall para procesar"""
    return """
    Active Recall es una técnica de estudio que consiste en recuperar información 
    de la memoria activamente, en lugar de simplemente releer material de estudio.
    
    Esta técnica mejora la retención a largo plazo porque fortalece las conexiones
    neuronales y hace que el cerebro trabaje más para recordar la información.
    
    Recuiva implementa Active Recall a través de sesiones de práctica espaciadas
    donde el usuario debe recordar conceptos sin mirar las respuestas primero.
    
    La validación semántica permite comparar respuestas del estudiante con el
    material original usando embeddings, sin requerir coincidencia exacta de palabras.
    
    Los intervalos de repetición se ajustan automáticamente según el rendimiento
    del estudiante en cada sesión de práctica, optimizando la retención.
    """

def dividir_en_chunks(texto, max_chars=400):
    """
    Divide el texto en chunks manejables para embeddings
    """
    # Limpiar y dividir por párrafos
    parrafos = [p.strip() for p in texto.split('\n') if p.strip()]
    
    chunks = []
    chunk_id = 1
    
    for parrafo in parrafos:
        if len(parrafo) <= max_chars:
            chunks.append({
                'id': f'chunk_{chunk_id:03d}',
                'content': parrafo,
                'length': len(parrafo),
                'type': 'paragraph'
            })
            chunk_id += 1
        else:
            # Dividir párrafos largos por oraciones
            oraciones = parrafo.split('.')
            chunk_actual = ""
            
            for oracion in oraciones:
                if len(chunk_actual + oracion) <= max_chars:
                    chunk_actual += oracion + "."
                else:
                    if chunk_actual:
                        chunks.append({
                            'id': f'chunk_{chunk_id:03d}',
                            'content': chunk_actual.strip(),
                            'length': len(chunk_actual),
                            'type': 'split_paragraph'
                        })
                        chunk_id += 1
                    chunk_actual = oracion + "."
            
            # Agregar último chunk
            if chunk_actual:
                chunks.append({
                    'id': f'chunk_{chunk_id:03d}',
                    'content': chunk_actual.strip(),
                    'length': len(chunk_actual),
                    'type': 'split_paragraph'
                })
                chunk_id += 1
    
    return chunks

def generar_embeddings_reales(chunks):
    """Generar embeddings reales usando sentence-transformers"""
    print("🤖 Cargando modelo sentence-transformers (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Extraer textos para procesar
    textos = [chunk['content'] for chunk in chunks]
    
    print(f"🧠 Generando embeddings para {len(textos)} chunks...")
    embeddings = model.encode(textos, show_progress_bar=True)
    
    # Combinar chunks con sus embeddings
    resultados = []
    for i, chunk in enumerate(chunks):
        embedding = embeddings[i]
        resultados.append({
            'id': chunk['id'],
            'content': chunk['content'],
            'length': chunk['length'],
            'type': chunk['type'],
            'embedding': {
                'vector': embedding.tolist(),
                'dimension': len(embedding),
                'norm': float(np.linalg.norm(embedding))
            }
        })
    
    return resultados

def generar_embeddings_mock(chunks):
    """Generar embeddings mock (para cuando no está sentence-transformers)"""
    print("🎭 Generando embeddings mock (384 dimensiones)...")
    
    resultados = []
    np.random.seed(42)  # Para reproducibilidad
    
    for chunk in chunks:
        # Vector aleatorio normalizado de 384 dimensiones
        vector = np.random.randn(384)
        vector = vector / np.linalg.norm(vector)  # Normalizar
        
        resultados.append({
            'id': chunk['id'],
            'content': chunk['content'],
            'length': chunk['length'],
            'type': chunk['type'],
            'embedding': {
                'vector': vector.tolist(),
                'dimension': 384,
                'norm': float(np.linalg.norm(vector))
            }
        })
    
    return resultados

def calcular_similaridades(embeddings_data):
    """Calcular similaridades coseno entre todos los pares"""
    print("📊 Calculando similaridades coseno...")
    
    vectores = np.array([item['embedding']['vector'] for item in embeddings_data])
    
    # Matriz de similaridades
    similaridades = np.dot(vectores, vectores.T)
    
    # Encontrar top-3 pares más similares (excluyendo diagonal)
    pares_similares = []
    for i in range(len(embeddings_data)):
        for j in range(i+1, len(embeddings_data)):
            similaridad = similaridades[i][j]
            pares_similares.append({
                'chunk_1': embeddings_data[i]['id'],
                'chunk_2': embeddings_data[j]['id'],
                'similaridad': float(similaridad),
                'content_1': embeddings_data[i]['content'][:80] + "...",
                'content_2': embeddings_data[j]['content'][:80] + "..."
            })
    
    # Ordenar por similaridad descendente
    pares_similares.sort(key=lambda x: x['similaridad'], reverse=True)
    
    return pares_similares[:3]  # Top-3

def guardar_resultados(embeddings_data, similaridades, output_file='embeddings_output.json'):
    """Guardar todos los resultados en JSON"""
    resultado_final = {
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'model': 'all-MiniLM-L6-v2' if TRANSFORMERS_AVAILABLE else 'mock',
            'total_chunks': len(embeddings_data),
            'dimension': embeddings_data[0]['embedding']['dimension'] if embeddings_data else 0,
            'script_version': '1.0',
            'purpose': 'Recuiva Active Recall - Evidencia técnica embeddings'
        },
        'chunks': embeddings_data,
        'top_similaridades': similaridades,
        'resumen': {
            'chunks_procesados': len(embeddings_data),
            'promedio_longitud': np.mean([item['length'] for item in embeddings_data]),
            'tipos_chunk': list(set([item['type'] for item in embeddings_data])),
            'similaridad_maxima': similaridades[0]['similaridad'] if similaridades else 0
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado_final, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultados guardados en: {output_file}")
    return resultado_final

def mostrar_resumen(resultado):
    """Mostrar resumen en consola"""
    print("\n" + "="*60)
    print("📋 RESUMEN DE PROCESAMIENTO - RECUIVA EMBEDDINGS")
    print("="*60)
    
    metadata = resultado['metadata']
    resumen = resultado['resumen']
    
    print(f"🕐 Timestamp: {metadata['timestamp']}")
    print(f"🤖 Modelo: {metadata['model']}")
    print(f"📊 Chunks procesados: {resumen['chunks_procesados']}")
    print(f"📐 Dimensión embeddings: {metadata['dimension']}")
    print(f"📏 Longitud promedio: {resumen['promedio_longitud']:.1f} caracteres")
    print(f"🎯 Similaridad máxima: {resumen['similaridad_maxima']:.4f}")
    
    print(f"\n📑 Tipos de chunk: {', '.join(resumen['tipos_chunk'])}")
    
    print(f"\n🔝 TOP-3 CHUNKS MÁS SIMILARES:")
    for i, sim in enumerate(resultado['top_similaridades'], 1):
        print(f"{i}. {sim['chunk_1']} ↔ {sim['chunk_2']} (similaridad: {sim['similaridad']:.4f})")
        print(f"   • {sim['content_1']}")
        print(f"   • {sim['content_2']}")
        print()

def main():
    """Función principal"""
    print("🚀 RECUIVA - GENERADOR DE EMBEDDINGS LOCALES")
    print("="*50)
    
    # Crear directorio de salida si no existe
    os.makedirs('output', exist_ok=True)
    
    try:
        # 1. Buscar archivos de texto o PDF
        pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt') and f.startswith('sample_')]
        
        if txt_files:
            txt_path = txt_files[0]
            print(f"📁 Archivo TXT encontrado: {txt_path}")
            with open(txt_path, 'r', encoding='utf-8') as f:
                texto = f.read()
            print(f"✅ Texto cargado: {len(texto)} caracteres")
        elif pdf_files:
            pdf_path = pdf_files[0]  # Tomar el primer PDF encontrado
            print(f"📁 PDF encontrado: {pdf_path}")
            texto = leer_pdf(pdf_path)
        else:
            print("📝 No se encontró archivo, creando texto de muestra...")
            texto = crear_texto_muestra()
        
        # 2. Dividir en chunks
        print("✂️  Dividiendo texto en chunks...")
        chunks = dividir_en_chunks(texto)
        print(f"   → {len(chunks)} chunks generados")
        
        # Mostrar preview de chunks
        print(f"\n📋 PREVIEW DE CHUNKS:")
        for i, chunk in enumerate(chunks[:3], 1):
            preview = chunk['content'][:80] + "..." if len(chunk['content']) > 80 else chunk['content']
            print(f"   {i}. {chunk['id']}: {preview}")
        if len(chunks) > 3:
            print(f"   ... y {len(chunks) - 3} chunks más")
        
        # 3. Generar embeddings
        if TRANSFORMERS_AVAILABLE:
            embeddings_data = generar_embeddings_reales(chunks)
        else:
            embeddings_data = generar_embeddings_mock(chunks)
        
        # 4. Calcular similaridades
        similaridades = calcular_similaridades(embeddings_data)
        
        # 5. Guardar resultados
        output_file = f"output/embeddings_recuiva_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        resultado = guardar_resultados(embeddings_data, similaridades, output_file)
        
        # 6. Mostrar resumen
        mostrar_resumen(resultado)
        
        print("\n✅ Procesamiento completado exitosamente!")
        print(f"📁 Archivo generado: {output_file}")
        
        return output_file
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {str(e)}")
        return None

if __name__ == "__main__":
    # Verificar si sentence-transformers está disponible
    if not TRANSFORMERS_AVAILABLE:
        print("📦 Para embeddings reales, instala: pip install sentence-transformers")
        print("🎭 Continuando con embeddings mock para demostración...\n")
    
    output_file = main()
    
    if output_file:
        print(f"\n🎯 PARA MOSTRAR AL PROFESOR:")
        print(f"1. Ejecutar: python {__file__}")
        print(f"2. Mostrar archivo: {output_file}")
        print(f"3. HU-010 (embeddings) → Parcial ✅")