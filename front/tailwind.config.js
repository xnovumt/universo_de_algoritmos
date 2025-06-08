// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}", "./src/components/UserTable.vue"],
  theme: {
    // No definas 'colors' directamente aquí para no sobrescribir los colores por defecto.
    // Usa 'extend' para AÑADIR tus colores personalizados.
    extend: {
      colors: {
        'background-blue': 'rgb(var(--color-background-blue) / <alpha-value>)', // Usamos alpha-value para opacidad
        'complementary-orange': 'rgb(var(--color-complementary-orange) / <alpha-value>)',
        'heading-blue': 'rgb(var(--color-heading-blue) / <alpha-value>)',
        'vue-green': 'var(--color-vue-green)', // Hex values usually don't need alpha-value
        'vue-green-dark': 'var(--color-vue-green-dark)',
      },
    },
  },
  plugins: [],
};