-- ========================================
-- ESQUEMA DE BASE DE DATOS PARA RECUIVA
-- ========================================
-- Este archivo debe ejecutarse en Supabase SQL Editor
-- Ir a: Dashboard > SQL Editor > New Query > Pegar este código > Run

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

-- SELECT * FROM information_schema.tables WHERE table_schema = 'public';
-- SELECT * FROM pg_policies WHERE schemaname = 'public';
