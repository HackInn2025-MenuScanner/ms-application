from fastapi import APIRouter, HTTPException

from service import get_fatsecret_nutrition_facts, get_themealdb_food_image, get_gemini_dish_description

router = APIRouter()

@router.get("/")
async def root():
    print("sfksjfklsdjf")
    return {"message": "Hello World"}

@router.get("/fatsecret/{dish_name}")
async def get_fatsecret_data(dish_name: str):
    """
    Get nutrition information for a dish from FatSecret API
    """
    try:
        print("Get nutrition information for dish", dish_name)
        nutrition_data = await get_fatsecret_nutrition_facts(dish_name)
        return nutrition_data
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving nutrition data: {str(e)}"
        )

@router.get("/wikicommon/image/{dish_name}")
async def get_meal_image(dish_name: str):
    """
    Get a food image URL from TheMealDB API
    """
    try:
        return await get_themealdb_food_image(dish_name)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving food image: {str(e)}"
        )

@router.get("/gemini/description/{dish_name}")
async def get_dish_description(dish_name: str, language: str = "en"):
    """
    Get dish description using Google's Gemini 1.5 Flash model
    """
    try:
        return await get_gemini_dish_description(dish_name, language)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving dish description: {str(e)}"
        )