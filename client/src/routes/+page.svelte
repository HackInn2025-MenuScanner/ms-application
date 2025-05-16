<script module lang="ts">
	declare const Tesseract: any;
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, slide } from 'svelte/transition';

	let video: HTMLVideoElement;
	let canvas: HTMLCanvasElement;
	let stream: MediaStream | null = null;
	let capturing = $state(false);

	onMount(async () => {
		// Dynamically load Tesseract script
		const script = document.createElement('script');
		script.src = '/tesseract.min.js';
		script.async = true;
		document.body.appendChild(script);

		try {
			stream = await navigator.mediaDevices.getUserMedia({ video: true });
			if (video) {
				video.srcObject = stream;
				await video.play();
			}
		} catch (err) {
			console.error('Camera access error:', err);
		}

		setTimeout(() => {
			showIntroScreen = false;
		}, 1000);
	});

	async function captureAndRecognize(): Promise<void> {
		showLoader = true;
		if (!canvas || !video) return;
    video.classList.add("blur");
    video.pause();
		capturing = true;

		const ctx = canvas.getContext('2d');
		if (!ctx) {
			console.error('Could not get canvas context');
			capturing = false;
			return;
		}

		canvas.width = video.videoWidth;
		canvas.height = video.videoHeight;
		ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

		try {
			const result = await Tesseract.recognize(applyThreshold(canvas), 'eng', {
				tessedit_pageseg_mode: 9,
				oem: 2
			});
			console.log('OCR Result:', result.data.text);
			//Make api calls
			const res = await fetch('/api/fastapi', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ menu_text: result.data.text, language: 'de' })
			});
			const data = await res.json();

			//Show new Page
			showLoader = false;
			showSelectionScreen = true;
		} catch (error) {
			console.error('OCR failed:', error);
		}

		capturing = false;
	}

	function applyThreshold(canvas: HTMLCanvasElement) {
		const ctx = canvas.getContext('2d');
		if (!ctx) return '';

		const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
		const data = imgData.data;

		const threshold = 128; // Threshold value for binary conversion

		// Apply threshold to each pixel
		for (let i = 0; i < data.length; i += 4) {
			const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
			const color = avg > threshold ? 255 : 0;
			data[i] = data[i + 1] = data[i + 2] = color; // Set R, G, B to the thresholded value
		}

		ctx.putImageData(imgData, 0, 0);

		// Return the thresholded image as a Data URL
		return canvas.toDataURL('image/png');
	}

	let showIntroScreen = $state(true);
	let showSelectionScreen = $state(false);
	let showLoader = $state(false);
</script>

{#if showIntroScreen}
	<div
		class="intro_screen flex h-full w-full items-center justify-center bg-white"
		transition:fade={{ duration: 200 }}
	>
		<div
			class="icon h-62 w-62"
			style="background-image: url('/icons/icon_big.svg');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;"
		></div>
	</div>
{/if}

{#if showSelectionScreen}
	<div
		class="selection_screen z-99999 rounded-t-4xl absolute bottom-0 flex h-[calc(100vh+32px)] w-full items-center justify-center bg-white"
		transition:slide={{ duration: 1000, axis: 'y' }}
	></div>
{/if}

{#if showLoader}
	<div
		class="icon h-25 w-25 z-99999 absolute"
		style="background-image: url(/icons/loader.svg);
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    transform: translate(-50%, -50%);
    top: 50%;
    left: 50%;
    filter: invert(0.8) opacity(0.6);"
	></div>
{/if}

<video class="absolute h-full w-full object-cover" bind:this={video} autoplay playsinline>
	<track kind="captions" />
</video>

<button
	onclick={captureAndRecognize}
	disabled={capturing}
	class="z-9999 absolute bottom-10 left-1/2 m-auto h-14 w-14 -translate-x-1/2 rounded-full border-2 bg-none text-white"
>
	<div class="m-auto h-12 w-12 rounded-full bg-white"></div>
</button>

<canvas bind:this={canvas} style="display: none;"></canvas>
