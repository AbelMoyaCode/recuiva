// ===================================================================
// MI PERFIL - FUNCIONES COMPLETAS CON SUPABASE
// Todas las funciones guardan y leen desde Supabase, NO localStorage
// ===================================================================

// Helper para obtener supabaseClient de forma segura
function getSupabase() {
  return window.supabaseClient || supabaseClient;
}

// ===================================================================
// INICIALIZACIÓN - Cargar datos del perfil al abrir la página
// ===================================================================
window.addEventListener('DOMContentLoaded', async () => {
  console.log('🔄 Cargando datos del perfil desde Supabase...');

  // Esperar un poco para asegurar que supabaseClient esté listo
  await new Promise(resolve => setTimeout(resolve, 200));

  if (!getSupabase()) {
    console.error('❌ Supabase no está inicializado');
    return;
  }

  await loadProfileFromSupabase();
});

async function loadProfileFromSupabase() {
  try {
    const { data: { user } } = await getSupabase().auth.getUser();
    if (!user) {
      console.log('❌ Usuario no autenticado');
      return;
    }

    // Obtener perfil desde user_profiles
    const { data: profile, error } = await supabaseClient
      .from('user_profiles')
      .select('*')
      .eq('id', user.id)
      .single();

    if (error && error.code !== 'PGRST116') {
      console.error('❌ Error cargando perfil:', error);
    }

    // Actualizar UI con datos del usuario
    const nameEl = document.getElementById('profile-name');
    const emailEl = document.getElementById('profile-email');
    const imageEl = document.getElementById('profile-image');
    const rhythmEl = document.getElementById('current-rhythm');
    const modeEl = document.getElementById('current-mode');
    const reminderEl = document.getElementById('reminder-status');

    // Nombre: usar metadata de auth o perfil
    const displayName = user.user_metadata?.full_name ||
      profile?.full_name ||
      user.email?.split('@')[0] ||
      'Usuario';
    if (nameEl) nameEl.textContent = displayName;

    // Email
    if (emailEl) emailEl.textContent = user.email || '';

    // Avatar
    const avatarUrl = user.user_metadata?.avatar_url ||
      profile?.avatar_url ||
      `https://ui-avatars.com/api/?name=${encodeURIComponent(displayName)}&background=FF6600&color=fff`;
    if (imageEl) imageEl.src = avatarUrl;

    // Ritmo de estudio
    if (rhythmEl && profile?.study_rhythm) {
      const rhythm = profile.study_rhythm;
      rhythmEl.textContent = `${rhythm.questions_per_day || 10} preguntas/${rhythm.days_per_week || 5} días`;
    }

    // Modalidad de estudio
    if (modeEl && profile?.study_mode) {
      const modes = { 'intensivo': 'Intensivo', 'moderado': 'Moderado', 'relajado': 'Relajado' };
      modeEl.textContent = modes[profile.study_mode] || 'Intensivo';
    }

    // Recordatorios
    if (reminderEl && profile?.notification_settings) {
      const settings = profile.notification_settings;
      const active = settings.review_reminders || settings.progress_notifications;
      reminderEl.textContent = active ? 'Activos' : 'Inactivos';
      reminderEl.className = active ? 'text-green-600 font-medium' : 'text-red-600 font-medium';
    }

    // Badge de tipo de cuenta (Gmail vs Email)
    const badge = document.getElementById('account-type-badge');
    const isGmail = user.app_metadata?.provider === 'google';
    if (badge) {
      badge.textContent = isGmail ? 'Gmail' : 'Email';
      badge.className = `px-2 py-1 text-xs font-medium rounded-full ${isGmail ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}`;
      badge.classList.remove('hidden');
    }

    // Deshabilitar edición de email para cuentas Gmail
    const editEmailBtn = document.getElementById('edit-email-btn');
    if (editEmailBtn && isGmail) {
      editEmailBtn.style.opacity = '0.4';
      editEmailBtn.style.cursor = 'not-allowed';
      editEmailBtn.title = 'No puedes modificar el email de una cuenta Gmail';
    }

    console.log('✅ Perfil cargado correctamente');
  } catch (error) {
    console.error('❌ Error:', error);
  }
}

