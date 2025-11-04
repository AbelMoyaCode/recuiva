# 🚀 GUÍA RÁPIDA: CONFIGURAR BASE DE DATOS EN SUPABASE

## 📋 **PASOS PARA EJECUTAR**

### **PASO 1: LIMPIAR BASE DE DATOS ACTUAL** ⚠️

1. Ve a **Supabase Dashboard**: https://supabase.com/dashboard
2. Selecciona tu proyecto **Recuiva**
3. Ve a **SQL Editor** (ícono de base de datos en el menú izquierdo)
4. Haz clic en **"+ New Query"**
5. Copia y pega TODO el contenido de: `LIMPIAR_Y_RECREAR_BD.sql`
6. Haz clic en **"Run"** (▶️)
7. Espera el mensaje: **"Success. No rows returned"**

**✅ Resultado:** Base de datos completamente limpia.

---

### **PASO 2: CREAR TABLAS Y CONFIGURACIÓN**

1. En el mismo **SQL Editor**
2. Haz clic en **"+ New Query"** (nueva pestaña)
3. Copia y pega TODO el contenido de: `supabase_schema.sql`
4. Haz clic en **"Run"** (▶️)
5. Espera el mensaje: **"Success. No rows returned"**

**✅ Resultado:** 
- ✅ 7 tablas creadas (materials, folders, material_folders, questions, answers, user_profiles, spaced_repetition)
- ✅ Todas las políticas RLS activas
- ✅ Índices optimizados
- ✅ Triggers automáticos
- ✅ Vistas útiles creadas

---

### **PASO 3: INSERTAR DATOS DE PRUEBA** (OPCIONAL)

1. **PRIMERO:** Obtén tu `USER_ID`
   - Ve a **Authentication** > **Users** en Supabase
   - Encuentra el usuario **juanperez44@gmail.com** (o el que creaste)
   - Copia su **UUID** (ejemplo: `fff50ee0-b929-4d29-9eaf-c59ab7026bf6`)

2. Abre el archivo: `DATOS_PRUEBA.sql`

3. **REEMPLAZA** en la línea 16:
   ```sql
   v_user_id UUID := 'fff50ee0-b929-4d29-9eaf-c59ab7026bf6'; -- ✅ PON TU UUID AQUÍ
   ```

4. En **SQL Editor**, crea **"+ New Query"**

5. Copia y pega el contenido de `DATOS_PRUEBA.sql` (ya modificado)

6. Haz clic en **"Run"** (▶️)

**✅ Resultado:** Base de datos con datos de ejemplo listos para probar.

---

## 🔍 **VERIFICAR QUE TODO FUNCIONÓ**

### **Verificar Tablas:**

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
ORDER BY table_name;
```

**Deberías ver:**
- ✅ answers
- ✅ folders
- ✅ material_folders
- ✅ materials
- ✅ questions
- ✅ spaced_repetition
- ✅ user_profiles

---

### **Verificar Políticas RLS:**

```sql
SELECT schemaname, tablename, policyname 
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename;
```

**Deberías ver políticas para TODAS las tablas.**

---

### **Verificar Datos de Prueba:**

```sql
-- Ver perfil de usuario
SELECT * FROM public.user_profiles;

-- Ver carpetas
SELECT id, name, path FROM public.folders;

-- Ver materiales
SELECT id, title, file_name, total_chunks FROM public.materials;

-- Ver preguntas
SELECT id, question_text, topic FROM public.questions;

-- Ver estadísticas del usuario
SELECT * FROM public.user_stats;
```

---

## 🎯 **SIGUIENTE PASO: CONECTAR BACKEND**

Ahora que la BD está lista, necesitas:

1. **Instalar cliente de Supabase en backend:**
   ```bash
   cd c:\Users\Abel\Desktop\recuiva
   .\venv\Scripts\Activate.ps1
   pip install supabase
   ```

2. **Configurar variables de entorno:**
   - Abre `backend/.env`
   - Agrega las credenciales de Supabase:
   ```env
   SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
   SUPABASE_KEY=tu-anon-key-aqui
   ```

3. **Actualizar backend/main.py** para usar Supabase en lugar de archivos locales.

---

## ❓ **PROBLEMAS COMUNES**

### **Error: "relation does not exist"**
- **Solución:** Ejecutaste los archivos en orden incorrecto
- **Fix:** Ejecuta primero `LIMPIAR_Y_RECREAR_BD.sql`, luego `supabase_schema.sql`

### **Error: "violates row-level security policy"**
- **Solución:** No estás autenticado o el user_id no coincide
- **Fix:** Verifica que el user_id en DATOS_PRUEBA.sql sea correcto

### **Error: "duplicate key value violates unique constraint"**
- **Solución:** Ya existen datos con el mismo ID
- **Fix:** Ejecuta `LIMPIAR_Y_RECREAR_BD.sql` primero

---

## ✅ **CHECKLIST FINAL**

- [ ] Base de datos limpiada
- [ ] Tablas creadas correctamente
- [ ] Políticas RLS activas
- [ ] Datos de prueba insertados (opcional)
- [ ] Verificación con queries exitosa
- [ ] Variables de entorno configuradas en backend

---

**🎉 ¡LISTO! Tu base de datos está configurada y lista para usar.**

**Próximo paso:** Actualizar `backend/main.py` para que use Supabase.
