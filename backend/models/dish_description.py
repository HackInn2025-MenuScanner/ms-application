from pydantic import BaseModel

class DishDescription(BaseModel):
    dish_name: str
    description: str = ""
    language: str = "en"