// ===================================================================
// FUNCIÓN HELPER: Sincronizar localStorage después de cambios
// ===================================================================
async function syncLocalStorageUser(updates = {}) {
  try {
    const { data: { user } } = await getSupabase().auth.getUser();
    if (!user) return;

    // Cargar datos actuales de user_profiles
    const { data: profile } = await supabaseClient
      .from('user_profiles')
      .select('*')
      .eq('id', user.id)
      .single();

    // Construir objeto actualizado
    const userData = {
      id: user.id,
      email: user.email,
      name: profile?.full_name || user.user_metadata?.full_name || user.email.split('@')[0],
      full_name: profile?.full_name || user.user_metadata?.full_name || user.email.split('@')[0],
      avatar_url: profile?.avatar_url || user.user_metadata?.avatar_url || null,
      study_mode: profile?.study_mode || 'intensivo',
      study_rhythm: profile?.study_rhythm || { questions_per_day: 10, days_per_week: 5 },
      notification_settings: profile?.notification_settings || null,
      language: profile?.language || 'es',
      sm2_settings: profile?.sm2_settings || null,
      provider: user.app_metadata?.provider || 'email',
      ...updates  // Aplicar actualizaciones pasadas
    };

    localStorage.setItem('recuiva_user', JSON.stringify(userData));
    console.log('✅ localStorage sincronizado con Supabase');

    // Refrescar el header si existe la función
    if (typeof window.initializeHeaderFooter === 'function') {
      const currentPage = window.location.pathname.split('/').pop().replace('.html', '');
      window.initializeHeaderFooter(currentPage);
    }

    return userData;
  } catch (error) {
    console.error('❌ Error sincronizando localStorage:', error);
  }
}

// ===================================================================
// 1. CAMBIAR FOTO DE PERFIL (Supabase Storage)
// ===================================================================
window.changeProfilePicture = async function () {
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = 'image/jpeg,image/png,image/webp';

  fileInput.onchange = async function (e) {
    const file = e.target.files[0];
    if (!file) return;

    // Validar tamaño (máx 2MB)
    if (file.size > 2 * 1024 * 1024) {
      showErrorMessage('La imagen debe pesar menos de 2MB');
      return;
    }

    try {
      // Mostrar preview inmediato
      const reader = new FileReader();
      reader.onload = function (e) {
        const profileImg = document.getElementById('profile-image');
        if (profileImg) profileImg.src = e.target.result;
      };
      reader.readAsDataURL(file);

      // Obtener usuario actual
      const { data: { user } } = await getSupabase().auth.getUser();
      if (!user) {
        showErrorMessage('Debes iniciar sesión primero');
        return;
      }

      // Generar nombre único para el archivo
      const fileExt = file.name.split('.').pop();
      const fileName = `${user.id}_${Date.now()}.${fileExt}`;
      const filePath = `avatars/${fileName}`;

      console.log('📤 Subiendo foto a Supabase Storage...');

      // Subir a Supabase Storage
      const { data, error } = await getSupabase().storage
        .from('avatars')
        .upload(filePath, file, {
          cacheControl: '3600',
          upsert: true
        });

      if (error) {
        console.error('❌ Error subiendo foto:', error);
        showErrorMessage('Error al subir la foto: ' + error.message);
        return;
      }

      // Obtener URL pública
      const { data: { publicUrl } } = getSupabase().storage
        .from('avatars')
        .getPublicUrl(filePath);

      console.log('✅ Foto subida, URL:', publicUrl);

      // Actualizar user_profiles
      await ensureUserProfile(user.id);
      const { error: updateError } = await supabaseClient
        .from('user_profiles')
        .update({ avatar_url: publicUrl })
        .eq('id', user.id);

      if (updateError) {
        console.error('❌ Error actualizando perfil:', updateError);
        showErrorMessage('Error al actualizar perfil');
        return;
      }

      console.log('✅ Perfil actualizado con nueva foto');
      showSuccessMessage('Foto de perfil actualizada correctamente');

      // Sincronizar localStorage y refrescar header
      await syncLocalStorageUser({ avatar_url: publicUrl });

      // Actualizar en navbar si existe
      const navbarImg = document.querySelector('#profile-btn img');
      if (navbarImg) navbarImg.src = publicUrl;

    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al procesar la imagen');
    }
  };

  fileInput.click();
};

