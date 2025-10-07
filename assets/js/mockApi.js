/**
 * MockAPI para Recuiva - Sprint 1
 * Sistema centralizado de APIs mock con persistencia en localStorage
 * Preparado para migración a Flask + Supabase en Sprint 2
 */

class MockAPI {
  constructor() {
    this.initializeData();
  }

  initializeData() {
    // Usuarios por defecto
    if (!localStorage.getItem('recuiva_users')) {
      localStorage.setItem('recuiva_users', JSON.stringify([
        { 
          id: 'u1', 
          email: 'demo@recuiva.com', 
          password: 'demo123', 
          name: 'Usuario Demo',
          createdAt: '2025-09-20T10:00:00.000Z'
        },
        { 
          id: 'u2', 
          email: 'estudiante@upao.edu.pe', 
          password: 'upao2025', 
          name: 'Estudiante UPAO',
          createdAt: '2025-09-21T14:30:00.000Z'
        }
      ]));
    }
    
    // Sets de estudio por defecto
    if (!localStorage.getItem('recuiva_study_sets')) {
      localStorage.setItem('recuiva_study_sets', JSON.stringify([
        {
          id: 'set_1',
          userId: 'u1',
          title: 'Endodoncia - Pulpa Dental',
          questions: [
            { 
              id: 'q1', 
              question: '¿Qué es la pulpa dental?', 
              answer: 'Tejido conectivo ubicado en la cavidad pulpar del diente, contiene nervios, vasos sanguíneos y células especializadas. Es responsable de la vitalidad del diente.',
              difficulty: 2
            },
            { 
              id: 'q2', 
              question: '¿Cuáles son los síntomas de pulpitis?', 
              answer: 'Dolor intenso y punzante, sensibilidad térmica (especialmente al frío), dolor nocturno espontáneo, dolor al masticar.',
              difficulty: 3
            },
            { 
              id: 'q3', 
              question: '¿Qué es el tratamiento endodóntico?', 
              answer: 'Procedimiento para remover la pulpa infectada o dañada, limpiar y desinfectar los conductos radiculares, y sellarlos para prevenir reinfección.',
              difficulty: 1
            },
            { 
              id: 'q4', 
              question: '¿Cuándo está indicada la endodoncia?', 
              answer: 'Pulpitis irreversible, necrosis pulpar, periodontitis apical, traumatismos dentales, tratamientos protésicos que requieren desvitalización.',
              difficulty: 2
            },
            { 
              id: 'q5', 
              question: '¿Qué es la obturación del conducto?', 
              answer: 'Sellado tridimensional del espacio del conducto radicular con materiales biocompatibles, generalmente gutapercha y cemento sellador.',
              difficulty: 3
            }
          ],
          createdAt: '2025-09-22T09:15:00.000Z'
        },
        {
          id: 'set_2',
          userId: 'u1',
          title: 'Fisiología Cardiovascular',
          questions: [
            { 
              id: 'q6', 
              question: '¿Qué es el ciclo cardíaco?', 
              answer: 'Secuencia de eventos que ocurren durante un latido cardíaco, incluyendo sístole (contracción) y diástole (relajación).',
              difficulty: 2
            },
            { 
              id: 'q7', 
              question: '¿Cuál es la función del nodo sinoauricular?', 
              answer: 'Marcapasos natural del corazón, genera impulsos eléctricos que inician cada latido cardíaco a una frecuencia de 60-100 latidos por minuto.',
              difficulty: 3
            },
            { 
              id: 'q8', 
              question: '¿Qué es la presión arterial sistólica?', 
              answer: 'Presión máxima ejercida por la sangre contra las paredes arteriales durante la contracción ventricular (sístole). Valor normal: 120 mmHg.',
              difficulty: 1
            }
          ],
          createdAt: '2025-09-22T11:30:00.000Z'
        }
      ]));
    }
    
    // Progreso de repasos inicializado
    if (!localStorage.getItem('recuiva_review_progress')) {
      localStorage.setItem('recuiva_review_progress', JSON.stringify({}));
    }

    // Chunks de PDF mock
    if (!localStorage.getItem('recuiva_prepared_chunks')) {
      localStorage.setItem('recuiva_prepared_chunks', JSON.stringify([]));
    }

    // Embeddings mock
    if (!localStorage.getItem('recuiva_embeddings')) {
      localStorage.setItem('recuiva_embeddings', JSON.stringify([]));
    }
  }

  // === AUTH APIs ===
  async apiLoginMock(email, password) {
    await this.simulateDelay(500);
    const users = JSON.parse(localStorage.getItem('recuiva_users') || '[]');
    const user = users.find(u => u.email === email && u.password === password);
    
    if (user) {
      const token = 'mock_token_' + Date.now();
      const userSession = { ...user, token, loginAt: new Date().toISOString() };
      delete userSession.password; // No guardar password en sesión
      
      localStorage.setItem('recuiva_current_user', JSON.stringify(userSession));
      return { ok: true, token, userId: user.id, user: userSession };
    }
    return { ok: false, error: 'Credenciales incorrectas' };
  }

