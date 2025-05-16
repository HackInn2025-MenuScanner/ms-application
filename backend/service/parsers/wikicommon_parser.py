import httpx
from fastapi import HTTPException
from models import MealImage
import urllib.parse


async def get_food_image(dish_name: str) -> MealImage:
    """
    Get food image URL for a dish from Wikimedia Commons
    """
    base_url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "list": "search",
        "srsearch": f"{dish_name} food",
        "format": "json",
        "srnamespace": 6,
        "srlimit": 1
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error from Wikimedia Commons API: {response.text}"
            )

        data = response.json()
        search_results = data.get("query", {}).get("search", [])

        image_url = ""
        if search_results:
            title = search_results[0].get("title", "")
            if title.startswith("File:"):
                file_name = title[5:]
                encoded_file_name = urllib.parse.quote(file_name)
                image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded_file_name}"

        return MealImage(
            dish_name=dish_name,
            image_url=image_url
        )