// ===================================================================
// 2. EDITAR NOMBRE (Supabase user_profiles)
// ===================================================================
window.editName = async function () {
  const nameElement = document.getElementById('profile-name');
  const currentName = nameElement.textContent;

  showEditModal('Editar Nombre', 'Ingresa tu nuevo nombre:', currentName, async (newName) => {
    if (newName && newName.trim() !== '' && newName !== currentName) {
      try {
        const { data: { user } } = await getSupabase().auth.getUser();
        if (!user) {
          showErrorMessage('Debes iniciar sesión');
          return;
        }

        // Actualizar en auth.users metadata
        await getSupabase().auth.updateUser({
          data: { full_name: newName }
        });

        // Actualizar en user_profiles
        await ensureUserProfile(user.id);
        const { error } = await supabaseClient
          .from('user_profiles')
          .update({ full_name: newName })
          .eq('id', user.id);

        if (error) throw error;

        // Actualizar UI
        nameElement.textContent = newName;
        const navbarName = document.querySelector('#profile-btn .hidden.md\\:block');
        if (navbarName) navbarName.textContent = newName;

        // Sincronizar localStorage y refrescar header
        await syncLocalStorageUser({ name: newName, full_name: newName });

        console.log('✅ Nombre actualizado en Supabase');
        showSuccessMessage('Nombre actualizado correctamente');
      } catch (error) {
        console.error('❌ Error:', error);
        showErrorMessage('Error al actualizar nombre');
      }
    }
  });
};

// ===================================================================
// 3. EDITAR EMAIL (Supabase Auth)
// ===================================================================
window.editEmail = async function () {
  const { data: { user } } = await getSupabase().auth.getUser();

  // No permitir edición para cuentas Gmail
  if (user?.app_metadata?.provider === 'google') {
    showErrorMessage('No puedes modificar el email de una cuenta Gmail');
    return;
  }

  const emailElement = document.getElementById('profile-email');
  const currentEmail = emailElement.textContent;

  showEditModal('Editar Email', 'Ingresa tu nuevo email:', currentEmail, async (newEmail) => {
    if (newEmail && newEmail.trim() !== '' && newEmail !== currentEmail) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(newEmail)) {
        showErrorMessage('Por favor ingresa un email válido');
        return;
      }

      try {
        const { error } = await getSupabase().auth.updateUser({
          email: newEmail
        });

        if (error) throw error;

        showSuccessMessage('Se ha enviado un correo de verificación al nuevo email');
      } catch (error) {
        console.error('❌ Error:', error);
        showErrorMessage('Error al actualizar email: ' + error.message);
      }
    }
  });
};

