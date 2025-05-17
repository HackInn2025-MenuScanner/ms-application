<script module lang="ts">
	declare const Tesseract: any;
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { fade, slide } from 'svelte/transition';
  import { store } from "$lib/store.svelte";
  import { apiCall } from "$lib/api";

	let video: HTMLVideoElement;
	let canvas: HTMLCanvasElement;
	let stream: MediaStream | null = null;
	let capturing = $state(false);
  //let data: {original_name: string, translated_name: string}[] = $state([{original_name: "Hühnchen Schnitzel", translated_name: "Chicken Schnitzel"}]);

	onMount(async () => {
		// Dynamically load Tesseract script
		const script = document.createElement('script');
		script.src = '/tesseract.min.js';
		script.async = true;
		document.body.appendChild(script);

		try {
			stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
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

	function changeLanguage(): void {
		showLanguageSelect = !showLanguageSelect;
	}

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
      const res = await apiCall("POST", "/menu/translate", { menu_text: result.data.text, language: store.language });

			store.data = (await res.json()).items;
			showLoader = false;
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
	let showLoader = $state(false);
	let showLanguageSelect = $state(false);

	const langMap = {
		"en-US": "/icons/american.svg",
		"de-DE": "/icons/german.svg",
		"fr-FR": "/icons/french.svg"
	};
</script>

{#if showIntroScreen}
	<div
		class="intro_screen flex h-full w-full items-center justify-center bg-white z-999 absolute"
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

{#if store.data.length}
<style>
  .maincontainer {
    padding: 1rem;
    background: #FFFFFF;
    min-height: 100vh;
    box-sizing: border-box;
	width: 100vw;
  }
  .innercontainer {
	width: min(95vw, 600px);
	max-width: 600px;
    margin: 0 24px;
  }
  .header {
    display: flex;
    align-items: center;
  }
  .back-button {
    width: 2.5rem;
    height: 2.5rem;
    background: #F3C742;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  .title {
    margin: 1rem 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #000000;
  }
  .list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  .card {
    border: 2px solid #F3C742;
    border-radius: 8px;
    padding: 1rem;
  }
  .card-title {
    font-weight: 600;
    font-size: 1.1rem;
    border-bottom: 1px solid #000000;
    padding-bottom: 0.25rem;
    margin-bottom: 0.25rem;
  }
  .card-subtitle {
    font-size: 0.9rem;
    color: #555555;
  }
</style>

<div class="maincontainer absolute z-999999 flex justify-center"
transition:slide={{ duration: 1000, axis: 'y' }}>
  <div class="innercontainer">
	<div class="header">
		<button onclick={() => store.data = []}><img src="/icons/back.svg" alt="Back"></button>
	  </div>
	
	  <h1 class="title">Let's Explore Menu</h1>
	
	  <div class="list">
		{#each store.data as dish}
		  <a class="card" href="/dish/{dish.original_name}">
			<div class="card-title">{dish.original_name}</div>
			<div class="card-subtitle">{dish.translated_name}</div>
		  </a>
		{/each}
	  </div>
  </div>
</div>
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

<video class="absolute h-full w-full object-cover z-9" bind:this={video} autoplay playsinline>
	<track kind="captions"/>
</video>

<div class="absolute top-6 right-6 w-12 h-6 z-10">
	<button onclick={changeLanguage} class="cursor-pointer">
		<div class="w-8 h-8" style="background-image: url({langMap[store.language as "de-de" | "en-us"]})"></div>
		<div class="w-3 h-2 left-9 top-3 absolute {showLanguageSelect ? "-scale-y-100" : ""}">
			<img src="/icons/down_white.svg" alt="">
		</div>
	</button>
	{#if showLanguageSelect}
	<div class="mt-1 w-8 rounded-sm flex flex-col gap-0.5">
		{#each Object.entries(langMap).filter(e => e[0] !== store.language) as [lang, icon]}
		<button class="w-8 h-8 cursor-pointer" style="background-image: url({icon})" class:opacity-50={store.language === lang} onclick={() => {store.language = lang; showLanguageSelect = false;}} aria-label={lang}></button>
		{/each}
	</div>
	{/if}
</div>


<button
	onclick={captureAndRecognize}
	disabled={capturing}
	class="z-9999 absolute bottom-10 left-1/2 m-auto h-14 w-14 -translate-x-1/2 rounded-full border-2 bg-none text-white"
>
	<div class="m-auto h-12 w-12 rounded-full bg-white"></div>
</button>

<canvas bind:this={canvas} style="display: none;"></canvas>
