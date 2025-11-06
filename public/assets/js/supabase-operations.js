/**
 * Supabase Operations Module - Recuiva
 * Maneja todas las operaciones CRUD con Supabase
 * @author Abel Jesús Moya Acosta
 * @date 4 de noviembre de 2025
 */

class SupabaseOperations {
    
    /**
     * Obtiene el cliente de Supabase inicializado
     */
    static getClient() {
        if (!supabaseClient) {
            console.error('❌ Supabase no está inicializado');
            throw new Error('Supabase client no está inicializado');
        }
        return supabaseClient;
    }

    /**
     * Obtiene el usuario autenticado actual
     */
    /**
     * Obtiene el usuario autenticado actual
     * @returns {Promise<Object|null>} Usuario autenticado o null si no hay sesión
     */
    static async getCurrentUser() {
        try {
            const { data: { user }, error } = await this.getClient().auth.getUser();
            
            if (error) {
                console.warn('⚠️ Error obteniendo usuario de Auth:', error.message);
                return null;
            }
            
            if (!user) {
                console.warn('⚠️ No hay usuario autenticado. Redirige a login si es necesario.');
                return null;
            }
            
            console.log('✅ Usuario autenticado:', user.email);
            return user;
        } catch (error) {
            console.error('❌ Error obteniendo usuario:', error);
            return null;
        }
    }

    /**
     * Verifica si hay una sesión activa y redirige al login si no
     * @param {string} redirectUrl - URL a la que redirigir si no hay sesión (default: login.html)
     * @returns {Promise<Object|null>} Usuario autenticado o null
     */
    static async requireAuth(redirectUrl = 'login.html') {
        const user = await this.getCurrentUser();
        
        if (!user) {
            console.warn('🔒 Sesión no encontrada, redirigiendo a login...');
            window.location.href = redirectUrl;
            return null;
        }
        
        return user;
    }

    /**
     * Cierra la sesión del usuario actual
     * @returns {Promise<void>}
     */
    static async logout() {
        try {
            const { error } = await this.getClient().auth.signOut();
            
            if (error) throw error;
            
            console.log('✅ Sesión cerrada exitosamente');
            
            // Limpiar localStorage
            localStorage.removeItem('recuiva_user_email');
            localStorage.removeItem('recuiva_user_id');
            
            // Redirigir al login
            window.location.href = 'login.html';
        } catch (error) {
            console.error('❌ Error cerrando sesión:', error);
            throw error;
        }
    }

    // ============================================
    // CARPETAS (FOLDERS)
    // ============================================

    /**
     * Crea una nueva carpeta
     * @param {string} name - Nombre de la carpeta
     * @param {string|null} parentId - ID de la carpeta padre (null para raíz)
     * @param {Object} options - Opciones adicionales (color, icon, path)
     * @returns {Promise<Object>} Carpeta creada
     */
    static async createFolder(name, parentId = null, options = {}) {
        try {
            const user = await this.getCurrentUser();
            if (!user) throw new Error('Usuario no autenticado');

            const folderData = {
                name: name,
                parent_folder_id: parentId,
                user_id: user.id,
                color: options.color || '#FF6B35',
                icon: options.icon || 'folder',
                path: options.path || name
            };

            const { data, error } = await this.getClient()
                .from('folders')
                .insert([folderData])
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Carpeta creada en Supabase:', data);
            return data;
        } catch (error) {
            console.error('❌ Error creando carpeta:', error);
            throw error;
        }
    }

    /**
     * Obtiene todas las carpetas del usuario
     * @returns {Promise<Array>} Lista de carpetas
     */
    static async getFolders() {
        try {
            const user = await this.getCurrentUser();
            if (!user) return [];

            const { data, error } = await this.getClient()
                .from('folders')
                .select('*')
                .eq('user_id', user.id)
                .order('created_at', { ascending: false });

            if (error) throw error;
            console.log(`📁 ${data?.length || 0} carpetas obtenidas de Supabase`);
            return data || [];
        } catch (error) {
            console.error('❌ Error obteniendo carpetas:', error);
            return [];
        }
    }

