# 🚀 Guía de Implementación: Supabase para Recuiva

## 📖 Introducción

Esta guía te llevará paso a paso para convertir Recuiva de un sistema con localStorage a una aplicación multi-usuario con base de datos real usando **Supabase**.

**Tiempo estimado:** 2-3 horas  
**Nivel de dificultad:** ⭐⭐⭐ (Intermedio)  
**Costo:** $0 (100% Gratis)

---

## 📚 Recursos de Aprendizaje

### Videos Tutoriales (VER PRIMERO)

1. **Supabase desde CERO - Tutorial Completo** (midudev)
   - 🔗 https://www.youtube.com/watch?v=dU7GwCOgvNY
   - ⏱️ 32 minutos
   - 📝 Cubre: Setup, Auth, CRUD, RLS

2. **Supabase Authentication Tutorial** (Net Ninja)
   - 🔗 https://www.youtube.com/watch?v=oXWImFqsQF4
   - ⏱️ 15 minutos
   - 📝 Cubre: Login, Register, Session Management

### Documentación Oficial

1. **Quickstart Guide (JavaScript)**
   - 🔗 https://supabase.com/docs/guides/getting-started/quickstarts/javascript
   
2. **Authentication Documentation**
   - 🔗 https://supabase.com/docs/guides/auth

3. **Database Documentation**
   - 🔗 https://supabase.com/docs/guides/database

---

## 🎯 PASO 1: Crear Cuenta y Proyecto en Supabase

### 1.1 Registro

1. Ve a https://supabase.com
2. Click en **"Start your project"**
3. Registrarte con GitHub (recomendado) o email
4. Confirma tu email

### 1.2 Crear Nuevo Proyecto

1. Click en **"New project"**
2. Llena los datos:
   - **Name:** `recuiva-db`
   - **Database Password:** Genera una segura (GUÁRDALA EN UN LUGAR SEGURO)
   - **Region:** South America (São Paulo) - Lo más cercano a ti
   - **Pricing Plan:** Free (0$/month)
3. Click en **"Create new project"**
4. Espera 2-3 minutos mientras se crea la base de datos

### 1.3 Obtener Credenciales

1. En el dashboard del proyecto, ve a **Settings** (⚙️) > **API**
2. Copia y guarda estos valores:

```
Project URL: https://xxxxxxxxxxxxx.supabase.co
anon/public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**⚠️ IMPORTANTE:** Guarda estas credenciales en un lugar seguro. Las necesitarás después.

---

## 🗄️ PASO 2: Crear el Esquema de Base de Datos

### 2.1 Abrir SQL Editor

1. En el dashboard de Supabase, ve a **SQL Editor** (icono de </> en el menú lateral)
2. Click en **"New query"**

### 2.2 Ejecutar el Script

1. Abre el archivo `database/supabase_schema.sql` que creé para ti
2. Copia TODO el contenido
3. Pégalo en el SQL Editor de Supabase
4. Click en **"Run"** (o presiona Ctrl+Enter)
5. Deberías ver: ✅ "Success. No rows returned"

### 2.3 Verificar las Tablas

1. Ve a **Table Editor** en el menú lateral
2. Deberías ver estas tablas:
   - ✅ `materials`
   - ✅ `questions`
   - ✅ `answers`
   - ✅ `user_profiles`

### 2.4 Verificar Row Level Security (RLS)

1. Ve a **Authentication** > **Policies**
2. Deberías ver políticas para cada tabla:
   - `Users can view own materials`
   - `Users can insert own materials`
   - etc.

---

## 💻 PASO 3: Configurar Frontend

### 3.1 Crear Archivo de Configuración

Crea `public/assets/js/supabase-config.js`:

```javascript
/**
 * Configuración de Supabase
 * IMPORTANTE: Reemplaza estas credenciales con las tuyas
 */

// 🔑 Credenciales de Supabase (obtenidas en Paso 1.3)
const SUPABASE_URL = 'https://xxxxxxxxxxxxx.supabase.co'; // ⚠️ REEMPLAZAR
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'; // ⚠️ REEMPLAZAR

// Inicializar cliente de Supabase
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Exportar para uso global
window.supabaseClient = supabase;

