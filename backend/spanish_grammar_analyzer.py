"""
ANALIZADOR GRAMATICAL ESPAÑOL - RECUIVA
========================================

Módulo especializado en gramática española para distinguir:
- Nombres propios (personas, lugares) vs objetos comunes
- Sujeto vs predicado vs complementos
- Sustantivos vs verbos vs adjetivos
- Género y número gramatical
- NUEVO: Clasificación UNIVERSAL de entidades (persona, concepto, objeto, proceso)

PROBLEMA RESUELTO:
❌ ANTES: "Estaba y Ahol", "Henriet y Ancuet" (nombres mal formados)
✅ AHORA: Valida contexto gramatical antes de extraer

Autor: Abel Jesús Moya Acosta
Fecha: 10 de noviembre de 2025
Proyecto: Recuiva - Active Recall con IA
"""

import re
from typing import List, Dict, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum

# Importar tipos universales
from universal_entity_types import (
    EntityType,
    UNIVERSAL_INDICATORS,
    CONTEXT_VERBS,
    is_function_word
)


class WordType(Enum):
    """Tipos gramaticales en español"""
    NOMBRE_PROPIO = "nombre_propio"      # María, París, España
    SUSTANTIVO_COMUN = "sustantivo"      # casa, collar, ventana
    VERBO = "verbo"                      # correr, hablar, ser
    ADJETIVO = "adjetivo"                # grande, azul, hermoso
    ARTICULO = "articulo"                # el, la, un, una
    PREPOSICION = "preposicion"          # de, en, con, por
    PRONOMBRE = "pronombre"              # él, ella, usted


@dataclass
class GrammaticalEntity:
    """Entidad gramatical extraída del texto"""
    text: str                    # Texto original
    word_type: WordType          # Tipo gramatical
    confidence: float            # Confianza (0-1)
    context: str                 # Contexto donde aparece
    is_person: bool              # Es nombre de persona
    gender: Optional[str] = None # masculino/femenino/neutro
    number: Optional[str] = None # singular/plural


