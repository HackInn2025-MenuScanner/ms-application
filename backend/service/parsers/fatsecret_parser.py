import base64
import os

import httpx
from fastapi import HTTPException

from models import Nutrients, FoodNutrition

FATSECRET_CLIENT_ID = os.getenv("FATSECRET_CLIENT_ID", "")
FATSECRET_CLIENT_SECRET = os.getenv("FATSECRET_CLIENT_SECRET", "")
FATSECRET_API_URL = "https://platform.fatsecret.com/rest/server.api"


async def get_oauth_token() -> str:
    """Get OAuth token for FatSecret API"""
    if not FATSECRET_CLIENT_ID or not FATSECRET_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="FatSecret API credentials not configured"
        )

    credentials = f"{FATSECRET_CLIENT_ID}:{FATSECRET_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "basic"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://oauth.fatsecret.com/connect/token",
            headers=headers,
            data=data
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error getting FatSecret API token: {response.text}"
            )

        return response.json().get("access_token")


async def get_nutrition_facts(dish_name: str) -> FoodNutrition:
    """Get nutrition facts for a dish from FatSecret API"""
    token = await get_oauth_token()

    params = {
        "method": "foods.search",
        "search_expression": dish_name,
        "format": "json",
        "max_results": 1
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            FATSECRET_API_URL,
            params=params,
            headers=headers
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from FatSecret API: {response.text}"
            )

        data = response.json()
        print(data)
        foods = data.get("foods", {}).get("food", [])

        if not foods:
            return {"message": f"No nutrition data found for '{dish_name}'"}

        if isinstance(foods, dict):
            foods = [foods]

        food = foods[0]

        nutrient_str = food.get("food_description", "")

        calories = extract_nutrient(nutrient_str, "Calories", "kcal")
        fat = extract_nutrient(nutrient_str, "Fat", "g")
        carbs = extract_nutrient(nutrient_str, "Carbs", "g")
        protein = extract_nutrient(nutrient_str, "Protein", "g")

        return FoodNutrition(
            dish_name=dish_name,
            food_name=food.get("food_name", dish_name),
            food_id=food.get("food_id", ""),
            nutrients=Nutrients(
                calories=calories,
                protein_g=protein,
                fat_g=fat,
                carbs_g=carbs,
                fiber_g=0.0,
            ),
            food_description=nutrient_str,
            food_url=food.get("food_url", "")
        )


def extract_nutrient(nutrient_str: str, nutrient_name: str, unit: str) -> float:
    """Extract nutrient value from description string"""
    try:
        if nutrient_name in nutrient_str:
            start_idx = nutrient_str.find(nutrient_name) + len(nutrient_name) + 2  # +2 for ": "
            end_idx = nutrient_str.find(unit, start_idx)
            if end_idx > start_idx:
                return float(nutrient_str[start_idx:end_idx])
    except:
        pass
    return 0.0