    /**
     * Actualiza una carpeta existente
     * @param {string} folderId - UUID de la carpeta
     * @param {Object} updates - Datos a actualizar
     * @returns {Promise<Object>} Carpeta actualizada
     */
    static async updateFolder(folderId, updates) {
        try {
            const { data, error } = await this.getClient()
                .from('folders')
                .update(updates)
                .eq('id', folderId)
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Carpeta actualizada:', data);
            return data;
        } catch (error) {
            console.error('❌ Error actualizando carpeta:', error);
            throw error;
        }
    }

    /**
     * Elimina una carpeta
     * @param {string} folderId - UUID de la carpeta
     * @returns {Promise<boolean>} true si se eliminó correctamente
     */
    static async deleteFolder(folderId) {
        try {
            const { error } = await this.getClient()
                .from('folders')
                .delete()
                .eq('id', folderId);

            if (error) throw error;
            console.log('✅ Carpeta eliminada');
            return true;
        } catch (error) {
            console.error('❌ Error eliminando carpeta:', error);
            throw error;
        }
    }

    // ============================================
    // MATERIALES
    // ============================================

    /**
     * Obtiene todos los materiales del usuario
     * @returns {Promise<Array>} Lista de materiales
     */
    static async getMaterials() {
        try {
            const user = await this.getCurrentUser();
            if (!user) return [];

            const { data, error } = await this.getClient()
                .from('materials')
                .select('*')
                .eq('user_id', user.id)
                .order('created_at', { ascending: false });

            if (error) throw error;
            console.log(`📄 ${data?.length || 0} materiales obtenidos de Supabase`);
            return data || [];
        } catch (error) {
            console.error('❌ Error obteniendo materiales:', error);
            return [];
        }
    }

    /**
     * Obtiene un material por ID
     * @param {string} materialId - UUID del material
     * @returns {Promise<Object|null>} Material o null
     */
    static async getMaterialById(materialId) {
        try {
            const { data, error } = await this.getClient()
                .from('materials')
                .select('*')
                .eq('id', materialId)
                .single();

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('❌ Error obteniendo material:', error);
            return null;
        }
    }

    /**
     * Crea un nuevo material en Supabase
     * @param {Object} materialData - Datos del material
     * @param {string} materialData.title - Título del material
     * @param {string} materialData.file_name - Nombre del archivo
     * @param {string} materialData.file_type - Tipo de archivo ('pdf' o 'txt')
     * @param {number} materialData.total_chunks - Total de chunks procesados
     * @param {number} materialData.total_characters - Total de caracteres
     * @param {number} materialData.estimated_pages - Páginas estimadas
     * @param {string} materialData.processing_status - Estado del procesamiento
     * @returns {Promise<Object>} Material creado
     */
    static async createMaterial(materialData) {
        try {
            const user = await this.getCurrentUser();
            if (!user) throw new Error('Usuario no autenticado');

            const { data, error } = await this.getClient()
                .from('materials')
                .insert([{
                    user_id: user.id,
                    title: materialData.title,
                    file_name: materialData.file_name,
                    file_type: materialData.file_type,
                    total_chunks: materialData.total_chunks || 0,
                    total_characters: materialData.total_characters || 0,
                    estimated_pages: materialData.estimated_pages || 0,
                    processing_status: materialData.processing_status || 'completed'
                }])
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Material creado en Supabase:', data);
            return data;
        } catch (error) {
            console.error('❌ Error creando material:', error);
            throw error;
        }
    }

