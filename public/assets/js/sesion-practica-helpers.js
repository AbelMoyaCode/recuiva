// ===================================================================
// FUNCIONES CRÍTICAS QUE DEBEN ESTAR DISPONIBLES ANTES DEL HTML
// ===================================================================

// ⚡ FUNCIÓN CRÍTICA: window.checkValidateButton
window.checkValidateButton = function() {
  const questionInput = document.getElementById('user-question');
  const userAnswer = document.getElementById('user-answer');
  const btnValidate = document.getElementById('btn-validate-answer');
  const btnGenerate = document.getElementById('btn-generate-questions'); // 🆕 Botón de generar preguntas
  const statusDiv = document.getElementById('button-status');
  
  if (!questionInput || !userAnswer || !btnValidate) {
    console.warn('⚠️ Elementos no encontrados (aún no cargados)');
    return;
  }
  
  // LÓGICA SIMPLE: Solo requiere 1 carácter mínimo en cada campo
  const questionLength = questionInput.value.trim().length;
  const answerLength = userAnswer.value.trim().length;
  const hasQuestion = questionLength >= 1;
  const hasAnswer = answerLength >= 1;
  
  console.log('📝 Pregunta:', questionLength, 'chars');
  console.log('✍️ Respuesta:', answerLength, 'chars');
  
  // ✅ HABILITAR/DESHABILITAR TEXTAREA DE RESPUESTA según si hay pregunta
  if (hasQuestion) {
    if (userAnswer.disabled) {
      console.log('✅ Habilitando textarea de respuesta (hay pregunta)');
      userAnswer.disabled = false;
      userAnswer.classList.remove('opacity-50', 'cursor-not-allowed', 'bg-gray-100');
      userAnswer.classList.add('bg-white');
    }
  } else {
    if (!userAnswer.disabled) {
      console.log('❌ Deshabilitando textarea de respuesta (no hay pregunta)');
      userAnswer.disabled = true;
      userAnswer.classList.add('opacity-50', 'cursor-not-allowed', 'bg-gray-100');
      userAnswer.classList.remove('bg-white');
    }
  }
  
  // =========================================================================
  // 🆕 CORRECCIÓN PROFESOR SEMANA 15: Deshabilitar botón "Generar Preguntas"
  // cuando el usuario empieza a escribir en el campo de PREGUNTA.
  // Lógica: Si ya escribiste tu propia pregunta, no tiene sentido generar una automática.
  // =========================================================================
  if (btnGenerate) {
    // 🔒 NO interferir si el botón está en proceso de generación (tiene "Generando..." en innerHTML)
    const isGenerating = btnGenerate.innerHTML.includes('Generando') || btnGenerate.innerHTML.includes('progress_activity');
    
    if (!isGenerating) {
      if (hasQuestion) {
        // Si el usuario ya escribió algo en PREGUNTA → DESHABILITAR generar
        console.log('🔒 DESHABILITANDO botón "Generar Preguntas" (usuario ya tiene pregunta escrita)');
        btnGenerate.disabled = true;
        btnGenerate.classList.add('opacity-50', 'cursor-not-allowed');
        btnGenerate.classList.remove('hover:from-green-600', 'hover:to-emerald-700', 'hover:shadow-xl', 'hover:scale-105');
        btnGenerate.title = 'Ya tienes una pregunta escrita. Bórrala si quieres generar una automáticamente.';
      } else {
        // Si el campo de PREGUNTA está vacío → HABILITAR generar
        console.log('✅ Habilitando botón "Generar Preguntas" (campo pregunta vacío)');
        btnGenerate.disabled = false;
        btnGenerate.classList.remove('opacity-50', 'cursor-not-allowed');
        btnGenerate.classList.add('hover:from-green-600', 'hover:to-emerald-700', 'hover:shadow-xl', 'hover:scale-105');
        btnGenerate.title = 'Genera una nueva pregunta automáticamente basada en tu material';
      }
    }
  }
  
  if (hasQuestion && hasAnswer) {
    console.log('✅ HABILITANDO BOTÓN');
    
    btnValidate.disabled = false;
    btnValidate.classList.remove('opacity-50', 'cursor-not-allowed');
    btnValidate.classList.add('hover:bg-green-700', 'hover:shadow-xl', 'hover:-translate-y-0.5');
    
    // Actualizar estado visual
    if (statusDiv) {
      statusDiv.className = 'mt-3 px-4 py-2 rounded-lg border-2 bg-green-50 border-green-200 text-green-700 font-semibold text-sm flex items-center gap-2';
      statusDiv.innerHTML = '<span class="material-symbols-outlined text-lg">check_circle</span><span>✅ Botón HABILITADO (puedes validar)</span>';
    }
  } else {
    console.log('❌ DESHABILITANDO BOTÓN');
    
    btnValidate.disabled = true;
    btnValidate.classList.add('opacity-50', 'cursor-not-allowed');
    btnValidate.classList.remove('hover:bg-green-700', 'hover:shadow-xl', 'hover:-translate-y-0.5');
    
    // Actualizar estado visual
    if (statusDiv) {
      statusDiv.className = 'mt-3 px-4 py-2 rounded-lg border-2 bg-red-50 border-red-200 text-red-700 font-semibold text-sm flex items-center gap-2';
      statusDiv.innerHTML = '<span class="material-symbols-outlined text-lg">cancel</span><span>❌ Botón DESHABILITADO (escribe en ambos campos)</span>';
    }
  }
};

console.log('✅ window.checkValidateButton definida y lista (con control de generar preguntas)');

// ⚡ FUNCIÓN: window.updateCharCount - Contador de caracteres
window.updateCharCount = function(textarea) {
  const charCount = textarea.value.trim().length;
  const charCountEl = document.getElementById('char-count');
  
  if (charCountEl) {
    charCountEl.textContent = `${charCount} caracteres`;
    
    if (charCount >= 30) {
      charCountEl.classList.remove('text-gray-500');
      charCountEl.classList.add('text-green-600', 'font-semibold');
    } else {
      charCountEl.classList.remove('text-green-600', 'font-semibold');
      charCountEl.classList.add('text-gray-500');
    }
  }
  
  // También llamar a checkValidateButton
  if (typeof window.checkValidateButton === 'function') {
    window.checkValidateButton();
  }
};

console.log('✅ window.updateCharCount definida y lista');
