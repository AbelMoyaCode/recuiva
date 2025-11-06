"""
Supabase Client Module for Recuiva Backend
Manages connection to Supabase database
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno (.env tiene prioridad sobre las del sistema)
load_dotenv(override=False)  # No sobrescribir variables de Docker

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Debug: Verificar que las variables estén disponibles
print(f"🔍 [supabase_client.py] SUPABASE_URL cargada: {'✅' if SUPABASE_URL else '❌'}")
print(f"🔍 [supabase_client.py] SUPABASE_KEY cargada: {'✅' if SUPABASE_KEY else '❌'}")
if SUPABASE_URL:
    print(f"🔍 [supabase_client.py] URL: {SUPABASE_URL}")

# Cliente global de Supabase
supabase: Client = None

def get_supabase_client() -> Client:
    """
    Obtiene o crea el cliente de Supabase
    Returns:
        Client: Cliente de Supabase inicializado
    """
    global supabase
    
    if supabase is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError(
                "❌ SUPABASE_URL y SUPABASE_KEY deben estar configurados en .env"
            )
        
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✅ Cliente de Supabase inicializado: {SUPABASE_URL}")
    
    return supabase

def test_connection():
    """
    Prueba la conexión a Supabase
    Returns:
        bool: True si la conexión es exitosa
    """
    try:
        client = get_supabase_client()
        # Intentar hacer una consulta simple
        result = client.table('materials').select("count", count='exact').execute()
        print(f"✅ Conexión exitosa a Supabase. Materiales en BD: {result.count}")
        return True
    except Exception as e:
        print(f"❌ Error al conectar con Supabase: {e}")
        return False
