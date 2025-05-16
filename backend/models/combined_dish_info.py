from pydantic import BaseModel
from .nutrition import FoodNutrition
from .meal_image import MealImage
from .dish_description import DishDescription

class CombinedDishInfo(BaseModel):
    dish_name: str
    nutrition: FoodNutrition = None
    image: MealImage = None
    description: DishDescription = None