console.log('✅ Supabase configurado correctamente');
```

### 3.2 Modificar crear-cuenta.html

Agregar antes de `</head>`:

```html
<!-- Supabase JS -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="../../assets/js/supabase-config.js"></script>
```

Reemplazar el JavaScript del formulario:

```javascript
// Registro con Supabase
async function handleRegister(event) {
    event.preventDefault();
    
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // Validaciones
    if (password.length < 8) {
        alert('La contraseña debe tener al menos 8 caracteres');
        return;
    }
    
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden');
        return;
    }
    
    try {
        // Registrar usuario en Supabase
        const { data, error } = await supabaseClient.auth.signUp({
            email: email,
            password: password,
            options: {
                data: {
                    full_name: fullName
                }
            }
        });
        
        if (error) throw error;
        
        // Crear perfil de usuario
        const { error: profileError } = await supabaseClient
            .from('user_profiles')
            .insert([
                { 
                    id: data.user.id,
                    full_name: fullName 
                }
            ]);
        
        if (profileError) console.warn('Error creando perfil:', profileError);
        
        alert('✅ Cuenta creada exitosamente! Revisa tu email para confirmar.');
        window.location.href = 'iniciar-sesion.html';
        
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error al crear cuenta: ' + error.message);
    }
}

// Asociar función al formulario
document.querySelector('form').addEventListener('submit', handleRegister);
```

### 3.3 Modificar iniciar-sesion.html

Agregar antes de `</head>`:

```html
<!-- Supabase JS -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="../../assets/js/supabase-config.js"></script>
```

Reemplazar el JavaScript del formulario:

```javascript
// Login con Supabase
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    try {
        const { data, error } = await supabaseClient.auth.signInWithPassword({
            email: email,
            password: password
        });
        
        if (error) throw error;
        
        console.log('✅ Login exitoso:', data);
        window.location.href = '../dashboard.html';
        
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Credenciales incorrectas: ' + error.message);
    }
}

// Asociar función al formulario
document.querySelector('form').addEventListener('submit', handleLogin);
```

### 3.4 Crear Middleware de Autenticación

Crea `public/assets/js/auth-middleware.js`:

```javascript
/**
 * Middleware de autenticación
 * Verifica que el usuario esté logueado antes de acceder a páginas protegidas
 */

async function checkAuth() {
    const { data: { session }, error } = await supabaseClient.auth.getSession();
    
    if (error || !session) {
        console.warn('⚠️ Usuario no autenticado, redirigiendo...');
        window.location.href = '/public/app/auth/iniciar-sesion.html';
        return null;
    }
    
    console.log('✅ Usuario autenticado:', session.user.email);
    return session.user;
}

// Función para obtener el user_id actual
async function getCurrentUserId() {
    const { data: { user } } = await supabaseClient.auth.getUser();
    return user?.id || null;
}

// Función para logout
async function logout() {
    const { error } = await supabaseClient.auth.signOut();
    if (error) {
        console.error('Error en logout:', error);
    } else {
        window.location.href = '/public/app/auth/iniciar-sesion.html';
    }
}

// Verificar autenticación al cargar cualquier página protegida
if (window.location.pathname.includes('/app/') && 
    !window.location.pathname.includes('/auth/')) {
    checkAuth();
}
```

### 3.5 Agregar Middleware a Páginas Protegidas

En `dashboard.html`, `subir-material.html`, `crear-pregunta.html`, `validar-respuesta.html`:

Agregar antes de `</head>`:

```html
<!-- Auth Middleware -->
<script src="../assets/js/supabase-config.js"></script>
<script src="../assets/js/auth-middleware.js"></script>
```

---

## 🔧 PASO 4: Modificar Backend

### 4.1 Instalar Dependencias

```bash
cd backend
pip install supabase python-dotenv
```

### 4.2 Crear Archivo .env

Crea `backend/.env`:

```env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**⚠️ IMPORTANTE:** 
- El `SERVICE_KEY` es DIFERENTE al `anon key`
- Lo encuentras en: Settings > API > `service_role` key
- **NUNCA** compartas esta clave ni la subas a GitHub

### 4.3 Modificar backend/main.py

Agregar imports:

```python
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Inicializar Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)
```

### 4.4 Modificar Endpoint de Upload

Antes:
```python
@app.post("/upload-material")
async def upload_material(file: UploadFile = File(...), title: str = Form(...)):
    # ... código actual
    return {"message": "Material subido", "material_id": material_id}
```

Después:
```python
@app.post("/upload-material")
async def upload_material(
    file: UploadFile = File(...), 
    title: str = Form(...),
    user_id: str = Header(..., alias="X-User-Id")  # ⬅️ NUEVO
):
    # Crear carpeta específica del usuario
    user_upload_dir = os.path.join(UPLOAD_DIR, user_id)
    os.makedirs(user_upload_dir, exist_ok=True)
    
    # Guardar archivo
    file_path = os.path.join(user_upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    # Generar embeddings
    embeddings = generate_embeddings(chunks)
    
    # Guardar en Supabase
    data = supabase.table('materials').insert({
        'user_id': user_id,
        'title': title,
        'file_name': file.filename,
        'file_path': file_path,
        'file_type': file.filename.split('.')[-1]
    }).execute()
    
    material_id = data.data[0]['id']
    
    # Guardar embeddings en archivo
    embeddings_file = os.path.join(user_upload_dir, f"{material_id}_embeddings.json")
    # ... resto del código
    
    return {"message": "Material subido", "material_id": material_id}
```

