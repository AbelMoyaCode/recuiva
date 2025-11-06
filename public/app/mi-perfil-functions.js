// ===================================================================
// MI PERFIL - FUNCIONES COMPLETAS CON SUPABASE
// ===================================================================

// ===================================================================
// 1. CAMBIAR FOTO DE PERFIL (Supabase Storage)
// ===================================================================
window.changeProfilePicture = async function() {
  const fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.accept = 'image/jpeg,image/png,image/webp';
  
  fileInput.onchange = async function(e) {
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
      reader.onload = function(e) {
        const profileImg = document.getElementById('profile-image');
        if (profileImg) profileImg.src = e.target.result;
      };
      reader.readAsDataURL(file);
      
      // Obtener usuario actual
      const { data: { user } } = await _supabaseClient.auth.getUser();
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
      const { data, error } = await _supabaseClient.storage
        .from('avatars')
        .upload(filePath, file, {
          cacheControl: '3600',
          upsert: false
        });
      
      if (error) {
        console.error('❌ Error subiendo foto:', error);
        showErrorMessage('Error al subir la foto: ' + error.message);
        return;
      }
      
      // Obtener URL pública
      const { data: { publicUrl } } = _supabaseClient.storage
        .from('avatars')
        .getPublicUrl(filePath);
      
      console.log('✅ Foto subida, URL:', publicUrl);
      
      // Actualizar user_profiles
      const { error: updateError } = await _supabaseClient
        .from('user_profiles')
        .update({ avatar_url: publicUrl })
        .eq('user_id', user.id);
      
      if (updateError) {
        console.error('❌ Error actualizando perfil:', updateError);
        showErrorMessage('Error al actualizar perfil');
        return;
      }
      
      console.log('✅ Perfil actualizado con nueva foto');
      showSuccessMessage('Foto de perfil actualizada correctamente');
      
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
// 2. CAMBIAR CONTRASEÑA (Supabase Auth)
// ===================================================================
window.changePassword = async function() {
  // Verificar si es cuenta de Gmail
  const { data: { user } } = await _supabaseClient.auth.getUser();
  
  if (user && user.app_metadata.provider === 'google') {
    showGmailPasswordModal();
    return;
  }
  
  // Mostrar modal de cambio de contraseña
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
          <button type="button" onclick="closePasswordModal()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
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
  
  window.closePasswordModal = function() {
    document.body.removeChild(modal);
  };
  
  // Manejar submit
  document.getElementById('password-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const newPassword = document.getElementById('new-password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    if (newPassword !== confirmPassword) {
      showErrorMessage('Las contraseñas no coinciden');
      return;
    }
    
    if (newPassword.length < 6) {
      showErrorMessage('La contraseña debe tener al menos 6 caracteres');
      return;
    }
    
    try {
      console.log('🔐 Actualizando contraseña...');
      
      const { error } = await _supabaseClient.auth.updateUser({
        password: newPassword
      });
      
      if (error) {
        console.error('❌ Error:', error);
        showErrorMessage('Error al cambiar contraseña: ' + error.message);
        return;
      }
      
      console.log('✅ Contraseña actualizada');
      showSuccessMessage('Contraseña cambiada correctamente');
      closePasswordModal();
      
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al cambiar contraseña');
    }
  });
  
  // Cerrar con Escape
  modal.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closePasswordModal();
  });
  
  modal.addEventListener('click', function(e) {
    if (e.target === modal) closePasswordModal();
  });
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
          <button onclick="closeGmailPasswordModal()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
            Cerrar
          </button>
          <button onclick="openGoogleAccount()" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
            Ir a Google
          </button>
        </div>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  window.closeGmailPasswordModal = function() {
    document.body.removeChild(modal);
  };
  
  window.openGoogleAccount = function() {
    window.open('https://myaccount.google.com/security', '_blank');
    document.body.removeChild(modal);
  };
}

// ===================================================================
// 3. EXPORTAR DATOS (Excel, JSON, CSV)
// ===================================================================
window.exportData = async function() {
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
        <button onclick="exportToFormat('excel')" class="w-full text-left p-3 rounded-lg hover:bg-gray-100 transition-colors border border-gray-200 flex items-center gap-3">
          <span class="material-symbols-outlined text-orange-600">description</span>
          <div>
            <div class="font-medium text-gray-800">Excel</div>
            <div class="text-sm text-gray-600">Archivo .xlsx con formato</div>
          </div>
        </button>
      </div>
      <div class="flex justify-end gap-3 mt-6">
        <button onclick="closeExportModal()" class="px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  window.closeExportModal = function() {
    document.body.removeChild(modal);
  };
  
  window.exportToFormat = async function(format) {
    try {
      console.log(`📥 Exportando datos en formato ${format}...`);
      
      // Obtener todos los datos del usuario
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
        closeExportModal();
        return;
      }
      
      let fileContent, fileName, mimeType;
      
      if (format === 'json') {
        // JSON
        fileContent = JSON.stringify(allQuestions, null, 2);
        fileName = `recuiva_datos_${new Date().toISOString().split('T')[0]}.json`;
        mimeType = 'application/json';
        
      } else if (format === 'csv') {
        // CSV
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
        
      } else if (format === 'excel') {
        // Excel (usando formato HTML que Excel puede abrir)
        let html = `
          <html>
          <head><meta charset='utf-8'></head>
          <body>
          <table border='1'>
            <tr>
              <th>Material</th>
              <th>Pregunta</th>
              <th>Respuesta</th>
              <th>Score</th>
              <th>Clasificación</th>
              <th>Fecha</th>
            </tr>
        `;
        
        allQuestions.forEach(q => {
          html += `
            <tr>
              <td>${q.material}</td>
              <td>${q.pregunta}</td>
              <td>${q.respuesta}</td>
              <td>${q.score}</td>
              <td>${q.clasificacion}</td>
              <td>${q.fecha}</td>
            </tr>
          `;
        });
        
        html += '</table></body></html>';
        fileContent = html;
        fileName = `recuiva_datos_${new Date().toISOString().split('T')[0]}.xls`;
        mimeType = 'application/vnd.ms-excel';
      }
      
      // Crear y descargar archivo
      const blob = new Blob([fileContent], { type: mimeType });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
      
      console.log(`✅ Archivo ${fileName} descargado`);
      showSuccessMessage(`Datos exportados correctamente (${allQuestions.length} preguntas)`);
      closeExportModal();
      
    } catch (error) {
      console.error('❌ Error exportando:', error);
      showErrorMessage('Error al exportar datos');
    }
  };
};

