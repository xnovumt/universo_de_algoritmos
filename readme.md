# 🌌 Validador de Patrones con Autómatas Finitos Deterministas (AFD) 🤖

Este proyecto forma parte del emocionante **"Universo de Algoritmos"**, una iniciativa académica que explora la resolución de problemas complejos a través de la aplicación de autómatas y diversas técnicas de programación.

🎯 Específicamente, esta sección se enfoca en el **Módulo 2: “AFDs en la Vida Real: Patrullas Sintácticas para Detectar Cadenas Válidas”**. Aquí, hemos diseñado e implementado Autómatas Finitos Deterministas (AFD) para validar cadenas reales que poseen estructuras sintácticas rigurosas.

---

## 🚀 ¿Qué Valida Actualmente el Proyecto?

Nuestro validador de patrones basado en AFD está diseñado para reconocer dos tipos de estructuras de datos complejas y de uso común:

* 💳 **Números de Tarjeta de Crédito:** Se verifica el formato exacto (incluyendo espacios), la longitud y la estructura específica del número, la fecha de vencimiento y el código de verificación (CVV).
* 🇲🇽 **CURP (Clave Única de Registro de Población) de México:** Un patrón alfanumérico complejo que requiere una validación estricta de su longitud, composición y la secuencia de sus caracteres.

Además de la validación individual, la aplicación ofrece la capacidad de **procesar archivos de texto** (`.txt`) que contienen múltiples entradas. Esto permite validar conjuntos de datos de manera eficiente, mostrando resultados detallados y claros directamente en la interfaz gráfica.

---

## 🔍 Descripción del Problema (Módulo 2: AFDs en la Vida Real)

El corazón de este módulo reside en el diseño y la programación de dos Autómatas Finitos Deterministas (AFD) robustos. Estos AFD tienen la capacidad de validar cadenas con estructuras complejas que, aunque rigurosas en sus reglas sintácticas, pueden ser procesadas sin la necesidad de memoria adicional (es decir, sin el uso de pilas o gramáticas contextuales), lo cual las convierte en candidatas ideales para la validación mediante AFD.

### Requisitos por Cada Tipo de Cadena Elegido:

Para cada patrón de cadena implementado, se ha cumplido con los siguientes requisitos:

* **Definición Formal del AFD:** Se ha establecido formalmente el AFD, incluyendo todos sus componentes:
    * $\Sigma$ (Alfabeto): El conjunto de todos los caracteres de entrada válidos.
    * $Q$ (Conjunto de Estados): Los diferentes estados por los que el autómata puede transitar.
    * $q_0$ (Estado Inicial): El punto de partida de la validación.
    * $F$ (Conjunto de Estados Finales): Los estados que indican una cadena válida al finalizar la lectura.
    * $\delta$ (Función de Transición): Define cómo el autómata se mueve entre estados con cada carácter de entrada.
* **Representación:** La lógica de transiciones del AFD ha sido implementada (o puede ser representada) mediante una matriz de transiciones, reflejando su comportamiento determinista.
* **Programa de Validación:** Un programa que lee un archivo `.txt` (con una cadena por línea) y determina la validez de cada una.
* **Manejo de Errores Detallado:** En caso de que una cadena sea inválida, el sistema proporciona información precisa:
    * El número de línea donde se encuentra la cadena.
    * El carácter exacto donde ocurrió la falla (si es posible).
    * Una descripción clara de la causa del error.

### 🎯 Cadenas Elegidas para Este Proyecto:

#### 1. 💳 Número de Tarjeta de Crédito

* **Formato:** `dddd dddd dddd dddd mm/aaaa cvv`
    * `d`: representa un dígito numérico.
    * `m`: mes de vencimiento.
    * `a`: año de vencimiento.
    * `cvv`: código de verificación (Card Verification Value).
* **Reglas Cruciales:** Validaciones estrictas de los espacios exactos y la longitud total de la cadena.
* **Ejemplo Válido:** `1234 5678 9012 3456 03/2029 336`

#### 2. 🇲🇽 CURP de México (Clave Única de Registro de Población)

* **Formato:** `AAAAmmddHXXCCCNNNN`
    * `AAAA`: 4 letras iniciales (mayúsculas).
    * `mmdd`: 6 dígitos de fecha de nacimiento.
    * `H`: 1 letra para el sexo (H o M).
    * `XX`: 2 letras para el estado de nacimiento.
    * `CCC`: 3 letras internas.
    * `NN`: 2 dígitos alfanuméricos.
    * `N`: 1 dígito verificador.
* **Ejemplo Válido:** `GARC980512HDFLNS09`

---

## ✨ ¿Cómo los AFD Resuelven Este Problema?

Los Autómatas Finitos Deterministas (AFD) son herramientas computacionales sumamente eficaces para reconocer **lenguajes regulares**, es decir, conjuntos de cadenas que obedecen a un patrón estricto y predecible. La naturaleza de formatos como los números de tarjeta de crédito y las CURPs se alinea perfectamente con las capacidades de los AFD:

* **Estado a Estado 🔄:** Un AFD avanza a través de una secuencia de estados, donde cada transición se define por un carácter de entrada. Cada estado representa una porción específica del patrón ya reconocida. Por ejemplo, al validar una tarjeta de crédito, un estado podría significar "hemos leído los primeros 16 dígitos y el primer espacio", el siguiente estado "hemos procesado el mes", y así sucesivamente.
* **Validación de Secuencia y Longitud 📏:** Los AFD permiten establecer transiciones precisas para cada tipo de carácter esperado en una posición determinada. Esto asegura que la secuencia de dígitos, letras, espacios y símbolos (como `/` o `-`) sea correcta. La longitud total de la cadena y la de sus segmentos (ej. 4 dígitos para cada bloque de la tarjeta, 2 para el mes) se controlan implícitamente por la cantidad de transiciones y estados necesarios para alcanzar un estado final.
* **Caracteres Específicos y Rangos 🅰️🔢:** Es posible definir transiciones para rangos de caracteres (ej. '0'-'9' para cualquier dígito, 'A'-'Z' para cualquier letra mayúscula) y para caracteres literales específicos (ej. el espacio, el guion `-`, la barra `/`).
* **Estados de Error 🚫:** Si en algún punto de la cadena de entrada el AFD encuentra un carácter que no corresponde con ninguna transición válida desde su estado actual, se activa un "estado de error" (o simplemente no hay una transición definida). Esto indica que la cadena es inválida y, gracias a la implementación, permite identificar el carácter exacto y la posición donde se rompe el patrón.
* **Eficiencia ⚡:** Dada su naturaleza determinista y la ausencia de recursión o necesidad de estructuras de datos complejas como pilas, la validación mediante AFD es notablemente eficiente en términos de tiempo de ejecución y uso de recursos computacionales.

En este proyecto, se ha implementado un AFD específico y optimizado para cada formato (tarjeta de crédito y CURP), garantizando una validación robusta y una retroalimentación clara para cada entrada.

---

---

## ⚙️ Requisitos

Para poner este proyecto en marcha en tu entorno local, necesitarás tener instalados los siguientes componentes:

* **Node.js** y **npm** (o Yarn) para la ejecución y gestión de dependencias del frontend.
* **Python 3.x** y **pip** para el backend y sus dependencias.

---

## 🚀 Configuración y Ejecución

Sigue estos sencillos pasos para configurar y ejecutar el proyecto:

### 1. Configuración del Backend

1.  Navega al directorio del backend en tu terminal:
    ```bash
    cd backend
    ```
2.  **Crea un entorno virtual** (¡Altamente recomendado para gestionar dependencias!):
    ```bash
    python -m venv venv
    ```
3.  **Activa el entorno virtual**:
    * **En Windows (Command Prompt):**
        ```bash
        venv\Scripts\activate.bat
        ```
    * **En Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    * **En macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  **Instala las dependencias** de Python listadas en `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Inicia el servidor Flask**:
    ```bash
    python api.py
    ```
    🎉 El backend debería estar ahora corriendo y accesible en `http://127.0.0.1:5000`.

### 2. Configuración del Frontend

1.  Abre una **NUEVA terminal** (manteniendo el backend activo) y navega al directorio del frontend:
    ```bash
    cd front
    ```
2.  **Instala las dependencias** de Node.js:
    ```bash
    npm install
    # Si prefieres Yarn, usa:
    # yarn install
    ```
    **Nota Importante:** Confirma que las dependencias clave para el desarrollo (como `@tailwindcss/vite`, `axios`, `vue`, `vite`, `vite-plugin-vue-devtools`) estén correctamente instaladas en tu `package.json`.
3.  **Inicia el servidor de desarrollo de Vue (Vite)**:
    ```bash
    npm run dev
    # Si prefieres Yarn, usa:
    # yarn dev
    ```
    🌐 El frontend se abrirá automáticamente en tu navegador, usualmente en `http://localhost:5173/` (o un puerto similar).

---

## 💻 Uso de la Aplicación

Una vez que ambos servidores (backend de Python y frontend de Vue) estén activos y funcionando:

1.  **Validación Individual ⌨️:**
    * Dirígete a la sección de validación de tarjetas de crédito o CURPs en la interfaz.
    * Introduce la cadena de texto que deseas validar en el campo de entrada.
    * Haz clic en el botón "Validar Tarjeta" o "Validar CURP" para obtener el resultado instantáneo.
2.  **Validación desde Archivos 📁:**
    * **¡Crucial!** Asegúrate de que los archivos de ejemplo (`credit_cards.txt` y `curps.txt`) estén presentes en el **mismo directorio que tu script `api.py`** en el backend.
    * Desde la interfaz del frontend, haz clic en "Procesar 'curps.txt'" o "Procesar 'credit_cards.txt'". El backend leerá y validará cada línea de los archivos, y los resultados se mostrarán detalladamente en el frontend.

---

## 🧪 Ejemplos de Entradas para Pruebas

Usa estas cadenas para verificar el correcto funcionamiento de las validaciones:

### Para Tarjetas de Crédito:

* **✅ Válidas:**
    * `1234 5678 9012 3456 03/2029 336`
    * `4000123456789010 12/2025 000`
* **❌ Inválidas:**
    * `1234 5678 9012 3456 03/2029` (Falta CVV)
    * `1234 5678 9012 3456 13/2029 336` (Mes inválido)

### Para CURPs:

* **✅ Válidas:**
    * `GARC980512HDFLRN09`
    * `ABCD000101HXXXXX00`
* **❌ Inválidas:**
    * `GARC980512HDFLRN0` (CURP corta)
    * `GAR/980512HDFLRN09` (Carácter inválido)

---

## 🤝 Contribuciones

¡Tu interés es bienvenido! Si deseas contribuir a este proyecto, no dudes en:

* Abrir un *issue* para reportar errores o sugerir mejoras.
* Enviar un *pull request* con nuevas características o correcciones.
