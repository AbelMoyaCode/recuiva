// 🔍 SCRIPT DE DIAGNÓSTICO - Sincronización de Scores
// Ejecuta este script en la consola del navegador (F12) para verificar que los scores estén sincronizados

console.clear();
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: cyan; font-weight: bold');
console.log('%c🔍 DIAGNÓSTICO DE SINCRONIZACIÓN DE SCORES', 'color: yellow; font-size: 16px; font-weight: bold');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'color: cyan; font-weight: bold');

// 1. Obtener todas las keys de localStorage relacionadas con preguntas
const questionKeys = Object.keys(localStorage).filter(key => key.startsWith('recuiva_questions_material_'));

if (questionKeys.length === 0) {
  console.log('%c⚠️ No se encontraron preguntas en localStorage', 'color: orange; font-size: 14px');
  console.log('\n💡 Crea algunas preguntas en Sesión Práctica y vuelve a ejecutar este script\n');
} else {
  console.log(`%c📚 Materiales encontrados: ${questionKeys.length}`, 'color: green; font-weight: bold');
  
  let totalQuestions = 0;
  let questionsWithDecimalScore = 0;
  let questionsWithPercentageScore = 0;
  
  questionKeys.forEach(key => {
    const materialId = key.replace('recuiva_questions_material_', '');
    const questions = JSON.parse(localStorage.getItem(key) || '[]');
    totalQuestions += questions.length;
    
    console.log(`\n%c─── Material ID: ${materialId} (${questions.length} preguntas) ───`, 'color: blue; font-weight: bold');
    
    if (questions.length === 0) {
      console.log('   %c(sin preguntas)', 'color: gray');
    } else {
      
      const table = questions.map((q, idx) => {
        const isDecimal = q.score >= 0 && q.score <= 1;
        if (isDecimal) questionsWithDecimalScore++;
        else questionsWithPercentageScore++;
        
        return {
          '#': idx + 1,
          'Pregunta': q.pregunta.substring(0, 40) + '...',
          'Score': q.score,
          'Formato': isDecimal ? '❌ Decimal (0.0-1.0)' : '✅ Porcentaje (0-100)',
          'Fecha': new Date(q.timestamp).toLocaleDateString('es-ES')
        };
      });
      
      console.table(table);
      
      // Calcular promedio
      const avgScore = questions.reduce((sum, q) => {
        const normalizedScore = q.score >= 0 && q.score <= 1 ? q.score * 100 : q.score;
        return sum + normalizedScore;
      }, 0) / questions.length;
      
      console.log(`   %c📊 Promedio del material: ${Math.round(avgScore)}%`, 'color: purple; font-weight: bold');
    }
  });
  
  console.log('\n%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: cyan; font-weight: bold');
  console.log('%c📈 RESUMEN GENERAL', 'color: yellow; font-size: 16px; font-weight: bold');
  console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'color: cyan; font-weight: bold');
  
  console.log(`%c   Total de preguntas: ${totalQuestions}`, 'font-weight: bold');
  console.log(`%c   ✅ Con formato correcto (0-100): ${questionsWithPercentageScore}`, 'color: green');
  console.log(`%c   ❌ Con formato decimal (0.0-1.0): ${questionsWithDecimalScore}`, 'color: red');
  
  if (questionsWithDecimalScore > 0) {
    console.log('\n%c⚠️ ACCIÓN REQUERIDA:', 'color: orange; font-size: 14px; font-weight: bold');
    console.log('%c   Hay preguntas con formato decimal (0.0-1.0)', 'color: orange');
    console.log('%c   Solución:', 'color: white; font-weight: bold');
    console.log('%c   1. Recarga la página (Ctrl+F5)', 'color: white');
    console.log('%c   2. El sistema las convertirá automáticamente a porcentaje (0-100)', 'color: white');
    console.log('%c   3. Ejecuta este script nuevamente para verificar', 'color: white');
  } else {
    console.log(`\n%c✅ TODOS LOS SCORES ESTÁN EN FORMATO CORRECTO (0-100)`, 'color: green; font-size: 14px; font-weight: bold');
    console.log('%c   Las métricas del dashboard están sincronizadas correctamente', 'color: green');
  }
  
  // Calcular promedio global
  const allQuestions = questionKeys.flatMap(key => JSON.parse(localStorage.getItem(key) || '[]'));
  if (allQuestions.length > 0) {
    const globalAvg = allQuestions.reduce((sum, q) => {
      const normalizedScore = q.score >= 0 && q.score <= 1 ? q.score * 100 : q.score;
      return sum + normalizedScore;
    }, 0) / allQuestions.length;
    
    console.log(`\n%c📊 PROMEDIO GLOBAL DE TODOS LOS MATERIALES: ${Math.round(globalAvg)}%`, 'color: purple; font-size: 14px; font-weight: bold');
  }
}

console.log('\n%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: cyan; font-weight: bold');
console.log('%c🔧 COMANDOS ÚTILES:', 'color: yellow; font-size: 16px; font-weight: bold');
console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'color: cyan; font-weight: bold');

console.log('%c// Ver todas las preguntas de un material específico:', 'color: gray');
console.log('%cconst questions = JSON.parse(localStorage.getItem("recuiva_questions_material_1"));', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 5px 0');
console.log('%cconsole.table(questions.map(q => ({ pregunta: q.pregunta, score: q.score })));', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 5px 0');

console.log('\n%c// Normalizar manualmente todas las preguntas (si es necesario):', 'color: gray');
console.log('%cObject.keys(localStorage).filter(k => k.startsWith("recuiva_questions_material_")).forEach(key => {', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 5px 0');
console.log('%c  const questions = JSON.parse(localStorage.getItem(key));', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 0');
console.log('%c  const normalized = questions.map(q => ({ ...q, score: q.score >= 0 && q.score <= 1 ? Math.round(q.score * 100) : q.score }));', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 0');
console.log('%c  localStorage.setItem(key, JSON.stringify(normalized));', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 0');
console.log('%c});', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 0');
console.log('%cconsole.log("✅ Scores normalizados correctamente");', 'background: #f0f0f0; color: black; padding: 5px; display: block; margin: 5px 0');

console.log('\n%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'color: cyan; font-weight: bold');
