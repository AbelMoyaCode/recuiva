#!/usr/bin/env python3
"""
Recuiva - Launcher de Embeddings
Permite elegir entre ejecución en terminal o GUI visual

Autor: Abel Moya
Fecha: 30/09/2025
"""

import os
import sys
import subprocess

def mostrar_menu():
    """Mostrar menú de opciones"""
    print("\n" + "="*60)
    print("🚀 RECUIVA - GENERADOR DE EMBEDDINGS")
    print("   Evidencia Técnica HU-010: Active Recall Semantic Processing")
    print("="*60)
    print()
    print("Elige el modo de ejecución:")
    print()
    print("1. 🖥️  GUI VISUAL (Recomendado para demostración)")
    print("   • Interfaz gráfica completa")
    print("   • Upload visual de PDF")
    print("   • Barras de progreso")
    print("   • Métricas en tiempo real")
    print("   • Perfecto para mostrar al profesor")
    print()
    print("2. 💻 CONSOLA/TERMINAL (Modo técnico)")
    print("   • Ejecución por línea de comandos")
    print("   • Output detallado en terminal")
    print("   • Ideal para development/debugging")
    print()
    print("3. ❓ AYUDA")
    print("   • Información sobre el proyecto")
    print()
    print("4. 🚪 SALIR")
    print()

def mostrar_ayuda():
    """Mostrar información de ayuda"""
    print("\n" + "="*60)
    print("📚 INFORMACIÓN DEL PROYECTO")
    print("="*60)
    print()
    print("🎯 PROPÓSITO:")
    print("   Este script genera embeddings (vectores semánticos) para demostrar")
    print("   capacidades técnicas de procesamiento semántico en el proyecto Recuiva.")
    print()
    print("🏫 CONTEXTO ACADÉMICO:")
    print("   • Taller Integrador I - UPAO")
    print("   • Historia de Usuario HU-010: Implementación de embeddings")
    print("   • Evidencia técnica para presentación al profesor")
    print("   • Demostración de validación semántica en Active Recall")
    print()
    print("⚙️ TECNOLOGÍAS UTILIZADAS:")
    print("   • sentence-transformers (all-MiniLM-L6-v2)")
    print("   • PyPDF2 para lectura de PDF")
    print("   • NumPy para cálculos matemáticos")
    print("   • Tkinter para interfaz gráfica")
    print("   • JSON para almacenamiento de resultados")
    print()
    print("📊 FUNCIONALIDADES:")
    print("   • Lectura de archivos PDF y TXT")
    print("   • División automática en chunks")
    print("   • Generación de embeddings de 384 dimensiones")
    print("   • Cálculo de similaridades coseno")
    print("   • Exportación de resultados en JSON")
    print()
    print("🎬 DEMOSTRACIÓN:")
    print("   1. Selecciona un archivo PDF/TXT")
    print("   2. Observa el procesamiento en tiempo real")
    print("   3. Revisa las métricas de similaridad")
    print("   4. Guarda los resultados como evidencia")
    print()
    print("✅ EVIDENCIA GENERADA:")
    print("   • Archivo JSON con embeddings completos")
    print("   • Métricas de procesamiento")
    print("   • Top-3 chunks más similares")
    print("   • Timestamps y metadata técnica")
    print()

def verificar_dependencias():
    """Verificar si las dependencias están instaladas"""
    try:
        import sentence_transformers
        transformers_ok = True
    except ImportError:
        transformers_ok = False
        
    try:
        import PyPDF2
        pdf_ok = True
    except ImportError:
        pdf_ok = False
        
    try:
        import tkinter
        tkinter_ok = True
    except ImportError:
        tkinter_ok = False
        
    return transformers_ok, pdf_ok, tkinter_ok

