/**
 * Script para validación semántica de respuestas
 * Maneja la interfaz de Active Recall y la validación con IA
 * 
 * Autor: Abel Jesús Moya Acosta
 * Usar en: src/pages/sesion-practica.html
 */

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🧠 Inicializando módulo de validación semántica...');

    // Verificar conexión con backend
    const isConnected = await api.checkConnection();
    
    if (!isConnected) {
        const container = document.querySelector('.practice-container') || document.body;
        const errorDiv = document.createElement('div');
        errorDiv.innerHTML = api.showConnectionError();
        container.prepend(errorDiv);
        // Continuar para modo offline con preguntas de ejemplo
    }

    // Elementos del DOM
    const questionElement = document.getElementById('question-text') || document.querySelector('.question-text');
    const answerInput = document.getElementById('answer-input') || document.querySelector('textarea[name="answer"]');
    const submitButton = document.getElementById('submit-answer') || document.querySelector('button[type="submit"]');
    const resultContainer = document.getElementById('validation-result') || document.getElementById('result');
    const nextButton = document.getElementById('next-question');

    // Estado de la sesión
    let currentQuestion = null;
    let questionHistory = [];

    // Preguntas de ejemplo (fallback si no hay backend)
    const sampleQuestions = [
        {
            id: 1,
            text: "¿Qué es un grafo dirigido?",
            topic: "Grafos",
            difficulty: "medium",
            material_id: 1
        },
        {
            id: 2,
            text: "Explica el concepto de Active Recall",
            topic: "Aprendizaje",
            difficulty: "easy",
            material_id: 1
        },
        {
            id: 3,
            text: "¿Qué es la similaridad coseno y cómo se calcula?",
            topic: "Machine Learning",
            difficulty: "hard",
            material_id: 1
        }
    ];

    // Cargar pregunta inicial
    await loadQuestion();

    // Event listeners
    if (submitButton) {
        submitButton.addEventListener('click', handleSubmitAnswer);
    }

    if (nextButton) {
        nextButton.addEventListener('click', loadQuestion);
    }

    // También permitir Enter para enviar (pero Shift+Enter para nueva línea)
    if (answerInput) {
        answerInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmitAnswer();
            }
        });
    }

    // Funciones principales
    async function loadQuestion() {
        try {
            if (isConnected) {
                // Intentar obtener preguntas del backend
                const response = await api.getQuestions({ difficulty: 'medium' });
                
                if (response.questions && response.questions.length > 0) {
                    currentQuestion = response.questions[Math.floor(Math.random() * response.questions.length)];
                } else {
                    // Si no hay preguntas, usar ejemplos
                    currentQuestion = sampleQuestions[Math.floor(Math.random() * sampleQuestions.length)];
                }
            } else {
                // Modo offline: usar preguntas de ejemplo
                currentQuestion = sampleQuestions[Math.floor(Math.random() * sampleQuestions.length)];
            }

            displayQuestion(currentQuestion);
            
        } catch (error) {
            console.error('Error cargando pregunta:', error);
            // Usar pregunta de ejemplo como fallback
            currentQuestion = sampleQuestions[0];
            displayQuestion(currentQuestion);
        }
    }

    function displayQuestion(question) {
        if (questionElement) {
            questionElement.innerHTML = `
                <div class="question-header" style="margin-bottom: 20px;">
                    <span class="question-topic" style="display: inline-block; background: #e3f2fd; color: #1976d2; padding: 4px 12px; border-radius: 12px; font-size: 0.9em; margin-bottom: 10px;">
                        ${question.topic || 'General'}
                    </span>
                    <span class="question-difficulty" style="display: inline-block; background: ${getDifficultyColor(question.difficulty)}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.9em; margin-left: 8px;">
                        ${getDifficultyLabel(question.difficulty)}
                    </span>
                </div>
                <h2 style="color: #333; margin: 15px 0; font-size: 1.3em;">${question.text}</h2>
                <p style="color: #666; font-size: 0.9em; margin-top: 10px;">
                    💡 Escribe tu respuesta con tus propias palabras. El sistema validará semánticamente tu comprensión del tema.
                </p>
            `;
        }

        // Limpiar respuesta anterior
        if (answerInput) {
            answerInput.value = '';
            answerInput.focus();
        }

        // Limpiar resultado anterior
        if (resultContainer) {
            resultContainer.innerHTML = '';
        }

        // Habilitar botón de enviar
        if (submitButton) {
            submitButton.disabled = false;
        }
    }

    async function handleSubmitAnswer() {
        if (!currentQuestion) {
            showError('No hay pregunta cargada');
            return;
        }

        const userAnswer = answerInput ? answerInput.value.trim() : '';

        if (!userAnswer) {
            showError('Por favor escribe tu respuesta');
            return;
        }

        if (userAnswer.length < 20) {
            const confirm = window.confirm('Tu respuesta es muy corta. ¿Estás seguro de que quieres continuar?');
            if (!confirm) return;
        }

        // Deshabilitar botón mientras se valida
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = '🧠 Validando...';
        }

        // Mostrar loading
        showLoading();

        try {
            // Validar con el backend
            const validation = await api.validateAnswer(currentQuestion.id, userAnswer);

            // Mostrar resultado
            showValidationResult(validation);

            // Agregar a historial
            questionHistory.push({
                question: currentQuestion,
                answer: userAnswer,
                validation: validation,
                timestamp: new Date().toISOString()
            });

        } catch (error) {
            console.error('Error validando respuesta:', error);
            showError(`Error al validar: ${error.message}`);
        } finally {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = '📝 Enviar Respuesta';
            }
        }
    }

    function showLoading() {
        if (!resultContainer) return;

        resultContainer.innerHTML = `
            <div class="loading" style="text-align: center; padding: 40px;">
                <div class="spinner" style="border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px;"></div>
                <p style="color: #666;">Analizando tu respuesta semánticamente...</p>
            </div>
        `;
    }

    function showValidationResult(validation) {
        if (!resultContainer) return;

        const scoreColor = validation.is_correct ? '#4CAF50' : validation.score > 50 ? '#FF9800' : '#f44336';
        const scoreEmoji = validation.score >= 90 ? '🌟' : validation.score >= 70 ? '✅' : validation.score >= 50 ? '⚠️' : '❌';

        resultContainer.innerHTML = `
            <div class="validation-result" style="background: ${validation.is_correct ? '#e8f5e9' : '#fff3e0'}; border-left: 5px solid ${scoreColor}; padding: 25px; border-radius: 8px; margin: 20px 0; animation: slideIn 0.3s ease;">
                <h3 style="color: ${scoreColor}; margin-top: 0; font-size: 1.4em;">
                    ${scoreEmoji} ${validation.is_correct ? 'Correcto' : 'Necesitas mejorar'}
                </h3>
                
                <div class="score-container" style="margin: 20px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span style="font-weight: bold; color: #555;">Puntuación:</span>
                        <span style="font-size: 1.5em; font-weight: bold; color: ${scoreColor};">${validation.score}%</span>
                    </div>
                    <div class="score-bar" style="width: 100%; height: 30px; background: #e0e0e0; border-radius: 15px; overflow: hidden; position: relative;">
                        <div class="score-fill" style="width: ${validation.score}%; height: 100%; background: linear-gradient(90deg, ${scoreColor}, ${scoreColor}dd); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; transition: width 1s ease;">
                            ${validation.score}%
                        </div>
                    </div>
                </div>

                <div style="background: white; padding: 15px; border-radius: 6px; margin: 15px 0;">
                    <p style="margin: 0; color: #555;"><strong>📊 Similaridad semántica:</strong> ${(validation.similarity * 100).toFixed(2)}%</p>
                </div>

                <div class="feedback" style="background: white; padding: 20px; border-radius: 6px; border-left: 3px solid ${scoreColor};">
                    <p style="margin: 0; font-size: 1.05em; line-height: 1.6; color: #333;">
                        ${validation.feedback}
                    </p>
                </div>

                ${validation.best_match_chunk ? `
                    <details style="margin-top: 15px; background: white; padding: 15px; border-radius: 6px;">
                        <summary style="cursor: pointer; font-weight: bold; color: #1976d2;">
                            📚 Ver fragmento más similar del material
                        </summary>
                        <p style="margin: 15px 0 0 0; padding: 15px; background: #f5f5f5; border-radius: 4px; font-size: 0.95em; line-height: 1.6; color: #555;">
                            "${validation.best_match_chunk}"
                        </p>
                    </details>
                ` : ''}

                <div style="display: flex; gap: 10px; margin-top: 20px;">
                    <button onclick="location.reload()" style="flex: 1; background: ${scoreColor}; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-size: 1em; font-weight: bold;">
                        ➡️ Siguiente Pregunta
                    </button>
                    <button onclick="document.getElementById('answer-input').value = ''; document.getElementById('validation-result').innerHTML = ''" style="flex: 1; background: #757575; color: white; border: none; padding: 12px 20px; border-radius: 6px; cursor: pointer; font-size: 1em;">
                        🔄 Intentar de Nuevo
                    </button>
                </div>
            </div>

            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                @keyframes slideIn {
                    from {
                        opacity: 0;
                        transform: translateY(-20px);
                    }
                    to {
                        opacity: 1;
                        transform: translateY(0);
                    }
                }
            </style>
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
                <p style="margin: 0; color: #d32f2f;">❌ ${message}</p>
            </div>
        `;
    }

    function getDifficultyColor(difficulty) {
        const colors = {
            'easy': '#4caf50',
            'medium': '#ff9800',
            'hard': '#f44336'
        };
        return colors[difficulty] || '#2196f3';
    }

    function getDifficultyLabel(difficulty) {
        const labels = {
            'easy': 'Fácil',
            'medium': 'Medio',
            'hard': 'Difícil'
        };
        return labels[difficulty] || difficulty;
    }

    console.log('✅ Módulo de validación semántica listo');
});
