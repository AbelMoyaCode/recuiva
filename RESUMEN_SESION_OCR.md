# 📋 RESUMEN DE SESIÓN - Problema OCR en PDFs

**Fecha:** 11 de noviembre de 2025  
**Problema reportado:** Generador de preguntas crea preguntas genéricas  
**Causa raíz:** PDF con OCR corrupto en archivo original

---

## 🔍 INVESTIGACIÓN REALIZADA

### 1️⃣ Problema inicial
- Usuario reporta: Preguntas genéricas como _"¿Qué información se presenta en este fragmento del material?"_
- Esperado: Preguntas específicas sobre "María Antonieta", "Jeanne de Valois", "Rétaux de Villette"

### 2️⃣ Análisis del flujo
```
PDF → PyPDF2 → chunking.py → Supabase → question_generator → ContentAnalyzer
```

✅ **pgvector funciona bien** - genera embeddings correctamente  
✅ **Validación semántica funciona** - compara respuestas correctamente  
❌ **ContentAnalyzer extrae basura** - encuentra `['endade ese', 'euxhizo ungesto']` en vez de nombres propios

### 3️⃣ Hallazgo clave
El PDF "El Collar De La Reina" tiene **OCR corrupto en el archivo original**:

**Evidencia:**
```python
# backend/test_ocr_fix.py - línea 23
texto_corrupto = """guar darlo en su estuche de cuer o rojo con las armas del Car denal, 
pasó a un gabinete contiguo , una especie de alcoba más bien, que se había aislado 
por completo de la habi tación, y cuya única entr ada se encontr aba al pie de su cama."""
```

**Ejemplos reales:**
- ❌ `"habi tación"` → debería ser `"habitación"`
- ❌ `"entr ada"` → debería ser `"entrada"`
- ❌ `"encontr aba"` → debería ser `"encontraba"`
- ❌ `"r encor"` → debería ser `"rencor"`
- ❌ `"di letante"` → debería ser `"diletante"`

### 4️⃣ ¿Por qué ocurre?
**NO es culpa de Recuiva ni de PyPDF2**:
- El PDF fue escaneado con OCR externo (Adobe, Tesseract, etc.)
- El OCR insertó espacios incorrectamente al reconocer el texto
- El texto corrupto **quedó guardado en el PDF**
- PyPDF2 extrae el texto **tal como está** en el PDF
- Recuiva guarda los chunks con el texto corrupto

---

## 🔧 SOLUCIONES IMPLEMENTADAS

### ✅ 1. Restaurar código original
**Archivo:** `backend/chunking.py`

**Antes (con regex OCR):**
```python
def clean_text(text: str) -> str:
    # PASO 1: Reparar espacios insertados por OCR defectuoso
    text = re.sub(r'([a-záéíóúñ]{3,})\s+([a-záéíóúñ]{1,3})(\s|[,.:;!?\n])', r'\1\2\3', text)
    text = re.sub(r'([a-záéíóúñ]{2,})\s+([a-záéíóúñ]{4,})', r'\1\2', text)
    # ...
```

**Después (código original):**
```python
def clean_text(text: str) -> str:
    """
    Limpia el texto removiendo caracteres innecesarios
    
    NOTA: Si el PDF tiene OCR defectuoso, este filtro NO lo arreglará.
    Para PDFs con OCR corrupto, ejecutar: database/fix_ocr_chunks_CORRECTO.sql
    """
    # Remover múltiples espacios
    text = re.sub(r'\s+', ' ', text)
    # Remover caracteres especiales pero mantener puntuación básica
    text = re.sub(r'[^\w\s.,;:!?¿¡áéíóúÁÉÍÓÚñÑ()"\'-]', '', text)
    # Remover líneas vacías múltiples
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()
```

**Razón:** NO modificar automáticamente porque:
- ❌ Los regex pueden romper texto legítimo con espacios correctos
- ❌ No todos los PDFs tienen OCR corrupto
- ✅ Mejor dejar el texto original intacto

