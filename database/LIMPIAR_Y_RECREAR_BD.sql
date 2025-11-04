-- ========================================
-- SCRIPT DE LIMPIEZA Y RECREACIÓN DE BD
-- RECUIVA - EJECUTAR EN SUPABASE SQL EDITOR
-- ========================================
-- ⚠️ ADVERTENCIA: Este script ELIMINA TODOS LOS DATOS
-- Solo ejecutar si quieres empezar de cero
-- ========================================

-- PASO 1: ELIMINAR TODAS LAS POLÍTICAS RLS
-- ========================================
DROP POLICY IF EXISTS "Users can view own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can insert own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can update own materials" ON public.materials;
DROP POLICY IF EXISTS "Users can delete own materials" ON public.materials;

DROP POLICY IF EXISTS "Users can view own folders" ON public.folders;
DROP POLICY IF EXISTS "Users can insert own folders" ON public.folders;
DROP POLICY IF EXISTS "Users can update own folders" ON public.folders;
DROP POLICY IF EXISTS "Users can delete own folders" ON public.folders;

DROP POLICY IF EXISTS "Users can view own material_folders" ON public.material_folders;
DROP POLICY IF EXISTS "Users can insert own material_folders" ON public.material_folders;
DROP POLICY IF EXISTS "Users can delete own material_folders" ON public.material_folders;

DROP POLICY IF EXISTS "Users can view own questions" ON public.questions;
DROP POLICY IF EXISTS "Users can insert own questions" ON public.questions;
DROP POLICY IF EXISTS "Users can delete own questions" ON public.questions;

DROP POLICY IF EXISTS "Users can view own answers" ON public.answers;
DROP POLICY IF EXISTS "Users can insert own answers" ON public.answers;

DROP POLICY IF EXISTS "Users can view own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.user_profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON public.user_profiles;

DROP POLICY IF EXISTS "Users can view own spaced repetition" ON public.spaced_repetition;
DROP POLICY IF EXISTS "Users can insert own spaced repetition" ON public.spaced_repetition;
DROP POLICY IF EXISTS "Users can update own spaced repetition" ON public.spaced_repetition;
DROP POLICY IF EXISTS "Users can delete own spaced repetition" ON public.spaced_repetition;

-- PASO 2: ELIMINAR TODOS LOS TRIGGERS
-- ========================================
DROP TRIGGER IF EXISTS update_materials_updated_at ON public.materials;
DROP TRIGGER IF EXISTS update_folders_updated_at ON public.folders;
DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON public.user_profiles;
DROP TRIGGER IF EXISTS update_spaced_repetition_updated_at ON public.spaced_repetition;

-- PASO 3: ELIMINAR TODAS LAS FUNCIONES
-- ========================================
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- PASO 4: ELIMINAR TODAS LAS VISTAS
-- ========================================
DROP VIEW IF EXISTS public.user_stats;
DROP VIEW IF EXISTS public.questions_due_for_review;

-- PASO 5: ELIMINAR TODAS LAS TABLAS (en orden inverso por dependencias)
-- ========================================
DROP TABLE IF EXISTS public.material_folders CASCADE;
DROP TABLE IF EXISTS public.spaced_repetition CASCADE;
DROP TABLE IF EXISTS public.answers CASCADE;
DROP TABLE IF EXISTS public.questions CASCADE;
DROP TABLE IF EXISTS public.folders CASCADE;
DROP TABLE IF EXISTS public.materials CASCADE;
DROP TABLE IF EXISTS public.user_profiles CASCADE;

-- ========================================
-- ✅ BASE DE DATOS LIMPIA
-- ========================================
-- Ahora ejecuta el archivo: supabase_schema.sql
-- Para recrear todas las tablas desde cero
-- ========================================
