-- ============================================================
-- 🔧 FIX OCR CORRUPTION - LIMPIAR TODOS LOS MATERIALES
-- ============================================================
-- Problema: Espacios incorrectos en medio de palabras en PDFs
-- Ejemplos: "di letante" → "diletante", "r encor" → "rencor"
-- ============================================================

-- ============================================================
-- OPCIÓN A: LIMPIAR SOLO "El Collar De La Reina"
-- ============================================================

-- PASO 1: Ver chunks ANTES de la limpieza (material específico)
SELECT 
    chunk_index,
    LEFT(chunk_text, 150) AS texto_antes,
    LENGTH(chunk_text) AS longitud
FROM material_embeddings
WHERE material_id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56'
ORDER BY chunk_index
LIMIT 5;

-- PASO 2A: Limpiar SOLO "El Collar De La Reina"
-- 🔧 Patrón 1: Reparar palabras cortas (1-3 letras)
UPDATE material_embeddings
SET chunk_text = regexp_replace(
    chunk_text,
    '([a-záéíóúñ]{3,})\s+([a-záéíóúñ]{1,3})(\s|[,.:;!?\n])',
    '\1\2\3',
    'g'
)
WHERE material_id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56';

-- 🔧 Patrón 2: Reparar palabras largas (4+ letras)
UPDATE material_embeddings
SET chunk_text = regexp_replace(
    chunk_text,
    '([a-záéíóúñ]{2,})\s+([a-záéíóúñ]{4,})',
    '\1\2',
    'g'
)
WHERE material_id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56';

-- PASO 3A: Verificar limpieza (material específico)
SELECT 
    chunk_index,
    LEFT(chunk_text, 150) AS texto_despues,
    LENGTH(chunk_text) AS longitud
FROM material_embeddings
WHERE material_id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56'
ORDER BY chunk_index
LIMIT 10;

-- ============================================================
-- OPCIÓN B: LIMPIAR **TODOS** LOS MATERIALES EN LA BD
-- ============================================================

-- PASO 1B: Ver cuántos materiales tienes
SELECT 
    COUNT(DISTINCT material_id) AS total_materiales,
    COUNT(*) AS total_chunks
FROM material_embeddings;

-- PASO 2B: Ver muestra de chunks ANTES (todos los materiales)
SELECT 
    me.material_id,
    m.title,
    LEFT(me.chunk_text, 100) AS preview
FROM material_embeddings me
JOIN materials m ON me.material_id = m.id
WHERE me.chunk_index = 0
ORDER BY m.created_at DESC
LIMIT 5;

-- PASO 3B: Limpiar TODOS los chunks (SIN filtro de material_id)
-- ⚠️ ADVERTENCIA: Esto afectará TODOS los PDFs en tu base de datos

-- 🔧 Patrón 1: Reparar palabras cortas (TODOS los materiales)
UPDATE material_embeddings
SET chunk_text = regexp_replace(
    chunk_text,
    '([a-záéíóúñ]{3,})\s+([a-záéíóúñ]{1,3})(\s|[,.:;!?\n])',
    '\1\2\3',
    'g'
);
-- SIN WHERE = afecta TODAS las filas

-- 🔧 Patrón 2: Reparar palabras largas (TODOS los materiales)
UPDATE material_embeddings
SET chunk_text = regexp_replace(
    chunk_text,
    '([a-záéíóúñ]{2,})\s+([a-záéíóúñ]{4,})',
    '\1\2',
    'g'
);
-- SIN WHERE = afecta TODAS las filas

-- PASO 4B: Verificar limpieza (todos los materiales)
SELECT 
    me.material_id,
    m.title,
    LEFT(me.chunk_text, 100) AS texto_limpio
FROM material_embeddings me
JOIN materials m ON me.material_id = m.id
WHERE me.chunk_index = 0
ORDER BY m.created_at DESC
LIMIT 5;

-- ============================================================
-- PASO FINAL: BUSCAR NOMBRES PROPIOS (deben aparecer ahora)
-- ============================================================
SELECT 
    chunk_index,
    LEFT(chunk_text, 200) AS fragmento
FROM material_embeddings
WHERE material_id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56'
  AND (
    chunk_text ILIKE '%María Antonieta%' 
    OR chunk_text ILIKE '%Jeanne%'
    OR chunk_text ILIKE '%Rétaux%'
  )
LIMIT 5;

-- ============================================================
-- RESULTADO ESPERADO:
-- ============================================================
-- ✅ Texto ANTES: "porunrefinamientode diletanteen buscadeemociones"
-- ✅ Texto DESPUÉS: "por un refinamiento de diletante en busca de emociones"
-- 
-- ✅ Texto ANTES: "despedirse. El lareprimióun movimientoder etroceso"
-- ✅ Texto DESPUÉS: "despedirse. El la reprimió un movimiento de retroceso"
--
-- ✅ Nombres propios detectados: "María Antonieta", "Jeanne de Valois", "Rétaux de Villette"
-- ============================================================
