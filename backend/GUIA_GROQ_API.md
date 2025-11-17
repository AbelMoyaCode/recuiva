# 🚀 Guía Completa: Groq API para Recuiva

## 📋 ¿Qué es Groq?

**Groq** es la plataforma de IA MÁS RÁPIDA del mundo que ofrece:
- ✅ **100% GRATIS** (sin costos, sin tarjeta)
- ✅ **Ultra rápido**: 850+ tokens/segundo
- ✅ Modelos de código abierto (Llama 3.1 70B, Mixtral, Gemma)
- ✅ Compatible con OpenAI SDK
- ✅ Sin límites de crédito

**Ventajas sobre otras opciones:**
- ✅ **$0.00 USD** (vs Hugging Face que deprecó API gratis)
- ✅ 850 tokens/seg (vs 20-50 tokens/seg en otras plataformas)
- ✅ Sin tarjeta de crédito requerida
- ✅ Ideal para estudiantes y proyectos

---

## 🎯 PASO 1: Crear Cuenta en Groq

### 1.1 Ir al sitio web

```
https://console.groq.com
```

### 1.2 Registrarse

1. Click en **"Sign Up"** o **"Get Started"**
2. Opciones de registro:
   - ✅ **Google Account** (recomendado - 1 click)
   - ✅ GitHub Account
   - ✅ Email + contraseña

### 1.3 Acceso instantáneo

- ✅ **No requiere verificación de email**
- ✅ **No requiere tarjeta de crédito**
- ✅ Acceso inmediato a la consola

---

## 🔑 PASO 2: Obtener API Key

### 2.1 Ir a API Keys

Desde tu dashboard:

1. Click en **"API Keys"** en el menú lateral izquierdo
2. O ve directamente a:
   ```
   https://console.groq.com/keys
   ```

### 2.2 Crear nueva API Key

1. Click en **"+ Create API Key"**
2. (Opcional) Dale un nombre:
   ```
   Recuiva - Generación de Preguntas
   ```
3. Click en **"Submit"** o **"Create"**

### 2.3 Copiar el API Key

⚠️ **MUY IMPORTANTE:**
- El API Key se muestra **UNA SOLA VEZ**
- Cópiala inmediatamente
- Guárdala en lugar seguro

El API Key tiene este formato:
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 💰 PASO 3: Costos (¡GRATIS PARA SIEMPRE!)

### 3.1 ¿Cuánto cuesta Groq?

**RESPUESTA: $0.00 USD** 🎉🎉🎉

- ✅ **Sin tarjeta de crédito** (nunca)
- ✅ **Sin límites de billing**
- ✅ **Sin suscripciones**
- ✅ **Gratis para siempre**

### 3.2 Rate Limits (Límites de velocidad)

**Tier Gratuito:**
- ✅ **30 requests/minuto** (perfecto para 153 chunks)
- ✅ **14,400 tokens/minuto**
- ✅ **14,400 requests/día**

**Para Recuiva (153 chunks):**
- Tiempo estimado: ~5 minutos
- Costo: **$0.00**
- Velocidad: ⚡ Ultra rápido

### 3.3 Comparación con otras plataformas

| Servicio | Costo | Velocidad | Calidad | Requiere Tarjeta |
|----------|-------|-----------|---------|------------------|
| **Groq** | **$0.00** | **850 tok/s** | ⭐⭐⭐⭐⭐ | ❌ No |
| Hugging Face | ❌ Deprecado | - | - | - |
| OpenAI GPT-4 | $0.50+ | 50 tok/s | ⭐⭐⭐⭐⭐ | ✅ Sí |
| DeepSeek | $0.05 | 100 tok/s | ⭐⭐⭐⭐ | ✅ Sí |
| Together.AI | $5 gratis | 200 tok/s | ⭐⭐⭐⭐ | ✅ Sí |

---

## ⚙️ PASO 4: Configurar Recuiva con Groq

### 4.1 Agregar API Key en `.env`

1. Abre el archivo **`backend/.env`**

2. Agrega esta línea:

