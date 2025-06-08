# main.py
# Este archivo es el punto de entrada para ejecutar las pruebas en consola
# de los validadores AFD definidos en dfa_validators.py.

# Importa las clases de los autómatas y la función process_file
# desde el módulo dfa_validators.
from dfa_validators import CreditCardDFA, CURPDFA, process_file

def run_tests_in_console():
    """
    Función principal para la ejecución de todas las pruebas del programa en la consola.
    
    1. Crea instancias de los validadores de Tarjeta de Crédito y CURP.
    2. Ejecuta pruebas individuales con cadenas de ejemplo predefinidas.
    3. Llama a `process_file` para validar cadenas desde archivos de texto.
    """
    # Crea instancias de los validadores. Cada instancia de DFA está preconfigurada con sus propias reglas.
    cc_validator = CreditCardDFA() 
    curp_validator = CURPDFA()

    print("=== Pruebas individuales ===")
    
    print("\n--- Pruebas de Tarjeta de Crédito ---")
    # Conjunto de cadenas de ejemplo que deberían ser válidas según el formato de tarjeta de crédito.
    valid_cc_tests = [
        "1234 5678 9012 3456 03/2029 336",
        "4321 8765 2109 6543 12/2030 789",
        "9876 5432 1098 7654 05/2026 123",
    ]
    # Itera sobre las cadenas válidas y muestra su resultado de validación.
    for test_cc in valid_cc_tests:
        is_valid, error_msg, error_pos = cc_validator.validate(test_cc)
        print(f"Credit Card - '{test_cc}': {'Válida' if is_valid else f'Inválida ({error_msg})'}")

    # Conjunto de cadenas de ejemplo que deberían ser inválidas.
    invalid_cc_tests = [
        "1234 5678 9012 3456 13/2029 336",   # Mes inválido (validación semántica de la fecha).
        "1234 5678 9012 3456 03/2024 336",   # Año inválido (< 2025) (validación semántica de la fecha).
        "123 4567 8901 2345 01/2025 123",    # Formato con menos dígitos (capturado por la regex preliminar).
        "1234 5678 9012 3456 01/2025 12",    # CVV corto (capturado por la regex preliminar).
        "ABCD 1234 5678 9012 01/2025 123",   # Carácter inválido 'A' al inicio (capturado por la regex, o por el DFA si la regex no lo atrajara).
    ]
    # Itera sobre las cadenas inválidas y muestra su resultado de validación.
    for test_cc in invalid_cc_tests:
        is_valid, error_msg, error_pos = cc_validator.validate(test_cc)
        print(f"Credit Card - '{test_cc}': {'Válida' if is_valid else f'Inválida ({error_msg})'}")


    print("\n--- Pruebas de CURP ---")
    # Conjunto de cadenas de ejemplo para CURP, incluyendo válidas e inválidas para demostrar el comportamiento.
    curp_tests = [
        "GARC980512HDFLRN09", # Válida estructuralmente según el AFD.
        "LOPE950305MGRRRS08", # Válida estructuralmente según el AFD.
        "PERE870920QTSJMS07", # Inválida: 'Q' en el campo de sexo (se espera H o M), detectado por el DFA.
        "GARC980512ZDFLNS09", # Inválida: 'Z' en el campo de sexo, detectado por el DFA.
        "MART991231HSLPPR04", # Válida estructuralmente.
        "GOME850415MNLQWS06", # Válida estructuralmente.
        "GARC980512HDFLRN0",  # Inválida: Longitud incorrecta (validación preliminar de longitud).
        "GARC980512HDFLRN0!", # Inválida: Carácter '!' no está en el alfabeto permitido (detectado por DFA.validate).
        "GARC981312HDFLRN09", # Válida estructuralmente: '13' para el mes es un dígito, el DFA lo acepta.
                              # Una validación semántica adicional fuera del DFA podría marcar esto como inválido (mes > 12).
        "GARC980512HXXLRN09", # Válida estructuralmente: 'X' es una letra válida para la sección de estado, el DFA la acepta.
        "GARC980512HDFLRN09A", # Inválida: Longitud incorrecta (validación preliminar de longitud).
    ]

    # Itera sobre las cadenas de CURP y muestra su resultado de validación.
    for test_curp in curp_tests:
        is_valid, error_msg, error_pos = curp_validator.validate(test_curp)
        print(f"CURP - '{test_curp}': {'Válida' if is_valid else f'Inválida ({error_msg})'}")

    print("\n=== Pruebas con archivos ===")
    # Llama a la función `process_file` para leer y validar cadenas desde archivos de texto.
    # Asegúrate de que los archivos 'credit_cards.txt' y 'curps.txt' estén en el mismo directorio
    # desde donde ejecutas este script.
    process_file('credit_cards.txt', cc_validator, "Credit Card")
    process_file('curps.txt', curp_validator, "CURP")

# Este bloque asegura que la función `run_tests_in_console()` se ejecute solo cuando el script es ejecutado directamente,
# no cuando es importado como un módulo en otro script.
if __name__ == "__main__":
    run_tests_in_console()