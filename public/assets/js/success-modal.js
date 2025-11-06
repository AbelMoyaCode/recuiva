/**
 * Módulo de modales de éxito y error para RECUIVA
 * Proporciona funciones para mostrar notificaciones al usuario
 */

/**
 * Muestra un modal de éxito con un mensaje personalizado
 * @param {string} message - Mensaje a mostrar en el modal
 * @param {function} callback - Función opcional a ejecutar después de cerrar el modal
 */
function showSuccessModal(message, callback) {
    // Crear el modal si no existe
    let modal = document.getElementById('success-modal');
    
    if (!modal) {
        modal = createModal('success-modal', 'success');
    }
    
    // Establecer el mensaje
    const messageElement = modal.querySelector('.modal-message');
    if (messageElement) {
        messageElement.textContent = message || '✅ Operación completada exitosamente';
    }
    
    // Mostrar el modal
    modal.style.display = 'flex';
    modal.classList.add('show');
    
    // Configurar el cierre
    const closeBtn = modal.querySelector('.modal-close-btn');
    const confirmBtn = modal.querySelector('.modal-confirm-btn');
    
    const closeModal = () => {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
        
        if (typeof callback === 'function') {
            callback();
        }
    };
    
    if (closeBtn) {
        closeBtn.onclick = closeModal;
    }
    
    if (confirmBtn) {
        confirmBtn.onclick = closeModal;
    }
    
    // Cerrar al hacer clic fuera del modal
    modal.onclick = (e) => {
        if (e.target === modal) {
            closeModal();
        }
    };
    
    // Auto-cerrar después de 5 segundos
    setTimeout(closeModal, 5000);
}

/**
 * Muestra un modal de error con un mensaje personalizado
 * @param {string} message - Mensaje de error a mostrar
 * @param {function} callback - Función opcional a ejecutar después de cerrar el modal
 */
function showErrorModal(message, callback) {
    // Crear el modal si no existe
    let modal = document.getElementById('error-modal');
    
    if (!modal) {
        modal = createModal('error-modal', 'error');
    }
    
    // Establecer el mensaje
    const messageElement = modal.querySelector('.modal-message');
    if (messageElement) {
        messageElement.textContent = message || '❌ Ha ocurrido un error';
    }
    
    // Mostrar el modal
    modal.style.display = 'flex';
    modal.classList.add('show');
    
    // Configurar el cierre
    const closeBtn = modal.querySelector('.modal-close-btn');
    const confirmBtn = modal.querySelector('.modal-confirm-btn');
    
    const closeModal = () => {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300);
        
        if (typeof callback === 'function') {
            callback();
        }
    };
    
    if (closeBtn) {
        closeBtn.onclick = closeModal;
    }
    
    if (confirmBtn) {
        confirmBtn.onclick = closeModal;
    }
    
    // Cerrar al hacer clic fuera del modal
    modal.onclick = (e) => {
        if (e.target === modal) {
            closeModal();
        }
    };
}

/**
 * Crea dinámicamente un modal en el DOM
 * @param {string} id - ID del modal
 * @param {string} type - Tipo de modal ('success' o 'error')
 * @returns {HTMLElement} - El elemento modal creado
 */