```bash
# Groq API Configuration (GRATIS 100%)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

3. **Reemplaza** `gsk_xxx...` con tu API Key real de Groq

### 4.2 Verificar dependencia

Groq ya está instalado. Verifica ejecutando:

```bash
pip list | findstr groq
```

**Salida esperada:**
```
groq    0.34.1
```

Si no está, instala:
```bash
pip install groq
```

---

## ✅ PASO 5: Probar la Conexión

### 5.1 Probar desde Python

Ejecuta en `backend/`:

```bash
python question_generator_ai.py
```

**Salida esperada:**

```
🔍 Probando conexión con Groq API...
✅ Conexión exitosa con Groq
   Modelo: llama-3.1-70b-versatile
   Respuesta: OK

======================================================================
  TEST: Generación de pregunta de ejemplo
======================================================================

✅ Preguntas generadas:

   1. Explica cómo el personaje de Arsène Lupin representa el arquetipo 
      del "ladrón de guante blanco" en la literatura francesa.

   2. Analiza la relación entre el collar histórico de María Antonieta 
      y el argumento principal de la novela.
```

### 5.2 Probar desde la API (FastAPI)

1. Inicia el servidor:

```bash
python main.py
```

2. Ve a la documentación:

```
http://localhost:8000/docs
```

3. Prueba el endpoint:

```
GET /api/test-groq
```

**Respuesta esperada:**

```json
{
  "success": true,
  "message": "Conexión exitosa",
  "response": "OK"
}
```

---

## 🎓 PASO 6: Generar Preguntas para tu Material

### 6.1 Desde la API

Endpoint:

```
POST /api/materials/{material_id}/generate-questions-ai
```

**Body (JSON):**

```json
{
  "num_questions_per_chunk": 2,
  "max_chunks": null,
  "save_to_db": true
}
```

**Parámetros:**

- `num_questions_per_chunk`: 1-3 (recomendado: 2)
- `max_chunks`: Limitar chunks (null = todos)
- `save_to_db`: Guardar en Supabase automáticamente

### 6.2 Ejemplo de respuesta

```json
{
  "success": true,
  "material_id": "0394a7f6-cb99-4886-a8e9-0ea05c5d7c56",
  "questions": [
    {
      "question": "Explica la importancia del collar en el contexto histórico...",
      "chunk_id": "881b25af-9484-4f6b-9ea6-0a2f2cc955e5",
      "chunk_index": 11,
      "material_id": "0394a7f6-cb99-4886-a8e9-0ea05c5d7c56",
      "source_preview": "ededordesugrácilcuello..."
    }
  ],
  "total_questions": 306,
  "chunks_processed": 153,
  "chunks_failed": 0,
  "cost_estimate": 0.0,
  "saved_to_db": true,
  "saved_count": 306
}
```

---

## 📊 PASO 7: Modelos Disponibles en Groq

### Modelo usado en Recuiva: **Llama 3.1 70B Versatile**

**Especificaciones:**
- 🧠 70 mil millones de parámetros
- 🌍 Multilingüe (excelente en español)
- ⚡ 850+ tokens/segundo
- 📝 Contexto: 128K tokens

### Modelos alternativos (si necesitas cambiar)

Edita en `question_generator_ai.py`:

```python
# Modelo actual (recomendado)
GROQ_MODEL = "llama-3.1-70b-versatile"

# Alternativas disponibles:
# GROQ_MODEL = "llama-3.1-8b-instant"      # Más rápido, menor calidad
# GROQ_MODEL = "mixtral-8x7b-32768"        # Alternativa europea
# GROQ_MODEL = "gemma2-9b-it"              # Google Gemma
```

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Problema 1: "API key not found"

**Causa:** Variable de entorno no cargada

**Solución:**
1. Verifica que `.env` existe en `backend/`
2. Verifica la línea: `GROQ_API_KEY=gsk_xxx...`
3. Reinicia el servidor

### Problema 2: "Rate limit exceeded"

**Causa:** Superaste 30 requests/minuto

**Solución:**
- El código ya tiene delay de 1 segundo entre chunks
- Si falla, espera 1 minuto y reintenta
- Para 153 chunks tardarás ~5 minutos (dentro del límite)

### Problema 3: "Invalid API key"

**Causa:** API Key incorrecta o expirada

**Solución:**
1. Verifica que copiaste el key completo (empieza con `gsk_`)
2. Ve a https://console.groq.com/keys
3. Genera una nueva API Key
4. Actualiza `.env`

### Problema 4: "Model not found"

**Causa:** Nombre de modelo incorrecto

**Solución:**
- Verifica que `GROQ_MODEL = "llama-3.1-70b-versatile"`
- Lista de modelos: https://console.groq.com/docs/models

---

## 🎯 MEJORES PRÁCTICAS

### 1. Empieza con pocos chunks (testing)

```json
{
  "num_questions_per_chunk": 2,
  "max_chunks": 10,
  "save_to_db": false
}
```

### 2. Ajusta cantidad de preguntas

- **1 pregunta/chunk**: Rápido (~2 min)
- **2 preguntas/chunk**: ✅ **Recomendado** (~5 min)
- **3 preguntas/chunk**: Completo (~8 min)

### 3. Genera con anticipación

- No esperes al día de la presentación
- Genera las 306 preguntas 1-2 días antes
- Guárdalas en Supabase
- Ten backup en JSON

### 4. Monitorea uso

Ve a: https://console.groq.com/settings/limits

Verás:
- Requests usados hoy
- Tokens consumidos
- Rate limits actuales

---

## 📝 RESUMEN RÁPIDO

```bash
# 1. Crear cuenta
https://console.groq.com

