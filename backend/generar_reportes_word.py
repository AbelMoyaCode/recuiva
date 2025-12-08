"""
═══════════════════════════════════════════════════════════════════════════════
GENERADOR DE REPORTES INDIVIDUALES PARA WORD
═══════════════════════════════════════════════════════════════════════════════
Genera reportes detallados de cada módulo de pruebas para incluir en Word
Autor: Abel Jesús Moya Acosta
Fecha: 5 de diciembre de 2025
═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import os
from datetime import datetime

def ejecutar_modulo(nombre_archivo, titulo, descripcion, total_tests):
    """Ejecuta un módulo de tests y captura la salida"""
    print("\n" + "═"*80)
    print(f"  {titulo}")
    print(f"  {descripcion}")
    print("═"*80)
    
    # Ejecutar pytest con salida detallada
    cmd = f"python -m pytest tests/{nombre_archivo} -v --tb=short --color=yes"
    
    print(f"\n▶ Ejecutando: {cmd}\n")
    
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='ignore'
    )
    
    # Mostrar salida
    print(result.stdout)
    if result.stderr:
        print("ERRORES:", result.stderr)
    
    # Guardar reporte en archivo
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_reporte = f"reporte_{nombre_archivo.replace('.py', '')}_{fecha}.txt"
    
    with open(nombre_reporte, 'w', encoding='utf-8') as f:
        f.write("═"*80 + "\n")
        f.write(f"{titulo}\n")
        f.write(f"{descripcion}\n")
        f.write(f"Fecha: {datetime.now().strftime('%d de %B de %Y - %H:%M:%S')}\n")
        f.write("═"*80 + "\n\n")
        f.write(result.stdout)
        f.write("\n\n" + "═"*80 + "\n")
        f.write(f"✅ TOTAL: {total_tests} pruebas documentadas\n")
        f.write("═"*80 + "\n")
    
    print(f"\n💾 Reporte guardado: {nombre_reporte}")
    
    input("\n⏸  Presiona ENTER para continuar al siguiente módulo...")
    
    return result.returncode == 0

def main():
    """Ejecuta todos los módulos y genera reportes"""
    
    print("\n" + "█"*80)
    print("  GENERADOR DE REPORTES INDIVIDUALES - PRUEBAS UNITARIAS RECUIVA")
    print("  Para documentación en Word con capturas de pantalla")
    print("█"*80)
    
    input("\n⏸  Presiona ENTER para comenzar...")
    
    modulos = [
        {
            'archivo': 'test_embeddings.py',
            'titulo': 'MÓDULO 1: EMBEDDINGS (Objetivo 1)',
            'descripcion': 'Generación de vectores semánticos con all-MiniLM-L6-v2 (384 dim)',
            'tests': 20
        },
        {
            'archivo': 'test_chunking.py',
            'titulo': 'MÓDULO 2: CHUNKING SEMÁNTICO (Objetivo 1)',
            'descripcion': 'Chunks de 80-100 palabras con overlap de 20 palabras',
            'tests': 20
        },
        {
            'archivo': 'test_hybrid_validator.py',
            'titulo': 'MÓDULO 3: VALIDADOR HÍBRIDO (Objetivo 2)',
            'descripcion': 'BM25 (5%) + Similitud Coseno (80%) + Cobertura (15%)',
            'tests': 23
        },
        {
            'archivo': 'test_groq_api.py',
            'titulo': 'MÓDULO 4: API GROQ (Objetivo 3)',
            'descripcion': 'Generación de preguntas con Llama 3.3 70B Versatile',
            'tests': 23
        },
        {
            'archivo': 'test_sm2_algorithm.py',
            'titulo': 'MÓDULO 5: ALGORITMO SM-2 (Objetivo 4)',
            'descripcion': 'Repetición espaciada con Easiness Factor y scheduling',
            'tests': 17
        },
        {
            'archivo': 'test_integration.py',
            'titulo': 'MÓDULO 6: INTEGRACIÓN Y PERFORMANCE',
            'descripcion': 'Pruebas end-to-end y métricas de rendimiento',
            'tests': 9
        }
    ]
    
    resultados = []
    
    for i, modulo in enumerate(modulos, 1):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"\n{'='*80}")
        print(f"  MÓDULO {i}/6")
        print(f"{'='*80}")
        
        exito = ejecutar_modulo(
            modulo['archivo'],
            modulo['titulo'],
            modulo['descripcion'],
            modulo['tests']
        )
        
        resultados.append({
            'modulo': modulo['archivo'],
            'exito': exito,
            'tests': modulo['tests']
        })
    
    # Resumen final
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "█"*80)
    print("  ✅ GENERACIÓN DE REPORTES COMPLETADA")
    print("█"*80)
    print("\n  RESUMEN:")
    
    total_tests = 0
    for r in resultados:
        estado = "✓ PASS" if r['exito'] else "✗ FAIL"
        print(f"    - {r['modulo']:<30} {r['tests']:>3} tests  {estado}")
        total_tests += r['tests']
    
    print(f"\n  TOTAL: {total_tests} pruebas unitarias")
    print("\n" + "█"*80)
    print("\n  📂 Archivos generados:")
    print("     - reporte_test_embeddings_*.txt")
    print("     - reporte_test_chunking_*.txt")
    print("     - reporte_test_hybrid_validator_*.txt")
    print("     - reporte_test_groq_api_*.txt")
    print("     - reporte_test_sm2_algorithm_*.txt")
    print("     - reporte_test_integration_*.txt")
    print("\n  📋 Usa estos reportes para copiar al Word y tomar capturas")
    print("█"*80)
    
    input("\n⏸  Presiona ENTER para finalizar...")

if __name__ == '__main__':
    # Cambiar al directorio backend
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
