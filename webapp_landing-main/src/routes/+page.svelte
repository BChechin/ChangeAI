<script lang="ts">
	let free_options = ['1', '2'];
	let pro_options = ['1', '2', '3', '4'];
	import Check from '$lib/icons/check.svg';
	import Close from '$lib/icons/close.svg';
	import Lock from '$lib/icons/lock.svg';
	import Arrow from '$lib/icons/arrow.svg';
	import { onMount } from 'svelte';
	import { init, waitLocale, register } from 'svelte-i18n';
	import { _, locale } from 'svelte-i18n';
	import { stringify } from 'postcss';

	register('ru', () => import('$lib/i18n/locales/ru.json'));
	register('en', () => import('$lib/i18n/locales/en.json'));

	const tg_language = Telegram.WebApp.initDataUnsafe.user?.language_code;
	console.log(tg_language);


	const SHOP_ID = import.meta.env.VITE_SHOP_ID
	console.log(SHOP_ID)
	console.log(import.meta.env)
	

	init({
		fallbackLocale: 'en',
		initialLocale: tg_language || 'en'
	});

	locale.set(tg_language || 'en');

	const Skins = {
		light: 'classic',
		dark: 'modern'
	};

	function loadScript(src: string) {
		let script = document.createElement('script');
		script.src = src;
		script.async = true;
		// script.defer = true;
		document.body.append(script);
	}

	// console.log({$_('buy_now')})

	// console.log()
	// import './cloudpayments.js';
	let handleClick: svelte.JSX.MouseEventHandler<HTMLDivElement> | null | undefined = undefined;
	// let serviceWorkerHandler = undefined;
	onMount(async () => {

		const colorScheme = Telegram.WebApp.colorScheme;

		const user_id = Telegram.WebApp.initDataUnsafe.user?.id;

		loadScript('https://widget.cloudpayments.ru/bundles/cloudpayments');

		const pay = function () {
			console.log(Telegram.WebApp.colorScheme);
			var widget = new cp.CloudPayments({language: $_('cloudpayments.language_code')});
			var receipt = {
				Items: [
					//товарные позиции
					{
						label: $_('cloudpayments.description'), //наименование товара
						price: parseInt($_('cloudpayments.price')), //цена
						quantity: 1.0, //количество
						amount: parseInt($_('cloudpayments.price')), //сумма
						vat: 0, //ставка НДС
						method: 0, // тег-1214 признак способа расчета - признак способа расчета
						object: 0 // тег-1212 признак предмета расчета - признак предмета товара, работы, услуги, платежа, выплаты, иного предмета расчета
					}
				],
				taxationSystem: 0, //система налогообложения; необязательный, если у вас одна система налогообложения
				email: '', //e-mail покупателя, если нужно отправить письмо с чеком
				phone: '', //телефон покупателя в любом формате, если нужно отправить сообщение со ссылкой на чек
				isBso: false, //чек является бланком строгой отчетности
				amounts: {
					electronic: $_('cloudpayments.price'), // Сумма оплаты электронными деньгами
					advancePayment: 0.0, // Сумма из предоплаты (зачетом аванса) (2 знака после запятой)
					credit: 0.0, // Сумма постоплатой(в кредит) (2 знака после запятой)
					provision: 0.0 // Сумма оплаты встречным предоставлением (сертификаты, др. мат.ценности) (2 знака после запятой)
				}
			};

			var data = {};
			data.CloudPayments = {
				CustomerReceipt: receipt, //чек для первого платежа
				recurrent: {
					interval: 'Month',
					period: 1,
					customerReceipt: receipt //чек для регулярных платежей
				}
			}; //создание ежемесячной подписки

			widget.charge(
				{
					// options
					publicId: SHOP_ID, //id из личного кабинета
					description: $_('cloudpayments.description'), //назначение
					amount: parseInt($_('cloudpayments.price')), //сумма
					currency: $_('cloudpayments.currency'), //валюта
					accountId: `${user_id}`, //идентификатор плательщика (обязательно для создания подписки)
					requireEmail: false,
					data: data,
					skin: Skins[colorScheme]
				},
				function (options) {
					// success
					Telegram.WebApp.close();
				},
				function (reason, options) {
					// fail
					//действие при неуспешной оплате
				}
			);
		};
		handleClick = function handleClick() {
			pay();
			console.log('helo');
		};
	});
</script>

