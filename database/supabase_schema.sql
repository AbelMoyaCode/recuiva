-- ========================================
-- ESQUEMA DE BASE DE DATOS PARA RECUIVA
-- ========================================
-- Este archivo debe ejecutarse en Supabase SQL Editor
-- Ir a: Dashboard > SQL Editor > New Query > Pegar este código > Run

-- ========================================
-- 🔥 MIGRACIONES (EJECUTAR PRIMERO SI LAS TABLAS YA EXISTEN)
-- ========================================
-- Copiar desde aquí y ejecutar en Supabase SQL Editor

-- ========================================
-- PASO 1: Habilitar extensión pgvector para embeddings
-- ========================================
CREATE EXTENSION IF NOT EXISTS vector;

-- ========================================
-- PASO 2: Permitir que file_path sea NULL
-- ========================================
ALTER TABLE public.materials 
ALTER COLUMN file_path DROP NOT NULL;

-- ========================================
-- PASO 3: Agregar columnas faltantes a tabla questions
-- ========================================
ALTER TABLE public.questions 
ADD COLUMN IF NOT EXISTS topic TEXT,
ADD COLUMN IF NOT EXISTS difficulty TEXT DEFAULT 'medium',
ADD COLUMN IF NOT EXISTS expected_answer TEXT;

-- ========================================
-- PASO 4: Agregar columnas faltantes a tabla materials
-- ========================================
ALTER TABLE public.materials 
ADD COLUMN IF NOT EXISTS total_chunks INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS total_characters INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS estimated_pages INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS storage_bucket TEXT DEFAULT 'materials',
ADD COLUMN IF NOT EXISTS storage_path TEXT,
ADD COLUMN IF NOT EXISTS processing_status TEXT DEFAULT 'pending';

-- ========================================
-- FIN DE MIGRACIONES
-- ========================================

-- ========================================
-- TABLA: materials
-- Almacena los PDFs/TXTs subidos por cada usuario
-- ========================================
CREATE TABLE IF NOT EXISTS public.materials (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT, -- Ruta en el servidor (puede ser NULL si se usa Supabase Storage)
    file_type TEXT NOT NULL, -- 'pdf' o 'txt'
    total_chunks INTEGER DEFAULT 0, -- ✅ NUEVO: Total de chunks procesados
    total_characters INTEGER DEFAULT 0, -- ✅ NUEVO: Total de caracteres
    estimated_pages INTEGER DEFAULT 0, -- ✅ NUEVO: Páginas estimadas
    storage_bucket TEXT DEFAULT 'materials', -- ✅ NUEVO: Bucket de Supabase Storage
    storage_path TEXT, -- ✅ NUEVO: Ruta en Storage
    processing_status TEXT DEFAULT 'pending', -- ✅ NUEVO: 'pending', 'processing', 'completed', 'failed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para búsquedas rápidas por usuario
CREATE INDEX IF NOT EXISTS idx_materials_user_id ON public.materials(user_id);
CREATE INDEX IF NOT EXISTS idx_materials_status ON public.materials(processing_status);

-- ========================================
-- TABLA: material_embeddings (VECTORES CON PGVECTOR)
-- Almacena los embeddings (vectores) de cada chunk de texto
-- ========================================
CREATE TABLE IF NOT EXISTS public.material_embeddings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(384) NOT NULL, -- Dimensión del modelo all-MiniLM-L6-v2
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(material_id, chunk_index) -- Un chunk por material
);

-- Índice para búsquedas vectoriales (similitud coseno)
-- OPTIMIZADO: lists calculado para 100-1000 chunks por material
-- Fórmula: lists = sqrt(total_rows_esperados)
-- Para 100 materiales × 300 chunks = 30,000 embeddings → sqrt(30000) ≈ 173
CREATE INDEX IF NOT EXISTS idx_embeddings_ivfflat
ON public.material_embeddings 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- Ajustar a 200-300 si tienes > 50,000 embeddings

-- Índice para búsquedas por material
CREATE INDEX IF NOT EXISTS idx_embeddings_material_id ON public.material_embeddings(material_id);

