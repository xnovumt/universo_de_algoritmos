# api.py
from flask import Flask, request, jsonify
from flask_cors import CORS # Importa CORS para manejar solicitudes de origen cruzado
import os
import sys

# Añade el directorio que contiene dfa_validators.py a la ruta de Python
# Esto es crucial para que Flask pueda encontrar tus clases validadoras
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from dfa_validators import CreditCardDFA, CURPDFA # Importa tu lógica existente

app = Flask(__name__)
# Habilita CORS para todas las rutas. Esto es importante para que tu aplicación Vue.js
# (que se ejecuta en un puerto diferente) pueda realizar solicitudes a tu API de Flask.
# En un entorno de producción, es posible que quieras restringir esto a orígenes específicos.
CORS(app)

# Inicializa tus validadores una vez cuando la aplicación se inicie
cc_validator = CreditCardDFA()
curp_validator = CURPDFA()

@app.route('/')
def index():
    """Ruta principal para verificar que la API está funcionando."""
    return "¡La API de Validadores AFD está funcionando!"

@app.route('/validate/credit_card', methods=['POST'])
def validate_credit_card():
    """
    Endpoint para validar una cadena de tarjeta de crédito.
    Recibe una cadena de texto y devuelve el resultado de la validación.
    """
    data = request.get_json() # Obtiene los datos JSON enviados en la solicitud.
    input_string = data.get('input_string', '') # Extrae la cadena de entrada.

    is_valid, error_msg, error_pos = cc_validator.validate(input_string) # Llama a tu validador Python.

    response = { # Prepara la respuesta en formato JSON.
        'input_string': input_string,
        'is_valid': is_valid,
        'error_message': error_msg,
        'error_position': error_pos
    }
    return jsonify(response) # Devuelve la respuesta JSON.

@app.route('/validate/curp', methods=['POST'])
def validate_curp():
    """
    Endpoint para validar una cadena de CURP.
    Recibe una cadena de texto y devuelve el resultado de la validación.
    """
    data = request.get_json()
    input_string = data.get('input_string', '')

    is_valid, error_msg, error_pos = curp_validator.validate(input_string)

    response = {
        'input_string': input_string,
        'is_valid': is_valid,
        'error_message': error_msg,
        'error_position': error_pos
    }
    return jsonify(response)

@app.route('/process_file_curp', methods=['GET'])
def process_file_curp():
    """
    Endpoint para procesar el archivo 'curps.txt' y devolver los resultados de cada línea.
    """
    filename = 'curps.txt' # Nombre del archivo a procesar (debe estar en el mismo directorio).
    results = [] # Lista para almacenar los resultados de cada línea.

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, 1): # Itera sobre cada línea del archivo.
                line = line.strip()
                if line:
                    is_valid, error_msg, error_pos = curp_validator.validate(line)
                    results.append({ # Añade el resultado de la línea a la lista.
                        'line_number': i,
                        'input_string': line,
                        'is_valid': is_valid,
                        'error_message': error_msg,
                        'error_position': error_pos
                    })
    except FileNotFoundError: # Maneja el error si el archivo no se encuentra.
        return jsonify({'error': f"Error: El archivo '{filename}' no se encontró"}), 404
    except Exception as e: # Captura cualquier otro error durante el procesamiento.
        return jsonify({'error': f"Error al procesar el archivo: {str(e)}"}), 500
    
    return jsonify(results) # Devuelve la lista de resultados en JSON.

@app.route('/process_file_credit_card', methods=['GET'])
def process_file_credit_card():
    """
    Endpoint para procesar el archivo 'credit_cards.txt' y devolver los resultados de cada línea.
    """
    filename = 'credit_cards.txt' # Nombre del archivo a procesar.
    results = []

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file, 1):
                line = line.strip()
                if line:
                    is_valid, error_msg, error_pos = cc_validator.validate(line)
                    results.append({
                        'line_number': i,
                        'input_string': line,
                        'is_valid': is_valid,
                        'error_message': error_msg,
                        'error_position': error_pos
                    })
    except FileNotFoundError:
        return jsonify({'error': f"Error: El archivo '{filename}' no se encontró"}), 404
    except Exception as e:
        return jsonify({'error': f"Error al procesar el archivo: {str(e)}"}), 500
    
    return jsonify(results)


if __name__ == '__main__':
    # Asegúrate de que dfa_validators.py esté en el mismo directorio o sea accesible.
    # Para desarrollo, puedes ejecutar esto con `python api.py`
    # Para producción, usa un servidor WSGI como Gunicorn
    app.run(debug=True, port=5000) # Ejecuta en el puerto 5000 en modo depuración