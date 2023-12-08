/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './ssr_demo/core/templates/**/*.html',
  ],
  safelist: [
    // Injected by Django, and may be referenced by CSS rules
    'errorlist',
  ],
  plugins: [
    require('@tailwindcss/forms'),
    require('daisyui'),
  ],
  daisyui: {
    logs: false,
  },
}
