// ===================================================================
// 🧠 SISTEMA DE REPASO ESPACIADO (Spaced Repetition System)
// ===================================================================
// Basado en el algoritmo SM-2 (SuperMemo 2) simplificado
// Actualizado: 14 de octubre de 2025
// ===================================================================

/**
 * Clase principal del sistema de repaso espaciado
 */
class SpacedRepetitionSystem {
  constructor() {
    // Intervalos base en días para cada nivel de calidad
    this.intervals = {
      1: 1,      // Muy mal - 1 día
      2: 3,      // Mal - 3 días  
      3: 7,      // Regular - 7 días
      4: 14,     // Bien - 14 días
      5: 30      // Excelente - 30 días
    };
    
    // Factor de facilidad (ease factor) por defecto
    this.defaultEaseFactor = 2.5;
  }

  /**
   * Convierte un score (0-100) a calidad (1-5)
   * @param {number} score - Score de 0 a 100
   * @returns {number} Calidad de 1 a 5
   */
  scoreToQuality(score) {
    if (score >= 90) return 5; // Excelente
    if (score >= 75) return 4; // Bien
    if (score >= 60) return 3; // Regular
    if (score >= 40) return 2; // Mal
    return 1; // Muy mal
  }

  /**
   * Calcula el próximo intervalo de repaso
   * @param {number} quality - Calidad de la respuesta (1-5)
   * @param {number} repetition - Número de repeticiones exitosas
   * @param {number} easeFactor - Factor de facilidad actual
   * @returns {object} { interval, nextEaseFactor, nextRepetition }
   */
  calculateNextInterval(quality, repetition = 0, easeFactor = 2.5) {
    let nextEaseFactor = easeFactor;
    let nextRepetition = repetition;
    let interval = 0;

    // Si la calidad es menor a 3, reiniciar el aprendizaje
    if (quality < 3) {
      nextRepetition = 0;
      interval = 1; // Volver a repasar mañana
    } else {
      // Incrementar el contador de repeticiones
      nextRepetition = repetition + 1;

      // Calcular el intervalo según el número de repeticiones
      if (nextRepetition === 1) {
        interval = 1; // Primera repetición: 1 día
      } else if (nextRepetition === 2) {
        interval = 6; // Segunda repetición: 6 días
      } else {
        // Repeticiones posteriores: multiplicar por el factor de facilidad
        interval = Math.round(this.intervals[quality] * easeFactor);
      }

      // Actualizar el factor de facilidad
      nextEaseFactor = easeFactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
      
      // El factor de facilidad no puede ser menor a 1.3
      if (nextEaseFactor < 1.3) {
        nextEaseFactor = 1.3;
      }
    }

    return {
      interval: interval,
      nextEaseFactor: nextEaseFactor,
      nextRepetition: nextRepetition
    };
  }

  /**
   * Calcula la fecha del próximo repaso
   * @param {number} intervalDays - Intervalo en días
   * @param {Date} lastReviewDate - Fecha del último repaso (por defecto: ahora)
   * @returns {Date} Fecha del próximo repaso
   */
  calculateNextReviewDate(intervalDays, lastReviewDate = new Date()) {
    const nextDate = new Date(lastReviewDate);
    nextDate.setDate(nextDate.getDate() + intervalDays);
    return nextDate;
  }

  /**
   * Verifica si una pregunta debe repasarse hoy
   * @param {Date} nextReviewDate - Fecha del próximo repaso
   * @returns {boolean} true si debe repasarse hoy
   */
  isDueToday(nextReviewDate) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const reviewDate = new Date(nextReviewDate);
    reviewDate.setHours(0, 0, 0, 0);
    
