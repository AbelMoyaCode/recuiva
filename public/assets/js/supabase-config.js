// Configuración de Supabase
const SUPABASE_URL = 'https://xqicgzqgluslzleddmfv.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhxaWNnenFnbHVzbHpsZWRkbWZ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIxOTExNjgsImV4cCI6MjA3Nzc2NzE2OH0.8IURJAIdKF_XgjaeAZhHm-_P8wfkevgnCAbr4MN8mg8';

// Inicializar cliente de Supabase
let supabaseClient;

// Función para inicializar Supabase de forma segura
function initSupabase() {
  try {
    if (typeof supabase === 'undefined') {
      console.error('❌ Supabase SDK no está cargado. Verifica que el script CDN esté incluido.');
      return null;
    }
    
    if (!supabaseClient) {
      supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
      console.log('✅ Cliente de Supabase inicializado correctamente');
    }
    
    return supabaseClient;
  } catch (error) {
    console.error('❌ Error al inicializar Supabase:', error);
    return null;
  }
}

// Inicializar automáticamente
supabaseClient = initSupabase();

// ✅ Hacerlo disponible globalmente en window
window.supabaseClient = supabaseClient;

// Helper functions
async function getCurrentUser() {
  if (!supabaseClient) {
    console.error('❌ Supabase no está inicializado');
    return null;
  }
  
  try {
    const { data: { user }, error } = await supabaseClient.auth.getUser();
    if (error) throw error;
    return user;
  } catch (error) {
    console.error('Error al obtener usuario:', error);
    return null;
  }
}

async function getCurrentUserId() {
  const user = await getCurrentUser();
  return user ? user.id : null;
}

async function isAuthenticated() {
  const user = await getCurrentUser();
  return user !== null;
}

async function logout() {
  if (!supabaseClient) {
    console.error('❌ Supabase no está inicializado');
    return;
  }
  
  try {
    const { error } = await supabaseClient.auth.signOut();
    if (error) throw error;
    
    localStorage.removeItem('recuiva_user');
    localStorage.removeItem('recuiva_isAuthenticated');
    window.location.href = '/index.html';
  } catch (error) {
    console.error('Error al cerrar sesión:', error);
  }
}

