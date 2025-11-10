"""
TIPOS DE ENTIDADES UNIVERSALES - RECUIVA
==========================================

Define indicadores lingüísticos UNIVERSALES que funcionan para:
- Literatura (señor, conde, reina)
- Ciencia (proteína, enzima, compuesto)
- Técnico (algoritmo, método, proceso)
- Académico (teoría, ley, principio)

NO es específico de "El Collar de la Reina" - funciona para CUALQUIER PDF.

Autor: Abel Jesús Moya Acosta
Fecha: 10 de noviembre de 2025
"""

from enum import Enum
from typing import Dict, Set, List
import re


class EntityType(Enum):
    """Tipos de entidades universales (independientes del dominio)"""
    PERSON = "persona"          # María, doctor García
    CONCEPT = "concepto"        # teoría de la relatividad, ley de Newton
    OBJECT = "objeto"           # proteína BRCA1, collar de la reina
    PROCESS = "proceso"         # algoritmo QuickSort, fotosíntesis
    LOCATION = "ubicación"      # París, laboratorio X
    ORGANIZATION = "org"        # universidad, empresa
    UNKNOWN = "desconocido"


# ============================================================================
# INDICADORES UNIVERSALES - Funcionan para CUALQUIER dominio
# ============================================================================

UNIVERSAL_INDICATORS: Dict[EntityType, List[str]] = {
    
    # PERSONAS - Literatura, Historia, Biografías
    EntityType.PERSON: [
        # Títulos nobleza
        'señor', 'señora', 'señorita', 'don', 'doña',
        'conde', 'condesa', 'duque', 'duquesa', 'marqués', 'marquesa',
        'rey', 'reina', 'príncipe', 'princesa', 'emperador', 'emperatriz',
        
        # Títulos religiosos
        'papa', 'cardenal', 'obispo', 'arzobispo', 'padre', 'fray',
        'hermano', 'hermana', 'sor', 'san', 'santa', 'monseñor',
        
        # Títulos académicos/profesionales
        'doctor', 'doctora', 'dr', 'dra',
        'profesor', 'profesora', 'prof',
        'ingeniero', 'ingeniera', 'ing',
        'licenciado', 'licenciada', 'lic',
        'maestro', 'maestra', 'mtra', 'mtro',
        
        # Títulos militares
        'general', 'coronel', 'capitán', 'teniente', 'sargento',
        'almirante', 'comandante', 'mayor',
        
        # Relaciones familiares (solo en contexto específico)
        'esposo', 'esposa', 'hijo', 'hija', 'hermano', 'hermana',
        'padre', 'madre', 'abuelo', 'abuela', 'tío', 'tía',
        'sobrino', 'sobrina', 'primo', 'prima'
    ],
    
    # CONCEPTOS - Ciencia, Filosofía, Academia
    EntityType.CONCEPT: [
        # Científicos
        'teoría', 'ley', 'principio', 'hipótesis', 'modelo',
        'paradigma', 'postulado', 'axioma', 'teorema', 'corolario',
        
        # Filosóficos
        'concepto', 'idea', 'noción', 'tesis', 'doctrina',
        'ideología', 'corriente', 'escuela', 'movimiento',
        
        # Técnicos
        'método', 'técnica', 'metodología', 'enfoque', 'estrategia',
        'sistema', 'marco', 'esquema', 'estructura'
    ],
    
    # OBJETOS - Ciencia, Medicina, Química, Física
    EntityType.OBJECT: [
        # Biología/Medicina
        'proteína', 'enzima', 'gen', 'cromosoma', 'adn', 'arn',
        'célula', 'órgano', 'tejido', 'molécula', 'átomo',
        'bacteria', 'virus', 'anticuerpo', 'hormona',
        
        # Química
        'compuesto', 'elemento', 'sustancia', 'reactivo', 'catalizador',
        'ácido', 'base', 'sal', 'óxido', 'ion', 'radical',
        
        # Física
        'partícula', 'onda', 'campo', 'fuerza', 'energía',
        'masa', 'velocidad', 'aceleración',
        
        # Objetos físicos generales
        'objeto', 'artefacto', 'dispositivo', 'instrumento',
        'herramienta', 'máquina', 'aparato', 'equipo',
        
        # Objetos específicos (literatura, historia)
        'collar', 'anillo', 'corona', 'espada', 'armadura',
        'libro', 'manuscrito', 'documento', 'carta', 'diploma'
    ],
    
    # PROCESOS - Informática, Matemáticas, Procedimientos
    EntityType.PROCESS: [
        # Informática
        'algoritmo', 'programa', 'software', 'aplicación', 'función',
        'procedimiento', 'rutina', 'script', 'código',
        
        # Biología
        'proceso', 'ciclo', 'síntesis', 'metabolismo', 'respiración',
        'fotosíntesis', 'mitosis', 'meiosis', 'transcripción', 'traducción',
        
        # Generales
        'mecanismo', 'operación', 'protocolo',
        'fase', 'etapa', 'paso', 'secuencia'
    ],
    
    # UBICACIONES - Geografía, Lugares
    EntityType.LOCATION: [
        'ciudad', 'país', 'región', 'provincia', 'estado', 'nación',
        'continente', 'isla', 'península', 'cabo', 'golfo',
        'montaña', 'cordillera', 'valle', 'río', 'lago', 'mar', 'océano',
        'calle', 'avenida', 'plaza', 'parque', 'edificio', 'torre',
        'palacio', 'castillo', 'catedral', 'iglesia', 'templo',
        'museo', 'biblioteca', 'universidad', 'hospital', 'laboratorio'
    ],
    
    # ORGANIZACIONES - Instituciones, Empresas
    EntityType.ORGANIZATION: [
        'universidad', 'instituto', 'academia', 'escuela', 'colegio',
        'empresa', 'corporación', 'compañía', 'firma', 'negocio',
        'organización', 'asociación', 'fundación', 'sociedad',
        'gobierno', 'ministerio', 'departamento', 'agencia',
        'partido', 'grupo', 'equipo'
    ]
}