class SpanishGrammarAnalyzer:
    """
    Analizador especializado en gramática española
    
    REGLAS IMPLEMENTADAS:
    1. Nombres propios: Mayúscula + contexto verbal de persona
    2. Sujeto: Quien realiza la acción (antes del verbo)
    3. Predicado: Verbo + complementos
    4. Validación de género/número
    """
    
    # ===== DICCIONARIOS GRAMATICALES =====
    
    # Artículos definidos e indefinidos
    ARTICULOS = {
        'el', 'la', 'los', 'las',       # Definidos
        'un', 'una', 'unos', 'unas'     # Indefinidos
    }
    
    # Preposiciones comunes
    PREPOSICIONES = {
        'a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'durante',
        'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 'por',
        'según', 'sin', 'sobre', 'tras'
    }
    
    # Pronombres personales
    PRONOMBRES = {
        'yo', 'tú', 'él', 'ella', 'usted', 'nosotros', 'nosotras',
        'vosotros', 'vosotras', 'ellos', 'ellas', 'ustedes',
        'me', 'te', 'se', 'lo', 'la', 'le', 'nos', 'os', 'les'
    }
    
    # Verbos auxiliares y copulativos
    VERBOS_AUXILIARES = {
        'ser', 'estar', 'haber', 'tener', 'poder', 'deber',
        'es', 'está', 'estaba', 'era', 'fue', 'había', 'hubo',
        'tiene', 'tenía', 'tuvo', 'puede', 'podía', 'pudo'
    }
    
    # Verbos de acción comunes (infinitivos y conjugaciones frecuentes)
    VERBOS_ACCION = {
        'hacer', 'hizo', 'hice', 'decir', 'dijo', 'dije',
        'ver', 'vio', 'vi', 'dar', 'dio', 'di',
        'poner', 'puso', 'puse', 'tomar', 'tomó', 'tomé',
        'llevar', 'llevó', 'llevé', 'dejar', 'dejó', 'dejé',
        'llamar', 'llamó', 'llamé', 'encontrar', 'encontró', 'encontré',
        'pensar', 'pensó', 'pensé', 'creer', 'creyó', 'creí',
        'mirar', 'miró', 'miré', 'parecer', 'pareció', 'parecí',
        'quedar', 'quedó', 'quedé', 'seguir', 'siguió', 'seguí',
        'venir', 'vino', 'vine', 'salir', 'salió', 'salí',
        'entrar', 'entró', 'entré', 'preguntar', 'preguntó', 'pregunté',
        'responder', 'respondió', 'respondí', 'abrir', 'abrió', 'abrí',
        'cerrar', 'cerró', 'cerré', 'ofrecer', 'ofreció', 'ofrecí',
        'comprender', 'comprendió', 'comprendí', 'conocer', 'conoció', 'conocí'
    }
    
    # Sustantivos comunes que NO son nombres propios (aunque empiecen con mayúscula en títulos)
    SUSTANTIVOS_COMUNES = {
        'libro', 'casa', 'ventana', 'puerta', 'collar', 'anillo', 'joya',
        'habitación', 'patio', 'gabinete', 'edificio', 'calle', 'camino',
        'noche', 'día', 'mañana', 'tarde', 'año', 'mes', 'semana',
        'hombre', 'mujer', 'niño', 'niña', 'persona', 'gente',
        'señor', 'señora', 'conde', 'condesa', 'rey', 'reina', 'cardenal',
        'esposa', 'marido', 'hijo', 'hija', 'sobrino', 'sobrina', 'tío', 'tía',
        'mano', 'ojo', 'cara', 'voz', 'palabra', 'gesto',
        'diamante', 'oro', 'plata', 'piedra', 'montura',
        'objeto', 'cosa', 'lugar', 'sitio', 'parte'
    }
    
    # Títulos y tratamientos que indican persona
    TITULOS_PERSONA = {
        'señor', 'señora', 'don', 'doña', 'conde', 'condesa',
        'duque', 'duquesa', 'rey', 'reina', 'príncipe', 'princesa',
        'cardenal', 'obispo', 'papa', 'doctor', 'doctora',
        'profesor', 'profesora', 'ingeniero', 'ingeniera'
    }
    
    # Conectores de nombres compuestos
    CONECTORES_NOMBRES = {'de', 'del', 'la', 'y'}
    
    def __init__(self):
        """Inicializa el analizador gramatical"""
        self.stats = {
            'entities_extracted': 0,
            'proper_nouns_found': 0,
            'common_nouns_found': 0
        }
    
    def extract_proper_nouns(
        self,
        text: str,
        min_confidence: float = 0.6
    ) -> List[GrammaticalEntity]:
        """
        Extrae nombres propios con validación gramatical
        
        MEJORAS vs ContentAnalyzer:
        - ✅ Valida contexto gramatical (no solo mayúsculas)
        - ✅ Distingue "Toca" (objeto) de "María" (persona)
        - ✅ Detecta títulos ("señor Dreux", "condesa de X")
        - ✅ Maneja nombres compuestos ("María Antonieta", "Luis de Francia")
        
        Args:
            text: Texto a analizar
            min_confidence: Confianza mínima (0-1)
            
        Returns:
            Lista de entidades gramaticales validadas
        """
        entities = []
        
        # PASO 1: Buscar nombres con títulos (alta confianza)
        # Patrón: "señor/condesa/etc + Nombre(s)"
        title_pattern = r'\b(' + '|'.join(self.TITULOS_PERSONA) + r')\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de|del|la|y)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2})\b'
        
        for match in re.finditer(title_pattern, text, re.IGNORECASE):
            title = match.group(1).lower()
            name = match.group(2)
            
            # Determinar género por título
            gender = self._detect_gender_from_title(title)
            
            entities.append(GrammaticalEntity(
                text=name,
                word_type=WordType.NOMBRE_PROPIO,
                confidence=0.95,  # Alta confianza (tiene título)
                context=match.group(0),
                is_person=True,
                gender=gender,
                number='singular'
            ))
        
        # PASO 2: Buscar nombres propios sin título (validación contextual)
        # Patrón: 1-4 palabras capitalizadas, permitiendo conectores
        name_pattern = r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de|del|la|y)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2})\b'
        
        for match in re.finditer(name_pattern, text):
            name_candidate = match.group(1)
            
            # VALIDACIÓN 1: Omitir si es sustantivo común conocido
            first_word = name_candidate.split()[0].lower()
            if first_word in self.SUSTANTIVOS_COMUNES:
                continue
            
            # VALIDACIÓN 2: Omitir si está en lista negra
            if self._is_blacklisted_term(name_candidate):
                continue
            
            # VALIDACIÓN 3: Analizar contexto gramatical
            start_pos = max(0, match.start() - 50)
            end_pos = min(len(text), match.end() + 50)
            context = text[start_pos:end_pos]
            
            confidence = self._calculate_name_confidence(name_candidate, context)
            
            if confidence >= min_confidence:
                # Verificar si ya fue extraído con título
                if not any(e.text == name_candidate for e in entities):
                    entities.append(GrammaticalEntity(
                        text=name_candidate,
                        word_type=WordType.NOMBRE_PROPIO,
                        confidence=confidence,
                        context=context,
                        is_person=self._is_person_name(name_candidate, context),
                        gender=self._detect_gender_from_context(context),
                        number='singular'
                    ))
        
        # PASO 3: Deduplicar y ordenar por confianza
        seen = set()
        unique_entities = []
        
        for entity in sorted(entities, key=lambda e: e.confidence, reverse=True):
            # Normalizar para comparación
            normalized = entity.text.lower().strip()
            
            if normalized not in seen:
                seen.add(normalized)
                unique_entities.append(entity)
                self.stats['entities_extracted'] += 1
                if entity.is_person:
                    self.stats['proper_nouns_found'] += 1
        
        return unique_entities
    
    def _detect_gender_from_title(self, title: str) -> str:
        """Detecta género gramatical por título"""
        feminine_titles = {'señora', 'doña', 'condesa', 'duquesa', 'reina', 'princesa', 'doctora', 'profesora', 'ingeniera'}
        
        if title.lower() in feminine_titles:
            return 'femenino'
        else:
            return 'masculino'
    
    def _is_blacklisted_term(self, term: str) -> bool:
        """
        Verifica si el término es un falso positivo común
        
        LISTA NEGRA:
        - Inicio de oraciones genéricas ("Dos o tres", "Era en")
        - Objetos comunes ("Toca", "Collar", "Ventana")
        - Conectores mal capitalizados
        """
        blacklist = {
            # Números/cuantificadores
            'Dos', 'Tres', 'Cuatro', 'Cinco', 'Muchos', 'Varios', 'Algunos',
            
            # Objetos del "Collar de la Reina"
            'Toca', 'Collar', 'Ventana', 'Puerta', 'Habitación', 'Patio',
            'Gabinete', 'Edificio', 'Diamante', 'Montura',
            
            # Temporales
            'Era', 'Fue', 'Había', 'Noche', 'Día', 'Mañana', 'Tarde',
            
            # Inicio de oración genérico
            'De', 'En', 'Con', 'Por', 'Para', 'Sobre', 'Entre'
        }
        
        first_word = term.split()[0]
        return first_word in blacklist
    
    def _calculate_name_confidence(self, name: str, context: str) -> float:
        """
        Calcula confianza de que sea nombre propio
        
        FACTORES:
        1. Longitud (nombres muy cortos = baja confianza)
        2. Presencia de verbos de acción cerca (sujeto probable)
        3. Preposiciones "de"/"del" antes (títulos nobiliarios)
        4. Artículos antes (probablemente objeto común)
        """
        confidence = 0.5  # Base
        
        # FACTOR 1: Longitud y estructura
        words = name.split()
        if len(words) >= 2:
            confidence += 0.2  # Nombres compuestos son más probables
        elif len(words) == 1 and len(name) <= 4:
            confidence -= 0.2  # Nombres muy cortos son dudosos
        
        # FACTOR 2: Contexto verbal (es sujeto de una acción)
        context_lower = context.lower()
        for verb in self.VERBOS_ACCION:
            if verb in context_lower:
                # Buscar si el nombre está antes del verbo (patrón sujeto-verbo)
                name_pos = context_lower.find(name.lower())
                verb_pos = context_lower.find(verb)
                
                if name_pos < verb_pos and (verb_pos - name_pos) < 30:
                    confidence += 0.15
                    break
        
        # FACTOR 3: Títulos nobiliarios ("conde de X", "duque de Y")
        if re.search(r'\b(?:de|del)\s+' + re.escape(name), context, re.IGNORECASE):
            # Verificar si hay título antes
            if any(title in context_lower for title in self.TITULOS_PERSONA):
                confidence += 0.25
        
        # FACTOR 4: Artículos antes (indica objeto común)
        for article in self.ARTICULOS:
            if re.search(r'\b' + article + r'\s+' + re.escape(name), context, re.IGNORECASE):
                confidence -= 0.3  # "el Toca", "la Ventana" = no es nombre
                break
        
        # FACTOR 5: Conectores de nombres compuestos
        if any(conn in name.lower() for conn in ['de', 'del', 'la', 'y']):
            confidence += 0.15  # "María de Francia", "Juan y Pedro"
        
        return min(1.0, max(0.0, confidence))
    
    def _is_person_name(self, name: str, context: str) -> bool:
        """
        Determina si el nombre es de una persona (vs lugar/cosa)
        
        HEURÍSTICAS:
        - Verbos de diálogo cerca ("dijo X", "preguntó Y")
        - Pronombres personales ("él", "ella", "usted")
        - Posesivos de persona ("su", "sus" + nombre)
        """
        context_lower = context.lower()
        name_lower = name.lower()
        
        # Verbos de diálogo (fuerte indicador de persona)
        dialogue_verbs = {
            'dijo', 'preguntó', 'respondió', 'exclamó', 'gritó', 'susurró',
            'contestó', 'murmuró', 'replicó', 'añadió', 'continuó'
        }
        
        for verb in dialogue_verbs:
            if re.search(r'\b' + re.escape(name_lower) + r'\s+' + verb, context_lower):
                return True
            if re.search(verb + r'\s+' + re.escape(name_lower), context_lower):
                return True
        
        # Pronombres personales cerca
        if re.search(r'\b(?:él|ella|usted|señor|señora)\b.*' + re.escape(name_lower), context_lower):
            return True
        
        # Verbos de acción con el nombre como sujeto
        for verb in ['entró', 'salió', 'caminó', 'miró', 'pensó', 'sintió']:
            if re.search(r'\b' + re.escape(name_lower) + r'\s+' + verb, context_lower):
                return True
        
        return False
    
    def _detect_gender_from_context(self, context: str) -> Optional[str]:
        """Detecta género por contexto (pronombres, artículos)"""
        context_lower = context.lower()
        
        # Pronombres/artículos masculinos
        if re.search(r'\b(?:él|señor|don|el)\b', context_lower):
            return 'masculino'
        
        # Pronombres/artículos femeninos
        if re.search(r'\b(?:ella|señora|doña|la)\b', context_lower):
            return 'femenino'
        
        return None
    
    def identify_subject_predicate(self, sentence: str) -> Dict[str, str]:
        """
        Identifica sujeto y predicado en una oración
        
        REGLAS:
        - Sujeto: Quien realiza la acción (antes del verbo principal)
        - Predicado: Verbo + complementos
        
        Returns:
            {'subject': str, 'predicate': str, 'verb': str}
        """
        # Buscar verbo principal
        words = sentence.split()
        verb_pos = -1
        main_verb = ""
        
        for i, word in enumerate(words):
            word_lower = word.lower().strip('.,;:!?')
            if word_lower in self.VERBOS_ACCION or word_lower in self.VERBOS_AUXILIARES:
                verb_pos = i
                main_verb = word_lower
                break
        
        if verb_pos == -1:
            return {'subject': '', 'predicate': sentence, 'verb': ''}
        
        # Sujeto: palabras antes del verbo (excluyendo artículos/preposiciones)
        subject_words = []
        for i in range(verb_pos):
            word = words[i].strip('.,;:!?')
            word_lower = word.lower()
            
            # Omitir artículos y preposiciones iniciales
            if word_lower not in self.ARTICULOS and word_lower not in self.PREPOSICIONES:
                subject_words.append(word)
        
        subject = ' '.join(subject_words) if subject_words else '(sujeto tácito)'
        predicate = ' '.join(words[verb_pos:])
        
        return {
            'subject': subject,
            'predicate': predicate,
            'verb': main_verb
        }
    
    def get_stats(self) -> Dict:
        """Retorna estadísticas del analizador"""
        return self.stats