def instalar_dependencias():
    """Guía para instalar dependencias"""
    print("\n" + "⚠️"*20)
    print("DEPENDENCIAS FALTANTES")
    print("⚠️"*20)
    print()
    
    transformers_ok, pdf_ok, tkinter_ok = verificar_dependencias()
    
    if not transformers_ok:
        print("❌ sentence-transformers no está instalado")
        print("   Instalar con: pip install sentence-transformers")
        print()
        
    if not pdf_ok:
        print("❌ PyPDF2 no está instalado")
        print("   Instalar con: pip install PyPDF2")
        print()
        
    if not tkinter_ok:
        print("❌ tkinter no está disponible")
        print("   (Generalmente viene preinstalado con Python)")
        print()
        
    if transformers_ok and pdf_ok and tkinter_ok:
        print("✅ Todas las dependencias están instaladas!")
        return True
        
    print("🔧 Para instalar todas las dependencias:")
    print("   pip install sentence-transformers PyPDF2 numpy")
    print()
    
    respuesta = input("¿Quieres intentar instalar automáticamente? (y/n): ")
    if respuesta.lower() in ['y', 'yes', 's', 'si']:
        try:
            print("Instalando dependencias...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", 
                                 "sentence-transformers", "PyPDF2", "numpy<2"])
            print("✅ Dependencias instaladas exitosamente!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False
    
    return False

def ejecutar_gui():
    """Ejecutar la interfaz gráfica"""
    transformers_ok, pdf_ok, tkinter_ok = verificar_dependencias()
    
    if not tkinter_ok:
        print("❌ Error: tkinter no está disponible.")
        print("La GUI requiere tkinter que viene preinstalado con Python.")
        input("Presiona Enter para continuar...")
        return
        
    print("\n🚀 Iniciando GUI Visual...")
    print("   • Cargando interfaz gráfica")
    print("   • Inicializando componentes")
    
    try:
        # Importar y ejecutar GUI
        import embeddings_gui
        print("   • ✅ GUI cargada exitosamente")
        print("\n💡 La ventana debería aparecer en unos segundos...")
        print("💡 Si no aparece, revisa si está minimizada en la barra de tareas")
        
        # Ejecutar GUI
        embeddings_gui.main()
        
    except ImportError as e:
        print(f"\n❌ Error importando GUI: {e}")
        print("Asegúrate de que embeddings_gui.py esté en el mismo directorio")
        input("Presiona Enter para continuar...")
    except Exception as e:
        print(f"\n❌ Error ejecutando GUI: {e}")
        input("Presiona Enter para continuar...")

def ejecutar_consola():
    """Ejecutar en modo consola"""
    print("\n💻 Iniciando modo consola...")
    print("   • Cargando script de terminal")
    
    try:
        # Verificar si existe el script original
        if os.path.exists("embeddings_local.py"):
            print("   • ✅ Script encontrado: embeddings_local.py")
            print("\n" + "-"*50)
            
            # Ejecutar script original
            subprocess.run([sys.executable, "embeddings_local.py"])
            
            print("-"*50)
        else:
            print("   • ❌ Script embeddings_local.py no encontrado")
            print("\nCreando versión básica de consola...")
            
            # Crear versión básica si no existe
            crear_script_basico_consola()
            
    except Exception as e:
        print(f"\n❌ Error ejecutando script de consola: {e}")
        input("Presiona Enter para continuar...")

def crear_script_basico_consola():
    """Crear script básico de consola si no existe"""
    script_basico = """#!/usr/bin/env python3
# Script básico de consola para embeddings
print("Ejecutando script básico de embeddings...")
print("Para funcionalidad completa, usa embeddings_local.py")
"""
    
    with open("embeddings_console_basic.py", "w") as f:
        f.write(script_basico)
        
    subprocess.run([sys.executable, "embeddings_console_basic.py"])

def main():
    """Función principal del launcher"""
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("Selecciona una opción (1-4): ").strip()
            
            if opcion == "1":
                ejecutar_gui()
                
            elif opcion == "2":
                ejecutar_consola()
                
            elif opcion == "3":
                mostrar_ayuda()
                input("\nPresiona Enter para volver al menú...")
                
            elif opcion == "4":
                print("\n👋 ¡Gracias por usar Recuiva Embeddings Generator!")
                print("   Proyecto: Active Recall Semantic Processing")
                print("   Autor: Abel Moya - Taller Integrador I UPAO")
                print()
                break
                
            else:
                print("\n❌ Opción no válida. Selecciona 1, 2, 3 o 4.")
                input("Presiona Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Saliendo del programa...")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    print("🚀 Recuiva Embeddings Launcher")
    print("   Inicializando sistema...")
    
    # Verificar dependencias al inicio
    transformers_ok, pdf_ok, tkinter_ok = verificar_dependencias()
    
    if not (transformers_ok and pdf_ok):
        print("\n⚠️ Algunas dependencias no están instaladas.")
        if not instalar_dependencias():
            print("\n💡 Puedes continuar, pero algunas funciones estarán limitadas.")
            print("💡 Los embeddings se generarán en modo 'mock' si no están las librerías.")
            input("Presiona Enter para continuar...")
    
    main()