  async apiRegisterMock(userData) {
    await this.simulateDelay(700);
    const users = JSON.parse(localStorage.getItem('recuiva_users') || '[]');
    
    if (users.find(u => u.email === userData.email)) {
      return { ok: false, error: 'Email ya registrado' };
    }
    
    const newUser = {
      id: 'u' + Date.now(),
      email: userData.email,
      password: userData.password,
      name: userData.name || userData.email.split('@')[0],
      createdAt: new Date().toISOString()
    };
    
    users.push(newUser);
    localStorage.setItem('recuiva_users', JSON.stringify(users));
    
    // Auto-login después del registro
    const token = 'mock_token_' + Date.now();
    const userSession = { ...newUser, token, loginAt: new Date().toISOString() };
    delete userSession.password;
    
    localStorage.setItem('recuiva_current_user', JSON.stringify(userSession));
    
    return { ok: true, userId: newUser.id, user: userSession, token };
  }

  // === SETS/MATERIALES APIs ===
  async apiCreateSetMock(payload) {
    await this.simulateDelay(800);
    const sets = JSON.parse(localStorage.getItem('recuiva_study_sets') || '[]');
    const user = this.getCurrentUser();
    
    if (!user) {
      return { ok: false, error: 'Usuario no autenticado' };
    }
    
    const newSet = {
      id: 'set_' + Date.now(),
      userId: user.id,
      title: payload.title,
      questions: this.generateQuestionsFromText(payload.content),
      createdAt: new Date().toISOString()
    };
    
    sets.push(newSet);
    localStorage.setItem('recuiva_study_sets', JSON.stringify(sets));
    localStorage.setItem('recuiva_current_study_set', JSON.stringify(newSet));
    
    return { ok: true, setId: newSet.id, set: newSet };
  }

  async apiListSetsMock(userId) {
    await this.simulateDelay(300);
    const sets = JSON.parse(localStorage.getItem('recuiva_study_sets') || '[]');
    const userSets = sets.filter(set => set.userId === userId);
    return { ok: true, sets: userSets };
  }

  // === REVIEWS APIs ===
  async apiLoadTodayReviewsMock(userId) {
    await this.simulateDelay(400);
    const mockReviews = [
      {
        id: 'rev_1',
        setId: 'set_1',
        setTitle: 'Endodoncia - Pulpa Dental',
        questionsCount: 5,
        status: 'vencido',
        daysOverdue: 2,
        lastScore: 0.58,
        currentInterval: 1,
        priority: 'urgent',
        nextReview: '2025-09-21T09:00:00.000Z'
      },
      {
        id: 'rev_2',
        setId: 'set_2',
        setTitle: 'Fisiología Cardiovascular',
        questionsCount: 3,
        status: 'hoy',
        daysOverdue: 0,
        lastScore: 0.78,
        currentInterval: 14,
        priority: 'normal',
        nextReview: '2025-09-23T10:00:00.000Z'
      },
      {
        id: 'rev_3',
        setId: 'set_3',
        setTitle: 'Farmacología Básica',
        questionsCount: 4,
        status: 'bonus',
        daysOverdue: -1,
        lastScore: 0.91,
        currentInterval: 30,
        priority: 'optional',
        nextReview: '2025-09-24T15:00:00.000Z'
      }
    ];
    
    return { ok: true, items: mockReviews };
  }