-- ========================================
-- TABLA: folders (ORGANIZACIÓN DE CARPETAS)
-- Permite a cada usuario organizar sus materiales en carpetas
-- ========================================
CREATE TABLE IF NOT EXISTS public.folders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    parent_folder_id UUID REFERENCES public.folders(id) ON DELETE CASCADE, -- NULL = carpeta raíz
    name TEXT NOT NULL,
    path TEXT, -- Ruta completa tipo "Anatomía > Capítulo 1 > Tema 3"
    color TEXT DEFAULT '#FF6B35', -- Color para UI
    icon TEXT DEFAULT 'folder', -- Ícono material-symbols
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_folders_user_id ON public.folders(user_id);
CREATE INDEX IF NOT EXISTS idx_folders_parent_id ON public.folders(parent_folder_id);

-- ========================================
-- TABLA: material_folders (RELACIÓN MUCHOS A MUCHOS)
-- Un material puede estar en varias carpetas
-- ========================================
CREATE TABLE IF NOT EXISTS public.material_folders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
    folder_id UUID NOT NULL REFERENCES public.folders(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    -- Un material no puede estar 2 veces en la misma carpeta
    UNIQUE(material_id, folder_id)
);

CREATE INDEX IF NOT EXISTS idx_material_folders_material ON public.material_folders(material_id);
CREATE INDEX IF NOT EXISTS idx_material_folders_folder ON public.material_folders(folder_id);

-- ========================================
-- TABLA: questions
-- Almacena las preguntas creadas por cada usuario
-- ========================================
CREATE TABLE IF NOT EXISTS public.questions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    material_id UUID NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    topic TEXT, -- ✅ NUEVO: Tema/categoría de la pregunta
    difficulty TEXT DEFAULT 'medium', -- ✅ NUEVO: 'easy', 'medium', 'hard'
    expected_answer TEXT, -- Opcional: respuesta esperada generada por el sistema
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_questions_user_id ON public.questions(user_id);
CREATE INDEX IF NOT EXISTS idx_questions_material_id ON public.questions(material_id);

-- ========================================
-- TABLA: answers
-- Almacena las respuestas de los usuarios y su validación
-- ========================================
CREATE TABLE IF NOT EXISTS public.answers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    score DECIMAL(5,2) NOT NULL, -- Puntuación 0.00 - 100.00
    similarity DECIMAL(5,4), -- ✅ NUEVO: Similitud semántica 0.0000 - 1.0000
    is_correct BOOLEAN DEFAULT FALSE, -- ✅ NUEVO: Si pasó el umbral
    classification TEXT NOT NULL, -- 'EXCELENTE', 'BUENO', 'ACEPTABLE', 'INSUFICIENTE'
    feedback TEXT, -- ✅ CAMBIADO: De JSONB a TEXT para simplicidad
    best_match_chunk TEXT, -- ✅ NUEVO: El chunk que mejor coincidió
    relevant_chunks JSONB, -- ✅ NUEVO: Top 3 chunks relevantes con scores
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_answers_user_id ON public.answers(user_id);
CREATE INDEX IF NOT EXISTS idx_answers_question_id ON public.answers(question_id);
CREATE INDEX IF NOT EXISTS idx_answers_score ON public.answers(score);

