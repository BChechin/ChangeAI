import { sveltekit } from '@sveltejs/kit/vite';
import svg from '@poppanator/sveltekit-svg';
import type { UserConfig } from 'vite';

// import { VitePWA } from 'vite-plugin-pwa';

const config: UserConfig = {
	plugins: [
		sveltekit(),
		svg({
			includePaths: ['./src/lib/icons/', './src/assets/icons/', './src/lib/icons/*/'],
			svgoOptions: {
				multipass: true,
				plugins: [
					{
						name: 'preset-default',
						// by default svgo removes the viewBox which prevents svg icons from scaling
						// not a good idea! https://github.com/svg/svgo/pull/1461
						params: { overrides: { removeViewBox: false } }
					},
					{ name: 'removeAttrs', params: { attrs: '(fill|stroke)' } }
				]
			}
		}),
		// VitePWA({
		// 	injectRegister: null,
		// 	registerType: 'autoUpdate',
		// 	devOptions: {
		// 		enabled: true
		// 	}
		// })
	],
	server: {
		host: '127.0.0.1',
		port: 5175
	}
};

export default config;