# 2. Obtener API Key
https://console.groq.com/keys

# 3. NO necesitas agregar crédito (¡GRATIS!)

# 4. Configurar en .env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx

# 5. Verificar instalación
pip list | findstr groq

# 6. Probar conexión
python question_generator_ai.py

# 7. Iniciar servidor
python main.py

# 8. Generar preguntas
POST /api/materials/{material_id}/generate-questions-ai
```

---

## 🆘 SOPORTE

Si tienes problemas:

1. **Groq Discord**: https://discord.gg/groq
2. **Documentación oficial**: https://console.groq.com/docs
3. **Community**: https://community.groq.com/

---

## 🎓 EJEMPLO COMPLETO DE USO

### Desde Terminal (cURL)

```bash
# Terminal 1: Backend
cd backend
python main.py

# Terminal 2: Generar preguntas
curl -X POST http://localhost:8000/api/materials/0394a7f6-cb99-4886-a8e9-0ea05c5d7c56/generate-questions-ai \
  -H "Content-Type: application/json" \
  -d '{
    "num_questions_per_chunk": 2,
    "max_chunks": 5,
    "save_to_db": false
  }'
```

### Desde FastAPI Docs (UI)

1. Ve a: http://localhost:8000/docs
2. Busca: `POST /api/materials/{material_id}/generate-questions-ai`
3. Click **"Try it out"**
4. Material ID: `0394a7f6-cb99-4886-a8e9-0ea05c5d7c56`
5. Body:
   ```json
   {
     "num_questions_per_chunk": 2,
     "max_chunks": 5,
     "save_to_db": false
   }
   ```
6. Click **"Execute"**

---

## ⚡ VENTAJAS DE GROQ vs HUGGING FACE

| Característica | Groq | Hugging Face (deprecado) |
|----------------|------|--------------------------|
| **Costo** | $0.00 | ❌ Requiere suscripción |
| **Velocidad** | 850 tok/s | 20-50 tok/s |
| **API Status** | ✅ Activa | ❌ Deprecada (410) |
| **Rate Limits** | 30/min | - |
| **Calidad** | Llama 3.1 70B | Mistral 7B |
| **Tarjeta** | ❌ No | ❌ No (pero no funciona) |

---

## ✅ ¡LISTO!

Ahora tienes Groq configurado en Recuiva:

- ✅ **$0.00 USD** (gratis para siempre)
- ✅ **Ultra rápido** (850 tokens/seg)
- ✅ **Sin tarjeta** de crédito
- ✅ **Llama 3.1 70B** (mejor que Mistral-7B)

**Próximos pasos:**
1. ✅ Crea tu API Key en https://console.groq.com/keys
2. ✅ Agrégala al archivo `.env`
3. ✅ Prueba con `python question_generator_ai.py`
4. ✅ Genera las 306 preguntas para "El Collar de la Reina"
5. ✅ Presenta tu proyecto el jueves con IA de última generación

**¡Éxito en tu presentación! 🎓⚡✨**

---

**Autor:** Abel Jesús Moya Acosta  
**Fecha:** 17 de noviembre de 2025  
**Proyecto:** Recuiva - Active Recall con RAG  
**Modelo IA:** Groq Llama 3.1 70B Versatile