    return reviewDate <= today;
  }

  /**
   * Calcula cuántos días faltan para el próximo repaso
   * @param {Date} nextReviewDate - Fecha del próximo repaso
   * @returns {number} Días restantes (negativo si está atrasado)
   */
  daysUntilReview(nextReviewDate) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const reviewDate = new Date(nextReviewDate);
    reviewDate.setHours(0, 0, 0, 0);
    
    const diffTime = reviewDate - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays;
  }

  /**
   * Procesa una nueva respuesta y actualiza los datos de repaso
   * @param {object} question - Objeto de pregunta con historial de repasos
   * @param {number} score - Score obtenido (0-100)
   * @returns {object} Datos actualizados de repaso
   */
  processAnswer(question, score) {
    const quality = this.scoreToQuality(score);
    
    // Obtener datos actuales de repaso o usar valores por defecto
    const currentRepetition = question.repetition || 0;
    const currentEaseFactor = question.easeFactor || this.defaultEaseFactor;
    
    // Calcular el próximo intervalo
    const { interval, nextEaseFactor, nextRepetition } = this.calculateNextInterval(
      quality,
      currentRepetition,
      currentEaseFactor
    );
    
    // Calcular la fecha del próximo repaso
    const nextReviewDate = this.calculateNextReviewDate(interval);
    
    // Crear entrada en el historial de repasos
    const reviewEntry = {
      date: new Date().toISOString(),
      score: score,
      quality: quality,
      interval: interval,
      easeFactor: nextEaseFactor,
      repetition: nextRepetition
    };
    
    // Actualizar el historial
    const reviewHistory = question.reviewHistory || [];
    reviewHistory.push(reviewEntry);
    
    return {
      repetition: nextRepetition,
      easeFactor: nextEaseFactor,
      nextReviewDate: nextReviewDate.toISOString(),
      lastReviewDate: new Date().toISOString(),
      reviewHistory: reviewHistory,
      interval: interval
    };
  }

  /**
   * Obtiene todas las preguntas que deben repasarse hoy
   * @param {Array} questions - Array de preguntas con datos de repaso
   * @returns {Array} Preguntas que deben repasarse hoy
   */
  getDueQuestions(questions) {
    const dueQuestions = [];
    
    questions.forEach(q => {
      // Si no tiene fecha de próximo repaso, es nueva y debe repasarse
      if (!q.nextReviewDate) {
        dueQuestions.push({
          ...q,
          daysOverdue: 0,
          isNew: true
        });
        return;
      }
      
      // Verificar si está pendiente de repaso
      const nextDate = new Date(q.nextReviewDate);
      if (this.isDueToday(nextDate)) {
        const daysOverdue = -this.daysUntilReview(nextDate);
        dueQuestions.push({
          ...q,
          daysOverdue: daysOverdue,
          isNew: false
        });
      }
    });
    
    // Ordenar por prioridad: primero las más atrasadas
    dueQuestions.sort((a, b) => {
      if (a.isNew && !b.isNew) return 1;
      if (!a.isNew && b.isNew) return -1;
      return b.daysOverdue - a.daysOverdue;
    });
    
    return dueQuestions;
  }

  /**
   * Obtiene estadísticas de repasos
   * @param {Array} questions - Array de preguntas
   * @returns {object} Estadísticas de repasos
   */
  getStats(questions) {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const stats = {
      total: questions.length,
      dueToday: 0,
      upcoming: 0,
      completed: 0,
      new: 0,
      byMaterial: {}
    };
    
    questions.forEach(q => {
      // Contar por estado
      if (!q.nextReviewDate) {
        stats.new++;
      } else {
        const nextDate = new Date(q.nextReviewDate);
        if (this.isDueToday(nextDate)) {
          stats.dueToday++;
        } else if (nextDate > today) {
          stats.upcoming++;
        }
      }
      
      // Contar por material
      const materialId = q.material_id || q.carpeta_id || 'sin_material';
      if (!stats.byMaterial[materialId]) {
        stats.byMaterial[materialId] = {
          total: 0,
          dueToday: 0,
          upcoming: 0,
          new: 0
        };
      }
      stats.byMaterial[materialId].total++;
      
      if (!q.nextReviewDate) {
        stats.byMaterial[materialId].new++;
      } else if (this.isDueToday(new Date(q.nextReviewDate))) {
        stats.byMaterial[materialId].dueToday++;
      } else {
        stats.byMaterial[materialId].upcoming++;
      }
    });
    
    return stats;
  }

  /**
   * Obtiene el calendario de repasos para un mes
   * @param {Array} questions - Array de preguntas
   * @param {number} year - Año
   * @param {number} month - Mes (0-11)
   * @returns {object} Calendario con fechas y cantidad de repasos
   */
  getCalendar(questions, year, month) {
    const calendar = {};
    
    // Inicializar todos los días del mes
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      calendar[dateStr] = {
        date: dateStr,
        count: 0,
        questions: []
      };
    }
    
    // Contar repasos por día
    questions.forEach(q => {
      if (!q.nextReviewDate) return;
      
      const reviewDate = new Date(q.nextReviewDate);
      if (reviewDate.getFullYear() !== year || reviewDate.getMonth() !== month) return;
      
      const dateStr = reviewDate.toISOString().split('T')[0];
      if (calendar[dateStr]) {
        calendar[dateStr].count++;
        calendar[dateStr].questions.push(q);
      }
    });
    
    return calendar;
  }
}

// ===================================================================
// EXPORTAR INSTANCIA GLOBAL
// ===================================================================
window.SRS = new SpacedRepetitionSystem();

console.log('✅ Sistema de Repaso Espaciado inicializado');
