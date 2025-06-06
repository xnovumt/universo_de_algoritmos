# dfa_validators.py
# Este archivo contiene la lógica de los autómatas finitos deterministas (AFD)
# para la validación de formatos, sin lógica de ejecución directa.

import re # Importa el módulo 're' para usar expresiones regulares (útil para validaciones preliminares de formato).
from typing import Set, Dict, Tuple # Importa tipos para mejorar la legibilidad y validación de parámetros (type hinting) en las definiciones de funciones y clases.

# Clase base para el Autómata Finito Determinista (AFD)
# Esta clase genérica implementa la lógica fundamental de un AFD.
class DFA:
    def __init__(self, states: Set[str], alphabet: Set[str], transitions: Dict[Tuple[str, str], str], 
                 start_state: str, accept_states: Set[str]):
        """
        Inicializa un autómata finito determinista (AFD).

        Parámetros:
        - states (Set[str]): Conjunto de todos los estados posibles del AFD (ej. {'S0', 'S1', ..., 'Sn', 'E'}).
          'E' es comúnmente usado como un estado de error al que se transiciona si la entrada es inesperada.
        - alphabet (Set[str]): Conjunto de todos los símbolos de entrada válidos que el AFD puede procesar.
          Cada carácter de la cadena de entrada debe pertenecer a este alfabeto.
        - transitions (Dict[Tuple[str, str], str]): Un diccionario que define la función de transición (δ) del AFD.
          La clave de cada entrada es una tupla (estado_actual, símbolo_de_entrada) y el valor es el estado_siguiente.
          Ejemplo: {('S0', '1'): 'S1'} significa que si el AFD está en el estado 'S0' y lee un '1',
          transiciona al estado 'S1'.
        - start_state (str): El estado inicial desde el cual el AFD comienza a procesar cualquier cadena de entrada.
          Por convención, suele ser 'S0'.
        - accept_states (Set[str]): Conjunto de estados de aceptación del AFD.
          Si el AFD termina en uno de estos estados después de procesar completamente una cadena,
          esa cadena se considera válida (aceptada).
        """
        self.states = states          # Almacena el conjunto de estados
        self.alphabet = alphabet      # Almacena el alfabeto de entrada
        self.transitions = transitions  # Almacena el diccionario de transiciones (la función delta)
        self.start_state = start_state  # Almacena el estado inicial
        self.accept_states = accept_states  # Almacena el conjunto de estados de aceptación

    def validate(self, input_string: str) -> Tuple[bool, str, int]:
        """
        Valida una cadena de entrada utilizando el AFD.

        Este método simula el recorrido del AFD sobre la cadena de entrada carácter por carácter.
        Determina si la cadena es aceptada por el AFD de acuerdo con sus transiciones y estados de aceptación.

        Flujo de validación:
        1. Inicia en el estado inicial.
        2. Para cada carácter en la cadena de entrada:
            a. Verifica si el carácter es parte del alfabeto del AFD. Si no, la cadena es inválida.
            b. Busca la transición para el estado actual y el carácter leído.
            c. Si no hay una transición definida, asume una transición al estado de error 'E'.
            d. Actualiza el estado actual al nuevo estado.
            e. Si se llega al estado 'E' (y 'E' no es un estado de aceptación), la cadena es inválida.
        3. Después de procesar todos los caracteres, verifica si el estado final es uno de los estados de aceptación.

        Parámetros:
        - input_string (str): La cadena que se va a validar (ej. "1234 5678...").

        Retorna:
        - Tuple[bool, str, int]: Una tupla que contiene:
            - bool: True si la cadena es aceptada por el AFD, False en caso contrario.
            - str: Un mensaje descriptivo del error si la cadena es inválida (vacío si es válida).
            - int: La posición (índice basado en 0) en la cadena donde se detectó el error (-1 si es válida).
        """
        current_state = self.start_state # El AFD siempre comienza en su estado inicial.
        
        # Itera sobre cada carácter de la cadena de entrada, obteniendo tanto el índice (i) como el carácter (char).
        for i, char in enumerate(input_string):
            # Paso 2a: Verifica si el carácter actual es parte del alfabeto definido para este AFD.
            if char not in self.alphabet:
                # Si el carácter no está en el alfabeto, la cadena es inválida inmediatamente.
                return False, f"Carácter inválido: '{char}'", i 
            
            # Paso 2b y 2c: Obtiene el siguiente estado basándose en el estado actual y el carácter leído.
            # `self.transitions.get((current_state, char), 'E')` busca la transición.
            # Si no se encuentra una transición explícitamente definida para esa combinación (estado, carácter),
            # se asume que el AFD transiciona al estado de error 'E'.
            next_state = self.transitions.get((current_state, char), 'E')
            
            current_state = next_state # Paso 2d: Actualiza el estado actual al estado recién determinado.
            
            # Paso 2e: Si el AFD ha entrado en el estado de error 'E', y 'E' no está configurado
            # como un estado de aceptación (que es el caso normal para 'E'),
            # significa que la cadena no es válida en este punto.
            if current_state == 'E' and 'E' not in self.accept_states:
                return False, f"Transición a estado de error en '{char}'", i # Retorna False con un mensaje de error y la posición.
            
        # Paso 3: Una vez que todos los caracteres de la cadena han sido procesados,
        # se verifica si el estado en el que el AFD ha terminado es uno de los estados de aceptación.
        if current_state in self.accept_states:
            return True, "", -1 # Si el estado final es de aceptación, la cadena es válida. Se retorna True, sin mensaje de error y -1 en posición.
        else:
            # Si el estado final no es de aceptación, la cadena es inválida. Se retorna False con un mensaje que indica el estado final.
            return False, f"Estado final {current_state} no es de aceptación", len(input_string) # La posición de error es el final de la cadena.


