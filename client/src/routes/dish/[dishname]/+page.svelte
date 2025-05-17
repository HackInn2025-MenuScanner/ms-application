<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
    let dishData = data.dishData;


  // Example static rating (1-5) – could be made dynamic later
  const rating = 4;
  const maxStars = 5;
  const stars = Array.from({ length: maxStars }, (_, i) => i < rating);

  // Extract the first paragraph of the description
  const shortDesc = dishData.description.description.split("\n\n")[0];
</script>
<a href="/">Back</a>
<style>
  .card {
    width: 360px;
    margin: 1rem auto;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 1rem;
    font-family: system-ui, sans-serif;
  }
  .back {
    background: #ffca28;
    border: none;
    border-radius: 50%;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    margin-bottom: 0.5rem;
  }
  .back:hover {
    background: #ffc107;
  }
  .image-container {
    width: 100%;
    height: 200px;
    overflow: hidden;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin-bottom: 0.75rem;
  }
  .image-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  h2 {
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
  }
  .rating {
    margin: 0.5rem 0;
    color: #fbc02d;
    font-size: 1.1rem;
  }
  .rating .star {
    margin-right: 2px;
  }
  .desc {
    font-size: 0.9rem;
    color: #555;
    margin: 0.5rem 0;
  }
  hr {
    border: none;
    border-top: 1px solid #eee;
    margin: 0.75rem 0;
  }
  .calories {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
    color: #e64a19;
  }
  .calories::before {
    content: "🔥";
    margin-right: 0.5rem;
  }
</style>

<div class="card">
  <!-- Back Button -->
  <button class="back" aria-label="Go back" on:click={() => history.back()}>&larr;</button>

  <!-- Dish Image -->
  <div class="image-container">
    <img src="{dishData.image.image_url}" alt="{dishData.dish_name}" />
  </div>

  <!-- Dish Name -->
  <h2>{dishData.dish_name}</h2>

  <!-- Star Rating -->
  <div class="rating">
    {#each stars as full, idx}
      <span class="star">{full ? '★' : '☆'}</span>
    {/each}
  </div>

  <!-- Short Description -->
  <p class="desc">{shortDesc}</p>

  <hr />

  <!-- Calorie Info -->
  <div class="calories">{dishData.nutrition.nutrients.calories} Calories</div>
</div>