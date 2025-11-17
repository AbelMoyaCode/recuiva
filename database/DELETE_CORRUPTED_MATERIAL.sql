-- ============================================================
-- 🗑️ ELIMINAR MATERIAL CORRUPTO "El Collar De La Reina"
-- ============================================================
-- Material ID: 0394a7f6-cb99-4886-a8e9-0ea05c5d7c56
-- ============================================================

-- PASO 1: Verificar material antes de eliminar
SELECT 
    id,
    title,
    file_name,
    total_chunks,
    created_at
FROM materials
WHERE id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56';

-- PASO 2: Ver cuántos chunks tiene
SELECT COUNT(*) AS total_chunks
FROM material_embeddings
WHERE material_id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56';

-- PASO 3: ELIMINAR chunks (se eliminan automáticamente por CASCADE)
-- PASO 4: ELIMINAR material (esto también elimina chunks por ON DELETE CASCADE)
DELETE FROM materials
WHERE id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56';

-- PASO 5: Verificar que se eliminó
SELECT COUNT(*) AS materiales_restantes
FROM materials
WHERE user_id = 'f2d8b3d1-1b98-4e6e-8c82-52acfc3888fe';

SELECT COUNT(*) AS chunks_restantes
FROM material_embeddings
WHERE material_id = '0394a7f6-cb99-4886-a8e9-0ea05c5d7c56';

-- ============================================================
-- RESULTADO ESPERADO:
-- ============================================================
-- materiales_restantes: 0
-- chunks_restantes: 0
-- ============================================================

-- ============================================================
-- SIGUIENTE PASO: VOLVER A SUBIR EL PDF
-- ============================================================
-- 1. Ve a recuiva.duckdns.org/subir-material
-- 2. Sube "El Collar De La Reina" nuevamente
-- 3. chunking.py ahora tiene el fix de OCR
-- 4. Los chunks nuevos serán MÁS LIMPIOS
-- 5. El question_generator podrá extraer nombres propios correctamente
-- ============================================================
