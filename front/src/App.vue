<template>
  <div id="app" class="min-h-screen p-8 bg-background-blue flex items-center justify-center">
    <div class="max-w-4xl w-full mx-auto p-8 rounded-lg shadow-2xl bg-complementary-orange text-gray-800">
      <h1 class="text-4xl font-extrabold mb-8 text-heading-blue text-center tracking-wide">Validadores de Patrones con AFD</h1>

      <div class="mb-10 p-6 border border-gray-200 rounded-xl bg-white shadow-lg text-center">
        <h2 class="text-3xl font-bold mb-5 text-heading-blue border-b pb-3 border-gray-200">Validación de Tarjeta de Crédito</h2>
        <div class="flex flex-col md:flex-row items-center justify-center gap-4">
          <input
            v-model="creditCardInput"
            placeholder="Ej: 1234 5678 9012 3456 03/2029 336"
            class="flex-grow w-full md:w-3/4 p-3 border border-gray-300 rounded-md text-lg shadow-sm
                   focus:outline-none focus:ring-4 focus:ring-blue-300 focus:border-blue-500 transition duration-200 ease-in-out"
          />
          <button @click="validateCreditCard"
                  class="bg-vue-green hover:bg-vue-green-dark text-white font-bold py-3 px-6 rounded-lg text-lg
                         transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105
                         shadow-lg hover:shadow-xl w-full md:w-auto focus:outline-none focus:ring-4 focus:ring-vue-green-dark">
            Validar Tarjeta
          </button>
        </div>
        <div v-if="creditCardResult"
             :class="['mt-6 p-5 rounded-lg text-left transition-all duration-300 ease-in-out',
                      { 'bg-green-100 border border-green-500 text-green-800 shadow-md': creditCardResult.is_valid,
                        'bg-red-100 border border-red-500 text-red-800 shadow-md': !creditCardResult.is_valid }]">
          <p class="mb-2 text-lg"><strong>Cadena:</strong> <span class="break-all">{{ creditCardResult.input_string }}</span></p>
          <p class="mb-2 text-lg"><strong>Resultado:</strong> <span :class="{ 'font-semibold text-green-700': creditCardResult.is_valid, 'font-semibold text-red-700': !creditCardResult.is_valid }">{{ creditCardResult.is_valid ? 'Válida' : 'Inválida' }}</span></p>
          <p v-if="!creditCardResult.is_valid" class="font-bold text-red-700 text-lg">
            <strong>Error:</strong> {{ creditCardResult.error_message }}
            <span v-if="creditCardResult.error_position !== -1">(Posición: {{ creditCardResult.error_position }})</span>
          </p>
        </div>
      </div>

      <div class="mb-10 p-6 border border-gray-200 rounded-xl bg-white shadow-lg text-center">
        <h2 class="text-3xl font-bold mb-5 text-heading-blue border-b pb-3 border-gray-200">Validación de CURP</h2>
        <div class="flex flex-col md:flex-row items-center justify-center gap-4">
          <input
            v-model="curpInput"
            placeholder="Ej: GARC980512HDFLRN09"
            class="flex-grow w-full md:w-3/4 p-3 border border-gray-300 rounded-md text-lg shadow-sm
                   focus:outline-none focus:ring-4 focus:ring-blue-300 focus:border-blue-500 transition duration-200 ease-in-out"
          />
          <button @click="validateCurp"
                  class="bg-vue-green hover:bg-vue-green-dark text-white font-bold py-3 px-6 rounded-lg text-lg
                         transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105
                         shadow-lg hover:shadow-xl w-full md:w-auto focus:outline-none focus:ring-4 focus:ring-vue-green-dark">
            Validar CURP
          </button>
        </div>
        <div v-if="curpResult"
             :class="['mt-6 p-5 rounded-lg text-left transition-all duration-300 ease-in-out',
                      { 'bg-green-100 border border-green-500 text-green-800 shadow-md': curpResult.is_valid,
                        'bg-red-100 border border-red-500 text-red-800 shadow-md': !curpResult.is_valid }]">
          <p class="mb-2 text-lg"><strong>Cadena:</strong> <span class="break-all">{{ curpResult.input_string }}</span></p>
          <p class="mb-2 text-lg"><strong>Resultado:</strong> <span :class="{ 'font-semibold text-green-700': curpResult.is_valid, 'font-semibold text-red-700': !curpResult.is_valid }">{{ curpResult.is_valid ? 'Válida' : 'Inválida' }}</span></p>
          <p v-if="!curpResult.is_valid" class="font-bold text-red-700 text-lg">
            <strong>Error:</strong> {{ curpResult.error_message }}
            <span v-if="curpResult.error_position !== -1">(Posición: {{ curpResult.error_position }})</span>
          </p>
        </div>
      </div>

      <div class="file-processing-section p-6 border border-gray-200 rounded-xl bg-white shadow-lg text-center">
        <h2 class="text-3xl font-bold mb-5 text-heading-blue border-b pb-3 border-gray-200">Validación desde Archivos</h2>
        <p class="mb-6 text-gray-700 text-lg">Asegúrate de que 'credit_cards.txt' y 'curps.txt' estén en el mismo directorio que tu `api.py`.</p>

        <div class="flex flex-col md:flex-row justify-center gap-4 mb-6">
          <button @click="processCurpFile"
                  class="bg-vue-green hover:bg-vue-green-dark text-white font-bold py-3 px-6 rounded-lg text-lg
                         transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105
                         shadow-lg hover:shadow-xl w-full md:w-auto focus:outline-none focus:ring-4 focus:ring-vue-green-dark">
            Procesar 'curps.txt'
          </button>
          <button @click="processCreditCardFile"
                  class="bg-vue-green hover:bg-vue-green-dark text-white font-bold py-3 px-6 rounded-lg text-lg
                         transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105
                         shadow-lg hover:shadow-xl w-full md:w-auto focus:outline-none focus:ring-4 focus:ring-vue-green-dark">
            Procesar 'credit_cards.txt'
          </button>
        </div>

        <div v-if="curpFileResults.length > 0"
             class="mt-8 p-5 border border-gray-300 rounded-lg bg-gray-50 text-left max-h-96 overflow-y-auto shadow-inner">
          <h3 class="text-2xl font-semibold mb-4 text-gray-800 border-b pb-2 border-gray-200">Resultados de 'curps.txt':</h3>
          <ul class="list-none p-0 space-y-2">
            <li v-for="res in curpFileResults" :key="res.line_number"
                :class="['py-2 px-3 rounded-md transition-colors duration-200 ease-in-out text-lg',
                         { 'bg-green-100 text-green-800 border border-green-400': res.is_valid,
                           'bg-red-100 text-red-800 border border-red-400 font-medium': !res.is_valid }]">
              Línea {{ res.line_number }}: '<span class="break-all">{{ res.input_string }}</span>' es
              <span :class="{ 'font-bold': res.is_valid, 'font-extrabold': !res.is_valid }">
                {{ res.is_valid ? 'válida' : 'inválida' }}
              </span>
              <span v-if="!res.is_valid" class="block mt-1 text-sm text-red-600">
                Error: {{ res.error_message }} <span v-if="res.error_position !== -1">(en pos. {{ res.error_position }})</span>
              </span>
            </li>
          </ul>
        </div>
        <p v-if="curpFileError" class="text-red-600 font-bold mt-5 text-lg">{{ curpFileError }}</p>

        <div v-if="creditCardFileResults.length > 0"
             class="mt-8 p-5 border border-gray-300 rounded-lg bg-gray-50 text-left max-h-96 overflow-y-auto shadow-inner">
          <h3 class="text-2xl font-semibold mb-4 text-gray-800 border-b pb-2 border-gray-200">Resultados de 'credit_cards.txt':</h3>
          <ul class="list-none p-0 space-y-2">
            <li v-for="res in creditCardFileResults" :key="res.line_number"
                :class="['py-2 px-3 rounded-md transition-colors duration-200 ease-in-out text-lg',
                         { 'bg-green-100 text-green-800 border border-green-400': res.is_valid,
                           'bg-red-100 text-red-800 border border-red-400 font-medium': !res.is_valid }]">
              Línea {{ res.line_number }}: '<span class="break-all">{{ res.input_string }}</span>' es
              <span :class="{ 'font-bold': res.is_valid, 'font-extrabold': !res.is_valid }">
                {{ res.is_valid ? 'válida' : 'inválida' }}
              </span>
              <span v-if="!res.is_valid" class="block mt-1 text-sm text-red-600">
                Error: {{ res.error_message }} <span v-if="res.error_position !== -1">en pos. {{ res.error_position }}</span>
              </span>
            </li>
          </ul>
        </div>
        <p v-if="creditCardFileError" class="text-red-600 font-bold mt-5 text-lg">{{ creditCardFileError }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      creditCardInput: '',
      creditCardResult: null,
      curpInput: '',
      curpResult: null,
      curpFileResults: [],
      creditCardFileResults: [],
      curpFileError: null,
      creditCardFileError: null,
      API_BASE_URL: 'http://127.0.0.1:5000',
    };
  },
  methods: {
    async validateCreditCard() {
      try {
        const response = await axios.post(`${this.API_BASE_URL}/validate/credit_card`, {
          input_string: this.creditCardInput,
        });
        this.creditCardResult = response.data;
      } catch (error) {
        console.error('Error al validar la tarjeta de crédito:', error);
        this.creditCardResult = {
          input_string: this.creditCardInput,
          is_valid: false,
          error_message: 'Error de conexión con el servidor o error inesperado.',
          error_position: -1,
        };
      }
    },
    async validateCurp() {
      try {
        const response = await axios.post(`${this.API_BASE_URL}/validate/curp`, {
          input_string: this.curpInput,
        });
        this.curpResult = response.data;
      } catch (error) {
        console.error('Error al validar la CURP:', error);
        this.curpResult = {
          input_string: this.curpInput,
          is_valid: false,
          error_message: 'Error de conexión con el servidor o error inesperado.',
          error_position: -1,
        };
      }
    },
    async processCurpFile() {
      this.curpFileResults = [];
      this.curpFileError = null;
      try {
        const response = await axios.get(`${this.API_BASE_URL}/process_file_curp`);
        this.curpFileResults = response.data;
      } catch (error) {
        console.error('Error al procesar el archivo CURP:', error);
        if (error.response && error.response.data && error.response.data.error) {
          this.curpFileError = error.response.data.error;
        } else {
          this.curpFileError = 'Error de conexión con el servidor o error inesperado al procesar archivo CURP.';
        }
      }
    },
    async processCreditCardFile() {
      this.creditCardFileResults = [];
      this.creditCardFileError = null;
      try {
        const response = await axios.get(`${this.API_BASE_URL}/process_file_credit_card`);
        this.creditCardFileResults = response.data;
      } catch (error) {
        console.error('Error al procesar el archivo de Tarjeta de Crédito:', error);
        if (error.response && error.response.data && error.response.data.error) {
          this.creditCardFileError = error.response.data.error;
        } else {
          this.creditCardFileError = 'Error de conexión con el servidor o error inesperado al procesar archivo de tarjeta de crédito.';
        }
      }
    }
  },
};
</script>

<style>
/* No es necesario un bloque <style> aquí en App.vue si Tailwind cubre todos los estilos.
   Los estilos globales y las directivas @tailwind van en src/assets/main.css
*/
</style>