# ===== FUNCIÓN DE INTEGRACIÓN =====

def extract_validated_names(text: str) -> List[str]:
    """
    Wrapper para integración rápida con content_analyzer.py
    
    Args:
        text: Chunk de texto a analizar
        
    Returns:
        Lista de nombres propios validados (solo texto)
    """
    analyzer = SpanishGrammarAnalyzer()
    entities = analyzer.extract_proper_nouns(text, min_confidence=0.6)
    
    # Filtrar solo personas y ordenar por confianza
    person_names = [
        e.text for e in entities
        if e.is_person and e.confidence >= 0.6
    ]
    
    return person_names[:10]  # Top 10


# ===== EJEMPLO DE USO =====

if __name__ == "__main__":
    print("="*80)
    print("🇪🇸 ANALIZADOR GRAMATICAL ESPAÑOL")
    print("="*80)
    
    # Texto de prueba del "Collar de la Reina"
    test_text = """
    Dos o tres veces al año, con motivo de solemnidades importantes,
    como los bailes de la embajada de Austria o las veladas de lady
    Billingstone, la condesa de Dreux-Soubise lucía sobre sus blancos
    hombros «el collar de la reina». Era, en efecto, el famoso collar,
    el legendario collar que Böhmer y Bassenge, joyeros de la corona,
    destinaban a la Du Barry, que el cardenal de Rohan-Soubise creyó
    ofrecer a María Antonieta, reina de Francia.
    """
    
    analyzer = SpanishGrammarAnalyzer()
    entities = analyzer.extract_proper_nouns(test_text)
    
    print("\n✅ NOMBRES PROPIOS EXTRAÍDOS:")
    print(f"{'Nombre':<30} {'Tipo':<15} {'Confianza':<12} {'¿Persona?':<10} {'Género':<12}")
    print("-" * 80)
    
    for entity in entities:
        print(f"{entity.text:<30} {entity.word_type.value:<15} {entity.confidence:<12.0%} {str(entity.is_person):<10} {entity.gender or 'N/A':<12}")
    
    print(f"\n📊 Total extraído: {len(entities)} entidades")
    print(f"   - Personas: {sum(1 for e in entities if e.is_person)}")
    print(f"   - Otros: {sum(1 for e in entities if not e.is_person)}")
    
    # Ejemplo de análisis sujeto-predicado
    print("\n" + "="*80)
    print("🔍 ANÁLISIS SUJETO-PREDICADO")
    print("="*80)
    
    sentence = "La condesa de Dreux-Soubise lucía sobre sus blancos hombros el collar de la reina"
    analysis = analyzer.identify_subject_predicate(sentence)
    
    print(f"\nOración: {sentence}")
    print(f"   Sujeto:    {analysis['subject']}")
    print(f"   Verbo:     {analysis['verb']}")
    print(f"   Predicado: {analysis['predicate']}")
    
    print("\n" + "="*80)


