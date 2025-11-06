/**
 * MODAL DE REGISTRO EXITOSO CON ANIMACIÓN
 * Sistema modular para mostrar confirmaciones elegantes
 */

window.showSuccessModal = function({
  title = '¡Registro exitoso!',
  message = 'Tu cuenta ha sido creada correctamente.',
  icon = 'check_circle',
  buttonText = 'Continuar',
  onClose = null,
  redirectUrl = null,
  autoRedirect = true,
  delay = 2000
} = {}) {

  // Crear modal si no existe
  let modal = document.getElementById('success-modal');

  if (!modal) {
    modal = document.createElement('div');
    modal.id = 'success-modal';
    modal.className = 'fixed inset-0 bg-black bg-opacity-60 backdrop-blur-sm flex items-center justify-center z-[9999] opacity-0 transition-opacity duration-500';
    modal.innerHTML = `
      <div id="success-modal-content" class="bg-white rounded-3xl shadow-2xl p-8 max-w-md mx-4 transform scale-75 opacity-0 transition-all duration-500">
        <!-- Logo Animado -->
        <div class="flex justify-center mb-6">
          <div class="relative">
            <!-- Círculos de fondo animados -->
            <div class="absolute inset-0 rounded-full bg-gradient-to-r from-orange-500 to-blue-700 animate-ping opacity-20"></div>
            <div class="absolute inset-0 rounded-full bg-gradient-to-r from-orange-500 to-blue-700 animate-pulse opacity-30"></div>
            <!-- Logo -->
            <div class="relative w-24 h-24 rounded-full bg-gradient-to-br from-orange-500 to-blue-700 flex items-center justify-center shadow-lg transform transition-transform hover:scale-110 hover:rotate-12">
              <img id="success-logo"
                   src="../../assets/img/Icon-Recuiva.png"
                   alt="Logo Recuiva"
                   class="w-16 h-16 object-contain animate-bounce"
                   style="animation-duration: 1s; animation-iteration-count: 3;" />
            </div>
          </div>
        </div>

        <!-- Icono de éxito -->
        <div class="flex justify-center mb-4">
          <div class="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center animate-scale-in">
            <span id="success-icon" class="material-symbols-outlined text-5xl text-green-600 animate-check">
              check_circle
            </span>
          </div>
        </div>

        <!-- Título -->
        <h3 id="success-title" class="text-2xl font-bold text-center text-gray-900 mb-3">
          ¡Registro exitoso!
        </h3>

        <!-- Mensaje -->
        <p id="success-message" class="text-center text-gray-600 mb-6">
          Tu cuenta ha sido creada correctamente.
        </p>

        <!-- Barra de progreso (solo si hay redirect) -->
        <div id="success-progress-container" class="hidden mb-6">
          <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div id="success-progress-bar" class="h-full bg-gradient-to-r from-orange-500 to-blue-700 transition-all duration-100" style="width: 0%"></div>
          </div>
          <p class="text-center text-sm text-gray-500 mt-2">
            Redirigiendo en <span id="success-countdown"></span> segundos...
          </p>
        </div>

        <!-- Botón -->
        <button
          id="success-btn"
          onclick="window.closeSuccessModal()"
          class="w-full bg-gradient-to-r from-orange-500 to-blue-700 text-white font-bold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300">
          Continuar
        </button>
      </div>
    `;

    document.body.appendChild(modal);
  }

  // Actualizar contenido
  document.getElementById('success-icon').textContent = icon;
  document.getElementById('success-title').textContent = title;
  document.getElementById('success-message').textContent = message;
  document.getElementById('success-btn').textContent = buttonText;

  // Mostrar modal con animación
  requestAnimationFrame(() => {
    modal.classList.remove('opacity-0');
    setTimeout(() => {
      const content = document.getElementById('success-modal-content');
      content.classList.remove('scale-75', 'opacity-0');
      content.classList.add('scale-100', 'opacity-100');
    }, 100);
  });

  // Configurar redirección automática
  if (autoRedirect && redirectUrl) {
    const progressContainer = document.getElementById('success-progress-container');
    const progressBar = document.getElementById('success-progress-bar');
    const countdown = document.getElementById('success-countdown');

    progressContainer.classList.remove('hidden');

    const totalTime = delay;
    const interval = 100;
    let elapsed = 0;

    const timer = setInterval(() => {
      elapsed += interval;
      const progress = (elapsed / totalTime) * 100;
      progressBar.style.width = `${progress}%`;

      const secondsLeft = Math.ceil((totalTime - elapsed) / 1000);
      countdown.textContent = secondsLeft;

      if (elapsed >= totalTime) {
        clearInterval(timer);
        window.location.href = redirectUrl;
      }
    }, interval);

    // Permitir cancelar redirección
    window.closeSuccessModal = function() {
      clearInterval(timer);
      closeModal();
      if (onClose) onClose();
    };
  } else {
    // Sin redirección automática
    window.closeSuccessModal = function() {
      closeModal();
      if (redirectUrl) {
        window.location.href = redirectUrl;
      } else if (onClose) {
        onClose();
      }
    };
  }

  function closeModal() {
    const content = document.getElementById('success-modal-content');
    content.classList.add('scale-75', 'opacity-0');
    content.classList.remove('scale-100', 'opacity-100');

    setTimeout(() => {
      modal.classList.add('opacity-0');
      setTimeout(() => {
        modal.remove();
      }, 500);
    }, 200);
  }

  // Cerrar con ESC
  const handleEsc = (e) => {
    if (e.key === 'Escape') {
      window.closeSuccessModal();
      document.removeEventListener('keydown', handleEsc);
    }
  };
  document.addEventListener('keydown', handleEsc);
};

// ==========================================
// MODAL DE ERROR (compatibilidad)
// ==========================================

window.showErrorModal = function(message, callback) {
  showSuccessModal({
    title: '❌ Error',
    message: message || 'Ha ocurrido un error',
    icon: 'error',
    buttonText: 'Cerrar',
    onClose: callback,
    autoRedirect: false
  });
};

// ==========================================
// MODAL DE CONFIRMACIÓN
// ==========================================

window.showConfirmModal = function(message, onConfirm, onCancel) {
  showSuccessModal({
    title: '❓ Confirmación',
    message: message,
    icon: 'help',
    buttonText: 'Confirmar',
    onClose: onConfirm,
    autoRedirect: false
  });
};

// ==========================================
// ESTILOS ANIMADOS
// ==========================================

const successModalStyles = `
<style id="success-modal-styles">
@keyframes scale-in {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes check-animation {
  0% {
    transform: scale(0) rotate(0deg);
  }
  50% {
    transform: scale(1.2) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
  }
}

.animate-scale-in {
  animation: scale-in 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.animate-check {
  animation: check-animation 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s backwards;
}

#success-modal {
  transition: opacity 0.5s ease;
}

#success-modal-content {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}
</style>
`;

// Insertar estilos si no existen
if (!document.getElementById('success-modal-styles')) {
  document.head.insertAdjacentHTML('beforeend', successModalStyles);
}
