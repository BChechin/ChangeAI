/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js,svelte,ts}",
    // Keep existing values and append the following:
    "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
  ],
  theme: {
    extend: {
      colors: {
        "tg-bg": "var(--tg-theme-bg-color, #282e33)",
        "tg-button": "var(--tg-theme-button-color, #e79c4b)",
        "tg-button-text": "var(--tg-theme-button-text-color, #ffffff)",
        "tg-hint": "var(--tg-theme-hint-color, #82868a)",
        "tg-link": "var(--tg-theme-link-color, #f39a51)",
        "tg-secondary-bg": "var(--tg-theme-secondary-bg-color, #313b43)",
        "tg-text": "var(--tg-theme-text-color, #f5f5f5)",
      },
      screens: {
        tg: "392px",
      },
      fontFamily: {
        'tg': ['"Open Sans"'],
      },
      dropShadow: {
        'block': '0 5px 5px rgba(0, 0, 0, 0.3)',
        '4xl': [
            '0 35px 35px rgba(0, 0, 0, 0.25)',
            '0 45px 65px rgba(0, 0, 0, 0.15)'
        ]
      }
    },
  },
  plugins: [
    // Keep any existing plugins present and append the following:
    require("flowbite/plugin"),
    require('tailwind-scrollbar-hide')
  ],
  // darkMode: "class",
};
