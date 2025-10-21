/**
 * Script para validación semántica REAL usando el backend FastAPI
 * Conecta directamente con el modelo de embeddings
 * 
 * Autor: Abel Jesús Moya Acosta
 * Fecha: 7 de octubre de 2025
 */

// Configuración del API
const API_BASE = 'https://api-recuiva.duckdns.org';

// Instancia del API
const recuivaAPI = new RecuivaAPI(API_BASE);

// Estado de la sesión
let currentQuestion = null;
let sessionHistory = [];
let currentMaterialId = null;

/**
 * Inicializar la sesión de práctica
 */
async function initPracticeSession() {
    console.log('🚀 Iniciando sesión de práctica con backend real...');
    
    // Obtener parámetros de la URL
    const urlParams = new URLSearchParams(window.location.search);
    const carpetaId = urlParams.get('carpeta');
    const materialNuevo = urlParams.get('material');
    
    console.log('📁 Carpeta:', carpetaId);
    console.log('📄 Material nuevo:', materialNuevo);
    
    // Verificar conexión con backend
    try {
        const healthCheck = await fetch(`${API_BASE}/api/health`);
        if (healthCheck.ok) {
            console.log('✅ Backend conectado');
            showNotification('Conexión establecida con el motor de IA', 'success');
        }
    } catch (error) {
        console.error('❌ Backend no disponible:', error);
        showNotification('No se puede conectar con el backend. Usando modo demo.', 'warning');
        return useDemoMode();
    }
    
    // Cargar modelo si no está cargado
    try {
        const modelStatus = await fetch(`${API_BASE}/api/model/status`);
        const status = await modelStatus.json();
        
        if (!status.loaded) {
            console.log('📥 Cargando modelo de embeddings...');
            showNotification('Cargando modelo de IA... esto puede tardar unos segundos', 'info');
            
            const loadResponse = await fetch(`${API_BASE}/api/model/load`, {
                method: 'POST'
            });
            
            if (loadResponse.ok) {
                console.log('✅ Modelo cargado exitosamente');
                showNotification('Modelo de IA cargado correctamente', 'success');
            }
        } else {
            console.log('✅ Modelo ya está cargado');
        }
    } catch (error) {
        console.error('Error cargando modelo:', error);
    }
    
    // Cargar materiales y generar primera pregunta
    await loadMaterialsAndGenerateQuestion();
}

/**
 * Cargar materiales y generar pregunta
 */
async function loadMaterialsAndGenerateQuestion() {
    try {
        // Obtener lista de materiales
        const materialsResponse = await recuivaAPI.getMaterials();
        
        if (materialsResponse.success && materialsResponse.materials.length > 0) {
            // Usar el primer material disponible
            currentMaterialId = materialsResponse.materials[0].id;
            console.log('📚 Material seleccionado ID:', currentMaterialId);
            
            // Generar pregunta
            await generateQuestion();
        } else {
            console.log('⚠️ No hay materiales procesados');
            showNotification('No hay materiales procesados. Por favor, sube un PDF primero.', 'warning');
            
            // Mostrar pregunta de ejemplo
            showSampleQuestion();
        }
    } catch (error) {
        console.error('Error cargando materiales:', error);
        showSampleQuestion();
    }
}

/**
 * Generar pregunta basada en el material
 */
async function generateQuestion() {
    const questions = [
        "¿Cuál es el concepto principal que se aborda en el material?",
        "Explica con tus propias palabras la idea central del texto",
        "¿Qué aspectos importantes menciona el autor sobre este tema?",
        "¿Cómo se relaciona este concepto con otros temas similares?",
        "Describe las características más relevantes mencionadas",
        "¿Qué aplicaciones prácticas tiene este conocimiento?",
        "Analiza los puntos clave que se desarrollan en el material",
        "¿Cuáles son las implicaciones de lo expuesto en el texto?"
    ];
    
    // Seleccionar pregunta aleatoria
    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
    
    currentQuestion = {
        id: Date.now(),
        text: randomQuestion,
        material_id: currentMaterialId,
        timestamp: new Date().toISOString()
    };
    
    displayQuestion(currentQuestion);
}

/**
 * Mostrar pregunta en la interfaz
 */
function displayQuestion(question) {
    const questionElement = document.getElementById('current-question');
    if (questionElement) {
        questionElement.textContent = question.text;
    }
    
    // Limpiar respuesta anterior
    const answerInput = document.getElementById('user-answer');
    if (answerInput) {
        answerInput.value = '';
    }
    
    // Ocultar resultado anterior
    const resultContainer = document.getElementById('validation-result');
    if (resultContainer) {
        resultContainer.style.display = 'none';
    }
    
    console.log('❓ Pregunta mostrada:', question.text);
}

/**
 * Validar respuesta del usuario usando el backend REAL
 */
async function validateAnswer() {
    const answerInput = document.getElementById('user-answer');
    const userAnswer = answerInput ? answerInput.value.trim() : '';
    
    if (!userAnswer) {
        showNotification('Por favor, escribe una respuesta', 'warning');
        return;
    }
    
    if (!currentQuestion) {
        showNotification('No hay pregunta activa', 'error');
        return;
    }
    
    console.log('🔍 Validando respuesta:', userAnswer);
    showNotification('Validando tu respuesta con IA...', 'info');
    
    // Mostrar loading
    const submitBtn = document.getElementById('submit-answer');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Validando...';
    }
    
    try {
        // Llamar al API real de validación
        const validation = await recuivaAPI.validateAnswer(currentQuestion.id, userAnswer);
        
        console.log('✅ Respuesta validada:', validation);
        
        // Mostrar resultado
        displayValidationResult(validation);
        
        // Guardar en historial
        sessionHistory.push({
            question: currentQuestion,
            answer: userAnswer,
            validation: validation,
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('❌ Error validando respuesta:', error);
        showNotification('Error al validar la respuesta: ' + error.message, 'error');
        
        // Fallback: validación simple
        displaySimpleValidation(userAnswer);
    } finally {
        // Restaurar botón
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Validar Respuesta';
        }
    }
}