    /**
     * Asocia un material a una carpeta
     * @param {string} materialId - UUID del material
     * @param {string} folderId - UUID de la carpeta
     * @returns {Promise<Object>} Asociación creada
     */
    static async linkMaterialToFolder(materialId, folderId) {
        try {
            const { data, error } = await this.getClient()
                .from('material_folders')
                .insert([{
                    material_id: materialId,
                    folder_id: folderId
                }])
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Material asociado a carpeta:', data);
            return data;
        } catch (error) {
            console.error('❌ Error asociando material a carpeta:', error);
            throw error;
        }
    }

    /**
     * Obtiene materiales de una carpeta específica
     * @param {string} folderId - UUID de la carpeta
     * @returns {Promise<Array>} Lista de materiales
     */
    static async getMaterialsByFolder(folderId) {
        try {
            const { data, error } = await this.getClient()
                .from('material_folders')
                .select(`
                    material_id,
                    materials (*)
                `)
                .eq('folder_id', folderId);

            if (error) throw error;
            return data?.map(item => item.materials) || [];
        } catch (error) {
            console.error('❌ Error obteniendo materiales de carpeta:', error);
            return [];
        }
    }

    // ============================================
    // PREGUNTAS
    // ============================================

    /**
     * Crea una nueva pregunta
     * @param {string} materialId - UUID del material
     * @param {string} questionText - Texto de la pregunta
     * @param {Object} options - Opciones adicionales
     * @returns {Promise<Object>} Pregunta creada
     */
    static async createQuestion(materialId, questionText, options = {}) {
        try {
            const user = await this.getCurrentUser();
            if (!user) throw new Error('Usuario no autenticado');

            const questionData = {
                user_id: user.id,
                material_id: materialId,
                question_text: questionText,
                topic: options.topic || null,
                difficulty: options.difficulty || 'medium',
                expected_answer: options.expectedAnswer || null
            };

            const { data, error } = await this.getClient()
                .from('questions')
                .insert([questionData])
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Pregunta creada en Supabase:', data);
            return data;
        } catch (error) {
            console.error('❌ Error creando pregunta:', error);
            throw error;
        }
    }

    /**
     * Obtiene preguntas de un material
     * @param {string} materialId - UUID del material
     * @returns {Promise<Array>} Lista de preguntas
     */
    static async getQuestionsByMaterial(materialId) {
        try {
            const user = await this.getCurrentUser();
            if (!user) {
                console.warn('⚠️ No user found, cannot get questions');
                return [];
            }

            console.log(`🔍 Buscando preguntas para material: ${materialId}, user: ${user.id} (${user.email})`);

            const { data, error } = await this.getClient()
                .from('questions')
                .select('*')
                .eq('material_id', materialId)
                .eq('user_id', user.id)
                .order('created_at', { ascending: false });

            if (error) {
                console.error('❌ Error query:', error);
                throw error;
            }
            
            console.log(`❓ ${data?.length || 0} preguntas obtenidas para material ${materialId}`);
            if (data && data.length > 0) {
                console.log('📋 Preguntas encontradas:', data.map(q => ({
                    id: q.id,
                    text: q.question_text.substring(0, 50) + '...',
                    created: q.created_at
                })));
            }
            return data || [];
        } catch (error) {
            console.error('❌ Error obteniendo preguntas:', error);
            return [];
        }
    }

    /**
     * Actualiza una pregunta
     * @param {string} questionId - UUID de la pregunta
     * @param {Object} updates - Datos a actualizar
     * @returns {Promise<Object>} Pregunta actualizada
     */
    static async updateQuestion(questionId, updates) {
        try {
            const { data, error } = await this.getClient()
                .from('questions')
                .update(updates)
                .eq('id', questionId)
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Pregunta actualizada:', data);
            return data;
        } catch (error) {
            console.error('❌ Error actualizando pregunta:', error);
            throw error;
        }
    }