### 4.5 Modificar Endpoint de Validación

```python
@app.post("/validate-answer")
async def validate_answer(
    request: ValidationRequest,
    user_id: str = Header(..., alias="X-User-Id")  # ⬅️ NUEVO
):
    # Validar que el material pertenece al usuario
    material = supabase.table('materials')\
        .select('*')\
        .eq('id', request.material_id)\
        .eq('user_id', user_id)\
        .single()\
        .execute()
    
    if not material.data:
        raise HTTPException(status_code=403, detail="Material no encontrado")
    
    # ... resto de la validación
    
    # Guardar respuesta en Supabase
    supabase.table('answers').insert({
        'user_id': user_id,
        'question_id': request.question_id,
        'answer_text': request.user_answer,
        'score': final_score,
        'classification': classification,
        'feedback': feedback,
        'top_chunks': top_chunks
    }).execute()
    
    return {
        "score": final_score,
        "classification": classification,
        # ...
    }
```

---

## 🔄 PASO 5: Actualizar Frontend API

### 5.1 Modificar public/assets/js/api.js

Agregar helper para obtener user_id:

```javascript
/**
 * Obtiene el user_id del usuario autenticado
 * @returns {Promise<string|null>}
 */
async function getUserId() {
    const { data: { user } } = await supabaseClient.auth.getUser();
    return user?.id || null;
}

/**
 * Sube un material
 */
async function uploadMaterial(file, title) {
    const userId = await getUserId();
    if (!userId) throw new Error('Usuario no autenticado');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    
    const response = await fetch(`${API_BASE_URL}/upload-material`, {
        method: 'POST',
        headers: {
            'X-User-Id': userId  // ⬅️ NUEVO
        },
        body: formData
    });
    
    return await response.json();
}

/**
 * Obtiene materiales del usuario
 */
async function getMaterials() {
    const userId = await getUserId();
    if (!userId) throw new Error('Usuario no autenticado');
    
    const { data, error } = await supabaseClient
        .from('materials')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false });
    
    if (error) throw error;
    return data;
}

/**
 * Valida una respuesta
 */
async function validateAnswer(materialId, questionId, questionText, userAnswer) {
    const userId = await getUserId();
    if (!userId) throw new Error('Usuario no autenticado');
    
    const response = await fetch(`${API_BASE_URL}/validate-answer`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-User-Id': userId  // ⬅️ NUEVO
        },
        body: JSON.stringify({
            material_id: materialId,
            question_id: questionId,
            question_text: questionText,
            user_answer: userAnswer
        })
    });
    
    return await response.json();
}
```

---

## ✅ PASO 6: Testing

### 6.1 Crear Cuenta de Prueba

1. Inicia el backend: `python backend/main.py`
2. Abre `public/app/auth/crear-cuenta.html`
3. Crea una cuenta con:
   - Nombre: Test User
   - Email: test@example.com
   - Contraseña: Test1234
4. Revisa tu email y confirma la cuenta

### 6.2 Probar Login

1. Ve a `iniciar-sesion.html`
2. Ingresa las credenciales
3. Deberías ser redirigido a `dashboard.html`

### 6.3 Probar Flujo Completo

1. **Subir Material:**
   - Ve a "Subir Material"
   - Sube un PDF
   - Verifica en Supabase (Table Editor > materials) que aparezca

2. **Crear Pregunta:**
   - Crea una pregunta sobre el material
   - Verifica en Supabase (Table Editor > questions)

3. **Validar Respuesta:**
   - Responde la pregunta
   - Verifica en Supabase (Table Editor > answers)
   - Verifica que el score y feedback se guarden

### 6.4 Probar Multi-Usuario

1. Cierra sesión
2. Crea otra cuenta: test2@example.com
3. Sube un material diferente
4. Verifica que SOLO veas tus propios materiales
5. Cierra sesión y vuelve a entrar con test@example.com
6. Verifica que SOLO veas los materiales del primer usuario

---

## 🚀 PASO 7: Deploy a Producción

### 7.1 Actualizar docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
    volumes:
      - ./data:/app/data
