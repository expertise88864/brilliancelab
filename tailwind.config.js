/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './404.html',
    './search.html',
    './blog/**/*.html',
    './amp/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        ivory: { 50: '#fffdf7', 100: '#faf8f3', 200: '#f3ede0' },
        ink:   { 950: '#0e0f1a', 900: '#1a1d2e', 800: '#2c2f40', 700: '#4a4d5e', 500: '#7e8194', 400: '#a4a6b6', 300: '#c5c6d2' },
        gold:  { 50: '#fbf3df', 100: '#f5e9d0', 200: '#ecd9a9', 300: '#d4b87a', 400: '#c9a45c', 500: '#b89146', 600: '#8a6e30', 700: '#5e4a1f' },
      },
      fontFamily: {
        display: ['"Noto Serif TC"', '"Microsoft JhengHei"', '"PingFang TC"', 'Georgia', 'serif'],
        sans:    ['Inter', '"Microsoft JhengHei"', '"PingFang TC"', '"Noto Sans TC"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
