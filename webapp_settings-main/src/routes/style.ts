function rbgStringDifference(colorString1: string, colorString2: string): object {
	const colorValues1 = colorString1.match(/\d+/g).map((num) => +num);
	const colorValues2 = colorString2.match(/\d+/g).map((num) => +num);

	const newColorValues = colorValues1.map((value, index) => value - colorValues2[index]);

	const newColorString = { r: newColorValues[0], g: newColorValues[1], b: newColorValues[2] };
	return newColorString;
}

function rgbToHex(r: number, g: number, b: number): string {
	return '#' + ((1 << 24) | (r << 16) | (g << 8) | b).toString(16).slice(1);
}

export function alterSecondaryBg(document: Document) {
	const secondaryBgClass = '.bg-tg-secondary-bg';
	const bgSecondary = document.querySelectorAll(secondaryBgClass);
	const mainColor: string = getComputedStyle(document.querySelector('.bg-tg-bg') as Element).getPropertyValue('background-color');
	console.log(mainColor);

	const [r, g, b] = mainColor.match(/\d+/g).map((num) => +num);

	for (const button of bgSecondary) {
		const secondaryColor: string = getComputedStyle(button).getPropertyValue('background-color');
		console.log(secondaryColor);
		button.classList.remove(secondaryBgClass);

		const diff = rbgStringDifference(secondaryColor, mainColor);

		const sum = Object.values(diff).reduce((acc, value) => acc + value, 0);

		let newColorString = '';
		let newColorHex = '';
		if (sum < 0) {
			newColorString = `rgb(${r - 2 * diff.r}, ${g - 2 * diff.g}, ${b - 2 * diff.b})`;
			newColorHex = rgbToHex(r - 2 * diff.r, g - 2 * diff.g, b - 2 * diff.b);
		} else {
			newColorString = `rgb(${r + diff.r}, ${g + diff.g}, ${b + diff.b})`;
			newColorHex = rgbToHex(r + diff.r, g + diff.g, b + diff.b);
		}

		// console.log(newColorString);
		// (button as HTMLElement).style.setProperty('background-color', newColorString);
		document.documentElement.style.setProperty('--tg-theme-secondary-bg-color', newColorHex);
	}
}

export function alterSecondaryBgFixed(document: Document) {
	const secondaryBgClass = '.bg-tg-secondary-bg';
	const bgSecondary = document.querySelectorAll(secondaryBgClass);
	const mainColor: string = getComputedStyle(document.querySelector('.bg-tg-bg') as Element).getPropertyValue('background-color');
	console.log(mainColor);

	const [r, g, b] = mainColor.match(/\d+/g).map((num) => +num);

	for (const button of bgSecondary) {
		const color: string = getComputedStyle(button).getPropertyValue('background-color');
		console.log(color);
		button.classList.remove(secondaryBgClass);

		const newColorString = `rgb(${r + 11}, ${g + 11}, ${b + 11})`;
		// console.log(newColorString);
		(button as HTMLElement).style.setProperty('background-color', newColorString);
	}
}