# ============================================================================
# PALABRAS FUNCIONALES - NUNCA son entidades (español universal)
# ============================================================================

FUNCTION_WORDS: Set[str] = {
    # Artículos
    'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
    
    # Preposiciones
    'a', 'ante', 'bajo', 'con', 'contra', 'de', 'desde', 'durante',
    'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 'por',
    'según', 'sin', 'sobre', 'tras', 'versus', 'vía',
    
    # Conjunciones
    'y', 'e', 'ni', 'que', 'o', 'u', 'pero', 'mas', 'sino',
    'aunque', 'como', 'cuando', 'donde', 'porque', 'pues', 'si',
    'mientras', 'luego', 'conque',
    
    # Pronombres
    'yo', 'tú', 'él', 'ella', 'nosotros', 'nosotras', 'vosotros',
    'vosotras', 'ellos', 'ellas', 'usted', 'ustedes',
    'me', 'te', 'se', 'nos', 'os', 'lo', 'la', 'le', 'les',
    'este', 'ese', 'aquel', 'esto', 'eso', 'aquello',
    'quien', 'cual', 'cuyo', 'cuanto',
    
    # Adverbios comunes
    'muy', 'más', 'menos', 'tan', 'tanto', 'mucho', 'poco',
    'bastante', 'demasiado', 'casi', 'solo', 'solamente',
    'también', 'tampoco', 'sí', 'no', 'nunca', 'siempre', 'jamás',
    'aquí', 'ahí', 'allí', 'acá', 'allá', 'cerca', 'lejos',
    'antes', 'después', 'luego', 'entonces', 'ahora', 'hoy',
    'ayer', 'mañana', 'bien', 'mal', 'así', 'tal', 'recién',
    
    # Determinantes
    'algún', 'alguna', 'algunos', 'algunas', 'ningún', 'ninguna',
    'todo', 'toda', 'todos', 'todas', 'otro', 'otra', 'otros', 'otras',
    'mismo', 'misma', 'mismos', 'mismas', 'cada', 'cualquier',
    
    # Números cardinales (evitar "Dos personas", "Tres días")
    'cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete',
    'ocho', 'nueve', 'diez', 'once', 'doce', 'trece', 'catorce', 'quince',
    'veinte', 'treinta', 'cuarenta', 'cincuenta', 'cien', 'mil',
    'varios', 'muchos', 'pocos', 'algunos', 'demasiados'
}


# ============================================================================
# VERBOS DE CONTEXTO - Ayudan a identificar tipo de entidad
# ============================================================================

CONTEXT_VERBS: Dict[EntityType, Set[str]] = {
    
    EntityType.PERSON: {
        # Verbos de comunicación (solo personas hablan)
        'dijo', 'dice', 'decir', 'preguntó', 'pregunta', 'preguntar',
        'respondió', 'responde', 'responder', 'exclamó', 'exclama',
        'gritó', 'grita', 'susurró', 'susurra', 'murmuró', 'murmura',
        
        # Verbos de pensamiento/emoción
        'pensó', 'piensa', 'pensar', 'creyó', 'cree', 'creer',
        'sintió', 'siente', 'sentir', 'amó', 'ama', 'amar',
        'temió', 'teme', 'temer', 'odiaba', 'odia', 'odiar',
        
        # Verbos de acción humana
        'caminó', 'camina', 'entró', 'entra', 'salió', 'sale',
        'miró', 'mira', 'vio', 've', 'escuchó', 'escucha'
    },
    
    EntityType.CONCEPT: {
        'define', 'explica', 'establece', 'propone', 'postula',
        'plantea', 'sugiere', 'implica', 'sostiene', 'afirma'
    },
    
    EntityType.OBJECT: {
        'contiene', 'produce', 'forma', 'compone', 'integra',
        'consiste', 'incluye', 'abarca', 'presenta', 'muestra'
    },
    
    EntityType.PROCESS: {
        'ejecuta', 'realiza', 'implementa', 'desarrolla', 'procesa',
        'calcula', 'genera', 'transforma', 'convierte', 'opera'
    },
    
    EntityType.LOCATION: {
        'ubica', 'sitúa', 'localiza', 'encuentra', 'está',
        'queda', 'extiende', 'limita', 'bordea'
    }
}


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def is_function_word(word: str) -> bool:
    """Verifica si una palabra es funcional (nunca entidad)"""
    return word.lower() in FUNCTION_WORDS


def get_indicators_for_type(entity_type: EntityType) -> List[str]:
    """Retorna indicadores para un tipo específico"""
    return UNIVERSAL_INDICATORS.get(entity_type, [])


def get_all_indicators() -> Set[str]:
    """Retorna TODOS los indicadores de todos los tipos"""
    all_indicators = set()
    for indicators in UNIVERSAL_INDICATORS.values():
        all_indicators.update(indicators)
    return all_indicators


def infer_type_from_indicator(indicator: str) -> EntityType:
    """Infiere tipo de entidad basándose en el indicador usado"""
    indicator_lower = indicator.lower()
    
    for entity_type, indicators in UNIVERSAL_INDICATORS.items():
        if indicator_lower in indicators:
            return entity_type
    
    return EntityType.UNKNOWN