-- ========================================
-- TABLA: user_profiles
-- Información adicional de usuarios (opcional pero recomendada)
-- ========================================
CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT,
    avatar_url TEXT,
    bio TEXT,
    institution TEXT, -- Universidad/Institución educativa
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ========================================
-- TABLA: spaced_repetition
-- Guarda el progreso de repetición espaciada por usuario y pregunta
-- Implementa algoritmo SM-2 para optimizar el aprendizaje
-- ========================================
CREATE TABLE IF NOT EXISTS public.spaced_repetition (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    next_review DATE NOT NULL, -- Fecha próxima de repaso
    interval_days INT NOT NULL DEFAULT 1, -- Intervalo actual en días
    ease_factor DECIMAL(4,2) NOT NULL DEFAULT 2.5, -- Factor de facilidad SM-2 (min: 1.3)
    repetitions INT NOT NULL DEFAULT 0, -- Número de repeticiones exitosas consecutivas
    last_score DECIMAL(5,2), -- Última puntuación obtenida (0-100)
    last_review DATE, -- Fecha del último repaso
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    -- Constraint: solo un registro por usuario y pregunta
    UNIQUE(user_id, question_id)
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_spaced_user_id ON public.spaced_repetition(user_id);
CREATE INDEX IF NOT EXISTS idx_spaced_question_id ON public.spaced_repetition(question_id);
CREATE INDEX IF NOT EXISTS idx_spaced_next_review ON public.spaced_repetition(next_review);

-- ========================================
-- ROW LEVEL SECURITY (RLS)
-- CRÍTICO: Cada usuario solo puede ver sus propios datos
-- ========================================

-- Habilitar RLS en todas las tablas
ALTER TABLE public.materials ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.material_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.material_folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.spaced_repetition ENABLE ROW LEVEL SECURITY;

-- Políticas para MATERIALS
CREATE POLICY "Users can view own materials" 
    ON public.materials FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own materials" 
    ON public.materials FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own materials" 
    ON public.materials FOR UPDATE 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own materials" 
    ON public.materials FOR DELETE 
    USING (auth.uid() = user_id);

-- Políticas para MATERIAL_EMBEDDINGS
CREATE POLICY "Users can view own embeddings" 
    ON public.material_embeddings FOR SELECT 
    USING (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert own embeddings" 
    ON public.material_embeddings FOR INSERT 
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete own embeddings" 
    ON public.material_embeddings FOR DELETE 
    USING (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

-- Políticas para FOLDERS
CREATE POLICY "Users can view own folders" 
    ON public.folders FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own folders" 
    ON public.folders FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own folders" 
    ON public.folders FOR UPDATE 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own folders" 
    ON public.folders FOR DELETE 
    USING (auth.uid() = user_id);

-- Políticas para MATERIAL_FOLDERS (relación)
CREATE POLICY "Users can view own material_folders" 
    ON public.material_folders FOR SELECT 
    USING (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert own material_folders" 
    ON public.material_folders FOR INSERT 
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete own material_folders" 
    ON public.material_folders FOR DELETE 
    USING (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

-- Políticas para QUESTIONS
CREATE POLICY "Users can view own questions" 
    ON public.questions FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own questions" 
    ON public.questions FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own questions" 
    ON public.questions FOR DELETE 
    USING (auth.uid() = user_id);

-- Políticas para ANSWERS
CREATE POLICY "Users can view own answers" 
    ON public.answers FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own answers" 
    ON public.answers FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

-- Políticas para USER_PROFILES
CREATE POLICY "Users can view own profile" 
    ON public.user_profiles FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" 
    ON public.user_profiles FOR UPDATE 
    USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" 
    ON public.user_profiles FOR INSERT 
    WITH CHECK (auth.uid() = id);

-- Políticas para SPACED_REPETITION
CREATE POLICY "Users can view own spaced repetition" 
    ON public.spaced_repetition FOR SELECT 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own spaced repetition" 
    ON public.spaced_repetition FOR INSERT 
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own spaced repetition" 
    ON public.spaced_repetition FOR UPDATE 
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own spaced repetition" 
    ON public.spaced_repetition FOR DELETE 
    USING (auth.uid() = user_id);

-- ========================================
-- FUNCIONES ÚTILES
-- ========================================

-- Función para búsqueda vectorial optimizada (PGVECTOR)
-- Encuentra los chunks más similares a un embedding dado
CREATE OR REPLACE FUNCTION search_similar_chunks(
    query_embedding vector(384),
    target_material_id UUID,
    similarity_threshold FLOAT DEFAULT 0.3,
    max_results INT DEFAULT 10
)
RETURNS TABLE (
    chunk_text TEXT,
    chunk_index INTEGER,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        me.chunk_text,
        me.chunk_index,
        1 - (me.embedding <=> query_embedding) AS similarity
    FROM material_embeddings me
    WHERE me.material_id = target_material_id
        AND (1 - (me.embedding <=> query_embedding)) >= similarity_threshold
    ORDER BY me.embedding <=> query_embedding
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql STABLE;

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para materials
CREATE TRIGGER update_materials_updated_at 
    BEFORE UPDATE ON public.materials 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para folders
CREATE TRIGGER update_folders_updated_at 
    BEFORE UPDATE ON public.folders 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para user_profiles
CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON public.user_profiles 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger para spaced_repetition
CREATE TRIGGER update_spaced_repetition_updated_at 
    BEFORE UPDATE ON public.spaced_repetition 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- VISTAS ÚTILES (OPCIONAL)
-- ========================================

-- Vista para ver estadísticas por usuario
CREATE OR REPLACE VIEW public.user_stats AS
SELECT 
    u.id as user_id,
    u.email,
    COUNT(DISTINCT m.id) as total_materials,
    COUNT(DISTINCT q.id) as total_questions,
    COUNT(DISTINCT a.id) as total_answers,
    AVG(a.score) as avg_score,
    COUNT(CASE WHEN a.classification = 'EXCELENTE' THEN 1 END) as excellent_answers,
    COUNT(CASE WHEN a.classification = 'BUENO' THEN 1 END) as good_answers,
    COUNT(CASE WHEN a.classification = 'ACEPTABLE' THEN 1 END) as acceptable_answers,
    COUNT(CASE WHEN a.classification = 'INSUFICIENTE' THEN 1 END) as insufficient_answers
FROM auth.users u
LEFT JOIN public.materials m ON u.id = m.user_id
LEFT JOIN public.questions q ON u.id = q.user_id
LEFT JOIN public.answers a ON u.id = a.user_id
GROUP BY u.id, u.email;

-- Vista para estadísticas de embeddings (pgvector)
CREATE OR REPLACE VIEW public.material_embeddings_stats AS
SELECT 
    m.id as material_id,
    m.title,
    m.user_id,
    COUNT(me.id) as total_embeddings,
    AVG(LENGTH(me.chunk_text)) as avg_chunk_length,
    m.total_chunks,
    m.total_characters,
    m.estimated_pages
FROM public.materials m
LEFT JOIN public.material_embeddings me ON m.id = me.material_id
GROUP BY m.id, m.title, m.user_id, m.total_chunks, m.total_characters, m.estimated_pages;

-- Vista para preguntas pendientes de repaso (repetición espaciada)
CREATE OR REPLACE VIEW public.questions_due_for_review AS
SELECT 
    sr.user_id,
    sr.question_id,
    q.question_text,
    q.material_id,
    m.title as material_title,
    sr.next_review,
    sr.interval_days,
    sr.ease_factor,
    sr.repetitions,
    sr.last_score
FROM public.spaced_repetition sr
JOIN public.questions q ON sr.question_id = q.id
JOIN public.materials m ON q.material_id = m.id
WHERE sr.next_review <= CURRENT_DATE
ORDER BY sr.next_review ASC;

-- ========================================
-- DATOS DE EJEMPLO (OPCIONAL - SOLO PARA DESARROLLO)
-- ========================================
-- NO ejecutar en producción, solo para testing local

-- Insertar usuario de prueba (requiere que ya exista en auth.users)
-- INSERT INTO public.user_profiles (id, full_name, institution)
-- VALUES (
--     '00000000-0000-0000-0000-000000000000', -- Reemplazar con UUID real de auth.users
--     'Usuario de Prueba',
--     'Universidad de Ejemplo'
-- );

-- ========================================
-- VERIFICACIÓN
-- ========================================
-- Ejecuta estas queries para verificar que todo se creó correctamente:

-- Ver todas las tablas creadas
-- SELECT * FROM information_schema.tables WHERE table_schema = 'public';

-- Ver todas las políticas RLS
-- SELECT * FROM pg_policies WHERE schemaname = 'public';

-- Verificar que pgvector está habilitado
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Ver columnas de material_embeddings
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'material_embeddings';

-- Ver políticas RLS
SELECT policyname 
FROM pg_policies 
WHERE tablename = 'material_embeddings';

-- Ver estadísticas de embeddings
-- SELECT * FROM material_embeddings_stats;

-- ========================================
-- EJEMPLOS DE USO DE BÚSQUEDA VECTORIAL
-- ========================================

-- Ejemplo 1: Buscar chunks similares a un embedding
-- (Reemplaza el array con un embedding real de 384 dimensiones)
/*
SELECT * FROM search_similar_chunks(
    '[0.1, 0.2, 0.3, ...]'::vector(384),  -- Embedding de la pregunta
    'uuid-del-material'::UUID,             -- ID del material
    0.5,                                   -- Umbral de similitud mínima (0-1)
    5                                      -- Top 5 resultados
);
*/

-- Ejemplo 2: Búsqueda manual con operador de distancia
/*
SELECT 
    chunk_text,
    chunk_index,
    1 - (embedding <=> '[0.1, 0.2, ...]'::vector(384)) AS similarity
FROM material_embeddings
WHERE material_id = 'uuid-del-material'
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector(384)
LIMIT 10;
*/

-- Ejemplo 3: Ver todos los embeddings de un material
/*
SELECT 
    chunk_index,
    LEFT(chunk_text, 100) as preview,
    created_at
FROM material_embeddings
WHERE material_id = 'uuid-del-material'
ORDER BY chunk_index;
*/

-- Ejemplo 4: Contar embeddings por material
/*
SELECT 
    m.title,
    COUNT(me.id) as total_embeddings,
    m.total_chunks
FROM materials m
LEFT JOIN material_embeddings me ON m.id = me.material_id
WHERE m.user_id = auth.uid()
GROUP BY m.id, m.title, m.total_chunks;
*/
-- ============================================================
-- FIX: Políticas RLS faltantes para tabla materials
-- ============================================================
-- Problema: La tabla materials tiene RLS habilitado pero no tiene
-- políticas, por lo que rechaza todas las inserciones.
-- Solución: Agregar políticas CRUD para usuarios autenticados
-- ============================================================


-- ============================================================
-- FIX DEFINITIVO: Eliminar políticas antiguas y crear nuevas
-- ============================================================

-- PASO 1: ELIMINAR TODAS LAS POLÍTICAS ANTIGUAS DE LA TABLA MATERIALS
DROP POLICY IF EXISTS "Users can view own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can insert own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can update own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can delete own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can view their own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can insert their own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can update their own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can delete their own materials" ON public.materials;

-- PASO 2: CREAR POLÍTICAS NUEVAS CON TO authenticated
CREATE POLICY "Users can view own materials" 
    ON public.materials FOR SELECT 
    TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own materials" 
    ON public.materials FOR INSERT 
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own materials" 
    ON public.materials FOR UPDATE 
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own materials" 
    ON public.materials FOR DELETE 
    TO authenticated
    USING (auth.uid() = user_id);

-- PASO 3: VERIFICAR QUE SOLO EXISTEN 4 POLÍTICAS
SELECT 
    policyname,
    cmd,
    roles
FROM pg_policies
WHERE tablename = 'materials'
ORDER BY policyname;

-- Deberías ver exactamente 4 filas:
-- 1. Users can delete own materials | DELETE | {authenticated}
-- 2. Users can insert own materials | INSERT | {authenticated}
-- 3. Users can update own materials | UPDATE | {authenticated}
-- 4. Users can view own materials   | SELECT | {authenticated}


SELECT policyname FROM pg_policies WHERE tablename = 'materials';

SELECT policyname, cmd, roles FROM pg_policies WHERE tablename = 'materials' ORDER BY cmd;








-- ============================================
-- FIX: Agregar columnas faltantes en tabla answers
-- Ejecutar en Supabase SQL Editor
-- ============================================

-- PASO 1: Verificar columnas actuales
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'answers' 
ORDER BY ordinal_position;

-- PASO 2: Agregar columnas faltantes (si no existen)

-- Columna: similarity (similitud semántica)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'answers' AND column_name = 'similarity'
    ) THEN
        ALTER TABLE public.answers 
        ADD COLUMN similarity DECIMAL(5,4);
        
        RAISE NOTICE '✅ Columna similarity agregada';
    ELSE
        RAISE NOTICE '⚠️ Columna similarity ya existe';
    END IF;
END $$;

-- Columna: is_correct (si pasó el umbral)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'answers' AND column_name = 'is_correct'
    ) THEN
        ALTER TABLE public.answers 
        ADD COLUMN is_correct BOOLEAN DEFAULT FALSE;
        
        RAISE NOTICE '✅ Columna is_correct agregada';
    ELSE
        RAISE NOTICE '⚠️ Columna is_correct ya existe';
    END IF;
END $$;

-- Columna: feedback (feedback textual)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'answers' AND column_name = 'feedback'
    ) THEN
        ALTER TABLE public.answers 
        ADD COLUMN feedback TEXT;
        
        RAISE NOTICE '✅ Columna feedback agregada';
    ELSE
        RAISE NOTICE '⚠️ Columna feedback ya existe';
    END IF;
END $$;

-- Columna: best_match_chunk (chunk más relevante)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'answers' AND column_name = 'best_match_chunk'
    ) THEN
        ALTER TABLE public.answers 
        ADD COLUMN best_match_chunk TEXT;
        
        RAISE NOTICE '✅ Columna best_match_chunk agregada';
    ELSE
        RAISE NOTICE '⚠️ Columna best_match_chunk ya existe';
    END IF;
END $$;

-- Columna: relevant_chunks (top chunks relevantes)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'answers' AND column_name = 'relevant_chunks'
    ) THEN
        ALTER TABLE public.answers 
        ADD COLUMN relevant_chunks JSONB;
        
        RAISE NOTICE '✅ Columna relevant_chunks agregada';
    ELSE
        RAISE NOTICE '⚠️ Columna relevant_chunks ya existe';
    END IF;
END $$;

-- PASO 3: Verificar columnas después de agregar
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'answers' 
ORDER BY ordinal_position;

-- ============================================
-- RESULTADO ESPERADO:
-- ============================================
-- id                  | uuid              | NO
-- user_id             | uuid              | NO
-- question_id         | uuid              | NO
-- answer_text         | text              | NO
-- score               | numeric           | NO
-- similarity          | numeric           | YES  ✅ NUEVA
-- is_correct          | boolean           | YES  ✅ NUEVA
-- classification      | text              | NO
-- feedback            | text              | YES  ✅ NUEVA
-- best_match_chunk    | text              | YES  ✅ NUEVA
-- relevant_chunks     | jsonb             | YES  ✅ NUEVA
-- created_at          | timestamp         | YES
-- ============================================





SELECT id, email, full_name FROM users 
WHERE id = 'a7ad2f68-3946-4e40-b73a-fe2867d9af0f';

INSERT INTO users (id, email, full_name, created_at, updated_at) 
VALUES (
    'a7ad2f68-3946-4e40-b73a-fe2867d9af0f',
    'juan.perez@example.com',
    'Juan Pérez',
    NOW(),
    NOW()
);




-- 2. Si NO existe, crear el usuario MOCK
-- (Ejecutar SOLO si la consulta anterior no devuelve resultados)
INSERT INTO users (
    id,
    email,
    full_name,
    created_at,
    updated_at
) VALUES (
    'a7ad2f68-3946-4e40-b73a-fe2867d9af0f',
    'juan.perez@example.com',
    'Juan Pérez',
    NOW(),
    NOW()
)
ON CONFLICT (id) DO NOTHING;



-- 3. Verificar que se creó correctamente
SELECT id, email, full_name, created_at 
FROM users 
WHERE id = 'a7ad2f68-3946-4e40-b73a-fe2867d9af0f';


-- 5. Ver los materiales de este usuario
SELECT 
    id,
    title,
    file_name,
    total_chunks,
    real_pages,
    processing_status,
    created_at
FROM materials 
WHERE user_id = 'a7ad2f68-3946-4e40-b73a-fe2867d9af0f'
ORDER BY created_at DESC;


SELECT 
    id, 
    title, 
    user_id,
    total_chunks,
    created_at
FROM materials 
WHERE user_id = '49ae3509-edb7-44b4-9ccd-004629409430'
ORDER BY created_at DESC;













-- 2.1 Permitir a usuarios autenticados SUBIR sus propias fotos
CREATE POLICY "Users can upload their own avatar"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
  bucket_id = 'avatars' 
  AND (storage.foldername(name))[1] = auth.uid()::text
);

