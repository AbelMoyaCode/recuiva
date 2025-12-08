-- ============================================================
-- MIGRACIÓN: Agregar columnas a user_profiles para Mi Perfil
-- ============================================================
-- Ejecutar en Supabase SQL Editor
-- Fecha: Diciembre 2024
-- ============================================================

-- Agregar columna study_rhythm (JSONB) para ritmo de estudio
ALTER TABLE public.user_profiles 
ADD COLUMN IF NOT EXISTS study_rhythm JSONB DEFAULT '{"questions_per_day": 10, "days_per_week": 5}'::jsonb;

-- Agregar columna notification_settings (JSONB) para recordatorios
ALTER TABLE public.user_profiles 
ADD COLUMN IF NOT EXISTS notification_settings JSONB DEFAULT '{"reminder_time": "09:00", "review_reminders": true, "progress_notifications": true}'::jsonb;

-- Agregar columna language (TEXT) para idioma preferido
ALTER TABLE public.user_profiles 
ADD COLUMN IF NOT EXISTS language TEXT DEFAULT 'es';

-- Agregar columna study_mode (TEXT) para modalidad de estudio
ALTER TABLE public.user_profiles 
ADD COLUMN IF NOT EXISTS study_mode TEXT DEFAULT 'intensivo';

-- Agregar columna dark_mode (BOOLEAN) para tema oscuro
ALTER TABLE public.user_profiles 
ADD COLUMN IF NOT EXISTS dark_mode BOOLEAN DEFAULT false;

-- ============================================================
-- VERIFICAR CAMBIOS
-- ============================================================
-- Ejecutar para verificar:
-- SELECT column_name, data_type, column_default 
-- FROM information_schema.columns 
-- WHERE table_name = 'user_profiles' AND table_schema = 'public';
-- ============================================================
