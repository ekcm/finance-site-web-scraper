/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        "background-black-1": "#383838",
        "background-black-2": "#1E1E1E",
        "grey-1": "#858585",
        "yellow-1": "#F6D06C",
        "yellow-2": "#DFA638",
        "blue-1": "#12A8FD",
        "blue-2": "#0B74B0"
      },
    },
  },
  plugins: [],
}