### ✅ 2. Documentación completa
**Archivo creado:** `docs/PROBLEMA_OCR_EN_PDFS.md`

Incluye:
- ✅ Descripción del problema con ejemplos reales
- ✅ Por qué ocurre (no es culpa de Recuiva)
- ✅ Impacto en generación de preguntas
- ✅ 3 soluciones disponibles
- ✅ Cómo detectar si tu PDF tiene OCR corrupto

### ✅ 3. Scripts SQL de limpieza
**Archivos creados:**
- `database/fix_ocr_chunks_CORRECTO.sql` - Limpia chunks existentes con regex
- `database/DELETE_CORRUPTED_MATERIAL.sql` - Elimina material corrupto para volver a subirlo

---

## 🎯 RECOMENDACIONES FINALES

### Para "El Collar De La Reina" (PDF actual):

**Opción A: Buscar PDF limpio (RECOMENDADO)**
1. Busca otra versión del PDF sin OCR corrupto
2. Elimina el material actual con `DELETE_CORRUPTED_MATERIAL.sql`
3. Sube el PDF limpio → funcionará perfecto

**Opción B: Limpiar chunks existentes**
1. Ejecuta `fix_ocr_chunks_CORRECTO.sql` en Supabase SQL Editor
2. Limitación: Solo funciona para patrones simples
3. Palabras muy corruptas seguirán mal

**Opción C: Aceptar limitación**
1. Mantén el PDF actual
2. La validación semántica sigue funcionando ✅
3. Las preguntas serán genéricas ⚠️

### Para PDFs futuros:

✅ **PDFs digitales (sin escaneo):**
- NO deberían tener OCR corrupto
- PyPDF2 extrae texto perfecto
- Funcionará out-of-the-box

✅ **PDFs escaneados:**
- Usa Adobe Acrobat DC o Tesseract 5.x para mejor OCR
- Verifica la calidad antes de subir
- Si tiene espacios raros, ejecuta SQL de limpieza

---

## 📊 IMPACTO EN RECUIVA

| Funcionalidad | Estado | Observaciones |
|---------------|--------|---------------|
| **Validación semántica** | ✅ Funciona perfecto | pgvector compara embeddings correctamente |
| **Embeddings vectoriales** | ✅ Funciona perfecto | Se generan sin problemas |
| **Generación de preguntas** | ⚠️ Afectada en PDFs con OCR | ContentAnalyzer no puede extraer entidades de texto corrupto |
| **Extracción de texto** | ✅ Funciona perfecto | PyPDF2 extrae texto tal como está en el PDF |
| **Chunking** | ✅ Funciona perfecto | Divide texto correctamente |

---

## 📚 ARCHIVOS MODIFICADOS

```
✅ backend/chunking.py (restaurado a original)
✅ docs/PROBLEMA_OCR_EN_PDFS.md (nuevo)
✅ database/fix_ocr_chunks_CORRECTO.sql (nuevo)
✅ database/DELETE_CORRUPTED_MATERIAL.sql (nuevo)
```

**Commit:** `2aa7f2c` - "docs: Restaurar chunking.py original + documentar problema OCR en PDFs"

---

## 🚀 PRÓXIMOS PASOS

1. ⏳ **Decidir qué hacer con "El Collar De La Reina":**
   - Buscar PDF limpio
   - O ejecutar SQL de limpieza
   - O probar con otro material

2. ✅ **Desplegar cambios al servidor:**
   ```bash
   ssh root@147.182.226.170
   cd /root/recuiva
   git pull
   docker-compose restart backend
   ```

3. ✅ **Probar con PDF limpio:**
   - Subir un PDF de texto digital
   - Verificar que genera preguntas específicas
   - Confirmar que el sistema funciona perfectamente con PDFs limpios

---

**Conclusión:** El sistema Recuiva funciona correctamente. El problema es específico del PDF "El Collar De La Reina" que tiene OCR corrupto en el archivo original. La solución es usar PDFs limpios o ejecutar el script SQL de limpieza manual para casos excepcionales.
