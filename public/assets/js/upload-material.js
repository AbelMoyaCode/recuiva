/**
 * Script para la página de subir materiales
 * Maneja el upload de PDF/TXT y muestra el progreso
 * 
 * Autor: Abel Jesús Moya Acosta
 * Usar en: src/pages/subir-material.html
 */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('📤 Inicializando módulo de subida de materiales...');

    // Verificar conexión con backend
    const isConnected = await api.checkConnection();
    
    if (!isConnected) {
        const container = document.querySelector('.upload-container') || document.body;
        const errorDiv = document.createElement('div');
        errorDiv.innerHTML = api.showConnectionError();
        container.prepend(errorDiv);
        return;
    }

    // Elementos del DOM
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('material-file') || document.querySelector('input[type="file"]');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress-bar') || document.querySelector('.progress-bar');
    const progressText = document.getElementById('progress-text');
    const resultContainer = document.getElementById('result-container') || document.getElementById('upload-result');

    if (!uploadForm || !fileInput) {
        console.error('❌ No se encontraron los elementos del formulario');
        return;
    }

    // Event listener para el formulario
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const file = fileInput.files[0];
        
        if (!file) {
            showError('Por favor selecciona un archivo');
            return;
        }

        // Validar tipo de archivo
        if (!file.name.endsWith('.pdf') && !file.name.endsWith('.txt')) {
            showError('Solo se permiten archivos PDF o TXT');
            return;
        }

        // Validar tamaño mínimo (aprox 80 páginas)
        const minSize = 200000; // bytes (200 KB)
        if (file.size < minSize) {
            const confirmUpload = confirm(
                `El archivo parece ser pequeño (${formatFileSize(file.size)}). \n\n` +
                `Se recomienda al menos 80 páginas (~200 KB de texto). \n\n` +
                `¿Deseas continuar de todos modos?`
            );
            if (!confirmUpload) return;
        }

        // Mostrar progreso
        showProgress(true);
        updateProgress(0, 'Preparando archivo...');

        try {
            // Simular progreso de lectura del archivo
            updateProgress(10, 'Leyendo archivo...');
            await sleep(300);

            updateProgress(30, 'Enviando al servidor...');
            await sleep(300);

            // Subir material
            const response = await api.uploadMaterial(file);

            // Simular procesamiento
            updateProgress(60, 'Procesando texto...');
            await sleep(500);

            updateProgress(80, 'Generando embeddings...');
            await sleep(500);

            updateProgress(100, '¡Completado!');

            // Mostrar resultado exitoso
            showSuccess(response);

            // Limpiar formulario
            uploadForm.reset();
            
            // Ocultar progreso después de 2 segundos
            setTimeout(() => {
                showProgress(false);
            }, 2000);

        } catch (error) {
            console.error('Error al subir material:', error);
            showError(error.message);
            showProgress(false);
        }
    });

    // Funciones auxiliares
    function showProgress(show) {
        if (progressContainer) {
            progressContainer.style.display = show ? 'block' : 'none';
        }
    }

    function updateProgress(percentage, message = '') {
        if (progressBar) {
            progressBar.value = percentage;
            progressBar.style.width = `${percentage}%`;
            progressBar.textContent = `${percentage}%`;
        }
        if (progressText) {
            progressText.textContent = message;
        }
    }

    function showSuccess(response) {
        if (!resultContainer) return;

        const stats = response.data;
        const pagesEstimate = Math.ceil(stats.total_characters / 2500);

        resultContainer.innerHTML = `
            <div class="success-message" style="background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #2e7d32; margin-top: 0;">✅ Material subido exitosamente</h3>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
                    <div class="stat-card" style="background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="font-size: 0.9em; color: #666;">ID del Material</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #4caf50;">#${response.material_id}</div>
                    </div>
                    
                    <div class="stat-card" style="background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="font-size: 0.9em; color: #666;">Chunks Generados</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #2196f3;">${stats.total_chunks}</div>
                    </div>
                    
                    <div class="stat-card" style="background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="font-size: 0.9em; color: #666;">Caracteres Procesados</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #ff9800;">${stats.total_characters.toLocaleString()}</div>
                    </div>
                    
                    <div class="stat-card" style="background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="font-size: 0.9em; color: #666;">Páginas Aprox.</div>
                        <div style="font-size: 1.5em; font-weight: bold; color: #9c27b0;">${pagesEstimate}</div>
                    </div>
                </div>

                <div style="background: white; padding: 15px; border-radius: 6px; margin-top: 15px;">
                    <p style="margin: 5px 0;"><strong>📄 Título:</strong> ${stats.title}</p>
                    <p style="margin: 5px 0;"><strong>📅 Fecha:</strong> ${formatTimestamp(stats.uploaded_at)}</p>
                    <p style="margin: 5px 0;"><strong>📝 Archivo:</strong> ${stats.filename}</p>
                </div>

                <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 6px; border-left: 4px solid #ffc107;">
                    <p style="margin: 0; color: #856404;">
                        <strong>💡 Siguiente paso:</strong> El material ha sido vectorizado y está listo para validación semántica. 
                        Ahora puedes crear preguntas asociadas a este material.
                    </p>
                </div>
            </div>
        `;

        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function showError(message) {
        if (!resultContainer) {
            alert(`Error: ${message}`);
            return;
        }

        resultContainer.innerHTML = `
            <div class="error-message" style="background: #ffebee; border-left: 4px solid #f44336; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="color: #c62828; margin-top: 0;">❌ Error al subir material</h3>
                <p style="color: #d32f2f;">${message}</p>
                <button onclick="this.parentElement.style.display='none'" style="background: #f44336; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin-top: 10px;">
                    Cerrar
                </button>
            </div>
        `;

        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    }

    function formatTimestamp(timestamp) {
        // Formato: YYYYMMDD_HHMMSS
        const year = timestamp.substring(0, 4);
        const month = timestamp.substring(4, 6);
        const day = timestamp.substring(6, 8);
        const hour = timestamp.substring(9, 11);
        const minute = timestamp.substring(11, 13);
        
        return `${day}/${month}/${year} ${hour}:${minute}`;
    }

    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    console.log('✅ Módulo de subida de materiales listo');
});