function createModal(id, type) {
    const modal = document.createElement('div');
    modal.id = id;
    modal.className = 'modal-overlay';
    
    const isSuccess = type === 'success';
    const icon = isSuccess ? '✅' : '❌';
    const title = isSuccess ? '¡Éxito!' : 'Error';
    const buttonClass = isSuccess ? 'success' : 'error';
    
    modal.innerHTML = `
        <div class="modal-content ${type}">
            <div class="modal-header">
                <span class="modal-icon">${icon}</span>
                <h2 class="modal-title">${title}</h2>
                <button class="modal-close-btn" aria-label="Cerrar">&times;</button>
            </div>
            <div class="modal-body">
                <p class="modal-message"></p>
            </div>
            <div class="modal-footer">
                <button class="modal-confirm-btn btn-${buttonClass}">Aceptar</button>
            </div>
        </div>
    `;
    
    // Agregar estilos si no existen
    if (!document.getElementById('modal-styles')) {
        const style = document.createElement('style');
        style.id = 'modal-styles';
        style.textContent = `
            .modal-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                justify-content: center;
                align-items: center;
                z-index: 9999;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .modal-overlay.show {
                opacity: 1;
            }
            
            .modal-content {
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                max-width: 500px;
                width: 90%;
                max-height: 90vh;
                overflow-y: auto;
                transform: scale(0.7);
                transition: transform 0.3s ease;
            }
            
            .modal-overlay.show .modal-content {
                transform: scale(1);
            }
            
            .modal-content.success {
                border-top: 4px solid #10b981;
            }
            
            .modal-content.error {
                border-top: 4px solid #ef4444;
            }
            
            .modal-header {
                display: flex;
                align-items: center;
                padding: 20px 24px;
                border-bottom: 1px solid #e5e7eb;
                position: relative;
            }
            
            .modal-icon {
                font-size: 32px;
                margin-right: 12px;
            }
            
            .modal-title {
                flex: 1;
                font-size: 20px;
                font-weight: 600;
                color: #1f2937;
                margin: 0;
            }
            
            .modal-close-btn {
                position: absolute;
                top: 20px;
                right: 20px;
                background: none;
                border: none;
                font-size: 28px;
                color: #6b7280;
                cursor: pointer;
                padding: 0;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 6px;
                transition: all 0.2s ease;
            }
            
            .modal-close-btn:hover {
                background-color: #f3f4f6;
                color: #1f2937;
            }
            
            .modal-body {
                padding: 24px;
            }
            
            .modal-message {
                font-size: 16px;
                color: #4b5563;
                line-height: 1.6;
                margin: 0;
            }
            
            .modal-footer {
                padding: 16px 24px;
                border-top: 1px solid #e5e7eb;
                display: flex;
                justify-content: flex-end;
                gap: 12px;
            }
            
            .modal-confirm-btn {
                padding: 10px 24px;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                color: white;
            }
            
            .btn-success {
                background-color: #10b981;
            }
            
            .btn-success:hover {
                background-color: #059669;
            }
            
            .btn-error {
                background-color: #ef4444;
            }
            
            .btn-error:hover {
                background-color: #dc2626;
            }
            
            @media (max-width: 640px) {
                .modal-content {
                    width: 95%;
                    margin: 20px;
                }
                
                .modal-header {
                    padding: 16px;
                }
                
                .modal-body {
                    padding: 20px 16px;
                }
                
                .modal-footer {
                    padding: 12px 16px;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(modal);
    return modal;
}

/**
 * Muestra un modal de confirmación con opciones de confirmar/cancelar
 * @param {string} message - Mensaje a mostrar
 * @param {function} onConfirm - Función a ejecutar al confirmar
 * @param {function} onCancel - Función opcional a ejecutar al cancelar
 */
function showConfirmModal(message, onConfirm, onCancel) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay show';
    modal.style.display = 'flex';
    
    modal.innerHTML = `
        <div class="modal-content">
            <div class="modal-header">
                <span class="modal-icon">❓</span>
                <h2 class="modal-title">Confirmación</h2>
                <button class="modal-close-btn" aria-label="Cerrar">&times;</button>
            </div>
            <div class="modal-body">
                <p class="modal-message">${message}</p>
            </div>
            <div class="modal-footer">
                <button class="modal-cancel-btn">Cancelar</button>
                <button class="modal-confirm-btn btn-success">Confirmar</button>
            </div>
        </div>
    `;
    
    // Agregar estilos para botón cancelar si no existen
    const cancelBtnStyle = `
        .modal-cancel-btn {
            padding: 10px 24px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            background-color: white;
            color: #6b7280;
        }
        
        .modal-cancel-btn:hover {
            background-color: #f3f4f6;
            border-color: #9ca3af;
        }
    `;
    
    if (!document.getElementById('confirm-modal-styles')) {
        const style = document.createElement('style');
        style.id = 'confirm-modal-styles';
        style.textContent = cancelBtnStyle;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(modal);
    
    const closeModal = () => {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    };
    
    modal.querySelector('.modal-close-btn').onclick = () => {
        closeModal();
        if (typeof onCancel === 'function') {
            onCancel();
        }
    };
    
    modal.querySelector('.modal-cancel-btn').onclick = () => {
        closeModal();
        if (typeof onCancel === 'function') {
            onCancel();
        }
    };
    
    modal.querySelector('.modal-confirm-btn').onclick = () => {
        closeModal();
        if (typeof onConfirm === 'function') {
            onConfirm();
        }
    };
    
    modal.onclick = (e) => {
        if (e.target === modal) {
            closeModal();
            if (typeof onCancel === 'function') {
                onCancel();
            }
        }
    };
}

// Exportar funciones globalmente
window.showSuccessModal = showSuccessModal;
window.showErrorModal = showErrorModal;
window.showConfirmModal = showConfirmModal;
