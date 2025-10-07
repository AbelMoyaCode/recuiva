# 🚀 Guía Rápida: Activar Backend de Recuiva

## ⚡ Inicio Rápido (5 minutos)

### 1. Navegar al backend
```powershell
cd C:\Users\Abel\Desktop\recuiva\backend
```

### 2. Crear entorno virtual
```powershell
python -m venv venv
```

### 3. Activar entorno virtual
```powershell
.\venv\Scripts\activate
```

**Nota:** Si hay error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar dependencias
```powershell
pip install -r requirements.txt
```

**⏱️ Esto tomará unos 3-5 minutos** (descarga ~300MB de paquetes)

### 5. Iniciar servidor
```powershell
python main.py
```

**✅ Si ves esto, está funcionando:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

---

## 🧪 Probar que Funciona

### Opción 1: Navegador (Más fácil)

1. Abre tu navegador
2. Ve a: **http://localhost:8000/docs**
3. Verás la documentación interactiva de FastAPI
4. Prueba el endpoint `GET /` haciendo clic en "Try it out"

### Opción 2: PowerShell

```powershell
Invoke-RestMethod -Uri "http://localhost:8000" -Method Get
```

Deberías ver:
```json
{
  "message": "Recuiva Backend API",
  "version": "2.0.0",
  "status": "running"
}
```

---

## 📤 Subir tu Primer Material

### Preparar un PDF de prueba

Necesitas un PDF de **mínimo 80 páginas** (o ~200,000 caracteres).

**Opciones:**
- Usa un libro académico digital
- Combina varios PDFs con herramientas online
- Descarga material educativo libre

### Subir vía interfaz web

1. Abre: **http://localhost:5500/src/pages/subir-material.html** (con Live Server)
2. Arrastra tu PDF a la zona de upload
3. Espera el procesamiento (puede tardar 1-3 minutos)
4. ✅ Verás confirmación con número de chunks generados

### Subir vía API directamente

```powershell
$headers = @{
    "Content-Type" = "multipart/form-data"
}
$body = @{
    file = Get-Item "C:\ruta\a\tu\archivo.pdf"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/materials/upload" -Method Post -Form $body
```

---

## 🔍 Verificar que se Crearon los Embeddings

Después de subir un material, deberías ver:

```
recuiva/
└── data/
    └── embeddings/
        └── material_1.json  ← ¡AQUÍ ESTÁ!
```

Abre ese archivo JSON y verás:
```json
{
  "material_id": 1,
  "filename": "matematicas_discretas.pdf",
  "total_chunks": 156,
  "chunks": [
    {
      "chunk_id": 1,
      "text": "...",
      "embedding": [0.123, -0.456, ...]  ← Vector de 384 dimensiones
    }
  ]
}
```

---

## ❓ Crear y Validar Preguntas

### 1. Crear pregunta
```powershell
$body = @{
    id = 1
    text = "¿Qué es un grafo dirigido?"
    topic = "Teoría de Grafos"
    difficulty = "medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/questions" -Method Post -Body $body -ContentType "application/json"
```

### 2. Validar respuesta de estudiante
```powershell
$body = @{
    question_id = 1
    user_answer = "Un grafo dirigido es una estructura matemática que consiste en vértices conectados por aristas que tienen dirección, permitiendo representar relaciones asimétricas."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/validate-answer" -Method Post -Body $body -ContentType "application/json"
```

**Respuesta esperada:**
```json
{
  "score": 92.5,
  "is_correct": true,
  "feedback": "¡Excelente! Tu respuesta demuestra una comprensión profunda del concepto de grafo dirigido.",
  "similarity": 0.9254
}
```

---

