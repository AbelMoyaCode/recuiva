/**
 * API Client para Recuiva
 * Maneja todas las llamadas al backend FastAPI
 * 
 * Autor: Abel Jesús Moya Acosta
 * Fecha: 7 de octubre de 2025
 */

const API_CONFIG = {
    BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : 'https://tu-dominio-backend.com', // Cambiar en producción
    ENDPOINTS: {
        ROOT: '/',
        UPLOAD_MATERIAL: '/api/materials/upload',
        VALIDATE_ANSWER: '/api/validate-answer',
        GET_MATERIALS: '/api/materials',
        GET_MATERIAL: '/api/materials',
        CREATE_QUESTION: '/api/questions',
        GET_QUESTIONS: '/api/questions',
        GET_STATS: '/api/stats',
        HEALTH: '/api/health'
    }
};

class RecuivaAPI {
    constructor(baseUrl = API_CONFIG.BASE_URL) {
        this.baseUrl = baseUrl;
        this.isConnected = false;
    }

    /**
     * Realiza una petición HTTP genérica
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...options.headers
                }
            });

            if (!response.ok) {
                const error = await response.json().catch(() => ({ detail: 'Error en la petición' }));
                throw new Error(error.detail || `Error ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            
            // Si es error de conexión, marcar como desconectado
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                this.isConnected = false;
                throw new Error('No se puede conectar con el servidor. Asegúrate de que el backend esté ejecutándose.');
            }
            
            throw error;
        }
    }

    /**
     * Sube un material (PDF o TXT)
     */
    async uploadMaterial(file, onProgress = null) {
        const formData = new FormData();
        formData.append('file', file);

        return await this.request(API_CONFIG.ENDPOINTS.UPLOAD_MATERIAL, {
            method: 'POST',
            body: formData,
            // No incluir Content-Type header, el navegador lo establece automáticamente con boundary
        });
    }

    /**
     * Valida una respuesta semánticamente
     */
    async validateAnswer(questionId, userAnswer) {
        return await this.request(API_CONFIG.ENDPOINTS.VALIDATE_ANSWER, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question_id: questionId,
                user_answer: userAnswer
            })
        });
    }

    /**
     * Obtiene todos los materiales
     */
    async getMaterials() {
        return await this.request(API_CONFIG.ENDPOINTS.GET_MATERIALS);
    }

    /**
     * Obtiene un material específico
     */
    async getMaterial(materialId) {
        return await this.request(`${API_CONFIG.ENDPOINTS.GET_MATERIAL}/${materialId}`);
    }

    /**
     * Crea una nueva pregunta
     */
    async createQuestion(questionData) {
        return await this.request(API_CONFIG.ENDPOINTS.CREATE_QUESTION, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(questionData)
        });
    }

    /**
     * Obtiene preguntas filtradas
     */
    async getQuestions(filters = {}) {
        const params = new URLSearchParams(filters);
        const queryString = params.toString();
        const endpoint = queryString 
            ? `${API_CONFIG.ENDPOINTS.GET_QUESTIONS}?${queryString}`
            : API_CONFIG.ENDPOINTS.GET_QUESTIONS;
        
        return await this.request(endpoint);
    }

    /**
     * Obtiene estadísticas del sistema
     */
    async getStats() {
        return await this.request(API_CONFIG.ENDPOINTS.GET_STATS);
    }

    /**
     * Verifica la conexión con el backend
     */
    async checkConnection() {
        try {
            const response = await this.request(API_CONFIG.ENDPOINTS.HEALTH);
            this.isConnected = response.status === 'healthy';
            return this.isConnected;
        } catch (error) {
            this.isConnected = false;
            console.error('Backend no disponible:', error.message);
            return false;
        }
    }

    /**
     * Muestra un mensaje de error de conexión
     */
    showConnectionError() {
        const errorHtml = `
            <div style="background: #fee; border: 2px solid #f44; padding: 20px; border-radius: 8px; margin: 20px;">
                <h3 style="color: #c00; margin-top: 0;">⚠️ Backend no disponible</h3>
                <p>No se puede conectar con el servidor backend.</p>
                <p><strong>Solución:</strong></p>
                <ol>
                    <li>Abre una terminal en la carpeta <code>backend/</code></li>
                    <li>Ejecuta: <code>python main.py</code></li>
                    <li>Espera a que veas: "🚀 Iniciando Recuiva Backend API"</li>
                    <li>Recarga esta página</li>
                </ol>
                <p style="font-size: 0.9em; color: #666;">
                    El backend debe estar ejecutándose en: <strong>${this.baseUrl}</strong>
                </p>
            </div>
        `;
        return errorHtml;
    }
}

// Instancia global de la API
const api = new RecuivaAPI();

// Verificar conexión al cargar la página
window.addEventListener('DOMContentLoaded', async () => {
    const isConnected = await api.checkConnection();
    
    if (!isConnected) {
        console.warn('⚠️ Backend no disponible. La aplicación funcionará en modo limitado.');
    } else {
        console.log('✅ Conectado con el backend en:', api.baseUrl);
    }
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { RecuivaAPI, api, API_CONFIG };
}