```

### 7.2 Configurar Variables en Dokploy

1. Ve a Dokploy Dashboard
2. Selecciona tu proyecto "recuiva"
3. Settings > Environment Variables
4. Agrega:
   - `SUPABASE_URL`: https://xxxxxxxxxxxxx.supabase.co
   - `SUPABASE_SERVICE_KEY`: eyJhbGc...

### 7.3 Actualizar supabase-config.js en Producción

```javascript
const SUPABASE_URL = 'https://xxxxxxxxxxxxx.supabase.co'; // PRODUCCIÓN
const SUPABASE_ANON_KEY = 'eyJhbGc...'; // PRODUCCIÓN
```

### 7.4 Deploy

```bash
git add .
git commit -m "feat: Integración con Supabase - Multi-usuario"
git push origin main
```

Dokploy detectará el cambio y hará deploy automáticamente.

---

## 🔒 Seguridad

### Reglas Importantes

1. **NUNCA** subas el `.env` a GitHub:
   ```bash
   echo "backend/.env" >> .gitignore
   ```

2. **NUNCA** uses el `service_role` key en el frontend:
   - Frontend: usa `anon` key
   - Backend: usa `service_role` key

3. **SIEMPRE** verifica RLS (Row Level Security):
   - Cada usuario solo puede ver sus propios datos
   - Supabase lo maneja automáticamente

4. **Habilita Email Verification** en Supabase:
   - Authentication > Settings > Enable email confirmations

---

## 📊 Monitoreo

### Dashboard de Supabase

1. **Database > Logs:** Ver queries ejecutadas
2. **Auth > Users:** Ver usuarios registrados
3. **Table Editor:** Ver datos en tiempo real
4. **API Docs:** Documentación auto-generada de tu API

### Queries Útiles

```sql
-- Ver usuarios con más materiales
SELECT 
    u.email,
    COUNT(m.id) as total_materials
FROM auth.users u
LEFT JOIN materials m ON u.id = m.user_id
GROUP BY u.email
ORDER BY total_materials DESC;

-- Ver promedio de scores por usuario
SELECT 
    u.email,
    AVG(a.score) as avg_score,
    COUNT(a.id) as total_answers
FROM auth.users u
LEFT JOIN answers a ON u.id = a.user_id
GROUP BY u.email;
```

---

## 🆘 Troubleshooting

### Error: "Invalid API key"
- ✅ Verifica que copiaste bien el `anon` key
- ✅ Verifica que el proyecto de Supabase esté activo

### Error: "Row Level Security violation"
- ✅ Ejecuta de nuevo el script SQL completo
- ✅ Verifica en Authentication > Policies que las políticas existan

### Error: "User not found"
- ✅ Verifica que el usuario haya confirmado su email
- ✅ Ve a Authentication > Users y verifica el estado

### Los materiales no se cargan
- ✅ Abre DevTools > Console y busca errores
- ✅ Verifica que `X-User-Id` se esté enviando en los headers
- ✅ Verifica en Supabase que los materiales tengan el `user_id` correcto

---

## 📚 Recursos Adicionales

### Comunidad

- 🌐 **Discord de Supabase:** https://discord.supabase.com
- 📖 **Supabase Blog:** https://supabase.com/blog
- 🎥 **Canal de YouTube:** https://www.youtube.com/@Supabase

### Cursos Gratuitos

- **Supabase Crash Course:** https://www.youtube.com/watch?v=7uKQBl9uZ00
- **Full Stack con Supabase:** https://egghead.io/courses/build-a-saas-product-with-next-js-supabase-and-stripe

---

## ✨ Mejoras Futuras

Una vez que tengas esto funcionando, puedes agregar:

1. **Recuperar Contraseña:** `supabase.auth.resetPasswordForEmail()`
2. **Google OAuth:** Login con Google
3. **Almacenamiento de Archivos:** Supabase Storage para PDFs
4. **Realtime:** Notificaciones en tiempo real
5. **Edge Functions:** Lógica serverless
6. **Analytics:** Gráficas de progreso del usuario

---

## 🎉 ¡Listo!

Si seguiste todos los pasos, ahora tienes:

✅ Base de datos PostgreSQL real  
✅ Autenticación segura con Supabase  
✅ Sistema multi-usuario  
✅ Row Level Security (RLS)  
✅ Backend actualizado  
✅ Frontend con auth real  
✅ Deploy en producción  

**¡Felicidades! 🎊** Ahora Recuiva es una aplicación profesional lista para presentar al profesor.

---

**¿Tienes dudas?** Revisa los tutoriales en video o pregúntame. ¡Éxito! 🚀
