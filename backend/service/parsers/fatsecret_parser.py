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


async def get_nutrition_from_gemini(dish_name: str) -> FoodNutrition:
    """Get nutrition facts for a dish using Gemini AI when FatSecret fails"""
    from .gemini_parser import GEMINI_API_KEY, GEMINI_API_URL

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured"
        )

    prompt = (
        f"Provide nutrition facts for '{dish_name}'. Include only these values:\n"
        f"- Calories (kcal)\n"
        f"- Protein (g)\n"
        f"- Fat (g)\n"
        f"- Carbs (g)\n"
        f"- Fiber (g)\n\n"
        f"Format your response as follows:\n"
        f"CALORIES: [value]kcal\n"
        f"PROTEIN: [value]g\n"
        f"FAT: [value]g\n"
        f"CARBS: [value]g\n"
        f"FIBER: [value]g\n"
        f"DESCRIPTION: [brief description of the food]\n"
    )

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 300,
            "topP": 0.95
        }
    }

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.post(
            GEMINI_API_URL,
            json=payload,
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Gemini API: {response.text}"
            )

        data = response.json()

        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]

            calories = extract_gemini_nutrient(text, "CALORIES", "kcal")
            protein = extract_gemini_nutrient(text, "PROTEIN", "g")
            fat = extract_gemini_nutrient(text, "FAT", "g")
            carbs = extract_gemini_nutrient(text, "CARBS", "g")
            fiber = extract_gemini_nutrient(text, "FIBER", "g")

            description = ""
            desc_start = text.find("DESCRIPTION:")
            if desc_start != -1:
                description = text[desc_start + len("DESCRIPTION:"):].strip()

            return FoodNutrition(
                dish_name=dish_name,
                food_name=dish_name,
                food_id="gemini_generated",
                nutrients=Nutrients(
                    calories=calories,
                    protein_g=protein,
                    fat_g=fat,
                    carbs_g=carbs,
                    fiber_g=fiber,
                ),
                food_description=description,
                food_url=""
            )

        except (KeyError, IndexError) as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing Gemini response: {str(e)}"
            )


def extract_gemini_nutrient(text: str, nutrient_name: str, unit: str) -> float:
    """Extract nutrient value from Gemini formatted response"""
    try:
        if nutrient_name in text:
            line_start = text.find(nutrient_name)
            line_end = text.find("\n", line_start)
            if line_end == -1:
                line_end = len(text)

            line = text[line_start:line_end]
            value_start = line.find(":") + 1
            value_end = line.find(unit, value_start)

            if value_end > value_start:
                value_str = line[value_start:value_end].strip()
                return float(value_str)
    except:
        pass
    return 0.0


async def get_nutrition_facts(dish_name: str) -> FoodNutrition:
    """Get nutrition facts for a dish from FatSecret API with Gemini fallback"""
    try:
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
                headers=headers,
                timeout=5.0
            )

            if response.status_code != 200:
                return await get_nutrition_from_gemini(dish_name)

            data = response.json()
            foods = data.get("foods", {}).get("food", [])

            if not foods:
                return await get_nutrition_from_gemini(dish_name)

            if isinstance(foods, dict):
                foods = [foods]

            food = foods[0]
            nutrient_str = food.get("food_description", "")

            if not nutrient_str or "Calories" not in nutrient_str:
                return await get_nutrition_from_gemini(dish_name)

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

    except Exception:
        return await get_nutrition_from_gemini(dish_name)


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