  async apiSaveReviewResultMock(result) {
    await this.simulateDelay(200);
    const progress = JSON.parse(localStorage.getItem('recuiva_review_progress') || '{}');
    
    // Algoritmo de intervalos espaciados
    const newInterval = this.calculateNewInterval(result.currentInterval || 1, result.score);
    const nextReviewDate = new Date(Date.now() + newInterval * 24 * 60 * 60 * 1000);
    
    progress[result.questionId] = {
      ...result,
      newInterval,
      nextReviewDate: nextReviewDate.toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    localStorage.setItem('recuiva_review_progress', JSON.stringify(progress));
    return { ok: true, newInterval, nextReviewDate: nextReviewDate.toISOString() };
  }

  // === PDF/EMBEDDINGS APIs ===
  async apiProcessPdfMock(file) {
    await this.simulateDelay(1500);
    
    // Mock de procesamiento de PDF
    const mockChunks = [
      { 
        id: 'chunk_1', 
        content: 'La pulpa dental es un tejido conectivo ubicado en la cavidad pulpar del diente. Contiene nervios, vasos sanguíneos y células especializadas como odontoblastos.', 
        page: 1,
        startChar: 0,
        endChar: 150
      },
      { 
        id: 'chunk_2', 
        content: 'Los síntomas de pulpitis incluyen dolor intenso, sensibilidad térmica y dolor nocturno. La pulpitis puede ser reversible o irreversible según el grado de inflamación.', 
        page: 1,
        startChar: 151,
        endChar: 320
      },
      { 
        id: 'chunk_3', 
        content: 'El tratamiento endodóntico consiste en la eliminación de la pulpa infectada, limpieza y desinfección de los conductos radiculares, y posterior obturación.', 
        page: 2,
        startChar: 0,
        endChar: 155
      },
      { 
        id: 'chunk_4', 
        content: 'La obturación del conducto se realiza con gutapercha y cemento sellador, proporcionando un sellado tridimensional para prevenir la reinfección.', 
        page: 2,
        startChar: 156,
        endChar: 300
      }
    ];
    
    localStorage.setItem('recuiva_prepared_chunks', JSON.stringify(mockChunks));
    return { ok: true, chunks: mockChunks, fileName: file.name };
  }

  async apiGenerateEmbeddingsMock(chunks) {
    await this.simulateDelay(1000);
    
    // Mock de embeddings (simular MiniLM-L6-v2 de 384 dimensiones)
    const mockVectors = chunks.map((chunk, i) => ({
      id: chunk.id,
      vector: Array(384).fill(0).map(() => Math.random() * 2 - 1), // Vectores aleatorios [-1, 1]
      metadata: { 
        content: chunk.content, 
        page: chunk.page,
        chunkId: chunk.id,
        length: chunk.content.length
      }
    }));
    
    localStorage.setItem('recuiva_embeddings', JSON.stringify(mockVectors));
    return { ok: true, vectors: mockVectors, model: 'sentence-transformers/all-MiniLM-L6-v2' };
  }

  // === UTILIDADES ===
  generateQuestionsFromText(text) {
    // Generador simple de preguntas mock desde texto
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 20);
    const questions = [];
    
    sentences.slice(0, Math.min(5, sentences.length)).forEach((sentence, i) => {
      const cleanSentence = sentence.trim();
      if (cleanSentence.length > 0) {
        questions.push({
          id: 'q_' + Date.now() + '_' + i,
          question: `¿Qué significa: "${cleanSentence.substring(0, 50)}${cleanSentence.length > 50 ? '...' : ''}"?`,
          answer: cleanSentence,
          difficulty: Math.floor(Math.random() * 3) + 1 // 1-3
        });
      }
    });
    
    // Si el texto es muy corto, crear al menos una pregunta
    if (questions.length === 0) {
      questions.push({
        id: 'q_' + Date.now() + '_default',
        question: '¿Cuál es el concepto principal de este material?',
        answer: text.substring(0, 200) + (text.length > 200 ? '...' : ''),
        difficulty: 2
      });
    }
    
    return questions;
  }

  calculateNewInterval(currentInterval, score) {
    // Algoritmo de intervalos espaciados basado en SM-2 simplificado
    switch(score) {
      case 1: // Mala
        return 1; // Resetear a 1 día
      case 2: // Regular  
        return Math.max(1, Math.floor(currentInterval * 0.5)); // Reducir 50%
      case 3: // Buena
        return currentInterval; // Mantener intervalo actual
      case 4: // Excelente
        return Math.floor(currentInterval * 1.3); // Incrementar 30%
      default:
        return currentInterval;
    }
  }

  async simulateDelay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  getCurrentUser() {
    try {
      return JSON.parse(localStorage.getItem('recuiva_current_user') || 'null');
    } catch (e) {
      return null;
    }
  }

  isAuthenticated() {
    const user = this.getCurrentUser();
    return !!(user && user.token);
  }

  logout() {
    localStorage.removeItem('recuiva_current_user');
    return { ok: true };
  }

  // === MÉTRICAS Y ESTADÍSTICAS MOCK ===
  async getStudyStatsMock(userId) {
    await this.simulateDelay(300);
    
    const sets = JSON.parse(localStorage.getItem('recuiva_study_sets') || '[]');
    const userSets = sets.filter(s => s.userId === userId);
    const progress = JSON.parse(localStorage.getItem('recuiva_review_progress') || '{}');
    
    const totalQuestions = userSets.reduce((sum, set) => sum + set.questions.length, 0);
    const reviewsCompleted = Object.keys(progress).length;
    const avgScore = reviewsCompleted > 0 ? 
      Object.values(progress).reduce((sum, p) => sum + (p.score || 0), 0) / reviewsCompleted : 0;
    
    return {
      ok: true,
      stats: {
        totalSets: userSets.length,
        totalQuestions,
        reviewsCompleted,
        averageScore: Math.round(avgScore * 100) / 100,
        studyStreak: Math.floor(Math.random() * 7) + 1, // Mock streak
        weeklyProgress: [0.65, 0.72, 0.78, 0.81, 0.85, 0.88, 0.91] // Mock weekly data
      }
    };
  }
}

// Instancia global
window.mockAPI = new MockAPI();

// Log para debug
console.log('🧠 Recuiva MockAPI v1.0 cargado - Sprint 1');
console.log('📊 Datos inicializados en localStorage');