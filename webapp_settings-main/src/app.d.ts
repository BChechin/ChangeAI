import type { TelegramWebApps } from 'telegram-webapps-types-new';


// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	interface Window {
    Telegram: TelegramWebApps.SDK;
  }
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface Platform {}
	}
}

export {};
