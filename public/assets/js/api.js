/**
 * API Client para Recuiva - Sistema de Active Recall con IA
 * Maneja todas las llamadas al backend FastAPI con validación semántica
 * 
 * @author Abel Jesús Moya Acosta
 * @date 7 de octubre de 2025
 * @version 1.0.0
 */

/**
 * @typedef {Object} ValidationResult
 * @property {number} score - Score de comprensión (0-100)
 * @property {boolean} is_correct - Si la respuesta es correcta (score >= 55)
 * @property {number} similarity - Similitud del coseno (0-1)
 * @property {string} feedback - Feedback generado para el estudiante
 * @property {Array<ChunkMatch>} relevant_chunks - Top 3 chunks más relevantes
 * @property {BestMatch} best_match_chunk - Chunk con mayor similitud
 */

/**
 * @typedef {Object} ChunkMatch
 * @property {string} text - Texto del chunk (preview)
 * @property {string} text_full - Texto completo del chunk
 * @property {number} similarity - Score de similitud (0-1)
 * @property {number} position - Posición del chunk en el material
 * @property {number} total_chunks - Total de chunks del material
 */

/**
 * @typedef {Object} BestMatch
 * @property {string} text - Texto del chunk
 * @property {string} text_short - Preview del texto
 * @property {number} similarity - Score de similitud
 * @property {number} chunk_id - ID del chunk
 * @property {number} total_chunks - Total de chunks
 * @property {number} estimated_page - Página estimada
 */

/**
 * @typedef {Object} MaterialData
 * @property {number} id - ID del material
 * @property {string} filename - Nombre del archivo original
 * @property {string} title - Título del material
 * @property {string} uploaded_at - Timestamp de subida
 * @property {number} total_chunks - Total de chunks generados
 * @property {number} total_characters - Total de caracteres
 * @property {number} estimated_pages - Páginas estimadas
 * @property {number} [real_pages] - Páginas reales (solo PDF)
 */

/**
 * @typedef {Object} QuestionData
 * @property {number} id - ID de la pregunta
 * @property {string} text - Texto de la pregunta
 * @property {string} topic - Tema de la pregunta
 * @property {string} difficulty - Dificultad (fácil, medio, difícil)
 * @property {number} [material_id] - ID del material asociado
 */

/**
 * @typedef {Object} APIResponse
 * @property {boolean} success - Si la operación fue exitosa
 * @property {string} [message] - Mensaje de respuesta
 * @property {*} [data] - Datos de respuesta
 */

/**
 * Configuración de la API
 * @const {Object}
 */
