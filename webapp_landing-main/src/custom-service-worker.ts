import { build, files, version } from '$service-worker';
declare const self: ServiceWorkerGlobalScope;

const ASSETS = 'assets' + version;

// `build` is an array of all the files generated by the bundler, `files` is an
// array of everything in the `static` directory (except exlucdes defined in
// svelte.config.js)
const cached = build.concat(files);

// if you use typescript:
// (self as unknown as ServiceWorkerGlobalScope).addEventListener(
self.addEventListener('install', (event) => {
	event.waitUntil(
		caches
			.open(ASSETS)
			.then((cache) => cache.addAll(cached))
			.then(() => {
				// if you use typescript:
				// (self as unknown as ServiceWorkerGlobalScope).skipWaiting();
				self.skipWaiting();
			})
	);
});

// if you use typescript:
// (self as unknown as ServiceWorkerGlobalScope).addEventListener(
self.addEventListener('activate', (event) => {
	event.waitUntil(
		caches.keys().then(async (keys) => {
			// delete old caches
			keys.map(async (key) => {
				if (key !== ASSETS) {
					await caches.delete(key);
				}
			});

			// if you use typescript:
			// (self as unknown as ServiceWorkerGlobalScope).clients.claim();
			self.clients.claim();
		})
	);
});

/**
 * Fetch the asset from the network and store it in the cache.
 * Fall back to the cache if the user is offline.
 */
// if you use typescript:
// async function fetchAndCache(request: Request) {
async function fetchAndCache(request: RequestInfo | URL) {
	// if (request == 'https://widget.cloudpayments.ru/bundles/cloudpayments/') return new Response();
	const cache = await caches.open(`offline${version}`);

	try {
		const response = await fetch(request);
		if (response.status === 200) {
			cache.put(request, response.clone());
		}

		return response;
	} catch (err) {
		const response = await cache.match(request);
		if (response) {
			return response;
		}

		throw err;
	}
}

// if you use typescript:
// (self as unknown as ServiceWorkerGlobalScope).addEventListener(
self.addEventListener('fetch', (event) => {
	if (event.request.method !== 'GET' || event.request.headers.has('range')) {
		return;
	}
  console.log(event.request.url)
  if (event.request.url == 'https://widget.cloudpayments.ru/bundles/cloudpayments') {
		console.log('niga')
	};


	const url = new URL(event.request.url);

	if (
		// don't try to handle e.g. data: URIs
		!url.protocol.startsWith('http') ||
		// ignore dev server requests
		(url.hostname === self.location.hostname && url.port !== self.location.port) ||
		// ignore /_app/version.json
		url.pathname === '/_app/version.json'
	) {
		return;
	}

	// always serve static files and bundler-generated assets from cache
	const isStaticAsset = url.host === self.location.host && cached.indexOf(url.pathname) > -1;

	if (event.request.cache === 'only-if-cached' && !isStaticAsset) {
		return;
	}

	// for everything else, try the network first, falling back to cache if the
	// user is offline. (If the pages never change, you might prefer a cache-first
	// approach to a network-first one.)
	event.respondWith(
		(async () => {
			// always serve static files and bundler-generated assets from cache.
			// if your application has other URLs with data that will never change,
			// set this variable to true for them and they will only be fetched once.
			const cachedAsset = isStaticAsset && (await caches.match(event.request));

			return cachedAsset || fetchAndCache(event.request);
		})()
	);
});