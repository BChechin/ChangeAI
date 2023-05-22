<script context="module">
	import { register, waitLocale, init } from 'svelte-i18n';

	register('ru', () => import('$lib/i18n/locales/ru.json'));
	register('en', () => import('$lib/i18n/locales/en.json'));

	const tg_language = Telegram.WebApp.initDataUnsafe.user?.language_code || 'en';

	init({ fallbackLocale: 'en' , initialLocale: tg_language });

	export async function preload() {
		// awaits for 'en' loaders
		return waitLocale();
	}
	locale.set('en');
</script>

<script lang="ts">
	import Range from './Range.svelte';
	import Radio from './Radio.svelte';
	import { onMount } from 'svelte';
	let sampler = 'DDIM';
	let samplers = ['Euler A', 'Euler', 'DDIM'];
	import { myStore } from './store.js';
	import { alterSecondaryBg, alterSecondaryBgFixed } from './style';

	import Lock from '$lib/icons/lock-small-solid.svg?component';

	import { _, locale } from 'svelte-i18n';

	import { page } from '$app/stores';

	// import { init, register, t } from 'svelte-i18n';


	const tg_language = Telegram.WebApp.initDataUnsafe.user?.language_code;

	// locale.set(tg_language);

	// const isPremium = $page.url.searchParams.has('premium');
	let urlParam = $page.url.searchParams.get('premium');

	let isPremium = false;
	if (urlParam === 'true') {
		isPremium = true;
	} else {
		isPremium = false;
	}
	console.log(urlParam);
	console.log(isPremium);

	let radioValue = '-1';

	function calcSeed(radio: string): number {
		if (radio === '-1') {
			return -1;
		} else {
			// Get somehow last generated seed
			return 2345234;
		}
	}
	let seed = 1324552;
	$: seed = calcSeed(radioValue);

	// let settings = {};

	$: settings = {
		text_cfg: $myStore.data['slider1_dragend'] || 1,
		image_cfg: $myStore.data['slider2_dragend'] || 1,
		sampling_steps: $myStore.data['slider3_dragend'] || 1,
		sampler: sampler,
		seed: seed
	};

	// $: console.log(settings);

	let theme = 'default';

	let slider1 = 7;
	let slider1min = 0;
	let slider1max = 40;
	let slider1step = 0.5;
	let slider1TickStep = 5;

	let slider2 = 1.5;
	let slider2min = 0;
	let slider2max = 5;
	let slider2step = 0.1;
	let slider2TickStep = 13;

	let slider3 = 35;
	let slider3min = 20;
	let slider3max = 50;
	let slider3step = 1;
	let slider3TickStep = 2;
	let slider3OptionStep = 10;
	// let slider2 = 0;

	var colorScheme = window.Telegram.WebApp.colorScheme;
	var platform = window.Telegram.WebApp.platform;
	var initData = window.Telegram.WebApp.initDataUnsafe;
	// window.Telegram.WebApp.sendData("hello");

	// << Static color >>

	onMount(async () => {
		// alterSecondaryBg(document);
		alterSecondaryBgFixed(document);

		document.querySelectorAll('svg').forEach((svg) => {
			const { xMin, xMax, yMin, yMax } = [...svg.children].reduce((acc, el) => {
				const { x, y, width, height } = el.getBBox();
				if (!acc.xMin || x < acc.xMin) acc.xMin = x;
				if (!acc.xMax || x + width > acc.xMax) acc.xMax = x + width;
				if (!acc.yMin || y < acc.yMin) acc.yMin = y;
				if (!acc.yMax || y + height > acc.yMax) acc.yMax = y + height;
				return acc;
			}, {});

			const viewbox = `${xMin} ${yMin} ${xMax - xMin} ${yMax - yMin}`;
			svg.setAttribute('viewBox', viewbox);
		});
		// console.log($_('text_cfg'));

		// console.log(Telegram.WebApp.colorScheme); // Dark or light
		// console.log(Telegram.WebApp.viewportHeight)
	});

	Telegram.WebApp.ready();

	let _auth = {
		query_id: 'AAFE17gZAAAAAETXuBl_qh9A',
		user: {
			id: 431544132,
			first_name: 'Vladimir Nazarov',
			last_name: '',
			username: 'barni_official',
			language_code: 'en'
		},
		auth_date: '1675835560',
		hash: '92cc0de5b4aeab9e695aef16efdb80c0e70153e503634def0d4d7254b669d0ee'
	};

	async function doPost(body: object) {
		// const response = await fetch('https://tg-bot.loophole.site/webapp/reply_demo/setSettings', {
		const response = await fetch(import.meta.env.VITE_WEBAPP_SERVER_URL + '/settings/setSettings', {
			method: 'POST',
			mode: 'cors',
			headers: {
				'Access-Control-Allow-Origin': '*',
				Accept: 'application/json',
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ _auth, ...body })
		});
		const j = await response.json();
		console.log(j);
	}

	$: {
		doPost(settings);
	}

	const range = (start: number, stop: number, step: number) => Array.from({ length: (stop - start) / step + 1 }, (_, i) => start + i * step);

	let sliderValue = 0;

	// const element = document.createElement('div');
	// element.className = 'text-telegram-white text-telegram-black text-telegram-hint text-telegram-link text-telegram-primary  text-telegram-primary-text text-telegram-secondary-white';
	// document.body.appendChild(element);
	function unlockPremium() {
		// alert('no more alerts');
		console.log('unlock premium');
		console.log($_('popup.title'));
		// Telegram.WebApp.showAlert(message=)
		Telegram.WebApp.showPopup(
			{
				title: $_('popup.title'),
				message: $_('popup.message'),
				buttons: [
					{ id: 'cancel', type: 'close' },
					{ id: 'buy', type: 'ok', text: 'Buy' }
				]
			},
			function (buttonId) {
				if (buttonId === 'cancel') {
					// DemoApp.showAlert("'Delete all' selected");
					// console.log('delete')
				} else if (buttonId === 'buy') {
					// Telegram.WebApp.openLink('https://telegram.org/faq');
					let url = 'https://tg-landing.loophole.site';
					// Telegram.WebApp.BackButton.show();
					window.location.replace(url);

					// Telegram.WebApp.BackButton.onClick(() => {
					// 	console.log('hi');
					// 	window.history.back();
					// });
				}
			}
		);
	}
