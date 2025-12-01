import numpy as np
import re
from typing import List, Dict, Tuple
from rank_bm25 import BM25Okapi

class HybridValidator:
    def __init__(self, embedding_model):
        self.model = embedding_model
        # Umbrales para clasificación de respuestas (basados en Short Answer Grading - SAG)
        # Estos umbrales se aplican sobre S_raw (score bruto en [0,1])
        self.thresholds = {
            'excelente': 0.85,   # ≥0.85 → Excelente (90-100%)
            'bueno': 0.70,       # 0.70-0.84 → Bueno (70-89%)
            'aceptable': 0.50,   # 0.50-0.69 → Aceptable (50-69%)
            'rechazo': 0.50      # <0.50 → Necesita mejorar (0-49%)
        }
        # Pesos optimizados para OCR + parafraseo (basado en literatura SAG)
        # Priorizan semántica sobre léxico por errores OCR en PDFs
        self.weights = {
            'bm25': 0.05,        # 5% - Coincidencias léxicas (reducido por OCR)
            'cosine': 0.80,      # 80% - Similitud semántica (eje principal)
            'coverage': 0.15     # 15% - Cobertura de keywords clave
        }
        # Rango de normalización para cosine similarity (valores empíricos)
        # AJUSTADO: Para PDFs con texto corrupto/OCR, los cosines son más bajos
        # Basado en all-MiniLM-L6-v2 + análisis de respuestas reales
        self.cosine_min = 0.25   # Por debajo: casi siempre incorrecto (antes: 0.30)
        self.cosine_max = 0.70   # Por encima: muy similar al texto (antes: 0.80)
        
        # Min-max scaling para porcentaje 0-100%
        # AJUSTADO: Más tolerante para texto con errores de espaciado
        self.expected_min = 0.25  # Respuesta muy mala → 0% (antes: 0.30)
        self.expected_max = 0.85  # Respuesta excelente → 100% (antes: 0.90)
        
        self.stopwords = {'el', 'la', 'los', 'las', 'un', 'una', 'de', 'del', 'a', 'al', 'en', 'por', 'para', 'con', 'y', 'o', 'pero', 'si', 'no', 'que', 'como', 'cuando', 'donde', 'cual', 'quien', 'su', 'sus', 'mi', 'mis', 'tu', 'tus', 'se', 'le', 'lo', 'me', 'te', 'nos', 'os'}
        
        # ═══════════════════════════════════════════════════════════════
        # VERBOS DE RAZONAMIENTO (para compute_reasoning_score)
        # Verbos que indican pensamiento, opinión, deducción, etc.
        # ═══════════════════════════════════════════════════════════════
        self.reasoning_verbs = [
            # Verbos de pensamiento
            'pensó', 'pensaba', 'piensa', 'pensar', 'pensando',
            'creyó', 'creía', 'cree', 'creer', 'creyendo',
            'supuso', 'suponía', 'supone', 'suponer', 'suponiendo',
            'imaginó', 'imaginaba', 'imagina', 'imaginar', 'imaginando',
            
            # Verbos de deducción/conclusión
            'dedujo', 'deducía', 'deduce', 'deducir', 'deduciendo',
            'concluyó', 'concluía', 'concluye', 'concluir', 'concluyendo',
            'infirió', 'infería', 'infiere', 'inferir', 'infiriendo',
            'razonó', 'razonaba', 'razona', 'razonar', 'razonando',
            
            # Verbos de sospecha/duda
            'sospechó', 'sospechaba', 'sospecha', 'sospechar', 'sospechando',
            'dudó', 'dudaba', 'duda', 'dudar', 'dudando',
            'desconfió', 'desconfiaba', 'desconfía', 'desconfiar',
            
            # Verbos de decisión/juicio
            'decidió', 'decidía', 'decide', 'decidir', 'decidiendo',
            'juzgó', 'juzgaba', 'juzga', 'juzgar', 'juzgando',
            'opinó', 'opinaba', 'opina', 'opinar', 'opinando',
            'consideró', 'consideraba', 'considera', 'considerar',
            
            # Verbos de comprensión
            'comprendió', 'comprendía', 'comprende', 'comprender',
            'entendió', 'entendía', 'entiende', 'entender',
            'advirtió', 'advertía', 'advierte', 'advertir',
            'notó', 'notaba', 'nota', 'notar',
            'percibió', 'percibía', 'percibe', 'percibir',
            
            # Verbos de intención
            'pretendió', 'pretendía', 'pretende', 'pretender',
            'intentó', 'intentaba', 'intenta', 'intentar',
            'quiso', 'quería', 'quiere', 'querer',
            'buscó', 'buscaba', 'busca', 'buscar',
            
            # Verbos de reflexión
            'reflexionó', 'reflexionaba', 'reflexiona', 'reflexionar',
            'meditó', 'meditaba', 'medita', 'meditar',
            'analizó', 'analizaba', 'analiza', 'analizar',
        ]
        
        # Caracteres que indican diálogo
        self.dialogue_chars = ['"', '«', '»', '—', '-', '"', '"', ''', ''']
    
    def classify_question_type(self, question: str) -> str:
        """
        Clasifica el tipo de pregunta: 'reasoning', 'literal', u 'other'.
        
        ═══════════════════════════════════════════════════════════════
        BASADO EN: Taxonomía de Bloom + Reading Comprehension Research
        ═══════════════════════════════════════════════════════════════
        
        RAZONAMIENTO/INFERENCIAL:
        - Preguntas que requieren deducir, inferir, explicar motivos
        - "¿Por qué...?", "¿Qué proceso de pensamiento...?", "¿Qué intención...?"
        
        LITERAL/HECHO:
        - Preguntas sobre información explícita en el texto
        - "¿Qué hizo...?", "¿Dónde estaba...?", "¿Cuándo...?"
        
        Args:
            question: Texto de la pregunta
            
        Returns:
            str: 'reasoning', 'literal', u 'other'
        """
        question_lower = question.lower()
        
        # Patrones para preguntas de RAZONAMIENTO
        reasoning_patterns = [
            # Causales
            'por qué', 'por que', 'cuál es la razón', 'cual es la razon',
            'qué razones', 'que razones', 'qué motivo', 'que motivo',
            'a qué se debe', 'a que se debe', 'cómo se explica', 'como se explica',
            
            # Procesos mentales
            'qué proceso de pensamiento', 'que proceso de pensamiento',
            'qué pensó', 'que penso', 'qué opinión', 'que opinion',
            'qué postura', 'que postura', 'cómo interpreta', 'como interpreta',
            'qué intención', 'que intencion', 'con qué propósito', 'con que proposito',
            
            # Inferencia
            'qué sugiere', 'que sugiere', 'qué indica', 'que indica',
            'qué permite deducir', 'que permite deducir', 'qué implica', 'que implica',
            'qué se puede inferir', 'que se puede inferir',
            'qué conclusión', 'que conclusion',
            
            # Significado
            'qué representa', 'que representa', 'qué simboliza', 'que simboliza',
            'qué significa', 'que significa', 'cuál es el significado',
            'qué importancia tiene', 'que importancia tiene',
        ]
        
        # Patrones para preguntas LITERALES
        literal_patterns = [
            # Hechos directos
            'qué hizo', 'que hizo', 'qué dijo', 'que dijo',
            'dónde estaba', 'donde estaba', 'dónde se encontraba', 'donde se encontraba',
            'cuándo ocurrió', 'cuando ocurrio', 'cuándo sucedió', 'cuando sucedio',
            'quién era', 'quien era', 'quiénes eran', 'quienes eran',
            
            # Relaciones/Datos
            'qué relación tenía', 'que relacion tenia', 'qué recibía', 'que recibia',
            'qué papel cumple', 'que papel cumple', 'cuántos', 'cuantos',
            'qué tipo de', 'que tipo de', 'cuál era', 'cual era',
            
            # Descripciones
            'cómo era', 'como era', 'cómo se llamaba', 'como se llamaba',
            'qué contenía', 'que contenia', 'qué incluía', 'que incluia',
        ]
        
        # Verificar patrones de razonamiento primero
        for pattern in reasoning_patterns:
            if pattern in question_lower:
                return 'reasoning'
        
        # Verificar patrones literales
        for pattern in literal_patterns:
            if pattern in question_lower:
                return 'literal'
        
        # Por defecto
        return 'other'
    
    def compute_reasoning_score(self, chunk_text: str) -> float:
        """
        Calcula un score de "razonamiento" para un chunk [0, 1].
        
        ═══════════════════════════════════════════════════════════════
        PROPÓSITO:
        Para preguntas de razonamiento/inferenciales, priorizar chunks
        que contengan más diálogo y verbos de pensamiento/opinión.
        ═══════════════════════════════════════════════════════════════
        
        COMPONENTES:
        1. dialogue_ratio: Proporción de caracteres de diálogo
        2. reasoning_verbs_ratio: Densidad de verbos de razonamiento
        
        FÓRMULA:
        score = 0.6 * dialogue_ratio + 0.4 * reasoning_verbs_normalized
        
        Args:
            chunk_text: Texto del chunk
            
        Returns:
            float: Score en [0, 1]
        """
        if not chunk_text or len(chunk_text) < 10:
            return 0.0
        
        chunk_lower = chunk_text.lower()
        
        # ═══════════════════════════════════════════════════════════════
        # 1. RATIO DE DIÁLOGO
        # Proporción de caracteres que son marcadores de diálogo
        # ═══════════════════════════════════════════════════════════════
        dialogue_count = sum(chunk_text.count(char) for char in self.dialogue_chars)
        dialogue_ratio = min(1.0, dialogue_count / (len(chunk_text) * 0.05))  # Normalizar
        
        # ═══════════════════════════════════════════════════════════════
        # 2. RATIO DE VERBOS DE RAZONAMIENTO
        # Contar apariciones de verbos de pensamiento/opinión
        # ═══════════════════════════════════════════════════════════════
        words = chunk_lower.split()
        word_count = max(len(words), 1)
        
        reasoning_count = 0
        for verb in self.reasoning_verbs:
            reasoning_count += chunk_lower.count(verb)
        
        # Normalizar: esperamos ~1-3 verbos de razonamiento por cada 100 palabras
        reasoning_ratio = min(1.0, (reasoning_count / word_count) * 50)
        
        # ═══════════════════════════════════════════════════════════════
        # COMBINAR: 60% diálogo + 40% verbos de razonamiento
        # ═══════════════════════════════════════════════════════════════
        score = 0.6 * dialogue_ratio + 0.4 * reasoning_ratio
        
        return max(0.0, min(1.0, score))
    
    def normalize_cosine(self, cosine_sim: float) -> float:
        """
        Normaliza similitud del coseno al rango 0-1 usando límites empíricos
        
        Basado en investigación de Sentence-BERT:
        - cosine < 0.30: sin relación (0%)
        - cosine = 0.80: muy similar (100%)
        
        Referencia: Reimers & Gurevych (2019), "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"
        """
        normalized = (cosine_sim - self.cosine_min) / (self.cosine_max - self.cosine_min)
        return max(0.0, min(1.0, normalized))  # Clamp a [0, 1]
    
    def length_bonus(self, answer: str) -> float:
        """
        Bonus pequeño por respuestas de longitud razonable
        Evita respuestas telegrama o testamentos
        
        Args:
            answer: Texto de la respuesta del alumno
            
        Returns:
            float: Bonus en [0, 0.05] (máximo 5 puntos extra)
        """
        tokens = len(answer.split())
        if 8 <= tokens <= 80:  # Rango razonable para Active Recall
            return 0.05
        return 0.0
    
    def to_percentage(self, score_raw: float) -> float:
        """
        Convierte score bruto [0,1] a porcentaje 0-100% con min-max scaling
        
        Mapea el rango esperado de scores reales [0.30-0.90] a [0-100%]
        para distribuir mejor los resultados en toda la escala.
        
        Args:
            score_raw: Score bruto en [0,1]
            
        Returns:
            float: Porcentaje en [0.0, 100.0]
        """
        scaled = (score_raw - self.expected_min) / (self.expected_max - self.expected_min)
        scaled = max(0.0, min(1.0, scaled))  # Clamp a [0,1]
        return round(scaled * 100, 1)
    
    def is_inferential_question(self, question: str) -> bool:
        """
        Detecta si una pregunta es inferencial por palabras clave.
        
        BASADO EN: Taxonomía de Bloom + Investigación en Reading Comprehension
        
        NIVELES DE COMPRENSIÓN (Barrett, 1968; Bloom, 1956):
        
        1. LITERAL: Recordar información explícita del texto
           - "¿Quién...?", "¿Cuándo...?", "¿Dónde...?", "¿Qué dijo...?"
           
        2. INFERENCIAL: Deducir información implícita
           - "¿Por qué...?", "¿Qué sugiere...?", "¿Cómo se explica...?"
           
        3. CRÍTICO/EVALUATIVO: Juzgar y valorar
           - "¿Qué opinas...?", "¿Estás de acuerdo...?"
        
        Las preguntas inferenciales requieren que el lector:
        - Conecte información de diferentes partes del texto
        - Use conocimiento previo + información del texto
        - Haga deducciones lógicas
        
        Referencia: Education Endowment Foundation (2025), 
        "Reading Comprehension Strategies" - Making inferences
        
        Args:
            question: Texto de la pregunta
            
        Returns:
            bool: True si es inferencial, False si es literal
        """
        # Keywords para preguntas INFERENCIALES (requieren razonamiento)
        inferential_keywords = [
            # Causales - "¿Por qué?"
            'por qué', 'por que', 'cuál es la razón', 'cual es la razon',
            'qué razones', 'que razones', 'qué motivo', 'que motivo',
            'a qué se debe', 'a que se debe', 'cómo se explica', 'como se explica',
            
            # Inferenciales - Deducción
            'qué sugiere', 'que sugiere', 'qué indica', 'que indica',
            'qué permite deducir', 'que permite deducir', 'qué implica', 'que implica',
            'qué evidencia', 'que evidencia', 'qué indicio', 'que indicio',
            'cómo deduce', 'como deduce', 'cómo sabes', 'como sabes',
            'qué puedes inferir', 'que puedes inferir',
            'qué conclusión', 'que conclusion',
            
            # Predictivas
            'qué pasaría si', 'que pasaria si', 'qué crees que', 'que crees que',
            'qué hubiera pasado', 'que hubiera pasado',
            
            # Comparativas/Analíticas
            'en qué se diferencia', 'en que se diferencia',
            'qué relación', 'que relacion', 'cómo se relaciona', 'como se relaciona',
            'qué tienen en común', 'que tienen en comun',
            
            # Intenciones/Propósito
            'con qué intención', 'con que intencion',
            'para qué', 'para que', 'cuál es el propósito', 'cual es el proposito',
            'qué pretende', 'que pretende',
            
            # Significado/Simbolismo (NUEVO)
            'qué representa', 'que representa', 'qué simboliza', 'que simboliza',
            'qué significa', 'que significa', 'cuál es el significado', 'cual es el significado',
            'qué importancia', 'que importancia', 'cuál es la importancia', 'cual es la importancia',
            'qué papel', 'que papel', 'qué rol', 'que rol',
            'qué sentido', 'que sentido'
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in inferential_keywords)
    
    def detect_contradiction(self, user_answer: str, chunk_text: str, question: str = "") -> Tuple[bool, float, str]:
        """
        Detecta si la respuesta del usuario CONTRADICE el contenido del chunk.
        
        ═══════════════════════════════════════════════════════════════
        PROBLEMA IDENTIFICADO (Testing con GPT):
        ═══════════════════════════════════════════════════════════════
        
        Ejemplo de fallo sin esta función:
        - Chunk dice: "Henriette recibía dinero cada año por correo"
        - Usuario responde: "La condesa nunca le mandó dinero"
        - Sin NLI: score alto (78%) porque comparte palabras como "dinero", "correo"
        - Con NLI: debería ser RECHAZO (<50%)
        
        ═══════════════════════════════════════════════════════════════
        ESTRATEGIA DE DETECCIÓN:
        ═══════════════════════════════════════════════════════════════
        
        1. Identificar KEYWORDS CLAVE del chunk (sustantivos importantes)
        2. Buscar patrones de NEGACIÓN en la respuesta del usuario
        3. Si encuentra negación de keyword clave → CONTRADICCIÓN
        
        Patrones de negación:
        - "no [keyword]", "nunca [keyword]", "sin [keyword]"
        - "jamás", "ningún/ninguna", "nada de"
        
        Args:
            user_answer: Respuesta del usuario
            chunk_text: Texto del chunk de referencia
            question: Pregunta original (para contexto)
            
        Returns:
            Tuple[bool, float, str]: (is_contradiction, penalty_factor, reason)
        """
        answer_lower = user_answer.lower()
        chunk_lower = chunk_text.lower()
        
        # ═══════════════════════════════════════════════════════════════
        # KEYWORDS CRÍTICOS EXPANDIDOS (GENERALIZADO PARA CUALQUIER PDF)
        # ═══════════════════════════════════════════════════════════════
        # Agrupados por categoría semántica - funciona para múltiples dominios
        critical_keywords = {
            # ─────────────────────────────────────────────────────────────
            # ECONOMÍA / DINERO (expandido)
            # ─────────────────────────────────────────────────────────────
            'dinero': ['dinero', 'francos', 'billetes', 'moneda', 'plata', 'efectivo', 
                       'suma', 'pago', 'precio', 'costo', 'valor', 'fortuna', 'riqueza',
                       'pobre', 'rico', 'deuda', 'préstamo', 'herencia', 'tesoro'],
            
            # ─────────────────────────────────────────────────────────────
            # ENVÍO / COMUNICACIÓN
            # ─────────────────────────────────────────────────────────────
            'envio': ['envió', 'enviaba', 'enviar', 'mandó', 'mandaba', 'mandar', 
                      'recibía', 'recibió', 'recibir', 'entregó', 'entregaba', 'entregar',
                      'llegó', 'llegaba', 'llegar', 'trajo', 'traía', 'traer'],
            'correo': ['correo', 'carta', 'cartas', 'sobre', 'sobres', 'correspondencia',
                       'mensaje', 'mensajes', 'telegrama', 'paquete', 'envío'],
            
            # ─────────────────────────────────────────────────────────────
            # AYUDA / ASISTENCIA
            # ─────────────────────────────────────────────────────────────
            'ayuda': ['ayuda', 'ayudó', 'ayudaba', 'ayudar', 'asistencia', 'apoyo',
                      'auxilio', 'socorro', 'colaboración', 'contribución', 'donación'],
            
            # ─────────────────────────────────────────────────────────────
            # CRIMEN / JUSTICIA
            # ─────────────────────────────────────────────────────────────
            'robo': ['robó', 'robar', 'robo', 'hurto', 'ladrón', 'robado', 'robaron',
                     'sustrajo', 'sustraer', 'apropió', 'apropiar', 'estafó', 'estafa'],
            'culpa': ['culpable', 'inocente', 'sospechoso', 'acusado', 'condenado',
                      'absuelto', 'criminal', 'delincuente', 'cómplice', 'víctima'],
            
            # ─────────────────────────────────────────────────────────────
            # EXISTENCIA / OCURRENCIA (NUEVO - GENERAL)
            # ─────────────────────────────────────────────────────────────
            'existencia': ['existió', 'existía', 'existe', 'existir', 'hubo', 'había',
                           'ocurrió', 'ocurría', 'ocurrir', 'sucedió', 'sucedía', 'suceder',
                           'pasó', 'pasaba', 'pasar', 'aconteció', 'tuvo', 'tenía', 'tiene'],
            
            # ─────────────────────────────────────────────────────────────
            # VERDAD / CERTEZA (NUEVO - GENERAL)
            # ─────────────────────────────────────────────────────────────
            'verdad': ['verdad', 'cierto', 'real', 'realidad', 'verdadero', 'auténtico',
                       'legítimo', 'genuino', 'válido', 'confirmado', 'probado', 'demostrado'],
            
            # ─────────────────────────────────────────────────────────────
            # SALUD / ESTADO FÍSICO (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'salud': ['enfermo', 'enferma', 'enfermedad', 'salud', 'sano', 'sana',
                      'curó', 'curaba', 'curar', 'murió', 'moría', 'morir', 'muerte',
                      'herido', 'herida', 'lesión', 'recuperó', 'recuperar', 'sobrevivió'],
            
            # ─────────────────────────────────────────────────────────────
            # EMOCIONES / SENTIMIENTOS (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'emocion': ['feliz', 'triste', 'alegre', 'miedo', 'asustado', 'contento',
                        'enojado', 'furioso', 'preocupado', 'ansioso', 'nervioso', 'tranquilo',
                        'enamorado', 'amaba', 'odiaba', 'quería', 'deseaba', 'temía', 'esperaba'],
            
            # ─────────────────────────────────────────────────────────────
            # EVENTOS / SUCESOS (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'evento': ['guerra', 'batalla', 'conflicto', 'revolución', 'terremoto', 'accidente',
                       'incendio', 'inundación', 'catástrofe', 'desastre', 'celebración', 'fiesta',
                       'boda', 'funeral', 'nacimiento', 'reunión', 'encuentro', 'viaje'],
            
            # ─────────────────────────────────────────────────────────────
            # TIEMPO / TEMPORALIDAD (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'tiempo': ['antes', 'después', 'durante', 'siempre', 'frecuentemente',
                       'diariamente', 'anualmente', 'mensualmente', 'primero', 'último',
                       'antiguo', 'moderno', 'reciente', 'pasado', 'futuro', 'presente'],
            
            # ─────────────────────────────────────────────────────────────
            # UBICACIÓN / LUGAR (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'ubicacion': ['aquí', 'allí', 'cerca', 'lejos', 'dentro', 'fuera', 'arriba', 'abajo',
                          'norte', 'sur', 'este', 'oeste', 'ciudad', 'pueblo', 'país', 'región',
                          'casa', 'edificio', 'palacio', 'habitación', 'lugar', 'sitio'],
            
            # ─────────────────────────────────────────────────────────────
            # PERSONAS / RELACIONES (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'persona': ['padre', 'madre', 'hijo', 'hija', 'hermano', 'hermana', 'esposo', 'esposa',
                        'amigo', 'enemigo', 'rey', 'reina', 'conde', 'condesa', 'señor', 'señora',
                        'jefe', 'empleado', 'sirviente', 'criado', 'niño', 'adulto', 'anciano'],
            
            # ─────────────────────────────────────────────────────────────
            # ACCIONES / VERBOS COMUNES (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'accion': ['hizo', 'hacía', 'hacer', 'dijo', 'decía', 'decir', 'vio', 'veía', 'ver',
                       'oyó', 'oía', 'oír', 'sabía', 'saber', 'conocía', 'conocer', 'pensaba', 'pensar',
                       'quiso', 'quería', 'querer', 'pudo', 'podía', 'poder', 'debía', 'deber',
                       'logró', 'lograr', 'consiguió', 'conseguir', 'intentó', 'intentar',
                       'decidió', 'decidir', 'descubrió', 'descubrir', 'encontró', 'encontrar'],
            
            # ─────────────────────────────────────────────────────────────
            # CANTIDAD / NÚMEROS (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'cantidad': ['todo', 'nada', 'mucho', 'poco', 'algunos', 'ninguno', 'varios',
                         'único', 'solo', 'solamente', 'doble', 'triple', 'mitad', 'completo',
                         'mayoría', 'minoría', 'total', 'parcial', 'entero'],
            
            # ─────────────────────────────────────────────────────────────
            # CIENCIA / ACADÉMICO (NUEVO)
            # ─────────────────────────────────────────────────────────────
            'ciencia': ['experimento', 'teoría', 'hipótesis', 'resultado', 'conclusión',
                        'descubrimiento', 'invento', 'investigación', 'estudio', 'análisis',
                        'prueba', 'evidencia', 'demostración', 'fórmula', 'ley', 'principio'],
        }
        
        # ═══════════════════════════════════════════════════════════════
        # PATRONES DE NEGACIÓN EXPANDIDOS
        # ═══════════════════════════════════════════════════════════════
        negation_patterns = [
            # Patrones directos (negación + keyword)
            r'\bno\s+{keyword}\b',
            r'\bnunca\s+{keyword}\b',
            r'\bjamás\s+{keyword}\b',
            r'\bsin\s+{keyword}\b',
            r'\bningún\s+{keyword}\b',
            r'\bninguna\s+{keyword}\b',
            r'\bnada\s+de\s+{keyword}\b',
            r'\bnadie\s+{keyword}\b',
            # Patrones con 1 palabra intermedia
            r'\bno\s+\w+\s+{keyword}\b',
            r'\bnunca\s+\w+\s+{keyword}\b',
            r'\bno\s+le\s+\w+\s+{keyword}\b',
            r'\bnunca\s+le\s+\w+\s+{keyword}\b',
            r'\bno\s+se\s+\w+\s+{keyword}\b',
            r'\bnunca\s+se\s+\w+\s+{keyword}\b',
            # Patrones con 2 palabras intermedias
            r'\bno\s+\w+\s+\w+\s+{keyword}\b',
            r'\bnunca\s+\w+\s+\w+\s+{keyword}\b',
            r'\bjamás\s+\w+\s+\w+\s+{keyword}\b',
            # Patrones con 3 palabras intermedias
            r'\bno\s+\w+\s+\w+\s+\w+\s+{keyword}\b',
            r'\bnunca\s+\w+\s+\w+\s+\w+\s+{keyword}\b',
            # Patrones compuestos con "pero"
            r'\bpero\s+no\s+{keyword}\b',
            r'\bpero\s+nunca\s+{keyword}\b',
            r'\bpero\s+no\s+\w+\s+{keyword}\b',
            r'\bpero\s+nunca\s+\w+\s+{keyword}\b',
            r'\bpero\s+nunca\s+\w+\s+\w+\s+{keyword}\b',
            # Patrones con "tampoco" (NUEVO)
            r'\btampoco\s+{keyword}\b',
            r'\btampoco\s+\w+\s+{keyword}\b',
            # Patrones con "ni" (NUEVO)
            r'\bni\s+{keyword}\b',
            r'\bni\s+\w+\s+{keyword}\b',
            r'\bni\s+siquiera\s+{keyword}\b',
        ]
        
        contradictions_found = []
        
        # ═══════════════════════════════════════════════════════════════
        # ESTRATEGIA 1: Contradicción con el CHUNK
        # ═══════════════════════════════════════════════════════════════
        for category, keywords in critical_keywords.items():
            for keyword in keywords:
                # Verificar si el keyword está en el chunk (es relevante)
                if keyword in chunk_lower:
                    # Buscar si el usuario NIEGA este keyword
                    for pattern_template in negation_patterns:
                        pattern = pattern_template.format(keyword=keyword)
                        if re.search(pattern, answer_lower):
                            contradictions_found.append({
                                'category': category,
                                'keyword': keyword,
                                'pattern': pattern,
                                'source': 'chunk'
                            })
        
        # ═══════════════════════════════════════════════════════════════
        # ESTRATEGIA 2: Contradicción con la PREGUNTA (EXPANDIDA)
        # ═══════════════════════════════════════════════════════════════
        question_lower = question.lower() if question else ""
        
        # Detectar tema de la pregunta - EXPANDIDO para múltiples dominios
        question_topics = {
            # Económico
            'economico': ['ayuda económica', 'dinero', 'económica', 'francos', 'billetes', 
                          'pago', 'suma', 'precio', 'costo', 'fortuna', 'herencia', 'deuda'],
            # Envío/Comunicación
            'envio': ['recibía', 'enviaba', 'mandaba', 'por correo', 'carta', 'mensaje',
                      'llegaba', 'entregaba', 'correspondencia'],
            # Existencia/Ocurrencia
            'existencia': ['ocurrió', 'sucedió', 'pasó', 'hubo', 'existió', 'había',
                           'tuvo lugar', 'aconteció', 'se produjo'],
            # Salud
            'salud': ['enfermedad', 'enfermo', 'murió', 'curó', 'salud', 'herido',
                      'recuperó', 'sobrevivió', 'falleció'],
            # Emociones
            'emocion': ['sentía', 'emoción', 'feliz', 'triste', 'miedo', 'amaba',
                        'odiaba', 'quería', 'temía'],
            # Eventos
            'evento': ['guerra', 'batalla', 'accidente', 'celebración', 'boda',
                       'viaje', 'reunión', 'encuentro'],
            # Verdad
            'verdad': ['verdad', 'cierto', 'real', 'confirmó', 'demostró', 'probó'],
            # Acciones
            'accion': ['hizo', 'dijo', 'decidió', 'logró', 'consiguió', 'intentó',
                       'descubrió', 'encontró', 'vio', 'oyó'],
        }
        
        for topic, topic_keywords in question_topics.items():
            # Si la pregunta trata sobre este tema
            if any(tk in question_lower for tk in topic_keywords):
                # Buscar keywords relacionados de critical_keywords
                related_keywords = critical_keywords.get(topic, [])
                # También agregar keywords del tema 'dinero' si es económico
                if topic == 'economico':
                    related_keywords = related_keywords + critical_keywords.get('dinero', [])
                # Agregar keywords de existencia para temas de eventos
                if topic in ['evento', 'existencia']:
                    related_keywords = related_keywords + critical_keywords.get('existencia', [])
                
                for keyword in related_keywords:
                    for pattern_template in negation_patterns:
                        pattern = pattern_template.format(keyword=keyword)
                        if re.search(pattern, answer_lower):
                            # Evitar duplicados
                            if not any(c['keyword'] == keyword and c['source'] == 'question' for c in contradictions_found):
                                contradictions_found.append({
                                    'category': topic,
                                    'keyword': keyword,
                                    'pattern': pattern,
                                    'source': 'question'
                                })
        
        # ═══════════════════════════════════════════════════════════════
        # ESTRATEGIA 3: Detección de contradicción numérica (NUEVO)
        # ═══════════════════════════════════════════════════════════════
        # Si el chunk menciona un número y la respuesta menciona otro diferente
        chunk_numbers = set(re.findall(r'\b\d+\b', chunk_lower))
        answer_numbers = set(re.findall(r'\b\d+\b', answer_lower))
        
        # Si hay números en ambos y no coinciden (excluyendo números muy comunes como 1, 2)
        significant_chunk_nums = {n for n in chunk_numbers if int(n) > 10}
        significant_answer_nums = {n for n in answer_numbers if int(n) > 10}
        
        if significant_chunk_nums and significant_answer_nums:
            mismatched = significant_answer_nums - significant_chunk_nums
            if mismatched and len(mismatched) > 0:
                # Hay números en la respuesta que no están en el chunk
                contradictions_found.append({
                    'category': 'numerico',
                    'keyword': f"números: {list(mismatched)[:2]}",
                    'pattern': 'numeric_mismatch',
                    'source': 'numeric'
                })
        
        if contradictions_found:
            # Cuantas más contradicciones, mayor penalización
            num_contradictions = len(contradictions_found)
            
            # Verificar si hay contradicciones con la PREGUNTA (más graves)
            question_contradictions = [c for c in contradictions_found if c.get('source') == 'question']
            has_question_contradiction = len(question_contradictions) > 0
            
            # ═══════════════════════════════════════════════════════════════
            # PENALIZACIÓN MÁS SEVERA:
            # - Contradicción con la pregunta = muy grave (el usuario niega
            #   exactamente lo que la pregunta pregunta)
            # - Múltiples contradicciones = grave
            # ═══════════════════════════════════════════════════════════════
            
            if has_question_contradiction:
                # Si niega algo que la pregunta pregunta directamente
                # Ejemplo: pregunta sobre "ayuda económica" y responde "nunca le mandó dinero"
                penalty = 0.20  # Reducir score al 20% (forzar rechazo)
                severity = "MUY GRAVE (contradice la pregunta)"
            elif num_contradictions >= 3:
                penalty = 0.25  # Reducir score al 25%
                severity = "GRAVE"
            elif num_contradictions >= 2:
                penalty = 0.30  # Reducir score al 30%
                severity = "MODERADA"
            else:
                penalty = 0.40  # Reducir score al 40%
                severity = "LEVE"
            
            keywords_negated = [c['keyword'] for c in contradictions_found[:3]]
            reason = f"Contradicción {severity}: negación de '{', '.join(keywords_negated)}'"
            
            print(f"   ⚠️ CONTRADICCIÓN DETECTADA: {reason}")
            print(f"   📉 Penalización: score × {penalty}")
            
            return True, penalty, reason
        
        return False, 1.0, ""
    
    def apply_pedagogical_boost(self, score_raw: float, cosine: float, 
                                user_answer: str, ref_text: str, question: str = "") -> float:
        """
        Booster pedagógico para respuestas de comprensión lectora.
        
        ═══════════════════════════════════════════════════════════════
        BASADO EN INVESTIGACIÓN:
        ═══════════════════════════════════════════════════════════════
        
        1. Sentence-BERT (Reimers & Gurevych, 2019):
           - Cosine similarity en embeddings tiene rango efectivo [0.3-0.8]
           - Por debajo de 0.3: sin relación semántica
           - Por encima de 0.6: alta similitud
           
        2. Short Answer Grading (Lloyd et al., 2022):
           - Las respuestas parafraseadas son tan válidas como las literales
           - El contenido semántico importa más que las palabras exactas
           
        3. Reading Comprehension Strategies (EEF, 2025):
           - Preguntas inferenciales requieren conectar ideas
           - La respuesta correcta puede NO contener palabras del texto
           
        ═══════════════════════════════════════════════════════════════
        ESTRATEGIA DE BOOST:
        ═══════════════════════════════════════════════════════════════
        
        A) LITERAL (recuerdo directo):
           - Threshold: cosine >= 0.40
           - Boost: x1.3 si respuesta concisa
           
        B) INFERENCIAL (razonamiento):
           - Threshold: cosine >= 0.35 (más flexible!)
           - Boost: x1.4 (reconoce esfuerzo cognitivo mayor)
           - El usuario puede usar palabras propias
        
        Args:
            score_raw: Score antes del boost [0,1]
            cosine: Similitud de embeddings normalizada [0,1]
            user_answer: Texto de la respuesta del usuario
            ref_text: Texto del chunk de referencia
            question: Texto de la pregunta (para detectar tipo)
            
        Returns:
            float: Score después del boost (máx 0.99)
        """
        is_inferential = question and self.is_inferential_question(question)
        
        # Umbrales diferenciados según tipo de pregunta
        if is_inferential:
            # Preguntas inferenciales: más tolerantes
            # El usuario usa sus propias palabras para explicar
            BASE_THRESHOLD = 0.30      # Más bajo: permite parafraseo
            BOOST_THRESHOLD = 0.35     # Umbral para boost
            BOOST_FACTOR = 1.45        # Boost más alto: reconoce razonamiento
            print(f"   🧠 Pregunta INFERENCIAL detectada - umbral flexible")
        else:
            # Preguntas literales: estándar
            BASE_THRESHOLD = 0.40
            BOOST_THRESHOLD = 0.45
            BOOST_FACTOR = 1.30
        
        # Si está por debajo del umbral base, no hay boost
        if cosine < BASE_THRESHOLD:
            return score_raw
        
        # Calcular ratio de longitud (palabras)
        len_user = max(len(user_answer.split()), 1)
        len_ref = max(len(ref_text.split()), 1)
        len_ratio = len_user / len_ref
        
        boosted = score_raw
        
        # Boost 1: Respuestas concisas pero correctas (síntesis)
        if len_ratio < 0.5 and cosine >= BOOST_THRESHOLD:
            # El usuario sintetizó bien la información
            factor = 1.5 if len_ratio < 0.3 else 1.35
            boosted = score_raw * factor
            print(f"   📝 Boost síntesis aplicado: x{factor:.2f}")
        
        # Boost 2: Preguntas inferenciales con respuesta razonada
        elif is_inferential and cosine >= BOOST_THRESHOLD:
            # El usuario demostró comprensión profunda
            boosted = score_raw * BOOST_FACTOR
            print(f"   🎯 Boost inferencial aplicado: x{BOOST_FACTOR:.2f}")
        
        # Limitar a 99% máximo (nunca dar 100% automáticamente)
        return min(boosted, 0.99)
    
    def normalize_embedding(self, embedding: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(embedding)
        if norm < 1e-10:  # Threshold para evitar division por cero o numeros muy pequeños
            return embedding
        return embedding / norm
    
    def extract_keywords(self, text: str):
        # Normalizar texto antes de extraer keywords (quitar espacios OCR)
        # Ejemplo: "H enriet te" → "Henriette"
        text = re.sub(r'\b(\w{1,2})\s+(\w{1,2})\b', r'\1\2', text)
        for _ in range(3):
            text = re.sub(r'\b(\w{1,2})\s+(\w{1,2})\b', r'\1\2', text)
        text = re.sub(r'\b(\w{2,4})\s+(\w{3,6})\b', r'\1\2', text)
        
        text = text.lower()
        words = re.findall(r'\b\w{3,}\b', text)
        keywords = [w for w in words if w not in self.stopwords]
        return keywords
    
    def expand_keywords(self, keywords):
        expanded = set(keywords)
        for word in keywords:
            expanded.add(word)
            if len(word) >= 6:
                expanded.add(word[:6])
            elif len(word) >= 5:
                expanded.add(word[:5])
            if word[0].isupper():
                expanded.add(word.lower())
        return expanded
    
    def bm25_score(self, query_keywords, chunk_text: str, corpus):
        tokenized_corpus = [self.extract_keywords(text) for text in corpus]
        
        # Protección: si el corpus está vacío o todos los documentos vacíos
        if not tokenized_corpus or all(len(doc) == 0 for doc in tokenized_corpus):
            return 0.0
        
        bm25 = BM25Okapi(tokenized_corpus)
        expanded_query = list(self.expand_keywords(query_keywords))
        
        # Protección: si la query está vacía
        if not expanded_query:
            return 0.0
        
        scores = bm25.get_scores(expanded_query)
        chunk_keywords = self.extract_keywords(chunk_text)
        try:
            chunk_index = tokenized_corpus.index(chunk_keywords)
            return scores[chunk_index]
        except ValueError:
            return np.mean(scores) if len(scores) > 0 else 0.0
    
    def cosine_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        emb1_norm = self.normalize_embedding(emb1)
        emb2_norm = self.normalize_embedding(emb2)
        similarity = np.dot(emb1_norm, emb2_norm)
        return max(0.0, min(1.0, similarity))
    
    def calculate_coverage(self, answer_keywords, chunk_keywords):
        answer_expanded = self.expand_keywords(answer_keywords)
        chunk_expanded = self.expand_keywords(chunk_keywords)
        intersection = answer_expanded & chunk_expanded
        if len(answer_expanded) == 0:
            return 0.0
        coverage = len(intersection) / len(answer_expanded)
        return coverage
    
    def hybrid_score(self, question: str, answer: str, chunk, all_chunks):
        question_keywords = self.extract_keywords(question)
        answer_keywords = self.extract_keywords(answer)
        combined_keywords = list(set(question_keywords + answer_keywords))
        
        answer_embedding = self.normalize_embedding(
            self.model.encode(answer, convert_to_tensor=False)
        )
        chunk_embedding = self.normalize_embedding(
            np.array(chunk['embedding'])
        )
        
        corpus = [c['text_full'] for c in all_chunks]
        bm25_score_raw = self.bm25_score(combined_keywords, chunk['text_full'], corpus)
        bm25_normalized = min(1.0, bm25_score_raw / 10.0)
        
        cosine_score_raw = self.cosine_similarity(answer_embedding, chunk_embedding)
        # NUEVO: Normalizar cosine al rango 0-1 basado en valores empíricos
        cosine_normalized = self.normalize_cosine(cosine_score_raw)
        
        chunk_keywords = self.extract_keywords(chunk['text_full'])
        coverage_score = self.calculate_coverage(answer_keywords, chunk_keywords)
        
        # Score base: combinar métricas normalizadas con pesos calibrados
        # 80% semántica + 15% cobertura + 5% léxico (reducido por OCR)
        score_base = (
            self.weights['bm25'] * bm25_normalized +
            self.weights['cosine'] * cosine_normalized +
            self.weights['coverage'] * coverage_score
        )
        
        # Aplicar bonus por longitud razonable (+5% máximo)
        bonus = self.length_bonus(answer)
        score_raw = max(0.0, min(1.0, score_base + bonus))  # Clamp a [0,1]
        
        # NUEVO: Aplicar boost pedagógico para respuestas concisas pero correctas
        # + boost inferencial para preguntas de razonamiento
        score_raw = self.apply_pedagogical_boost(
            score_raw=score_raw,
            cosine=cosine_normalized,
            user_answer=answer,
            ref_text=chunk['text_full'],
            question=question  # Para detectar preguntas inferenciales
        )
        
        # ═══════════════════════════════════════════════════════════════
        # NUEVO: Re-ranking basado en tipo de pregunta (Rationale-Aware)
        # ═══════════════════════════════════════════════════════════════
        # Si la pregunta es de razonamiento, dar boost a chunks con más
        # diálogo y verbos de pensamiento/opinión
        question_type = self.classify_question_type(question)
        reasoning_score = self.compute_reasoning_score(chunk['text_full'])
        reasoning_boost_applied = 0.0
        
        if question_type == 'reasoning' and reasoning_score > 0.1:
            # Boost suave: máximo +20% al score
            # No rompe el score semántico, solo inclina la balanza
            reasoning_boost_applied = 0.20 * reasoning_score
            score_raw = score_raw * (1 + reasoning_boost_applied)
            score_raw = min(score_raw, 0.99)  # Nunca superar 99%
            print(f"   🧠 Boost razonamiento: +{reasoning_boost_applied*100:.1f}% (reasoning_score={reasoning_score:.2f})")
        
        # ═══════════════════════════════════════════════════════════════
        # NUEVO: Detección de contradicción (NLI simplificado)
        # ═══════════════════════════════════════════════════════════════
        # Si el usuario NIEGA conceptos clave del chunk, penalizar fuertemente
        # Ejemplo: chunk dice "recibía dinero" → usuario dice "nunca le mandó dinero"
        is_contradiction, penalty_factor, contradiction_reason = self.detect_contradiction(
            user_answer=answer,
            chunk_text=chunk['text_full'],
            question=question
        )
        
        if is_contradiction:
            score_raw = score_raw * penalty_factor
            print(f"   📉 Score después de penalización: {score_raw:.4f}")
        
        # Convertir a porcentaje 0-100% con min-max scaling
        score_pct = self.to_percentage(score_raw)
        
        details = {
            'bm25': round(bm25_normalized, 4),
            'cosine': round(cosine_score_raw, 4),  # Raw para logs
            'cosine_normalized': round(cosine_normalized, 4),  # Normalizado
            'coverage': round(coverage_score, 4),
            'score_base': round(score_base, 4),
            'length_bonus': round(bonus, 4),
            'score_raw': round(score_raw, 4),  # Score bruto [0,1]
            'score_pct': score_pct,  # Porcentaje [0-100]
            'final': round(score_raw, 4),  # Mantener compatibilidad
            'weights': self.weights,
            'keywords_found': list(
                self.expand_keywords(answer_keywords) & 
                self.expand_keywords(chunk_keywords)
            )[:5],
            # NUEVO: Info de contradicción para debugging
            'contradiction_detected': is_contradiction,
            'contradiction_reason': contradiction_reason if is_contradiction else None,
            'contradiction_penalty': penalty_factor if is_contradiction else 1.0,
            # NUEVO: Info de re-ranking por tipo de pregunta
            'question_type': question_type,
            'reasoning_score': round(reasoning_score, 4),
            'reasoning_boost': round(reasoning_boost_applied, 4)
        }
        
        return score_raw, details
    
    def detect_ambiguity(self, ranked_chunks):
        if len(ranked_chunks) < 2:
            return {'is_ambiguous': False, 'reason': 'Menos de 2 chunks'}
        
        top1_score = ranked_chunks[0][1]
        top2_score = ranked_chunks[1][1]
        score_diff = top1_score - top2_score
        is_ambiguous = score_diff < 0.08
        
        return {
            'is_ambiguous': is_ambiguous,
            'score_diff': round(score_diff, 4),
            'top1_score': round(top1_score, 4),
            'top2_score': round(top2_score, 4),
            'threshold': 0.08
        }
    
    def validate_answer(self, question: str, user_answer: str, chunks):
        if not chunks or len(chunks) == 0:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'feedback': 'No hay chunks disponibles para validacion',
                'category': 'error'
            }
        
        if len(user_answer.strip()) < 10:
            return {
                'is_valid': False,
                'confidence': 0.0,
                'feedback': 'La respuesta es demasiado corta (minimo 10 caracteres)',
                'category': 'error'
            }
        
        scored_chunks = []
        for chunk in chunks:
            score, details = self.hybrid_score(question, user_answer, chunk, chunks)
            scored_chunks.append((chunk, score, details))
        
        ranked_chunks = sorted(scored_chunks, key=lambda x: x[1], reverse=True)
        top_k = ranked_chunks[:3]
        
        ambiguity = self.detect_ambiguity([(c, s) for c, s, _ in ranked_chunks])
        
        best_chunk, best_score_raw, best_details = top_k[0]
        best_score_pct = best_details['score_pct']  # Usar porcentaje para UI
        
        # Clasificación basada en score_raw (0-1)
        if best_score_raw >= self.thresholds['excelente']:
            category = 'excelente'
            is_valid = True
            feedback = 'Excelente! Tu respuesta captura perfectamente el contenido.'
        elif best_score_raw >= self.thresholds['bueno']:
            category = 'bueno'
            is_valid = True
            feedback = 'Muy bien. Tu respuesta es correcta y bien fundamentada.'
        elif best_score_raw >= self.thresholds['aceptable']:
            category = 'aceptable'
            is_valid = True
            feedback = 'Aceptable. Tu respuesta esta en la direccion correcta.'
        else:
            category = 'necesita_mejorar'
            is_valid = False
            feedback = 'Tu respuesta necesita más trabajo. Revisa el material.'
        
        result = {
            'is_valid': is_valid,
            'confidence': best_score_pct,  # Porcentaje 0-100
            'score_raw': round(best_score_raw, 4),  # Score bruto [0,1]
            'feedback': feedback,
            'category': category,
            'best_chunk': {
                'text': best_chunk['text_full'][:200] + '...' if len(best_chunk['text_full']) > 200 else best_chunk['text_full'],
                'page': best_chunk.get('page_number', 'N/A'),
                'chunk_id': best_chunk.get('chunk_id', 'N/A')
            },
            'top_3_scores': [
                {
                    'score': d['score_pct'],  # Porcentaje
                    'score_raw': d['score_raw'],  # Bruto
                    'chunk_id': c.get('chunk_id', 'N/A'),
                    'details': d
                }
                for c, s, d in top_k
            ],
            'ambiguity': ambiguity,
            'thresholds': {k: v * 100 for k, v in self.thresholds.items()},
            'scoring_method': 'HybridValidator (BM25 + Cosine + Coverage)',
            'weights_used': self.weights
        }
        
        return result
