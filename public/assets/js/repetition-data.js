// ===================================================================
// 🔄 SISTEMA DE SINCRONIZACIÓN DE DATOS DE REPASO
// ===================================================================
// Gestiona la persistencia y sincronización de datos de repaso
// entre localStorage, sesión actual y backend
// ===================================================================

/**
 * Clase para gestionar datos de repaso
 */
class RepetitionDataManager {
  constructor() {
    this.storagePrefix = 'recuiva_questions_material_';
    this.globalStorageKey = 'recuiva_all_questions';
  }

  /**
   * Obtiene todas las preguntas de todos los materiales
   * @returns {Array} Array de todas las preguntas
   */
  getAllQuestions() {
    const allQuestions = [];
    
    // Buscar todas las keys de localStorage que empiecen con el prefijo
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(this.storagePrefix)) {
        try {
          const questions = JSON.parse(localStorage.getItem(key));
          if (Array.isArray(questions)) {
            allQuestions.push(...questions);
          }
        } catch (e) {
          console.error(`Error al cargar preguntas de ${key}:`, e);
        }
      }
    }
    
    console.log(`📚 Total de preguntas cargadas: ${allQuestions.length}`);
    return allQuestions;
  }

  /**
   * Obtiene preguntas de un material específico
   * @param {string} materialId - ID del material
   * @returns {Array} Array de preguntas del material
   */
  getQuestionsByMaterial(materialId) {
    const key = `${this.storagePrefix}${materialId}`;
    try {
      const questions = JSON.parse(localStorage.getItem(key) || '[]');
      return Array.isArray(questions) ? questions : [];
    } catch (e) {
      console.error(`Error al cargar preguntas del material ${materialId}:`, e);
      return [];
    }
  }

  /**
   * Guarda preguntas de un material específico
   * @param {string} materialId - ID del material
   * @param {Array} questions - Array de preguntas
   */
  saveQuestionsByMaterial(materialId, questions) {
    const key = `${this.storagePrefix}${materialId}`;
    try {
      localStorage.setItem(key, JSON.stringify(questions));
      console.log(`✅ Guardadas ${questions.length} preguntas del material ${materialId}`);
    } catch (e) {
      console.error(`Error al guardar preguntas del material ${materialId}:`, e);
    }
  }

  /**
   * Actualiza los datos de repaso de una pregunta
   * @param {string} materialId - ID del material
   * @param {number} questionIndex - Índice de la pregunta
   * @param {object} reviewData - Datos de repaso actualizados
   */
  updateQuestionReviewData(materialId, questionIndex, reviewData) {
    const questions = this.getQuestionsByMaterial(materialId);
    
    if (questionIndex >= 0 && questionIndex < questions.length) {
      // Actualizar datos de repaso
      questions[questionIndex] = {
        ...questions[questionIndex],
        ...reviewData,
        lastUpdated: new Date().toISOString()
      };
      
      this.saveQuestionsByMaterial(materialId, questions);
      console.log(`✅ Datos de repaso actualizados para pregunta ${questionIndex} del material ${materialId}`);
      return true;
    }
    
    console.error(`❌ Índice de pregunta inválido: ${questionIndex}`);
    return false;
  }

  /**
   * Inicializa los datos de repaso para una pregunta nueva
   * @param {object} question - Objeto de pregunta
   * @returns {object} Pregunta con datos de repaso inicializados
   */
  initializeReviewData(question) {
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    return {
      ...question,
      repetition: 0,
      easeFactor: 2.5,
      nextReviewDate: tomorrow.toISOString(),
      lastReviewDate: now.toISOString(),
      reviewHistory: [{
        date: now.toISOString(),
        score: question.score || 0,
        quality: window.SRS ? window.SRS.scoreToQuality(question.score || 0) : 3,
        interval: 1,
        easeFactor: 2.5,
        repetition: 0
      }],
      interval: 1
    };
  }

  /**
   * Migra preguntas antiguas para agregar datos de repaso
   */
  migrateOldQuestions() {
    console.log('🔄 Migrando preguntas antiguas...');
    let migratedCount = 0;
    
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(this.storagePrefix)) {
        try {
          const questions = JSON.parse(localStorage.getItem(key));
          if (Array.isArray(questions)) {
            let needsSave = false;
            
            const migratedQuestions = questions.map(q => {
              // Si no tiene datos de repaso, inicializarlos
              if (!q.nextReviewDate || !q.reviewHistory) {
                needsSave = true;
                migratedCount++;
                return this.initializeReviewData(q);
              }
              return q;
            });
            
            if (needsSave) {
              localStorage.setItem(key, JSON.stringify(migratedQuestions));
            }
          }
        } catch (e) {
          console.error(`Error al migrar ${key}:`, e);
        }
      }
    }
    
    console.log(`✅ Migradas ${migratedCount} preguntas antiguas`);
    return migratedCount;
  }
  
  /**
   * 🔧 Normalizar todos los scores a escala 0-100
   * Convierte scores en formato decimal (0.69) a porcentaje (69)
   */
  normalizeAllScores() {
    console.log('🔄 Normalizando scores en todas las preguntas...');
    
    let totalNormalized = 0;
    
    // Recorrer todos los materiales
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(this.storagePrefix)) {
        const materialId = key.replace(this.storagePrefix, '');
        const questions = this.getQuestionsByMaterial(materialId);
        let normalized = 0;
        
        const updatedQuestions = questions.map(q => {
          // Si el score está en formato decimal (0-1), convertir a porcentaje
          if (q.score !== undefined && q.score > 0 && q.score <= 1) {
            const oldScore = q.score;
            q.score = Math.round(q.score * 100);
            console.log(`  📊 Pregunta "${q.pregunta.substring(0, 30)}...": ${oldScore} → ${q.score}%`);
            normalized++;
          }
          return q;
        });
        
        if (normalized > 0) {
          this.saveQuestionsByMaterial(materialId, updatedQuestions);
          totalNormalized += normalized;
        }
      }
    }
    
    console.log(`✅ ${totalNormalized} scores normalizados correctamente`);
    return totalNormalized;
  }

  /**
   * Obtiene estadísticas globales de repasos
   * @returns {object} Estadísticas de repasos
   */
  getGlobalStats() {
    const allQuestions = this.getAllQuestions();
    
    if (!window.SRS) {
      console.error('❌ Sistema de repaso espaciado no inicializado');
      return null;
    }
    
    return window.SRS.getStats(allQuestions);
  }

  /**
   * Obtiene preguntas que deben repasarse hoy
   * @returns {Array} Preguntas pendientes de repaso
   */
  getDueQuestions() {
    const allQuestions = this.getAllQuestions();
    
    if (!window.SRS) {
      console.error('❌ Sistema de repaso espaciado no inicializado');
      return [];
    }
    
    return window.SRS.getDueQuestions(allQuestions);
  }

  /**
   * Obtiene calendario de repasos
   * @param {number} year - Año
   * @param {number} month - Mes (0-11)
   * @returns {object} Calendario de repasos
   */
  getCalendar(year, month) {
    const allQuestions = this.getAllQuestions();
    
    if (!window.SRS) {
      console.error('❌ Sistema de repaso espaciado no inicializado');
      return {};
    }
    
    return window.SRS.getCalendar(allQuestions, year, month);
  }

  /**
   * Procesa una respuesta y actualiza los datos de repaso
   * @param {string} materialId - ID del material
   * @param {number} questionIndex - Índice de la pregunta
   * @param {number} score - Score obtenido (0-100)
   * @returns {object} Datos de repaso actualizados
   */
  processAnswer(materialId, questionIndex, score) {
    const questions = this.getQuestionsByMaterial(materialId);
    
    if (questionIndex < 0 || questionIndex >= questions.length) {
      console.error(`❌ Índice de pregunta inválido: ${questionIndex}`);
      return null;
    }
    
    if (!window.SRS) {
      console.error('❌ Sistema de repaso espaciado no inicializado');
      return null;
    }
    
    const question = questions[questionIndex];
    const reviewData = window.SRS.processAnswer(question, score);
    
    // Actualizar la pregunta con los nuevos datos
    this.updateQuestionReviewData(materialId, questionIndex, reviewData);
    
    console.log(`✅ Respuesta procesada. Próximo repaso: ${new Date(reviewData.nextReviewDate).toLocaleDateString('es-ES')}`);
    
    return reviewData;
  }

  /**
   * Exporta todos los datos de repaso a JSON
   * @returns {string} JSON con todos los datos
   */
  exportData() {
    const allQuestions = this.getAllQuestions();
    const stats = this.getGlobalStats();
    
    const exportData = {
      exportDate: new Date().toISOString(),
      totalQuestions: allQuestions.length,
      stats: stats,
      questions: allQuestions
    };
    
    return JSON.stringify(exportData, null, 2);
  }

  /**
   * Importa datos de repaso desde JSON
   * @param {string} jsonData - JSON con los datos
   * @returns {boolean} true si se importó correctamente
   */
  importData(jsonData) {
    try {
      const data = JSON.parse(jsonData);
      
      if (!data.questions || !Array.isArray(data.questions)) {
        console.error('❌ Formato de datos inválido');
        return false;
      }
      
      // Agrupar preguntas por material
      const byMaterial = {};
      data.questions.forEach(q => {
        const materialId = q.material_id || q.carpeta_id || 'sin_material';
        if (!byMaterial[materialId]) {
          byMaterial[materialId] = [];
        }
        byMaterial[materialId].push(q);
      });
      
      // Guardar por material
      Object.keys(byMaterial).forEach(materialId => {
        this.saveQuestionsByMaterial(materialId, byMaterial[materialId]);
      });
      
      console.log(`✅ Importadas ${data.questions.length} preguntas`);
      return true;
    } catch (e) {
      console.error('❌ Error al importar datos:', e);
      return false;
    }
  }
}

// ===================================================================
// EXPORTAR INSTANCIA GLOBAL
// ===================================================================
window.RepetitionData = new RepetitionDataManager();

console.log('✅ Gestor de datos de repaso inicializado');

// Migrar preguntas antiguas automáticamente
window.RepetitionData.migrateOldQuestions();
