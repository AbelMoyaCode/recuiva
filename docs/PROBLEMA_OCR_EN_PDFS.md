# 📄 PROBLEMA: PDFs con OCR Defectuoso

## 🔍 Descripción del problema

Algunos PDFs tienen **texto extraído con OCR defectuoso**, insertando espacios en medio de palabras:

### Ejemplos reales del PDF "El Collar De La Reina":
```
❌ "habi tación" → debería ser "habitación"
❌ "entr ada" → debería ser "entrada"  
❌ "encontr aba" → debería ser "encontraba"
❌ "r encor" → debería ser "rencor"
❌ "di letante" → debería ser "diletante"
```

## 🎯 ¿Por qué ocurre esto?

**NO es culpa de Recuiva ni de PyPDF2**. El problema viene del PDF original:

1. El PDF fue **escaneado con un OCR externo** (Adobe, Tesseract, etc.)
2. El OCR insertó espacios incorrectamente al reconocer el texto
3. El texto corrupto **quedó guardado en el PDF**
4. PyPDF2 extrae el texto **tal como está** en el PDF
5. Recuiva guarda los chunks con el texto corrupto en Supabase

## ⚠️ Impacto en Recuiva

La corrupción OCR afecta:

### ❌ Generación de preguntas
- **ContentAnalyzer** no puede extraer entidades correctamente
- Extrae: `['endade ese', 'euxhizo ungesto', 'deesclavade la']`
- **Esperado:** `['María Antonieta', 'Jeanne de Valois', 'Rétaux de Villette']`
- **Resultado:** Preguntas genéricas como _"¿Qué información se presenta en este fragmento?"_

### ✅ Validación semántica (NO afectada)
- Los embeddings funcionan correctamente
- pgvector puede comparar texto corrupto vs. texto corrupto
- La validación de respuestas sigue funcionando

## 🔧 Soluciones

### ✅ Opción 1: Usar un PDF limpio (RECOMENDADO)

1. Busca otra versión del PDF sin OCR corrupto
2. O regenera el PDF con mejor OCR (Adobe Acrobat DC, Tesseract 5.x)
3. Sube el PDF limpio a Recuiva

### ✅ Opción 2: Limpiar chunks existentes con SQL

Si ya subiste el PDF corrupto:

1. Ve a Supabase SQL Editor
2. Ejecuta: `database/fix_ocr_chunks_CORRECTO.sql`
3. Los regex intentarán reparar patrones comunes:
   - `"habi tación"` → `"habitación"`
   - `"r encor"` → `"rencor"`

**Limitación:** Solo funciona para patrones simples. Palabras muy corruptas seguirán mal.

### ❌ Opción 3: Modificar chunking.py (NO RECOMENDADO)

**NO agregamos regex automáticos** a `chunking.py` porque:

- ❌ Pueden romper texto legítimo con espacios correctos
- ❌ No todos los PDFs tienen OCR corrupto
- ❌ Los regex son heurísticos, no 100% precisos
- ❌ Mejor dejar el texto original intacto

## 📊 Cómo detectar si tu PDF tiene OCR corrupto

Ejecuta en Supabase:

```sql
-- Ver primeros 3 chunks del material
SELECT 
    chunk_index,
    LEFT(chunk_text, 200) AS preview
FROM material_embeddings
WHERE material_id = 'TU_MATERIAL_ID'
ORDER BY chunk_index
LIMIT 3;
```

Busca patrones como:
- ❌ `"habi tación"`, `"entr ada"`, `"r encor"`
- ❌ Palabras con espacios en medio
- ❌ Letras sueltas seguidas de palabras: `"y o"`, `"l a"`, `"e l"`

## 🎯 Recomendaciones

### Para PDFs digitales (sin escaneo):
- ✅ NO deberían tener OCR corrupto
- ✅ PyPDF2 extrae texto perfecto
- ✅ NO necesitas limpiar nada

### Para PDFs escaneados:
- ⚠️ Verifica la calidad del OCR
- ⚠️ Usa Adobe Acrobat DC o Tesseract 5.x para mejor precisión
- ⚠️ Ejecuta `fix_ocr_chunks_CORRECTO.sql` si es necesario

## 📚 Referencias

- **Archivo de prueba:** `backend/test_ocr_fix.py`
- **Script SQL de limpieza:** `database/fix_ocr_chunks_CORRECTO.sql`
- **Función de limpieza:** `backend/chunking.py` → `clean_text()`
- **Análisis de entidades:** `backend/content_analyzer.py`

---

**Última actualización:** 11 de noviembre de 2025  
**Autor:** Abel Jesús Moya Acosta
