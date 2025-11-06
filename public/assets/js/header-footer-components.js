/**
 * HEADER Y FOOTER UNIVERSAL DE RECUIVA
 * Sistema completo de componentes reutilizables con:
 * - Menú hamburguesa responsive
 * - Dropdown de perfil con cerrar sesión
 * - Auto-detección de página activa
 * - Integración con Supabase Auth
 */

// ==========================================
// CONFIGURACIÓN GLOBAL
// ==========================================

const RECUIVA_CONFIG = {
  logo: '/assets/img/Icon-Recuiva.png',
  logoAlt: 'Logo Recuiva',
  brandName: 'Recuiva',
  colors: {
    primary: '#FF6600',
    secondary: '#004EAA',
    accent: '#A5CDED'
  }
};

// ==========================================
// UTILIDADES
// ==========================================

function isAuthenticated() {
  return localStorage.getItem('recuiva_isAuthenticated') === 'true';
}

function getCurrentUser() {
  const userStr = localStorage.getItem('recuiva_user');
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch(e) {
    return null;
  }
}

function getRelativePath(basePath) {
  const currentPath = window.location.pathname;
  const depth = (currentPath.match(/\//g) || []).length;
  
  if (depth <= 2) return basePath.replace('../', '');
  if (depth === 3) return '../' + basePath.replace('../', '');
  return basePath;
}

// ==========================================
// HEADER PÚBLICO (NO AUTENTICADO)
// ==========================================

function renderPublicHeader() {
  return `
    <header class="bg-white shadow-md sticky top-0 z-50">
      <div class="container mx-auto px-6 py-4 flex justify-between items-center">
        <!-- Logo -->
        <div class="flex items-center gap-2">
          <a href="/index.html" class="flex items-center gap-2">
            <img src="/assets/img/Icon-Recuiva.png" alt="${RECUIVA_CONFIG.logoAlt}" 
                 class="h-10 w-10 object-contain md:h-12 md:w-12" style="max-width:48px; max-height:48px;"/>
            <span class="text-2xl font-extrabold text-gray-900">${RECUIVA_CONFIG.brandName}</span>
          </a>
        </div>

        <!-- Navegación Desktop -->
        <nav class="hidden md:flex items-center gap-8">
          <a class="text-gray-600 hover:text-orange-500 transition-colors" href="/index.html">Inicio</a>
        </nav>

        <!-- Botones Desktop -->
        <div class="hidden md:flex items-center gap-4">
          <a href="/app/auth/iniciar-sesion.html">
            <button type="button" class="border-2 border-blue-700 text-blue-700 font-bold py-2 px-6 rounded-full hover:bg-blue-50 transition-all">
              Iniciar sesión
            </button>
          </a>
          <a href="/app/auth/crear-cuenta.html">
            <button type="button" class="bg-blue-700 text-white font-bold py-2 px-6 rounded-full hover:bg-blue-800 transition-all">
              Crear cuenta
            </button>
          </a>
        </div>

        <!-- Menú Mobile -->
        <div class="md:hidden">
          <button class="menu-btn z-50 p-2 rounded-full hover:bg-gray-100" id="menu-btn" onclick="window.toggleMobileMenu(event)">
            <span class="material-symbols-outlined text-3xl text-gray-900 menu-icon">menu</span>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div class="mobile-menu md:hidden fixed top-[73px] left-0 w-full bg-white z-40 shadow-lg" id="mobile-menu">
        <div class="flex flex-col h-[calc(100vh-73px)] items-center justify-center gap-8 px-6">
          <a class="text-2xl text-gray-600 hover:text-orange-500 transition-colors" href="/index.html">Inicio</a>
          <hr class="w-2/3 border-gray-300" />
          <a href="/app/auth/iniciar-sesion.html" class="w-full max-w-xs">
            <button type="button" class="w-full border-2 border-blue-700 text-blue-700 font-bold py-3 px-6 rounded-full hover:bg-blue-50 transition-all">
              Iniciar sesión
            </button>
          </a>
          <a href="/app/auth/crear-cuenta.html" class="w-full max-w-xs">
            <button type="button" class="w-full bg-blue-700 text-white font-bold py-3 px-6 rounded-full hover:bg-blue-800 transition-all">
              Crear cuenta
            </button>
          </a>
        </div>
      </div>
    </header>
  `;
}

// ==========================================
// HEADER AUTENTICADO (CON MENÚ DE USUARIO)
// ==========================================

function renderAuthenticatedHeader(currentPage = '') {
  const user = getCurrentUser();
  const userName = user?.name || 'Usuario';
  const userInitials = userName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
  
  // Rutas absolutas (funcionan desde cualquier página)
  const routes = {
    inicio: '/app/home.html',
    materiales: '/app/materiales.html',
    dashboard: '/app/dashboard.html',
    repasos: '/app/repasos.html',
    practica: '/app/sesion-practica.html',
    perfil: '/app/mi-perfil.html'
  };

  return `
    <header class="bg-white shadow-md sticky top-0 z-50">
      <div class="container mx-auto px-4 md:px-6 py-3 flex justify-between items-center">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <a href="${routes.inicio}" class="flex items-center gap-2">
            <img src="/assets/img/Icon-Recuiva.png" alt="${RECUIVA_CONFIG.logoAlt}" 
                 class="h-10 w-10 object-contain md:h-12 md:w-12" style="max-width:48px; max-height:48px;"/>
            <span class="text-2xl font-extrabold text-gray-900 hidden sm:inline">${RECUIVA_CONFIG.brandName}</span>
          </a>
        </div>

        <!-- Navegación Desktop -->
        <nav class="hidden md:flex items-center gap-4">
          <a class="text-gray-600 hover:text-orange-500 transition-colors px-3 py-2 rounded-lg ${currentPage === 'inicio' ? 'text-orange-500 font-semibold' : ''}" 
             href="${routes.inicio}">Inicio</a>
          <a class="text-gray-600 hover:text-orange-500 transition-colors px-3 py-2 rounded-lg ${currentPage === 'materiales' ? 'text-orange-500 font-semibold' : ''}" 
             href="${routes.materiales}">Materiales</a>
          <a class="text-gray-600 hover:text-orange-500 transition-colors px-3 py-2 rounded-lg ${currentPage === 'dashboard' ? 'text-orange-500 font-semibold' : ''}" 
             href="${routes.dashboard}">Dashboard</a>
          <a class="text-gray-600 hover:text-orange-500 transition-colors px-3 py-2 rounded-lg ${currentPage === 'repasos' ? 'text-orange-500 font-semibold' : ''}" 
             href="${routes.repasos}">Repasos</a>
          <a class="text-gray-600 hover:text-orange-500 transition-colors px-3 py-2 rounded-lg ${currentPage === 'practica' ? 'text-orange-500 font-semibold' : ''}" 
             href="${routes.practica}">Práctica</a>
        </nav>

        <!-- Menú de Usuario Desktop -->
        <div class="hidden md:flex items-center gap-3">
          <div class="relative">
            <button 
              id="profile-btn" 
              onclick="window.toggleProfileMenu()"
              class="flex items-center gap-2 px-3 py-2 rounded-full hover:bg-gray-100 transition-all cursor-pointer group"
            >
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-orange-500 to-blue-700 flex items-center justify-center text-white font-bold text-sm">
                ${userInitials}
              </div>
              <span class="text-gray-700 font-medium hidden lg:inline">${userName}</span>
              <span class="material-symbols-outlined text-gray-600 transition-transform group-hover:rotate-180">
                expand_more
              </span>
            </button>

            <!-- Dropdown Menu -->
            <div id="profile-dropdown" class="profile-dropdown absolute right-0 top-full mt-2 bg-white border border-gray-200 rounded-xl shadow-xl min-w-[14rem] z-50">
              <div class="p-4 border-b border-gray-100">
                <p class="font-semibold text-gray-900">${userName}</p>
                <p class="text-sm text-gray-500">${user?.email || ''}</p>
              </div>
              <div class="py-2">
                <a href="${routes.perfil}" class="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 transition-all">
                  <span class="material-symbols-outlined text-gray-600">person</span>
                  <span class="text-gray-700">Mi perfil</span>
                </a>
                <a href="${routes.dashboard}" class="flex items-center gap-3 px-4 py-2 hover:bg-gray-50 transition-all">
                  <span class="material-symbols-outlined text-gray-600">dashboard</span>
                  <span class="text-gray-700">Dashboard</span>
                </a>
                <hr class="my-2 border-gray-100" />
                <button onclick="window.cerrarSesion()" class="w-full flex items-center gap-3 px-4 py-2 hover:bg-red-50 transition-all text-red-600">
                  <span class="material-symbols-outlined">logout</span>
                  <span class="font-medium">Cerrar sesión</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Menú Mobile (Hamburguesa) -->
        <div class="md:hidden">
          <button class="menu-btn z-50 p-2 rounded-full hover:bg-gray-100" id="menu-btn" onclick="window.toggleMobileMenu(event)">
            <span class="material-symbols-outlined text-3xl text-gray-900 menu-icon">menu</span>
          </button>
        </div>
      </div>

      <!-- Mobile Menu Expandido -->
      <div class="mobile-menu md:hidden fixed top-[73px] left-0 w-full bg-white z-40 shadow-lg" id="mobile-menu">
        <div class="flex flex-col h-[calc(100vh-73px)] items-center justify-center gap-5 px-6 py-8 overflow-y-auto">
          <!-- Perfil en móvil -->
          <div class="flex flex-col items-center gap-3 pb-5 border-b-2 border-gray-200 w-full max-w-sm">
            <div class="w-20 h-20 rounded-full bg-gradient-to-br from-orange-500 to-blue-700 flex items-center justify-center text-white font-bold text-2xl shadow-lg">
              ${userInitials}
            </div>
            <span class="font-bold text-lg text-gray-900">${userName}</span>
            <span class="text-sm text-gray-500 text-center break-all px-2">${user?.email || ''}</span>
          </div>

          <!-- Navegación móvil -->
          <nav class="flex flex-col items-center gap-5 w-full max-w-sm py-4">
            <a class="text-xl font-medium text-gray-700 hover:text-orange-500 transition-colors w-full text-center py-3 rounded-lg hover:bg-orange-50 ${currentPage === 'inicio' ? 'text-orange-500 font-bold bg-orange-50' : ''}" 
               href="${routes.inicio}">Inicio</a>
            <a class="text-xl font-medium text-gray-700 hover:text-orange-500 transition-colors w-full text-center py-3 rounded-lg hover:bg-orange-50 ${currentPage === 'materiales' ? 'text-orange-500 font-bold bg-orange-50' : ''}" 
               href="${routes.materiales}">Materiales</a>
            <a class="text-xl font-medium text-gray-700 hover:text-orange-500 transition-colors w-full text-center py-3 rounded-lg hover:bg-orange-50 ${currentPage === 'dashboard' ? 'text-orange-500 font-bold bg-orange-50' : ''}" 
               href="${routes.dashboard}">Dashboard</a>
            <a class="text-xl font-medium text-gray-700 hover:text-orange-500 transition-colors w-full text-center py-3 rounded-lg hover:bg-orange-50 ${currentPage === 'repasos' ? 'text-orange-500 font-bold bg-orange-50' : ''}" 
               href="${routes.repasos}">Repasos</a>
            <a class="text-xl font-medium text-gray-700 hover:text-orange-500 transition-colors w-full text-center py-3 rounded-lg hover:bg-orange-50 ${currentPage === 'practica' ? 'text-orange-500 font-bold bg-orange-50' : ''}" 
               href="${routes.practica}">Práctica</a>
          </nav>

          <hr class="w-3/4 border-gray-300 my-2" />

          <button onclick="window.cerrarSesion()" class="flex items-center justify-center gap-3 text-xl text-red-600 font-bold py-3 px-6 rounded-lg hover:bg-red-50 transition-colors w-full max-w-sm">
            <span class="material-symbols-outlined text-2xl">logout</span>
            <span>Cerrar sesión</span>
          </button>
        </div>
      </div>
    </header>
  `;
}

// ==========================================
// FOOTER UNIVERSAL
// ==========================================

function renderFooter() {
  return `
    <footer class="text-gray-100 py-12 px-6 mt-16" style="background-color: #004EAA;">
      <div class="container mx-auto text-center">
        <div class="flex justify-center items-center gap-2 mb-6">
          <img src="/assets/img/Icon-Recuiva.png" alt="${RECUIVA_CONFIG.logoAlt}" 
               class="h-10 w-10 object-contain md:h-12 md:w-12" style="max-width:48px; max-height:48px;"/>
          <span class="text-2xl font-extrabold">${RECUIVA_CONFIG.brandName}</span>
        </div>
        <div class="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 mb-6">
          <a class="hover:text-orange-400 transition-colors" href="/app/institucional/active-recall.html">Active Recall</a>
          <a class="hover:text-orange-400 transition-colors" href="/app/institucional/validacion-semantica.html">Validación Semántica</a>
          <a class="hover:text-orange-400 transition-colors" href="/app/institucional/diferencias.html">Diferencias</a>
          <a class="hover:text-orange-400 transition-colors" href="#">Contacto</a>
          <a class="hover:text-orange-400 transition-colors" href="#">Términos</a>
          <a class="hover:text-orange-400 transition-colors" href="#">Privacidad</a>
        </div>
        <p class="text-sm opacity-75">© 2025 Recuiva. Todos los derechos reservados.</p>
      </div>
    </footer>
  `;
}

// ==========================================
// FUNCIONES DE INTERACCIÓN
// ==========================================

window.toggleMobileMenu = function(event) {
  // Prevenir propagación del evento para evitar que se cierre inmediatamente
  if (event) {
    event.stopPropagation();
    event.preventDefault();
  }
  
  const mobileMenu = document.getElementById('mobile-menu');
  const menuBtn = document.getElementById('menu-btn');
  const menuIcon = menuBtn?.querySelector('.menu-icon');
  
  if (!mobileMenu || !menuIcon) {
    console.warn('⚠️ No se encontraron elementos del menú móvil');
    return;
  }
  
  const isOpen = mobileMenu.classList.contains('active');
  
  console.log(`🍔 Toggle menú móvil: ${isOpen ? 'CERRAR' : 'ABRIR'}`);
  
  if (isOpen) {
    // Cerrar
    mobileMenu.classList.remove('active');
    document.body.classList.remove('overflow-hidden');
    menuIcon.style.transition = 'transform 0.3s ease, opacity 0.15s ease';
    menuIcon.style.transform = 'rotate(90deg)';
    menuIcon.style.opacity = '0';
    setTimeout(() => {
      menuIcon.textContent = 'menu';
      menuIcon.style.transform = 'rotate(0deg)';
      menuIcon.style.opacity = '1';
    }, 150);
  } else {
    // Abrir
    mobileMenu.classList.add('active');
    document.body.classList.add('overflow-hidden');
    menuIcon.style.transition = 'transform 0.3s ease, opacity 0.15s ease';
    menuIcon.style.transform = 'rotate(90deg)';
    menuIcon.style.opacity = '0';
    setTimeout(() => {
      menuIcon.textContent = 'close';
      menuIcon.style.transform = 'rotate(0deg)';
      menuIcon.style.opacity = '1';
    }, 150);
  }
};

window.toggleProfileMenu = function() {
  const dropdown = document.getElementById('profile-dropdown');
  if (!dropdown) return;
  dropdown.classList.toggle('active');
};

window.cerrarSesion = async function() {
  if (!confirm('¿Estás seguro de que deseas cerrar sesión?')) return;
  
  try {
    // Si Supabase está disponible, cerrar sesión
    if (typeof supabaseClient !== 'undefined') {
      await supabaseClient.auth.signOut();
    }
  } catch(e) {
    console.log('Supabase no disponible, limpiando localStorage directamente');
  }
  
  // Limpiar localStorage
  localStorage.removeItem('recuiva_user');
  localStorage.removeItem('recuiva_isAuthenticated');
  localStorage.clear();
  
  // Redirigir a landing
  window.location.href = '/index.html';
};

// Cerrar dropdown al hacer clic fuera
document.addEventListener('click', function(e) {
  const profileBtn = document.getElementById('profile-btn');
  const profileDropdown = document.getElementById('profile-dropdown');
  
  if (profileDropdown && profileBtn && 
      !profileBtn.contains(e.target) && 
      !profileDropdown.contains(e.target)) {
    profileDropdown.classList.remove('active');
  }
  
  // NO cerrar el menú móvil si el clic es en el botón del menú o dentro del menú
  const menuBtn = document.getElementById('menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  
  // Solo cerrar si se hace clic FUERA del menú y del botón
  if (mobileMenu && 
      mobileMenu.classList.contains('active') && 
      menuBtn && 
      !menuBtn.contains(e.target) && 
      !mobileMenu.contains(e.target)) {
    // No hacer nada - dejar que el usuario cierre con el botón hamburguesa
    // window.toggleMobileMenu(); // COMENTADO para evitar cierre automático
  }
});

// ==========================================
// FUNCIÓN PRINCIPAL DE INICIALIZACIÓN
// ==========================================

window.initializeHeaderFooter = function(currentPage = '') {
  // Insertar Header
  const headerContainer = document.getElementById('header-container');
  if (headerContainer) {
    const authenticated = isAuthenticated();
    headerContainer.innerHTML = authenticated 
      ? renderAuthenticatedHeader(currentPage)
      : renderPublicHeader();
  }

  // Insertar Footer
  const footerContainer = document.getElementById('footer-container');
  if (footerContainer) {
    footerContainer.innerHTML = renderFooter();
  }
};

// ==========================================
// ESTILOS CSS NECESARIOS
// ==========================================

const styles = `
<style>
/* Menú móvil - Inicialmente oculto */
.mobile-menu {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.3s ease;
  opacity: 0;
}

/* Menú móvil - Cuando está activo */
.mobile-menu.active {
  max-height: 500px !important;
  opacity: 1 !important;
  overflow-y: auto;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Icono del menú - Animaciones */
.menu-icon {
  transition: transform 0.3s ease, opacity 0.15s ease !important;
  display: inline-block;
}

/* Dropdown de perfil - Estado inicial (oculto) */
.profile-dropdown {
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.2s ease;
  pointer-events: none;
}

/* Dropdown de perfil - Cuando está activo (visible) */
.profile-dropdown.active {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateY(0) !important;
  pointer-events: auto !important;
}

/* Prevenir scroll cuando el menú está abierto */
body.overflow-hidden {
  overflow: hidden;
}
</style>
`;

// Insertar estilos en el head
if (!document.getElementById('header-footer-styles')) {
  document.head.insertAdjacentHTML('beforeend', styles.replace('<style>', '<style id="header-footer-styles">'));
}

// ==========================================
// AUTO-INICIALIZACIÓN
// ==========================================

// Asegurar que los componentes se carguen cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('🎨 Inicializando componentes Header/Footer...');
    // Si no se ha llamado manualmente, inicializar con página por defecto
    if (!document.getElementById('header-container')?.innerHTML) {
      initializeHeaderFooter('inicio');
    }
  });
} else {
  // El DOM ya está cargado
  console.log('🎨 DOM ya cargado, verificando componentes...');
  if (!document.getElementById('header-container')?.innerHTML) {
    initializeHeaderFooter('inicio');
  }
}
