from pydantic import BaseModel

class MealImage(BaseModel):
    dish_name: str
    image_url: str = ""