// ===================================================================
// 4. CAMBIAR CONTRASEÑA (Supabase Auth)
// ===================================================================
window.changePassword = async function () {
  const { data: { user } } = await getSupabase().auth.getUser();

  if (user?.app_metadata?.provider === 'google') {
    showGmailPasswordModal();
    return;
  }

  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Cambiar Contraseña</h3>
      <form id="password-form" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nueva Contraseña</label>
          <input type="password" id="new-password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent" required minlength="6">
          <p class="text-xs text-gray-500 mt-1">Mínimo 6 caracteres</p>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Confirmar Contraseña</label>
          <input type="password" id="confirm-password" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent" required>
        </div>
        <div class="flex gap-3 mt-6">
          <button type="button" onclick="this.closest('.fixed').remove()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
            Cancelar
          </button>
          <button type="submit" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
            Cambiar
          </button>
        </div>
      </form>
    </div>
  `;

  document.body.appendChild(modal);

  document.getElementById('password-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (newPassword !== confirmPassword) {
      showErrorMessage('Las contraseñas no coinciden');
      return;
    }

    try {
      const { error } = await getSupabase().auth.updateUser({
        password: newPassword
      });

      if (error) throw error;

      showSuccessMessage('Contraseña cambiada correctamente');
      modal.remove();
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al cambiar contraseña: ' + error.message);
    }
  });

  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
};

function showGmailPasswordModal() {
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <div class="text-center">
        <span class="material-symbols-outlined text-4xl text-blue-600 mb-4">info</span>
        <h3 class="text-lg font-semibold mb-4 text-gray-800">Cuenta enlazada con Gmail</h3>
        <p class="text-gray-600 mb-6">Tu cuenta está enlazada con Gmail. Para cambiar la contraseña, debes hacerlo desde tu cuenta de Google.</p>
        <div class="flex gap-3">
          <button onclick="this.closest('.fixed').remove()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
            Cerrar
          </button>
          <button onclick="window.open('https://myaccount.google.com/security', '_blank'); this.closest('.fixed').remove();" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
            Ir a Google
          </button>
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(modal);
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
}

// ===================================================================
// 5. MODALIDAD DE ESTUDIO (Supabase)
// ===================================================================
window.showStudyModeModal = async function () {
  const { data: { user } } = await getSupabase().auth.getUser();
  const { data: profile } = await supabaseClient
    .from('user_profiles')
    .select('study_mode')
    .eq('id', user?.id)
    .single();

  const currentMode = profile?.study_mode || 'intensivo';

  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Modalidad de Estudio</h3>
      <div class="space-y-3">
        <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50 ${currentMode === 'intensivo' ? 'border-orange-500 bg-orange-50' : 'border-gray-200'}">
          <input type="radio" name="study-mode" value="intensivo" ${currentMode === 'intensivo' ? 'checked' : ''} class="mr-3">
          <div>
            <div class="font-medium">Intensivo</div>
            <div class="text-sm text-gray-500">Máximo aprendizaje, más preguntas por día</div>
          </div>
        </label>
        <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50 ${currentMode === 'moderado' ? 'border-orange-500 bg-orange-50' : 'border-gray-200'}">
          <input type="radio" name="study-mode" value="moderado" ${currentMode === 'moderado' ? 'checked' : ''} class="mr-3">
          <div>
            <div class="font-medium">Moderado</div>
            <div class="text-sm text-gray-500">Balance entre aprendizaje y tiempo</div>
          </div>
        </label>
        <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50 ${currentMode === 'relajado' ? 'border-orange-500 bg-orange-50' : 'border-gray-200'}">
          <input type="radio" name="study-mode" value="relajado" ${currentMode === 'relajado' ? 'checked' : ''} class="mr-3">
          <div>
            <div class="font-medium">Relajado</div>
            <div class="text-sm text-gray-500">Pocas preguntas, ritmo tranquilo</div>
          </div>
        </label>
      </div>
      <div class="flex gap-3 mt-6">
        <button onclick="this.closest('.fixed').remove()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button onclick="saveStudyMode()" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
          Guardar
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

  window.saveStudyMode = async function () {
    const selectedMode = document.querySelector('input[name="study-mode"]:checked')?.value;
    if (!selectedMode) return;

    try {
      await ensureUserProfile(user.id);
      const { error } = await supabaseClient
        .from('user_profiles')
        .update({ study_mode: selectedMode })
        .eq('id', user.id);

      if (error) throw error;

      const modes = { 'intensivo': 'Intensivo', 'moderado': 'Moderado', 'relajado': 'Relajado' };
      document.getElementById('current-mode').textContent = modes[selectedMode];

      showSuccessMessage('Modalidad de estudio actualizada');
      modal.remove();
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al guardar');
    }
  };
};

// ===================================================================
// 6. RITMO DE ESTUDIO (Supabase)
// ===================================================================
window.showStudyRhythmModal = async function () {
  const { data: { user } } = await getSupabase().auth.getUser();
  const { data: profile } = await supabaseClient
    .from('user_profiles')
    .select('study_rhythm')
    .eq('id', user?.id)
    .single();

  const rhythm = profile?.study_rhythm || { questions_per_day: 10, days_per_week: 5 };

  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Configurar Ritmo de Estudio</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Preguntas por día</label>
          <input type="number" id="questions-per-day" min="1" max="100" value="${rhythm.questions_per_day}" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Días de estudio por semana</label>
          <select id="days-per-week" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
            <option value="3" ${rhythm.days_per_week == 3 ? 'selected' : ''}>3 días</option>
            <option value="5" ${rhythm.days_per_week == 5 ? 'selected' : ''}>5 días</option>
            <option value="7" ${rhythm.days_per_week == 7 ? 'selected' : ''}>7 días (diario)</option>
          </select>
        </div>
      </div>
      <div class="flex gap-3 mt-6">
        <button onclick="this.closest('.fixed').remove()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button onclick="saveStudyRhythm()" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
          Guardar
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

  window.saveStudyRhythm = async function () {
    const questionsPerDay = parseInt(document.getElementById('questions-per-day').value);
    const daysPerWeek = parseInt(document.getElementById('days-per-week').value);

    try {
      await ensureUserProfile(user.id);
      const { error } = await supabaseClient
        .from('user_profiles')
        .update({
          study_rhythm: {
            questions_per_day: questionsPerDay,
            days_per_week: daysPerWeek,
            updated_at: new Date().toISOString()
          }
        })
        .eq('id', user.id);

      if (error) throw error;

      document.getElementById('current-rhythm').textContent = `${questionsPerDay} preguntas/${daysPerWeek} días`;
      showSuccessMessage('Ritmo de estudio guardado');
      modal.remove();
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al guardar');
    }
  };
};

// ===================================================================
// 7. RECORDATORIOS (Supabase)
// ===================================================================
window.configureReminders = async function () {
  const { data: { user } } = await getSupabase().auth.getUser();
  const { data: profile } = await supabaseClient
    .from('user_profiles')
    .select('notification_settings')
    .eq('id', user?.id)
    .single();

  const settings = profile?.notification_settings || {
    reminder_time: '09:00',
    review_reminders: true,
    progress_notifications: true
  };

  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Configurar Recordatorios</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Hora de recordatorio diario</label>
          <input type="time" id="reminder-time" value="${settings.reminder_time}" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700">Recordatorios de repaso</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" id="review-reminders" class="sr-only peer" ${settings.review_reminders ? 'checked' : ''}>
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-orange-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-orange-600"></div>
          </label>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700">Notificaciones de progreso</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" id="progress-notifications" class="sr-only peer" ${settings.progress_notifications ? 'checked' : ''}>
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-orange-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-orange-600"></div>
          </label>
        </div>
      </div>
      <div class="flex gap-3 mt-6">
        <button onclick="this.closest('.fixed').remove()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button onclick="saveReminders()" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
          Guardar
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

  window.saveReminders = async function () {
    const reminderTime = document.getElementById('reminder-time').value;
    const reviewReminders = document.getElementById('review-reminders').checked;
    const progressNotifications = document.getElementById('progress-notifications').checked;

    try {
      await ensureUserProfile(user.id);
      const { error } = await supabaseClient
        .from('user_profiles')
        .update({
          notification_settings: {
            reminder_time: reminderTime,
            review_reminders: reviewReminders,
            progress_notifications: progressNotifications,
            updated_at: new Date().toISOString()
          }
        })
        .eq('id', user.id);

      if (error) throw error;

      const statusEl = document.getElementById('reminder-status');
      const active = reviewReminders || progressNotifications;
      if (statusEl) {
        statusEl.textContent = active ? 'Activos' : 'Inactivos';
        statusEl.className = active ? 'text-green-600 font-medium' : 'text-red-600 font-medium';
      }

      showSuccessMessage('Recordatorios configurados');
      modal.remove();
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al guardar');
    }
  };
};

// ===================================================================
// 8. GESTIONAR NOTIFICACIONES (Supabase)
// ===================================================================
window.manageNotifications = async function () {
  // Redirigir a configureReminders ya que es la misma funcionalidad
  await window.configureReminders();
};

// ===================================================================
// 9. CAMBIAR IDIOMA (Supabase)
// ===================================================================
window.changeLanguage = async function () {
  const { data: { user } } = await getSupabase().auth.getUser();
  const { data: profile } = await supabaseClient
    .from('user_profiles')
    .select('language')
    .eq('id', user?.id)
    .single();

  const currentLang = profile?.language || 'es';

  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Cambiar Idioma</h3>
      <div class="space-y-3">
        <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50 ${currentLang === 'es' ? 'border-orange-500 bg-orange-50' : 'border-gray-200'}">
          <input type="radio" name="language" value="es" ${currentLang === 'es' ? 'checked' : ''} class="mr-3">
          <span class="mr-2">🇪🇸</span>
          <span>Español</span>
        </label>
        <label class="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50 ${currentLang === 'en' ? 'border-orange-500 bg-orange-50' : 'border-gray-200'}">
          <input type="radio" name="language" value="en" ${currentLang === 'en' ? 'checked' : ''} class="mr-3">
          <span class="mr-2">🇺🇸</span>
          <span>English</span>
        </label>
      </div>
      <div class="flex gap-3 mt-6">
        <button onclick="this.closest('.fixed').remove()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button onclick="saveLanguage()" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
          Guardar
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

  window.saveLanguage = async function () {
    const selectedLang = document.querySelector('input[name="language"]:checked')?.value;
    if (!selectedLang) return;

    try {
      await ensureUserProfile(user.id);
      const { error } = await supabaseClient
        .from('user_profiles')
        .update({ language: selectedLang })
        .eq('id', user.id);

      if (error) throw error;

      showSuccessMessage(`Idioma cambiado a: ${selectedLang === 'es' ? 'Español' : 'English'}`);
      modal.remove();
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al guardar');
    }
  };
};

// ===================================================================
// 10. EXPORTAR DATOS (Supabase)
// ===================================================================
window.exportData = async function () {
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Exportar Datos</h3>
      <p class="text-gray-600 mb-4">Selecciona el formato para descargar tus datos:</p>
      <div class="space-y-3">
        <button onclick="exportToFormat('json')" class="w-full text-left p-3 rounded-lg hover:bg-gray-100 transition-colors border border-gray-200 flex items-center gap-3">
          <span class="material-symbols-outlined text-blue-600">code</span>
          <div>
            <div class="font-medium text-gray-800">JSON</div>
            <div class="text-sm text-gray-600">Formato estructurado para programadores</div>
          </div>
        </button>
        <button onclick="exportToFormat('csv')" class="w-full text-left p-3 rounded-lg hover:bg-gray-100 transition-colors border border-gray-200 flex items-center gap-3">
          <span class="material-symbols-outlined text-green-600">table_chart</span>
          <div>
            <div class="font-medium text-gray-800">CSV</div>
            <div class="text-sm text-gray-600">Compatible con Excel y Google Sheets</div>
          </div>
        </button>
      </div>
      <div class="flex justify-end mt-6">
        <button onclick="this.closest('.fixed').remove()" class="px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);
  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });

  window.exportToFormat = async function (format) {
    try {
      console.log(`📥 Exportando datos en formato ${format}...`);

      const materials = await SupabaseOperations.getMaterials();
      const allQuestions = [];

      for (const material of materials) {
        const questions = await SupabaseOperations.getQuestionsByMaterial(material.id);
        for (const question of questions) {
          const answers = await SupabaseOperations.getAnswersByQuestion(question.id);
          const lastAnswer = answers[0];
          if (lastAnswer) {
            allQuestions.push({
              material: material.title,
              pregunta: question.question_text,
              respuesta: lastAnswer.answer_text,
              score: lastAnswer.score,
              clasificacion: lastAnswer.classification,
              fecha: new Date(lastAnswer.created_at).toLocaleString('es-ES')
            });
          }
        }
      }

      if (allQuestions.length === 0) {
        showErrorMessage('No tienes preguntas para exportar');
        modal.remove();
        return;
      }

      let fileContent, fileName, mimeType;

      if (format === 'json') {
        fileContent = JSON.stringify(allQuestions, null, 2);
        fileName = `recuiva_datos_${new Date().toISOString().split('T')[0]}.json`;
        mimeType = 'application/json';
      } else {
        const headers = ['Material', 'Pregunta', 'Respuesta', 'Score', 'Clasificación', 'Fecha'];
        const rows = allQuestions.map(q => [
          q.material,
          `"${q.pregunta.replace(/"/g, '""')}"`,
          `"${q.respuesta.replace(/"/g, '""')}"`,
          q.score,
          q.clasificacion,
          q.fecha
        ]);
        fileContent = [headers, ...rows].map(row => row.join(',')).join('\n');
        fileName = `recuiva_datos_${new Date().toISOString().split('T')[0]}.csv`;
        mimeType = 'text/csv;charset=utf-8;';
      }

      const blob = new Blob([fileContent], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      showSuccessMessage(`Datos exportados correctamente (${allQuestions.length} preguntas)`);
      modal.remove();
    } catch (error) {
      console.error('❌ Error exportando:', error);
      showErrorMessage('Error al exportar datos');
    }
  };
};

