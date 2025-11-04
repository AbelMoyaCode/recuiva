-- ========================================
-- DATOS DE PRUEBA - RECUIVA
-- ========================================
-- Ejecutar DESPUÉS de supabase_schema.sql
-- ========================================

-- ⚠️ IMPORTANTE: Reemplaza el USER_ID con tu UUID real de Supabase
-- Para obtenerlo:
-- 1. Ve a Authentication > Users en Supabase Dashboard
-- 2. Copia el UUID del usuario (ejemplo: fff50ee0-b929-4d29-9eaf-c59ab7026bf6)

-- ========================================
-- CONFIGURACIÓN: CAMBIA ESTE UUID
-- ========================================
DO $$
DECLARE
    v_user_id UUID := 'fff50ee0-b929-4d29-9eaf-c59ab7026bf6'; -- ✅ REEMPLAZA CON TU USER_ID
    v_material1_id UUID;
    v_material2_id UUID;
    v_folder1_id UUID;
    v_folder2_id UUID;
    v_question1_id UUID;
BEGIN

-- ========================================
-- 1. PERFIL DE USUARIO
-- ========================================
INSERT INTO public.user_profiles (id, full_name, institution)
VALUES (
    v_user_id,
    'Juan Pérez',
    'Universidad Privada Antenor Orrego'
) ON CONFLICT (id) DO NOTHING;

-- ========================================
-- 2. CARPETAS DE EJEMPLO
-- ========================================
-- Carpeta raíz: Anatomía
INSERT INTO public.folders (id, user_id, parent_folder_id, name, path, color)
VALUES (
    gen_random_uuid(),
    v_user_id,
    NULL,
    'Anatomía Dental',
    'Anatomía Dental',
    '#FF6B35'
) RETURNING id INTO v_folder1_id;

-- Subcarpeta: Capítulo 1
INSERT INTO public.folders (user_id, parent_folder_id, name, path, color)
VALUES (
    v_user_id,
    v_folder1_id,
    'Capítulo 1: Dientes',
    'Anatomía Dental > Capítulo 1: Dientes',
    '#4ECDC4'
) RETURNING id INTO v_folder2_id;

-- ========================================
-- 3. MATERIALES DE EJEMPLO
-- ========================================
-- Material 1: PDF de Anatomía
INSERT INTO public.materials (
    user_id, 
    title, 
    file_name, 
    file_type, 
    total_chunks,
    total_characters,
    estimated_pages,
    processing_status
)
VALUES (
    v_user_id,
    'Anatomía Dental - Capítulo 1',
    'anatomia_dental_cap1.pdf',
    'pdf',
    25,
    12500,
    15,
    'completed'
) RETURNING id INTO v_material1_id;

-- Asociar material1 con folder2
INSERT INTO public.material_folders (material_id, folder_id)
VALUES (v_material1_id, v_folder2_id);

-- Material 2: TXT de Resumen
INSERT INTO public.materials (
    user_id, 
    title, 
    file_name, 
    file_type, 
    total_chunks,
    total_characters,
    processing_status
)
VALUES (
    v_user_id,
    'Resumen de Anatomía',
    'resumen_anatomia.txt',
    'txt',
    10,
    5000,
    'completed'
) RETURNING id INTO v_material2_id;

-- Asociar material2 con folder1
INSERT INTO public.material_folders (material_id, folder_id)
VALUES (v_material2_id, v_folder1_id);

-- ========================================
-- 4. PREGUNTAS DE EJEMPLO
-- ========================================
INSERT INTO public.questions (
    user_id,
    material_id,
    question_text,
    topic,
    difficulty
)
VALUES (
    v_user_id,
    v_material1_id,
    '¿Cuáles son las partes anatómicas de un diente?',
    'Anatomía Dental',
    'medium'
) RETURNING id INTO v_question1_id;

INSERT INTO public.questions (
    user_id,
    material_id,
    question_text,
    topic,
    difficulty
)
VALUES (
    v_user_id,
    v_material1_id,
    'Explica la función del esmalte dental',
    'Anatomía Dental',
    'easy'
);

-- ========================================
-- 5. RESPUESTAS DE EJEMPLO
-- ========================================
INSERT INTO public.answers (
    user_id,
    question_id,
    answer_text,
    score,
    similarity,
    is_correct,
    classification,
    feedback
)
VALUES (
    v_user_id,
    v_question1_id,
    'Las partes de un diente son: corona, cuello y raíz',
    85.50,
    0.8550,
    true,
    'BUENO',
    'Respuesta correcta. Has identificado las tres partes principales del diente.'
);

-- ========================================
-- 6. REPETICIÓN ESPACIADA
-- ========================================
INSERT INTO public.spaced_repetition (
    user_id,
    question_id,
    next_review,
    interval_days,
    ease_factor,
    repetitions,
    last_score
)
VALUES (
    v_user_id,
    v_question1_id,
    CURRENT_DATE + INTERVAL '3 days',
    3,
    2.5,
    1,
    85.50
);

END $$;

-- ========================================
-- ✅ VERIFICACIÓN
-- ========================================
-- Ejecuta estas queries para ver los datos creados:

-- SELECT * FROM public.user_profiles;
-- SELECT * FROM public.folders;
-- SELECT * FROM public.materials;
-- SELECT * FROM public.material_folders;
-- SELECT * FROM public.questions;
-- SELECT * FROM public.answers;
-- SELECT * FROM public.spaced_repetition;

-- Ver estadísticas del usuario:
-- SELECT * FROM public.user_stats;

-- Ver preguntas pendientes de repaso:
-- SELECT * FROM public.questions_due_for_review;