const API_CONFIG = {
    BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8000'
        : 'https://api-recuiva.duckdns.org',
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

/**
 * Cliente HTTP para la API de Recuiva
 * Implementa métodos para todas las operaciones del backend
 * 
 * @class RecuivaAPI
 */
class RecuivaAPI {
    /**
     * Crea una instancia del cliente API
     * @param {string} [baseUrl=API_CONFIG.BASE_URL] - URL base del backend
     */
    constructor(baseUrl = API_CONFIG.BASE_URL) {
        this.baseUrl = baseUrl;
        this.isConnected = false;
    }

    /**
     * Realiza una petición HTTP genérica
     * @param {string} endpoint - Ruta del endpoint
     * @param {RequestInit} [options={}] - Opciones de fetch
     * @returns {Promise<any>} Respuesta JSON del servidor
     * @throws {Error} Si hay error de conexión o respuesta no exitosa
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
     * Sube un material (PDF o TXT) al backend
     * Genera embeddings y chunking automático
     * 
     * @param {File} file - Archivo a subir (PDF o TXT)
     * @param {string} [userId=null] - ID del usuario (opcional, se obtiene de Supabase si no se provee)
     * @param {Function} [onProgress=null] - Callback de progreso (opcional)
     * @returns {Promise<APIResponse & {data: MaterialData}>} Información del material procesado
     * 
     * @example
     * const file = document.getElementById('file-input').files[0];
     * const result = await api.uploadMaterial(file);
     * console.log(`Material ID: ${result.data.id}`);
     */
    async uploadMaterial(file, userId = null, onProgress = null) {
        const formData = new FormData();
        formData.append('file', file);

        // Obtener user_id de Supabase si no se provee
        let finalUserId = userId;
        
        // Intentar obtener usuario de Supabase o SupabaseOperations
        if (!finalUserId) {
            try {
                // Método 1: Usar SupabaseOperations si está disponible
                if (typeof SupabaseOperations !== 'undefined') {
                    const user = await SupabaseOperations.getCurrentUser();
                    if (user && user.id) {
                        finalUserId = user.id;
                        console.log('✅ User ID obtenido de SupabaseOperations:', finalUserId);
                    }
                }
                // Método 2: Fallback a supabaseClient directo
                else if (typeof supabaseClient !== 'undefined' && supabaseClient) {
                    const { data: { user } } = await supabaseClient.auth.getUser();
                    if (user) {
                        finalUserId = user.id;
                        console.log('✅ User ID obtenido de Supabase Auth:', finalUserId);
                    }
                }
            } catch (error) {
                console.warn('⚠️ Error obteniendo user_id:', error);
            }
        }

        // Headers con user_id (siempre debe estar presente gracias al mock)
        const headers = {};
        if (finalUserId) {
            headers['X-User-ID'] = finalUserId;
            console.log('📤 Enviando material con User-ID:', finalUserId);
        } else {
            console.error('❌ CRÍTICO: No se pudo obtener user_id. Verifica SupabaseOperations.');
        }

        return await this.request(API_CONFIG.ENDPOINTS.UPLOAD_MATERIAL, {
            method: 'POST',
            headers: headers,
            body: formData,
            // No incluir Content-Type header, el navegador lo establece automáticamente con boundary
        });
    }

    /**
     * Valida una respuesta semánticamente usando Cosine Similarity
     * Compara el embedding de la respuesta con los chunks del material
     * 
     * @param {number|null} questionId - ID de la pregunta guardada (o null para pregunta dinámica)
     * @param {string} userAnswer - Respuesta del estudiante
     * @returns {Promise<ValidationResult>} Resultado de la validación con score y feedback
     * 
     * @example
     * const result = await api.validateAnswer(null, "La fotosíntesis convierte luz en energía");
     * console.log(`Score: ${result.score}%`);
     * console.log(result.feedback);
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
     * Obtiene todos los materiales subidos
     * @returns {Promise<APIResponse & {materials: MaterialData[]}>} Lista de materiales
     */
    async getMaterials() {
        return await this.request(API_CONFIG.ENDPOINTS.GET_MATERIALS);
    }

    /**
     * Obtiene un material específico por ID
     * @param {number} materialId - ID del material
     * @returns {Promise<APIResponse & {material: MaterialData}>} Datos del material
     */
    async getMaterial(materialId) {
        return await this.request(`${API_CONFIG.ENDPOINTS.GET_MATERIAL}/${materialId}`);
    }

    /**
     * Crea una nueva pregunta
     * @param {Partial<QuestionData>} questionData - Datos de la pregunta
     * @returns {Promise<APIResponse & {question: QuestionData}>} Pregunta creada
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
     * Obtiene preguntas filtradas por tema y/o dificultad
     * @param {Object} [filters={}] - Filtros de búsqueda
     * @param {string} [filters.topic] - Tema de la pregunta
     * @param {string} [filters.difficulty] - Dificultad
     * @returns {Promise<APIResponse & {questions: QuestionData[]}>} Lista de preguntas
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
     * @returns {Promise<APIResponse & {stats: Object}>} Estadísticas globales
     */
    async getStats() {
        return await this.request(API_CONFIG.ENDPOINTS.GET_STATS);
    }

    /**
     * Verifica la conexión con el backend (health check)
     * @returns {Promise<boolean>} True si el backend está disponible
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
     * Muestra un mensaje de error de conexión con instrucciones
     * @returns {string} HTML del mensaje de error
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

/**
 * Instancia global de la API para uso en todo el frontend
 * @type {RecuivaAPI}
 * @global
 * 
 * @example
 * // Usar en cualquier página
 * const materials = await api.getMaterials();
 * const result = await api.validateAnswer(null, "Mi respuesta...");
 */
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