// ===================================================================
// FUNCIONES AUXILIARES
// ===================================================================

// Asegurar que existe el perfil del usuario
async function ensureUserProfile(userId) {
  const { data, error } = await supabaseClient
    .from('user_profiles')
    .select('id')
    .eq('id', userId)
    .single();

  if (error && error.code === 'PGRST116') {
    // No existe, crear
    await supabaseClient
      .from('user_profiles')
      .insert([{ id: userId }]);
  }
}

// Modal de edición genérico
function showEditModal(title, label, currentValue, onSave) {
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">${title}</h3>
      <div class="mb-4">
        <label class="block text-sm font-medium text-gray-700 mb-2">${label}</label>
        <input type="text" id="edit-input" value="${currentValue}" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500 focus:border-transparent">
      </div>
      <div class="flex gap-3">
        <button onclick="this.closest('.fixed').remove()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button id="save-btn" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
          Guardar
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(modal);

  const input = document.getElementById('edit-input');
  input.focus();
  input.select();

  document.getElementById('save-btn').onclick = () => {
    onSave(input.value);
    modal.remove();
  };

  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      onSave(input.value);
      modal.remove();
    }
  });

  modal.addEventListener('click', (e) => { if (e.target === modal) modal.remove(); });
}

// Mensajes de éxito
function showSuccessMessage(message) {
  const toast = document.createElement('div');
  toast.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2';
  toast.innerHTML = `
    <span class="material-symbols-outlined">check_circle</span>
    <span>${message}</span>
  `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s';
    toast.style.opacity = '0';
    setTimeout(() => document.body.removeChild(toast), 300);
  }, 3000);
}

// Mensajes de error
function showErrorMessage(message) {
  const toast = document.createElement('div');
  toast.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2';
  toast.innerHTML = `
    <span class="material-symbols-outlined">error</span>
    <span>${message}</span>
  `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.transition = 'opacity 0.3s';
    toast.style.opacity = '0';
    setTimeout(() => document.body.removeChild(toast), 300);
  }, 3000);
}

console.log('✅ Mi Perfil Functions (Supabase) cargado');
