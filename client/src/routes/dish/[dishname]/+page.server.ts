import { store } from '$lib/store.svelte';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ params, fetch }) => {
    const response = await fetch("/dish/" + params.dishname + "?language=" + store.language, {
        method: "GET"
    });
    //console.log(response)
    //const dishData: {dish_name: string, nutrition: {}, image: {dish_name: string, image_url: string}, description: {}} = await response.json();

    const dishData: {original_name: string, dish_name: string, nutrition: {}, image: {dish_name: string, image_url: string}, description: {}} = {
    "original_name": params.dishname,
    "dish_name": "schnitzel",
    "nutrition": {
        "dish_name": "schnitzel",
        "food_name": "Chicken Schnitzel",
        "food_id": "320553",
        "nutrients": {
        "calories": 297,
        "protein_g": 15.59,
        "fat_g": 18.82,
        "carbs_g": 16.32,
        "fiber_g": 0
        },
        "food_description": "Per 100g - Calories: 297kcal | Fat: 18.82g | Carbs: 16.32g | Protein: 15.59g",
        "food_url": "https://www.fatsecret.com/calories-nutrition/generic/chicken-schnitzel"
    },
    "image": {
        "dish_name": "schnitzel",
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Allg%C3%A4uer%20Schnitzel%20mit%20Kr%C3%A4uterr%C3%B6sti.jpg"
    },
    "description": {
        "dish_name": "schnitzel",
        "description": "Schnitzel is a thin, breaded, and pan-fried cutlet of meat, most commonly veal, pork, or chicken.  Its origins trace back to Austria and Germany, though variations exist across Central Europe.  The precise etymology is debated, but it likely derives from the German word *Schnitzel*, meaning \"slice\" or \"cut\".\n\nPreparation involves pounding the meat very thinly, then dredging it in flour, egg, and breadcrumbs before frying in butter or oil until golden brown and crispy.  Simple seasonings like salt and pepper are typical, but variations include lemon wedges, herbs, and different breading techniques.\n\nCulturally, schnitzel holds a significant place in Austrian and German cuisine, representing a classic comfort food.  It's often served with potato salad, spaetzle, or dumplings, reflecting its hearty nature. While a straightforward dish, its preparation requires skill to achieve the perfect balance of tender meat and crisp breading, making it a symbol of culinary craftsmanship.  Many countries have adopted and adapted it, creating their own regional variations.\n",
        "language": "en"
    }};

	return {
		dishData: dishData
	};
};