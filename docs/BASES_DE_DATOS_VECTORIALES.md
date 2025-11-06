# 🎯 Bases de Datos Vectoriales para Recuiva

## 📖 **¿QUÉ ES UNA BASE DE DATOS VECTORIAL?**

Una base de datos vectorial es un sistema optimizado para almacenar y buscar **embeddings** (vectores numéricos que representan el significado semántico del texto).

### **¿Por qué la necesitas en Recuiva?**

Actualmente tu sistema:
1. Genera embeddings de cada chunk del PDF (vectores de 384 dimensiones)
2. Los guarda en archivos JSON locales
3. Cuando validas una respuesta, carga TODOS los embeddings a memoria
4. Calcula similitud del coseno con cada uno
5. Encuentra el top 5 más similar

**Problema**: Con 50 materiales y 10,000 chunks, esto es **muy lento** ⏱️

**Solución**: Base de datos vectorial que hace búsquedas en **milisegundos** ⚡

---

## 🏆 **COMPARACIÓN DE OPCIONES PARA RECUIVA**

| Característica | **pgvector** ⭐ | Pinecone | Qdrant | Weaviate |
|----------------|---------------|----------|---------|----------|
| **Integración con Supabase** | ✅ Nativa | ❌ API externa | ❌ API externa | ❌ API externa |
| **Costo Plan Gratis** | ✅ Incluido | ✅ 1M vectores | ✅ 1GB | ✅ Limitado |
| **Facilidad de Setup** | 🟢 Fácil | 🟡 Media | 🟡 Media | 🔴 Difícil |
| **Escalabilidad** | 🟡 Media | 🟢 Alta | 🟢 Alta | 🟢 Alta |
| **Latencia** | 🟢 <50ms | 🟢 <100ms | 🟢 <50ms | 🟡 <150ms |
| **Open Source** | ✅ Sí | ❌ No | ✅ Sí | ✅ Sí |
| **Self-Hosted** | ✅ Sí | ❌ No | ✅ Sí | ✅ Sí |
| **Cloud Managed** | ✅ Supabase | ✅ Sí | ✅ Sí | ✅ Sí |

---

## ⭐ **RECOMENDACIÓN: pgvector en Supabase**

### **¿Por qué pgvector?**

1. **Ya tienes Supabase** - No necesitas otro servicio
2. **Datos centralizados** - Metadata + vectores en un solo lugar
3. **Queries SQL familiares** - Usas SQL normal con funciones de similitud
4. **100% gratis** - Incluido en tu plan actual de Supabase
5. **Transacciones ACID** - Consistencia garantizada
6. **RLS integrado** - Los vectores también tienen seguridad por usuario

### **¿Cómo funciona?**

```sql
-- Crear tabla para embeddings
CREATE TABLE embeddings (
    id UUID PRIMARY KEY,
    material_id UUID REFERENCES materials(id),
    chunk_id INT,
    text TEXT,
    embedding vector(384)  -- pgvector: vector de 384 dimensiones
);

-- Crear índice para búsquedas rápidas
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);

-- Buscar los 5 chunks más similares
SELECT 
    text,
    1 - (embedding <=> '[0.1, 0.2, ...]') as similarity
FROM embeddings
WHERE material_id = 'uuid-del-material'
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

**Resultado**: Búsqueda en **20-50ms** vs **2-5 segundos** con archivos JSON

---

## 📊 **ARQUITECTURA RECOMENDADA PARA RECUIVA**

```
┌─────────────────────────────────────────────────────────────┐
│                       SUPABASE                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  materials   │  │  embeddings  │  │  user_profiles  │   │
│  ├──────────────┤  ├──────────────┤  ├─────────────────┤   │
│  │ id (UUID)    │  │ id (UUID)    │  │ id (UUID)       │   │
│  │ user_id      │──┤ material_id  │  │ full_name       │   │
│  │ title        │  │ chunk_id     │  │ email           │   │
│  │ file_name    │  │ text         │  └─────────────────┘   │
│  │ total_chunks │  │ embedding    │                        │
│  │ created_at   │  │  (vector384) │                        │
│  └──────────────┘  └──────────────┘                        │
│                           ↑                                 │
│                           │                                 │
│                    pgvector extension                       │
│                    Búsquedas <50ms                          │
└─────────────────────────────────────────────────────────────┘
                            ↑
                            │ REST API
                            │
                    ┌───────┴────────┐
                    │  FastAPI       │
                    │  Backend       │
                    └────────────────┘
```

---

## 🚀 **PLAN DE IMPLEMENTACIÓN - 3 HORAS**

### **Fase 1: Habilitar pgvector en Supabase** (15 min)

1. Ve a Supabase Dashboard
2. SQL Editor → New Query
3. Ejecuta:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
4. Verifica:
   ```sql
   SELECT * FROM pg_extension WHERE extname = 'vector';
   ```

### **Fase 2: Crear tabla de embeddings** (30 min)

```sql
-- Tabla para almacenar embeddings
CREATE TABLE IF NOT EXISTS public.embeddings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    chunk_id INTEGER NOT NULL,
    text TEXT NOT NULL, -- Texto del chunk
    embedding vector(384), -- Vector de 384 dimensiones (all-MiniLM-L6-v2)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(material_id, chunk_id) -- Un chunk por material
);

-- Índice para búsquedas vectoriales rápidas
CREATE INDEX embeddings_vector_idx 
    ON public.embeddings 
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Índice para filtrar por material
CREATE INDEX embeddings_material_idx ON public.embeddings(material_id);
CREATE INDEX embeddings_user_idx ON public.embeddings(user_id);

