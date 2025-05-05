/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./binder/templates/**/*.html',],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}

