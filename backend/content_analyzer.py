"""
ANALIZADOR DE CONTENIDO INTELIGENTE - RECUIVA
==============================================

Sistema de análisis lingüístico profundo SIN usar LLMs externos.
Basado en patrones lingüísticos, morfología y sintaxis del español.

Autor: Abel Jesús Moya Acosta
Fecha: 10 de noviembre de 2025
Proyecto: Recuiva - Active Recall con IA

CARACTERÍSTICAS:
- Análisis morfológico (sustantivos, verbos, adjetivos)
- Detección de patrones sintácticos
- Clasificación semántica basada en reglas
- Compatible con UTF-8, emojis, caracteres especiales
- Robusto ante imágenes/tablas en PDFs
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter

# Importar analizador gramatical español
try:
    from spanish_grammar_analyzer import SpanishGrammarAnalyzer, extract_validated_names
    GRAMMAR_ANALYZER_AVAILABLE = True
except ImportError:
    GRAMMAR_ANALYZER_AVAILABLE = False
    print("⚠️ SpanishGrammarAnalyzer no disponible, usando regex básico")

@dataclass
class ChunkAnalysis:
    """Resultado del análisis profundo de un chunk"""
    content_type: str  # narrative, academic, technical, descriptive, procedural
    confidence: float  # 0.0 a 1.0
    key_entities: List[str]  # Nombres propios, conceptos clave
    main_verbs: List[str]  # Verbos principales
    patterns_detected: List[str]  # Patrones encontrados
    linguistic_features: Dict[str, any]  # Características lingüísticas
    justification: str  # Explicación de la decisión


class ContentAnalyzer:
    """
    Motor de análisis lingüístico que procesa chunks de texto
    y detecta su tipo, conceptos clave y estructura
    """
    
    # ========================================
    # PATRONES LINGÜÍSTICOS UNIVERSALES
    # ========================================
    
    DEFINITION_PATTERNS = [
        r'(?:se define|se entiende|consiste en|significa|es el|es la|es un|es una)\s+',
        r'(?:llamado|conocido como|denominado)\s+',
        r'(?:concepto de|noción de|idea de)\s+'
    ]
    
    EXAMPLE_PATTERNS = [
        r'(?:por ejemplo|como|tal como|a saber|verbigracia)',
        r'(?:tales como|entre ellos|incluyendo)',
        r'(?:caso de|ejemplo de)\s+'
    ]
    
    COMPARISON_PATTERNS = [
        r'(?:mientras que|sin embargo|no obstante|por el contrario)',
        r'(?:a diferencia de|en contraste con|comparado con)',
        r'(?:similar a|parecido a|análogo a)\s+'
    ]
    
    CAUSALITY_PATTERNS = [
        r'(?:porque|debido a|dado que|puesto que|ya que)',
        r'(?:por lo tanto|por consiguiente|en consecuencia)',
        r'(?:causa de|razón de|motivo de)\s+'
    ]
    
    PROCEDURAL_PATTERNS = [
        r'(?:primero|segundo|tercero|finalmente|por último)',
        r'(?:paso \d+|etapa \d+|fase \d+)',
        r'(?:se debe|hay que|es necesario)\s+'
    ]
    
    # Verbos narrativos (acciones en historias)
    NARRATIVE_VERBS = [
        'dijo', 'exclamó', 'preguntó', 'respondió', 'gritó', 'susurró',
        'miró', 'vio', 'observó', 'contempló', 'escuchó',
        'caminó', 'corrió', 'saltó', 'entró', 'salió',
        'pensó', 'recordó', 'imaginó', 'sintió', 'temió'
    ]
    
    # Verbos académicos (análisis, investigación)
    ACADEMIC_VERBS = [
        'analiza', 'investiga', 'demuestra', 'comprueba', 'verifica',
        'establece', 'determina', 'identifica', 'clasifica', 'categoriza',
        'explica', 'describe', 'define', 'conceptualiza', 'teoriza'
    ]
    
    # Verbos técnicos (procedimientos, instrucciones)
    TECHNICAL_VERBS = [
        'configura', 'instala', 'ejecuta', 'compila', 'depura',
        'implementa', 'desarrolla', 'diseña', 'construye', 'programa',
        'calcula', 'procesa', 'optimiza', 'evalúa', 'mide'
    ]
    
    # Marcadores de metadata (NO son contenido útil)
    METADATA_MARKERS = [
        r'LIBRO DESCARGADO',
        r'WWW\.[A-Z]+\.(COM|ORG|NET)',
        r'FUENTE:.*PROJECT',
        r'PUBLICADO.*\d{4}',
        r'ISBN.*\d',
        r'COPYRIGHT|©|\(C\)',
        r'DOMINIO P[UÚ]BLICO',
        r'^\*+\s*$',  # Líneas de asteriscos
        r'^[\-\_]{5,}$',  # Líneas decorativas
        r'^\d+\s*$'  # Solo números (paginación)
    ]
    
    def __init__(self):
        """Inicializa el analizador"""
        self.stats = {
            'chunks_analyzed': 0,
            'types_detected': Counter(),
            'patterns_found': Counter()
        }
    
    def analyze(self, chunk: str) -> ChunkAnalysis:
        """
        Analiza un chunk de texto en profundidad
        
        Args:
            chunk: Texto a analizar
            
        Returns:
            ChunkAnalysis: Resultado del análisis completo
        """
        self.stats['chunks_analyzed'] += 1
        
        # Limpiar chunk
        clean_chunk = self._clean_chunk(chunk)
        
        # Detectar si es metadata (no contenido)
        if self._is_metadata(clean_chunk):
            return self._create_metadata_analysis(chunk)
        
        # Análisis morfológico
        entities = self._extract_entities(clean_chunk)
        verbs = self._extract_verbs(clean_chunk)
        
        # Análisis de patrones
        patterns = self._detect_patterns(clean_chunk)
        
        # Características lingüísticas
        features = self._extract_linguistic_features(clean_chunk)
        
        # Clasificación semántica
        content_type, confidence, justification = self._classify_content(
            clean_chunk, entities, verbs, patterns, features
        )
        
        self.stats['types_detected'][content_type] += 1
        for pattern in patterns:
            self.stats['patterns_found'][pattern] += 1
        
        return ChunkAnalysis(
            content_type=content_type,
            confidence=confidence,
            key_entities=entities,
            main_verbs=verbs,
            patterns_detected=patterns,
            linguistic_features=features,
            justification=justification
        )
    
    def _clean_chunk(self, text: str) -> str:
        """Limpia el chunk preservando estructura"""
        # Normalizar espacios pero preservar saltos de línea significativos
        text = re.sub(r' +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def _is_metadata(self, text: str) -> bool:
        """Detecta si el chunk es metadata (no contenido útil)"""
        # Muy corto (< 50 caracteres)
        if len(text) < 50:
            return True
        
        # Coincide con patrones de metadata
        for pattern in self.METADATA_MARKERS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Más del 40% es números/símbolos (probablemente tabla/fórmula sin contexto)
        non_alpha = len(re.findall(r'[^a-záéíóúñA-ZÁÉÍÓÚÑ\s]', text))
        if non_alpha / len(text) > 0.4:
            return True
        
        return False
    
    def _create_metadata_analysis(self, chunk: str) -> ChunkAnalysis:
        """Crea análisis para chunks de metadata"""
        return ChunkAnalysis(
            content_type='metadata',
            confidence=1.0,
            key_entities=[],
            main_verbs=[],
            patterns_detected=['metadata_detected'],
            linguistic_features={'is_metadata': True},
            justification="Chunk identificado como metadata (información de publicación, copyright, etc.) y excluido de generación de preguntas"
        )
    
    def _extract_entities(self, text: str) -> List[str]:
        """
        Extrae entidades clave (nombres propios, conceptos) con validación gramatical
        
        MEJORA vs versión anterior:
        ✅ Usa SpanishGrammarAnalyzer para validar contexto
        ✅ Distingue nombres propios de objetos comunes
        ✅ Evita "Toca", "Collar", "Ventana" como nombres
        ✅ Detecta títulos nobiliarios ("condesa de X")
        """
        entities = []
        
        # MÉTODO 1: Analizador gramatical (PREFERIDO)
        if GRAMMAR_ANALYZER_AVAILABLE:
            try:
                validated_names = extract_validated_names(text)
                entities.extend(validated_names)
            except Exception as e:
                print(f"⚠️ Error en analizador gramatical: {e}, usando fallback")
        
        # MÉTODO 2: Regex mejorado (FALLBACK)
        # Solo si no hay suficientes entidades del analizador
        if len(entities) < 3:
            # Nombres propios con validación básica
            # Patrón: 1-3 palabras capitalizadas, permitiendo "de", "del", "y"
            proper_names = re.findall(
                r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+(?:de|del|la|y)\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2})\b',
                text
            )
            
            # Filtrar objetos comunes que empiezan con mayúscula
            blacklist = {
                'Toca', 'Collar', 'Ventana', 'Puerta', 'Habitación', 'Patio',
                'Gabinete', 'Edificio', 'Diamante', 'Montura', 'Noche', 'Día',
                'Dos', 'Tres', 'Cuatro', 'Varios', 'Muchos', 'Era', 'Fue'
            }
            
            for name in proper_names:
                first_word = name.split()[0]
                if first_word not in blacklist and name not in entities:
                    entities.append(name)
        
        # MÉTODO 3: Conceptos técnicos (palabras capitalizadas sueltas)
        technical_terms = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{3,}\b', text)
        for term in technical_terms:
            if term not in entities and len(entities) < 10:
                # Validar que no sea inicio de oración común
                if not re.search(r'^' + re.escape(term) + r'\s+(?:es|fue|era|está)', text):
                    entities.append(term)
        
        # MÉTODO 4: Términos entre comillas (conceptos definidos)
        quoted_terms = re.findall(r'"([^"]{3,30})"', text)
        entities.extend(quoted_terms)
        
        # Deduplicar y filtrar
        entities = list(dict.fromkeys([e.strip() for e in entities if len(e.strip()) > 3]))
        return entities[:10]  # Top 10
    
    def _extract_verbs(self, text: str) -> List[str]:
        """Extrae verbos principales del chunk"""
        text_lower = text.lower()
        verbs_found = []
        
        # Buscar verbos narrativos
        for verb in self.NARRATIVE_VERBS:
            if verb in text_lower:
                verbs_found.append(('narrative', verb))
        
        # Buscar verbos académicos
        for verb in self.ACADEMIC_VERBS:
            if verb in text_lower:
                verbs_found.append(('academic', verb))
        
        # Buscar verbos técnicos
        for verb in self.TECHNICAL_VERBS:
            if verb in text_lower:
                verbs_found.append(('technical', verb))
        
        return verbs_found[:8]  # Top 8
    
    def _detect_patterns(self, text: str) -> List[str]:
        """Detecta patrones sintácticos en el texto"""
        patterns = []
        
        if any(re.search(p, text, re.IGNORECASE) for p in self.DEFINITION_PATTERNS):
            patterns.append('definition')
        
        if any(re.search(p, text, re.IGNORECASE) for p in self.EXAMPLE_PATTERNS):
            patterns.append('example')
        
        if any(re.search(p, text, re.IGNORECASE) for p in self.COMPARISON_PATTERNS):
            patterns.append('comparison')
        
        if any(re.search(p, text, re.IGNORECASE) for p in self.CAUSALITY_PATTERNS):
            patterns.append('causality')
        
        if any(re.search(p, text, re.IGNORECASE) for p in self.PROCEDURAL_PATTERNS):
            patterns.append('procedural')
        
        # Detectar diálogos
        if '"' in text or '«' in text or '—' in text:
            patterns.append('dialogue')
        
        # Detectar listas/enumeraciones
        if re.search(r'(?:\n|^)\s*[\-\*\•]\s+', text):
            patterns.append('list')
        
        # Detectar números/datos
        if re.search(r'\b\d{4}\b|\d+%|\d+\s*(?:metros|años|personas|km)', text):
            patterns.append('numerical_data')
        
        # Detectar fórmulas matemáticas
        if re.search(r'[=].*[\d+\-*/]|∫|∑|√|∏|∆', text):
            patterns.append('mathematical_formula')
        
        return patterns
    
    def _extract_linguistic_features(self, text: str) -> Dict[str, any]:
        """Extrae características lingüísticas del chunk"""
        words = text.split()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'has_questions': '¿' in text or '?' in text,
            'has_exclamations': '¡' in text or '!' in text,
            'capital_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
            'punctuation_density': len(re.findall(r'[.,;:!?]', text)) / len(words) if words else 0
        }
    
    def _classify_content(
        self,
        text: str,
        entities: List[str],
        verbs: List[Tuple[str, str]],
        patterns: List[str],
        features: Dict
    ) -> Tuple[str, float, str]:
        """
        Clasifica el tipo de contenido y genera justificación
        
        Returns:
            (tipo, confianza, justificación)
        """
        scores = {
            'narrative': 0.0,
            'academic': 0.0,
            'technical': 0.0,
            'descriptive': 0.0,
            'procedural': 0.0
        }
        
        reasons = []
        
        # ANÁLISIS 1: Verbos
        narrative_verbs = sum(1 for t, _ in verbs if t == 'narrative')
        academic_verbs = sum(1 for t, _ in verbs if t == 'academic')
        technical_verbs = sum(1 for t, _ in verbs if t == 'technical')
        
        if narrative_verbs >= 2:
            scores['narrative'] += 0.3
            reasons.append(f"Contiene {narrative_verbs} verbos narrativos ({', '.join([v for t,v in verbs if t=='narrative'][:3])})")
        
        if academic_verbs >= 2:
            scores['academic'] += 0.3
            reasons.append(f"Contiene {academic_verbs} verbos académicos")
        
        if technical_verbs >= 2:
            scores['technical'] += 0.3
            reasons.append(f"Contiene {technical_verbs} verbos técnicos")
        
        # ANÁLISIS 2: Patrones
        if 'dialogue' in patterns:
            scores['narrative'] += 0.25
            reasons.append("Detectado diálogo directo (comillas)")
        
        if 'definition' in patterns:
            scores['academic'] += 0.2
            reasons.append("Detectado patrón de definición")
        
        if 'procedural' in patterns or 'list' in patterns:
            scores['procedural'] += 0.3
            reasons.append("Detectado patrón procedimental o lista")
        
        if 'mathematical_formula' in patterns:
            scores['technical'] += 0.25
            reasons.append("Detectada fórmula matemática")
        
        if 'numerical_data' in patterns:
            scores['technical'] += 0.15
            reasons.append("Contiene datos numéricos")
        
        # ANÁLISIS 3: Entidades
        if len(entities) >= 3:
            # Muchas entidades → probablemente narrativa o descriptiva
            if narrative_verbs > 0:
                scores['narrative'] += 0.2
            else:
                scores['descriptive'] += 0.2
            reasons.append(f"Detectadas {len(entities)} entidades clave")
        
        # ANÁLISIS 4: Características lingüísticas
        if features['has_questions']:
            scores['academic'] += 0.1
        
        if features['avg_sentence_length'] > 20:
            scores['academic'] += 0.15
            reasons.append("Oraciones largas (estilo académico)")
        
        # Determinar tipo ganador
        winner_type = max(scores, key=scores.get)
        confidence = scores[winner_type]
        
        # Si no hay puntuación clara, es descriptivo
        if confidence < 0.3:
            winner_type = 'descriptive'
            confidence = 0.5
            reasons.append("Contenido descriptivo general (sin patrones claros)")
        
        # Normalizar confianza a [0, 1]
        confidence = min(1.0, confidence)
        
        # Generar justificación
        justification = f"Clasificado como '{winner_type}' con confianza {confidence:.0%}. Razones: " + "; ".join(reasons)
        
        return winner_type, confidence, justification
    
    def get_stats(self) -> Dict:
        """Retorna estadísticas del analizador"""
        return {
            'chunks_analyzed': self.stats['chunks_analyzed'],
            'types_distribution': dict(self.stats['types_detected']),
            'patterns_frequency': dict(self.stats['patterns_found'].most_common(10))
        }