    /**
     * Elimina una pregunta
     * @param {string} questionId - UUID de la pregunta
     * @returns {Promise<boolean>} true si se eliminó
     */
    static async deleteQuestion(questionId) {
        try {
            const { error } = await this.getClient()
                .from('questions')
                .delete()
                .eq('id', questionId);

            if (error) throw error;
            console.log('✅ Pregunta eliminada');
            return true;
        } catch (error) {
            console.error('❌ Error eliminando pregunta:', error);
            throw error;
        }
    }

    // ============================================
    // RESPUESTAS
    // ============================================

    /**
     * Crea una nueva respuesta con validación
     * @param {string} questionId - UUID de la pregunta
     * @param {string} answerText - Texto de la respuesta
     * @param {number} score - Puntuación (0-100)
     * @param {Object} validationData - Datos de validación semántica
     * @returns {Promise<Object>} Respuesta creada
     */
    static async createAnswer(questionId, answerText, score, validationData = {}) {
        try {
            const user = await this.getCurrentUser();
            if (!user) throw new Error('Usuario no autenticado');

            const answerData = {
                user_id: user.id,
                question_id: questionId,
                answer_text: answerText,
                score: parseFloat(score),
                similarity: validationData.similarity || null,
                is_correct: validationData.is_correct || score >= 55,
                classification: validationData.classification || this.classifyScore(score),
                feedback: validationData.feedback || null,
                best_match_chunk: validationData.best_match_chunk ? 
                    JSON.stringify(validationData.best_match_chunk) : null,
                relevant_chunks: validationData.relevant_chunks || null
            };

            const { data, error } = await this.getClient()
                .from('answers')
                .insert([answerData])
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Respuesta guardada en Supabase:', data);
            return data;
        } catch (error) {
            console.error('❌ Error creando respuesta:', error);
            throw error;
        }
    }

    /**
     * Obtiene respuestas de una pregunta
     * @param {string} questionId - UUID de la pregunta
     * @returns {Promise<Array>} Lista de respuestas
     */
    static async getAnswersByQuestion(questionId) {
        try {
            const { data, error } = await this.getClient()
                .from('answers')
                .select('*')
                .eq('question_id', questionId)
                .order('created_at', { ascending: false });

            if (error) throw error;
            return data || [];
        } catch (error) {
            console.error('❌ Error obteniendo respuestas:', error);
            return [];
        }
    }

    /**
     * Clasifica el score en categoría
     * @param {number} score - Puntuación (0-100)
     * @returns {string} Clasificación
     */
    static classifyScore(score) {
        if (score >= 85) return 'EXCELENTE';
        if (score >= 70) return 'BUENO';
        if (score >= 55) return 'ACEPTABLE';
        return 'INSUFICIENTE';
    }

    // ============================================
    // REPETICIÓN ESPACIADA (SPACED REPETITION)
    // ============================================

    /**
     * Crea o actualiza datos de repetición espaciada
     * @param {string} questionId - UUID de la pregunta
     * @param {Date} nextReview - Fecha próximo repaso
     * @param {number} intervalDays - Intervalo en días
     * @param {number} easeFactor - Factor de facilidad
     * @param {Object} options - Opciones adicionales
     * @returns {Promise<Object>} Datos de repetición
     */
    static async upsertSpacedRepetition(questionId, nextReview, intervalDays, easeFactor, options = {}) {
        try {
            const user = await this.getCurrentUser();
            if (!user) throw new Error('Usuario no autenticado');

            const reviewData = {
                user_id: user.id,
                question_id: questionId,
                next_review: nextReview instanceof Date ? 
                    nextReview.toISOString().split('T')[0] : nextReview,
                interval_days: intervalDays,
                ease_factor: parseFloat(easeFactor),
                repetitions: options.repetitions || 0,
                last_score: options.lastScore || null,
                last_review: options.lastReview ? 
                    (options.lastReview instanceof Date ? 
                        options.lastReview.toISOString().split('T')[0] : options.lastReview) 
                    : null
            };

            const { data, error } = await this.getClient()
                .from('spaced_repetition')
                .upsert([reviewData], { 
                    onConflict: 'user_id,question_id',
                    ignoreDuplicates: false 
                })
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Repetición espaciada guardada:', data);
            return data;
        } catch (error) {
            console.error('❌ Error guardando repetición espaciada:', error);
            throw error;
        }
    }

