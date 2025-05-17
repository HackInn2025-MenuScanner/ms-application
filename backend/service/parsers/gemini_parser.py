import os
import httpx
from fastapi import HTTPException
from models import DishDescription

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"


async def get_dish_description(dish_name: str, language: str = "en") -> DishDescription:
    """
    Get dish description and tags using Google's Gemini 1.5 Flash model
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured"
        )

    # Construct the prompt asking for shorter description and tags
    prompt = (
        f"For the dish '{dish_name}', provide TWO things:\n"
        f"1. A SHORT description (maximum 100 words) about its origin, ingredients, and cultural significance.\n"
        f"2. A list of 5-8 tags that describe key aspects of the dish (ingredients, origin, cooking method, dietary info, etc.)\n\n"
        f"Format your response as follows:\n"
        f"DESCRIPTION: [your short description here]\n"
        f"TAGS: [tag1], [tag2], [tag3], etc.\n\n"
        f"Write everything in {language} language."
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
            "temperature": 0.7,
            "maxOutputTokens": 800,
            "topK": 40,
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
        description = ""
        tags = []

        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]

            desc_start = text.find("DESCRIPTION:")
            tags_start = text.find("TAGS:")

            if desc_start != -1 and tags_start != -1:
                description = text[desc_start + len("DESCRIPTION:"):tags_start].strip()
                tags_text = text[tags_start + len("TAGS:"):].strip()
                tags = [tag.strip() for tag in tags_text.split(",") if tag.strip()]
            else:
                description = text[:200] + "..."

        except (KeyError, IndexError):
            description = "No description available."

        return DishDescription(
            dish_name=dish_name,
            description=description,
            tags=tags,
            language=language
        )


async def normalize_dish_name(dish_name: str) -> str:
    """
    Normalize a dish name using Gemini to get a clean version for API searches
    """
    if not GEMINI_API_KEY:
        return dish_name

    prompt = (
        f"I need to search for information about '{dish_name}'. "
        f"Return ONLY a clean normalized version of this dish name with no special characters (like '+') "
        f"and with proper spacing. Just return the name itself with no other text or explanation."
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
            "temperature": 0.1,
            "maxOutputTokens": 50,
            "topP": 0.95
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                GEMINI_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                params={"key": GEMINI_API_KEY}
            )

            if response.status_code != 200:
                return dish_name

            data = response.json()
            normalized = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            normalized = normalized.replace('"', '').replace("'", "").strip()
            return normalized if normalized else dish_name
        except Exception:
            return dish_name