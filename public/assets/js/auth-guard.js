/**
 * AUTH GUARD - Protege páginas que requieren autenticación
 * Usar en TODAS las páginas del /app/ (excepto login y registro)
 * 
 * Uso: <script src="../assets/js/auth-guard.js"></script>
 */

(async function() {
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
        
        // Guardar info básica en localStorage para UI
        const userData = {
            id: user.id,
            email: user.email,
            full_name: user.user_metadata?.full_name || user.email
        };
        localStorage.setItem('recuiva_user', JSON.stringify(userData));
        localStorage.setItem('recuiva_isAuthenticated', 'true');
        
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
            window.location.replace('../auth/iniciar-sesion.html');
        } else {
            // Fallback
            window.location.replace('/public/app/auth/iniciar-sesion.html');
        }
    }
})();