    /**
     * Obtiene repasos pendientes para hoy
     * @returns {Promise<Array>} Lista de repasos pendientes
     */
    static async getReviewsForToday() {
        try {
            const user = await this.getCurrentUser();
            if (!user) return [];

            const today = new Date().toISOString().split('T')[0];

            const { data, error } = await this.getClient()
                .from('spaced_repetition')
                .select(`
                    *,
                    questions (
                        id,
                        question_text,
                        material_id,
                        materials (
                            id,
                            title
                        )
                    )
                `)
                .eq('user_id', user.id)
                .lte('next_review', today)
                .order('next_review', { ascending: true });

            if (error) throw error;
            console.log(`📅 ${data?.length || 0} repasos pendientes para hoy`);
            return data || [];
        } catch (error) {
            console.error('❌ Error obteniendo repasos:', error);
            return [];
        }
    }

    /**
     * Actualiza datos de repetición después de un repaso
     * @param {string} repetitionId - UUID del registro de repetición
     * @param {Object} updates - Datos actualizados
     * @returns {Promise<Object>} Datos actualizados
     */
    static async updateReviewData(repetitionId, updates) {
        try {
            const { data, error } = await this.getClient()
                .from('spaced_repetition')
                .update(updates)
                .eq('id', repetitionId)
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Datos de repaso actualizados:', data);
            return data;
        } catch (error) {
            console.error('❌ Error actualizando repaso:', error);
            throw error;
        }
    }

    // ============================================
    // PERFILES DE USUARIO
    // ============================================

    /**
     * Obtiene o crea el perfil del usuario
     * @returns {Promise<Object|null>} Perfil del usuario
     */
    static async getUserProfile() {
        try {
            const user = await this.getCurrentUser();
            if (!user) return null;

            const { data, error } = await this.getClient()
                .from('user_profiles')
                .select('*')
                .eq('id', user.id)
                .single();

            if (error && error.code === 'PGRST116') {
                // Perfil no existe, crearlo
                return await this.createUserProfile({
                    full_name: user.user_metadata?.full_name || user.email.split('@')[0]
                });
            }

            if (error) throw error;
            return data;
        } catch (error) {
            console.error('❌ Error obteniendo perfil:', error);
            return null;
        }
    }

    /**
     * Crea un perfil de usuario
     * @param {Object} profileData - Datos del perfil
     * @returns {Promise<Object>} Perfil creado
     */
    static async createUserProfile(profileData) {
        try {
            const user = await this.getCurrentUser();
            if (!user) throw new Error('Usuario no autenticado');

            const { data, error } = await this.getClient()
                .from('user_profiles')
                .insert([{
                    id: user.id,
                    ...profileData
                }])
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Perfil creado:', data);
            return data;
        } catch (error) {
            console.error('❌ Error creando perfil:', error);
            throw error;
        }
    }

    /**
     * Actualiza el perfil del usuario
     * @param {Object} updates - Datos a actualizar
     * @returns {Promise<Object>} Perfil actualizado
     */
    static async updateUserProfile(updates) {
        try {
            const user = await this.getCurrentUser();
            if (!user) throw new Error('Usuario no autenticado');

            const { data, error } = await this.getClient()
                .from('user_profiles')
                .update(updates)
                .eq('id', user.id)
                .select()
                .single();

            if (error) throw error;
            console.log('✅ Perfil actualizado:', data);
            return data;
        } catch (error) {
            console.error('❌ Error actualizando perfil:', error);
            throw error;
        }
    }
}

// Exportar para uso global
window.SupabaseOperations = SupabaseOperations;

console.log('✅ Supabase Operations Module cargado');