<!-- App -->
<div class="h-screen w-full select-none text-tg-text">
	<!-- Wrapper -->
	<!-- w-[412px] h-[781px] -->
	<!-- <button on:click={serviceWorkerHandler}>Service worker</button> -->
	<div class=" relative m-auto flex h-screen flex-col bg-tg-bg px-6 pt-0">
		<!-- <div class="flex tracking-wide flex-col w-[412px] h-[781px] bg-tg-bg m-auto px-6 pt-4 relative"> -->
		<!-- Header -->
		<div class="mt-2">
			<!-- <p class="tracking-wider font-extrabold text-2xl leading-8">Go Pro with</p>
			<p class="tracking-wider mt-0 font-extrabold text-2xl leading-8">Change AI</p> -->
			<p class="text-2xl font-extrabold leading-8 tracking-wider">{$_('header.first')}</p>
		</div>
		<!-- Second header -->
		<div class="mt-2 ml-0">
			<p class=" max-w-xs text-sm text-gray-500">
				{$_('header.second')}
			</p>
		</div>

		<!-- Free -->
		<div
			class=" border-[1px] shadow-inner mt-4  flex flex-col  rounded-3xl py-1 px-4  shadow-black/10"
		>
			<p class="m-auto mt-2 mb-2 text-2xl leading-4">{$_('free.title')}</p>
			<ul class="flex flex-col">
				{#each free_options as option}
					<li class="flex items-center">
						<Close
							class="my-auto h-6 w-6 scale-50 text-tg-text [stroke-width:2]"
							fill="currentColor"
							stroke="none"
						/>
						<p class="my-auto ml-2 pb-[1px] text-lg ">{$_(`free.opitons.${option}`)}</p>
					</li>
				{/each}
			</ul>
		</div>
		<div />
		<!-- Pro -->
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			class="mt-4 flex cursor-pointer flex-col rounded-3xl bg-[#2E71FC] py-1 px-4 text-tg-button-text shadow-md shadow-black/50  duration-100 hover:bg-[#2560d7]  hover:shadow-md"
			on:click={handleClick}
		>
			<p class="m-auto mt-2 mb-2 text-2xl leading-4 [word-spacing:-8px]">{$_('pro.title')}</p>
			<ul class="flex flex-col">
				{#each pro_options as option}
					<li class="flex items-center">
						<Check
							class="my-auto	h-6 w-6 scale-90 scale-[.7] text-tg-button-text [stroke-width:2]"
							fill="currentColor"
							stroke="none"
						/>
						<p class="my-auto ml-2  text-lg">{$_(`pro.opitons.${option}`)}</p>
					</li>
				{/each}
			</ul>
		</div>
		<!-- Buy Now -->
		<!-- svelte-ignore a11y-click-events-have-key-events -->
		<div
			on:click={handleClick}
			class="mx-auto mt-4 cursor-pointer rounded-3xl bg-[#2E71FC] shadow-md duration-100  hover:bg-[#2560d7]"
		>
			<div class="flex  w-fit space-y-2   px-6  text-tg-button-text">
				<div class="flex items-center">
					<p class="my-auto pb-[2px]  text-2xl ">{$_('buy_now')}</p>
					<Arrow
						class="ml-4scale-x-[2] h-4 w-6  scale-y-[1.5] pt-[1px]   text-tg-button-text [stroke-width:1]"
						fill="currentColor"
						stroke="none"
					/>
				</div>
			</div>
		</div>

		<!-- assurance -->
		<div class="mx-auto mt-2">
			<div class="flex space-x-1">
				<Lock class="h-4 w-4 text-tg-text [stroke-width:1]" fill="none" stroke="currentColor" />
				<p class="my-auto text-xs">{$_('assurance')}</p>
			</div>
		</div>

		<!-- <button class="btn-primary"></button> -->

		<!-- Footer -->
		<!-- <div class="absolute bottom-2 left-1/2 -translate-x-1/2 w-full">
			<div class="mx-auto align-middle">
				<p class="my-auto w-full text-gray-500 text-[10px]"><a href="">Terms of Service</a> • <a href="">contact@4u studio</a></p>
			</div>
		</div> -->
		<div class="mx-auto mt-auto pt-4">
			<p class="my-auto text-[10px] text-gray-500">
				<a href="https://mdn.github.io/dom-examples/service-worker/simple-service-worker/"
					>Terms of Service</a
				>
				• <a href="@">contact@4u studio</a>
			</p>
		</div>
	</div>
</div>

<!-- Footer -->

<!-- <div class="fixed bottom-2 flex justify-center w-full">
	<p class="my-auto text-gray-500 text-[10px]">
		<a href="">Terms of Service</a> • <a href="">contact@4u studio</a>
	</p>
</div> -->
<style>
	/* .sticky-bottom {
   position: absolute;
   bottom: 0;
   left: 0;
   width: 100%;
} */
	/* @font-face {
	font-family: 'Space Mono Mine';
	font-style: normal;
	src: url('/fonts/SpaceMono-Regular.ttf');
}
p {
	font-family: "Space Mono Mine";
} */
</style>