-- RLS: Cada usuario solo ve sus embeddings
ALTER TABLE public.embeddings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own embeddings" 
    ON public.embeddings FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own embeddings" 
    ON public.embeddings FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own embeddings" 
    ON public.embeddings FOR DELETE 
    USING (auth.uid() = user_id);
```

### **Fase 3: Modificar backend para usar pgvector** (1.5 horas)

**Archivo**: `backend/main.py`

```python
# En el endpoint /upload-material, después de generar embeddings:

if SUPABASE_ENABLED and user_id:
    supabase = get_supabase_client()
    
    # Guardar material (ya lo haces)
    material_result = supabase.table('materials').insert(...).execute()
    material_uuid = material_result.data[0]['id']
    
    # NUEVO: Guardar embeddings en pgvector
    print(f"💾 Guardando {len(embeddings_data)} embeddings en pgvector...")
    
    embeddings_batch = []
    for emb in embeddings_data:
        embeddings_batch.append({
            "material_id": material_uuid,
            "user_id": user_id,
            "chunk_id": emb["chunk_id"],
            "text": emb["text_full"],
            "embedding": emb["embedding"]  # Lista de 384 floats
        })
        
        # Insertar en lotes de 50 para evitar timeouts
        if len(embeddings_batch) >= 50:
            supabase.table('embeddings').insert(embeddings_batch).execute()
            embeddings_batch = []
            print(f"  ✅ {len(embeddings_batch)} embeddings guardados...")
    
    # Insertar remanentes
    if embeddings_batch:
        supabase.table('embeddings').insert(embeddings_batch).execute()
    
    print(f"✅ Todos los embeddings guardados en pgvector")
```

### **Fase 4: Modificar validación semántica** (1 hora)

```python
# En el endpoint /validate-answer:

async def validate_answer(answer: Answer, user_id: str = Header(...)):
    # Generar embedding de la respuesta del usuario
    user_embedding = generate_embeddings(answer.user_answer)
    
    # Buscar chunks más similares usando pgvector
    supabase = get_supabase_client()
    
    # Convertir embedding a string para la query
    embedding_str = str(user_embedding.tolist())
    
    # Query de similitud con pgvector
    result = supabase.rpc(
        'match_chunks',
        {
            'query_embedding': embedding_str,
            'match_threshold': 0.5,
            'match_count': 5,
            'material_uuid': answer.material_id
        }
    ).execute()
    
    # result.data contiene los 5 chunks más similares
    top_chunks = result.data
    
    # Calcular score basado en similitud (como ya lo haces)
    # ...
```

**Función SQL en Supabase** (crear en SQL Editor):

```sql
CREATE OR REPLACE FUNCTION match_chunks(
    query_embedding vector(384),
    match_threshold float,
    match_count int,
    material_uuid uuid
)
RETURNS TABLE (
    id uuid,
    chunk_id int,
    text text,
    similarity float
)
LANGUAGE sql STABLE
AS $$
    SELECT
        e.id,
        e.chunk_id,
        e.text,
        1 - (e.embedding <=> query_embedding) as similarity
    FROM embeddings e
    WHERE e.material_id = material_uuid
        AND 1 - (e.embedding <=> query_embedding) > match_threshold
    ORDER BY e.embedding <=> query_embedding
    LIMIT match_count;
$$;
```

---

## 📈 **BENEFICIOS ESPERADOS**

| Métrica | Antes (JSON local) | Después (pgvector) | Mejora |
|---------|-------------------|-------------------|--------|
| **Tiempo de búsqueda** | 2-5 segundos | 20-50ms | **100x más rápido** |
| **Memoria RAM usada** | ~500 MB | ~50 MB | **90% menos** |
| **Escalabilidad** | Max 10 materiales | Miles de materiales | **Ilimitado** |
| **Seguridad** | Sin control | RLS por usuario | **100% seguro** |
| **Backup** | Manual | Automático | **Automatizado** |

---

## 🎓 **RECURSOS PARA APRENDER**

### **Videos (VER PRIMERO)**

1. **pgvector Tutorial** - Supabase (15 min)
   - https://www.youtube.com/watch?v=Yk0kEMCEKbQ

2. **Vector Databases Explained** - Fireship (5 min)
   - https://www.youtube.com/watch?v=klTvEwg3oJ4

### **Documentación**

1. **pgvector en Supabase**
   - https://supabase.com/docs/guides/ai/vector-embeddings

2. **pgvector GitHub**
   - https://github.com/pgvector/pgvector

---

## ✅ **SIGUIENTE PASO RECOMENDADO**

1. **PRIMERO**: Prueba el sistema actual (sube 1-2 materiales)
2. **LUEGO**: Implementa pgvector siguiendo las fases
3. **FINALMENTE**: Migra los embeddings existentes a pgvector

**Tiempo total estimado**: 3-4 horas  
**Complejidad**: Media (tienes todo el código listo para copiar)

---

## 💡 **ALTERNATIVA: Pinecone (Si prefieres servicio especializado)**

### **Ventajas de Pinecone:**
- Optimizado al 100% para vectores
- Escalabilidad ilimitada
- Dashboard visual muy bueno
- SDKs para Python/JavaScript

### **Desventajas:**
- Otro servicio externo (más complejidad)
- Requiere API key adicional
- Datos fragmentados (Supabase + Pinecone)

### **¿Cuándo elegir Pinecone?**
- Si planeas escalar a **millones de vectores**
- Si necesitas **latencia <10ms**
- Si el presupuesto no es problema ($0-$70/mes)

**Para Recuiva (proyecto académico/MVP)**: **pgvector es suficiente** ✅

---

¿Listo para implementar pgvector? Te puedo guiar paso a paso 🚀