## 📊 Ver Estadísticas

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/stats" -Method Get
```

Verás:
```json
{
  "total_materials": 1,
  "total_questions": 1,
  "total_chunks": 156,
  "embeddings_model": "all-MiniLM-L6-v2"
}
```

---

## 🎯 Checklist para el Profesor

Usa esto para demostrar que cumples los requisitos:

- [ ] **✅ Backend API REST funcional** → Mostrar http://localhost:8000/docs
- [ ] **✅ Procesamiento de 80+ páginas** → Mostrar archivo PDF subido y chunks generados
- [ ] **✅ Chunking implementado** → Mostrar material_1.json con chunks
- [ ] **✅ Embeddings vectoriales** → Mostrar array de 384 dimensiones en JSON
- [ ] **✅ Base de datos vectorial** → Mostrar carpeta data/embeddings/
- [ ] **✅ Validación semántica con IA** → Probar endpoint /api/validate-answer
- [ ] **✅ Similarity score** → Mostrar respuesta con similarity y feedback

---

## 🐛 Solución de Problemas

### Error: "No module named 'fastapi'"
```powershell
# Asegúrate de tener el entorno activado
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Address already in use"
```powershell
# El puerto 8000 está ocupado, usa otro
uvicorn main:app --port 8001
```

### El modelo tarda mucho en cargar
**Es normal la primera vez** (descarga ~90MB). Espera 2-3 minutos.

### PDF rechazado por tamaño
Verifica que tenga **mínimo 200,000 caracteres** (~80 páginas).

```powershell
# Ver tamaño de archivo
(Get-Item "archivo.pdf").Length / 1KB  # Debería ser > 500KB aprox
```

---

## 🎓 Para Presentar al Profesor

### 1. Preparación (5 min)
- Backend corriendo en http://localhost:8000
- PDF de 80+ páginas listo
- Navegador con http://localhost:8000/docs abierto

### 2. Demo en vivo (10 min)
1. **Mostrar API docs** → "Aquí están todos los endpoints REST"
2. **Subir material** → "Procesando 80+ páginas con chunking"
3. **Mostrar embeddings** → "Aquí está la base de datos vectorial en JSON"
4. **Crear pregunta** → "Vinculada al material subido"
5. **Validar respuesta** → "Validación semántica con IA usando similarity"
6. **Mostrar score** → "Feedback generado automáticamente"

### 3. Evidencia técnica
- **Código fuente:** `backend/main.py`, `embeddings_module.py`, `chunking.py`
- **Archivos JSON:** `data/embeddings/material_*.json`
- **Logs:** Terminal mostrando procesamiento
- **Swagger UI:** Documentación automática de FastAPI

---

## 📁 Estructura de Archivos Importante

```
recuiva/
├── backend/
│   ├── main.py              ← ⭐ API principal
│   ├── embeddings_module.py ← ⭐ Generación de embeddings
│   ├── chunking.py          ← ⭐ Procesamiento de textos
│   ├── requirements.txt
│   ├── .env                 ← Configuración
│   └── README.md
├── data/
│   ├── embeddings/          ← ⭐ Base de datos vectorial
│   │   └── material_*.json
│   └── materials/           ← Archivos subidos (opcional)
├── assets/
│   └── js/
│       ├── api.js           ← ⭐ Cliente API
│       ├── upload-material.js
│       └── validate-answer.js
└── src/
    └── pages/
        ├── subir-material.html
        └── sesion-practica.html
```

---

## 🚀 Próximos Pasos

1. **Documenta en el Project Charter:**
   - "Sistema implementado con FastAPI REST API"
   - "Procesamiento de documentos extensos (80+ páginas)"
   - "Base de datos vectorial con embeddings semánticos"
   - "Validación automática usando Sentence Transformers"

2. **Actualiza el Product Backlog:**
   - ✅ HU-010: Embeddings implementados
   - ✅ HU-XXX: Chunking implementado
   - ✅ HU-XXX: Validación semántica implementada

3. **Prepara evidencias:**
   - Capturas de Swagger UI
   - Ejemplo de archivo embeddings JSON
   - Logs de procesamiento
   - Ejemplo de validación con score

---

**¿Necesitas ayuda?** Revisa `backend/README.md` para documentación completa.

**Autor:** Abel Jesús Moya Acosta  
**Fecha:** 7 de octubre de 2025  
**Versión Backend:** 2.0.0
