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

		if (!canvas || !video) return;
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
			const result = await Tesseract.recognize(canvas.toDataURL('image/png'), 'eng');
			console.log('OCR Result:', result.data.text);
      //Make api calls

      //Show new Page
      showSelectionScreen = true;

		} catch (error) {
			console.error('OCR failed:', error);
		}

		capturing = false;
	}

  let showIntroScreen = $state(true);
  let showSelectionScreen = $state(false)
</script>

{#if showIntroScreen}
<div
	class="intro_screen h-full w-full bg-white flex justify-center items-center"
  transition:fade={{duration: 200}}
>
	<div
		class="icon"
		style="background-image: url('/icons/icon_big.svg');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    height: 300px;
    width: 300px;"
	></div>
</div>
{/if}

{#if showSelectionScreen}
<div
	class="selection_screen h-[calc(100vh+32px)] w-full bg-white flex justify-center items-center bottom-0 absolute z-99999 rounded-t-4xl"
  transition:slide={{duration: 1000, axis: 'y'}}
>
</div>
{/if}

<video class="w-full h-full absolute object-cover" bind:this={video} autoplay playsinline>
	<track kind="captions" />
</video>

<button onclick={captureAndRecognize} disabled={capturing} class="z-9999 m-auto border-2 text-white w-14 h-14 bg-none rounded-full left-1/2 -translate-x-1/2 bottom-10 absolute">
  <div class="w-12 h-12 bg-white rounded-full m-auto"></div>
</button>

<canvas bind:this={canvas} style="display: none;"></canvas>