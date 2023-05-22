/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		theme: {
			// fontSize: {
			// 	'xs': '.75rem',
			// 	'sm': '.875rem',
			// 	'base': '1rem',
			// 	'lg': '1.125rem',
			// 	'xl': '1.25rem',
			// 	'2xl': '1.5rem',
			// 	'3xl': '1.875rem',
			// 	'4xl': '2.25rem',
			// 	'5xl': '3rem',
			// 	'6xl': '4rem',
			// },
		},
		extend: {
			colors: {
        // Dark mode
				// 'tg-bg': 'var(--tg-theme-bg-color, #282e33)',
				// 'tg-button': 'var(--tg-theme-button-color, #e79c4b)',
				// 'tg-button-text': 'var(--tg-theme-button-text-color, #ffffff)',
				// 'tg-hint': 'var(--tg-theme-hint-color, #82868a)',
				// 'tg-link': 'var(--tg-theme-link-color, #f39a51)',
				// 'tg-secondary-bg': 'var(--tg-theme-secondary-bg-color, #313b43)',
				// 'tg-text': 'var(--tg-theme-text-color, #f5f5f5)'

        // Light mode
        'tg-bg': 'var(--tg-theme-bg-color, #ffffff)',
				'tg-button': 'var(--tg-theme-button-color, #40a7e3)',
				'tg-button-text': 'var(--tg-theme-button-text-color, #ffffff)',
				'tg-hint': 'var(--tg-theme-hint-color, #999999)',
				'tg-link': 'var(--tg-theme-link-color, #168dcd)',
				'tg-secondary-bg': 'var(--tg-theme-secondary-bg-color, #f1f1f1)',
				'tg-text': 'var(--tg-theme-text-color, #000000)'
			},
			screens: {
				tg: '392px'
			},
			fontFamily: {
				tg: ['"Open Sans"']
			},
			dropShadow: {
				block: '0 5px 5px rgba(0, 0, 0, 0.3)',
				'4xl': ['0 35px 35px rgba(0, 0, 0, 0.25)', '0 45px 65px rgba(0, 0, 0, 0.15)']
			}
		}
	},
	plugins: []
};
