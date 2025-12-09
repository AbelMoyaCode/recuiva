/**
 * AUTH GUARD - Protege páginas que requieren autenticación
 * Usar en TODAS las páginas del /app/ (excepto login y registro)
 * 
 * MEJORADO: Ahora carga datos completos de user_profiles incluyendo avatar
 * 
 * Uso: <script src="../assets/js/auth-guard.js"></script>
 */

(async function () {
    console.log('🔐 Verificando autenticación...');

    // Verificar si estamos en una página pública (no requiere auth)
    const publicPages = [
        '/index.html',
        '/landing-page.html',
        '/app/auth/iniciar-sesion.html',
        '/app/auth/crear-cuenta.html'
    ];

    const currentPath = window.location.pathname;
    const isPublicPage = publicPages.some(page => currentPath.includes(page));

    if (isPublicPage) {
        console.log('📄 Página pública, no requiere autenticación');
        return;
    }

    // Verificar autenticación con Supabase
    try {
        if (typeof supabaseClient === 'undefined') {
            console.error('❌ Supabase no está inicializado');
            redirectToLogin();
            return;
        }

        const { data: { user }, error } = await supabaseClient.auth.getUser();

        if (error || !user) {
            console.warn('⚠️ No hay sesión activa');
            redirectToLogin();
            return;
        }

        console.log('✅ Usuario autenticado:', user.email);

        // Cargar datos completos del perfil desde user_profiles
        let profileData = null;
        try {
            const { data: profile, error: profileError } = await supabaseClient
                .from('user_profiles')
                .select('*')
                .eq('id', user.id)
                .single();

            if (!profileError && profile) {
                profileData = profile;
                console.log('✅ Perfil cargado desde Supabase:', profile);
                console.log('🖼️ Avatar URL en Supabase:', profile.avatar_url || 'NULL');
            } else if (profileError) {
                console.warn('⚠️ Error cargando perfil:', profileError);
            }
        } catch (e) {
            console.warn('⚠️ No se pudo cargar user_profiles:', e);
        }

        // Construir objeto de usuario completo
        const userData = {
            id: user.id,
            email: user.email,
            name: profileData?.full_name || user.user_metadata?.full_name || user.email.split('@')[0],
            full_name: profileData?.full_name || user.user_metadata?.full_name || user.email.split('@')[0],
            avatar_url: profileData?.avatar_url || user.user_metadata?.avatar_url || null,
            study_mode: profileData?.study_mode || 'intensivo',
            study_rhythm: profileData?.study_rhythm || { questions_per_day: 10, days_per_week: 5 },
            notification_settings: profileData?.notification_settings || null,
            language: profileData?.language || 'es',
            sm2_settings: profileData?.sm2_settings || null,
            provider: user.app_metadata?.provider || 'email'
        };

        localStorage.setItem('recuiva_user', JSON.stringify(userData));
        localStorage.setItem('recuiva_isAuthenticated', 'true');

        console.log('✅ Datos de usuario sincronizados en localStorage:', userData);
        console.log('🖼️ Avatar URL guardado en localStorage:', userData.avatar_url || 'NULL');

        // Refrescar el header para mostrar el avatar actualizado
        if (typeof window.initializeHeaderFooter === 'function') {
            const currentPage = window.location.pathname.split('/').pop().replace('.html', '');
            console.log('🔄 Refrescando header con datos actualizados...');
            setTimeout(() => {
                window.initializeHeaderFooter(currentPage);
            }, 100);
        }

    } catch (error) {
        console.error('❌ Error verificando autenticación:', error);
        redirectToLogin();
    }

    function redirectToLogin() {
        // Guardar la URL actual para volver después del login
        const returnUrl = window.location.href;
        localStorage.setItem('recuiva_returnUrl', returnUrl);

        console.log('🔄 Redirigiendo a login...');

        // Calcular ruta relativa al login
        const pathSegments = window.location.pathname.split('/');
        const appIndex = pathSegments.indexOf('app');

        if (appIndex !== -1) {
            // Estamos en alguna página dentro de /app/
            window.location.replace('/app/auth/iniciar-sesion.html');
        } else {
            // Fallback
            window.location.replace('/app/auth/iniciar-sesion.html');
        }
    }
})();
