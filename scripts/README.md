# 🔧 Scripts de Diagnóstico y Utilidades

Este directorio contiene scripts útiles para diagnosticar y solucionar problemas en Recuiva.

---

## 📊 `diagnostico-scores.js`

### ¿Para qué sirve?

Este script verifica que los **scores de las preguntas** estén correctamente sincronizados entre:
- 🎴 Tarjetas de preguntas en Sesión Práctica
- 📊 Métricas del Dashboard
- 💾 localStorage del navegador

### ¿Cuándo usarlo?

- ✅ Después de actualizar Recuiva a una nueva versión
- ✅ Si ves que los promedios del dashboard no coinciden con los scores individuales
- ✅ Para verificar que la migración automática funcionó correctamente
- ✅ Para hacer una auditoría de los datos guardados

### 🚀 Cómo ejecutarlo

#### Opción 1: Desde la consola del navegador

1. **Abre Recuiva** en tu navegador
2. **Presiona F12** para abrir las DevTools
3. **Ve a la pestaña "Console"**
4. **Copia y pega** el contenido completo de `diagnostico-scores.js`
5. **Presiona Enter**

#### Opción 2: Como Snippet (recomendado)

1. **Abre las DevTools** (F12)
2. **Ve a la pestaña "Sources"**
3. **En el panel izquierdo**, haz clic en **"Snippets"**
4. **Haz clic en "New snippet"**
5. **Nómbralo:** `Diagnóstico Scores`
6. **Pega el contenido** de `diagnostico-scores.js`
7. **Guarda** (Ctrl+S)
8. **Ejecuta** haciendo clic derecho → "Run"

### 📊 Qué información muestra

El script te mostrará:

#### 1. **Materiales y Preguntas**
```
📚 Materiales encontrados: 3

─── Material ID: 1 (5 preguntas) ───
┌───┬──────────────────────────┬────────┬─────────────────────┬────────────┐
│ # │ Pregunta                  │ Score  │ Formato             │ Fecha      │
├───┼──────────────────────────┼────────┼─────────────────────┼────────────┤
│ 1 │ ¿Qué es la pulpa dental? │ 69     │ ✅ Porcentaje       │ 11/10/2025 │
│ 2 │ ¿Cuál es la función...   │ 0.81   │ ❌ Decimal          │ 12/10/2025 │
└───┴──────────────────────────┴────────┴─────────────────────┴────────────┘

   📊 Promedio del material: 75%
```

#### 2. **Resumen General**
```
📈 RESUMEN GENERAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Total de preguntas: 12
   ✅ Con formato correcto (0-100): 8
   ❌ Con formato decimal (0.0-1.0): 4
```

#### 3. **Acciones Recomendadas**

Si encuentra preguntas con formato decimal:
```
⚠️ ACCIÓN REQUERIDA:
   Hay preguntas con formato decimal (0.0-1.0)
   Solución:
   1. Recarga la página (Ctrl+F5)
   2. El sistema las convertirá automáticamente
   3. Ejecuta este script nuevamente para verificar
```

Si todo está bien:
```
✅ TODOS LOS SCORES ESTÁN EN FORMATO CORRECTO (0-100)
   Las métricas del dashboard están sincronizadas correctamente

📊 PROMEDIO GLOBAL DE TODOS LOS MATERIALES: 74%
```

#### 4. **Comandos Útiles**

Al final del diagnóstico, se muestran comandos que puedes copiar y pegar para:
- Ver todas las preguntas de un material específico
- Normalizar manualmente todas las preguntas (si es necesario)

---

## 🔧 Solución de Problemas

### Problema: Scores en formato decimal (0.0-1.0)

**Síntoma:**
```
❌ Con formato decimal (0.0-1.0): 4
```

**Solución automática:**
1. **Recarga la página** (Ctrl+F5)
2. El sistema detectará automáticamente los scores en formato decimal
3. Los convertirá a porcentaje (0-100)
4. Los guardará en localStorage

**Solución manual (si la automática falla):**

Ejecuta este código en la consola:
```javascript
Object.keys(localStorage)
  .filter(k => k.startsWith("recuiva_questions_material_"))
  .forEach(key => {
    const questions = JSON.parse(localStorage.getItem(key));
    const normalized = questions.map(q => ({ 
      ...q, 
      score: q.score >= 0 && q.score <= 1 
        ? Math.round(q.score * 100) 
        : q.score 
    }));
    localStorage.setItem(key, JSON.stringify(normalized));
  });

console.log("✅ Scores normalizados correctamente");
```

### Problema: Promedio del dashboard no coincide con los scores individuales

**Diagnóstico:**
1. Ejecuta `diagnostico-scores.js`
2. Verifica que **todos** los scores estén en formato **0-100**
3. Compara el **promedio global** del script con el del dashboard

**Solución:**
- Si hay scores en formato decimal → Sigue los pasos de "Solución automática" arriba
- Si todos están en formato correcto → Recarga el dashboard (Ctrl+F5)

---

## 📁 Otros Scripts (próximamente)

Este directorio se irá expandiendo con más utilidades:

- [ ] `diagnostico-materiales.js` - Verificar materiales cargados
- [ ] `diagnostico-embeddings.js` - Verificar chunks y embeddings
- [ ] `limpiar-storage.js` - Limpiar localStorage de forma segura
- [ ] `exportar-datos.js` - Exportar todas las preguntas a JSON
- [ ] `importar-datos.js` - Importar preguntas desde JSON

---

## 🛠️ Desarrollo

### Cómo crear un nuevo script de diagnóstico

1. **Crea un archivo** en `scripts/` con nombre descriptivo (ej: `diagnostico-X.js`)
2. **Agrega encabezado:**
   ```javascript
   // 🔍 SCRIPT DE DIAGNÓSTICO - Título
   // Descripción breve de qué hace el script
   
   console.clear();
   console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━', 'color: cyan; font-weight: bold');
   console.log('%c🔍 TÍTULO DEL DIAGNÓSTICO', 'color: yellow; font-size: 16px; font-weight: bold');
   console.log('%c━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n', 'color: cyan; font-weight: bold');
   ```

3. **Implementa la lógica** de diagnóstico
4. **Muestra resultados** con `console.log`, `console.table`, etc.
5. **Proporciona soluciones** si se detectan problemas
6. **Agrega comandos útiles** al final
7. **Documenta** en este README

---

**Última actualización:** 14 de octubre de 2025  
**Mantenedor:** Equipo Recuiva
