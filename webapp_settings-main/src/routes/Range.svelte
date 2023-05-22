<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { fly, fade } from 'svelte/transition';
	// var Decimal = require('decimal.js-light');
	import Decimal from 'decimal.js-light';
	import { myStore } from './store.js';


	// Props
	export let min: number = 0;
	export let max: number = 100;
	export let initialValue: number = 0;
	export let id: string | null = null;
	export let value: number = typeof initialValue === 'string' ? parseInt(initialValue) : initialValue;
	export let step: number = 1;
	export let storeVariableName: string

	// Node Bindings
	let container: Element | null = null;
	let thumb: Element | null = null;
	let progressBar: Element | null = null;
	let element: Element | null = null;

	// Internal State
	let elementX: number | null | undefined = null;
	let currentThumb: Element | null = null;
	let holding = false;
	let thumbHover = false;
	let keydownAcceleration = 0;

	let accelerationTimer: number | undefined = undefined;

	// Dispatch 'change' events
	const dispatch = createEventDispatcher();

	// Mouse shield used onMouseDown to prevent any mouse events penetrating other elements,
	// ie. hover events on other elements while dragging. Especially for Safari
	const mouseEventShield = document.createElement('div');
	mouseEventShield.setAttribute('class', 'mouse-over-shield');
	mouseEventShield.addEventListener('mouseover', (e) => {
		e.preventDefault();
		e.stopPropagation();
	});

	function resizeWindow() {
		elementX = element?.getBoundingClientRect().left;
	}

	// Allows both bind:value and on:change for parent value retrieval
	function setValue(val: number) {
		value = val;
		dispatch('change', { value });
	}

	function onTrackEvent(e: MouseEvent | TouchEvent) {
		// Update value immediately before beginning drag
		updateValueOnEvent(e as MouseEvent);
		onDragStart(e as MouseEvent);
	}

	// function onHover(e) {
	//   thumbHover = thumbHover ? false : true;
	// }

	function onDragStart(e: MouseEvent) {
		// If mouse event add a pointer events shield
		if (e.type === 'mousedown') document.body.append(mouseEventShield);
		currentThumb = thumb;
	}

	function onDragEnd(e: MouseEvent) {
		// If using mouse - remove pointer event shield
		if (e.type === 'mouseup') {
			if (document.body.contains(mouseEventShield)) document.body.removeChild(mouseEventShield);
			// Needed to check whether thumb and mouse overlap after shield removed
			if (isMouseInElement(e, thumb)) thumbHover = true;
		}
		currentThumb = null;

		myStore.update(store => {
      store.data[storeVariableName] = value;
      return store;
    });
	}

	// Check if mouse event cords overlay with an element's area
	function isMouseInElement(event: MouseEvent, element: Element) {
		let rect = element.getBoundingClientRect();
		let { clientX: x, clientY: y } = event;
		if (x < rect.left || x >= rect.right) return false;
		if (y < rect.top || y >= rect.bottom) return false;
		return true;
	}

	// Accessible keypress handling
	function onKeyPress(e) {
		// Max out at +/- 10 to value per event (50 events / 5)
		// 100 below is to increase the amount of events required to reach max velocity
		if (keydownAcceleration < 50) keydownAcceleration++;
		let throttled = Math.ceil(keydownAcceleration / 5);

		if (e.key === 'ArrowUp' || e.key === 'ArrowRight') {
			if (value + throttled > max || value >= max) {
				setValue(max);
			} else {
				setValue(value + throttled);
			}
		}
		if (e.key === 'ArrowDown' || e.key === 'ArrowLeft') {
			if (value - throttled < min || value <= min) {
				setValue(min);
			} else {
				setValue(value - throttled);
			}
		}

		// Reset acceleration after 100ms of no events
		window.clearTimeout((id = accelerationTimer));
		accelerationTimer = window.setTimeout(() => (keydownAcceleration = 1), 100);
	}

	function roundToStep(num: number, step: number): number {
		const decimalNum = new Decimal(num);
		const decimalStep = new Decimal(step);
		const remainder = decimalNum.mod(decimalStep);
		let rounded = decimalNum.minus(remainder);
		if (remainder.abs().greaterThanOrEqualTo(decimalStep.dividedBy(2))) {
			rounded = rounded.plus(decimalStep);
		}
		return rounded.toNumber();
	}

	function calculateNewValue(clientX: number) {
		// Find distance between cursor and element's left cord (8px / 2 = 10px) - Center of thumb
		if (elementX == null) return;
		let delta: number = clientX - (elementX + 4);

		// Use width of the container minus (5px * 2 sides) offset for percent calc
		if (container === null) return;
		let percent = (delta * 100) / (container.clientWidth - 8);

		// Limit percent 0 -> 100
		percent = percent < 0 ? 0 : percent > 100 ? 100 : percent;

		// Limit value min -> max
		// setValue(parseInt((percent * (max - min)) / 100 + min));
		setValue(roundToStep((percent * (max - min)) / 100 + min, step));
	}

	// Handles both dragging of touch/mouse as well as simple one-off click/touches
	function updateValueOnEvent(e) {
		// e.preventDefault();
		// touchstart && mousedown are one-off updates, otherwise expect a currentPointer node
		if (!currentThumb && e.type !== 'touchstart' && e.type !== 'mousedown') return false;

		if (e.stopPropagation) e.stopPropagation();
		if (e.preventDefault) e.preventDefault();

		// Get client's x cord either touch or mouse
		const clientX = e.type === 'touchmove' || e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;

		calculateNewValue(clientX);

		// console.log("niggas");
	}

	// React to left position of element relative to window
	$: if (element) elementX = element.getBoundingClientRect().left;

	// Set a class based on if dragging
	$: holding = Boolean(currentThumb);

	// Update progressbar and thumb styles to represent value
	$: if (progressBar && thumb) {
		// leftOffset if half of Thumb width
		// rightOffset is how far can Thumb go on the right
		// const leftOffset = -4
		// const rightOffset = 0
		const leftOffset = 0;
		const rightOffset = 8;
		const progressBarOffset = 4;
		// Limit value min -> max
		value = value > min ? value : min;
		value = value < max ? value : max;

		let percent = ((value - min) * 100) / (max - min);
		let offsetLeft = (container.clientWidth - rightOffset) * (percent / 100) + leftOffset;

		// Update thumb position + active range track width
		thumb.style.left = `${offsetLeft}px`;
		progressBar.style.width = `${offsetLeft + progressBarOffset}px`;
	}

	function handleEvent(event) {
		console.log(event.type, event.detail);
	}

	function onSelect(e) {
		console.log(e.type, e.detail);
	}
	// window.addEventListener("*", handleEvent);
	// window.addEventListener("touchmove", function (event) {
	//   let selectStartEvent = new Event("selectstart");
	//   // window.dispatchEvent(selectStartEvent);
	//   console.log("hello");
	//   // const selectStartEvent = new Event("selectstart");
	//   window.dispatchEvent(selectStartEvent);
	// });

	// window.addEventListener("touchstart", function (event) {
	//   // event.preventDefault();
	//   const selectStartEvent = new Event("selectstart");
	//   window.dispatchEvent(selectStartEvent);
	//   console.log('lmao')
	// });

	// window.addEventListener("selectstart", function (event) {
	//   // event.preventDefault();
	//   // const selectStartEvent = new Event("selectstart");
	//   // window.dispatchEvent(selectStartEvent);
	//   console.log('AYOOOO')
	// });
