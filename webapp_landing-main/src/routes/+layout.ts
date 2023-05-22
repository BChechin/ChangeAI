// +layout.ts
// import { browser } from '$app/environment';
// import '$lib/i18n'; // Import to initialize. Important :)
// import { init, locale, waitLocale, register } from 'svelte-i18n';
// import type { LayoutLoad } from './$types';

// register('ru', () => import('$lib/i18n/locales/ru.json'));
// register('en', () => import('$lib/i18n/locales/en.json'));

// const defaultLocale = 'en';

// init({
// 	fallbackLocale: defaultLocale,
// 	// initialLocale: Telegram.WebApp.initDataUnsafe.user?.language_code || 'en',
// 	initialLocale: 'en'
// });

// export const load: LayoutLoad = async () => {
// 	if (browser) {
// 		locale.set('en');
// 		console.log('+layout.ts');
// 	}
// 	await waitLocale();
// };
export const ssr = false;
export const csr = true;

export const prerender = true;