// ===================================================================
// 4. RITMO DE ESTUDIO (Guardar en user_profiles)
// ===================================================================
window.showStudyRhythmModal = async function() {
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Configurar Ritmo de Estudio</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Preguntas por día</label>
          <input type="number" id="questions-per-day" min="1" max="100" value="10" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Días de estudio por semana</label>
          <select id="days-per-week" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
            <option value="3">3 días</option>
            <option value="5" selected>5 días</option>
            <option value="7">7 días (diario)</option>
          </select>
        </div>
      </div>
      <div class="flex gap-3 mt-6">
        <button onclick="closeStudyRhythmModal()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button onclick="saveStudyRhythm()" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
          Guardar
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  window.closeStudyRhythmModal = function() {
    document.body.removeChild(modal);
  };
  
  window.saveStudyRhythm = async function() {
    const questionsPerDay = document.getElementById('questions-per-day').value;
    const daysPerWeek = document.getElementById('days-per-week').value;
    
    try {
      const { data: { user } } = await _supabaseClient.auth.getUser();
      
      const studyRhythm = {
        questions_per_day: parseInt(questionsPerDay),
        days_per_week: parseInt(daysPerWeek),
        updated_at: new Date().toISOString()
      };
      
      const { error } = await _supabaseClient
        .from('user_profiles')
        .update({ study_rhythm: studyRhythm })
        .eq('user_id', user.id);
      
      if (error) throw error;
      
      document.getElementById('current-rhythm').textContent = `${questionsPerDay} preguntas/${daysPerWeek} días`;
      showSuccessMessage('Ritmo de estudio guardado');
      closeStudyRhythmModal();
      
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al guardar configuración');
    }
  };
};

// ===================================================================
// 5. RECORDATORIOS (Configurar notificaciones)
// ===================================================================
window.configureReminders = async function() {
  const modal = document.createElement('div');
  modal.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
  modal.innerHTML = `
    <div class="bg-white rounded-lg p-6 w-96 max-w-md mx-4">
      <h3 class="text-lg font-semibold mb-4 text-gray-800">Configurar Recordatorios</h3>
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Hora de recordatorio diario</label>
          <input type="time" id="reminder-time" value="09:00" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-500">
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700">Recordatorios de repaso</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" id="review-reminders" class="sr-only peer" checked>
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-orange-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-orange-600"></div>
          </label>
        </div>
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700">Notificaciones de progreso</span>
          <label class="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" id="progress-notifications" class="sr-only peer" checked>
            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-orange-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-orange-600"></div>
          </label>
        </div>
      </div>
      <div class="flex gap-3 mt-6">
        <button onclick="closeRemindersModal()" class="flex-1 px-4 py-2 text-gray-600 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors">
          Cancelar
        </button>
        <button onclick="saveReminders()" class="flex-1 px-4 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 transition-colors">
          Guardar
        </button>
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  window.closeRemindersModal = function() {
    document.body.removeChild(modal);
  };
  
  window.saveReminders = async function() {
    const reminderTime = document.getElementById('reminder-time').value;
    const reviewReminders = document.getElementById('review-reminders').checked;
    const progressNotifications = document.getElementById('progress-notifications').checked;
    
    try {
      const { data: { user } } = await _supabaseClient.auth.getUser();
      
      const notificationSettings = {
        reminder_time: reminderTime,
        review_reminders: reviewReminders,
        progress_notifications: progressNotifications,
        updated_at: new Date().toISOString()
      };
      
      const { error } = await _supabaseClient
        .from('user_profiles')
        .update({ notification_settings: notificationSettings })
        .eq('user_id', user.id);
      
      if (error) throw error;
      
      document.getElementById('reminder-status').textContent = reviewReminders || progressNotifications ? 'Activos' : 'Desactivados';
      showSuccessMessage('Recordatorios configurados');
      closeRemindersModal();
      
    } catch (error) {
      console.error('❌ Error:', error);
      showErrorMessage('Error al guardar recordatorios');
    }
  };
};

// ===================================================================
// MENSAJES DE ÉXITO/ERROR
// ===================================================================
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

console.log('✅ Mi Perfil Functions cargado');
