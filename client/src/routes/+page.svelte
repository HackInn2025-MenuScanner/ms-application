<script>
  import { onMount } from 'svelte';

  let video;
  let canvas;
  let stream;
  let capturing = $state(false);

  onMount(async () => {
    const script = document.createElement('script');
    script.src = '/tesseract.min.js';
    script.async = true;
    document.body.appendChild(script);

    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: true });
      video.srcObject = stream;
      await video.play();
    } catch (err) {
      console.error('Camera access error:', err);
    }
  });

  async function captureAndRecognize() {
    if (!canvas || !video) return;
    capturing = true;

    const ctx = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw the current frame from the video to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Get image data from canvas
    const dataURL = canvas.toDataURL('image/png');

    console.log('Running OCR...');
    const result = await Tesseract.recognize(dataURL, 'eng', {
      logger: m => console.log(m),
    });

    console.log('OCR Result:', result.data.text);
    capturing = false;
  }
</script>

<video bind:this={video} autoplay playsinline style="width: 100%; max-width: 500px;" >
  <track kind="captions">`
</video>
<br />
<button onclick={captureAndRecognize} disabled={capturing}>
  {capturing ? 'Processing...' : 'Capture & OCR'}
</button>

<canvas bind:this={canvas} style="display: none;"></canvas>