-- 2.2 Permitir a usuarios autenticados ACTUALIZAR sus propias fotos
CREATE POLICY "Users can update their own avatar"
ON storage.objects
FOR UPDATE
TO authenticated
USING (
  bucket_id = 'avatars' 
  AND (storage.foldername(name))[1] = auth.uid()::text
);

-- 2.3 Permitir a usuarios autenticados ELIMINAR sus propias fotos
CREATE POLICY "Users can delete their own avatar"
ON storage.objects
FOR DELETE
TO authenticated
USING (
  bucket_id = 'avatars' 
  AND (storage.foldername(name))[1] = auth.uid()::text
);

-- 2.4 Permitir a TODOS (incluso no autenticados) VER las fotos
CREATE POLICY "Anyone can view avatars"
ON storage.objects
FOR SELECT
TO public
USING (bucket_id = 'avatars');


SELECT 
  policyname,
  cmd,
  roles
FROM pg_policies
WHERE tablename = 'objects'
  AND policyname LIKE '%avatar%'
ORDER BY policyname;










SELECT 
  id, 
  name, 
  public,
  file_size_limit,
  allowed_mime_types
FROM storage.buckets 
WHERE name = 'avatars';








UPDATE user_profiles 
SET avatar_url = 'https://xqicgzqgluslzleddmfv.supabase.co/storage/...'
WHERE id = 'user_id';