</script>

<!-- on:touchmove|nonpassive={updateValueOnEvent}
  on:touchcancel={onDragEnd}
  on:touchend={onDragEnd}
  on:mousemove={updateValueOnEvent}
  on:mouseup={onDragEnd}
  on:resize={resizeWindow} -->

<svelte:window on:touchmove|nonpassive="{updateValueOnEvent}" on:touchcancel="{onDragEnd}" on:touchend="{onDragEnd}" on:mousemove="{updateValueOnEvent}" on:mouseup="{onDragEnd}" on:resize="{resizeWindow}" />
<div class="range">
	<div class="range__wrapper" tabindex="0" on:keydown="{onKeyPress}" bind:this="{element}" role="slider" aria-valuemin="{min}" aria-valuemax="{max}" aria-valuenow="{value}" id="{id}" on:mousedown="{onTrackEvent}" on:touchstart="{onTrackEvent}">
		<div class="range__track" bind:this="{container}">
			<div class="range__track--highlighted" bind:this="{progressBar}"></div>
			<div class="range__thumb active:scale-125 hover:scale-110 duration-500" class:range__thumb--holding="{holding}" bind:this="{thumb}" on:touchstart="{onDragStart}" on:mousedown="{onDragStart}" on:mouseover="{() => (thumbHover = true)}" on:mouseout="{() => (thumbHover = false)}">
			</div>
		</div>
	</div>
</div>

<svelte:head>
	<style>
		.mouse-over-shield {
			/* position: fixed;
			top: 0px;
			left: 0px;
			height: 100%;
			width: 100%;
			background-color: rgba(255, 0, 0, 0);
			z-index: 10000;
			cursor: grabbing; */
      @apply fixed top-0 left-0 h-0 w-0 bg-transparent z-10 cursor-grabbing;
		}
	</style>
</svelte:head>

<style>
	.range {
		position: relative;
		flex: 1;
	}

	.range__wrapper {
		/* min-width: 100%;
    position: relative;
    padding: 0.5rem;
    box-sizing: border-box;
    outline: none; */
		@apply min-w-full relative py-2 box-border outline-none;
	}

	.range__wrapper:focus-visible > .range__track {
		box-shadow: 0 0 0 2px white, 0 0 0 3px var(--track-focus, #6185ff);
	}

	.range__track {
		/* background-color: var(--track-bgcolor, #d0d0d0); */
    @apply h-[6px] rounded-md bg-tg-hint;
	}

	.range__track--highlighted {
		/* background-color: var(--track-highlight-bgcolor, #6185ff); */
		/* background: var(--track-highlight-bg, linear-gradient(90deg, #6185ff, #9c65ff)); */

    @apply w-0 h-[6px] absolute rounded-sm bg-tg-button;
	}

	.range__thumb {
		/* background-color: var(--thumb-bgcolor, white); */
		transition: box-shadow 100ms;
		box-shadow: var(--thumb-boxshadow, 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 0px 2px 1px rgba(0, 0, 0, 0.2));
		@apply flex items-center justify-center absolute w-2 h-[20px] cursor-pointer rounded-sm -mt-[7px] select-none z-[1000] bg-tg-button-text bg-opacity-50;
	}

	/* .range__thumb--holding {
		box-shadow: 0 1px 1px 0 rgba(0, 0, 0, 0.14), 0 1px 2px 1px rgba(0, 0, 0, 0.2), 0 0 0 6px var(--thumb-holding-outline, rgba(113, 120, 250, 0.638));
	} */
</style>
