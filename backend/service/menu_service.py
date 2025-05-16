import os
import httpx
from fastapi import HTTPException
from models import MenuItems, MenuItem

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"


async def process_menu_text(menu_text: str, language: str = "en") -> MenuItems:
    """
    Process raw menu text to extract and translate dish names using Gemini
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key not configured"
        )

    prompt = (
        f"Below is raw text from a menu (its extracted with OCR, so it could contain some strange characters - therefore extract only the dishes names, that make sence)"
        f". Extract each dish name and translate it to {language}.\n\n"
        f"Raw menu text:\n{menu_text}\n\n"
        f"Format each dish exactly as follows (one per line):\n"
        f"original_name, translated_name\n\n"
        f"Just provide the list with no additional text, explanations, or headers."
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
            "maxOutputTokens": 1000,
            "topK": 40,
            "topP": 0.95
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    params = {
        "key": GEMINI_API_KEY
    }

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
            response_text = data["candidates"][0]["content"]["parts"][0]["text"]
            menu_items = []

            for line in response_text.strip().split('\n'):
                if line and ',' in line:
                    parts = line.split(',', 1)
                    original = parts[0].strip()
                    translated = parts[1].strip()
                    menu_items.append(MenuItem(
                     original_name=original,
                        translated_name=translated
                    ))

            return MenuItems(
                items=menu_items,
            )
        except (KeyError, IndexError) as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing Gemini response: {str(e)}"
            )