</script>

<div class="scrollbar-hide no-scrollbar">
	<!-- <div class="w-full scrollbar-hide no-scrollbar"> -->
	<div class="bg-tg-bg h-screen break-all">
		<!-- <div class="bg-gray-500 text-white h-full break-all"> -->
		<!-- <select bind:value="{user_language}" class="px-2 py-1 bg-inherit rounded-md border-solid border-0 focus:ring-1 focus:ring-tg-button ring-1 ring-tg-hint">
			{#each languages as language}
				<option value="{language}" class="bg-slate-500">{language}</option>
			{/each}
		</select> -->
		<div class="px-2 pt-0  flex flex-col space-y-4">
			<!-- text cfg -->
			<div class="drop-shadow-block px-4 py-2 bg-tg-secondary-bg rounded-md" style="">
				<!-- labes -->
				<div class="flex justify-between">
					<div class="select-none">{$_('text_cfg')}</div>
					<input type="number" bind:value="{slider1}" min="{slider1min}" max="{slider1max} " class="bg-inherit p-0 text-center rounded-md caret-tg-button  border-solid border-0 w-16 focus:ring-1 focus:ring-tg-button ring-1 ring-tg-hint" />
				</div>
				<!-- slider -->
				<div class:purple-theme="{theme === 'purple'}" class="mt-2">
					<Range storeVariableName="slider1_dragend" on:change="{(e) => (slider1 = e.detail.value)}" bind:value="{slider1}" id="basic-slider" min="{slider1min}" max="{slider1max}" step="{slider1step}" />
				</div>
				<!-- ticks -->
				<!-- <div class="mx-[3px] -mt-[14px] flex justify-between">
					{#each range(slider1min, slider1max, 1) as option}
						<div class="text-center select-none z-[10]">
							<div class="border-x border-tg-secondary-bg h-[6px] "></div>
						</div>
					{/each}
				</div> -->
				<!-- <div class="mx-[3px] -mt-[12px] flex justify-between">
					{#each range(slider1min, slider1max, 1) as option}
						<div class="text-center select-none z-[1000]">
							<div class="border-r border-tg-button-text opacity-50 h-[2px]"></div>
						</div>
					{/each}
				</div> -->
				<div class="mx-[3px] -mt-1 flex justify-between">
					{#each range(slider1min, slider1max, 2.5) as option}
						<div class="text-center select-none">
							<div class="border-r border-tg-text opacity-80 w-[1px] h-2"></div>
						</div>
					{/each}
				</div>
				<div class="-mx-3 flex justify-between">
					{#each range(slider1min, slider1max, slider1TickStep) as option}
						<option value="{option}" class="w-8 text-center select-none">{option}</option>
					{/each}
				</div>
			</div>

			<!-- img cfg -->
			<div class="drop-shadow-block  px-4 py-2 bg-tg-secondary-bg rounded-md">
				<!-- labes -->
				<div class="flex justify-between">
					<div class="select-none">{$_('image_cfg')}</div>
					<input type="number" bind:value="{slider2}" min="{slider2min}" max="{slider2max}" class="bg-inherit p-0 text-center rounded-md caret-tg-button  border-solid border-0 w-16 focus:ring-1 focus:ring-tg-button ring-1 ring-tg-hint" />
				</div>
				<!-- slider -->
				<div class:purple-theme="{theme === 'purple'}" class="mt-2">
					<Range storeVariableName="slider2_dragend" on:change="{(e) => (slider2 = e.detail.value)}" bind:value="{slider2}" id="basic-slider" min="{slider2min}" max="{slider2max}" step="{slider2step}" />
				</div>
				<!-- ticks -->
				<div class="mx-[3px] -mt-1 flex justify-between">
					{#each range(slider2min, slider2max, 0.2) as option}
						<div class="text-center select-none">
							<div class="border-r border-tg-text opacity-80 w-[1px] h-2"></div>
						</div>
					{/each}
				</div>
				<!-- numbers -->
				<div class="-mx-3 -mt-1 flex justify-between">
					{#each range(slider2min, slider2max, 1) as option}
						<option value="{option}" class="w-8 text-center select-none">{option}</option>
					{/each}
				</div>
			</div>

			<!-- Sampling -->
			<div class="drop-shadow-block  flex justify-between px-4 py-2 bg-tg-secondary-bg rounded-md">
				<!-- Sampling method -->
				<div>
					<div class="flex content-center h-6">
						<span class="inline-block align-middle">{$_('sampler')}</span>
						<div class="ml-1 mb-1"><Lock class="fill-tg-button-text w-3 h-full opacity-80" /></div>
					</div>
					<div class="mt-2">
						<select bind:value="{sampler}" class="px-2 py-1 bg-inherit rounded-md border-solid border-0 focus:ring-1 focus:ring-tg-button ring-1 ring-tg-hint">
							{#each samplers as item}
								<option value="{item}" class="bg-slate-500">{item}</option>
							{/each}
						</select>
					</div>
				</div>

				<!-- Sampling steps -->
				<div class="w-full ml-4">
					<!-- labes -->
					<div class="flex justify-between content-center">
						<div class="select-none flex">
							{$_('sampling_steps')}
							<div class="ml-1 mb-1"><Lock class="fill-tg-button-text w-3 h-full opacity-80" /></div>
						</div>

						<!-- <Icon class="text-tg-button-text" data={lock_dollar} size="40px" stroke=currentColor fill=currentColor /> -->
						<!-- you can pass class (or anything else) using $$restProps -->
						<input type="number" bind:value="{slider3}" min="{slider3min}" max="{slider3max}" class="bg-inherit p-0 text-center rounded-md caret-tg-button  border-solid border-0 w-16 focus:ring-1 focus:ring-tg-button ring-1 ring-tg-hint" />
					</div>
					<!-- slider -->
					<div class:purple-theme="{theme === 'purple'}" class="mt-2">
						<Range storeVariableName="slider3_dragend" on:change="{(e) => (slider3 = e.detail.value)}" bind:value="{slider3}" id="basic-slider" min="{slider3min}" max="{slider3max}" step="{slider3step}" />
					</div>
					<!-- ticks -->
					<div class="mx-[3px] -mt-[6px] flex justify-between">
						{#each range(slider3min, slider3max, slider3TickStep) as option}
							<div class="text-center select-none">
								<div class="w-[1px] h-2 bg-gray-300 m-auto"></div>
							</div>
						{/each}
					</div>
					<div class="-mx-3 -mt-1 flex justify-between">
						{#each range(slider3min, slider3max, slider3OptionStep) as option}
							<option value="{option}" class="w-8 text-center select-none">{option}</option>
						{/each}
					</div>
				</div>
				<!-- Premium lock -->
				<div on:click="{unlockPremium}" class="absolute inset-0 bg-tg-bg opacity-50 z-[1000] cursor-pointer rounded-md"></div>
			</div>

			<!-- SEED -->
			<div class="drop-shadow-block  flex justify-between px-2 bg-tg-secondary-bg rounded-md px-4 py-2">
				<!-- Seed options -->
				<Radio fontSize="{16}" bind:userSelected="{radioValue}" />
				<!-- Seed value -->
				<div>
					<div class="flex content-center justify-end"><span class="inline-block align-middle">{$_('image_cfg')}</span></div>

					<input type="number" bind:value="{seed}" class="bg-inherit p-0 text-center rounded-md caret-tg-button  border-solid border-0 w-28 focus:ring-1 focus:ring-tg-button ring-1 ring-tg-hint" />
				</div>
			</div>

			<!-- <div>Greetings, {initData.user?.first_name}!</div>
			<div>initData: {JSON.stringify(initData)}!</div>
			<div>color scheme: {colorScheme}</div>
			<div>userAgent: {navigator.userAgent}</div>
			<div>platform: {platform}</div> -->
		</div>
	</div>
</div>

<style>
	.purple-theme {
		--track-focus: #c368ff;
		--track-highlight-bgcolor: #c368ff;
		--track-highlight-bg: linear-gradient(90deg, #c368ff, #c965ff);
		--thumb-holding-outline: rgba(191, 102, 251, 0.3);
		--tooltip-bgcolor: #c368ff;
		--tooltip-bg: linear-gradient(45deg, #c368ff, #c965ff);
		--track-bgcolor: red;
	}

	/* Hide scrollbar for Chrome, Safari and Opera */
	.no-scrollbar::-webkit-scrollbar {
		display: none;
	}

	/* Hide scrollbar for IE, Edge and Firefox */
	.no-scrollbar {
		-ms-overflow-style: none; /* IE and Edge */
		scrollbar-width: none; /* Firefox */
	}
</style>