/**
 * Mostrar resultado de la validación
 */
function displayValidationResult(validation) {
    // Llamar a la función principal de visualización (estilo Python GUI)
    if (typeof window.showValidationResult === 'function') {
        window.showValidationResult({
            score: validation.score / 100, // Convertir a decimal (0-1)
            feedback: validation.feedback,
            relevantChunks: validation.relevant_chunks ? validation.relevant_chunks.map(chunk => ({
                content: chunk.content || chunk,
                similarity: chunk.similarity || validation.score / 100
            })) : [],
            bestMatchChunk: validation.best_match_chunk
        });
        return;
    }
    
    // Fallback: código original si no existe showValidationResult
    const resultContainer = document.getElementById('validation-result');
    if (!resultContainer) return;
    
    // Determinar color según score
    let scoreClass = 'text-red-600';
    let emoji = '😞';
    
    if (validation.score >= 90) {
        scoreClass = 'text-green-600';
        emoji = '🌟';
    } else if (validation.score >= 70) {
        scoreClass = 'text-blue-600';
        emoji = '👍';
    } else if (validation.score >= 50) {
        scoreClass = 'text-yellow-600';
        emoji = '📚';
    }
    
    resultContainer.innerHTML = `
        <div class="bg-white p-6 rounded-xl shadow-lg border-2 border-gray-200">
            <div class="text-center mb-4">
                <div class="text-6xl mb-2">${emoji}</div>
                <div class="text-3xl font-bold ${scoreClass}">${validation.score}%</div>
                <div class="text-gray-600 mt-2">Similaridad Semántica</div>
            </div>
            
            <div class="mb-4">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-sm text-gray-600">Precisión</span>
                    <span class="text-sm font-bold">${validation.score}%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-3">
                    <div class="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-500" 
                         style="width: ${validation.score}%"></div>
                </div>
            </div>
            
            <div class="bg-gray-50 p-4 rounded-lg mb-4">
                <p class="text-sm text-gray-700">${validation.feedback}</p>
            </div>
            
            ${validation.best_match_chunk ? `
                <details class="mt-4">
                    <summary class="cursor-pointer text-sm text-blue-600 hover:text-blue-800">
                        Ver fragmento más similar del material
                    </summary>
                    <div class="mt-2 p-3 bg-blue-50 rounded text-sm text-gray-700">
                        "${validation.best_match_chunk}"
                    </div>
                </details>
            ` : ''}
            
            <div class="mt-4 flex gap-2">
                <button onclick="generateQuestion()" 
                        class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Siguiente Pregunta →
                </button>
                <button onclick="showHistory()" 
                        class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">
                    Ver Historial
                </button>
            </div>
        </div>
    `;
    
    resultContainer.style.display = 'block';
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Validación simple como fallback
 */
function displaySimpleValidation(userAnswer) {
    const wordCount = userAnswer.split(/\s+/).length;
    const score = Math.min(100, Math.max(40, wordCount * 5));
    
    displayValidationResult({
        score: score,
        is_correct: score >= 70,
        feedback: score >= 70 
            ? 'Respuesta aceptable. Has demostrado comprensión del tema.' 
            : 'Tu respuesta podría ser más completa. Intenta desarrollar más las ideas.',
        similarity: score / 100,
        best_match_chunk: null
    });
}

/**
 * Mostrar pregunta de ejemplo (modo demo)
 */
function showSampleQuestion() {
    currentQuestion = {
        id: 1,
        text: "¿Qué es Active Recall y cómo ayuda en el aprendizaje?",
        material_id: null,
        timestamp: new Date().toISOString()
    };
    
    displayQuestion(currentQuestion);
    showNotification('Usando pregunta de ejemplo. Sube un PDF para preguntas personalizadas.', 'info');
}

/**
 * Usar modo demo sin backend
 */
function useDemoMode() {
    console.log('📝 Modo demo activado');
    showSampleQuestion();
}

/**
 * Mostrar notificación
 */
function showNotification(message, type = 'info') {
    // Implementación simple de notificaciones
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        type === 'warning' ? 'bg-yellow-500' :
        'bg-blue-500'
    } text-white`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

/**
 * Mostrar historial de respuestas
 */
function showHistory() {
    if (sessionHistory.length === 0) {
        showNotification('No hay historial de respuestas aún', 'info');
        return;
    }
    
    console.log('📊 Historial de sesión:', sessionHistory);
    
    // Calcular estadísticas
    const avgScore = sessionHistory.reduce((acc, item) => acc + item.validation.score, 0) / sessionHistory.length;
    const correctAnswers = sessionHistory.filter(item => item.validation.is_correct).length;
    
    alert(`Estadísticas de la sesión:
    
📊 Preguntas respondidas: ${sessionHistory.length}
✅ Respuestas correctas: ${correctAnswers}
📈 Promedio de score: ${avgScore.toFixed(1)}%
    `);
}

// Inicializar cuando la página cargue
document.addEventListener('DOMContentLoaded', initPracticeSession);

// Exportar funciones globales
window.validateAnswer = validateAnswer;
window.generateQuestion = generateQuestion;
window.showHistory = showHistory;