# Implementación específica de un AFD para validar números de tarjeta de crédito
# Cumple con el requisito 1 del proyecto: "Número de tarjeta de crédito".
class CreditCardDFA:
    def _init_(self):
        """
        Inicializa el AFD diseñado para validar el formato de números de tarjeta de crédito.
        
        El formato esperado es: dddd dddd dddd dddd mm/aaaa cvv
        (16 dígitos en 4 grupos, espacio, fecha de 2 dígitos de mes / 4 dígitos de año, espacio, 3 dígitos de CVV).
        """
        # Define el conjunto de estados para el AFD de tarjeta de crédito.
        # Se necesitan 31 estados para el recorrido de la cadena (S0 a S31), más el estado de error 'E'.
        states = {f'S{i}' for i in range(32)} | {'E'} 
        # Define el alfabeto permitido: dígitos (0-9), espacio (' ') y barra ('/').
        alphabet = set('0123456789 /')
        transitions = {} # Se inicializa un diccionario vacío para definir las transiciones.

        # --- Definición de transiciones por secciones del formato de la tarjeta ---

        # 1. Primeros 4 dígitos del número de tarjeta (S0 a S4)
        for i in range(4): # Estados S0, S1, S2, S3
            for c in '0123456789': # Para cada dígito
                transitions[(f'S{i}', c)] = f'S{i+1}' # Transiciona al siguiente estado
        transitions[('S4', ' ')] = 'S5' # Después de 4 dígitos, espera un espacio para ir a S5.

        # 2. Siguientes 4 dígitos (S5 a S9)
        for i in range(5, 9): # Estados S5, S6, S7, S8
            for c in '0123456789':
                transitions[(f'S{i}', c)] = f'S{i+1}'
        transitions[('S9', ' ')] = 'S10' # Después de 4 dígitos, espera un espacio para ir a S10.

        # 3. Siguientes 4 dígitos (S10 a S14)
        for i in range(10, 14): # Estados S10, S11, S12, S13
            for c in '0123456789':
                transitions[(f'S{i}', c)] = f'S{i+1}'
        transitions[('S14', ' ')] = 'S15' # Después de 4 dígitos, espera un espacio para ir a S15.

        # 4. Últimos 4 dígitos del número de tarjeta (S15 a S19)
        for i in range(15, 19): # Estados S15, S16, S17, S18
            for c in '0123456789':
                transitions[(f'S{i}', c)] = f'S{i+1}'
        transitions[('S19', ' ')] = 'S20' # Después de 4 dígitos, espera un espacio antes de la fecha.

        # 5. Fecha de expiración (mm/aaaa) (S20 a S27)
        # Primer dígito del mes (0 o 1)
        for m1 in '01':
            transitions[('S20', m1)] = 'S21'
        # Segundo dígito del mes (0-9)
        for m2 in '0123456789': 
            transitions[('S21', m2)] = 'S22'
        
        transitions[('S22', '/')] = 'S23' # Espera la barra separadora entre mes y año.

        # 4 dígitos del año
        for i in range(23, 27): # Estados S23, S24, S25, S26
            for y in '0123456789':
                transitions[(f'S{i}', y)] = f'S{i+1}'
        
        transitions[('S27', ' ')] = 'S28' # Espera un espacio antes del CVV.

        # 6. Código de verificación CVV (3 dígitos) (S28 a S31)
        for i in range(28, 31): # Estados S28, S29, S30
            for c in '0123456789':
                transitions[(f'S{i}', c)] = f'S{i+1}'

        # Llenar transiciones al estado de error 'E'
        # Esto asegura que si cualquier estado recibe un carácter no esperado o no definido en sus transiciones,
        # el AFD se mueva al estado de error 'E'.
        for state in states:
            for char in alphabet:
                if (state, char) not in transitions:
                    transitions[(state, char)] = 'E'
        # Una vez en el estado 'E', cualquier caracter lo mantiene en 'E'.
        for c in alphabet:
            transitions[('E', c)] = 'E'

        # Inicializa una instancia de la clase base DFA con la configuración específica de la tarjeta de crédito.
        # El estado final de aceptación para el formato de la tarjeta es S31.
        self.dfa = DFA(states, alphabet, transitions, 'S0', {'S31'})

    def validate(self, input_string: str) -> Tuple[bool, str, int]:
        """
        Valida una cadena de tarjeta de crédito.
        
        Realiza una serie de validaciones:
        1. Validación preliminar del formato general y longitud usando una expresión regular.
        2. Validación semántica de la fecha de vencimiento (mes válido y año no expirado).
        3. Validación estructural completa utilizando el AFD (self.dfa.validate).
        """
        # 1. Validación preliminar con expresiones regulares:
        # Esta regex verifica la estructura general (número de dígitos, espacios y barra)
        # de forma rápida antes de involucrar al DFA. Es más eficiente para un chequeo de formato inicial.
        if not re.match(r'^\d{4} \d{4} \d{4} \d{4} \d{2}/\d{4} \d{3}$', input_string):
            return False, "Formato inválido: debe ser dddd dddd dddd dddd mm/aaaa cvv", 0
        
        # 2. Validación semántica de la fecha de vencimiento:
        # El DFA solo valida la estructura (dos dígitos, barra, cuatro dígitos).
        # Las reglas de negocio (mes 1-12, año >= 2025) son validaciones semánticas
        # que se manejan aquí.
        parts = input_string.split(' ') # Divide la cadena por espacios.
        date_part = parts[4] # La parte de la fecha es el quinto elemento (índice 4).
        month_str, year_str = date_part.split('/') # Divide la fecha en mes y año.

        try:
            month = int(month_str) # Convierte el mes a entero.
            year = int(year_str)   # Convierte el año a entero.
            # Verifica que el mes esté entre 1 y 12, y que el año no sea anterior a 2025 (regla de negocio arbitraria).
            if not (1 <= month <= 12 and year >= 2025): 
                return False, "Mes o año inválido", input_string.find('/') # Retorna error si la fecha es semánticamente inválida.
        except ValueError: # Captura si month_str o year_str no son convertibles a enteros.
            return False, "Formato de fecha inválido (no numérico)", input_string.find('/')

        # 3. Validación estructural con el AFD:
        # Si todas las validaciones preliminares y semánticas pasan, se pasa la cadena
        # al AFD para la validación de la secuencia exacta de transiciones.
        return self.dfa.validate(input_string)


