<script lang="ts">
    import { page } from '$app/state';
	import { apiCall } from '$lib/api';
	import { store } from '$lib/store.svelte';

    let dishDataPromise = (async () => {
        const result = await apiCall("GET", "/dish/" + encodeURIComponent(page.params.dishname), { language: store.language });
        const data = await result.json();
        return data;
    })();

  // Example static rating (1-5) – could be made dynamic later
  const rating = 4;
  const maxStars = 5;
  const stars = Array.from({ length: maxStars }, (_, i) => i < rating);


  type SupportedLanguage = 'en-US' | 'de-DE' | 'fr-FR';

  interface Translations {
    calories: string;
    protein: string;
    carbs: string;
    fat: string;
  }

  const translations: Record<SupportedLanguage, Translations> = {
    'en-US': {
      calories: 'Calories',
      protein: 'Protein',
      carbs: 'Carbs',
      fat: 'Fat',
    },
    'de-DE': {
      calories: 'Kalorien',
      protein: 'Protein',
      carbs: 'Kohlenhydrate',
      fat: 'Fett',
    },
    'fr-FR': {
      calories: 'Calories',
      protein: 'Protéines',
      carbs: 'Glucides',
      fat: 'Lipides',
    },
  };
</script>
<style>
  .main {
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    background: white;
    padding: 1rem 1rem 0 1rem;
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
  .nutritionInfo {
    display: flex;
    align-items: center;
    font-size: 0.9rem;
    color: #e64a19;
  }
  .calories::before {
    content: "🔥";
    margin-right: 1px;
  }
  .protein::before {
    content: "🥩";
    margin-right: 1px;
  }
  .fat::before {
    content: "🍔";
    margin-right: 1px;
  }
  .fiber::before {
    content: "🥦";
    margin-right: 1px;
  }
  .carbs::before {
    content: "🍕";
    margin-right: 1px;
  }

  .skeleton {
    background-color: #e0e0e0;
    border-radius: 4px;
    position: relative; /* Added for pseudo-element positioning */
    overflow: hidden; /* Added to clip the pseudo-element */
  }

  .skeleton::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%; /* Start off-screen to the left */
    width: 100%;
    height: 100%;
    background: linear-gradient(to right, transparent 0%, rgba(255, 255, 255, 0.5) 50%, transparent 100%);
    animation: flash 2s linear infinite; /* Apply new animation */
  }

  @keyframes flash {
    0% {
      left: -100%;
    }
    100% {
      left: 100%; /* Move from left to right */
    }
  }

  .skeleton-image {
    width: 100%;
    aspect-ratio: 1 / 1;
    margin-bottom: 0.75rem;
  }

  .skeleton-title {
    width: 70%;
    height: 1.25rem;
    margin-bottom: 0.5rem;
  }

  .skeleton-rating {
    width: 50%;
    height: 1.1rem;
    margin: 0.5rem 0;
  }

  .skeleton-desc {
    width: 90%;
    height: 4rem;
    margin: 0.5rem 0;
  }

  .skeleton-nutrition {
    width: 5rem;
    height: 0.9rem;
    margin-top: 0.75rem;
  }

  .skeleton-tag {
    width: 5rem;
    height: 2rem;
    margin-top: 0.5rem;
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
            {#await dishDataPromise}
                <div class="skeleton skeleton-image"></div>
            {:then dishData} 
                <img src="{dishData.image.image_url}" alt="{dishData.dish_name}" />
            {/await}
        </div>
      
        <!-- Dish Name -->
        {#await dishDataPromise}
            <div class="skeleton skeleton-title"></div>
        {:then dishData} 
            <h2>{dishData.dish_name}</h2>
        {/await}
      
        <!-- Star Rating -->
        <div class="rating">
            {#await dishDataPromise}
                <div class="skeleton skeleton-rating"></div>
            {:then} 
                {#each stars as full, idx}
                    <span class="star">{full ? '★' : '☆'}</span>
                {/each}
            {/await}
        </div>

        <!-- Tags -->
        <div class="flex gap-2 flex-wrap">
            {#await dishDataPromise}
                {#each { length: 4 }}
                    <div class="skeleton skeleton-tag"></div>
                {/each}
            {:then dishData} 
                {#each dishData.description.tags as tag}
                    <span class="p-1 border border-gray-600 rounded-md text-sm text-gray-600">{tag}</span>
                {/each}
            {/await}
        </div>
      
        <!-- Short Description -->
        {#await dishDataPromise}
            <div class="skeleton skeleton-desc h-6"></div>
        {:then dishData} 
            <p class="desc">{dishData.description.description.split("\n\n")[0]}</p>
        {/await}
      
        <div class="sticky bottom-0 pb-4 bg-white shadow-[0_-4px_6px_3px_white]">
          <hr />
          <div class="flex flex-wrap gap-4">
            <!-- Calorie Info -->
            {#await dishDataPromise}
            <div class="skeleton skeleton-nutrition"></div>
            {:then dishData}
            <div class="nutritionInfo calories">{dishData.nutrition.nutrients.calories} {translations[store.language as SupportedLanguage].calories}</div>
            {/await}
  
            <!-- Protein Info -->
            {#await dishDataPromise}
              <div class="skeleton skeleton-nutrition"></div>
            {:then dishData}
              <div class="nutritionInfo protein">{dishData.nutrition.nutrients.protein_g} {translations[store.language as SupportedLanguage].protein}</div>
            {/await}
  
            <!-- Carbs -->
            {#await dishDataPromise}
              <div class="skeleton skeleton-nutrition"></div>
            {:then dishData}
              <div class="nutritionInfo carbs">{dishData.nutrition.nutrients.carbs_g} {translations[store.language as SupportedLanguage].carbs}</div>
            {/await}
  
            <!-- Fat -->
            {#await dishDataPromise}
              <div class="skeleton skeleton-nutrition"></div>
            {:then dishData}
              <div class="nutritionInfo fat">{dishData.nutrition.nutrients.fat_g} {translations[store.language as SupportedLanguage].fat}</div>
            {/await}
          </div>
      </div>
    </div>
</div>
