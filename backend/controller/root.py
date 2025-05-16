from fastapi import APIRouter, HTTPException

from service import get_fatsecret_nutrition_facts

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