<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
    let dishData = data.dishData;


  // Example static rating (1-5) – could be made dynamic later
  const rating = 4;
  const maxStars = 5;
  const stars = Array.from({ length: maxStars }, (_, i) => i < rating);

  console.log(dishData);
  // Extract the first paragraph of the description
  const shortDesc = dishData.description.description.split("\n\n")[0];
</script>
<style>
  .main {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    background: white;
    padding: 1rem;
  }
  .maincontainer {
    width: min(95vw, 600px);
    max-width: 600px;
    margin: 0 24px;
  }
  .image-container {
    width: 100%;
    aspect-ratio: 1 / 1;
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

<div class="main">
    <div class="maincontainer">
        <!-- Back Button -->
         <div class="w-full mb-8">
            <a href="/"><img src="/icons/back.svg" alt="Back"></a>
         </div>

      
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
</div>
