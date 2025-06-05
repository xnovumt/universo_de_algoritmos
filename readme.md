Validador de Patrones con Autómatas Finitos Deterministas (AFD)
Este proyecto es parte del "Universo de Algoritmos", una aplicación que explora la resolución de problemas complejos utilizando autómatas y diversas técnicas de programación. Específicamente, esta sección se enfoca en el Módulo 2: “AFDs en la Vida Real: Patrullas Sintácticas para Detectar Cadenas Válidas”, diseñando e implementando Autómatas Finitos Deterministas (AFD) para validar cadenas reales con estructuras sintácticas rigurosas.

Actualmente, el proyecto valida:

Números de Tarjeta de Crédito: Un patrón que requiere verificación de formato, longitud y estructura específica.
CURP (Clave Única de Registro de Población) de México: Un patrón alfanumérico complejo con reglas específicas de longitud y composición.
La aplicación permite la validación individual y el procesamiento de archivos de texto con múltiples entradas para validar conjuntos de datos a la vez, mostrando resultados detallados en una interfaz gráfica.

Descripción del Problema (Módulo 2: AFDs en la Vida Real)
El objetivo de este módulo es diseñar y programar dos Autómatas Finitos Deterministas (AFD) capaces de validar cadenas reales con estructuras complejas. Estas cadenas se caracterizan por tener reglas sintácticas rigurosas pero que pueden ser procesadas sin necesidad de memoria adicional (es decir, sin pilas ni gramáticas contextuales), lo que las hace ideales para la validación mediante AFD.

Para cada tipo de cadena elegido, se requiere:

Definir formalmente el AFD: Incluyendo el alfabeto (Σ), el conjunto de estados (Q), el estado inicial (q 
0
​
 ), el conjunto de estados finales (F), y la función de transición (δ).
Representación: Dibujar el grafo o implementar su matriz de transiciones.
Programa de Validación: Crear un programa que lea un archivo .txt con varias cadenas (una por línea) y determine si cada una es válida o no.
Manejo de Errores: En caso de error, el sistema debe mostrar el número de línea, el carácter donde falla (si es posible), y la causa del error.
Las cadenas elegidas para este proyecto son:

Número de tarjeta de crédito:

Formato: dddd dddd dddd dddd mm/aaaa cvv (dígitos d, mes m, año a, código de verificación cvv).
Reglas: Requiere validar espacios exactos y longitud.
Ejemplo válido: 1234 5678 9012 3456 03/2029 336
CURP de México (Clave Única de Registro de Población):

Formato: AAAAmmddHXXCCCNNNN
AAAA: 4 letras iniciales (mayúsculas)
mmdd: 6 dígitos de fecha de nacimiento
H: 1 letra para sexo (H o M)
XX: 2 letras para estado
CCC: 3 letras internas
NN: 2 dígitos
N: 1 dígito verificador
Ejemplo válido: GARC980512HDFLNS09
¿Cómo los AFD Resuelven Este Problema?
Los Autómatas Finitos Deterministas (AFD) son modelos computacionales ideales para reconocer lenguajes regulares, es decir, conjuntos de cadenas que siguen un patrón estricto y predecible. La naturaleza de las tarjetas de crédito y las CURPs se ajusta perfectamente a esta categoría:

Estado a Estado: Un AFD opera moviéndose de un estado a otro en función de cada carácter de entrada. Cada estado representa una porción del patrón ya reconocida. Por ejemplo, al validar una tarjeta de crédito, un estado podría significar "hemos leído 16 dígitos y un espacio", el siguiente estado "hemos leído el mes", y así sucesivamente.
Validación de Secuencia y Longitud: Los AFD permiten definir transiciones precisas para cada tipo de carácter esperado en una posición específica, asegurando que la secuencia de dígitos, letras, espacios y símbolos (/, -) sea la correcta. La longitud total y la de cada segmento (ej. 4 dígitos para cada bloque de tarjeta, 2 para el mes) se controlan implícitamente por el número de transiciones y estados requeridos para llegar a un estado final.
Caracteres Específicos: Se pueden definir transiciones para rangos de caracteres (ej. '0'-'9' para dígitos, 'A'-'Z' para letras mayúsculas) y para caracteres literales (ej. el espacio, el guion -, la barra /).
Estados de Error: Si en cualquier punto de la cadena de entrada el AFD recibe un carácter inesperado para su estado actual, se mueve a un estado de error (o simplemente no tiene una transición definida), indicando una cadena inválida. Esto permite detectar el carácter exacto y la posición donde el patrón se rompe.
Eficiencia: Dada su naturaleza determinista y la ausencia de recursión o pilas, la validación con AFD es extremadamente eficiente en términos de tiempo y recursos computacionales.
En este proyecto, se ha implementado un AFD específico para el formato de tarjeta de crédito y otro para el de CURP, permitiendo una validación robusta y clara para cada entrada.

Características
Backend con Python (Flask):
Implementación de AFD para la validación de patrones en dfa_validators.py.
Endpoints API RESTful para validación individual y procesamiento de archivos.
Manejo de errores y respuestas estructuradas que indican is_valid, error_message, y error_position.
Frontend con Vue.js 3:
Interfaz de usuario intuitiva para ingresar y validar cadenas.
Visualización clara de los resultados de validación, incluyendo mensajes de error y posiciones.
Funcionalidad para cargar y procesar archivos de texto.
Estilos modernos con Tailwind CSS para una experiencia de usuario agradable.

¡Excelente! Integrar la descripción del proyecto en el README es una idea fantástica para contextualizar la aplicación.

He actualizado el README.md para incluir la descripción del "Proyecto: Universo de Algoritmos" y, específicamente, cómo el Módulo 2 (tu parte de AFD) se alinea con este proyecto.

Validador de Patrones con Autómatas Finitos Deterministas (AFD)
Este proyecto es parte del "Universo de Algoritmos", una aplicación que explora la resolución de problemas complejos utilizando autómatas y diversas técnicas de programación. Específicamente, esta sección se enfoca en el Módulo 2: “AFDs en la Vida Real: Patrullas Sintácticas para Detectar Cadenas Válidas”, diseñando e implementando Autómatas Finitos Deterministas (AFD) para validar cadenas reales con estructuras sintácticas rigurosas.

Actualmente, el proyecto valida:

Números de Tarjeta de Crédito: Un patrón que requiere verificación de formato, longitud y estructura específica.
CURP (Clave Única de Registro de Población) de México: Un patrón alfanumérico complejo con reglas específicas de longitud y composición.
La aplicación permite la validación individual y el procesamiento de archivos de texto con múltiples entradas para validar conjuntos de datos a la vez, mostrando resultados detallados en una interfaz gráfica.

Descripción del Problema (Módulo 2: AFDs en la Vida Real)
El objetivo de este módulo es diseñar y programar dos Autómatas Finitos Deterministas (AFD) capaces de validar cadenas reales con estructuras complejas. Estas cadenas se caracterizan por tener reglas sintácticas rigurosas pero que pueden ser procesadas sin necesidad de memoria adicional (es decir, sin pilas ni gramáticas contextuales), lo que las hace ideales para la validación mediante AFD.

Para cada tipo de cadena elegido, se requiere:

Definir formalmente el AFD: Incluyendo el alfabeto (Σ), el conjunto de estados (Q), el estado inicial (q 
0
​
 ), el conjunto de estados finales (F), y la función de transición (δ).
Representación: Dibujar el grafo o implementar su matriz de transiciones.
Programa de Validación: Crear un programa que lea un archivo .txt con varias cadenas (una por línea) y determine si cada una es válida o no.
Manejo de Errores: En caso de error, el sistema debe mostrar el número de línea, el carácter donde falla (si es posible), y la causa del error.
Las cadenas elegidas para este proyecto son:

Número de tarjeta de crédito:

Formato: dddd dddd dddd dddd mm/aaaa cvv (dígitos d, mes m, año a, código de verificación cvv).
Reglas: Requiere validar espacios exactos y longitud.
Ejemplo válido: 1234 5678 9012 3456 03/2029 336
CURP de México (Clave Única de Registro de Población):

Formato: AAAAmmddHXXCCCNNNN
AAAA: 4 letras iniciales (mayúsculas)
mmdd: 6 dígitos de fecha de nacimiento
H: 1 letra para sexo (H o M)
XX: 2 letras para estado
CCC: 3 letras internas
NN: 2 dígitos
N: 1 dígito verificador
Ejemplo válido: GARC980512HDFLNS09
¿Cómo los AFD Resuelven Este Problema?
Los Autómatas Finitos Deterministas (AFD) son modelos computacionales ideales para reconocer lenguajes regulares, es decir, conjuntos de cadenas que siguen un patrón estricto y predecible. La naturaleza de las tarjetas de crédito y las CURPs se ajusta perfectamente a esta categoría:

Estado a Estado: Un AFD opera moviéndose de un estado a otro en función de cada carácter de entrada. Cada estado representa una porción del patrón ya reconocida. Por ejemplo, al validar una tarjeta de crédito, un estado podría significar "hemos leído 16 dígitos y un espacio", el siguiente estado "hemos leído el mes", y así sucesivamente.
Validación de Secuencia y Longitud: Los AFD permiten definir transiciones precisas para cada tipo de carácter esperado en una posición específica, asegurando que la secuencia de dígitos, letras, espacios y símbolos (/, -) sea la correcta. La longitud total y la de cada segmento (ej. 4 dígitos para cada bloque de tarjeta, 2 para el mes) se controlan implícitamente por el número de transiciones y estados requeridos para llegar a un estado final.
Caracteres Específicos: Se pueden definir transiciones para rangos de caracteres (ej. '0'-'9' para dígitos, 'A'-'Z' para letras mayúsculas) y para caracteres literales (ej. el espacio, el guion -, la barra /).
Estados de Error: Si en cualquier punto de la cadena de entrada el AFD recibe un carácter inesperado para su estado actual, se mueve a un estado de error (o simplemente no tiene una transición definida), indicando una cadena inválida. Esto permite detectar el carácter exacto y la posición donde el patrón se rompe.
Eficiencia: Dada su naturaleza determinista y la ausencia de recursión o pilas, la validación con AFD es extremadamente eficiente en términos de tiempo y recursos computacionales.
En este proyecto, se ha implementado un AFD específico para el formato de tarjeta de crédito y otro para el de CURP, permitiendo una validación robusta y clara para cada entrada.

Características
Backend con Python (Flask):
Implementación de AFD para la validación de patrones en dfa_validators.py.
Endpoints API RESTful para validación individual y procesamiento de archivos.
Manejo de errores y respuestas estructuradas que indican is_valid, error_message, y error_position.
Frontend con Vue.js 3:
Interfaz de usuario intuitiva para ingresar y validar cadenas.
Visualización clara de los resultados de validación, incluyendo mensajes de error y posiciones.
Funcionalidad para cargar y procesar archivos de texto.
Estilos modernos con Tailwind CSS para una experiencia de usuario agradable.

Requisitos
Para ejecutar este proyecto, necesitarás:

Node.js y npm (o Yarn) instalados para el frontend.
Python 3.x y pip instalados para el backend.
Configuración y Ejecución
Sigue estos pasos para poner el proyecto en marcha:

1. Configuración del Backend
Navega al directorio backend:
Bash

cd backend
Crea un entorno virtual (recomendado):
Bash

python -m venv venv
Activa el entorno virtual:
En Windows (Command Prompt): venv\Scripts\activate.bat
En Windows (PowerShell): .\venv\Scripts\Activate.ps1
En macOS/Linux: source venv/bin/activate
Instala las dependencias de Python:
Bash

pip install -r requirements.txt
Inicia el servidor Flask:
Bash

python api.py
El backend debería estar corriendo en http://127.0.0.1:5000.
