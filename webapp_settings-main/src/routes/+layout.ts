// +layout.ts
// import { browser } from '$app/environment';
import '$lib/i18n'; // Import to initialize. Important :)
import { locale, waitLocale } from 'svelte-i18n';
import type { LayoutLoad } from './$types';

// import { init, register } from 'svelte-i18n';
// import { _, locale } from 'svelte-i18n';

// register('ru', () => import('$lib/i18n/locales/ru.json'));
// register('en', () => import('$lib/i18n/locales/en.json'));

// const tg_language = Telegram.WebApp.initDataUnsafe.user?.language_code;
// console.log(tg_language);

// init({
// 	fallbackLocale: 'en',
// 	initialLocale: tg_language || 'en'
// });

// locale.set(tg_language || 'en');
// const tg_language = Telegram.WebApp.initDataUnsafe.user?.language_code;

// export const load: LayoutLoad = async () => {
// 	locale.set('en');
// 	locale.set('ru')
// };
// await waitLocale();
// locale.set('en');

export const ssr = false;
export const csr = true;

export const prerender = true;
