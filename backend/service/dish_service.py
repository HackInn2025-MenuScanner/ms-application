import asyncio
from models import CombinedDishInfo
from .parsers import get_nutrition_facts, get_food_image, get_dish_description


async def get_combined_dish_info(dish_name: str, language: str = "en") -> CombinedDishInfo:
    """
    Fetch combined dish information from all parsers (nutrition, image, description)
    """
    nutrition_task = asyncio.create_task(get_nutrition_facts(dish_name))
    image_task = asyncio.create_task(get_food_image(dish_name))
    description_task = asyncio.create_task(get_dish_description(dish_name, language))

    nutrition = await nutrition_task
    image = await image_task
    description = await description_task

    return CombinedDishInfo(
        dish_name=dish_name,
        nutrition=nutrition,
        image=image,
        description=description
    )