-- Verificar que la extensión pgvector está instalada
SELECT * FROM pg_extension WHERE extname = 'vector';



-- Query corregido dimension de embeddings 
SELECT 
  chunk_index,
  LEFT(chunk_text, 50) AS preview,
  array_length(embedding, 1) AS dimensions
FROM material_embeddings
LIMIT 5;


SELECT 
  m.title AS material,
  COUNT(me.id) AS num_chunks,
  ROUND(COUNT(me.id) * 1.5, 2) AS size_kb
FROM materials m
LEFT JOIN material_embeddings me ON m.id = me.material_id
GROUP BY m.id, m.title
ORDER BY num_chunks DESC;


SELECT 
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'material_embeddings';

SELECT proname 
FROM pg_proc 
WHERE proname = 'match_material_chunks';



CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS public.materials (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_path TEXT,
    file_type TEXT NOT NULL,
    total_chunks INTEGER DEFAULT 0,
    total_characters INTEGER DEFAULT 0,
    estimated_pages INTEGER DEFAULT 0,
    storage_bucket TEXT DEFAULT 'materials',
    storage_path TEXT,
    processing_status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.material_embeddings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(material_id, chunk_index)
);

CREATE TABLE IF NOT EXISTS public.folders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    parent_folder_id UUID REFERENCES public.folders(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    path TEXT,
    color TEXT DEFAULT '#FF6B35',
    icon TEXT DEFAULT 'folder',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.material_folders (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
    folder_id UUID NOT NULL REFERENCES public.folders(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(material_id, folder_id)
);

CREATE TABLE IF NOT EXISTS public.questions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    material_id UUID NOT NULL REFERENCES public.materials(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    topic TEXT,
    difficulty TEXT DEFAULT 'medium',
    expected_answer TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.answers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    similarity DECIMAL(5,4),
    is_correct BOOLEAN DEFAULT FALSE,
    classification TEXT NOT NULL,
    feedback TEXT,
    best_match_chunk TEXT,
    relevant_chunks JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name TEXT,
    avatar_url TEXT,
    bio TEXT,
    institution TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.spaced_repetition (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES public.questions(id) ON DELETE CASCADE,
    next_review DATE NOT NULL,
    interval_days INT NOT NULL DEFAULT 1,
    ease_factor DECIMAL(4,2) NOT NULL DEFAULT 2.5,
    repetitions INT NOT NULL DEFAULT 0,
    last_score DECIMAL(5,2),
    last_review DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, question_id)
);


CREATE INDEX IF NOT EXISTS idx_materials_user_id ON public.materials(user_id);
CREATE INDEX IF NOT EXISTS idx_materials_status ON public.materials(processing_status);

CREATE INDEX IF NOT EXISTS idx_embeddings_ivfflat
ON public.material_embeddings 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS idx_embeddings_material_id ON public.material_embeddings(material_id);

CREATE INDEX IF NOT EXISTS idx_folders_user_id ON public.folders(user_id);
CREATE INDEX IF NOT EXISTS idx_folders_parent_id ON public.folders(parent_folder_id);

CREATE INDEX IF NOT EXISTS idx_material_folders_material ON public.material_folders(material_id);
CREATE INDEX IF NOT EXISTS idx_material_folders_folder ON public.material_folders(folder_id);

CREATE INDEX IF NOT EXISTS idx_questions_user_id ON public.questions(user_id);
CREATE INDEX IF NOT EXISTS idx_questions_material_id ON public.questions(material_id);

CREATE INDEX IF NOT EXISTS idx_answers_user_id ON public.answers(user_id);
CREATE INDEX IF NOT EXISTS idx_answers_question_id ON public.answers(question_id);
CREATE INDEX IF NOT EXISTS idx_answers_score ON public.answers(score);

CREATE INDEX IF NOT EXISTS idx_spaced_user_id ON public.spaced_repetition(user_id);
CREATE INDEX IF NOT EXISTS idx_spaced_question_id ON public.spaced_repetition(question_id);
CREATE INDEX IF NOT EXISTS idx_spaced_next_review ON public.spaced_repetition(next_review);


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_materials_updated_at 
    BEFORE UPDATE ON public.materials 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_folders_updated_at 
    BEFORE UPDATE ON public.folders 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON public.user_profiles 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_spaced_repetition_updated_at 
    BEFORE UPDATE ON public.spaced_repetition 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();




SELECT * FROM information_schema.tables WHERE table_schema = 'public';
SELECT * FROM pg_extension WHERE extname = 'vector';
SELECT policyname, cmd, roles FROM pg_policies WHERE tablename = 'materials' ORDER BY policyname;



CREATE TABLE IF NOT EXISTS public.topics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS public.generated_questions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID REFERENCES public.materials(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES public.topics(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL,
    reference_chunk_index INTEGER,
    concepts TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


ALTER TABLE public.materials 
ADD COLUMN IF NOT EXISTS topic_id UUID REFERENCES public.topics(id) ON DELETE SET NULL;



















SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';




SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'materials';

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'answers';

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'questions';

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'material_embeddings';

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'generated_questions';

SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'topics';






SELECT * FROM pg_extension WHERE extname = 'vector';




SELECT policyname, cmd, roles 
FROM pg_policies 
WHERE tablename IN (
  'materials', 
  'material_embeddings', 
  'folders', 
  'material_folders', 
  'questions', 
  'answers', 
  'user_profiles', 
  'spaced_repetition'
)
ORDER BY tablename, policyname;






SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename IN (
  'materials', 
  'material_embeddings', 
  'questions', 
  'answers', 
  'spaced_repetition'
);


































-- ========================================
-- SPRINT 2: CREAR TABLAS Y COLUMNAS FALTANTES
-- ========================================

-- 1. Crear tabla TOPICS
CREATE TABLE IF NOT EXISTS public.topics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    folder_id UUID REFERENCES public.folders(id) ON DELETE CASCADE, -- NUEVO: relación con carpeta
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Crear tabla GENERATED_QUESTIONS
CREATE TABLE IF NOT EXISTS public.generated_questions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    material_id UUID REFERENCES public.materials(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES public.topics(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL,
    reference_chunk_index INTEGER,
    concepts TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Agregar columna TOPIC_ID a tabla MATERIALS
ALTER TABLE public.materials 
ADD COLUMN IF NOT EXISTS topic_id UUID REFERENCES public.topics(id) ON DELETE SET NULL;

-- 4. Crear índices para TOPICS
CREATE INDEX IF NOT EXISTS idx_topics_user_id ON public.topics(user_id);
CREATE INDEX IF NOT EXISTS idx_topics_folder_id ON public.topics(folder_id);

-- 5. Crear índices para GENERATED_QUESTIONS
CREATE INDEX IF NOT EXISTS idx_generated_questions_material_id ON public.generated_questions(material_id);
CREATE INDEX IF NOT EXISTS idx_generated_questions_topic_id ON public.generated_questions(topic_id);

-- 6. Habilitar RLS en TOPICS
ALTER TABLE public.topics ENABLE ROW LEVEL SECURITY;

-- 7. Crear políticas RLS para TOPICS
CREATE POLICY "Users can view own topics" 
    ON public.topics FOR SELECT 
    TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own topics" 
    ON public.topics FOR INSERT 
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own topics" 
    ON public.topics FOR UPDATE 
    TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own topics" 
    ON public.topics FOR DELETE 
    TO authenticated
    USING (auth.uid() = user_id);

-- 8. Habilitar RLS en GENERATED_QUESTIONS
ALTER TABLE public.generated_questions ENABLE ROW LEVEL SECURITY;

-- 9. Crear políticas RLS para GENERATED_QUESTIONS
CREATE POLICY "Users can view own generated questions" 
    ON public.generated_questions FOR SELECT 
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert own generated questions" 
    ON public.generated_questions FOR INSERT 
    TO authenticated
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete own generated questions" 
    ON public.generated_questions FOR DELETE 
    TO authenticated
    USING (
        EXISTS (
            SELECT 1 FROM public.materials m 
            WHERE m.id = material_id AND m.user_id = auth.uid()
        )
    );

-- ========================================
-- VERIFICACIÓN FINAL
-- ========================================

-- Verificar que las tablas nuevas existen
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('topics', 'generated_questions');

-- Verificar que topic_id existe en materials
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'materials' AND column_name = 'topic_id';

-- Verificar políticas de topics
SELECT policyname 
FROM pg_policies 
WHERE tablename = 'topics';

-- Verificar políticas de generated_questions
SELECT policyname 
FROM pg_policies 
WHERE tablename = 'generated_questions';





















-- Agregar columna folder_id a tabla topics (relación con carpetas)
ALTER TABLE public.topics 
ADD COLUMN IF NOT EXISTS folder_id UUID REFERENCES public.folders(id) ON DELETE CASCADE;

-- Crear índice para folder_id
CREATE INDEX IF NOT EXISTS idx_topics_folder_id ON public.topics(folder_id);

-- Verificar que se agregó
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'topics' AND column_name = 'folder_id';


-- Ver todas las columnas de topics
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'topics';