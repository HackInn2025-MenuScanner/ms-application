<script module lang="ts">
  // Declare Tesseract globally (e.g., from a <script> tag or external source)
  declare const Tesseract: any;
</script>

<script lang="ts">
  import { onMount } from 'svelte';

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

    console.log('Running OCR...');
    try {
      const result = await Tesseract.recognize(canvas.toDataURL('image/png'), 'eng');
      console.log('OCR Result:', result.data.text);
    } catch (error) {
      console.error('OCR failed:', error);
    }

    capturing = false;
  }
</script>

<video bind:this={video} autoplay playsinline style="width: 100%; max-width: 500px;">
  <track kind="captions" />
</video>

<br/>

<button onclick={captureAndRecognize} disabled={capturing}>
  {capturing ? 'Processing...' : 'Capture & OCR'}
</button>

<canvas bind:this={canvas} style="display: none;"></canvas>
