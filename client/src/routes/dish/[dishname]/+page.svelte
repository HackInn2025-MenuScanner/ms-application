<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
    let dishData = data.dishData;
</script>

<a href="/">Back</a>
<h1>Dish {dishData.original_name}</h1>
<div class="flex h-full w-full items-center justify-center bg-white z-999999 absolute">
    <img src={dishData.image.image_url} class="w-10 h-10" alt="">
</div>