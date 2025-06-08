import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [vue(),tailwindcss(), ],
  server: {
    /* proxy: {
      '/api': {
        target: 'http://localhost:4567', // Ajusta el puerto si APIReservas.jar usa otro (por ejemplo, 3000)
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/'), // Mantén el prefijo /api si APIReservas.jar lo usa
      },
    },*/
  }, 
})