# =============================================================================
# FUNCIÓN PRINCIPAL PARA CLASIFICACIÓN UNIVERSAL DE ENTIDADES
# =============================================================================

def get_entity_type(entity: str, context: str) -> EntityType:
    """
    Clasifica entidad en tipo UNIVERSAL basándose en contexto
    
    Funciona para CUALQUIER dominio (literatura, ciencia, técnico, académico)
    
    Args:
        entity: Nombre de la entidad ("García", "BRCA1", "QuickSort", "relatividad")
        context: Oración o párrafo completo donde aparece la entidad
    
    Returns:
        EntityType: PERSON | CONCEPT | OBJECT | PROCESS | LOCATION | ORGANIZATION | UNKNOWN
    
    Ejemplos:
        >>> get_entity_type("García", "el doctor García estudió medicina")
        EntityType.PERSON
        
        >>> get_entity_type("BRCA1", "la proteína BRCA1 regula el ciclo celular")
        EntityType.OBJECT
        
        >>> get_entity_type("QuickSort", "el algoritmo QuickSort ordena en O(n log n)")
        EntityType.PROCESS
        
        >>> get_entity_type("relatividad", "la teoría de la relatividad explica")
        EntityType.CONCEPT
    """
    context_lower = context.lower()
    entity_lower = entity.lower()
    
    # MÉTODO 1: Buscar INDICADOR en contexto (máxima confianza)
    # Ejemplo: "la proteína BRCA1" → indicador "proteína" → OBJECT
    for entity_type, indicators in UNIVERSAL_INDICATORS.items():
        for indicator in indicators:
            # Patrón: "indicador + entidad" o "entidad + indicador"
            pattern_before = rf'\b{re.escape(indicator)}\s+{re.escape(entity_lower)}'
            pattern_after = rf'\b{re.escape(entity_lower)}\s+{re.escape(indicator)}'
            
            if re.search(pattern_before, context_lower) or re.search(pattern_after, context_lower):
                return entity_type
    
    # MÉTODO 2: Buscar VERBO de contexto (alta confianza)
    # Ejemplo: "BRCA1 regula el ciclo" → verbo "regula" → OBJECT
    for entity_type, verbs in CONTEXT_VERBS.items():
        for verb in verbs:
            # Patrón: "entidad + verbo" (sujeto-verbo)
            pattern_subject = rf'\b{re.escape(entity_lower)}\s+{verb}'
            # Patrón: "verbo + entidad" (menos común pero válido)
            pattern_object = rf'\b{verb}\s+(?:el|la|los|las|un|una)?\s*{re.escape(entity_lower)}'
            
            if re.search(pattern_subject, context_lower) or re.search(pattern_object, context_lower):
                return entity_type
    
    # MÉTODO 3: Heurísticas por estructura y contexto
    entity_words = entity.split()
    
    # Si tiene ≥2 palabras capitalizadas y verbo de persona → PERSON
    if len(entity_words) >= 2 and entity[0].isupper():
        person_verbs = CONTEXT_VERBS.get(EntityType.PERSON, set())
        if any(verb in context_lower for verb in person_verbs):
            return EntityType.PERSON
        
        # Si no tiene verbo de persona pero tiene "de" o "del" → posiblemente LOCATION
        if 'de' in entity_words or 'del' in entity_words:
            return EntityType.LOCATION
    
    # Si contiene números/letras (ej: "BRCA1", "QuickSort") → OBJECT o PROCESS
    if re.search(r'\d', entity) or re.search(r'[A-Z]{2,}', entity):
        # Si tiene verbo técnico cerca → PROCESS
        technical_verbs = {'implementa', 'ejecuta', 'calcula', 'procesa', 'ordena'}
        if any(verb in context_lower for verb in technical_verbs):
            return EntityType.PROCESS
        # Si no → OBJECT
        return EntityType.OBJECT
    
    # Si tiene artículo determinado + sustantivo abstracto → CONCEPT
    if re.search(rf'\b(?:el|la)\s+{re.escape(entity_lower)}\s+(?:de|del|que|es|consiste)', context_lower):
        return EntityType.CONCEPT
    
    # Si todo falla → UNKNOWN
    return EntityType.UNKNOWN


# Función auxiliar para compatibilidad con código existente
def classify_entity(entity: str, context: str) -> str:
    """Wrapper que retorna string en lugar de enum (compatibilidad)"""
    entity_type = get_entity_type(entity, context)
    return entity_type.value

